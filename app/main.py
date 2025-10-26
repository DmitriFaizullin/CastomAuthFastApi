from fastapi import FastAPI

from app.routers import main_router

app = FastAPI(
    title='Тестовое задание на позицию junior python development',
    description=('Реализация backend с собственной '
                 'системой аутентификации и авторизации')
)

app.include_router(main_router)
