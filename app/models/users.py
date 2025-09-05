from tortoise import fields

from app.models.base import BaseModel


class User(BaseModel):
    username: str = fields.CharField(unique=True)
    password_hash: str = fields.CharField(max_length=255)