from tortoise import Model, fields

from app.models.base import BaseModel
from app.models.quotes import Quote
from app.models.users import User


class Bookmark(BaseModel, Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="bookmarks", on_delete=fields.CASCADE
    )
    quote: fields.ForeignKeyRelation[Quote] = fields.ForeignKeyField(
        "models.Quote", related_name="bookmarks", on_delete=fields.CASCADE
    )

    class Meta:
        table = "bookmarks"
