
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YouTube API key not found in .env")

youtube = build("youtube", "v3", developerKey=API_KEY)

search_queries = {
    "Hindi": {
        "query": "जलवायु परिवर्तन",
        "language": "hi"
    },
    "Bengali": {
        "query": "জলবায়ু পরিবর্তন",
        "language": "bn"
    }
}

def test_search(language, query, relevance_language):
    print(f"\n===== {language} SEARCH =====")

    response = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=5,
        relevanceLanguage=relevance_language,
        regionCode="IN"
    ).execute()

    for index, item in enumerate(response.get("items", []), 1):
        snippet = item["snippet"]

        print(f"\n{index}. {snippet['title']}")
        print(f"Channel: {snippet['channelTitle']}")
        print(f"Video ID: {item['id']['videoId']}")

    print(f"\nTotal results returned: {len(response.get('items', []))}")


if __name__ == "__main__":
    try:
        for language, details in search_queries.items():
            test_search(
                language,
                details["query"],
                details["language"]
            )

        print("\nYouTube API connection successful!")

    except HttpError as error:
        print("YouTube API error:", error)
