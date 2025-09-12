import random

from fastapi import APIRouter

from app.models.quotes import Quote
from app.schemas.quotes import QuoteResponse

quote_router = APIRouter(prefix="/quotes", tags=["quotes"])


@quote_router.get("/bring", status_code=200)
async def get_quote() -> QuoteResponse:
    random_id = random.randint(1, 100)
    quote = await Quote.get(id=random_id)
    return QuoteResponse.model_validate(quote)
