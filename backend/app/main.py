from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .Types.types import InputNewsType, OutputNewsType
from .model.model import ModelHandler
from .services.webScrap import extract_headline_from_meta
from .services.fetchNewsFromGoogle import fetchNewsFromGoogle

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

# CORS configuration (update the allowed origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# verify news end point starts here
@app.post("/verify-news", response_model=OutputNewsType)
async def verify_news(news: InputNewsType):
    category = news.category
    content = news.content
    
    if (category == "url"):
        fetchedNews = extract_headline_from_meta(content)
        content = fetchedNews.description
        
    results = fetchNewsFromGoogle(content)
        
    return OutputNewsType(label="fake")

# Checking connection status manually
@app.get("/connection-status")
async def connection_status():
    return {"status": "true"}

@app.get("/")
async def root():
    return {"message": "Fake New Detection Backend is running"}