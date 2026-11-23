import pandas as pd
from pathlib import Path

INPUT = "data/processed/language_review.csv"
OUTPUT = "data/processed/relevance_review.csv"

PRIORITY_VIDEOS = {
    # Hindi
    "XXPsWK-FHLI",
    "u_ISqc75exM",
    "JuuAvH830dk",
    "T6ydzaAPfT0",
    "5MR3bxWL36c",
    "QRD8TtrcA7k",
    "k01jpKF44N0",

    # Bengali
    "Q5iZ8mE17Qc",
    "p8phC6j9MXQ",
    "G3hPfIBSG_4",
    "_z3PZP4rylM",
    "gdK4jqj9_Jo",
    "1bGjK5KpFjE",
}

df = pd.read_csv(INPUT)

review = df[df["video_id"].isin(PRIORITY_VIDEOS)].copy()

review["relevance"] = ""
review["relevance_status"] = "Pending"

review["stance"] = ""
review["stance_status"] = "Pending"

Path("data/processed").mkdir(parents=True, exist_ok=True)
review.to_csv(OUTPUT, index=False)

print("===== RELEVANCE REVIEW DATASET =====")
print("Selected comments:", len(review))
print("Videos:", review["video_id"].nunique())

print("\n===== COMMENTS PER VIDEO =====")
print(
    review.groupby(["video_id", "video_title"])
    .size()
    .sort_values(ascending=False)
    .to_string()
)

print("\nSaved:", OUTPUT)
