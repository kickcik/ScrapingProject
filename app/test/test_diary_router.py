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
            ["app.models.diaries", "app.models.users", "app.models.token_blacklist"],  # 모델이 정의된 모듈 경로
            db_url=DB_URL,  # 메모리 DB 사용
        )
        super().setUpClass()
        print(DB_URL)

    @classmethod
    def tearDownClass(cls) -> None:
        finalizer()
        super().tearDownClass()

    async def test_create_diary(self) -> None:
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

            diary_create_response = await client.post(
                "/diaries/create",
                json={
                    "title": (title := "test_title"),
                    "content": (content := "test_content"),
                },
                headers={"Authorization": f"Bearer {access_token}"},
            )
        self.assertEqual(201, diary_create_response.status_code)
        response_body = diary_create_response.json()
        self.assertEqual(response_body["title"], title)
        self.assertEqual(response_body["content"], content)

    async def test_update_diary(self) -> None:
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

            diary_create_response = await client.post(
                "/diaries/create",
                json={
                    "title": "test_title",
                    "content": "test_content",
                },
                headers={"Authorization": f"Bearer {access_token}"},
            )
            diary_id = diary_create_response.json()["id"]

            diary_update_response = await client.patch(
                "/diaries/update",
                json={
                    "id": diary_id,
                    "title": (title := "updated_title"),
                    "content": (content := "updated_content"),
                },
                headers={"Authorization": f"Bearer {access_token}"},
            )
        self.assertEqual(200, diary_update_response.status_code)
        response_body = diary_update_response.json()
        self.assertEqual(response_body["title"], title)
        self.assertEqual(response_body["content"], content)

    async def test_delete_diary(self) -> None:
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

            diary_create_response = await client.post(
                "/diaries/create",
                json={
                    "title": "test_title",
                    "content": "test_content",
                },
                headers={"Authorization": f"Bearer {access_token}"},
            )
            diary_id = diary_create_response.json()["id"]

            diary_delete_response = await client.delete(
                f"/diaries/delete/{diary_id}",
                headers={"Authorization": f"Bearer {access_token}"},
            )
        self.assertEqual(204, diary_delete_response.status_code)

    async def test_get_diaries(self) -> None:
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

            await client.post(
                "/diaries/create",
                json={
                    "title": (title1 := "test_title"),
                    "content": (content1 := "test_content"),
                },
                headers={"Authorization": f"Bearer {access_token}"},
            )
            await client.post(
                "/diaries/create",
                json={
                    "title": (title2 := "test_title"),
                    "content": (content2 := "test_content"),
                },
                headers={"Authorization": f"Bearer {access_token}"},
            )

            get_diaries_response = await client.get("/diaries", headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, get_diaries_response.status_code)
        response_body = get_diaries_response.json()
        self.assertEqual(response_body[0]["title"], title1)
        self.assertEqual(response_body[0]["content"], content1)
        self.assertEqual(response_body[1]["title"], title2)
        self.assertEqual(response_body[1]["content"], content2)

    async def test_get_diary(self) -> None:
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

            create_diary_response = await client.post(
                "/diaries/create",
                json={
                    "title": (title := "test_title"),
                    "content": (content := "test_content"),
                },
                headers={"Authorization": f"Bearer {access_token}"},
            )
            diary_id = create_diary_response.json()["id"]

            get_diary_response = await client.get(
                f"/diaries/{diary_id}",
                headers={"Authorization": f"Bearer {access_token}"},
            )
        self.assertEqual(200, get_diary_response.status_code)
        response_body = get_diary_response.json()
        self.assertEqual(response_body["title"], title)
        self.assertEqual(response_body["content"], content)
