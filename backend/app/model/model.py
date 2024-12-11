import joblib
from scipy.sparse import hstack

class ModelHandler():
    def __init__(self):
        # load the model
        self.model = joblib.load("./app/model/joblib/logistic_regression_model.joblib")
        self.headline_vectorizer = joblib.load("./app/model/joblib/headline_tfidf_vectorizer.joblib")
        self.body_vectorizer = joblib.load("./app/model/joblib/body_tfidf_vectorizer.joblib")
        print("All models and vectorizers loaded successfully")
        
    def predict_stance(self, headline: str, body: str) -> str:
       # Preprocess inputs
        preprocessed_headline = preprocess_text(headline)
        preprocessed_body = preprocess_text(body)

        # Extract features
        headline_vector = headline_vectorizer.transform([preprocessed_headline])
        body_vector = body_vectorizer.transform([preprocessed_body])
        word_overlap = extract_word_overlap([headline], [body])
        cosine_similarity = extract_cosine_similarity([headline], [body])

        # Combine features
        combined_features = hstack([headline_vector, body_vector, word_overlap.T, cosine_similarity.T])

        # Predict stance
        stance = logistic_model.predict(combined_features)[0]
        return stance
    
    def predict_stance_Iterate_batch(self, news_list: List[ScrapedNewsType]) -> List[dict]:
        results = []
        for news in news_list:
            if news.title and news.description:
                # Call the existing method for each item
                stance = self.predict_stance(news.title, news.description)
                probabilities = self.model.predict_proba(hstack([headline_vector, body_vector]))[0]

                # Append the result with probabilities and label
                results.append({
                    "title": news.title,
                    "domain": news.domain,
                    "predicted_label": stance,
                    "probabilities": {
                        "real": float(probabilities[0]),
                        "fake": float(probabilities[1])
                    }
                })
        return results

    
    def predict_stance_batch(self, news_list: List[ScrapedNewsType]) -> List[dict]:
        results = []
        feature_list = []

        # Preprocess and extract features for all news articles
        for news in news_list:
            if news.title and news.description:
                preprocessed_headline = preprocess_text(news.title)
                preprocessed_body = preprocess_text(news.description)

                # Extract features
                headline_vector = self.headline_vectorizer.transform([preprocessed_headline])
                body_vector = self.body_vectorizer.transform([preprocessed_body])
                word_overlap = extract_word_overlap([news.title], [news.description])
                cosine_similarity = extract_cosine_similarity([news.title], [news.description])

                # Combine features and store in list
                combined_features = hstack([headline_vector, body_vector, word_overlap.T, cosine_similarity.T])
                feature_list.append(combined_features)

        # Stack all features
        combined_features = coo_matrix.vstack(feature_list)

        # Predict probabilities (softmax applied)
        probabilities = self.model.predict_proba(combined_features)
        softmax_probabilities = [softmax(prob) for prob in probabilities]

        # Append results with probabilities and predicted labels
        for i, news in enumerate(news_list):
            if news.title and news.description:
                label = self.model.classes_[np.argmax(softmax_probabilities[i])]
                results.append({
                    "title": news.title,
                    "domain": news.domain,
                    "predicted_label": label,
                    "probabilities": {
                        "real": float(softmax_probabilities[i][0]),
                        "fake": float(softmax_probabilities[i][1])
                    }
                })
        
        return results