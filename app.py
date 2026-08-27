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

st.markdown("<h1 class='header-title'>Análise Morfossintática (Top-Down vs Bottom-Up)</h1>", unsafe_allow_html=True)
st.markdown("Aplicação didática para a disciplina de Engenharia de Dados. Selecione uma sentença do corpus abaixo para gerar as árvores sintáticas (CFG).")

sentences = [
    "The White dog died Yesterday",
    "The coffee spilled on the floor",
    "The blue car crashed last week"
]

selected_sentence = st.selectbox("Selecione a Frase:", sentences)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='method-title'>Método Top-Down (Recursive Descent)</div>", unsafe_allow_html=True)
    trees_td, log_td = cached_top_down(selected_sentence)
    
    if trees_td:
        for tree in trees_td:
            svg_html = render_tree_to_svg(tree)
            st.markdown(f"<div class='tree-container'>{svg_html}</div>", unsafe_allow_html=True)
        
        with st.expander("🔍 Ver passo a passo (Log do Algoritmo)"):
            st.code(log_td, language="text")
    else:
        st.error("Nenhuma árvore encontrada pelo método Top-Down.")

with col2:
    st.markdown("<div class='method-title'>Método Bottom-Up (Shift-Reduce)</div>", unsafe_allow_html=True)
    trees_bu, log_bu = cached_bottom_up(selected_sentence)
    
    if trees_bu:
        for tree in trees_bu:
            svg_html = render_tree_to_svg(tree)
            st.markdown(f"<div class='tree-container'>{svg_html}</div>", unsafe_allow_html=True)
            
        with st.expander("🔍 Ver passo a passo (Log do Algoritmo)"):
            st.code(log_bu, language="text")
    else:
        st.error("Nenhuma árvore encontrada pelo método Bottom-Up.")
