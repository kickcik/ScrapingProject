from pydantic import BaseModel

from app.schemas.quotes import QuoteResponse


class BookmarkResponse(BaseModel):
    id: int
    user_id: int
    quote: QuoteResponse

    model_config = {"from_attributes": True}
