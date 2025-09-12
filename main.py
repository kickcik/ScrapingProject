import uvicorn
from fastapi import FastAPI

from app.configs.database import initialize_tortoise
from app.routers.bookmark_router import bookmark_router
from app.routers.diary_router import diary_router
from app.routers.quote_router import quote_router
from app.routers.user_router import user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(diary_router)
app.include_router(quote_router)
app.include_router(bookmark_router)

initialize_tortoise(app=app)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
