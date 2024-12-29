# from .extractKeywords import extract_keywords
from .fetchNewsFromGoogle import fetch_news_from_google

async def getRelatedNews(content):
    # try:
    #     keywords = extract_keywords(content)
    #     if not keywords:
    #         raise ValueError("Failed to extract keywords.")
    # except Exception as e:
    #     print(f"Error extracting keywords: {e}")
    
    try:
        print("Fetching Articles from google")
        articles = await fetch_news_from_google(content)
        articles
    except Exception as e:
        print(f"Error fetching articles from Google search: {e}")
        articles = []
            
    return articles