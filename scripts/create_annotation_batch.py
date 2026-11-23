
import pandas as pd
from pathlib import Path
import argparse

INPUT = Path("data/processed/relevance_review.csv")
OUTPUT_DIR = Path("data/processed")

BATCH_SIZE = 50

parser = argparse.ArgumentParser()
parser.add_argument(
    "--batch",
    type=int,
    required=True,
    help="Batch number, starting from 1"
)
args = parser.parse_args()

if args.batch < 1:
    raise ValueError("Batch number must be at least 1.")

df = pd.read_csv(INPUT)

# Stable ordering so batches remain consistent.
df = df.sort_values(
    ["video_id", "comment_id"]
).reset_index(drop=True)

# Calculate the rows belonging to this batch.
start = (args.batch - 1) * BATCH_SIZE
end = start + BATCH_SIZE

batch = df.iloc[start:end].copy()

if batch.empty:
    print("No comments available for this batch.")
    raise SystemExit(0)

# Initialize annotation columns as text.
for column in [
    "relevance",
    "confirmed_language",
    "stance",
    "annotation_notes",
]:
    batch[column] = ""

batch["annotation_status"] = "Pending"

OUTPUT = OUTPUT_DIR / f"annotation_batch_{args.batch:02d}.csv"

# Never overwrite an existing batch.
if OUTPUT.exists():
    print(f"Batch already exists: {OUTPUT}")
    print("Existing annotations were not changed.")
    raise SystemExit(1)

batch.to_csv(OUTPUT, index=False)

print(f"Batch {args.batch:02d} created.")
print("Comments:", len(batch))
print("Videos:", batch["video_id"].nunique())
print("Output:", OUTPUT)
