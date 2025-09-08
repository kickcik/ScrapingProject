from tortoise import Model, fields

from app.models.base import BaseModel
from app.models.users import User


class TokenBlacklist(BaseModel, Model):
    token = fields.CharField(max_length=255)
    expired_at = fields.DatetimeField(null=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="token_blacklist", on_delete=fields.CASCADE
    )

    class Meta:
        table = "token_blacklist"