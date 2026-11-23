import re
import pandas as pd
from pathlib import Path

ROUND1 = Path("data/processed/annotations_working.csv")
ROUND2 = Path("data/processed/round2_annotated_assisted.csv")
OUTPUT = Path("data/final/climate_stance_dataset.csv")
EXCLUDED = Path("data/final/excluded_comments.csv")

VALID_STANCES = {"Favour", "Against", "None"}

def read_csv(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return pd.read_csv(path, keep_default_na=False)

def normalize_text(text):
    text = str(text).lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text

def normalize_round1(df):
    return pd.DataFrame({
        "comment_id": df["comment_id"],
        "video_id": df["video_id"],
        "comment_text": df["comment_text"],
        "language": df["model_language"],
        "relevance": df["relevance_final"],
        "stance": df["stance_final"],
        "source": "Round1"
    })

def normalize_round2(df):
    return pd.DataFrame({
        "comment_id": df["comment_id"],
        "video_id": df["video_id"],
        "comment_text": df["comment_text"],
        "language": df["language_final"],
        "relevance": df["relevance_final"],
        "stance": df["stance_final"],
        "source": "Round2"
    })

r1 = normalize_round1(read_csv(ROUND1))
r2 = normalize_round2(read_csv(ROUND2))

combined = pd.concat([r1, r2], ignore_index=True)

# Keep only Hindi/Bengali-family comments.
target_languages = {
    "Hindi", "Hindi_Romanized", "Hinglish",
    "Bengali", "Bengali_Romanized"
}

# Keep only relevant comments with an assigned target stance.
usable = combined[
    combined["relevance"].eq("Relevant")
    & combined["stance"].isin(VALID_STANCES)
    & combined["language"].isin(target_languages)
    & combined["comment_text"].str.strip().ne("")
].copy()

# Normalize text for duplicate detection.
usable["normalized_text"] = usable["comment_text"].map(normalize_text)

# If identical text has conflicting stance labels, exclude the entire group.
conflicts = (
    usable.groupby("normalized_text")["stance"]
    .nunique()
)
conflicting_texts = set(conflicts[conflicts > 1].index)

conflict_rows = usable[
    usable["normalized_text"].isin(conflicting_texts)
].copy()

usable = usable[
    ~usable["normalized_text"].isin(conflicting_texts)
].copy()

# Remove exact normalized-text duplicates, keeping the first occurrence.
usable = usable.drop_duplicates(
    subset=["normalized_text"],
    keep="first"
).copy()

# Save excluded conflicting examples for transparency.
if not conflict_rows.empty:
    conflict_rows["exclusion_reason"] = "Conflicting stance labels for identical text"

conflict_rows.to_csv(EXCLUDED, index=False)

usable = usable.drop(columns=["normalized_text"])
usable = usable.reset_index(drop=True)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
usable.to_csv(OUTPUT, index=False)

print("\n========== FINAL DATASET PREPARATION ==========")
print("Round 1 records:", len(r1))
print("Round 2 records:", len(r2))
print("Combined records:", len(combined))
print("Usable records:", len(usable))
print("Conflicting duplicate records excluded:", len(conflict_rows))
print("Output:", OUTPUT)

print("\nStance distribution:")
print(usable["stance"].value_counts())

print("\nLanguage distribution:")
print(usable["language"].value_counts())

print("\nSource distribution:")
print(usable["source"].value_counts())

print("\nVideo distribution:")
print(usable.groupby("video_id").size().sort_values(ascending=False))

print("\nUnique videos:", usable["video_id"].nunique())
print("Duplicate comment IDs:", usable["comment_id"].duplicated().sum())
print("\nDataset saved successfully.")
