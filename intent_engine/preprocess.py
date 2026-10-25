"""
Pré-processamento de texto do assistente de intenções.

A MESMA função (preprocessar) é usada no treino e na frase digitada pelo
usuário. Assim o modelo sempre vê o texto no mesmo formato.
Não usa NLTK: a lista de stopwords é própria, para não depender de download
(que falha no Streamlit Cloud).
"""
import re
import unicodedata

from unidecode import unidecode

# Stopwords curtas, já sem acento (o texto passa pelo unidecode antes).
# Ficam de FORA palavras que carregam intenção: "hoje", "amanha", "nao",
# "mais", "menos", "para", "que", "quando", "como", etc.
STOPWORDS = {
    # artigos e preposições comuns
    "a", "o", "as", "os", "um", "uma", "uns", "umas",
    "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas",
    "ao", "aos", "e", "ou", "com",
    # pronomes pessoais e possessivos
    "eu", "me", "te", "tu", "voce", "meu", "minha", "meus", "minhas",
    "seu", "sua",
    # cortesia (não indica a intenção)
    "por", "favor", "pode", "podes", "poderia", "ola",
    # palavras de ativação do dataset (risco de atalho, ex.: "alexa" em iot)
    "ei", "hei", "olly", "alexa", "siri",
}


def preprocessar(texto: str) -> str:
    """Limpa o texto: Unicode, minúsculas, sem acentos, sem pontuação, sem stopwords."""
    if not isinstance(texto, str):
        return ""

    # 1) Normaliza Unicode (NFKC): o hífen não separável U+2011 vira hífen comum
    texto = unicodedata.normalize("NFKC", texto)

    # 2) Minúsculas e remoção de acentos ("último" -> "ultimo")
    texto = unidecode(texto.lower())

    # 3) Unifica "e-mail" / "e mail" em "email" ANTES de tirar a pontuação;
    #    senão o "e" vira stopword e sobra só "mail"
    texto = re.sub(r"\be[-\s]mail", "email", texto)

    # 4) Troca tudo que não é letra ou número por espaço (pontuação, hífens)
    texto = re.sub(r"[^a-z0-9]+", " ", texto)

    # 5) Remove stopwords e junta de novo com espaço simples
    palavras = [p for p in texto.split() if p not in STOPWORDS]
    return " ".join(palavras)