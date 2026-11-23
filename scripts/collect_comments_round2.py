import os
import time
import pandas as pd

from pathlib import Path
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langdetect import detect, LangDetectException

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in .env")

youtube = build("youtube", "v3", developerKey=API_KEY)

RAW_DIR = Path("data/raw")
ORIGINAL_FILE = RAW_DIR / "youtube_comments.csv"
OUTPUT_FILE = RAW_DIR / "youtube_comments_round2.csv"

# Collection limits
MAX_VIDEOS_PER_QUERY = 10
MAX_NEW_VIDEOS_PER_LANGUAGE = 10
MAX_COMMENT_PAGES_PER_VIDEO = 2
COMMENTS_PER_PAGE = 100

SEARCH_QUERIES = {
    "Hindi": [
        "ग्लोबल वार्मिंग सच या झूठ",
        "जलवायु परिवर्तन मानव निर्मित या प्राकृतिक",
        "जलवायु परिवर्तन पर बहस",
        "ग्लोबल वार्मिंग पर लोगों की राय",
        "क्या ग्लोबल वार्मिंग वास्तव में हो रही है",
        "जलवायु परिवर्तन पर वैज्ञानिकों की राय",
        "ग्लोबल वार्मिंग के दावे पर सवाल"
    ],
    "Bengali": [
        "বিশ্ব উষ্ণায়ন সত্যি নাকি মিথ্যা",
        "জলবায়ু পরিবর্তন মানুষের কারণে নাকি প্রাকৃতিক",
        "জলবায়ু পরিবর্তন নিয়ে বিতর্ক",
        "বিশ্ব উষ্ণায়ন নিয়ে মানুষের মতামত",
        "জলবায়ু পরিবর্তন কি সত্যিই হচ্ছে",
        "জলবায়ু পরিবর্তন নিয়ে বিজ্ঞানীদের মতামত",
        "বিশ্ব উষ্ণায়নের দাবি নিয়ে প্রশ্ন"
    ]
}

LANGUAGE_CODES = {
    "Hindi": "hi",
    "Bengali": "bn"
}


def detect_language(text):
    try:
        return detect(text)
    except (LangDetectException, Exception):
        return "unknown"


def load_existing_ids(path, column):
    if not path.exists():
        return set()

    df = pd.read_csv(path, keep_default_na=False)

    if column not in df.columns:
        return set()

    return set(df[column].astype(str))


def search_videos(query, language):
    response = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=MAX_VIDEOS_PER_QUERY,
        relevanceLanguage=LANGUAGE_CODES[language],
        regionCode="IN"
    ).execute()

    videos = []

    for item in response.get("items", []):
        videos.append({
            "video_id": item["id"]["videoId"],
            "video_title": item["snippet"]["title"],
            "channel_title": item["snippet"]["channelTitle"],
            "video_published_at": item["snippet"]["publishedAt"]
        })

    return videos


def collect_video_comments(video, language, query):
    comments = []
    page_token = None

    for _ in range(MAX_COMMENT_PAGES_PER_VIDEO):
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video["video_id"],
            maxResults=COMMENTS_PER_PAGE,
            textFormat="plainText",
            order="time",
            pageToken=page_token
        )

        response = request.execute()

        for item in response.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            text = snippet.get("textDisplay", "").strip()

            if not text:
                continue

            comments.append({
                "comment_id": item["snippet"]["topLevelComment"]["id"],
                "video_id": video["video_id"],
                "video_title": video["video_title"],
                "channel_title": video["channel_title"],
                "video_published_at": video["video_published_at"],
                "comment_text": text,
                "comment_published_at": snippet["publishedAt"],
                "like_count": snippet.get("likeCount", 0),
                "search_language": language,
                "search_query": query,
                "detected_language": detect_language(text)
            })

        page_token = response.get("nextPageToken")

        if not page_token:
            break

        time.sleep(0.2)

    return comments


