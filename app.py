import streamlit as st

st.set_page_config(page_title="PLN · FATEC Cotia", page_icon="🗂️", layout="wide")


def load_css(file_name: str):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


load_css("style.css")

st.markdown("<h1 class='header-title'>PLN — Portfólio de Trabalhos</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Disciplina de Processamento de Linguagem Natural — FATEC Cotia. "
    "Um único app, com uma página independente por trabalho: use o menu à esquerda "
    "ou os atalhos abaixo para navegar.</p>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='task-card'>"
    "<h3>📚 Tarefa 03 — Parsing Sintático</h3>"
    "<p>Compara os algoritmos Top-Down (Recursive Descent) e Bottom-Up (Shift-Reduce) "
    "sobre um corpus fechado de 3 frases, com árvores sintáticas e log passo a passo.</p>"
    "</div>",
    unsafe_allow_html=True,
)
st.page_link("pages/1_📚_Parsing_Sintatico.py", label="Abrir Parsing Sintático", icon="📚")

st.markdown(
    "<div class='task-card'>"
    "<h3>🧠 Tarefa 1 e 2 — Dependência Conceitual (CD)</h3>"
    "<p>Pesquisa sobre o método de Schank (1972) e programa que realiza, ao vivo, a "
    "análise semântica de uma frase em um frame CD (ATOR → ACT → OBJETO).</p>"
    "</div>",
    unsafe_allow_html=True,
)
st.page_link("pages/2_🧠_Dependencia_Conceitual.py", label="Abrir Dependência Conceitual", icon="🧠")

st.markdown(
    "<p class='subtitle' style='margin-top:28px;font-size:0.85rem;'>"
    "Cada trabalho vive em seus próprios arquivos (módulo <code>nlp_engine</code> para a "
    "Tarefa 03, módulo <code>cd_engine</code> para a Tarefa 1/2) — novas tarefas do "
    "semestre entram como uma nova página em <code>pages/</code>, sem tocar no código "
    "dos trabalhos anteriores.</p>",
    unsafe_allow_html=True,
)
