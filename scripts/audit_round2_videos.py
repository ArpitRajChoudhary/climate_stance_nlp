import pandas as pd

path = "data/raw/youtube_comments_round2.csv"
df = pd.read_csv(path, keep_default_na=False)

print("ROUND 2 VIDEO QUALITY AUDIT")
print("===========================")
print("Total comments:", len(df))
print("Unique videos:", df["video_id"].nunique())

for video_id, group in df.groupby("video_id", sort=False):

    first = group.iloc[0]

    print("\n" + "=" * 85)
    print("VIDEO ID:", video_id)
    print("TITLE:", first["video_title"])
    print("CHANNEL:", first["channel_title"])
    print("SEARCH LANGUAGE:", first["search_language"])
    print("COMMENTS:", len(group))

    print("\nDetected language distribution:")
    print(group["detected_language"].value_counts().head(8).to_string())

    print("\nSample comments:")

    for _, row in group.head(3).iterrows():
        print("-", row["comment_text"][:350].replace("\n", " "))

