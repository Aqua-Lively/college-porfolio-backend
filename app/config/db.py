import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# загружаем файл .env
load_dotenv()

POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')

# подключаемся к базе данных
engine = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')


# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Определяем базовый класс
Base = declarative_base()

# Dependency (зависимость)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

# print(POSTGRES_HOST)
# print(POSTGRES_DB)
# print(POSTGRES_USER)
# print(POSTGRES_PORT)
# print(POSTGRES_PASSWORD)