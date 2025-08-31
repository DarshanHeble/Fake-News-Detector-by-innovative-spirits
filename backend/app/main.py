from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .Types.types import (
    InputNewsType,
    OutputNewsType,
    InputMessageType,
    RelatedNewsType,
)
from .services.webScrap import extract_news_from_meta
from .services.extractKeywords import extract_keywords_yake
from .services.serper import search_news_with_serper
from .services.gemini import verify_text_with_gemini
from .useGem import gem_main
from .process import m_main
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()


# Helper function to sanitize input text
def sanitize_text(text: str) -> str:
    # Remove zero-width spaces and other problematic characters
    return text.replace("\u200b", "").replace("\ufeff", "").strip()


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
        content = sanitize_text(news.content)

        # ----------------------------------
        if category == "url":
            try:
                fetchedNews = extract_news_from_meta(content)
                if not fetchedNews or not fetchedNews.title:
                    raise ValueError("Failed to extract title from URL.")
                # Sanitize the extracted title
                sanitized_title = sanitize_text(fetchedNews.title)
                verdict = await m_main(content)
                keywords = extract_keywords_yake(sanitized_title)
                relatedNews = search_news_with_serper(keywords)
                return OutputNewsType(
                    label=verdict,
                    relatedNews=relatedNews,
                )
            except Exception as e:
                print(
                    f"Error extracting content from URL or m_main: {str(e).encode('utf-8', 'replace').decode('utf-8')}"
                )
                raise HTTPException(
                    status_code=400, detail="Invalid or inaccessible URL."
                )
        # ----------------------------------

        # Call gem_main for stance analysis
        gem_result = await gem_main(content)
        verdict = gem_result["verdict"]
        relatedNews = gem_result["relevant_news"]

        # Return the result (fake or real) and some related news
        return OutputNewsType(
            label=verdict,
            relatedNews=relatedNews,
        )

    except HTTPException as http_exc:
        # Re-raise HTTPExceptions for FastAPI to handle
        raise http_exc
    except Exception as e:
        # Catch-all for unexpected errors
        print(f"Unexpected error: {str(e).encode('utf-8', 'replace').decode('utf-8')}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the request.",
        )


# Simple endpoint to check if the backend is up and running
@app.get("/connection-status")
async def connection_status():
    return {"status": "true"}


@app.get("/")
async def root():
    return {"message": "Fake News Detection Backend is running"}


@app.post("/verify-message", response_model=OutputNewsType)
async def verify_message(message: InputNewsType):
    try:
        content = sanitize_text(message.content)
        verdict = await verify_text_with_gemini(content)
        # Since we are only verifying text, we can return an empty list for related news
        return OutputNewsType(
            label=verdict,
            relatedNews=[],
        )
    except Exception as e:
        print(f"Unexpected error: {str(e).encode('utf-8', 'replace').decode('utf-8')}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the request.",
        )
