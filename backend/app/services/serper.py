import requests
import json
from ..constants import SERPER_API_KEY

url = "https://google.serper.dev/news"


def search_news_with_serper(query: str):
    payload = json.dumps(
        {
            "q": query,
            "gl": "in",
            "num": 100,
        }
    )

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()
        filtered_news = [
            news for news in data["news"] if "title" in news and "snippet" in news
        ]
        return filtered_news
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []
