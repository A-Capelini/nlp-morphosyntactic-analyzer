"""
Modelo do assistente de intenções: TF-IDF (unigramas + bigramas) + Regressão Logística.

- treinar(): lê o CSV recortado, treina SÓ com o split 'train' e escolhe o
  limiar de confiança usando o split 'validation'. O split 'test' NÃO é usado aqui.
- prever(texto): devolve domínio, confiança, top-3 e se o modelo "entendeu".
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from intent_engine.preprocess import preprocessar

# --- Configurações --------------------------------------------------------
RAIZ = Path(__file__).resolve().parents[1]
ARQ_CSV = RAIZ / "data" / "intent_assistant" / "massive_ptbr_subset.csv"

ALVO_PRECISAO = 0.95     # precisão mínima desejada entre as respostas aceitas

# Limiar fixado em 0,35 (25/10, Etapa 4). Histórico: o limiar automático (0,25)
# deixava passar frases fora do escopo (ex.: "como faço um bolo de chocolate?" = 0,27);
# 0,30 ainda aceitava "qual é a raiz quadrada de 144?" (clima, 0,34) nas frases próprias.
# Escolhido com validação + frases próprias, NUNCA com o split de teste.
# Para voltar ao limiar automático da validação, troque por None.
LIMIAR_MANUAL = 0.35

# Modelo guardado em memória depois do primeiro treino
_MODELO = None


def escolher_limiar(pipeline, textos_val, y_val):
    """Escolhe o limiar de confiança na VALIDAÇÃO.

    Testa limiares de 0,20 a 0,90 e calcula, para cada um:
      - cobertura: % de frases que o modelo aceita responder;
      - precisão: % de acerto entre as frases aceitas.
    Fica com o MENOR limiar cuja precisão chega ao alvo (= maior cobertura).
    """
    proba = pipeline.predict_proba(textos_val)
    confianca = proba.max(axis=1)
    previsto = pipeline.classes_[proba.argmax(axis=1)]
    acertou = previsto == np.asarray(y_val)

    tabela = []
    for limiar in np.arange(0.20, 0.91, 0.05):
        aceitas = confianca >= limiar
        cobertura = aceitas.mean()
        precisao = acertou[aceitas].mean() if aceitas.any() else 0.0
        tabela.append((round(float(limiar), 2), float(cobertura), float(precisao)))

    # primeiro limiar (o menor) que atinge a precisão-alvo
    validos = [t for t in tabela if t[2] >= ALVO_PRECISAO]
    if validos:
        limiar = validos[0][0]
    else:  # nenhum atinge: usa o de maior precisão
        limiar = max(tabela, key=lambda t: t[2])[0]
    return limiar, tabela


def treinar(mostrar=False):
    """Treina o modelo e guarda em memória. Devolve um dicionário com
    o pipeline, o limiar escolhido e a tabela de limiares."""
    global _MODELO

    df = pd.read_csv(ARQ_CSV)
    treino = df[df["split"] == "train"]
    validacao = df[df["split"] == "validation"]

    pipeline = Pipeline([
        # O preprocessador é a MESMA função usada na entrada do usuário.
        # token_pattern aceita palavras de 1 letra/dígito (ex.: "7" em "acorde 7 manha").
        ("tfidf", TfidfVectorizer(preprocessor=preprocessar,
                                  token_pattern=r"(?u)\b\w+\b",
                                  ngram_range=(1, 2))),
        # class_weight='balanced' compensa classes pequenas (datetime) x grandes (calendar)
        ("clf", LogisticRegression(class_weight="balanced",
                                   random_state=42, max_iter=1000)),
    ])
    pipeline.fit(treino["texto"], treino["dominio"])

    limiar, tabela = escolher_limiar(pipeline, validacao["texto"], validacao["dominio"])
    if LIMIAR_MANUAL is not None:
        limiar = LIMIAR_MANUAL

    if mostrar:
        print(f"Treino: {len(treino)} frases | Validação: {len(validacao)} frases")
        print("limiar | cobertura | precisão entre aceitas")
        for lim, cob, prec in tabela:
            print(f"{lim:6.2f} | {cob:9.1%} | {prec:9.1%}")
        print(f"Limiar em uso: {limiar}")

    _MODELO = {"pipeline": pipeline, "limiar": limiar, "tabela": tabela}
    return _MODELO


def prever(texto):
    """Classifica uma frase. Devolve um dicionário:
    dominio (código do melhor palpite), confianca (0 a 1),
    top3 (lista de (domínio, probabilidade)) e entendeu (True se confiança >= limiar)."""
    if _MODELO is None:
        treinar()
    pipeline, limiar = _MODELO["pipeline"], _MODELO["limiar"]

    # Se sobrar texto vazio depois da limpeza (só stopwords/pontuação), não há o que classificar
    if preprocessar(texto) == "":
        return {"dominio": None, "confianca": 0.0, "top3": [], "entendeu": False}

    proba = pipeline.predict_proba([texto])[0]
    ordem = np.argsort(proba)[::-1][:3]                      # 3 maiores probabilidades
    top3 = [(str(pipeline.classes_[i]), float(proba[i])) for i in ordem]
    dominio, confianca = top3[0]
    return {"dominio": dominio, "confianca": confianca,
            "top3": top3, "entendeu": confianca >= limiar}