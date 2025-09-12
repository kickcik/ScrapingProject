import os

import httpx
from dotenv import load_dotenv
from tortoise.contrib.test import TestCase, finalizer, initializer

from app.models.quotes import Quote
from main import app

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_TEST_DB = os.getenv("MYSQL_TEST_DB")  # 테스트 전용 DB 권장

# f-string으로 DB URL 구성
DB_URL = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_TEST_DB}"


class TestQuoteRouter(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        initializer(
            ["app.models.quotes"],  # 모델이 정의된 모듈 경로
            db_url=DB_URL,  # 메모리 DB 사용
        )
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        finalizer()
        super().tearDownClass()

    async def test_bring_quote(self) -> None:
        for i in range(1, 101):
            await Quote.create(content=f"테스트 명언 {i}", author=f"Author{i}")
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            bring_quote_response = await client.get("/quotes/bring")
        self.assertEqual(bring_quote_response.status_code, 200)
        response_body = bring_quote_response.json()
        quote = await Quote.get(id=response_body["id"])
        self.assertEqual(response_body["id"], quote.id)
        self.assertEqual(response_body["content"], quote.content)
        self.assertEqual(response_body["author"], quote.author)
