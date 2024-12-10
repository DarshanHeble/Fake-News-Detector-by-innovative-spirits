import requests
from bs4 import BeautifulSoup
from ..Types.types import FetchedNewsType


# uncomment these line when executing this function alone
# from pydantic import BaseModel,Field
# from typing import Literal,Optional
# class FetchedNewsType(BaseModel):
#     title: Optional[str] = Field(None, description="The headline or title of the news article.")
#     description: Optional[str] = Field(None, description="The description or summary of the news article.")
#     published_at: Optional[str] = Field(None, description="The published date and time of the news article.")


def extract_headline_from_meta(url)-> FetchedNewsType:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    
    news_data = {}

    # Example logic
    title = soup.find('meta', property='og:title') or soup.title
    description = soup.find('meta', property='og:description') or soup.find('meta', attrs={'name': 'description'})
    published_at = soup.find('meta', property='article:published_time') or soup.find('time')

    # Construct the FetchedNewsType instance for type support
    news_data = FetchedNewsType(
        title=title['content'] if title and title.has_attr('content') else title.string if title else None,
        description=description['content'] if description and description.has_attr('content') else None,
        published_at=published_at['content'] if published_at and published_at.has_attr('content') else published_at.string if published_at else None
    )
    
    return news_data


# juST FOR EXAMPLE
# link = "https://indianexpress.com/article/world/unitedhealthcare-ceo-brian-thompson-murder-health-insurance-9709821/"  # Replace with a valid news article URL
# news_data = extract_headline_from_meta(link)
# # print(type(news_data["published_at"]))
# print(news_data.title)
# if news_data:
#     print("News Data:", news_data)
# else:
#     print("Failed to fetch news data.")