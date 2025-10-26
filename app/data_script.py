from typing import Any, Dict, List, Type, TypeVar

from sqlalchemy import select

from app.database import async_session_maker
from app.users.models import User
from app.users.auth import get_password_hash

password = get_password_hash('password')
USER_DATA = [
    {'first_name': 'User1', 'last_name': 'User1',
     'email': 'user1@example.com', 'password': password},
    {'first_name': 'User2', 'last_name': 'User2',
     'email': 'user2@example.com', 'password': password, 'is_user': False},
    {'first_name': 'User3', 'last_name': 'User3',
     'email': 'user3@example.com', 'password': password, 'is_active': False},
    {'first_name': 'admin', 'last_name': 'admin',
     'email': 'admin@example.com', 'password': password, 'is_admin': True}
]

Model = TypeVar('Model')


class DataLoader:
    """Класс для загрузки данных в базу данных."""
    @classmethod
    async def _bulk_insert(
        cls,
        session: Any,
        model: Type[Model],
        data: List[Dict[str, str]]
    ) -> None:
        """Вспомогательный метод для массовой загрузки данных."""
        session.add_all([model(**item) for item in data])
        await session.flush()

    @classmethod
    async def load_data(cls) -> None:
        """Загружает данные пользователя базу."""
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    result = await session.execute(select(User))
                    if result.scalars().all():
                        print('База не пустая, данные не загружены!')
                    else:
                        await cls._bulk_insert(session, User, USER_DATA)
                        print('Данные пользователя успешно загружены!')
        except Exception as e:
            print(f'Ошибка при загрузке данных: {e}')
