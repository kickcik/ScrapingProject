from pydantic import BaseModel


class QuoteResponse(BaseModel):
    content: str
    author: str
