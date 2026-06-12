# aqui ficará o agrupamento das cartas, por exemplo, cada carta vai pertencer a um baralho e aqui serão criados os baralhos

from database import db, base
from sqlalchemy import Column, String, Integer
from sqlalchemy import DateTime
from datetime import datetime


# criando as classes, são o que todos os decks obrigatoriamente devem ter
class Deck(base):
    __tablename__ = "Decks"

    id = Column(
        Integer, primary_key=True, autoincrement=True
    )  # id do flashcard para garantir que cada um seje único
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.now)

    def __init__(self, titulo, descricao):
        self.titulo = titulo
        self.descricao = descricao
