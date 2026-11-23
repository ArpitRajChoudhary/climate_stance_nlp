import pandas as pd
from pathlib import Path

BASE = Path("data/processed")

annotations_path = BASE / "annotations_all.csv"
language_path = BASE / "romanized_language_review.csv"
overrides_path = BASE / "adjudication_overrides.csv"
output_path = BASE / "annotations_working.csv"

annotations = pd.read_csv(annotations_path, keep_default_na=False)
languages = pd.read_csv(language_path, keep_default_na=False)
overrides = pd.read_csv(overrides_path, keep_default_na=False)

if len(annotations) != 611:
    raise ValueError("Unexpected annotation record count.")
if len(languages) != 104:
    raise ValueError("Expected 104 reviewed language records.")
if len(overrides) != 2:
    raise ValueError("Expected two relevance overrides.")

if annotations["comment_id"].duplicated().any():
    raise ValueError("Duplicate annotation IDs.")
if languages["comment_id"].duplicated().any():
    raise ValueError("Duplicate language-review IDs.")
if overrides["comment_id"].duplicated().any():
    raise ValueError("Duplicate override IDs.")

working = annotations.copy()

working["model_language"] = working["confirmed_language"]
working["language_review_status_final"] = "OriginalProvisional"
working["relevance_final"] = working["relevance"]
working["relevance_review_status_final"] = "OriginalProvisional"
working["stance_final"] = working["stance"]

language_map = languages.set_index("comment_id")["verified_language"]
working["model_language"] = working["comment_id"].map(language_map).fillna(
    working["model_language"]
)

reviewed_ids = set(languages["comment_id"])
working.loc[
    working["comment_id"].isin(reviewed_ids),
    "language_review_status_final"
] = "AssistantReviewed_PendingValidation"

override_map = overrides.set_index("comment_id")["relevance_override"]
working["relevance_final"] = working["comment_id"].map(override_map).fillna(
    working["relevance_final"]
)

override_ids = set(overrides["comment_id"])
working.loc[
    working["comment_id"].isin(override_ids),
    "relevance_review_status_final"
] = "Proposed_Manual_Adjudication"

if not working["stance"].equals(working["stance_final"]):
    raise ValueError("Stance labels unexpectedly changed.")

working.to_csv(output_path, index=False)

check = pd.read_csv(output_path, keep_default_na=False)

assert len(check) == 611
assert check["comment_id"].is_unique
assert check["model_language"].ne("").all()
assert check["relevance_final"].ne("").all()
assert check["stance_final"].equals(check["stance"])
assert (
    check["language_review_status_final"]
    == "AssistantReviewed_PendingValidation"
).sum() == 104
assert (
    check["relevance_review_status_final"]
    == "Proposed_Manual_Adjudication"
).sum() == 2

print("\nWORKING ANNOTATIONS CREATED")
print("===========================")
print("Total records:", len(check))
print("Language decisions applied:", len(reviewed_ids))
print("Proposed relevance corrections:", len(override_ids))
print("Original stance labels preserved: YES")

print("\nFinal working language distribution:")
print(check["model_language"].value_counts().to_string())

print("\nFinal working relevance distribution:")
print(check["relevance_final"].value_counts().to_string())

print("\nStance distribution among currently relevant records:")
relevant = check[check["relevance_final"] == "Relevant"]
print(relevant["stance_final"].value_counts().to_string())

print("\nSaved to:", output_path)
print("Original annotation files were not modified.")
