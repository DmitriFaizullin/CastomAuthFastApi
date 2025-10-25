from app.crud.user import user_crud
from app.exceptions import UserAlreadyExistsException


async def validate_email_uniqueness(email: str) -> bool:
    """Валидатор уникальности email"""
    user = user_crud.find_one_or_none(email=email)
    if user:
        raise UserAlreadyExistsException
    return True
