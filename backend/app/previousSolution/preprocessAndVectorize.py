from transformers import DistilBertTokenizer, DistilBertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
from ..Types.types import ScrapedNewsType
from typing import Optional, List

# Load the tokenizer and model for DistilBERT
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')

def get_embeddings(texts: List[str]):
    """Generates embeddings for a list of texts using DistilBERT."""
    try:
        inputs = tokenizer(texts, return_tensors='pt', truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        
        return None

def preprocess_and_vectorize_with_bert(claim: str, articles: List[ScrapedNewsType]):
    print("Preprocessing and vectorizing articles...")
    
    """
    Preprocesses a claim and a list of articles, calculates embeddings, and returns cosine similarities.

    Args:
        claim: The claim text.
        articles: A list of ScrapedNewsType objects.

    Returns:
        A list of cosine similarities between the claim and each article.
        Returns an empty list if no articles are provided.
        Returns None if an error occurs during embedding generation.
    """
    
    if not articles:
        return []
    
    try:
        # Preprocess the claim and articles text
        texts = [claim] + [article.description if article.description else "" for article in articles]
        
        # Ensure all inputs are strings
        if not all(isinstance(text, str) for text in texts):
            raise ValueError("All inputs must be strings.")
        
        # Get embeddings for claim and articles
        embeddings = get_embeddings(texts)
        if embeddings is None:
            return None

        # Calculate cosine similarities between the claim and articles
        claim_embedding = embeddings[0].unsqueeze(0)  # Get the claim embedding
        article_embeddings = embeddings[1:]  # All the article embeddings

        similarities = [cosine_similarity(claim_embedding, article_embedding.unsqueeze(0))[0][0] for article_embedding in article_embeddings]

        return similarities
    except Exception as e:
        print(f"An error occurred during processing: {e}")
        return None


# Example usage:
# claim = "Example claim text to fact-check."
# similarities = preprocess_and_vectorize_with_bert(claim, related_articles)
# print("Similarity Scores:", similarities)
