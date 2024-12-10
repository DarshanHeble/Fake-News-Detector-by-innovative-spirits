from pydantic import BaseModel,Field
from typing import Literal,Optional

# will update this class in future
class InputNewsType(BaseModel):
    category: Literal["text", "url"] # defines allowed values for category
    content: str # content will be in string format(text or url)
    
class OutputNewsType(BaseModel):
    label: Literal["real", "fake"] = Field(..., description="The classification label for the news article. 'real' indicates the article is truthful, while 'fake' indicates false information.")

class ScrapedNewsType(BaseModel):
    title: Optional[str] = Field(None, description="The headline or title of the news article.")
    description: Optional[str] = Field(None, description="The description or summary of the news article.")
    published_at: Optional[str] = Field(None, description="The published date and time of the news article.")

class FetchedNewsType(BaseModel):
    title: Optional[str] = Field(None, description="The title of the news article.")
    link: Optional[str] = Field(None, description="The link to the news article.")
    domain: Optional[str] = Field(None, description="The domain link of the link.")