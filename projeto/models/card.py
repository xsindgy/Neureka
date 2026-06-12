# models card.py

from sqlalchemy import ForeignKey, Column, Integer, String, Float, Date
from database import base
from datetime import date


class Card(base):
    __tablename__ = "Cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    deck_id = Column(Integer, ForeignKey("Decks.id"))
    frente = Column(String)
    fundo = Column(String)
    categoria = Column(String)
    nota = Column(Integer, nullable=True)
    ease_factor = Column(
        Float, default=2.5
    )  # controla a 'facilidade' e a frequencia que o card aparecera
    proxima_revisao = Column(
        Date, default=date.today
    )  # controla quando sera a pproxima revisao
