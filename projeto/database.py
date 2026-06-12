# aqui vai ficar armazenado o todo o db do projeto!!!

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# carregando o db para a .env
load_dotenv()

# 1. banco de dados criado
database_url = os.getenv("DATABASE_URL")
db = create_engine(database_url)
base = declarative_base()


SessionLocal = sessionmaker(bind=db, autocommit=False, autoflush=False)


def pegar_sessao():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
