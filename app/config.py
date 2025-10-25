import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки проекта."""
    DB_HOST: str = 'DB_HOST'
    DB_PORT: int = 5433
    DB_NAME: str = 'DB_NAME'
    DB_USER: str = 'DB_USER'
    DB_PASSWORD: str = 'HOST'
    SECRET_KEY: str = 'SECRET_KEY'
    ALGORITHM: str = 'HS256'

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              '..',
                              '.env')
    )

    @property
    def get_db_url(self):
        return (f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@'
                f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')

    @property
    def get_auth_data(self):
        return {'secret_key': self.SECRET_KEY, 'algorithm': self.ALGORITHM}


settings = Settings()