def save_comments(new_comments):
    if not new_comments:
        return

    new_df = pd.DataFrame(new_comments)

    if OUTPUT_FILE.exists():
        existing_df = pd.read_csv(OUTPUT_FILE, keep_default_na=False)
        combined = pd.concat(
            [existing_df, new_df],
            ignore_index=True
        )
    else:
        combined = new_df

    combined = combined.drop_duplicates(
        subset=["comment_id"],
        keep="first"
    )

    combined.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if not ORIGINAL_FILE.exists():
        raise FileNotFoundError(
            f"Original dataset not found: {ORIGINAL_FILE}"
        )

    # Exclude videos already collected in Round 1.
    original_video_ids = load_existing_ids(
        ORIGINAL_FILE, "video_id"
    )

    # Also exclude videos and comments already collected in Round 2.
    round2_video_ids = load_existing_ids(
        OUTPUT_FILE, "video_id"
    )

    existing_comment_ids = load_existing_ids(
        ORIGINAL_FILE, "comment_id"
    )
    existing_comment_ids.update(
        load_existing_ids(OUTPUT_FILE, "comment_id")
    )

    processed_videos = original_video_ids | round2_video_ids

    print("ROUND 2 COLLECTION")
    print("==================")
    print("Original videos excluded:", len(original_video_ids))
    print("Previously collected Round 2 videos:", len(round2_video_ids))

    total_new_comments = 0

    for language, queries in SEARCH_QUERIES.items():

        print(f"\n========== {language.upper()} ==========")

        new_videos_this_language = 0

        for query in queries:

            if new_videos_this_language >= MAX_NEW_VIDEOS_PER_LANGUAGE:
                break

            print(f"\nSearching: {query}")

            try:
                videos = search_videos(query, language)

            except HttpError as error:
                print("Search failed:", error)

                if "quotaExceeded" in str(error):
                    print("API quota exhausted. Stopping.")
                    return

                continue

            print("Search results:", len(videos))

            for video in videos:

                video_id = video["video_id"]

                if video_id in processed_videos:
                    continue

                if new_videos_this_language >= MAX_NEW_VIDEOS_PER_LANGUAGE:
                    break

                print("\nCollecting:", video["video_title"])
                print("Video ID:", video_id)

                try:
                    comments = collect_video_comments(
                        video, language, query
                    )

                    # Avoid duplicate comments across both rounds.
                    unique_comments = []

                    for comment in comments:
                        comment_id = comment["comment_id"]

                        if comment_id not in existing_comment_ids:
                            unique_comments.append(comment)
                            existing_comment_ids.add(comment_id)

                    save_comments(unique_comments)

                    processed_videos.add(video_id)
                    new_videos_this_language += 1
                    total_new_comments += len(unique_comments)

                    print("New unique comments:", len(unique_comments))
                    print(
                        f"New videos for {language}: "
                        f"{new_videos_this_language}/"
                        f"{MAX_NEW_VIDEOS_PER_LANGUAGE}"
                    )

                except HttpError as error:
                    print("Comment collection failed:", error)

                    if "quotaExceeded" in str(error):
                        print("API quota exhausted. Stopping.")
                        return

                    # Other errors, such as disabled comments, are skipped.
                    continue

                time.sleep(0.3)

    print("\n========== ROUND 2 COMPLETED ==========")
    print("New unique comments collected:", total_new_comments)

    if OUTPUT_FILE.exists():
        result = pd.read_csv(OUTPUT_FILE, keep_default_na=False)

        print("Total Round 2 comments:", len(result))
        print("Unique Round 2 videos:", result["video_id"].nunique())

        print("\nSearch language distribution:")
        print(result["search_language"].value_counts().to_string())

        print("\nDetected language distribution:")
        print(result["detected_language"].value_counts().to_string())

        print("\nSaved to:", OUTPUT_FILE)
    else:
        print("No comments were collected.")


if __name__ == "__main__":
    main()
