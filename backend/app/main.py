from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .Types.types import InputNewsType, OutputNewsType
from .services.webScrap import extract_news_from_meta
from .services.serper import fetch_news_from_serper
from .process import m_main
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Get the frontend URL from the environment, defaulting to localhost if not set
frontend_url = os.getenv("frontend_url", "http://localhost:5173")

# CORS configuration (update the allowed origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/verify-news", response_model=OutputNewsType)
async def verify_news(news: InputNewsType):
    try:
        category = news.category
        content = news.content
        url_extracted_news = ""
        
        # ----------------------------------
        if category == "url":
            try:
                fetchedNews = extract_news_from_meta(content)
                if not fetchedNews or not fetchedNews.title:
                    raise ValueError("Failed to extract title from URL.")
                url_extracted_news = fetchedNews.title
                print("Input URL extracted", url_extracted_news)
            except Exception as e:
                print(f"Error extracting content from URL: {e}")
                raise HTTPException(status_code=400, detail="Invalid or inaccessible URL.")
        # ----------------------------------
        
        result = await m_main(content)
        relatedNews = await fetch_news_from_serper(url_extracted_news)

        # Return the result (fake or real) and some related news
        return OutputNewsType(label=result, relatedNews=relatedNews)
    
    except HTTPException as http_exc:
        # Re-raise HTTPExceptions for FastAPI to handle
        raise http_exc
    except Exception as e:
        # Catch-all for unexpected errors
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the request.")


# Simple endpoint to check if the backend is up and running
@app.get("/connection-status")
async def connection_status():
    return {"status": "true"}

@app.get("/")
async def root():
    return {"message": "Fake New Detection Backend is running"}