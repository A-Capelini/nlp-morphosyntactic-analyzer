import streamlit as st

from cd_engine.frames import ConceptualDependencyFrame
from cd_engine.lexicon import SEMANTIC_LEXICON, tokenize, verbos_suportados
from cd_engine.parser import parse_sentence, UnknownVerbError

st.set_page_config(page_title="Dependência Conceitual · PLN", page_icon="🧠", layout="wide")


def load_css(file_name: str):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


load_css("style.css")

EXAMPLES = ["Ana deu livro Maria", "Ana comeu maca", "Pedro foi para Cotia"]


# ---------------------------------------------------------------------------
# Renderização visual do frame (camada de apresentação — fica aqui na página,
# não em cd_engine, para manter o motor de análise livre de HTML/Streamlit).
# ---------------------------------------------------------------------------
def render_frame_html(frame: ConceptualDependencyFrame, nested: bool = False) -> str:
    wrapper_class = "cd-frame nested" if nested else "cd-frame"
    inst_html = ""
    if isinstance(frame.instrument, ConceptualDependencyFrame):
        inst_html = (
            "<div class='cd-instrument-label'>INSTRUMENTO</div>"
            + render_frame_html(frame.instrument, nested=True)
        )
    elif frame.instrument:
        inst_html = f"<div class='cd-instrument-label'>INSTRUMENTO: {frame.instrument}</div>"

    return f"""
    <div class="{wrapper_class}">
      <div class="cd-flow">
        <div class="cd-node cd-node-pp">{frame.actor}<span>PP</span></div>
        <div class="cd-arrow">&rarr;</div>
        <div class="cd-node cd-node-act">{frame.act}<span>ACT</span></div>
        <div class="cd-arrow">&rarr;</div>
        <div class="cd-node cd-node-pp">{frame.obj if frame.obj is not None else "—"}<span>PP</span></div>
      </div>
      <div class="cd-direction">
        <span><strong>FROM</strong> {frame.origin}</span>
        <span><strong>TO</strong> {frame.recipient}</span>
      </div>
      {inst_html}
    </div>
    """


# ---------------------------------------------------------------------------
# Cabeçalho
# ---------------------------------------------------------------------------
st.markdown("<h1 class='header-title'>Dependência Conceitual (CD)</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Tarefa 2 — análise semântica ao vivo de uma frase escolhida na hora. "
    "Baseado na teoria de Roger Schank (1972).</p>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='cd-legend'>"
    "<code>ATRANS</code> transferência de posse&nbsp;&nbsp;·&nbsp;&nbsp;"
    "<code>PTRANS</code> transferência de local&nbsp;&nbsp;·&nbsp;&nbsp;"
    "<code>INGEST</code> ingestão (com inferência de instrumento)"
    "</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Entrada: exemplo rápido (para demonstração) + frase livre editável
# ---------------------------------------------------------------------------
if "cd_sentence" not in st.session_state:
    st.session_state.cd_sentence = EXAMPLES[0]


def _apply_example():
    st.session_state.cd_sentence = st.session_state.cd_example_choice


col_a, col_b = st.columns([1, 2])
with col_a:
    st.selectbox(
        "Exemplo rápido:", EXAMPLES, key="cd_example_choice", on_change=_apply_example
    )
with col_b:
    st.text_input(
        "Frase para analisar (Ator Verbo Complemento) — pode ser escolhida na hora:",
        key="cd_sentence",
        placeholder="Ex.: Ana comeu maca",
    )

st.caption(
    "Verbos suportados no momento: " + ", ".join(verbos_suportados())
    + ". Novos verbos podem ser adicionados em `cd_engine/lexicon.py`."
)

analisar = st.button("🔎 Analisar frase", type="primary")

# ---------------------------------------------------------------------------
# Resultado
# ---------------------------------------------------------------------------
if analisar:
    frase = st.session_state.cd_sentence

    try:
        tokens = tokenize(frase)
        if len(tokens) < 3:
            raise ValueError(
                "A frase precisa de ao menos Ator, Verbo e Complemento "
                "(ex.: 'Ana comeu maca')."
            )
        actor, verbo = tokens[0], tokens[1]
        regra = SEMANTIC_LEXICON.get(verbo.lower())
        if regra is None:
            raise UnknownVerbError(
                f"Verbo '{verbo}' fora do léxico semântico. "
                f"Verbos suportados: {', '.join(verbos_suportados())}."
            )

        st.markdown("#### Passo a passo")
        p1, p2, p3 = st.columns(3)
        with p1:
            st.markdown(
                "<div class='cd-phase'><strong>1 · Análise Léxica</strong>"
                f"<br>Tokens: {tokens}</div>",
                unsafe_allow_html=True,
            )
        with p2:
            st.markdown(
                "<div class='cd-phase'><strong>2 · Mapeamento Ontológico</strong>"
                f"<br>'{verbo}' &rarr; <code>{regra['act']}</code></div>",
                unsafe_allow_html=True,
            )
        with p3:
            st.markdown(
                "<div class='cd-phase'><strong>3-4 · Slots + Inferência</strong>"
                "<br>preenchidos no frame abaixo</div>",
                unsafe_allow_html=True,
            )

        frame = parse_sentence(frase)

        st.markdown("#### Frame CD resultante")
        st.markdown(render_frame_html(frame), unsafe_allow_html=True)

        with st.expander("Ver como JSON"):
            st.json(frame.to_dict())

    except (UnknownVerbError, ValueError) as e:
        st.error(str(e))
