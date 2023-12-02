from sqlalchemy import String, Column
from passlib.hash import pbkdf2_sha512

from .base import BaseModel


class User(BaseModel):

    email: str = Column(String(255), unique=True, nullable=False)
    password: str = Column(String(512), nullable=False)

    def __init__(self, password, **kwargs) -> None:
        super().__init__(**kwargs)
        self.password = pbkdf2_sha512.hash(password)

    def verify(self, password: str) -> bool:
        return pbkdf2_sha512.verify(password, self.password)
