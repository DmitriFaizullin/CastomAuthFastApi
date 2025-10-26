from fastapi import FastAPI

from app.data_script import DataLoader
from app.routers import main_router

app = FastAPI(
    title='Тестовое задание на позицию junior python development',
    description=('Реализация backend с собственной '
                 'системой аутентификации и авторизации')
)

app.include_router(main_router)


@app.on_event('startup')
async def startup_event():
    """Загрузка тестовых данных при старте приложения."""
    await DataLoader.load_data()
