from typing import Any

from .base import JSONModel, UUIDMixin, TimestampMixin, BaseModel


class UserPasswordMixin(BaseModel):
    password: str


class UserData(JSONModel, UserPasswordMixin):
    email: str


class User(UserData, UUIDMixin, TimestampMixin):
    def get_claims(self) -> dict[str, Any] | None:
        return {
            'email': self.email
        }
