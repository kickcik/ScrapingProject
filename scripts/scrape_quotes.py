import os

from bs4 import BeautifulSoup
from bs4.element import Tag
from dotenv import load_dotenv
from selenium import webdriver
from tortoise import Tortoise, run_async

from app.models.quotes import Quote


async def save_quotes(all_quotes: list[dict[str, Tag | None]]) -> None:
    await Tortoise.init(
        db_url=f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}",
        modules={"models": ["app.models.quotes"]},
    )

    for q in all_quotes:
        await Quote.create(content=q["content"], author=q["author"])
    await Tortoise.close_connections()


driver = webdriver.Chrome()

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

all_quotes = []
for page in range(1, 11):
    url = f"https://quotes.toscrape.com/page/{page}/"
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    quotes = soup.select(".quote")
    for q in quotes:
        if content := q.select_one(".text"):
            content = content.text.strip()

        if author := q.select_one(".author"):
            author = author.text.strip()

        all_quotes.append({"content": content, "author": author})

run_async(save_quotes(all_quotes))
