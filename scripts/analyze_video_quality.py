import pandas as pd

df = pd.read_csv("data/processed/language_review.csv")

report = (
    df.groupby(["video_id", "video_title", "search_language"], dropna=False)
    .agg(
        total_comments=("comment_id", "count"),
        language_candidates=("script_language_candidate", "nunique"),
        hindi_candidates=(
            "script_language_candidate",
            lambda x: x.isin([
                "hi", "hi_mixed", "hi_Latn_candidate"
            ]).sum()
        ),
        bengali_candidates=(
            "script_language_candidate",
            lambda x: x.isin([
                "bn", "bn_mixed", "bn_Latn_candidate"
            ]).sum()
        ),
        mixed_review=(
            "script_language_candidate",
            lambda x: x.isin([
                "mixed_hi_bn_review",
                "romanized_hi_bn_review"
            ]).sum()
        )
    )
    .reset_index()
    .sort_values("total_comments", ascending=False)
)

print("\n===== VIDEO-LEVEL DATASET REPORT =====\n")

for _, row in report.iterrows():
    print(f"\nVideo: {row['video_title']}")
    print(f"Video ID: {row['video_id']}")
    print(f"Search language: {row['search_language']}")
    print(f"Total comments: {row['total_comments']}")
    print(f"Hindi candidates: {row['hindi_candidates']}")
    print(f"Bengali candidates: {row['bengali_candidates']}")
    print(f"Mixed-language review: {row['mixed_review']}")

report.to_csv("data/processed/video_quality_report.csv", index=False)

print("\nSaved: data/processed/video_quality_report.csv")
