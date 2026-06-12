from database import db, base
from sqlalchemy import create_engine, Column, String, Integer


#  criando as classes dos flashes cards
class FlashCard(base):
    __tablename__ = "FlashCards"

    id = Column(
        Integer, primary_key=True, autoincrement=True
    )  # id do flashcard para garantir que cada um seje único
    frente = Column(String, nullable=False)
    fundo = Column(String, nullable=True)
    categoria = Column(String, nullable=True)

    def __init__(self, frente, fundo, categoria):
        self.frente = frente
        self.fundo = fundo
        self.categoria = categoria
