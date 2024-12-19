from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .Types.types import InputNewsType, OutputNewsType
from .model.model import ModelHandler
from .services.webScrap import extract_news_from_meta
from .services.fetchNewsFromGoogle import fetchNewsFromGoogle
from .services.fetchNewsFromGoogle import fetch_and_scrape_news_from_google
from .previousSolution.analyseStance import analyze_stance
from .previousSolution.aggregateStance import aggregate_weighted_stance
from .services.getRelatedArticles import fetch_and_scrape_news_from_newsApi
from .services.extractKeywords import extract_keywords

# Define lifecycle event handlers
def on_startup():
    global model_handler
    model_handler = ModelHandler()
    print("Model Initialized")
    
def on_shutdown():
    global model_handler
    model_handler = None
    print("Model Uninitialized")

# Initialize FastAPI app
# app = FastAPI(on_startup=[on_startup], on_shutdown=[on_shutdown])
app = FastAPI()

# CORS configuration (update the allowed origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/verify-news", response_model=OutputNewsType)
async def verify_news(news: InputNewsType):
    try:
        category = news.category
        content = news.content
        
        # ----------------------------------
        if category == "url":
            try:
                fetchedNews = extract_news_from_meta(content)
                if not fetchedNews or not fetchedNews.title:
                    raise ValueError("Failed to extract title from URL.")
                content = fetchedNews.title
                print("Input URL extracted")
            except Exception as e:
                print(f"Error extracting content from URL: {e}")
                raise HTTPException(status_code=400, detail="Invalid or inaccessible URL.")
        # ----------------------------------
        
        # Extract keywords from content (User Inputted News)
        try:
            keywords = extract_keywords(content)
            if not keywords:
                raise ValueError("Failed to extract keywords.")
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            raise HTTPException(status_code=400, detail="Failed to extract keywords from the provided content.")
        
        # Fetch articles from NewsAPI
        try:
            articles = fetch_and_scrape_news_from_newsApi(keywords)
            print("Articles using NewsAPI:", articles)
        except Exception as e:
            print(f"Error fetching articles from NewsAPI: {e}")
            articles = []

        # Check if NewsAPI returned sufficient articles; fetch from Google if not
        if not articles or len(articles) < 3:
            try:
                print("Not enough articles found using NewsAPI. Fetching from Google search...")
                additional_articles = fetch_and_scrape_news_from_google(keywords)
                if additional_articles:
                    articles.extend(additional_articles)
            except Exception as e:
                print(f"Error fetching articles from Google search: {e}")
        
        if not articles:
            raise HTTPException(status_code=404, detail="No related articles found for the given content.")

        print("Final Articles List:", articles)
        
        # Analyze stance
        try:
            analyzed_articles_stances = analyze_stance(content, articles)
            print("Analyzed Stances:", analyzed_articles_stances)
        except Exception as e:
            print(f"Error analyzing stances: {e}")
            raise HTTPException(status_code=500, detail="Error analyzing stances of articles.")
        
        # Aggregate stances
        try:
            result = aggregate_weighted_stance(analyzed_articles_stances)
            print("Final Aggregated Stance:", result)
        except Exception as e:
            print(f"Error aggregating stance: {e}")
            raise HTTPException(status_code=500, detail="Error aggregating stances.")

        return OutputNewsType(label=result)
    
    except HTTPException as http_exc:
        # Re-raise HTTPExceptions for FastAPI to handle
        raise http_exc
    except Exception as e:
        # Catch-all for unexpected errors
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the request.")


# Checking connection status manually
@app.get("/connection-status")
async def connection_status():
    return {"status": "true"}

@app.get("/")
async def root():
    return {"message": "Fake New Detection Backend is running"}