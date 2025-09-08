from fastapi import FastAPI

from app.configs.database import initialize_tortoise
from app.routers.user_router import user_router

app = FastAPI()

app.include_router(user_router)

initialize_tortoise(app=app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
