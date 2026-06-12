# rotas das sessoes de estudos

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.card import Card
from database import pegar_sessao
from models.review import Review
from models.deck import Deck
from datetime import date
from spaced_repetition import calcular_revisao

session_router = APIRouter(prefix="/session", tags=["sessions"])


# exibir proximas revisoes
@session_router.get("/{deck_id}")
def exibir_proximas_revisoes(deck_id: int, sessao: Session = Depends(pegar_sessao)):
    return (
        sessao.query(Card)
        .filter(Card.deck_id == deck_id, Card.proxima_revisao <= date.today())
        .all()
    )


# receber nota do user
@session_router.post("/{card_id}/revisar")
def dar_nota(card_id: int, nota: int, sessao: Session = Depends(pegar_sessao)):
    buscar_card = sessao.query(Card).filter(Card.id == card_id).first()
    if buscar_card:
        calcular_revisao(nota, buscar_card)
        novo_review = Review(card_id=card_id, nota=nota)
        sessao.add(novo_review)
        sessao.commit()
        sessao.refresh(buscar_card)
        return buscar_card
    else:
        raise HTTPException(status_code=404, detail="Card não encontrado")
