from tortoise import fields

from app.models.base import BaseModel


class Quote(BaseModel):
    content: str = fields.CharField(required=True, max_length=255)
    author: str = fields.CharField(required=True, max_length=255)