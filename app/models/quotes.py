from tortoise import Model, fields

from app.models.base import BaseModel


class Quote(BaseModel, Model):
    content = fields.TextField(required=True)
    author = fields.CharField(required=True, max_length=255)

    class Meta:
        table = "quotes"
