import pandas as pd
from pathlib import Path
import re
import json

BASE = Path("data/processed")
OUT = BASE / "audit_reports"
OUT.mkdir(parents=True, exist_ok=True)

ANNOTATIONS = BASE / "annotations_all.csv"
LANGUAGE_REVIEW = BASE / "romanized_language_review.csv"

if not ANNOTATIONS.exists():
    raise FileNotFoundError(ANNOTATIONS)

df = pd.read_csv(ANNOTATIONS, keep_default_na=False)

print("\n========== FULL DATASET AUDIT ==========")
print("Total records:", len(df))
print("Columns:", list(df.columns))

reports = {}

def save_report(name, data):
    path = OUT / f"{name}.csv"
    data.to_csv(path, index=False)
    reports[name] = len(data)
    print(f"Saved: {path} ({len(data)} records)")

def normalized_text(value):
    value = str(value).lower().strip()
    return re.sub(r"\s+", " ", value)

# 1. Missing values
print("\n========== MISSING VALUES ==========")

important_columns = [
    "comment_id",
    "comment_text",
    "relevance",
    "stance",
    "confirmed_language"
]

available = [c for c in important_columns if c in df.columns]

missing_rows = df[
    df[available].apply(
        lambda row: any(str(v).strip() == "" for v in row),
        axis=1
    )
].copy()

save_report("missing_values", missing_rows)

for col in available:
    count = (df[col].astype(str).str.strip() == "").sum()
    print(f"{col}: {count} missing")

# 2. Duplicate IDs
print("\n========== DUPLICATE COMMENT IDS ==========")

duplicate_ids = df[
    df["comment_id"].duplicated(keep=False)
].sort_values("comment_id")

save_report("duplicate_comment_ids", duplicate_ids)

# 3. Duplicate text
print("\n========== DUPLICATE COMMENT TEXT ==========")

df["_normalized_text"] = df["comment_text"].apply(normalized_text)

duplicate_text = df[
    df["_normalized_text"].duplicated(keep=False)
].sort_values("_normalized_text")

save_report(
    "duplicate_comment_text",
    duplicate_text.drop(columns=["_normalized_text"])
)

# 4. Label distributions
print("\n========== RELEVANCE DISTRIBUTION ==========")

if "relevance" in df.columns:
    print(df["relevance"].value_counts(dropna=False).to_string())

    valid_relevance = {"Relevant", "Irrelevant", "Uncertain"}
    invalid = df[~df["relevance"].isin(valid_relevance)]
    save_report("invalid_relevance_labels", invalid)

print("\n========== STANCE DISTRIBUTION ==========")

if "stance" in df.columns:
    print(df["stance"].value_counts(dropna=False).to_string())

    valid_stance = {"Favour", "Against", "None"}
    invalid = df[~df["stance"].isin(valid_stance)]
    save_report("invalid_stance_labels", invalid)

# 5. Stance by relevance
print("\n========== STANCE BY RELEVANCE ==========")

if {"relevance", "stance"}.issubset(df.columns):
    cross = pd.crosstab(
        df["relevance"],
        df["stance"],
        margins=True
    )
    print(cross.to_string())
    cross.to_csv(OUT / "stance_by_relevance.csv")

    # These are records to inspect, not automatically incorrect.
    conflicts = df[
        (df["relevance"] == "Irrelevant") &
        (df["stance"] != "None")
    ]
    save_report("relevance_stance_conflicts", conflicts)

# 6. Language distribution
print("\n========== LANGUAGE DISTRIBUTION ==========")

if "confirmed_language" in df.columns:
    print(
        df["confirmed_language"]
        .value_counts(dropna=False)
        .to_string()
    )

    if "relevance" in df.columns:
        relevant = df[df["relevance"] == "Relevant"]
        print("\nRelevant comments by language:")
        print(
            relevant["confirmed_language"]
            .value_counts(dropna=False)
            .to_string()
        )

# 7. Annotation status
print("\n========== ANNOTATION STATUS ==========")

for col in ["relevance_status", "stance_status"]:
    if col in df.columns:
        print(f"\n{col}:")
        print(df[col].value_counts(dropna=False).to_string())

# 8. Verify the 104 language review records
print("\n========== LANGUAGE REVIEW CROSS-CHECK ==========")

if LANGUAGE_REVIEW.exists():
    review = pd.read_csv(LANGUAGE_REVIEW, keep_default_na=False)

    merged = review.merge(
        df[["comment_id", "stance"]],
        on="comment_id",
        how="left",
        suffixes=("_review", "_annotation"),
        indicator=True
    )

    merged["stance_matches"] = (
        merged["stance_review"] == merged["stance_annotation"]
    )

    print("Review records:", len(review))
    print("Missing from annotations:", (merged["_merge"] != "both").sum())
    print("Stance mismatches:", (~merged["stance_matches"]).sum())

    save_report(
        "language_review_crosscheck",
        merged
    )

    print("\nVerified language distribution:")
    print(
        review["verified_language"]
        .value_counts(dropna=False)
        .to_string()
    )

else:
    print("Language review file not found.")

# 9. Summary
summary = {
    "total_annotations": len(df),
    "unique_comment_ids": int(df["comment_id"].nunique()),
    "duplicate_comment_ids": int(df["comment_id"].duplicated().sum()),
    "duplicate_text_records": len(duplicate_text),
    "missing_value_records": len(missing_rows),
    "relevant_comments": int(
        (df["relevance"] == "Relevant").sum()
    ) if "relevance" in df.columns else None,
    "irrelevant_comments": int(
        (df["relevance"] == "Irrelevant").sum()
    ) if "relevance" in df.columns else None,
    "uncertain_comments": int(
        (df["relevance"] == "Uncertain").sum()
    ) if "relevance" in df.columns else None,
    "stance_distribution": (
        df["stance"].value_counts().to_dict()
        if "stance" in df.columns else {}
    ),
    "reports_generated": reports
}

summary_path = OUT / "audit_summary.json"

with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=4, ensure_ascii=False)

print("\n========== AUDIT COMPLETE ==========")
print(json.dumps(summary, indent=4, ensure_ascii=False))
print("\nAll reports saved in:", OUT)
print("No original dataset files were modified.")
