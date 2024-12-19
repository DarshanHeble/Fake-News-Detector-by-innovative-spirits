from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .preprocessAndVectorize import preprocess_and_vectorize_with_bert
from ..Types.types import ScrapedNewsType, ScrapedNewsTypeWithStance
from typing import List, Optional

def analyze_stance(claim: str, articles: List[ScrapedNewsType]) -> Optional[List[ScrapedNewsTypeWithStance]]:
    print("Analyzing Stance...")
    
    """
    Analyzes the stance of articles relative to a claim based on cosine similarity of BERT embeddings.

    Args:
        claim: The claim text.
        articles: A list of ScrapedNewsType objects.

    Returns:
        A list of ScrapedNewsWithStance objects, or None if an error occurs.
        Returns the original list of articles if it is empty.
    """
    
    if not articles:
        print("No Articles provided")
        return articles
    
    # Preprocess and vectorize claim and article content
    similarities = preprocess_and_vectorize_with_bert(claim, articles)
    print("Similarites",similarities)
    
    if similarities is None:
        print("Error calculating similarities. Stance analysis failed.")
        return None
    
    # Classify based on similarity score thresholds
    stance_labels: List[str] = []
    
    for similarity in similarities:
        if similarity > 0.75:
            stance_labels.append('Agree')
        elif similarity > 0.4:
            stance_labels.append('Discuss')
        elif similarity > 0.1:
            stance_labels.append('Unrelated')
        else:
            stance_labels.append('Disagree')
    
    if len(stance_labels) != len(articles):
        print("Error: Number of stances does not match number of articles.")
        return None
    
    articles_with_stance: List[ScrapedNewsTypeWithStance] = []
    # Add stance to article information
    # for i, article in enumerate(articles):
    #     article['stance'] = stance[i]
    
    for i, article in enumerate(articles):
        articles_with_stance.append(ScrapedNewsTypeWithStance(
            title = article.title,
            description = article.description,
            domain=article.domain,
            stance=stance_labels[i]
        ))

    
    # print(articles_with_stance)
    return articles_with_stance
