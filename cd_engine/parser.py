"""
Parser da Tarefa 2 — Fases 2 a 4 da Dependência Conceitual.

Fase 1 (tokenização) fica em `lexicon.tokenize` / `lexicon.content_tokens`.
Este módulo cuida de:
  Fase 2 — Mapeamento Ontológico (verbo de superfície -> ACT)
  Fase 3 — Extração de Slots (ator, objeto, origem, destino)
  Fase 4 — Resolução de Inferências (instrumento e destinos ocultos)

O parser é tolerante a artigos/preposições comuns ("o", "a", "para", ...) e
não exige que o verbo esteja exatamente na segunda posição — ele procura,
token a token, o primeiro que bate com o léxico semântico. Isso cobre frases
como "A Ana deu o livro para a Maria", não só "Ana deu livro Maria". O que o
parser *não* faz é reconhecer verbos fora do léxico ou conjugações não
cadastradas (ex.: "come" em vez de "comeu") — isso é intencional: a
Dependência Conceitual trabalha com um conjunto fechado de primitivas
conceituais, então um vocabulário fechado é fiel à teoria, não uma
limitação de engenharia.
"""

from cd_engine.frames import ConceptualDependencyFrame
from cd_engine.lexicon import SEMANTIC_LEXICON, content_tokens, tokenize, verbos_suportados


class UnknownVerbError(ValueError):
    """Levantado quando nenhum token da frase bate com o léxico semântico."""


def _slot(lista, indice, default=None):
    """Acesso seguro a uma posição da lista (evita IndexError em frases curtas)."""
    return lista[indice] if -len(lista) <= indice < len(lista) else default


def locate_verb(content: list[str]):
    """Fase 2 (Mapeamento Ontológico): procura, a partir da posição 1, o
    primeiro token que bate com o léxico semântico — tolera complementos e
    preposições no meio do caminho, e não exige o verbo exatamente na
    segunda posição.

    Retorna (índice, verbo, regra) ou None se nenhum token bater com o
    léxico. Fica separado de `parse_sentence` para que a página da Tarefa 2
    reaproveite a mesma busca ao narrar o passo a passo, em vez de duplicar
    a lógica.
    """
    for i in range(1, len(content)):
        regra = SEMANTIC_LEXICON.get(content[i].lower())
        if regra is not None:
            return i, content[i], regra
    return None


def parse_sentence(frase: str) -> ConceptualDependencyFrame:
    """Converte uma frase em português em um frame CD completo."""
    tokens = tokenize(frase)
    content = content_tokens(tokens)

    if len(content) < 2:
        raise ValueError(
            "A frase precisa de ao menos um Ator e um Verbo "
            "(ex.: 'Ana comeu maca')."
        )

    actor = content[0]

    encontrado = locate_verb(content)
    if encontrado is None:
        disponiveis = ", ".join(verbos_suportados())
        raise UnknownVerbError(
            f"Nenhum verbo da frase está entre as primitivas suportadas. "
            f"Verbos disponíveis no momento: {disponiveis}."
        )

    verbo_idx, verbo, regra = encontrado
    resto = content[verbo_idx + 1:]  # tokens após o verbo: objeto, destino etc.
    act = regra["act"]

    # --- ATRANS: transferência de posse -----------------------------------
    if act == "ATRANS":
        obj = _slot(resto, 0, "algo")
        if regra.get("direction") == "receives":
            # Ex.: "Ana comprou pão [da padaria]" -> Ana recebe
            origem = _slot(resto, -1, "desconhecido") if len(resto) > 1 else "desconhecido"
            destino = actor
        else:
            # Ex.: "Ana deu livro [para] Maria" -> Ana dá
            origem = actor
            destino = _slot(resto, -1, "desconhecido") if len(resto) > 1 else "desconhecido"
        return ConceptualDependencyFrame(actor, act, obj, origin=origem, recipient=destino)

    # --- PTRANS: transferência de localização física ------------------------
    if act == "PTRANS":
        obj = actor if regra.get("obj_is_actor") else _slot(resto, 0, "algo")
        destino = _slot(resto, -1, "desconhecido")
        return ConceptualDependencyFrame(actor, act, obj, origin="Local_Atual", recipient=destino)

    # --- PROPEL: aplicação forçada de energia física -------------------------
    if act == "PROPEL":
        obj = _slot(resto, 0, "algo")
        destino = _slot(resto, -1) if len(resto) > 1 else None
        return ConceptualDependencyFrame(actor, act, obj, origin=actor, recipient=destino)

    # --- MOVE: movimento de uma parte do próprio corpo do ator ----------------
    if act == "MOVE":
        # Sem complemento (ex.: "Ana piscou") -> movimento do próprio corpo
        obj = _slot(resto, 0, "próprio corpo")
        return ConceptualDependencyFrame(actor, act, obj, origin=actor, recipient=actor)

    # --- GRASP: agarrar/segurar um objeto físico -------------------------------
    if act == "GRASP":
        obj = _slot(resto, 0, "algo")
        return ConceptualDependencyFrame(actor, act, obj, origin="mão", recipient=actor)

    # --- INGEST: ingestão de algo para o corpo -----------------------------------
    if act == "INGEST":
        obj = _slot(resto, 0, "algo")
        # Inferência do instrumento: para comer/beber, a mão leva o objeto à boca
        instrumento = ConceptualDependencyFrame(
            actor, regra.get("instrument_act", "MOVE"), obj,
            origin="mão", recipient=f"{actor}.boca",
        )
        # infer_dest completa o destino final oculto (o estômago)
        return ConceptualDependencyFrame(
            actor, act, obj,
            origin="mundo_externo",
            recipient=f"{actor}.{regra['infer_dest']}",
            instrument=instrumento,
        )

    # --- EXPEL: expulsão forçada de fluidos/gases do corpo -------------------------
    if act == "EXPEL":
        # Inferência simétrica ao INGEST: o que sai do corpo vai para o mundo externo
        obj = _slot(resto, 0, "algo")
        return ConceptualDependencyFrame(actor, act, obj, origin=actor, recipient="mundo_externo")

    # --- MTRANS: transferência de informação mental ---------------------------------
    if act == "MTRANS":
        obj = _slot(resto, 0, "algo")
        destino = _slot(resto, -1, "desconhecido") if len(resto) > 1 else "desconhecido"
        return ConceptualDependencyFrame(actor, act, obj, origin=actor, recipient=destino)

    # --- MBUILD: criação de novos pensamentos a partir de dados ----------------------
    if act == "MBUILD":
        # Inferência: o pensamento nasce de dados/experiência prévia e permanece
        # na mente do próprio ator (origem e destino não são localizações físicas)
        obj = _slot(resto, 0, "uma ideia")
        return ConceptualDependencyFrame(actor, act, obj, origin="dados/experiência", recipient=actor)

    raise NotImplementedError(f"ACT '{act}' ainda não implementado.")


if __name__ == "__main__":
    # Teste rápido de isolamento estrutural (sem depender do Streamlit)
    testes = [
        "Ana deu livro Maria",
        "A Ana deu o livro para a Maria",
        "Ana comeu maca",
        "Pedro foi para Cotia",
        "Ana comprou pão na padaria",
        "Pedro chutou a bola para o gol",
        "Ana piscou",
        "Pedro segurou a caneta",
        "Ana cuspiu",
        "Pedro falou a verdade para Ana",
        "Ana decidiu viajar",
    ]
    for frase in testes:
        frame = parse_sentence(frase)
        print(f"'{frase}' ->", frame.to_dict())
