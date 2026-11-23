import pandas as pd
from pathlib import Path

base = Path("data/processed")

status_columns = [
    "relevance_status",
    "language_review_status",
    "stance_status",
]

label_columns = [
    "relevance",
    "confirmed_language",
    "stance",
]

files = [
    base / f"annotation_batch_{i:02d}.csv"
    for i in range(1, 14)
]

files.append(base / "annotations_all.csv")

for path in files:
    if not path.exists():
        raise FileNotFoundError(path)

    df = pd.read_csv(path, keep_default_na=False)

    # Ensure annotation labels exist before changing status.
    for col in label_columns:
        if col not in df.columns:
            raise ValueError(f"{path}: Missing column {col}")

        if (df[col].str.strip() == "").any():
            raise ValueError(f"{path}: Empty values found in {col}")

    # Change status metadata only.
    for col in status_columns:
        df[col] = "Provisional"

    df.to_csv(path, index=False)
    print(f"Updated: {path}")

print("\nAll annotation status columns updated.")
print("No annotation labels were modified.")
