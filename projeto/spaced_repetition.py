# aqui vai ser calculadom o espacamento entre a exibicao de um card e outro

from models.card import Card
from datetime import timedelta, date


# funcao para calcular as a data da proxima revisao baseado na nota do user
def calcular_revisao(nota: int, card):
    if nota == 1:
        card.proxima_revisao = date.today() + timedelta(days=1)
    elif nota == 2:
        card.proxima_revisao = date.today() + timedelta(days=2)
    elif nota == 3:
        card.proxima_revisao = date.today() + timedelta(days=3)
    elif nota == 4:
        card.proxima_revisao = date.today() + timedelta(days=4)
    else:
        card.proxima_revisao = date.today() + timedelta(days=5)

    # atualiza o ease_factor baseado na nota
    if nota <= 2:
        card.ease_factor = max(1.3, card.ease_factor - 0.2)
    elif nota == 3:
        card.ease_factor = max(1.3, card.ease_factor - 0.1)
    elif nota == 5:
        card.ease_factor = card.ease_factor + 0.1

    return card
