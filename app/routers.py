# app/api/routers.py
from fastapi import APIRouter

from app.carts.router import cart_router
from app.products.router import product_router
from app.users.router import (auth_router,
                              user_router,
                              admin_router)

main_router = APIRouter()

main_router.include_router(
    auth_router, prefix='/auth', tags=['Аутентификация'])
main_router.include_router(
    user_router, prefix='/user', tags=['Пользователь'])
main_router.include_router(
    admin_router, prefix='/admin', tags=['Администратор'])

main_router.include_router(
    product_router, prefix='/products', tags=['Товары'])

main_router.include_router(
    cart_router, prefix='/cart', tags=['Корзина'])
