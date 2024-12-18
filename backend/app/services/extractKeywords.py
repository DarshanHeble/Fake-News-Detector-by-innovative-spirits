from rake_nltk import Rake
from typing import List, Optional

# Initialize Rake outside the function for efficiency
r = Rake()

def extract_keywords(text: str, top_n: int = 10) -> Optional[List[str]]:
    """
    Extracts the top N ranked keywords from a given text using RAKE.

    Args:
        text: The input text.
        top_n: The number of top keywords to return (default: 10).

    Returns:
        A list of the top N ranked keywords (phrases), or None if an error occurs.
        Returns an empty list if the input text is empty or None.
        If top_n is greater than the number of keywords found, it returns all keywords found.
    Raises:
        ValueError: If top_n is not a positive integer.
    """
    
    if not text:  # Check for empty or None input
        return []
    
    if not isinstance(top_n, int) or top_n <= 0:
        raise ValueError("top_n must be a positive integer.")

    try:
        r.extract_keywords_from_text(text)
        keywords = r.get_ranked_phrases()
        print("Extracted Keywords",keywords[:top_n])
        return keywords[:top_n]
    except Exception as e:
        print(f"An error occurred during keyword extraction: {e}")
        return None
    
# Example usage
# headline = "Artificial Intelligence (AI) is transforming industries by automating processes, enhancing decision-making, and creating new opportunities. However, ethical concerns, such as data privacy and bias, need to be addressed."
# keywords = extract_keywords(headline, 5)
# print(keywords)