import pandas as pd
from pathlib import Path

BASE = Path("data/raw")
INPUT = BASE / "youtube_comments_round2.csv"

REVIEW_OUTPUT = Path("data/processed/round2_video_review.csv")
COMMENTS_OUTPUT = Path("data/processed/round2_candidate_comments.csv")

df = pd.read_csv(INPUT, keep_default_na=False)

decisions = {
    "BJwvmT8iLs0": (
        "Candidate",
        "Hindi",
        "Cow methane and greenhouse gas emissions in global warming"
    ),
    "0UydzLKcFww": (
        "Priority",
        "Hindi",
        "Climate change sceptics versus activists"
    ),
    "BtsC1dYDsUk": (
        "Potential",
        "Hindi",
        "Carbon credit trading and climate mitigation"
    ),
    "KgMF1gVWzCw": (
        "Potential",
        "Hindi",
        "Carbon credits and global warming"
    ),
    "pVW47F8BHto": (
        "Potential",
        "Hindi",
        "Human impact and mass extinction; climate relevance needs verification"
    ),
    "K3xUcE8RJCY": (
        "Exclude",
        "English",
        "Climate-related but comments are English, outside target languages"
    ),
    "vjKgM2fMFlg": (
        "Exclude",
        "English",
        "Climate-related but comments are English, outside target languages"
    )
}

video_rows = []

for video_id, group in df.groupby("video_id", sort=False):
    first = group.iloc[0]

    status, category, reason = decisions.get(
        video_id,
        (
            "Exclude",
            "Unrelated_or_unsuitable",
            "Video topic is unrelated to the target climate-change stance task"
        )
    )

    video_rows.append({
        "video_id": video_id,
        "video_title": first["video_title"],
        "channel_title": first["channel_title"],
        "search_language": first["search_language"],
        "comment_count": len(group),
        "review_decision": status,
        "category": category,
        "review_reason": reason
    })

video_review = pd.DataFrame(video_rows)

video_review.to_csv(REVIEW_OUTPUT, index=False)

selected_ids = [
    video_id
    for video_id, decision in decisions.items()
    if decision[0] in ["Candidate", "Priority", "Potential"]
]

candidates = df[df["video_id"].isin(selected_ids)].copy()

candidates["relevance_review"] = ""
candidates["relevance_reason"] = ""

candidates.to_csv(COMMENTS_OUTPUT, index=False)

print("\nROUND 2 REVIEW FILES CREATED")
print("============================")
print("Videos audited:", len(video_review))
print("Candidate videos:", len(selected_ids))
print("Candidate comments:", len(candidates))

print("\nVideo decisions:")
print(video_review["review_decision"].value_counts().to_string())

print("\nCandidate comments by video:")
print(
    candidates.groupby(
        ["video_id", "video_title"]
    ).size().to_string()
)

print("\nFiles saved:")
print(REVIEW_OUTPUT)
print(COMMENTS_OUTPUT)

print("\nOriginal raw datasets were not modified.")
