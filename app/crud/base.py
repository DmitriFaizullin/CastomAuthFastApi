from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update as sqlalchemy_update
from typing import TypeVar

from app.database import async_session_maker, Base

T = TypeVar('T', bound=Base)


class CRUDBase:
    """Базовый класс методов CRUD."""
    def __init__(self, model: type[T]) -> None:
        """Инициализирует переменные класса CRUDBase."""
        self.model = model

    async def find_one_or_none(self, **filter_by):
        """Вернуть объект модели согласно фильтрам."""
        async with async_session_maker() as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def add(self, **values):
        """Добавить объект модели."""
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = self.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    async def update(self, filter_by, **values):
        """Обновить объект модели."""
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    sqlalchemy_update(self.model)
                    .where(*[getattr(self.model, k) == v
                             for k, v in filter_by.items()])
                    .values(**values)
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result

    async def find_all(self, **filter_by):
        async with async_session_maker() as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()
