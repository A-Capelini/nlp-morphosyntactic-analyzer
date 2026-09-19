import html

import streamlit as st

from sentiment_engine.corpus import EXEMPLOS_LIVRES, FRASES, FRASES_CONTROLE
from sentiment_engine.vader_core import LIMIAR, Resultado, analisar, carregar_analisador

st.set_page_config(page_title="Análise Pragmática · PLN", page_icon="🎭", layout="wide")


def load_css(file_name: str):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


load_css("style.css")


# O léxico do VADER é baixado uma única vez por sessão do servidor, e não a
# cada interação do usuário.
@st.cache_resource(show_spinner="Carregando o léxico do VADER...")
def get_analisador():
    return carregar_analisador()


try:
    sia = get_analisador()
except RuntimeError as erro:
    st.error(str(erro))
    st.stop()


# ---------------------------------------------------------------------------
# Renderização visual (camada de apresentação — fica aqui na página, não em
# sentiment_engine, para manter o motor livre de HTML/Streamlit).
# Todo texto vindo do usuário passa por html.escape antes de entrar no HTML.
# Cores: teal (positivo) e âmbar (negativo) — combinação segura para
# daltonismo — e o sentido também vai escrito (símbolo + palavra), nunca só
# na cor.
# ---------------------------------------------------------------------------
SIMBOLO = {"positivo": "▲", "negativo": "▼", "neutro": "●"}
EMOCAO = {"positivo": "positiva", "negativo": "negativa", "neutro": "neutra"}
IDIOMA = {"pt": "Português", "en": "Inglês"}


def fmt(valor: float, sinal: bool = False, casas: int = 3) -> str:
    """Formata com vírgula decimal e sinal de menos tipográfico."""
    # O zero não leva sinal (fica "0,0000", igual ao documento entregue).
    texto = f"{valor:+.{casas}f}" if sinal and valor != 0 else f"{valor:.{casas}f}"
    return texto.replace(".", ",").replace("-", "−")


def render_gauge(res: Resultado) -> str:
    posicao = (max(-1.0, min(1.0, res.compound)) + 1) / 2 * 100
    return (
        "<div class='sa-gauge'>"
        "<div class='sa-gauge-track'><div class='sa-gauge-zero'></div>"
        f"<div class='sa-gauge-marker {res.rotulo}' style='left:{posicao:.1f}%'></div></div>"
        "<div class='sa-gauge-scale'><span>−1 (negativo)</span><span>0</span>"
        "<span>+1 (positivo)</span></div>"
        "</div>"
    )


def render_status(res: Resultado) -> str:
    """Selo de acerto/erro em relação à emoção esperada (texto + símbolo)."""
    if res.esperado is None:
        return ""
    if res.acerto_acidental:
        return "<span class='sa-hit warn'>≈ acerto acidental</span>"
    if res.acertou:
        return "<span class='sa-hit ok'>✔ coincide com o esperado</span>"
    return "<span class='sa-hit miss'>✘ diferente do esperado</span>"


def render_words(res: Resultado) -> str:
    if not res.palavras:
        motivo = (
            "o léxico do VADER é em inglês, então ele não reconheceu palavra alguma"
            if res.idioma == "pt"
            else "nenhuma palavra desta frase está no léxico"
        )
        return f"<div class='sa-words'><strong>Palavras no léxico:</strong> <span class='sa-none'>nenhuma — {motivo}.</span></div>"
    chips = "".join(
        f"<span class='sa-chip {'pos' if valor > 0 else 'neg'}'>"
        f"{html.escape(palavra)} <b>{fmt(valor, sinal=True, casas=1)}</b></span>"
        for palavra, valor in res.palavras
    )
    return f"<div class='sa-words'><strong>Palavras no léxico:</strong> {chips}</div>"


def render_warning(res: Resultado) -> str:
    if not res.coincidencias:
        return ""
    lista = ", ".join(f"“{html.escape(p)}”" for p in res.coincidencias)
    return (
        "<div class='sa-warning'>⚠ O dicionário do VADER é em inglês: em português, "
        f"as palavras reconhecidas ({lista}) são coincidências com palavras inglesas, "
        "não compreensão da frase.</div>"
    )


def render_card(res: Resultado) -> str:
    esperado = (
        f"<div class='sa-expected-line'>Esperado: <strong>{res.esperado}</strong></div>"
        if res.esperado
        else ""
    )
    return (
        f"<div class='sa-card {res.rotulo}'>"
        f"<div class='sa-card-head'><span class='sa-badge {res.rotulo}'>"
        f"{SIMBOLO[res.rotulo]} {res.rotulo}</span>{render_status(res)}</div>"
        f"<div class='sa-text'>“{html.escape(res.texto)}”</div>"
        f"{render_gauge(res)}"
        "<div class='sa-scores'>"
        f"<span><strong>compound</strong> {fmt(res.compound, sinal=True, casas=4)}</span>"
        f"<span>neg {fmt(res.neg)}</span><span>neu {fmt(res.neu)}</span>"
        f"<span>pos {fmt(res.pos)}</span></div>"
        f"{esperado}{render_words(res)}{render_warning(res)}"
        "</div>"
    )


