from pydantic import BaseModel,Field
from typing import Literal,Optional

class InputNewsType(BaseModel):
    category: Literal["text", "url"] # defines allowed values for category
    content: str # content will be in string format(text or url)
    
class OutputNewsType(BaseModel):
    label: Literal["real", "fake"]

class FetchedNewsType(BaseModel):
    title: Optional[str] = Field(None, description="The headline or title of the news article.")
    description: Optional[str] = Field(None, description="The description or summary of the news article.")
    published_at: Optional[str] = Field(None, description="The published date and time of the news article.")
