"""Núcleo de análise: carrega o VADER, classifica frases e lista as palavras
que ele realmente reconheceu. Sem HTML e sem Streamlit."""
from __future__ import annotations

import re
from dataclasses import dataclass

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Convenção do VADER: compound >= 0,05 positivo; <= -0,05 negativo; entre os dois, neutro.
LIMIAR = 0.05


def carregar_analisador() -> SentimentIntensityAnalyzer:
    """Cria o analisador, baixando o léxico do VADER na primeira execução."""
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        nltk.download("vader_lexicon", quiet=True)
    try:
        return SentimentIntensityAnalyzer()
    except LookupError as erro:
        raise RuntimeError(
            "Não foi possível carregar o léxico do VADER (vader_lexicon). "
            "Verifique a conexão e tente novamente."
        ) from erro


def rotular(compound: float) -> str:
    """Converte o escore composto (-1 a +1) em 'positivo', 'negativo' ou 'neutro'."""
    if compound >= LIMIAR:
        return "positivo"
    if compound <= -LIMIAR:
        return "negativo"
    return "neutro"


def palavras_reconhecidas(sia: SentimentIntensityAnalyzer, texto: str) -> list[tuple[str, float]]:
    """Palavras do texto que existem no léxico do VADER, com a valência (-4 a +4).
    É uma aproximação: o VADER também aplica regras de negação, intensificação,
    maiúsculas e pontuação além do dicionário."""
    palavras = re.findall(r"[\w'\-]+", texto.lower())
    return [(p, sia.lexicon[p]) for p in palavras if p in sia.lexicon]


@dataclass
class Resultado:
    texto: str
    idioma: str                      # "pt" ou "en"
    neg: float
    neu: float
    pos: float
    compound: float
    rotulo: str
    esperado: str | None             # emoção real esperada (None = sem gabarito)
    palavras: list[tuple[str, float]]

    @property
    def acertou(self) -> bool | None:
        if self.esperado is None:
            return None
        return self.rotulo == self.esperado

    @property
    def coincidencias(self) -> list[str]:
        """Em português, toda palavra reconhecida é coincidência com o léxico
        inglês (o dicionário do VADER não tem português). Emoticons ficam de fora."""
        if self.idioma != "pt":
            return []
        return [p for p, _ in self.palavras if p.isalpha()]

    @property
    def acerto_acidental(self) -> bool:
        """Acertou em português, mas só por causa de palavras coincidentes."""
        return bool(
            self.acertou
            and self.coincidencias
            and len(self.coincidencias) == len(self.palavras)
        )


def analisar(
    sia: SentimentIntensityAnalyzer,
    texto: str,
    idioma: str,
    esperado: str | None = None,
) -> Resultado:
    escores = sia.polarity_scores(texto)
    return Resultado(
        texto=texto,
        idioma=idioma,
        neg=escores["neg"],
        neu=escores["neu"],
        pos=escores["pos"],
        compound=escores["compound"],
        rotulo=rotular(escores["compound"]),
        esperado=esperado,
        palavras=palavras_reconhecidas(sia, texto),
    )
