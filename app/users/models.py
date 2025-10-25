from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, str_uniq, int_pk, bool_false, bool_true


class User(Base):
    """Модель пользователя."""
    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str_uniq]
    password: Mapped[str]
    is_user: Mapped[bool_true]
    is_admin: Mapped[bool_false]
    is_active: Mapped[bool_true]
    auth_token: Mapped[str] = mapped_column(nullable=True)

    extend_existing = True
