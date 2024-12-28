import requests
from ..constants import BASE_NEWS_API_URL, NEWS_API_KEY
from ..Types.types import FetchedNewsType, ScrapedNewsType
from ..services.webScrap import extract_news_from_meta
from typing import List

def get_related_articles_news_api(keywords: List[str]) -> List[FetchedNewsType]:
    
    """
    Fetches related articles from the News API based on the provided keywords.

    Args:
        keywords (List[str]): A list of keywords to search for related articles.

    Returns:
        List[ScrapedNewsType]: A list of articles matching the search criteria.
    """
    
    query = '+'.join(keywords)  # Combine keywords for query
    params = {
        "q": query,
        "language": "en",        
        "sortBy": "relevancy",   
        "domain": "reuters.com",   
        "apiKey": NEWS_API_KEY,
        "pageSize": 10
    }
    response = requests.get(BASE_NEWS_API_URL, params=params)
    # print(response.request.url) #see url for api request
    data = response.json()
    
    fetched_articles = []
    if data.get('status') == 'ok':
        for article in data['articles']:
            # fetched_articles.append({
            #     # 'source': article['source']['name'],
            #     # 'title': article['title'],
            #     'url': article['url'],
            #     # 'description': article.get('description', ''),
            #     # 'content': article.get('content', '')
            # })
            fetched_articles.append(FetchedNewsType(
                link = article["url"]
            ))
    
    return fetched_articles

# Function to scrape full news content based on URLs
def fetch_and_scrape_news_from_newsApi(keywords: List[str]) -> List[ScrapedNewsType]:
    """
    Fetches URLs of related news articles from News API and scrapes their content.

    Args:
        keywords (List[str]): A list of keywords to search for related articles.

    Returns:
        List[ScrapedNewsType]: A list of scraped news with title, description, and domain.
    """
    
    fetched_news = get_related_articles_news_api(keywords) #only urls
    # print("fetched news urls", fetched_news)
    scraped_articles = []

    for news in fetched_news:
        if news.link:
            scraped_data = extract_news_from_meta(news.link)
            if scraped_data:
                scraped_articles.append(scraped_data)
    
    return scraped_articles

# Example usage
# keywords = ["military", "transgender recruits"]
# related_articles = get_related_articles_news_api(keywords)
# print("Related Articles:", related_articles)
