import os

import httpx
from dotenv import load_dotenv
from tortoise.contrib.test import TestCase, finalizer, initializer

from app.models.questions import Question
from main import app

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_TEST_DB = os.getenv("MYSQL_TEST_DB")  # 테스트 전용 DB 권장

# f-string으로 DB URL 구성
DB_URL = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_TEST_DB}"


class TestQuestionRouter(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        initializer(
            [
                "app.models.questions",
                "app.models.user_questions",
                "app.models.users",
                "app.models.token_blacklist",
            ],  # 모델이 정의된 모듈 경로
            db_url=DB_URL,  # 메모리 DB 사용
        )
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        finalizer()
        super().tearDownClass()

    async def test_get_question(self) -> None:
        for i in range(1, 101):
            await Question.create(question_text=f"테스트  질문 {i}")
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

            get_question_response = await client.get(
                "/questions/bring",
                headers={"Authorization": f"Bearer {access_token}"},
            )
        self.assertEqual(get_question_response.status_code, 200)
