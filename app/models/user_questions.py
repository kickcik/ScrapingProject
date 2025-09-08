from tortoise import Model, fields

from app.models.base import BaseModel
from app.models.questions import Question
from app.models.users import User


# id, user_id(FK), question_id(FK)
class UserQuestions(BaseModel, Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="questions", on_delete=fields.CASCADE
    )
    question: fields.ForeignKeyRelation[Question] = fields.ForeignKeyField(
        "models.Question", related_name="questions", on_delete=fields.CASCADE
    )
