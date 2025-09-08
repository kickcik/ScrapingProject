import os

import httpx
from dotenv import load_dotenv
from tortoise.contrib.test import TestCase, finalizer, initializer

from main import app

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_TEST_DB = os.getenv("MYSQL_TEST_DB")  # 테스트 전용 DB 권장

# f-string으로 DB URL 구성
DB_URL = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_TEST_DB}"


class TestUserRouter(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        initializer(
            ["app.models.users"],  # 모델이 정의된 모듈 경로
            db_url=DB_URL,  # 메모리 DB 사용
        )
        super().setUpClass()
        print(DB_URL)

    @classmethod
    def tearDownClass(cls) -> None:
        finalizer()
        super().tearDownClass()

    async def test_api_create_user(self) -> None:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            user_create_response = await client.post(
                "/users/register",
                json={
                    "username": "tester",
                    "password": "1234",
                },
            )
        self.assertEqual(200, user_create_response.status_code)

    async def test_api_create_user_exist(self) -> None:
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
            user_create_response = await client.post(
                "/users/register",
                json={
                    "username": "tester",
                    "password": "4321",
                },
            )
        self.assertEqual(400, user_create_response.status_code)
        response_body = user_create_response.json()
        self.assertEqual("User already exists", response_body["detail"])

    async def test_api_login_user(self) -> None:
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
        self.assertEqual(200, login_response.status_code)
        response_body = login_response.json()
        self.assertIsNotNone(response_body["access_token"])
        self.assertIsNotNone(response_body["refresh_token"])
        self.assertIsNotNone(response_body["token_type"], "Bearer")
