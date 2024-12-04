from pydantic import BaseModel
from typing import Literal

class InputNewsType(BaseModel):
    category: Literal["text", "link"] # defines allowed values for category
    content: str # content will be in string format(text or url)
    
class OutputNewsType(BaseModel):
    label: Literal["real", "fake"]