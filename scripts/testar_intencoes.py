"""
Avaliação do motor no terminal (sem Streamlit).

Parte 1: F1 por classe na VALIDAÇÃO e regra de saída do e-mail.
Parte 2: teste manual com frases dentro e fora do escopo (fallback).
O split de TESTE não é usado aqui (fica para a Etapa 4).

Uso (a partir da raiz do repositório):  python scripts/testar_intencoes.py
"""
import sys
from pathlib import Path

# Rodando "python scripts/...", o Python só enxerga a pasta scripts/.
# Esta linha coloca a raiz do repositório no caminho para achar intent_engine/.
RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

import pandas as pd
from sklearn.metrics import classification_report

from intent_engine.model import ARQ_CSV, prever, treinar
from intent_engine.responses import nome_exibicao

LIMITE_EMAIL = 0.80   # regra do plano: e-mail com F1 abaixo disso e distante dos demais sai

# =========================================================================
# PARTE 1 — F1 por classe na validação
# =========================================================================
modelo = treinar()
pipeline = modelo["pipeline"]

df = pd.read_csv(ARQ_CSV)
val = df[df["split"] == "validation"]
previsto = pipeline.predict(val["texto"])

rel = pd.DataFrame(
    classification_report(val["dominio"], previsto, output_dict=True, zero_division=0)
).T
classes = [c for c in rel.index if c in set(val["dominio"])]       # só as linhas dos domínios

print("=== F1 por classe na validação ===")
print(rel.loc[classes, ["precision", "recall", "f1-score", "support"]]
      .sort_values("f1-score").round(3).to_string())
print(f"\nF1 macro: {rel.loc['macro avg', 'f1-score']:.3f} | "
      f"acurácia: {rel.loc['accuracy', 'f1-score']:.3f}")

# --- Regra de saída do e-mail ---
f1_email = rel.loc["email", "f1-score"]
outras = rel.loc[[c for c in classes if c != "email"], "f1-score"]
print(f"\nF1 do e-mail: {f1_email:.3f} | média das outras: {outras.mean():.3f} "
      f"| menor das outras: {outras.min():.3f}")
if f1_email < LIMITE_EMAIL and f1_email < outras.mean():
    print("-> REGRA: e-mail abaixo de 0,80 e abaixo dos demais: REMOVER (linha 7 do script de preparo).")
else:
    print("-> REGRA: e-mail NÃO está claramente abaixo dos demais: MANTER.")

# Com quais domínios o e-mail se confunde? (ajuda a explicar a decisão)
eh_email = (val["dominio"] == "email").values
print("\nE-mails reais classificados como:")
print(pd.Series(previsto[eh_email]).value_counts().to_string())
print("\nFrases de outros domínios classificadas como e-mail:")
falsos = pd.Series(val["dominio"].values[(previsto == "email") & ~eh_email])
print(falsos.value_counts().to_string() if len(falsos) else "(nenhuma)")

# =========================================================================
# PARTE 2 — Teste manual (esperado = None significa fora do escopo)
# =========================================================================
FRASES = [
    ("acorde-me às sete da manhã", "alarm"),
    ("vai chover amanhã?", "weather"),
    ("toca uma música animada", "play"),
    ("marca uma reunião com o João na sexta", "calendar"),
    ("que dia é hoje?", "datetime"),
    ("lê meu último e\u2011mail", "email"),             # \u2011 = hífen não separável
    ("alexa, apaga as luzes da sala", "iot"),            # palavra de ativação
    ("alexa, que horas são?", "datetime"),               # "alexa" não pode puxar para iot
    # --- fora do escopo: o esperado é "não entendi" ---
    ("qual é a capital da França?", None),
    ("me conta uma piada", None),
    ("como faço um bolo de chocolate?", None),
    ("asdfgh qwerty", None),
    ("por favor", None),                                 # some tudo na limpeza
]

print(f"\n=== Teste de terminal (limiar = {modelo['limiar']}) ===")
rejeitadas = fora = 0
for frase, esperado in FRASES:
    r = prever(frase)
    nome = nome_exibicao(r["dominio"]) if r["dominio"] else "-"
    top3 = ", ".join(f"{d} {p:.2f}" for d, p in r["top3"])
    if esperado is None:                                  # fora do escopo
        fora += 1
        rejeitadas += not r["entendeu"]
        marca = "OK " if not r["entendeu"] else "ERRO"    # deveria ter caído no fallback
    else:                                                 # dentro do escopo
        marca = "OK " if (r["entendeu"] and r["dominio"] == esperado) else "ERRO"
    estado = "" if r["entendeu"] else "  [NÃO ENTENDI]"
    print(f"{marca} {frase!r}\n     -> {nome} ({r['confianca']:.2f}){estado}  | top3: {top3}")

print(f"\nFora do escopo: {rejeitadas} de {fora} caíram no 'não entendi'.")