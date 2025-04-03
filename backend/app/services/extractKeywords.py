import yake


def extract_keywords_yake(text: str, top_n: int = 10) -> list:
    """
    Extracts keywords using YAKE (fastest method) for searching news articles.

    Args:
        text: Input text (news headline, description, or content).
        top_n: Number of keywords to return.

    Returns:
        List of extracted keywords, or an empty list if an error occurs.
    """
    if not text or not isinstance(text, str):
        return []

    if not isinstance(top_n, int) or top_n <= 0:
        raise ValueError("top_n must be a positive integer.")

    try:
        kw_extractor = yake.KeywordExtractor(lan="en", n=3, top=top_n, dedupLim=0.9)
        keywords = kw_extractor.extract_keywords(text)

        return [kw[0] for kw in keywords]  # Extract only the keyword text
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []


# Example usage
# text = "Artificial Intelligence (AI) is transforming industries..."
# print(extract_keywords_yake(text, 5))
