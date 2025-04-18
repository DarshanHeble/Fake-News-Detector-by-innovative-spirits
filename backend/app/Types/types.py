from pydantic import BaseModel, Field
from typing import Literal, Optional, List


class ScrapedNewsType(BaseModel):
    """
    Represents scraped news data with title, description, and domain.

    Attributes:
        title: The headline or title of the news article (optional).
        description: The description or summary of the news article (optional).
        domain: The domain of the article's source (optional).
        link: The link of the article source(Optional)
    """

    title: Optional[str] = Field(
        None, description="The headline or title of the news article."
    )
    description: Optional[str] = Field(
        None, description="The description or summary of the news article."
    )
    domain: Optional[str] = Field(
        None, description="The domain of the link."
    )  # Not need for our current use case
    link: Optional[str] = Field(None, description="The link of the news")
    # published_at: Optional[str] = Field(None, description="The published date and time of the news article.")     # Not need for our current use case


class ScrapedNewsTypeWithStance(ScrapedNewsType):
    stance: Optional[str] = Field(
        None, description="The stance of the news article towards the claim"
    )


class FetchedNewsType(BaseModel):
    """
    Represents fetched news data containing a link and domain.

    Attributes:
        link: The link to the news article (optional).
        domain: The domain link of the link.
        title: The title of the news article (optional).
        snippet: A short excerpt or summary of the article (optional).
        source: The source or publisher of the article (optional).
    """

    link: Optional[str] = Field(None, description="The link to the news article.")
    title: Optional[str] = Field(None, description="The title of the news article.")
    snippet: Optional[str] = Field(
        None, description="A short excerpt or summary of the article."
    )
    source: Optional[str] = Field(
        None, description="The source or publisher of the article."
    )


# will update this class in future
class InputNewsType(BaseModel):
    category: Literal["text", "url"] = Field(
        ..., description="The category which will be either 'text' or 'url'"
    )
    content: str  # content will be in string format(text or url)


class OutputNewsType(BaseModel):
    label: Literal["real", "fake", "neutral"] = Field(
        ...,
        description="The classification label for the news article. 'real' indicates the article is truthful, while 'fake' indicates false information.",
    )
    relatedNews: List[dict] = Field(
        None, description="Related articles based on the news"
    )
    # keywordCheck: str = Field(
    #     ..., description="The result of the keyword-based check (real, fake, or neutral)."
    # )
