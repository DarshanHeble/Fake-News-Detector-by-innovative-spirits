from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .Types.types import InputNewsType, OutputNewsType


# Initialize FastAPI app
app = FastAPI()

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
    print(news)
    
    # Fake output for testing
    return OutputNewsType(label="fake")

# Checking connection status manually
@app.get("/connection-status")
async def connection_status():
    return {"status": "true"}

@app.get("/")
async def root():
    return {"message": "Fake New Detection Backend is running"}