import streamlit as st

from intent_engine.evaluate import avaliar_frases_proprias, avaliar_teste
from intent_engine.model import prever, treinar
from intent_engine.responses import NOMES, nome_exibicao, responder

st.set_page_config(page_title="Assistente de Intenções · PLN", page_icon="🤖", layout="wide")


def load_css(file_name: str):
    # Mesmo padrão das outras páginas do app
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


load_css("style.css")

EXEMPLOS = [
    "acorde-me às sete da manhã",
    "vai chover amanhã?",
    "apaga as luzes da sala",
    "lê meu último e-mail",
    "que dia é hoje?",
    "me conta uma piada",          # fora do escopo: deve cair no "não entendi"
]


# ---------------------------------------------------------------------------
# Carregamento (cache): o modelo treina UMA vez; a avaliação roda UMA vez.
# Toda a lógica de PLN fica em intent_engine; aqui só há interface.
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner="Treinando o modelo...")
def carregar_modelo():
    return treinar()


@st.cache_data(show_spinner="Avaliando no conjunto de teste...")
def carregar_avaliacao():
    modelo = carregar_modelo()
    return avaliar_teste(modelo), avaliar_frases_proprias()


modelo = carregar_modelo()
limiar = modelo["limiar"]

if "historico" not in st.session_state:
    st.session_state.historico = []


def processar(texto):
    """Classifica a frase e guarda no histórico (a mais recente fica no topo)."""
    texto = texto.strip()
    if not texto:
        return
    resultado = prever(texto)
    st.session_state.historico.insert(
        0, {"texto": texto, "resultado": resultado, "resposta": responder(resultado)}
    )


# ---------------------------------------------------------------------------
# Barra lateral: dataset e limitações
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Sobre o assistente")
    st.markdown(
        "Classifica a **intenção (domínio)** de uma frase em português, etapa de "
        "**NLU** de um assistente virtual. Não gera texto e não é IA agêntica: "
        "a resposta de cada domínio é fixa (simulada)."
    )
    st.markdown("**Domínios:** " + ", ".join(NOMES.values()) + ".")
    st.markdown(
        "**Dataset:** MASSIVE pt-BR (Hugging Face, `Magurofg/massive-pt-br`), "
        "licença CC BY 4.0."
    )
    st.markdown("**Modelo:** TF-IDF (unigramas + bigramas) + Regressão Logística.")
    st.caption(f"Limiar de confiança: {limiar:.2f}. Abaixo dele, o assistente diz 'não entendi'.")
    st.warning(
        "**Limitações:** a localização para pt-BR foi feita por um LLM, é parcial e "
        "ainda tem resíduos de português europeu e frases truncadas. "
        "O modelo só conhece 9 domínios."
    )

st.title("🤖 Assistente de Intenções")
aba_assistente, aba_modelo = st.tabs(["Assistente", "Sobre o modelo"])

# ---------------------------------------------------------------------------
# Aba 1: o assistente
# ---------------------------------------------------------------------------
with aba_assistente:
    with st.form("form_entrada", clear_on_submit=True):
        entrada = st.text_input("Digite uma frase", placeholder="Ex.: acorde-me às sete da manhã")
        enviado = st.form_submit_button("Enviar")
    if enviado:
        processar(entrada)

    st.caption("Ou clique em um exemplo:")
    colunas = st.columns(3)
    for i, exemplo in enumerate(EXEMPLOS):
        colunas[i % 3].button(exemplo, key=f"ex_{i}", on_click=processar,
                              args=(exemplo,), use_container_width=True)

    if st.session_state.historico:
        st.button("Limpar histórico", on_click=st.session_state.historico.clear)

    for item in st.session_state.historico:
        r = item["resultado"]
        with st.chat_message("user"):
            st.write(item["texto"])
        with st.chat_message("assistant"):
            if r["entendeu"]:
                st.markdown(f"**Domínio previsto:** {nome_exibicao(r['dominio'])}")
                st.write(item["resposta"])
            else:
                st.warning(item["resposta"])         # abaixo do limiar: "não entendi"
            st.progress(min(max(r["confianca"], 0.0), 1.0))
            st.caption(f"Confiança: {r['confianca']:.0%} (limiar: {limiar:.0%})")
            if r["top3"]:
                st.caption("Top-3: " + " · ".join(f"{nome_exibicao(d)} {p:.0%}" for d, p in r["top3"]))

# ---------------------------------------------------------------------------
# Aba 2: avaliação no conjunto de teste
# ---------------------------------------------------------------------------
with aba_modelo:
    aval, frases = carregar_avaliacao()

    st.subheader("Desempenho no conjunto de teste")
    st.caption(f"{aval['n_teste']} frases que o modelo nunca viu no treino nem na escolha do limiar.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Acurácia", f"{aval['acuracia']:.1%}")
    c2.metric("F1 macro", f"{aval['f1_macro']:.3f}")
    c3.metric("Cobertura (com limiar)", f"{aval['cobertura']:.1%}")
    c4.metric("Precisão nas aceitas", f"{aval['precisao_aceitas']:.1%}")

    # Interpretação curta, montada a partir dos números reais
    f1 = aval["por_classe"]["f1-score"]
    texto = (
        f"O modelo acertou {aval['acuracia']:.1%} das frases do teste "
        f"({aval['n_erros']} erros). O melhor F1 é de **{f1.idxmax()}** ({f1.max():.2f}) "
        f"e o pior é de **{f1.idxmin()}** ({f1.min():.2f}). "
        f"Com o limiar de {aval['limiar']:.2f}, o assistente responde a {aval['cobertura']:.1%} "
        f"das frases e acerta {aval['precisao_aceitas']:.1%} delas; o resto cai no 'não entendi'."
    )
    if len(aval["pares_erro"]):
        p = aval["pares_erro"].iloc[0]
        texto += f" A confusão mais comum é **{p['real']} → {p['previsto']}** ({p['qtd']} frases)."
    st.markdown(texto)
    st.info(
        "Cuidado ao interpretar: o corpus tem muitas frases parecidas (só as idênticas foram "
        "removidas) e a tradução é parcial, então o número real em frases novas pode ser menor."
    )

    st.subheader("Por classe")
    st.dataframe(aval["por_classe"])

    st.subheader("Matriz de confusão")
    st.caption("Linhas = domínio real; colunas = domínio previsto. Legenda: "
               + ", ".join(f"{c} = {n}" for c, n in NOMES.items()))
    st.dataframe(aval["matriz"])

    st.subheader("Erros mais comuns")
    st.dataframe(aval["pares_erro"])
    st.caption("Erros com maior confiança do modelo:")
    st.dataframe(aval["erros_confiantes"])

    st.subheader("Frases próprias (inclui fora do escopo)")
    acertos = int((frases["resultado"] == "OK").sum())
    st.caption(f"{acertos} de {len(frases)} frases corretas.")
    st.dataframe(frases)