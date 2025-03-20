import requests
import aiohttp
import asyncio
from aiohttp import ClientResponseError, ClientSession
from ..constants import CSE_ID, GOOGLE_API_KEY, BASE_SEARCH_URL
from ..Types.types import FetchedNewsType, ScrapedNewsType
from .webScrap import extract_news_from_meta
from typing import List, Optional, Union
from mimetypes import guess_type

async def fetch_news_from_google(
    keywords_or_string: Union[List[str], str], 
    start: int = 1, 
    num: int = 10
) -> List[FetchedNewsType]:
    """
    Fetches news links from Google Custom Search API using given keywords or query string.

    Args:
        keywords_or_string: A list of keywords or a single query string.
        start: Start index for pagination (default is 1).
        num: Number of results to fetch (default is 10, max 10).

    Returns:
        A list of FetchedNewsType containing news article links or an empty list if quota is exhausted.
    """
    # Form query string based on input type
    if isinstance(keywords_or_string, list):
        query = '+'.join(keywords_or_string)
    elif isinstance(keywords_or_string, str):
        query = keywords_or_string
    else:
        raise ValueError("Invalid input: Must be a list of keywords or a string query.")

    params = {
        "q": query,
        "cx": CSE_ID,  # Custom Search Engine ID
        "key": GOOGLE_API_KEY,  # Google API key
        "start": start,
        "num": min(num, 10),  # Google API limits num to 10
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(BASE_SEARCH_URL, params=params) as response:
                response.raise_for_status()  # Raise exception for HTTP errors

                # Parse response JSON
                response_data = await response.json()

                # Handle quota errors
                if "error" in response_data:
                    error_message = response_data["error"].get("message", "Unknown error.")
                    if "quota" in error_message.lower():
                        print("Google Custom Search API quota exceeded.")
                        return []  # Return empty list for exhausted quota

                # Process fetched articles
                articles = response_data.get("items", [])
                fetched_news = [
                    FetchedNewsType(
                        link=article.get("link"),
                        domain=article.get("displayLink")
                    )
                    for article in articles
                ]
                return fetched_news

        except ClientResponseError as e:
            print(f"HTTP error occurred: {e.status} - {e.message}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    return []  # Default return for failures


async def fetch_and_scrape_news_from_google(
    keywords_or_string: Union[List[str], str], 
    start: int = 1, 
    num: int = 10
) -> list[ScrapedNewsType]:
    """
    Fetches news articles using Google Custom Search and scrapes metadata concurrently.

    Args:
        keywords: A list of keywords to form the search query.

    Returns:
        A list of ScrapedNewsType containing titles and descriptions or an empty list if quota is exhausted.
    """
    print("Fetching news from Google...")
    articles = await fetch_news_from_google(keywords_or_string)
    print(f"Fetched {len(articles)} articles from Google.")

    if not articles:
        print("No articles fetched. Quota might be exhausted or no results found.")
        return []

    async with ClientSession() as session:
        tasks = [
            scrape_article(article.link, session)
            for article in articles
        ]
        results = await asyncio.gather(*tasks)
    
    # Filter out None results
    scraped_articles = [result for result in results if result is not None]
    print(f"Scraped {len(scraped_articles)} articles successfully.")
    return scraped_articles

async def scrape_article(link: str, session: ClientSession) -> Optional[ScrapedNewsType]:
    """
    Asynchronously scrapes a single article for metadata.

    Args:
        link: The article URL.
        session: The shared aiohttp session for making requests.

    Returns:
        ScrapedNewsType object or None if scraping fails or format unsupported.
    """
    mime_type, _ = guess_type(link)
    if mime_type and not mime_type.startswith("text/html"):
        print(f"Skipping unsupported format: {link} (MIME type: {mime_type})")
        return None

    try:
        content = extract_news_from_meta(link)
        if content:
            return ScrapedNewsType(title=content.title, description=content.description, link=link)
    except Exception as e:
        print(f"Error scraping article: {link} - {e}")
    return None
