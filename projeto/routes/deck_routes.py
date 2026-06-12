# aqui ficara todas as rotas dos decks

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.deck import Deck
from database import pegar_sessao
from schemas import DeckCreate

# criando a rota + adicionando o prefixo de todas as rotas relacionadas ao deck + tag 'deck'
deck_router = APIRouter(prefix="/deck", tags=["decks"])


@deck_router.get("/")
def listar_decks(sessao: Session = Depends(pegar_sessao)):
    return sessao.query(Deck).all()


@deck_router.post("/")
def criar_deck(deck: DeckCreate, sessao: Session = Depends(pegar_sessao)):
    novo_deck = Deck(titulo=deck.titulo, descricao=deck.descricao)
    sessao.add(novo_deck)
    sessao.commit()
    sessao.refresh(
        novo_deck
    )  # recarrega o deck criado no banco de dados, evitando com que chegue informacoes faltando
    return novo_deck
