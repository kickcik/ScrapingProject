from tortoise import fields

from app.models.base import BaseModel


class Question(BaseModel):
    question_text: str = fields.CharField(required=True, max_length=255)