import streamlit as st

st.set_page_config(page_title="PLN · FATEC Cotia", page_icon="🗂️", layout="wide")


def load_css(file_name: str):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


load_css("style.css")

st.markdown("<h1 class='header-title'>Processamento de Linguagem Natural (PLN)</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>PLN é a área da Inteligência Artificial que estuda como sistemas "
    "computacionais analisam, interpretam e geram linguagem humana. Essa análise costuma "
    "acontecer em camadas — da estrutura sintática de uma frase até o significado por trás "
    "dela — e os três projetos abaixo exploram, cada um, uma dessas camadas.</p>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='task-card'>"
    "<h3>📚 Parsing Sintático (Top-Down vs Bottom-Up)</h3>"
    "<p>Compara os algoritmos Top-Down (Recursive Descent) e Bottom-Up (Shift-Reduce) "
    "sobre um corpus fechado de 3 frases, com árvores sintáticas e log passo a passo.</p>"
    "</div>",
    unsafe_allow_html=True,
)
st.page_link("pages/1_📚_Parsing_Sintatico.py", label="Abrir Parsing Sintático", icon="📚")

st.markdown(
    "<div class='task-card'>"
    "<h3>🧠 Dependência Conceitual (CD)</h3>"
    "<p>Implementa o método de Schank (1972): converte uma frase, ao vivo, em um frame "
    "semântico ATOR → ACT → OBJETO, cobrindo as 9 primitivas conceituais da teoria.</p>"
    "</div>",
    unsafe_allow_html=True,
)
st.page_link("pages/2_🧠_Dependencia_Conceitual.py", label="Abrir Dependência Conceitual", icon="🧠")

st.markdown(
    "<div class='task-card'>"
    "<h3>🎭 Análise Pragmática (VADER)</h3>"
    "<p>Testa o VADER em quatro frases emocionalmente ambíguas — sarcasmo, exaltação com "
    "vocabulário de dor — e mostra onde a leitura literal das palavras diverge da "
    "intenção de quem fala.</p>"
    "</div>",
    unsafe_allow_html=True,
)
st.page_link("pages/3_🎭_Analise_Pragmatica.py", label="Abrir Análise Pragmática", icon="🎭")

st.markdown(
    "<p class='subtitle' style='margin-top:28px;font-size:0.85rem;'>"
    "Cada projeto vive em seus próprios arquivos (módulo <code>nlp_engine</code> para o "
    "parsing sintático, módulo <code>cd_engine</code> para a Dependência Conceitual, "
    "módulo <code>sentiment_engine</code> para a Análise Pragmática) — "
    "novos trabalhos entram como uma nova página em <code>pages/</code>, sem tocar no "
    "código dos projetos anteriores.</p>",
    unsafe_allow_html=True,
)
