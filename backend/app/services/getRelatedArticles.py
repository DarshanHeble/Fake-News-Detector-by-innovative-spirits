import requests
from ..constants import BASE_NEWS_API_URL, NEWS_API_KEY

def get_related_articles_news_api(keywords):
    
    query = '+'.join(keywords)  # Combine keywords for query
    params = {
        "q": query,
        "language": "en",        
        "sortBy": "relevancy",   
        "domain": "cnn.com",   
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(BASE_NEWS_API_URL, params=params)
    # print(response.request.url) #see url for api request
    data = response.json()
    
    articles = []
    if data.get('status') == 'ok':
        for article in data['articles']:
            articles.append({
                'source': article['source']['name'],
                'title': article['title'],
                'url': article['url'],
                'description': article.get('description', ''),
                'content': article.get('content', '')
            })
    
    return articles

# Example usage
# keywords = ["military", "transgender recruits"]
# related_articles = get_related_articles_news_api(keywords)
# print("Related Articles:", related_articles)
