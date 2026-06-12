from pydantic import BaseModel  # forcar a tipagem de dados
from typing import Optional  # fazer com que informacoes sejam opicionais


class DeckCreate(
    BaseModel
):  # usar o basemodel para o pydantic validar automaticamente o tipo de dados que estao sendo inseridos
    titulo: str
    descricao: Optional[str] = None

    class Config:
        from_attributes = (
            True  # evitar com que a classe seja tratada como se fosse um dicionario
        )


# criar o schema dos cards
class CardCreate(BaseModel):
    frente: str
    fundo: str
    deck_id: int
    categoria: Optional[str] = None

    class Config:
        from_attributes = True
