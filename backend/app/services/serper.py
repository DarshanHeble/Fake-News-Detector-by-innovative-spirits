import requests
import json
import asyncio
from typing import List, Union
from aiohttp import ClientSession
from ..Types.types import FetchedNewsType, ScrapedNewsType
from .webScrap import extract_news_from_meta
from typing import Optional

SERPER_API_KEY = 'cb0928906e7b91c67200cfd5cb820fc8b2b9a371'
SERPER_NEWS_URL = "https://google.serper.dev/news"

async def fetch_news_from_serper(
    keywords_or_string: Union[List[str], str],
    start: int = 1,
    num: int = 10
) -> List[FetchedNewsType]:
    """
    Fetches news using Serper API with given keywords or query string.

    Args:
        keywords_or_string: A list of keywords or a single query string
        start: Start index (currently not used by Serper API)
        num: Number of results to fetch (max 100)

    Returns:
        A list of FetchedNewsType containing news article links
    """
    # Form query string based on input type
    if isinstance(keywords_or_string, list):
        query = ' '.join(keywords_or_string)
    elif isinstance(keywords_or_string, str):
        query = keywords_or_string
    else:
        raise ValueError("Invalid input: Must be a list of keywords or a string query.")

    payload = json.dumps({
        "q": query,
        "gl": "in",
        "num": min(num, 100)
    })
    
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    try:
        async with ClientSession() as session:
            async with session.post(SERPER_NEWS_URL, headers=headers, data=payload) as response:
                response.raise_for_status()
                data = await response.json()
                
                news_items = data.get("news", [])
                return [
                    FetchedNewsType(
                        link=item.get("link"),
                        domain=item.get("source")
                    )
                    for item in news_items
                ]

    except Exception as e:
        print(f"Error fetching news from Serper: {e}")
        return []
