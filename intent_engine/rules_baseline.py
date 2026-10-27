"""
Baseline por REGRAS (estilo ELIZA / A.L.I.C.E., slide 4 da apresentação).

Serve só para comparar com o modelo de aprendizado de máquina: cada domínio
tem uma lista curta de palavras-chave (escrita à mão, a partir do conhecimento
dos domínios, SEM consultar o conjunto de teste e sem otimização).

Como decide:
  1) limpa a frase com a MESMA função do modelo (preprocessar);
  2) conta quantas palavras da frase COMEÇAM com algum radical de cada domínio;
  3) vence o domínio com mais palavras-chave; sem nenhuma, não responde.
Sem Streamlit: a página só exibe o resultado.
"""
import re

from intent_engine.preprocess import preprocessar

# Radicais já em minúsculas e SEM acento (preprocessar tira os acentos).
# A ORDEM importa em caso de empate: vale o primeiro domínio da lista, por isso
# os domínios mais genéricos (calendar e datetime) ficam por último.
REGRAS = {
    "alarm": ["alarm", "acord", "desperta", "soneca"],
    "weather": ["chov", "chuv", "clima", "previsao", "temperatura", "frio", "calor",
                "nublad", "ensolarad", "neve", "vento", "umidade"],
    "iot": ["luz", "lampada", "tomada", "termostato", "persiana", "cortina",
            "ventilador", "condicion", "aspirador", "cafeteira", "aquec", "acend"],
    "play": ["toc", "music", "cancao", "cancoes", "podcast", "play", "radio",
             "album", "ouvir", "pausa"],
    "email": ["email", "mail", "mensag", "contat", "caixa", "respond", "encaminh",
              "remetente", "spam", "envi"],
    "lists": ["list", "compras", "tarefa", "afazer", "anot", "adicion"],
    "news": ["notici", "manchete", "jornal", "reportagem", "acontec", "eleic", "politic"],
    "calendar": ["agend", "reuni", "event", "calendari", "compromiss", "lembr",
                 "convit", "aniversari"],
    "datetime": ["hora", "data", "dia", "fuso"],
}


def prever_regras(texto):
    """Classifica uma frase pelas regras. Devolve um dicionário:
    dominio (código, ou None se nenhuma palavra-chave foi reconhecida) e
    palavras (as palavras da frase que casaram com as regras do domínio)."""
    palavras = re.findall(r"[a-z0-9]+", preprocessar(texto))

    pontos, achadas = {}, {}
    for dominio, radicais in REGRAS.items():
        # startswith aceita uma tupla de começos de palavra
        casadas = [p for p in palavras if p.startswith(tuple(radicais))]
        if casadas:
            pontos[dominio] = len(casadas)
            achadas[dominio] = casadas

    if not pontos:                       # nenhuma palavra-chave: o baseline "não entende"
        return {"dominio": None, "palavras": []}

    # max() devolve o PRIMEIRO em caso de empate; a ordem de REGRAS desempata
    melhor = max(pontos, key=pontos.get)
    return {"dominio": melhor, "palavras": achadas[melhor]}