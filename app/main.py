from fastapi import FastAPI

# Нужен для разворачивания БД.
# т.к. в нём хранится информация
# о структуре всех таблиц
from .config.db import Base

# Движок для подключения к БД
from .config.db import engine

# Подключаем роутеры
from .routers import works
from .routers import authors
from .routers import types


app = FastAPI(
    title='College Portfolio Api',
    docs_url='/documentation',
    redoc_url=None
)

# Создаём в базе данных таблицы по моделям.
# Если таблицы у нас уже есть, то ничего не произойдёт
Base.metadata.create_all(bind=engine)

# Добавляем подключённый роутер в обьект app
app.include_router(works.router)
app.include_router(authors.router)
app.include_router(types.router)
