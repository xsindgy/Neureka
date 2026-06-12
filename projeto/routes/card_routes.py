# aqui ficara todas as rotas dos cards
from models.card import Card
from schemas import CardCreate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import pegar_sessao

# criar rota dos cards
card_router = APIRouter(prefix="/card", tags=["cards"])


# get para listar todos os cards
@card_router.get("/")
def listar_card(sessao: Session = Depends(pegar_sessao)):
    return sessao.query(Card).all()


@card_router.post("/")
def criar_card(card: CardCreate, sessao: Session = Depends(pegar_sessao)):
    novo_card = Card(
        frente=card.frente,
        fundo=card.fundo,
        categoria=card.categoria,
        deck_id=card.deck_id,
    )
    sessao.add(novo_card)
    sessao.commit()
    sessao.refresh(
        novo_card
    )  # recarrega o card criado no banco de dados, evitando com que chegue informacoes faltando
    return novo_card


# aqui sera a parte responsavel por buscar um card especifico por meio do id
@card_router.get("/{id}")
def buscar_card(id: int, sessao: Session = Depends(pegar_sessao)):
    return sessao.query(Card).filter(Card.id == id).first()


# deletar card
@card_router.delete("/{id}")
def delete_card(id: int, sessao: Session = Depends(pegar_sessao)):
    card_encontrado = (
        sessao.query(Card).filter(Card.id == id).first()
    )  # faz uma busca para everiguar se o card existe
    if card_encontrado:
        sessao.delete(card_encontrado)
        sessao.commit()
    else:  # se nn existir, retornar erro com o httpexception
        raise HTTPException(status_code=404, detail="Card não encontrado")
