import pandas as pd
import streamlit as st

from intent_engine.evaluate import avaliar_baseline, avaliar_frases_proprias, avaliar_teste
from intent_engine.model import ALVO_PRECISAO, prever, treinar
from intent_engine.responses import NOMES, nome_exibicao, responder
from intent_engine.rules_baseline import REGRAS, prever_regras

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


def pct(valor, casas=1):
    """Porcentagem com vírgula decimal: 0.937 -> '93,7%'."""
    return f"{valor * 100:.{casas}f}%".replace(".", ",")


def num(valor, casas=2):
    """Número com vírgula decimal: 0.35 -> '0,35'."""
    return f"{valor:.{casas}f}".replace(".", ",")


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
    return avaliar_teste(modelo), avaliar_frases_proprias(), avaliar_baseline("test")


modelo = carregar_modelo()
limiar = modelo["limiar"]

if "historico" not in st.session_state:
    st.session_state.historico = []


def processar(texto):
    """Classifica a frase (modelo e regras) e guarda no histórico (a mais recente no topo)."""
    texto = texto.strip()
    if not texto:
        return
    resultado = prever(texto)
    st.session_state.historico.insert(
        0, {"texto": texto, "resultado": resultado, "resposta": responder(resultado),
            "regras": prever_regras(texto)}
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
    st.markdown("**Comparação:** regras por palavras-chave (estilo ELIZA), só para contraste.")
    st.caption(f"Limiar de confiança: {num(limiar)}. Abaixo dele, o assistente diz 'não entendi'.")
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

    # Desligado por padrão: a demonstração principal fica limpa
    comparar = st.toggle("Comparar com as regras (estilo ELIZA)",
                         help="Mostra o que um baseline de palavras-chave responderia à mesma frase.")

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
            # Barra mais estreita (em tela larga ela ocupava a linha inteira)
            col_barra, _ = st.columns([2, 3])
            with col_barra:
                st.progress(min(max(r["confianca"], 0.0), 1.0))
            st.caption(f"Confiança: {r['confianca']:.0%} (limiar: {limiar:.0%})")
            if r["top3"]:
                st.caption("Top-3: " + " · ".join(f"{nome_exibicao(d)} {p:.0%}" for d, p in r["top3"]))
            if comparar and item.get("regras") is not None:
                rg = item["regras"]
                if rg["dominio"]:
                    st.caption(f"🔤 Regras: {nome_exibicao(rg['dominio'])} "
                               f"(palavra-chave: {', '.join(rg['palavras'])})")
                else:
                    st.caption("🔤 Regras: não entendi (nenhuma palavra-chave conhecida)")

# ---------------------------------------------------------------------------
# Aba 2: avaliação no conjunto de teste
# ---------------------------------------------------------------------------
with aba_modelo:
    aval, frases, base = carregar_avaliacao()

    st.subheader("Desempenho no conjunto de teste")
    st.caption(f"{aval['n_teste']} frases que o modelo nunca viu no treino nem na escolha do limiar.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Acurácia", pct(aval["acuracia"]))
    c2.metric("F1 macro", num(aval["f1_macro"], 3))
    c3.metric("Cobertura (com limiar)", pct(aval["cobertura"]))
    c4.metric("Precisão nas aceitas", pct(aval["precisao_aceitas"]))

    # Interpretação curta, montada a partir dos números reais
    f1 = aval["por_classe"]["f1-score"]
    texto = (
        f"O modelo acertou {pct(aval['acuracia'])} das frases do teste "
        f"({aval['n_erros']} erros). O melhor F1 é de **{nome_exibicao(f1.idxmax())}** ({num(f1.max())}) "
        f"e o pior é de **{nome_exibicao(f1.idxmin())}** ({num(f1.min())}). "
        f"Com o limiar de {num(aval['limiar'])}, o assistente responde a {pct(aval['cobertura'])} "
        f"das frases e acerta {pct(aval['precisao_aceitas'])} delas; o resto cai no 'não entendi'."
    )
    if len(aval["pares_erro"]):
        p = aval["pares_erro"].iloc[0]
        texto += (f" A confusão mais comum é **{nome_exibicao(p['real'])} → "
                  f"{nome_exibicao(p['previsto'])}** ({p['qtd']} frases).")
    st.markdown(texto)
    st.info(
        "Cuidado ao interpretar: o corpus tem muitas frases parecidas (só as idênticas foram "
        "removidas) e a tradução é parcial, então o número real em frases novas pode ser menor."
    )

    # --- Regras (estilo ELIZA) x modelo, no MESMO conjunto de teste ---
    st.subheader("Regras (estilo ELIZA) × modelo")
    st.caption("Mesmo conjunto de teste. Na acurácia, frase sem resposta conta como erro.")
    acuracia_com_limiar = aval["cobertura"] * aval["precisao_aceitas"]   # acertos / todas as frases
    comparacao = pd.DataFrame([
        {"Método": "Regras por palavras-chave",
         "Acurácia": pct(base["acuracia"]), "F1 macro": num(base["f1_macro"], 3),
         "Cobertura": pct(base["cobertura"]),
         "Precisão nas respondidas": pct(base["precisao_respondidas"])},
        {"Método": "Modelo sem limiar (responde sempre)",
         "Acurácia": pct(aval["acuracia"]), "F1 macro": num(aval["f1_macro"], 3),
         "Cobertura": "100,0%", "Precisão nas respondidas": pct(aval["acuracia"])},
        {"Método": f"Modelo com limiar {num(aval['limiar'])}",
         "Acurácia": pct(acuracia_com_limiar), "F1 macro": "—",
         "Cobertura": pct(aval["cobertura"]),
         "Precisão nas respondidas": pct(aval["precisao_aceitas"])},
    ])
    st.dataframe(comparacao, hide_index=True)

    texto_cmp = (
        f"As regras respondem a {pct(base['cobertura'])} das frases e acertam "
        f"{pct(base['precisao_respondidas'])} das que respondem; no total, acertam "
        f"{pct(base['acuracia'])}. O modelo, sem limiar, acerta {pct(aval['acuracia'])}."
    )
    if aval["acuracia"] > base["acuracia"]:
        texto_cmp += (
            " A diferença vem de o modelo aprender pesos para palavras e pares de palavras a "
            "partir de exemplos, em vez de depender de uma lista de palavras-chave escrita à mão: "
            "frases com sinônimos ou sem nenhuma palavra-chave conhecida ficam sem resposta nas regras."
        )
    st.markdown(texto_cmp)
    st.caption(
        "As regras foram escritas a partir do conhecimento dos domínios, sem consultar o "
        "conjunto de teste, e não foram otimizadas: com mais esforço manual elas melhorariam. "
        "A comparação é ilustrativa, não uma medida definitiva."
    )
    with st.expander("Ver as palavras-chave das regras"):
        st.caption("Radicais (começo da palavra, sem acento). Em caso de empate, vale a ordem desta tabela.")
        st.dataframe(
            pd.DataFrame([{"Domínio": nome_exibicao(d), "Radicais": ", ".join(r)}
                          for d, r in REGRAS.items()]),
            hide_index=True,
        )
        st.caption("Desempenho das regras por classe (teste):")
        st.dataframe(base["por_classe"])

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

    # --- Por que o limiar é 0,35? (tabela calculada na VALIDAÇÃO, não no teste) ---
    st.subheader(f"Por que o limiar é {num(limiar)}?")
    tabela_limiar = pd.DataFrame(
        [{"Limiar": num(lim), "Cobertura": pct(cob), "Precisão nas aceitas": pct(prec),
          "Em uso": "◀" if abs(lim - limiar) < 1e-9 else ""}
         for lim, cob, prec in modelo["tabela"] if lim <= 0.60]
    )
    st.dataframe(tabela_limiar, hide_index=True)
    st.caption("Calculado na validação (não no teste). Cobertura = % de frases que o assistente "
               "aceita responder; precisão = % de acerto entre elas. Limiar maior = mais "
               "cuidado, mas responde a menos frases.")
    automatico = next((lim for lim, cob, prec in modelo["tabela"] if prec >= ALVO_PRECISAO), None)
    if automatico is not None and abs(automatico - limiar) > 1e-9:
        st.markdown(
            f"O limiar automático (o menor com precisão ≥ {pct(ALVO_PRECISAO, 0)} na validação) "
            f"seria **{num(automatico)}**, mas deixava passar frases fora do escopo; por isso foi "
            f"fixado em **{num(limiar)}**, ao custo de responder a menos frases."
        )

    st.subheader("Frases próprias (inclui fora do escopo)")
    acertos = int((frases["resultado"] == "OK").sum())
    st.caption(f"{acertos} de {len(frases)} frases corretas.")
    st.dataframe(frases)