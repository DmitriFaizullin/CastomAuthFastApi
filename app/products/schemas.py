from decimal import Decimal
from pydantic import BaseModel


class SProductResponse(BaseModel):
    """Схема ответа на запрос списка продуков."""
    id: int
    name: str
    category: str
    price: Decimal


class SProductAdd(BaseModel):
    """Схема тела запроса для добавления продука."""
    name: str
    category: str
    price: Decimal
