import joblib
import numpy as np
from scipy.sparse import hstack, coo_matrix, vstack
from typing import List
from ..Types.types import ScrapedNewsType
from .featureExtraction import preprocess, extract_word_overlap, extract_cosine_similarity

class ModelHandler():
    def __init__(self):
        # load the model
        self.model = joblib.load("./app/model/joblib/logistic_regression_model.joblib")
        self.headline_vectorizer = joblib.load("./app/model/joblib/headline_tfidf_vectorizer.joblib")
        self.body_vectorizer = joblib.load("./app/model/joblib/body_tfidf_vectorizer.joblib")
        print("All models and vectorizers loaded successfully")
        
    def predict_stance(self, headline: str, body: str) -> dict:
        # Preprocess inputs
        preprocessed_headline = " ".join(preprocess(headline))
        preprocessed_body = " ".join(preprocess(body))

        # Extract features
        headline_vector = self.headline_vectorizer.transform([preprocessed_headline])
        body_vector = self.body_vectorizer.transform([preprocessed_body])
        word_overlap = extract_word_overlap([headline], [body])
        cosine_similarity = extract_cosine_similarity([headline], [body])

        # Combine features
        combined_features = hstack([headline_vector, body_vector, word_overlap.T, cosine_similarity.T])

        # Predict stance and probabilities
        stance = self.model.predict(combined_features)[0]
        probabilities = self.model.predict_proba(combined_features)[0]

        return {
            "predicted_label": stance,
            "probabilities": {
                "real": float(probabilities[0]),
                "fake": float(probabilities[1])
            }
        }

    
    def predict_stance_with_Iterate_batch(self, news_list: List[ScrapedNewsType]) -> list[dict]:
        results = []
        for news in news_list:
            if news.title and news.description:
                # Fetch description dynamically for each headline if needed
                description = self.fetch_description(news.title)
                
                # Predict using the existing method
                prediction = self.predict_stance(news.title, description)
                
                # Append the result
                results.append({
                    "title": news.title,
                    "domain": news.domain,
                    **prediction
                })
        return results

    
    def predict_stance_batch(self, news_list: List[ScrapedNewsType]) -> List[dict]:
        results = []
        feature_list = []
    
        # Preprocess and extract features for all news articles
        for news in news_list:
            if news.title and news.description:  # Ensure both title and description are available
                preprocessed_headline = " ".join(preprocess(news.title))
                preprocessed_body = " ".join(preprocess(news.description))
    
                # Extract features
                headline_vector = self.headline_vectorizer.transform([preprocessed_headline])
                body_vector = self.body_vectorizer.transform([preprocessed_body])
                word_overlap = extract_word_overlap([news.title], [news.description])
                cosine_similarity = extract_cosine_similarity([news.title], [news.description])
    
                # Combine features and store in list
                combined_features = hstack([headline_vector, body_vector, word_overlap.T, cosine_similarity.T])
                feature_list.append(combined_features)
    
        # Stack all features
        combined_features = vstack(feature_list)
    
        # Predict probabilities
        probabilities = self.model.predict_proba(combined_features)
    
        # Append results with probabilities and predicted labels
        for i, news in enumerate(news_list):
            if news.title and news.description:
                label = self.model.classes_[np.argmax(probabilities[i])]
                results.append({
                    "title": news.title,
                    "description": news.description,
                    "predicted_label": label,
                    "probabilities": {
                        "real": float(probabilities[i][0]),
                        "fake": float(probabilities[i][1])
                    }
                })
        
        return results



    def softmax(self,x):
        e_x = np.exp(x - np.max(x))  # Subtract max(x) for numerical stability
        return e_x / e_x.sum(axis=0)
