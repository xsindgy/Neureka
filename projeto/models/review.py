# aqui o user vai poder ter as revisoes dos cards
from database import base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import DateTime
from datetime import datetime


class Review(base):
    __tablename__ = "Review"

    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(Integer, ForeignKey("Cards.id"))
    nota = Column(Integer, nullable=False)
    revisado_em = Column(DateTime, default=datetime.now)
