from fastapi import status, HTTPException

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь с таким email уже зарегистрирован')

NoDataUpdateException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Пустое тело запроса")

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Неверная почта или пароль')

HeaderAuthorizationException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Отсутствует заголовок Authorization')

BearerTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=(
        'Неверный формат заголовка Authorization. Ожидается: Bearer <token>'))

TokenExpiredException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail='JWT токен истек, получите новый')

NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail='Токен не валидный!')

InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Недействительный токен, пройдите аутентификацию')

BunnedUserException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Вам запрещен доступ к ресурсу, обратитесь к администратору')

ForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                   detail='Недостаточно прав!')

UserNotFoundException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Пользователь не найден")
