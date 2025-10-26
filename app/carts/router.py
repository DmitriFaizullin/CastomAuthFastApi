from decimal import Decimal
from fastapi import APIRouter, Depends

from app.carts.schemas import SShoppingCart
from app.users.auth import get_current_user
from app.users.models import User

cart_router = APIRouter()


@cart_router.get('/me/', response_model=SShoppingCart)
async def get_shoppingcart(user: User = Depends(get_current_user)):
    """Получить корзину товаров пользователя."""
    products = [
        {'id': 1, 'name': 'Телевизор',
         'category': 'Электроника', 'price': Decimal('1000.0')},
        {'id': 2, 'name': 'Смартфон',
         'category': 'Электроника', 'price': Decimal('500.0')},
        {'id': 3, 'name': 'Штиблеты',
         'category': 'Одежда', 'price': Decimal('2.0')}
    ]
    cart_data = {
        'user_id': user.id,
        'products': products,
        'total_amount': Decimal('1502.0'),
        'total_quantity': 3
    }
    return cart_data


@cart_router.delete('/product/{product_id}/')
async def delete_product(product_id: int,
                         user: User = Depends(get_current_user)):
    """Удалить товар из корзины пользователя."""
    # логика удаления товара из корзины
    return {'message': f'товар {product_id} удален из корзины'}


@cart_router.post('/product/{product_id}/')
async def add_product(product_id: int,
                      user: User = Depends(get_current_user)):
    """Добавить товар в корзину пользователя."""
    # логика добавления товара в корзину
    return {'message': f'товар {product_id} добавлен в корзину'}
