from decimal import Decimal
from typing import List
from pydantic import BaseModel

from app.products.schemas import SProductResponse


class SShoppingCart(BaseModel):
    """Схема ответа на запрос корзины товаров пользователя."""
    user_id: int
    products: List[SProductResponse]
    total_amount: Decimal
    total_quantity: int
