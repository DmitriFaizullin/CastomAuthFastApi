from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update as sqlalchemy_update
from typing import cast

from app.crud.base import CRUDBase
from app.users.models import User
from app.database import async_session_maker


class UserCRUD(CRUDBase):
    """CRUD модели user."""
    def __init__(self, model) -> None:
        super().__init__(model)
        self.user_model = cast(User, self.model)

    async def delete_user(self, user_id):
        """Мягкое удаление пользователя."""
        async with async_session_maker() as session:
            async with session.begin():
                user_query = select(self.model).where(
                    self.user_model.id == user_id)
                user_result = await session.execute(user_query)
                user = user_result.scalar_one_or_none()
                if not user:
                    raise HTTPException(
                        status_code=404,
                        detail='Пользователь не найден'
                    )
                query = (
                    sqlalchemy_update(self.model)
                    .where(self.user_model.id == user_id)
                    .values(is_active=False)
                )
                await session.execute(query)
                try:
                    await session.commit()
                    return True
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

    async def set_token(self, user_id, internal_token):
        """Сохранить внутренний токен в системе."""
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    sqlalchemy_update(self.model)
                    .where(self.user_model.id == user_id)
                    .values(auth_token=internal_token)
                )

                await session.execute(query)
                try:
                    await session.commit()
                    return True
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

    async def delete_token(self, internal_token):
        """Удалить внутренний токен из системы."""
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    sqlalchemy_update(self.model)
                    .where(self.user_model.auth_token == internal_token)
                    .values(auth_token=None)
                )

                await session.execute(query)
                try:
                    await session.commit()
                    return True
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e


user_crud = UserCRUD(User)
