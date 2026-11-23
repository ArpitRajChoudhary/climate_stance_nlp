import pandas as pd
from pathlib import Path

review_path = Path("data/processed/romanized_language_review.csv")
annotations_path = Path("data/processed/annotations_all.csv")
backup_path = Path(
    "data/processed/romanized_language_review_backup_20261123_002159.csv"
)

review = pd.read_csv(review_path, keep_default_na=False)
annotations = pd.read_csv(annotations_path, keep_default_na=False)
backup = pd.read_csv(backup_path, keep_default_na=False)

print("\n========== BASIC CHECKS ==========")
print("Review records:", len(review))
print("Consolidated annotation records:", len(annotations))
print("Unique review comment IDs:", review["comment_id"].nunique())

print("\n========== LANGUAGE DISTRIBUTION ==========")
print(review["verified_language"].value_counts().to_string())

print("\n========== STANCE DISTRIBUTION ==========")
print(review["stance"].value_counts(dropna=False).to_string())

# Check missing IDs in consolidated annotations
review_ids = set(review["comment_id"])
annotation_ids = set(annotations["comment_id"])

missing_ids = review_ids - annotation_ids
print("\n========== COMMENT ID MATCH ==========")
print("Review IDs missing from annotations_all:", len(missing_ids))

if missing_ids:
    print("Missing IDs:", list(missing_ids)[:10])

# Compare stance labels with consolidated annotations
merged = review[["comment_id", "stance"]].merge(
    annotations[["comment_id", "stance"]],
    on="comment_id",
    how="left",
    suffixes=("_review", "_original"),
    indicator=True
)

mismatches = merged[
    (merged["_merge"] != "both") |
    (merged["stance_review"] != merged["stance_original"])
]

print("\n========== STANCE PRESERVATION ==========")
print("Stance mismatches:", len(mismatches))

if not mismatches.empty:
    print(mismatches.to_string(index=False))
else:
    print("All stance labels match annotations_all.csv.")

# Compare against backup
backup_check = review[
    ["comment_id", "stance"]
].merge(
    backup[["comment_id", "stance"]],
    on="comment_id",
    how="outer",
    suffixes=("_updated", "_backup"),
    indicator=True
)

backup_mismatches = backup_check[
    (backup_check["_merge"] != "both") |
    (backup_check["stance_updated"] != backup_check["stance_backup"])
]

print("\n========== BACKUP COMPARISON ==========")
print("Original stance differences:", len(backup_mismatches))

# Check duplicate IDs and comment text
print("\n========== DUPLICATE CHECK ==========")
print("Duplicate comment IDs:", review["comment_id"].duplicated().sum())

duplicate_text = review[
    review["comment_text"].duplicated(keep=False)
].sort_values("comment_text")

print("Records involved in duplicate text:", len(duplicate_text))

if not duplicate_text.empty:
    print("\nDuplicate comment entries:")
    print(
        duplicate_text[
            ["review_number", "comment_id", "stance", "comment_text"]
        ].to_string(index=False)
    )

print("\n========== FINAL AUDIT STATUS ==========")

checks = {
    "104 review records": len(review) == 104,
    "All language labels populated": review["verified_language"].ne("").all(),
    "No duplicate comment IDs": review["comment_id"].is_unique,
    "All IDs found in consolidated annotations": len(missing_ids) == 0,
    "Stance labels match consolidated annotations": len(mismatches) == 0,
    "Stance labels match backup": len(backup_mismatches) == 0,
}

for name, passed in checks.items():
    print(f"{'PASS' if passed else 'CHECK'}: {name}")

print("\nNo files were modified by this audit.")