def celula_resumo(res: Resultado) -> str:
    if res.acerto_acidental:
        selo, classe = "≈ acidental", "warn"
    elif res.acertou:
        selo, classe = "✔ acertou", "ok"
    else:
        selo, classe = "✘ errou", "miss"
    return (
        f"<td>{fmt(res.compound, sinal=True, casas=4)} · {res.rotulo} "
        f"<span class='sa-hit {classe}'>{selo}</span></td>"
    )


def selo_controle(res: Resultado) -> str:
    return (
        "<span class='sa-hit ok'>✔ acertou</span>"
        if res.acertou
        else "<span class='sa-hit miss'>✘ errou</span>"
    )


# ---------------------------------------------------------------------------
# Cabeçalho
# ---------------------------------------------------------------------------
st.markdown("<h1 class='header-title'>Análise Pragmática (VADER)</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Tarefa 04 — disciplina de PLN, FATEC Cotia. "
    "O VADER consegue captar intenção e contexto, ou lê só o significado literal das palavras?</p>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='sa-legend'>"
    "O <strong>VADER</strong> é um analisador de sentimentos baseado em léxico e regras: "
    "soma o valor emocional (de −4 a +4) das palavras que encontra em um dicionário "
    "<strong>em inglês</strong>. O escore <code>compound</code> vai de −1 a +1 e vira rótulo "
    f"assim: ≥ +{fmt(LIMIAR, casas=2)} positivo, ≤ −{fmt(LIMIAR, casas=2)} negativo, "
    "entre os dois neutro. Por isso cada frase é avaliada duas vezes: em português "
    "(original) e em uma tradução para o inglês."
    "</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Corpus do exercício: frase selecionada, PT x EN lado a lado
# ---------------------------------------------------------------------------
resultados_pt = [analisar(sia, f["pt"], "pt", f["esperado"]) for f in FRASES]
resultados_en = [analisar(sia, f["en"], "en", f["esperado"]) for f in FRASES]

st.markdown("#### As quatro frases do exercício")
indice = st.selectbox(
    "Selecione a frase:",
    range(len(FRASES)),
    format_func=lambda i: FRASES[i]["categoria"],
)
frase = FRASES[indice]

st.markdown(
    "<div class='sa-expected'>Emoção esperada (leitura pragmática): "
    f"<strong>{EMOCAO[frase['esperado']]}</strong> — {frase['nota']}</div>",
    unsafe_allow_html=True,
)

col_pt, col_en = st.columns(2)
with col_pt:
    st.markdown("<div class='sa-col-title'>Português (original)</div>", unsafe_allow_html=True)
    st.markdown(render_card(resultados_pt[indice]), unsafe_allow_html=True)
with col_en:
    st.markdown("<div class='sa-col-title'>Inglês (tradução)</div>", unsafe_allow_html=True)
    st.markdown(render_card(resultados_en[indice]), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Resumo comparativo das quatro frases
# ---------------------------------------------------------------------------
st.markdown("#### Resumo comparativo")
linhas = "".join(
    f"<tr><td>{html.escape(f['categoria'])}</td><td>{f['esperado']}</td>"
    f"{celula_resumo(rp)}{celula_resumo(re_)}</tr>"
    for f, rp, re_ in zip(FRASES, resultados_pt, resultados_en)
)
st.markdown(
    "<div class='sa-table-wrap'><table class='sa-table'><thead><tr>"
    "<th>Frase</th><th>Esperado</th><th>Português</th><th>Inglês</th></tr></thead>"
    f"<tbody>{linhas}</tbody></table></div>",
    unsafe_allow_html=True,
)

acertos_pt = sum(bool(r.acertou) for r in resultados_pt)
acidentais_pt = sum(r.acerto_acidental for r in resultados_pt)
acertos_en = sum(bool(r.acertou) for r in resultados_en)
total = len(FRASES)
st.caption(
    f"Acertos em inglês: {acertos_en}/{total}. Em português: {acertos_pt}/{total}, "
    f"dos quais {acidentais_pt} são acidentais (o escore veio de palavras que só "
    "coincidem com o léxico inglês). Amostra pequena, escolhida de propósito para "
    "pressionar o algoritmo: não estima a acurácia geral do VADER."
)

# ---------------------------------------------------------------------------
# Frase livre (pode ser escolhida na hora)
# ---------------------------------------------------------------------------
st.markdown("#### Teste uma frase sua")

if "sa_text" not in st.session_state:
    st.session_state.sa_text = EXEMPLOS_LIVRES[0]["texto"]
if "sa_lang" not in st.session_state:
    st.session_state.sa_lang = EXEMPLOS_LIVRES[0]["idioma"]


def _aplicar_exemplo():
    exemplo = EXEMPLOS_LIVRES[st.session_state.sa_example]
    st.session_state.sa_text = exemplo["texto"]
    st.session_state.sa_lang = exemplo["idioma"]


col_a, col_b, col_c = st.columns([1, 2, 1])
with col_a:
    st.selectbox(
        "Exemplo rápido:",
        range(len(EXEMPLOS_LIVRES)),
        format_func=lambda i: EXEMPLOS_LIVRES[i]["rotulo"],
        key="sa_example",
        on_change=_aplicar_exemplo,
    )
with col_b:
    st.text_input(
        "Frase para analisar — pode ser escolhida na hora:",
        key="sa_text",
        placeholder="Ex.: I am not happy with this service.",
    )
with col_c:
    st.radio(
        "Idioma da frase:",
        list(IDIOMA),
        format_func=lambda v: IDIOMA[v],
        key="sa_lang",
        horizontal=True,
    )

analisar_livre = st.button("🔎 Analisar frase", type="primary")

if analisar_livre:
    texto_livre = st.session_state.sa_text.strip()
    if not texto_livre:
        st.warning("Digite uma frase para analisar.")
    else:
        resultado_livre = analisar(sia, texto_livre, st.session_state.sa_lang)
        st.markdown(render_card(resultado_livre), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Testes de sensibilidade (frases de controle)
# ---------------------------------------------------------------------------
with st.expander("🧪 Testes de sensibilidade (controles A–D)"):
    st.markdown(
        "<div class='sa-legend'>Pequenas mudanças em uma frase para descobrir "
        "<strong>por que</strong> o VADER acertou ou errou.</div>",
        unsafe_allow_html=True,
    )
    linhas_controle = ""
    for c in FRASES_CONTROLE:
        r = analisar(sia, c["texto"], c["idioma"], c["esperado"])
        linhas_controle += (
            f"<tr><td><strong>{c['controle']}</strong></td>"
            f"<td>{html.escape(c['texto'])}<br><span class='sa-muted'>{IDIOMA[c['idioma']]}</span></td>"
            f"<td>{fmt(r.compound, sinal=True, casas=4)}<br>{r.rotulo}</td>"
            f"<td>{c['esperado']}</td><td>{selo_controle(r)}</td>"
            f"<td>{c['por_que']}</td></tr>"
        )
    st.markdown(
        "<div class='sa-table-wrap'><table class='sa-table'><thead><tr>"
        "<th>Controle</th><th>Frase</th><th>compound</th><th>Esperado</th>"
        "<th>Resultado</th><th>Por quê</th></tr></thead>"
        f"<tbody>{linhas_controle}</tbody></table></div>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Leitura crítica (resumo)
# ---------------------------------------------------------------------------
with st.expander("🧭 Leitura crítica: o VADER faz processamento pragmático?"):
    st.markdown(
        "**Não.** Ele faz uma leitura lexical: soma valores de palavras isoladas e aplica "
        "algumas regras (negação, intensificadores, “but”, pontuação), sem representar "
        "contexto situacional, conhecimento de mundo ou a intenção de quem fala."
    )
    st.markdown(
        "- **Sarcasmo (frase 2):** a palavra positiva do sarcasmo (“wonderful”) pesa mais "
        "que “broke”. Sem ela (controle B), a frase é lida como negativa.\n"
        "- **Exaltação com vocabulário de dor (frase 3):** “pain” e “tears” dominam o "
        "resultado, embora a mensagem seja de conquista. Com “won” (controle C), o "
        "resultado inverte: depende de uma única palavra.\n"
        "- **Idioma:** em português o VADER só “casa” com falsos cognatos como “no” e "
        "“sob” (controle A), e não reconhece palavras como “feliz”.\n"
        "- **Vocabulário exato:** “laid off” e “cannot afford” não estão no léxico "
        "(controle D): a mesma situação da frase 1 recebe escore zero."
    )
    st.markdown("**Como melhorar**")
    st.markdown(
        "- **Modelos contextuais** (BERT, RoBERTa, GPT via `transformers`): a mesma "
        "palavra recebe representações diferentes conforme a frase. Para português, um "
        "modelo multilíngue (por exemplo, baseado em XLM-RoBERTa).\n"
        "- **Léxico adaptado ao português** (como o LeIA, adaptação do VADER), o que evita "
        "falsos cognatos.\n"
        "- **Detector de ironia dedicado**, combinado com a análise de sentimentos.\n"
        "- **Avaliação com mais dados:** um conjunto maior de frases rotuladas por pessoas, "
        "com acurácia e F1 por categoria."
    )
    st.caption(
        "Os modelos `transformers` não rodam neste app: são pesados demais para os "
        "recursos do Streamlit Community Cloud."
    )
