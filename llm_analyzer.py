import os
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def analyze_titles_with_gemini(videos, query):
    if not GEMINI_API_KEY:
        raise ValueError("Missing Gemini API key in .env")

    model = "models/gemini-1.5-flash"  # or "models/gemini-pro"
    url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={GEMINI_API_KEY}"

    titles = [v['title'] for v in videos]

    prompt = f"""
You are an AI assistant. A user searched: "{query}". You are given the following YouTube video titles:

{chr(10).join([f"{i+1}. {title}" for i, title in enumerate(titles)])}

Pick the single most relevant and helpful title and return ONLY that exact title.
"""

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    try:
        return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
    except (KeyError, IndexError):
        return "No relevant result found."