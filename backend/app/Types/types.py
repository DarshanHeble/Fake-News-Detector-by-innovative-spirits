from pydantic import BaseModel, Field
from typing import Literal, Optional

# will update this class in future
class InputNewsType(BaseModel):
    category: Literal["text", "url"] = Field(..., description="The category which will be either 'text' or 'url'")
    content: str # content will be in string format(text or url)

# will update this class in future
class OutputNewsType(BaseModel):
    label: Literal["real", "fake"] = Field(..., description="The classification label for the news article. 'real' indicates the article is truthful, while 'fake' indicates false information.")

class ScrapedNewsType(BaseModel):
    title: Optional[str] = Field(None, description="The headline or title of the news article.")
    description: Optional[str] = Field(None, description="The description or summary of the news article.")
    # published_at: Optional[str] = Field(None, description="The published date and time of the news article.")     # Not need for our current use case
    # domain: Optional[str] = Field(None, description="The domain link of the link.")                               # Not need for our current use case

class FetchedNewsType(BaseModel):
    link: Optional[str] = Field(None, description="The link to the news article.")
    # title: Optional[str] = Field(None, description="The title of the news article.")                              # Not need for our use case
    # domain: Optional[str] = Field(None, description="The domain link of the link.")                               # Not need for our use case