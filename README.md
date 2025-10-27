# <p style="text-align:center">API интернет-магазина</p>
***
### Описание проекта.

Проект API интернет-магазина с системой аутентификации, управления товарами и корзиной покупок.
Выполнен в соответствии с тестовым заданием на позицию стажера python backend development.
Проект разработан с использованием фреймворка FastApi.
В проекте реализована собственная система аутентификации и авторизации без использования встроенных
возможностей FastApi.
Пользователя аутентифицируется по запросу на адрес /auth/login/ с email и паролем.
В ответ пользователь получает токент авторизации. Токен вешается в cooke браузера.
При авторизации пользователя токен получается из cooke и выдается соответствующий ресурс
по запросу. Так же токен можно передать в заголовке запроса поле Authorization ```Bearer <token>```.
Токен содержит информацию о времени истечения действия, а так же внутренний токен,
который хранится в базе данных для соответствующего пользователя.
При проверке внутреннего токена определяется пользователь, для которого он назначен и данные
пользователя (is_user, is_admin, is_active). Пользователь admin может поменять данные другого
пользователя: is_user - пользователь забанен, is_active - пользователь удален.
Забаненый или удаленный пользователь имеет доступ тольколько к открытым ресурсам
(не требуют аутентификации). При выходе пользователя из системы токен авторизации удаляется
из cooke браузера, кроме того внутренний токен так же удаляется у соответствующего пользователя,
дальнейшая авторизация с этим токеном невозможна. Ниже приведены эндпоинты
проекта с указанием категории разрешения для него.
***
### Использованные технологии.
Backend: Django 3.2
- API: FastApi
- Аутентификация: кастомная с использование библиотеки jose
- База данных: PostgreSQL
- Контейнеризация: Docker (контейнер базы данных)
***
### Запуск приложения локально.
1. Предварительные требования для запуска проекта
Python 3.11+
pip (менеджер пакетов Python)

2. Клонирование репозитория
```git clone git@github.com:DmitriFaizullin/CastomAuthFastApi.git```
```cd CastomAuthFastApi/```

3. Создание виртуального окружения
```python -m venv venv```
```source venv/bin/activate  # Linux/MacOS```
или
```venv\Scripts\activate  # Windows```

4. Установка зависимостей
```pip install -r requirements.txt```

5. Запуск контейнека с базой данных
Запустить Docker
Создать в дериктории /CastomAuthFastApi файл .env с такими данными
```DB_HOST=localhost```
```DB_PORT=5432```
```DB_NAME=postgres_db```
```DB_USER=admin```
```DB_PASSWORD=password```
```SECRET_KEY=secret_megakey```
```ALGORITHM=HS256```

6. Выполнить миграции
```alembic upgrade head```

7. Запуск сервера разработки
```uvicorn app.main:app```

При запуске приложения в базу данных добавится 4 пользователя
с одинаковым паролем 'password'.

"email": "user1@example.com",
"first_name": "User1",
"last_name": "User1",
"is_admin": false,
"is_user": true,
"is_active": true,

"email": "user2@example.com",
"first_name": "User2",
"last_name": "User2",
"is_admin": false,
"is_user": false,
"is_active": true,

"email": "user3@example.com",
"first_name": "User3",
"last_name": "User3",
"is_admin": false,
"is_user": true,
"is_active": false,

"email": "admin@example.com",
"first_name": "admin",
"last_name": "admin",
"is_admin": true,
"is_user": true,
"is_active": true,

Документация доступна по адресу: http://localhost:8000/docs
***
### Эндпоинты API.
##### Аутентификация
POST /auth/register/ - регистрация пользователя (any user)
POST /auth/login/ - аутентификация пользователя (any user)
POST /auth/logout/ - выход из системы (auth user)

##### Пользователь
GET /user/me/ - данные текущего пользователя (auth user)
DELETE /user/me/ - мягкое удаление пользователя (пользователь не активен) (auth user)
PATCH /user/me/ - редактирование данных текущего пользователя (auth user)

##### Администратор
GET /admin/users/ - список всех пользователей (admin user)
POST /admin/users/permitions/{user_id}/ - изменение прав доступа пользователя (admin user)

##### Товары
GET /products/all/ - получить все товары (any user)
GET /products/{product_id}/ - получить конкретный товар (any user)
POST /products/add_product/ - добавить товар (admin user)

##### Корзина
GET
/cart/me/ - корзина текущего пользователя (auth user)
DELETE /cart/product/{product_id}/ - удалить товар из корзины пользователя (auth user)
POST /cart/product/{product_id}/ - добавить товар в корзину пользователя (auth user)
***
Тестовый проект выполнил
Файзуллин Дмитрий Андреевич
Ссылка на страницу [GitHub](https://github.com/DmitriFaizullin/).
