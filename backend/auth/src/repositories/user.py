from typing import Iterator
from sqlalchemy import select

from .base import BaseRepository
from ..db.user import User


class UserRepository(BaseRepository):

    async def all(self) -> Iterator[User]:
        async with self.session_factory() as session:
            query = select(User)
            users = await session.execute(query)
            return users.all()
        
    async def get(self, **kwargs) -> User:
        query = select(User)

        for key, value in kwargs.items():
            query = query.filter(getattr(User, key) == value)

        async with self.session_factory() as session:
            user = await session.execute(query)
            return user.scalar()

    async def one(self, **kwargs) -> User:
        user = await self.get(**kwargs)
        
        if not user:
            raise ValueError(f"User not found, '{kwargs}'")
        
        return user

    async def add(self, email: str, password: str, **kwargs) -> User:
        async with self.session_factory() as session:
            user = User(email=email, password=password, **kwargs)

            session.add(user)
            await session.commit()
            await session.refresh(user)

            return user

    async def delete(self, **kwargs) -> None:
        query = select(User)

        for key, value in kwargs.items():
            query = query.filter(getattr(User, key) == value)

        async with self.session_factory() as session:

            entity = await session.execute(query)
            
            if (user := entity.scalar()) is None:
                raise ValueError(f"User not found, '{kwargs}'")
            
            await session.delete(user)
            await session.commit()
