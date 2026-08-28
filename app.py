import streamlit as st
from nlp_engine.parsers import run_top_down, run_bottom_up
from nlp_engine.tree_renderer import render_tree_to_svg

st.set_page_config(page_title="NLP Analyzer", layout="wide")

def load_css(file_name: str):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css("style.css")

# Cache: como o corpus é fechado (3 frases fixas), evita reprocessar o parsing
# (tokenização + POS tagging + parsing) toda vez que o usuário troca de frase
# e volta para uma já vista antes.
@st.cache_data(show_spinner=False)
def cached_top_down(sentence: str):
    return run_top_down(sentence)

@st.cache_data(show_spinner=False)
def cached_bottom_up(sentence: str):
    return run_bottom_up(sentence)

# Explicação curta de cada método: o que é, pra que serve e como funciona.
DESCRIPTION_TOP_DOWN = (
    "<div class='method-description'>"
    "<strong>O que é:</strong> parte da raiz da árvore (S) e tenta expandir cada regra "
    "da gramática, de cima pra baixo, até alcançar as palavras da frase."
    "<br><strong>Pra que serve:</strong> verificar se a frase é válida testando "
    "exaustivamente as regras possíveis."
    "<br><strong>Como funciona:</strong> a cada passo, expande um não-terminal ou casa "
    "uma palavra esperada com a real da frase, voltando atrás (backtracking) quando uma "
    "tentativa falha."
    "</div>"
)

DESCRIPTION_BOTTOM_UP = (
    "<div class='method-description'>"
    "<strong>O que é:</strong> parte das palavras da frase e vai agrupando (reduzindo) "
    "tokens em categorias gramaticais cada vez maiores, de baixo pra cima, até formar a "
    "sentença completa (S)."
    "<br><strong>Pra que serve:</strong> a mesma verificação de validade da frase, mas com "
    "uma estratégia gulosa (greedy)."
    "<br><strong>Como funciona:</strong> a cada passo, empilha a próxima palavra ou reduz "
    "o topo da pilha usando uma regra da gramática — sem voltar atrás se errar a decisão."
    "</div>"
)

# Legendas explicando as siglas que o trace do NLTK imprime no log, para que
# o log não fique só com letras soltas sem explicação para quem está lendo.
LEGEND_TOP_DOWN = (
    "<div class='log-legend'>"
    "<code>E</code> Expand — tenta expandir um não-terminal usando uma regra da gramática"
    "&nbsp;&nbsp;·&nbsp;&nbsp;"
    "<code>M</code> Match — compara a palavra esperada com a palavra real da frase"
    "&nbsp;&nbsp;·&nbsp;&nbsp;"
    "<code>+</code> encontrou uma árvore válida completa"
    "</div>"
)

LEGEND_BOTTOM_UP = (
    "<div class='log-legend'>"
    "<code>S</code> Shift — empilha a próxima palavra da frase"
    "&nbsp;&nbsp;·&nbsp;&nbsp;"
    "<code>R</code> Reduce — reduz o topo da pilha usando uma regra da gramática"
    "</div>"
)

st.markdown("<h1 class='header-title'>Análise Morfossintática (Top-Down vs Bottom-Up)</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Aplicação didática para a disciplina de Engenharia de Dados. "
    "Selecione uma sentença do corpus abaixo para gerar as árvores sintáticas (CFG).</p>",
    unsafe_allow_html=True,
)

sentences = [
    "The White dog died Yesterday",
    "The coffee spilled on the floor",
    "The blue car crashed last week"
]

selected_sentence = st.selectbox("Selecione a Frase:", sentences)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='method-title top-down'>Método Top-Down (Recursive Descent)</div>", unsafe_allow_html=True)
    st.markdown(DESCRIPTION_TOP_DOWN, unsafe_allow_html=True)
    trees_td, log_td = cached_top_down(selected_sentence)
    
    if trees_td:
        for tree in trees_td:
            svg_html = render_tree_to_svg(tree)
            st.markdown(f"<div class='tree-container top-down'>{svg_html}</div>", unsafe_allow_html=True)
        
        with st.expander("🔍 Ver passo a passo (Log do Algoritmo)"):
            st.markdown(LEGEND_TOP_DOWN, unsafe_allow_html=True)
            st.code(log_td, language="text")
    else:
        st.error("Nenhuma árvore encontrada pelo método Top-Down.")

with col2:
    st.markdown("<div class='method-title bottom-up'>Método Bottom-Up (Shift-Reduce)</div>", unsafe_allow_html=True)
    st.markdown(DESCRIPTION_BOTTOM_UP, unsafe_allow_html=True)
    trees_bu, log_bu = cached_bottom_up(selected_sentence)
    
    if trees_bu:
        for tree in trees_bu:
            svg_html = render_tree_to_svg(tree)
            st.markdown(f"<div class='tree-container bottom-up'>{svg_html}</div>", unsafe_allow_html=True)
            
        with st.expander("🔍 Ver passo a passo (Log do Algoritmo)"):
            st.markdown(LEGEND_BOTTOM_UP, unsafe_allow_html=True)
            st.code(log_bu, language="text")
    else:
        st.error("Nenhuma árvore encontrada pelo método Bottom-Up.")
