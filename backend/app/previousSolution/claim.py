import requests
from bs4 import BeautifulSoup
from typing import List

def fetch_headlines(query: str) -> List[str]:
    """Fetches article headlines from Google News based on the search query."""
    url = f"https://www.google.com/search?q={query}&tbm=nws"  # tbm=nws for news results
    headers = {
        "User -Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    #selecting the headlines from the google news
    headlines = []
    results = soup.find_all('h3')  # Assuming headlines are in <h3> tag
    for result in results:
        headlines.append(result.get_text())

    return headlines