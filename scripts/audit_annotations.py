import pandas as pd
from pathlib import Path

base = Path("data/processed")
frames = []

expected_columns = {
    "comment_id",
    "comment_text",
    "relevance",
    "confirmed_language",
    "stance",
}

for batch_num in range(1, 14):
    path = base / f"annotation_batch_{batch_num:02d}.csv"

    if not path.exists():
        raise FileNotFoundError(f"Missing batch: {path}")

    df = pd.read_csv(path, keep_default_na=False)

    expected_rows = 11 if batch_num == 13 else 50

    if len(df) != expected_rows:
        raise ValueError(
            f"Batch {batch_num:02d}: expected {expected_rows} rows, "
            f"found {len(df)}"
        )

    missing_columns = expected_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Batch {batch_num:02d} missing columns: {missing_columns}"
        )

    df["batch_number"] = batch_num
    frames.append(df)

all_df = pd.concat(frames, ignore_index=True)

print("=" * 55)
print("ANNOTATION AUDIT")
print("=" * 55)

print("\nTotal comments:", len(all_df))
print("Total batches:", len(frames))

print("\nExpected total: 611")
print("Actual total:", len(all_df))

if len(all_df) != 611:
    raise ValueError("Total annotation count does not match 611.")

print("\nDuplicate comment IDs:")
print(all_df["comment_id"].duplicated().sum())

print("\nMissing annotation values:")
for col in ["relevance", "confirmed_language", "stance"]:
    missing = (all_df[col].str.strip() == "").sum()
    print(f"{col}: {missing}")

print("\nRelevance distribution:")
print(all_df["relevance"].value_counts(dropna=False))

print("\nLanguage distribution:")
print(all_df["confirmed_language"].value_counts(dropna=False))

print("\nStance distribution:")
print(all_df["stance"].value_counts(dropna=False))

print("\nStance by relevance:")
print(pd.crosstab(all_df["relevance"], all_df["stance"]))

print("\nLanguage by relevance:")
print(pd.crosstab(all_df["relevance"], all_df["confirmed_language"]))

print("\nAnnotation status:")
for col in [
    "relevance_status",
    "language_review_status",
    "stance_status",
]:
    if col in all_df.columns:
        print(f"\n{col}:")
        print(all_df[col].value_counts(dropna=False))

# Check allowed labels
allowed = {
    "relevance": {"Relevant", "Irrelevant", "Uncertain"},
    "stance": {"Favour", "Against", "None"},
}

for col, valid_values in allowed.items():
    invalid = sorted(set(all_df[col]) - valid_values)
    if invalid:
        raise ValueError(f"Invalid values in {col}: {invalid}")

output = base / "annotations_all.csv"
all_df.to_csv(output, index=False)

print("\nAudit file saved:", output)
print("\nAUDIT SCRIPT COMPLETED.")
