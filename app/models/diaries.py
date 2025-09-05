from tortoise import fields

from app.models.base import BaseModel
from app.models.users import User


class Diary(BaseModel):
    title: str = fields.CharField(required=True, max_length=255)
    content: str = fields.TextField(required=True, max_length=255)
    created_at = fields.DatetimeField(required=True, auto_now=True)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="diaries", on_delete=fields.CASCADE
    )