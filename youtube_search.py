import os
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from dotenv import load_dotenv
from utils import parse_duration

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def search_youtube(query):
    if not YOUTUBE_API_KEY:
        raise ValueError("Missing YouTube API key in .env")

    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    search_response = youtube.search().list(
        q=query,
        part="id",
        type="video",
        maxResults=50,  # fetch more to filter down to 20
        publishedAfter=(datetime.utcnow() - timedelta(days=14)).isoformat("T") + "Z"
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_response["items"]]

    # Get details of videos
    videos_response = youtube.videos().list(
        part="snippet,contentDetails",
        id=",".join(video_ids)
    ).execute()

    results = []
    for item in videos_response["items"]:
        title = item["snippet"]["title"]
        video_id = item["id"]
        duration = item["contentDetails"]["duration"]
        parsed_duration = parse_duration(duration)

        if 240 <= parsed_duration <= 1200:  # 4–20 minutes in seconds
            results.append({
                "title": title,
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })

        if len(results) >= 20:
            break

    return results