import streamlit as st

from cd_engine.frames import ConceptualDependencyFrame
from cd_engine.lexicon import content_tokens, tokenize, verbos_por_primitiva, verbos_suportados
from cd_engine.parser import locate_verb, parse_sentence, UnknownVerbError

st.set_page_config(page_title="Dependência Conceitual · PLN", page_icon="🧠", layout="wide")


def load_css(file_name: str):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


load_css("style.css")

EXAMPLES = [
    "Ana deu livro Maria",
    "Ana comeu maca",
    "Pedro foi para Cotia",
    "Pedro chutou a bola para o gol",
    "Ana decidiu viajar",
]


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
    "A Dependência Conceitual trabalha com um conjunto <strong>fechado</strong> "
    f"de 9 primitivas — esta demonstração cobre todas elas, com {len(verbos_suportados())} "
    "verbos ao todo. Fora dessa lista, a teoria (não o programa) não define "
    "uma primitiva correspondente."
    "</div>",
    unsafe_allow_html=True,
)

with st.expander("📋 Ver todos os verbos suportados, por primitiva (ACT)"):
    grupos = verbos_por_primitiva()
    cols = st.columns(3)
    for i, (act, verbos) in enumerate(grupos.items()):
        with cols[i % 3]:
            st.markdown(
                f"<div class='cd-phase' style='margin-bottom:10px;'>"
                f"<code>{act}</code><br>{', '.join(verbos)}</div>",
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
    f"{len(verbos_suportados())} verbos suportados no momento, cobrindo as 9 primitivas "
    "(lista completa no expansor acima). Novos verbos entram em `cd_engine/lexicon.py`, "
    "sem precisar tocar no parser."
)

analisar = st.button("🔎 Analisar frase", type="primary")

# ---------------------------------------------------------------------------
# Resultado
# ---------------------------------------------------------------------------
if analisar:
    frase = st.session_state.cd_sentence

    try:
        tokens = tokenize(frase)
        content = content_tokens(tokens)
        if len(content) < 2:
            raise ValueError(
                "A frase precisa de ao menos um Ator e um Verbo "
                "(ex.: 'Ana comeu maca')."
            )

        encontrado = locate_verb(content)
        if encontrado is None:
            raise UnknownVerbError(
                "Nenhum verbo da frase está entre as primitivas suportadas. "
                f"Verbos disponíveis: {', '.join(verbos_suportados())}."
            )
        _, verbo, regra = encontrado

        st.markdown("#### Passo a passo")
        p1, p2, p3 = st.columns(3)
        with p1:
            st.markdown(
                "<div class='cd-phase'><strong>1 · Análise Léxica</strong>"
                f"<br>Tokens: {tokens}"
                f"<br><span style='color:#94A3B8;'>sem artigos/preposições: {content}</span></div>",
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

    except UnknownVerbError as e:
        st.error(str(e))
        st.caption(
            "Isso é esperado, não é um bug: a Dependência Conceitual trabalha com um "
            "conjunto fechado de primitivas conceituais (Schank, 1972) — fora da lista "
            "acima, a própria teoria não define uma primitiva correspondente."
        )
    except ValueError as e:
        st.error(str(e))
