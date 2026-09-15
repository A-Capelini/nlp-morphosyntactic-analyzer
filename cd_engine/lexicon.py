"""
Léxico Semântico da Tarefa 2.

Mapeia verbos de superfície (em português) para as primitivas ACT da teoria
de Dependência Conceitual de Schank (1972), junto com as regras de
inferência que o parser (`cd_engine.parser`) usa para preencher os slots
obrigatórios de cada frame.

Adicionar um novo verbo suportado é só adicionar uma nova entrada aqui —
o parser em `parser.py` não precisa ser tocado, desde que o ACT já tenha
um ramo implementado lá.
"""

SEMANTIC_LEXICON = {
    "deu": {
        "act": "ATRANS",             # transferência de posse/controle
        "origin_is_actor": True,     # quem dá é sempre a origem
    },
    "comeu": {
        "act": "INGEST",             # ingestão de algo para o corpo
        "infer_dest": "estômago",    # destino final inferido
        "instrument_act": "MOVE",    # instrumento inferido: mão -> boca
    },
    "foi": {
        "act": "PTRANS",             # transferência de localização física
        "obj_is_actor": True,        # o ator move o próprio corpo
    },
}


def tokenize(frase: str) -> list[str]:
    """Fase 1 (Análise Léxica): tokenização simplificada por espaços.

    Numa análise POS/NER completa isso viria de um pipeline como o SpaCy;
    aqui usamos um recorte didático que assume a ordem fixa
    Ator-Verbo-Complemento, suficiente para o escopo da Tarefa 2.

    A capitalização original é preservada (não damos `.lower()` na frase
    inteira) para que nomes próprios como "Ana" ou "Cotia" apareçam
    corretamente no frame final — só o verbo é comparado em minúsculas
    no léxico, dentro de `cd_engine.parser`.
    """
    return frase.strip().split()


def verbos_suportados() -> list[str]:
    """Lista os verbos atualmente cobertos pelo léxico (para uso na UI)."""
    return sorted(SEMANTIC_LEXICON)
