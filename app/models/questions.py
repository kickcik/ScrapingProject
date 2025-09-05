from tortoise import Model, fields

from app.models.base import BaseModel


class Question(BaseModel, Model):
    question_text = fields.CharField(required=True, max_length=255)

    class Meta:
        table = "questions"
