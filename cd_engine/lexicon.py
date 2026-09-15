"""
Léxico Semântico da Tarefa 2.

Mapeia verbos de superfície (em português) para as primitivas ACT da teoria
de Dependência Conceitual de Schank (1972), junto com as regras de
inferência que o parser (`cd_engine.parser`) usa para preencher os slots
obrigatórios de cada frame.

Adicionar um novo verbo suportado é só adicionar uma nova entrada aqui —
o parser em `parser.py` não precisa ser tocado, desde que o ACT já tenha
um ramo implementado lá.

O léxico cobre pelo menos dois verbos para cada uma das 9 primitivas
clássicas de Schank, para que "o professor escolhe a frase na hora" tenha
uma chance razoável de cair em algo suportado — mas o conjunto continua
fechado de propósito: é a própria teoria da CD que trabalha com um número
fechado de primitivas, não uma limitação técnica deste código (ver
`parser.UnknownVerbError` para como isso é comunicado na interface).
"""

SEMANTIC_LEXICON = {
    # --- ATRANS: transferência de posse/controle -------------------------
    "deu":     {"act": "ATRANS", "direction": "gives"},
    "vendeu":  {"act": "ATRANS", "direction": "gives"},
    "doou":    {"act": "ATRANS", "direction": "gives"},
    "comprou": {"act": "ATRANS", "direction": "receives"},

    # --- PTRANS: transferência de localização física ---------------------
    "foi":       {"act": "PTRANS", "obj_is_actor": True},
    "andou":     {"act": "PTRANS", "obj_is_actor": True},
    "empurrou":  {"act": "PTRANS", "obj_is_actor": False},

    # --- PROPEL: aplicação forçada de energia física ----------------------
    "chutou":      {"act": "PROPEL"},
    "arremessou":  {"act": "PROPEL"},

    # --- MOVE: movimento de uma parte do próprio corpo --------------------
    "piscou":    {"act": "MOVE"},
    "mastigou":  {"act": "MOVE"},

    # --- GRASP: agarrar/segurar um objeto físico ---------------------------
    "segurou": {"act": "GRASP"},
    "pegou":   {"act": "GRASP"},

    # --- INGEST: ingestão de algo para o corpo -----------------------------
    "comeu":  {"act": "INGEST", "infer_dest": "estômago", "instrument_act": "MOVE"},
    "bebeu":  {"act": "INGEST", "infer_dest": "estômago", "instrument_act": "MOVE"},

    # --- EXPEL: expulsão forçada de fluidos/gases do corpo ------------------
    "cuspiu":  {"act": "EXPEL"},
    "chorou":  {"act": "EXPEL"},

    # --- MTRANS: transferência de informação mental -------------------------
    "falou":  {"act": "MTRANS"},
    "leu":    {"act": "MTRANS"},

    # --- MBUILD: criação de novos pensamentos a partir de dados --------------
    "pensou":   {"act": "MBUILD"},
    "decidiu":  {"act": "MBUILD"},
}

# Artigos e preposições comuns: removidos antes da extração de slots para
# tolerar frases mais naturais ("Ana deu o livro para Maria") sem precisar
# de um POS tagger de verdade — ver `parser.parse_sentence`.
STOPWORDS = {
    "o", "a", "os", "as", "um", "uma", "uns", "umas",
    "para", "de", "do", "da", "dos", "das", "no", "na", "nos", "nas",
    "em", "com", "ao", "à", "aos", "às",
}


def tokenize(frase: str) -> list[str]:
    """Fase 1 (Análise Léxica): tokenização simplificada por espaços.

    Numa análise POS/NER completa isso viria de um pipeline como o SpaCy;
    aqui usamos um recorte didático suficiente para o escopo da Tarefa 2.

    A capitalização original é preservada (não damos `.lower()` na frase
    inteira) para que nomes próprios como "Ana" ou "Cotia" apareçam
    corretamente no frame final — comparações com o léxico usam
    `.lower()` pontualmente, em `parser.py`.
    """
    return frase.strip().split()


def content_tokens(tokens: list[str]) -> list[str]:
    """Remove artigos/preposições da lista de tokens, mantendo a ordem.

    Não é POS tagging — é um filtro raso por lista fixa (`STOPWORDS`) que
    permite frases como "Ana deu o livro para Maria" sem que "o" ou "para"
    atrapalhem a extração posicional do objeto e do destino.
    """
    return [t for t in tokens if t.lower() not in STOPWORDS]


def verbos_suportados() -> list[str]:
    """Lista (ordenada) todos os verbos cobertos pelo léxico."""
    return sorted(SEMANTIC_LEXICON)


def verbos_por_primitiva() -> dict[str, list[str]]:
    """Agrupa os verbos suportados por primitiva ACT (para uso na UI)."""
    grupos: dict[str, list[str]] = {}
    for verbo, regra in SEMANTIC_LEXICON.items():
        grupos.setdefault(regra["act"], []).append(verbo)
    return {act: sorted(verbos) for act, verbos in sorted(grupos.items())}
