import secrets
from datetime import datetime, timedelta, timezone

from fastapi import Request, Depends, Response
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.crud.user import user_crud
from app.exceptions import (BearerTokenException, ForbiddenException,
                            HeaderAuthorizationException,
                            IncorrectEmailOrPasswordException,
                            NoJwtException,
                            NoUserException,
                            TokenExpiredException)
from app.users.models import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    """Хеширование пароля."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка совпадения паролей."""
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: EmailStr, password: str) -> User:
    """Аутентификация пользователя."""
    user = await user_crud.find_one_or_none(email=email)
    if (
        user and
        user.is_active and
        verify_password(plain_password=password,
                        hashed_password=user.password)
    ):
        return user
    raise IncorrectEmailOrPasswordException


def generate_auth_token() -> str:
    """Генерация внутреннего токена аутентификации."""
    return secrets.token_urlsafe(32)


async def create_access_token(user_id: int) -> str:
    """Созание токена для аутентификации пользователя."""
    internal_token = generate_auth_token()
    jwt_payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=30),
        'internal_token': internal_token
    }
    await user_crud.set_token(user_id=user_id, internal_token=internal_token)
    auth_data = settings.get_auth_data
    access_token = jwt.encode(jwt_payload,
                              auth_data['secret_key'],
                              algorithm=auth_data['algorithm'])
    return access_token


def get_access_token(request: Request) -> str:
    """Извлечение JWT токен из заголовка Authorization запроса, или cookies."""
    token = request.cookies.get('access_token')
    if token:
        return token
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise HeaderAuthorizationException
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise BearerTokenException
    return parts[1]


def verify_access_token(access_token: str = Depends(get_access_token)) -> str:
    """Проверка токена пользователя."""
    try:
        auth_data = settings.get_auth_data
        payload = jwt.decode(access_token,
                             auth_data['secret_key'],
                             algorithms=[auth_data['algorithm']])
    except JWTError:
        raise NoJwtException
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException
    internal_token = payload.get('internal_token')
    if not internal_token:
        raise NoJwtException
    return internal_token


async def get_current_user(internal_token: str = Depends(verify_access_token)):
    """Получить текущего пользователя."""
    user = await user_crud.find_one_or_none(auth_token=internal_token)
    if not user:
        raise NoUserException
    return user


async def logout(response: Response,
                 user: User = Depends(get_current_user)) -> User:
    """Выйти из системы."""
    await user_crud.delete_token(internal_token=user.auth_token)
    response.delete_cookie(key='access_token')
    return user


async def get_current_admin_user(
        current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        return current_user
    raise ForbiddenException
