from collections import Counter
from .getReliabilityScore import get_reliability_score
from ..Types.types import ScrapedNewsTypeWithStance
from typing import List

def aggregate_weighted_stance(articles: List[ScrapedNewsTypeWithStance]) -> str:
    print("Aggregating Weighted Stance...")
    
    """
    Aggregates the stances of articles based on weighted reliability scores.

    Args:
        articles: A list of ScrapedNewsWithStance objects.

    Returns:
        "real" if the majority weighted stance is "Agree",
        "fake" if the majority weighted stance is "Disagree",
        "neutral" if the majority weighted stance is "Discuss" or "Unrelated" or if the input list is empty,
        "neutral" if there is a tie.
    """
    
    if not articles:
        print("No articles provided.")
        return "Neutral" # Return neutral for empty input
    
    weighted_stance_counts = Counter()
    
    for article in articles:
        stance = article.stance
        
        if stance is None:
            continue  # Skip this article if stance is None
        
        source = article.domain or "Unknown"  # Use 'domain' or a fallback value
        reliability_score = get_reliability_score(source)
        weighted_stance_counts[stance] += reliability_score
    
    print("Weighted Stance Counts:", weighted_stance_counts)
    
    # Determine majority stance based on weighted scores
    most_common_stance, highest_score = weighted_stance_counts.most_common(1)[0]
    
    # Apply thresholds for decision
    if highest_score >= 2.5 and most_common_stance == "Agree":
        return "real"
    elif highest_score >= 2.5 and most_common_stance == "Disagree":
        return "fake"
    else:
        return "neutral"

# Example usage
# result = aggregate_weighted_stance(analyzed_articles)
# print(result)
