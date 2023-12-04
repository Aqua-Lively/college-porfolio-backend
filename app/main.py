from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Нужен для разворачивания БД.
# т.к. в нём хранится информация
# о структуре всех таблиц
from .config.db import Base

# Движок для подключения к БД
from .config.db import engine

# Подключаем роутеры
from .routers import works, authors, types

app = FastAPI(
    title='College Portfolio Api',
    docs_url='/documentation',
    redoc_url=None
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

origins = [
    'http://localhost',
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Создаём в базе данных таблицы по моделям.
# Если таблицы у нас уже есть, то ничего не произойдёт
Base.metadata.create_all(bind=engine)

# Добавляем подключённый роутер в обьект app
app.include_router(works.router)
app.include_router(authors.router)
app.include_router(types.router)
