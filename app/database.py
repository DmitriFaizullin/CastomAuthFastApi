from datetime import datetime

from typing import Annotated
from sqlalchemy import func, text
from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    AsyncAttrs)
from sqlalchemy.orm import (DeclarativeBase,
                            declared_attr,
                            Mapped,
                            mapped_column)

from app.config import settings

engine = create_async_engine(settings.get_db_url)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(),
                                               onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
bool_true = Annotated[bool, mapped_column(default=True,
                                          server_default=text('true'))]
bool_false = Annotated[bool, mapped_column(default=False,
                                           server_default=text('false'))]


class Base(AsyncAttrs, DeclarativeBase):
    """Базовая модель."""
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
