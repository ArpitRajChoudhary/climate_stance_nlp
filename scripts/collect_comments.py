
import os
import time
import pandas as pd

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langdetect import detect, LangDetectException

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in .env")

youtube = build("youtube", "v3", developerKey=API_KEY)

OUTPUT_FILE = "data/raw/youtube_comments.csv"

# Pilot collection settings
MAX_VIDEOS_PER_QUERY = 5
MAX_COMMENT_PAGES_PER_VIDEO = 2
COMMENTS_PER_PAGE = 100

SEARCH_QUERIES = {
    "Hindi": [
        "जलवायु परिवर्तन",
        "ग्लोबल वार्मिंग",
        "धरती का तापमान बढ़ना",
        "जलवायु संकट",
        "पर्यावरण संकट"
    ],
    "Bengali": [
        "জলবায়ু পরিবর্তন",
        "বিশ্ব উষ্ণায়ন",
        "পৃথিবীর তাপমাত্রা বৃদ্ধি",
        "জলবায়ু সংকট",
        "পরিবেশ সংকট"
    ]
}

LANGUAGE_CODES = {
    "Hindi": "hi",
    "Bengali": "bn"
}


def detect_language(text):
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"
    except Exception:
        return "unknown"


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

    for page in range(MAX_COMMENT_PAGES_PER_VIDEO):
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


def save_comments(all_comments):
    if not all_comments:
        return

    df = pd.DataFrame(all_comments)

    if os.path.exists(OUTPUT_FILE):
        existing = pd.read_csv(OUTPUT_FILE)
        df = pd.concat([existing, df], ignore_index=True)

    df = df.drop_duplicates(subset=["comment_id"])
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")


def main():
    all_comments = []
    processed_videos = set()

    for language, queries in SEARCH_QUERIES.items():

        print(f"\n========== {language.upper()} COLLECTION ==========")

        for query in queries:

            print(f"\nSearching: {query}")

            try:
                videos = search_videos(query, language)

            except HttpError as error:
                print("Video search failed:", error)
                continue

            print(f"Videos found: {len(videos)}")

            for video in videos:

                video_id = video["video_id"]

                if video_id in processed_videos:
                    continue

                processed_videos.add(video_id)

                print(f"\nCollecting: {video['video_title']}")

                try:
                    comments = collect_video_comments(
                        video, language, query
                    )

                    all_comments.extend(comments)

                    print(f"Comments collected: {len(comments)}")

                    # Save after every video to prevent data loss
                    save_comments(all_comments)
                    all_comments.clear()

                except HttpError as error:
                    print("Comment collection failed:", error)

                    error_text = str(error)

                    if "quotaExceeded" in error_text:
                        print("API quota exhausted. Stopping collection.")
                        return

                time.sleep(0.2)

    if all_comments:
        save_comments(all_comments)

    print("\n========== COLLECTION COMPLETED ==========")

    if os.path.exists(OUTPUT_FILE):
        df = pd.read_csv(OUTPUT_FILE)

        print("Total unique comments:", len(df))
        print("\nDetected language distribution:")
        print(df["detected_language"].value_counts())

        print("\nSaved to:", OUTPUT_FILE)
    else:
        print("No comments were collected.")


if __name__ == "__main__":
    main()
