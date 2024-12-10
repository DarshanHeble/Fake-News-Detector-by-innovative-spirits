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