from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .Types.types import InputNewsType, OutputNewsType
from .model.model import ModelHandler
from .services.webScrap import extract_news_from_meta
from .services.getNews import getRelatedNews
from .mithun import m_main
from .AD import ad_main
from dotenv import load_dotenv
import os

load_dotenv()

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
app = FastAPI(on_startup=[on_startup], on_shutdown=[on_shutdown])
app = FastAPI()

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
        
        # ----------------------------------
        if category == "url":
            try:
                fetchedNews = extract_news_from_meta(content)
                if not fetchedNews or not fetchedNews.title:
                    raise ValueError("Failed to extract title from URL.")
                content = fetchedNews.title
                print("Input URL extracted", content)
            except Exception as e:
                print(f"Error extracting content from URL: {e}")
                raise HTTPException(status_code=400, detail="Invalid or inaccessible URL.")
        # ----------------------------------
        
        approaches = {
            "mithun": m_main,  # Function for "mithun" approach
            "AD": ad_main      # Function for "AD" approach
        }
        
        approach = "AD"     # Add the desired approach
        
        # Get the corresponding function based on the approach
        result = ""
        if approach in approaches:
            result = await approaches[approach](content)  # Call the respective function
        else:
            raise ValueError(f"Unknown approach: {approach}")
        
        relatedNews = await getRelatedNews(content)

        return OutputNewsType(label=result, relatedNews=relatedNews)
    
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