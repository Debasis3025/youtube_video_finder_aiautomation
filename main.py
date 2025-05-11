from youtube_search import search_youtube
from llm_analyzer import analyze_titles_with_gemini

def main():
    query = input("Enter your search query: ")
    videos = search_youtube(query)
    print("\n🎬 Top 20 Filtered Videos:\n")
    for i, video in enumerate(videos, start=1):
     print(f"{i}. {video['title']}")
     print(f"   {video['url']}")

    if not videos:
        print("No relevant videos found.")
        return

    best_video_title = analyze_titles_with_gemini(videos, query)

    print("\n🎯 Best Match:")
    print("Title:", best_video_title)

if __name__ == "__main__":
    main()