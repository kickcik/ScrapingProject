from tortoise import Model, fields

from app.models.base import BaseModel
from app.models.users import User


class Diary(BaseModel, Model):
    title = fields.CharField(required=True, max_length=255)
    content = fields.TextField(required=True, max_length=255)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="diaries", on_delete=fields.CASCADE
    )

    class Meta:
        table = "diaries"
