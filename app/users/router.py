from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.exc import IntegrityError

from app.crud.user import user_crud
from app.exceptions import NoDataUpdateException, UserAlreadyExistsException
from app.users.auth import (authenticate_user,
                            create_access_token, get_current_admin_user,
                            get_current_user,
                            get_password_hash,
                            logout)
from app.users.models import User
from app.users.schemas import (SUserAuth,
                               SUserRegister,
                               SUserUpdate,
                               SUserResponse)

auth_router = APIRouter(prefix='/auth', tags=['Аутентификация'])
user_router = APIRouter(prefix='/user', tags=['Пользователь'])
admin_router = APIRouter(prefix='/admin', tags=['Администратор'])


@auth_router.post('/register/')
async def register_user(user_data: SUserRegister) -> dict:
    """Регистрация пользователя."""
    user = await user_crud.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    user_dict = user_data.model_dump(exclude={'password_replay'})
    user_dict['password'] = get_password_hash(user_data.password)
    await user_crud.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}


@user_router.patch('/user/me/')
async def update_user(new_data: SUserUpdate,
                      user: User = Depends(get_current_user)):
    """Обновление пользователя."""
    update_data = new_data.model_dump(exclude_unset=True)
    if not update_data:
        raise NoDataUpdateException
    try:
        await user_crud.update(filter_by={'id': user.id}, **update_data)
    except IntegrityError:
        raise UserAlreadyExistsException
    return {'message': 'Данные пользователя успешно обновлены!'}


@user_router.delete('/user/me/')
async def delete_user(user: User = Depends(logout)):
    """Удаление пользователя."""
    await user_crud.delete_user(user_id=user.id)
    return {'message': 'Пользователь удален!'}


@auth_router.post('/login/')
async def auth_user(response: Response, user_data: SUserAuth):
    """Аутентификация пользователя."""
    user = await authenticate_user(email=user_data.email,
                                   password=user_data.password)
    access_token = await create_access_token(user.id)
    response.set_cookie(key='access_token', value=access_token)
    return {'ok': True,
            'access_token': access_token,
            'token_type': 'Bearer',
            'message': 'Авторизация успешна!'}


@auth_router.post('/logout/', dependencies=[Depends(logout)])
async def logout_user():
    """Выйти из системы."""
    return {'message': 'Пользователь успешно вышел из системы'}


@user_router.get("/users/",
                 response_model=List[SUserResponse],
                 dependencies=[Depends(get_current_admin_user)])
async def get_all_users():
    return await user_crud.find_all()


@user_router.get("/me/", response_model=SUserResponse)
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data
