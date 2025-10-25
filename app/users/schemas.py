from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, model_validator


class SUserBase(BaseModel):
    """Базовая схема пользователя."""
    first_name: str = Field(...,
                            min_length=1,
                            max_length=50,
                            description='Имя, от 1 до 50 символов')
    last_name: str = Field(...,
                           min_length=1,
                           max_length=50,
                           description='Фамилия, от 1 до 50 символов')
    email: EmailStr = Field(..., description='Электронная почта')


class SUserRegister(SUserBase):
    """Схема регистрации пользователя."""
    password: str = Field(...,
                          min_length=5,
                          max_length=50,
                          description='Пароль, от 5 до 50 знаков')
    password_replay: str = Field(...,
                                 min_length=5,
                                 max_length=50, description='Повтор пароля')

    @model_validator(mode='after')
    def check_passwords(self):
        if self.password != self.password_replay:
            raise ValueError('Пароли не совпадают')
        return self


class SUserUpdate(BaseModel):
    """Схема для обновления данных пользователя."""
    first_name: Optional[str] = Field(None,
                                      min_length=1,
                                      max_length=50,
                                      description="Имя, от 1 до 50 символов")
    last_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="Фамилия, от 1 до 50 символов")
    email: Optional[EmailStr] = Field(None, description="Электронная почта")


class SUserAuth(BaseModel):
    email: EmailStr = Field(..., description='Электронная почта')
    password: str = Field(...,
                          min_length=5,
                          max_length=50,
                          description='Пароль, от 5 до 50 знаков')


class SUserResponse(BaseModel):
    email: str
    first_name: str
    last_name: str
    is_admin: bool
    is_user: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
