import requests
from ..constants import CSE_ID, GOOGLE_API_KEY, BASE_SEARCH_URL
from ..Types.types import FetchedNewsType, ScrapedNewsType
from .webScrap import extract_news_from_meta
from typing import List


def fetchNewsFromGoogle(keywords: List[str]) -> list[FetchedNewsType]:
    """
    Fetches news links from Google Custom Search API using given keywords.

    Args:
        keywords: A list of keywords to form the search query.

    Returns:
        A list of FetchedNewsType containing news article links or an empty list if quota is exhausted.
    """
    query = '+'.join(keywords)
    params = {
        "q": query,
        "cx": CSE_ID,
        "key": GOOGLE_API_KEY,
        "num": 10  # maximum number of articles to be fetched from Google
    }

    try:
        response = requests.get(BASE_SEARCH_URL, params=params)
        response.raise_for_status()  # Raise an error for bad requests

        # Check for quota exceeded in response JSON
        response_data = response.json()
        if "error" in response_data:
            error_message = response_data["error"]["message"]
            if "quota" in error_message.lower():
                print("Google Custom Search API quota exceeded.")
                return []  # Return an empty list or handle as needed

        articles = response_data.get("items", [])
        fetched_news = []
        for article in articles:
            news_item = FetchedNewsType(
                link=article.get("link"),
            )
            fetched_news.append(news_item)

        return fetched_news

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching news from Google: {e}")
        return []


def fetch_and_scrape_news_from_google(keywords: List[str]) -> list[ScrapedNewsType]:
    """
    Fetches news articles using Google Custom Search and scrapes metadata.

    Args:
        keywords: A list of keywords to form the search query.

    Returns:
        A list of ScrapedNewsType containing titles and descriptions or an empty list if quota is exhausted.
    """
    print("Fetching news from Google...")
    articles = fetchNewsFromGoogle(keywords)
    print(f"Fetched {len(articles)} articles from Google.")

    if not articles:
        print("No articles fetched. Quota might be exhausted or no results found.")
        return []

    scraped_articles: list[ScrapedNewsType] = []
    for article in articles:
        try:
            content = extract_news_from_meta(article.link)
            news = ScrapedNewsType(
                title=content.title,
                description=content.description
            )
            scraped_articles.append(news)
        except Exception as e:
            print(f"Error scraping article: {article.link} - {e}")

    return scraped_articles
