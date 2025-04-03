import requests
from bs4 import BeautifulSoup
import re
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)

# List of reputable news sources
REPUTABLE_SOURCES = [
    "bbc.com",
    "cnn.com",
    "reuters.com",
    "nytimes.com",
    "theguardian.com",
    "www.msn.com",
    "forbes.com",
    "wsj.com",
    "aljazeera.com",
    "npr.org",
    "abcnews.go.com",
]


def clean_text(text):
    """Clean the input text by removing HTML tags and special characters."""
    text = re.sub(r"<.*?>", "", text)  # Remove HTML tags
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters and numbers
    return text.lower().strip()  # Normalize to lowercase and strip whitespace


def baadkar_scrape(statement):
    """Scrape news headlines from Google based on the search statement."""
    url = f"{statement}"  # -- tbm=nws for news results

    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return [], []

    soup = BeautifulSoup(response.text, "html.parser")

    # Find news results (adjust the selector based on the actual HTML structure)
    results = soup.find_all("div")  # Adjust class as needed
    links = soup.find_all("a", href=True)  # Extract links from the search results

    fetched_data = [clean_text(result.text) for result in results]
    fetched_links = [link["href"] for link in links if "href" in link.attrs]
    # print(f'-----------{fetched_data}-------{fetched_links}---------') just for Testing purpose

    return fetched_data, fetched_links


def classify_news(headlines, links):
    """Classify news headlines based on keywords and reputable sources."""
    fake_keywords = [
        "hoax",
        "fake",
        "scam",
        "unbelievable",
        "shocking",
        "you won't believe",
        "exclusive",
        "breaking",
        "urgent",
        "bizarre",
        "conspiracy",
        "revealed",
    ]

    for headline, link in zip(headlines, links):
        # Check if the link is from a reputable source
        if any(source in link for source in REPUTABLE_SOURCES):
            continue  # Skip reputable sources
        elif any(keyword.lower() in headline.lower() for keyword in fake_keywords):
            return "fake"  # Return immediately if a fake news indicator is found

    return "real"  # Default to real news if no fake indicators found


async def m_main(statement):
    # statement = input("Enter the News Text or URL ")
    result, links = baadkar_scrape(statement)

    if result:
        # Classify the fetched headlines
        classification = classify_news(result, links)
        print(classification)
        return classification
    else:
        print("No results found.")
        return "neutral"


# Main execution
# if __name__ == "__main__":
#     statement = input("Enter the News Topic or Keyword: ")
#     result, links = baadkar_scrape(statement)

#     if result:
#         # Classify the fetched headlines
#         labels = classify_news(result, links)


#         # Vectorization
#         vectorizer = TfidfVectorizer()
#         X = vectorizer.fit_transform(result)  # Vectorize the headlines
#         y = np.array(labels)  # Convert labels to numpy array

#         # Train a simple classifier (Random Forest in this case)
#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#         classifier = RandomForestClassifier()
#         classifier.fit(X_train, y_train)

#         # Evaluate the classifier
#         accuracy = classifier.score(X_test, y_test)
#         print(f"Model Accuracy: {accuracy:.2f}")

#         # Classify the fetched headlines
#         predictions = classifier.predict(X)
#         for headline, prediction in zip(result, predictions):
#             classification = "Fake News" if prediction == 1 else "Real News"
#             print(f"{classification}: {headline}")
#     else:
#         print("No results found.")

# async def get_headlines_and_links(
#     keywords_or_string: Union[List[str], str], start: int = 1, num: int = 10
# ) -> Tuple[List[str], List[str]]:
#     """
#     Fetches and scrapes news articles, returning their headlines and links.

#     Args:
#         keywords_or_string: A list of keywords or a single string to form the search query.

#     Returns:
#         A tuple containing two lists:
#         - List of headlines (str).
#         - List of links (str).
#     """
#     print("Fetching and scraping news articles...")
#     scraped_articles = await fetch_and_scrape_news_from_google(keywords_or_string)

#     # Extract headlines and links from scraped articles
#     headlines = [article.title for article in scraped_articles if article.title]
#     links = [article.link for article in scraped_articles if article.link]

#     print(f"Extracted {len(headlines)} headlines and {len(links)} links.")
#     return headlines, links
