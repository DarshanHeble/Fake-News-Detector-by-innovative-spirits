import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Optional
from ..Types.types import ScrapedNewsType

def extract_news_from_meta(url: str) -> Optional[ScrapedNewsType]:
    """
    Extract metadata (title, description, domain) from a URL.

    Args:
        url: The URL of the webpage to scrape.

    Returns:
        ScrapedNewsType object or None if scraping fails.
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise error for non-200 status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract domain
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        # Extract title
        title_tag = soup.find('meta', property='og:title') or soup.find('title')
        title_text = (
            title_tag['content'] if title_tag and title_tag.has_attr('content') else
            title_tag.string if title_tag else
            "Title not available"
        )

        # Extract description
        description_tag = soup.find('meta', property='og:description') or soup.find('meta', attrs={'name': 'description'})
        description_text = (
            description_tag['content'] if description_tag and description_tag.has_attr('content') else
            "Description not available"
        )

        # Construct and return the ScrapedNewsType object
        return ScrapedNewsType(
            title=title_text.strip(),
            description=description_text.strip(),
            domain=domain
        )

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {url} - {e}")
    except Exception as e:
        print(f"Error scraping article: {url} - {e}")

    return None
