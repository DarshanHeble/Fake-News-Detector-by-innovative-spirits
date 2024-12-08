import joblib

class ModelHandler():
    def __init__(self):
        # load the model
        self.model = joblib.load("./vectorizers/logistic_regression_model.joblib")
        self.headline_vectorizer = joblib.load("./vectorizers/headline_tfidf_vectorizer.joblib")
        self.body_vectorizer = joblib.load("./vectorizers/body_tfidf_vectorizer.joblib")
        print("All models and vectorizers loaded successfully")
        
    def predict_stance(self, headline: str, body: str) -> str:
        print("Got data",headline, body)