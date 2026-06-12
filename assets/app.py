# criando o front do projeto

import streamlit as st
import requests
from datetime import date

# url base da api
API_URL = "http://localhost:8000"

# adicionando o titulo
st.set_page_config(page_title="🧠 Neureka")


def get(url):
    try:
        resposta = requests.get(url)
        return resposta.json()
    except:
        st.error(
            "❌ Não foi possível conectar com a API. Verifique se o servidor está rodando."
        )
        st.stop()


def post(url, json=None, params=None):
    try:
        resposta = requests.post(url, json=json, params=params)
        return resposta.json()
    except:
        st.error(
            "❌ Não foi possível conectar com a API. Verifique se o servidor está rodando."
        )
        st.stop()


def delete(url):
    try:
        requests.delete(url)
    except:
        st.error(
            "❌ Não foi possível conectar com a API. Verifique se o servidor está rodando."
        )
        st.stop()


# pagina lateral com 4 opcoes
pagina = st.sidebar.radio(
    "Menu",
    ["Estudar agora", "Meus baralhos", "Novo card", "Deletar card", "Estatísticas"],
)

if pagina == "Estudar agora":
    st.title("🧠 Estudar agora")

    # buscar baralhos da API
    baralhos = get(f"{API_URL}/deck/")

    # extrair títulos pro selectbox
    titulos = [b["titulo"] for b in baralhos]
    baralho_escolhido = st.selectbox("Escolha um baralho", titulos)

    # pegar o id do baralho escolhido
    deck_id = next(b["id"] for b in baralhos if b["titulo"] == baralho_escolhido)

    # buscar cards devidos hoje
    cards = get(f"{API_URL}/session/{deck_id}")

    if not cards:
        st.success("✅ Nenhum card para revisar hoje nesse baralho!")
    else:
        # mostrar quantos cards faltam
        st.info(f"📚 {len(cards)} card(s) para revisar hoje")

        # pegar o primeiro card
        card = cards[0]

        st.subheader("Pergunta:")
        st.write(card["frente"])

        # botao pra revelar resposta
        if st.button("Revelar resposta"):
            st.subheader("Resposta:")
            st.write(card["fundo"])

            st.write("Como foi?")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if st.button("Errei (1)"):
                    post(f"{API_URL}/session/{card['id']}/revisar?nota=1")
                    st.rerun()
            with col2:
                if st.button("Difícil (2)"):
                    post(f"{API_URL}/session/{card['id']}/revisar?nota=2")
                    st.rerun()
            with col3:
                if st.button("Fácil (4)"):
                    post(f"{API_URL}/session/{card['id']}/revisar?nota=4")
                    st.rerun()
            with col4:
                if st.button("Ótimo (5)"):
                    post(f"{API_URL}/session/{card['id']}/revisar?nota=5")
                    st.rerun()

elif pagina == "Meus baralhos":
    st.title("📚 Meus baralhos")

    # listar decks existentes
    baralhos = get(f"{API_URL}/deck/")

    if not baralhos:
        st.info("Nenhum baralho criado ainda!")
    else:
        for b in baralhos:
            with st.expander(f"📖 {b['titulo']}"):
                st.write(f"**Descrição:** {b['descricao'] or 'Sem descrição'}")
                st.write(f"**Criado em:** {b['criado_em'][:10]}")

                # listar cards do deck
                cards = get(f"{API_URL}/card/")
                cards_do_baralho = [c for c in cards if c["deck_id"] == b["id"]]
                st.write(f"**Total de cards:** {len(cards_do_baralho)}")

    st.divider()
    st.subheader("➕ Criar novo baralho")

    titulo = st.text_input("Nome do baralho")
    descricao = st.text_input("Descrição (opcional)")

    if st.button("Criar baralho"):
        if titulo:
            post(
                f"{API_URL}/deck/",
                json={"titulo": titulo, "descricao": descricao or None},
            )
            st.success("✅ Baralho criado com sucesso!")
            st.rerun()
        else:
            st.error("❌ Digite um nome para o baralho!")

elif pagina == "Novo card":
    st.title("➕ Novo card")

    # buscar decks
    baralhos = get(f"{API_URL}/deck/")
    titulos = [b["titulo"] for b in baralhos]

    # formulario
    baralho_escolhido = st.selectbox("Baralho", titulos)
    deck_id = next(b["id"] for b in baralhos if b["titulo"] == baralho_escolhido)

    frente = st.text_input("Pergunta (frente do card)")
    fundo = st.text_input("Resposta (fundo do card)")
    categoria = st.text_input("Categoria (opcional)")

    if st.button("Criar card"):
        if frente and fundo:
            post(
                f"{API_URL}/card/",
                json={
                    "frente": frente,
                    "fundo": fundo,
                    "deck_id": deck_id,
                    "categoria": categoria or None,
                },
            )
            st.success("✅ Card criado com sucesso!")
        else:
            st.error("❌ Preencha a pergunta e a resposta!")

elif pagina == "Deletar card":
    st.title("🗑️ Deletar card")

    # buscar decks
    baralhos = get(f"{API_URL}/deck/")
    titulos = [b["titulo"] for b in baralhos]

    # escolher baralho pra filtrar os cards
    baralho_escolhido = st.selectbox("Filtrar por baralho", titulos)
    deck_id = next(b["id"] for b in baralhos if b["titulo"] == baralho_escolhido)

    # listar cards do deck escolhido
    cards = get(f"{API_URL}/card/")
    cards_do_baralho = [c for c in cards if c["deck_id"] == deck_id]

    if not cards_do_baralho:
        st.info("Nenhum card nesse baralho!")
    else:
        for c in cards_do_baralho:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{c['frente']}** — {c['fundo']}")
            with col2:
                if st.button("🗑️ Deletar", key=c["id"]):
                    delete(f"{API_URL}/card/{c['id']}")
                    st.success("✅ Card deletado!")
                    st.rerun()

elif pagina == "Estatísticas":
    st.title("📊 Estatísticas")

    # buscar todos os cards
    cards = get(f"{API_URL}/card/")
    baralhos = get(f"{API_URL}/deck/")

    if not cards:
        st.info("Nenhum card cadastrado ainda!")
    else:
        # metricas gerais
        total_cards = len(cards)
        cards_hoje = [c for c in cards if c["proxima_revisao"] <= str(date.today())]
        cards_dominados = [c for c in cards if c["ease_factor"] >= 2.7]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de cards", total_cards)
        with col2:
            st.metric("Para revisar hoje", len(cards_hoje))
        with col3:
            st.metric("Dominados", len(cards_dominados))

        st.divider()

        # cards por deck
        st.subheader("Cards por baralho")
        for b in baralhos:
            cards_do_baralho = [c for c in cards if c["deck_id"] == b["id"]]
            total = len(cards_do_baralho)
            dominados = len([c for c in cards_do_baralho if c["ease_factor"] >= 2.7])
            if total > 0:
                progresso = dominados / total
                st.write(f"**{b['titulo']}** — {dominados}/{total} dominados")
                st.progress(progresso)

        st.divider()

        # ease factor medio por deck
        st.subheader("Dificuldade média por baralho")
        for b in baralhos:
            cards_do_baralho = [c for c in cards if c["deck_id"] == b["id"]]
            if cards_do_baralho:
                media = sum(c["ease_factor"] for c in cards_do_baralho) / len(
                    cards_do_baralho
                )
                st.write(f"**{b['titulo']}:** {media:.2f}")
