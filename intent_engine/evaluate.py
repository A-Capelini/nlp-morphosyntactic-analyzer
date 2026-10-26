"""
Avaliação do modelo no split de TESTE (Etapa 4).

Este é o ÚNICO lugar que lê o split 'test'. As funções devolvem tabelas
(DataFrames) e números; quem desenha na tela é a página Streamlit.
Regra: nada aqui deve ser usado para ajustar o modelo ou o limiar.
"""
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, f1_score

from intent_engine.model import ARQ_CSV, prever, treinar

# Frases próprias (esperado = None significa FORA DO ESCOPO: deve cair no "não entendi").
# Substitua/complete com frases suas.
FRASES_PROPRIAS = [
    ("me acorda às seis e meia", "alarm"),
    ("cancela o alarme das sete", "alarm"),
    ("vai fazer frio hoje à noite?", "weather"),
    ("qual a previsão para o fim de semana", "weather"),
    ("coloca um podcast de tecnologia", "play"),
    ("apaga a luz do quarto", "iot"),
    ("liga o ar condicionado da sala", "iot"),
    ("agenda o dentista na terça às três", "calendar"),
    ("adiciona leite na lista de compras", "lists"),
    ("que horas são em Tóquio?", "datetime"),
    ("quais são as notícias de hoje?", "news"),
    ("envia um e-mail para a Maria", "email"),
    # --- fora do escopo ---
    ("quanto custa um iPhone?", None),
    ("traduz bom dia para inglês", None),
    ("me ensina a programar em Python", None),
    ("quem descobriu o Brasil?", None),
    ("qual é a raiz quadrada de 144?", None),
    ("pede uma pizza de calabresa", None),
]


def avaliar_teste(modelo=None):
    """Avalia o modelo treinado no split de teste e devolve um dicionário."""
    if modelo is None:
        modelo = treinar()
    pipeline, limiar = modelo["pipeline"], modelo["limiar"]
    classes = list(pipeline.classes_)

    df = pd.read_csv(ARQ_CSV)
    teste = df[df["split"] == "test"].reset_index(drop=True)

    # Previsão de todas as frases do teste de uma vez
    proba = pipeline.predict_proba(teste["texto"])
    confianca = proba.max(axis=1)
    previsto = pipeline.classes_[proba.argmax(axis=1)]
    real = teste["dominio"].to_numpy()

    # --- Métricas gerais (sobre TODAS as frases, sem aplicar o limiar) ---
    acuracia = accuracy_score(real, previsto)
    f1_macro = f1_score(real, previsto, average="macro")

    # --- Relatório por classe ---
    rel = pd.DataFrame(
        classification_report(real, previsto, output_dict=True, zero_division=0)
    ).T
    por_classe = rel.loc[classes, ["precision", "recall", "f1-score", "support"]].copy()
    por_classe["support"] = por_classe["support"].astype(int)
    por_classe = por_classe.round(3).sort_values("f1-score")

    # --- Matriz de confusão simples (linhas = real, colunas = previsto) ---
    matriz = pd.crosstab(pd.Series(real, name="real"),
                         pd.Series(previsto, name="previsto"))
    matriz = matriz.reindex(index=classes, columns=classes, fill_value=0)

    # --- Análise de erros ---
    dados = pd.DataFrame({"texto": teste["texto"], "real": real,
                          "previsto": previsto, "confianca": confianca.round(2)})
    erros = dados[dados["real"] != dados["previsto"]]
    pares_erro = (erros.groupby(["real", "previsto"]).size()
                  .reset_index(name="qtd")
                  .sort_values("qtd", ascending=False).head(8)
                  .reset_index(drop=True))
    # Erros em que o modelo estava mais "confiante": os mais reveladores
    erros_confiantes = (erros.sort_values("confianca", ascending=False)
                        .head(10).reset_index(drop=True))

    # --- Efeito do limiar de confiança (só medimos, não ajustamos) ---
    aceitas = confianca >= limiar
    cobertura = float(aceitas.mean())
    precisao_aceitas = float((real[aceitas] == previsto[aceitas]).mean()) if aceitas.any() else 0.0

    return {"n_teste": len(teste), "n_erros": len(erros), "limiar": limiar,
            "acuracia": float(acuracia), "f1_macro": float(f1_macro),
            "cobertura": cobertura, "precisao_aceitas": precisao_aceitas,
            "por_classe": por_classe, "matriz": matriz,
            "pares_erro": pares_erro, "erros_confiantes": erros_confiantes}


def avaliar_frases_proprias():
    """Roda as frases próprias pelo modelo e marca OK/ERRO em cada uma."""
    linhas = []
    for frase, esperado in FRASES_PROPRIAS:
        r = prever(frase)
        if esperado is None:                       # fora do escopo: deve cair no fallback
            ok = not r["entendeu"]
        else:                                      # dentro do escopo: precisa acertar o domínio
            ok = r["entendeu"] and r["dominio"] == esperado
        linhas.append({"frase": frase,
                       "esperado": esperado or "fora do escopo",
                       "previsto": r["dominio"] or "-",
                       "confianca": round(r["confianca"], 2),
                       "entendeu": "sim" if r["entendeu"] else "não",
                       "resultado": "OK" if ok else "ERRO"})
    return pd.DataFrame(linhas)