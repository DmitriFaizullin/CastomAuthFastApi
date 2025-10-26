from typing import List
from fastapi import APIRouter, Depends

from app.products.schemas import SProductResponse, SProductAdd
from app.users.auth import get_current_admin_user


product_router = APIRouter()


@product_router.get("/all/", response_model=List[SProductResponse])
async def get_all_products():
    """Получить список товаров."""
    products = [
        {'id': 1, 'name': 'Телевизор',
         'category': 'Электроника', 'price': 1000.0},
        {'id': 2, 'name': 'Смартфон',
         'category': 'Электроника', 'price': 500.0},
        {'id': 3, 'name': 'Штиблеты', 'category': 'Одежда', 'price': 2.0}
    ]
    return products


@product_router.get('/{product_id}/', response_model=SProductResponse)
async def get_product(product_id: int):
    """Получить Товар по id."""
    product = {'id': product_id,
               'name': 'Телевизор',
               'category':
               'Электроника',
               'price': 1000.0}
    return product


@product_router.post('/add_product/',
                     response_model=SProductResponse,
                     dependencies=[Depends(get_current_admin_user)])
async def add_product(product_data: SProductAdd):
    """Добавить товар."""
    data_response = product_data.model_dump()
    data_response['id'] = 100500
    return data_response
