from fastapi import FastAPI

from app.users.router import auth_router, admin_router, user_router
from app.products.router import product_router
from app.carts.router import cart_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)

app.include_router(product_router)
app.include_router(cart_router)
