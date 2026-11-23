import re
import pandas as pd
from pathlib import Path

SOURCE = Path("data/processed/round2_candidate_comments.csv")
OUTPUT = Path("data/processed/round2_relevance_shortlist.csv")

df = pd.read_csv(SOURCE, keep_default_na=False)

PRIORITY_VIDEOS = {
    "0UydzLKcFww",
    "BJwvmT8iLs0"
}

# High-recall vocabulary. This is only a shortlist filter,
# not an automatic relevance or stance classifier.
pattern = re.compile(
    r"""
    global\s*warming|
    climate\s*change|
    climate\s*crisis|
    jalvayu|
    jalvayu\s*parivartan|
    vishv\s*ushna|
    tapman|
    तापमान|
    जलवायु|
    ग्लोबल\s*वार्मिंग|
    जलवायु\s*परिवर्तन|
    गर्मी|
    गरमी|
    धरती.*गर्म|
    पृथ्वी.*गर्म|
    carbon|
    methane|
    greenhouse|
    cow|
    cattle|
    गाय|
    गोबर|
    पशु|
    मवेशी|
    प्रदूषण|
    पर्यावरण|
    उद्योग|
    प्रकृति|
    """,
    re.IGNORECASE | re.VERBOSE
)

selected = df[df["video_id"].isin(PRIORITY_VIDEOS)].copy()

dw = selected[selected["video_id"] == "0UydzLKcFww"].copy()

cow = selected[selected["video_id"] == "BJwvmT8iLs0"].copy()

cow["keyword_match"] = cow["comment_text"].apply(
    lambda text: bool(pattern.search(str(text)))
)

# Keep every DW comment and keyword-matched cow-video comments.
shortlist = pd.concat(
    [dw, cow[cow["keyword_match"]]],
    ignore_index=True
)

shortlist["relevance_review"] = ""
shortlist["relevance_reason"] = ""
shortlist["stance_review"] = ""
shortlist["annotation_status"] = "Pending"

shortlist = shortlist.drop_duplicates(
    subset=["comment_id"],
    keep="first"
)

shortlist.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

print("\nROUND 2 SHORTLIST CREATED")
print("=========================")
print("DW comments retained:", len(dw))
print("Cow-video comments:", len(cow))
print(
    "Cow-video keyword matches:",
    int(cow["keyword_match"].sum())
)
print("Total shortlist comments:", len(shortlist))

print("\nShortlist by video:")
print(
    shortlist.groupby(
        ["video_id", "video_title"]
    ).size().to_string()
)

print("\nSaved to:", OUTPUT)
print("Original datasets were not modified.")
