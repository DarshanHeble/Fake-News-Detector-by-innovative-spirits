# #import all libraries and variables
import requests
from ..constants import CSE_ID, GOOGLE_API_KEY, BASE_SEARCH_URL
from ..Types.types import FetchedNewsType, ScrapedNewsType
from .webScrap import extract_news_from_meta


def fetchNewsFromGoogle(query: str) -> list[FetchedNewsType]:
    """
    code explanation here(coming soon)

    """
    params = {
        "q": query,
        "cx": CSE_ID,
        "key": GOOGLE_API_KEY,
        "num": 10  # maximum number of articles to be fetched from Google
    }
    
    response = requests.get(BASE_SEARCH_URL, params=params)
    response.raise_for_status()  # Raise an error for bad requests
    articles = response.json().get("items", [])
    
    fetched_news = []
    for article in articles:
        news_item = FetchedNewsType(
            # title=article.get("title"),
            link=article.get("link"),
            # domain=article.get("displayLink")
        )
        fetched_news.append(news_item)
    
    return fetched_news


def fetch_and_scrape_news_from_google(query: str) -> list[ScrapedNewsType]:
    print("Fetching news from google ...")
    # Fetch news articles from Google
    articles = fetchNewsFromGoogle(query)
    
    scraped_articles: list[ScrapedNewsType] = []
    for article in articles:
        content = extract_news_from_meta(article.link)
        
        news = ScrapedNewsType(
            title= content.title,
            description = content.description
        )
        scraped_articles.append(news)
        
    return scraped_articles

# Example usage
# query = "U.S. military to accept transgender recruits on Monday: Pentagon"
# results = fetch_and_scrape_news(query)
# for result in results:
#     print(f"Title: {result['title']}\nLink: {result['link']}\nContent: {result['content']}\n")