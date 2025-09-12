import os
import random

import httpx
from dotenv import load_dotenv
from tortoise.contrib.test import TestCase, finalizer, initializer

from app.models.bookmarks import Bookmark
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


class TestBookmarkRouter(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        initializer(
            ["app.models.users", "app.models.token_blacklist", "app.models.bookmarks"],  # 모델이 정의된 모듈 경로
            db_url=DB_URL,  # 메모리 DB 사용
        )
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        finalizer()
        super().tearDownClass()

    async def test_create_bookmark(self) -> None:
        for i in range(1, 101):
            await Quote.create(content=f"테스트 명언 {i}", author=f"Author{i}")

        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            create_user_response = await client.post(
                "/users/register",
                json={
                    "username": "tester",
                    "password": "1234",
                },
            )
            user_id = int(create_user_response.json()["id"])
            login_response = await client.post(
                "/users/login",
                data={
                    "username": "tester",
                    "password": "1234",
                },
            )
            access_token = login_response.json()["access_token"]
            quote_id = random.randint(1, 100)

            create_bookmark_response = await client.post(
                f"/bookmarks/create/{quote_id}",
                headers={"Authorization": f"Bearer {access_token}"},
            )
        self.assertEqual(201, create_bookmark_response.status_code)
        response_body = create_bookmark_response.json()

        print(response_body)
        self.assertEqual(user_id, response_body["id"])
        self.assertEqual(quote_id, response_body["quote"]["id"])

        quote = await Quote.get(id=response_body["quote"]["id"])
        self.assertEqual(quote.content, response_body["quote"]["content"])
        self.assertEqual(quote.author, response_body["quote"]["author"])

    async def test_get_bookmarks(self) -> None:

        for i in range(1, 101):
            await Quote.create(content=f"테스트 명언 {i}", author=f"Author{i}")

        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            await client.post(
                "/users/register",
                json={
                    "username": "tester",
                    "password": "1234",
                },
            )
            login_response = await client.post(
                "/users/login",
                data={
                    "username": "tester",
                    "password": "1234",
                },
            )
            access_token = login_response.json()["access_token"]
            quote_id_first = random.randint(1, 100)
            quote_id_second = quote_id_first % 100 + 1

            await client.post(
                f"/bookmarks/create/{quote_id_first}",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            await client.post(
                f"/bookmarks/create/{quote_id_second}",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            get_bookmarks_response = await client.get(
                "/bookmarks",
                headers={"Authorization": f"Bearer {access_token}"},
            )
        self.assertEqual(200, get_bookmarks_response.status_code)
        response_body = get_bookmarks_response.json()

        for idx, response in enumerate(response_body, 0):
            bookmark = await Bookmark.get(id=idx + 1)
            quote = await bookmark.quote
            self.assertEqual(response["id"], bookmark.id)
            self.assertEqual(response["quote"]["id"], quote.id)
            self.assertEqual(response["quote"]["content"], quote.content)
            self.assertEqual(response["quote"]["author"], quote.author)

    async def test_delete_bookmarks(self) -> None:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            for i in range(1, 101):
                await Quote.create(content=f"테스트 명언 {i}", author=f"Author{i}")
                # print(f'{quote.id}, {quote.content}, {quote.author}')
            await client.post(
                "/users/register",
                json={
                    "username": "tester1",
                    "password": "1234",
                },
            )
            login_response = await client.post(
                "/users/login",
                data={
                    "username": "tester1",
                    "password": "1234",
                },
            )
            access_token = login_response.json()["access_token"]
            quotes = await Quote.all()
            quote_id = random.choice(quotes).id

            crate_bookmark_response = await client.post(
                f"/bookmarks/create/{quote_id}",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            bookmark_id = int(crate_bookmark_response.json()["id"])
            delete_bookmark_response = await client.delete(
                f"/bookmarks/{bookmark_id}", headers={"Authorization": f"Bearer {access_token}"}
            )
        self.assertEqual(204, delete_bookmark_response.status_code)
