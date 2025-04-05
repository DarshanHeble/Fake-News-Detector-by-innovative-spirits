import pandas as pd
from eventregistry import (
    EventRegistry,
    QueryArticlesIter,
    RequestArticlesInfo,
    QueryItems,
)
from extractKeywords import extract_keywords_yake

API_KEY = "4c5fa027-b98f-4581-86d2-271a1ce0c14c"
er = EventRegistry(apiKey=API_KEY)


def fetch_event_registry_news(
    keywords: list[str], max_articles: int = 100
) -> list[dict]:
    """
    Fetches news articles using the official Event Registry library.

    Args:
        keywords (list[str]): List of keywords to search for.
        max_articles (int): Max number of articles to fetch (max 100 per query).

    Returns:
        List[dict]: List of article dictionaries.
    """
    if not keywords:
        return []

    query = QueryItems.AND(keywords)

    q = QueryArticlesIter(keywords=query)
    q.setRequestedResult(
        RequestArticlesInfo(count=max_articles, sortBy="sourceImportance")
    )

    try:
        response = er.execQuery(q)
        articles = response.get("articles", {}).get("results", [])
        # print(articles)
        return articles
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return []


news = " Donald Trump Sends Out Embarrassing New Years Eve Message; This is Disturbing"
keywords = extract_keywords_yake(news, top_n=15, strict=True)
datas = fetch_event_registry_news(keywords)
print("len ", len(datas))
for data in datas:
    print(data)
    print("*" * 100)
