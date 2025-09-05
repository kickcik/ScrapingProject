from tortoise import Model, fields

from app.models.base import BaseModel


class User(BaseModel, Model):
    username = fields.CharField(unique=True, max_length=255)
    password_hash = fields.CharField(max_length=255)

    class Meta:
        table = "users"
