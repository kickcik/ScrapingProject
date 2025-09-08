from tortoise import Model, fields

from app.models.base import BaseModel
from passlib.hash import bcrypt

class User(BaseModel, Model):
    username = fields.CharField(unique=True, max_length=255)
    password_hash = fields.CharField(max_length=255)

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password_hash)

    class Meta:
        table = "users"
