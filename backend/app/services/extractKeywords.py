import yake


def extract_keywords_yake(text: str, top_n: int = 15, strict: bool = False) -> list:
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
        keywordsData = kw_extractor.extract_keywords(text)
        keywords = [kw[0] for kw in keywordsData[:top_n]]
        # print(keywords, "\n")
        # ['Challenges Waqf Amendment', 'Waqf Amendment Bill', 'Owaisi Challenges Waqf', 'Supreme Court', 'Religious Affairs']

        if strict:
            # Strip single quotes and split
            flattened_keywords = [
                word.strip("'") for phrase in keywords for word in phrase.split()
            ]
            # Remove duplicate keywords
            seen = set()
            unique_keywords = []
            for word in flattened_keywords:
                if word not in seen:
                    seen.add(word)
                    unique_keywords.append(word)

            unique_keywords = unique_keywords[:top_n]
            print(unique_keywords)
            return unique_keywords
        else:
            return keywords[:top_n]
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []


# Example usage
# text = "Owaisi Challenges Waqf Amendment Bill In Supreme Court; Says It Strips Muslims Of Right To Manage Their Own Religious Affairs"
# extract_keywords_yake(text, strict=True)
