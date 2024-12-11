import requests
from bs4 import BeautifulSoup
from ..Types.types import ScrapedNewsType
from urllib.parse import urlparse

def extract_headline_from_meta(url)-> ScrapedNewsType:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the domain from the URL
    parsed_url = urlparse(url)
    # print("parsed url:", parsed_url)
    domain =parsed_url.netloc

    # Example logic
    title = soup.find('meta', property='og:title') or soup.title
    description = soup.find('meta', property='og:description') or soup.find('meta', attrs={'name': 'description'})
    published_at = soup.find('meta', property='article:published_time') or soup.find('time')

    # Construct the FetchedNewsType instance for type support
    news_data = ScrapedNewsType(
        title=title['content'] if title and title.has_attr('content') else title.string if title else None,
        description=description['content'] if description and description.has_attr('content') else None,
        published_at=published_at['content'] if published_at and published_at.has_attr('content') else published_at.string if published_at else None,
        domain= domain
    )
    
    # print(news_data)
    return news_data