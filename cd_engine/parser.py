"""
Parser da Tarefa 2 — Fases 2 a 4 da Dependência Conceitual.

Fase 1 (tokenização) fica em `lexicon.tokenize`. Este módulo cuida de:
  Fase 2 — Mapeamento Ontológico (verbo de superfície -> ACT)
  Fase 3 — Extração de Slots (ator, objeto, origem, destino)
  Fase 4 — Resolução de Inferências (instrumento e destinos ocultos)
"""

from cd_engine.frames import ConceptualDependencyFrame
from cd_engine.lexicon import SEMANTIC_LEXICON, tokenize, verbos_suportados


class UnknownVerbError(ValueError):
    """Levantado quando o verbo da frase não está no léxico semântico."""


def parse_sentence(frase: str) -> ConceptualDependencyFrame:
    """Converte uma frase 'Ator Verbo Complemento' em um frame CD completo."""
    tokens = tokenize(frase)
    if len(tokens) < 3:
        raise ValueError(
            "A frase precisa de ao menos Ator, Verbo e Complemento "
            "(ex.: 'Ana comeu maca')."
        )

    actor, verbo = tokens[0], tokens[1]
    regra = SEMANTIC_LEXICON.get(verbo.lower())
    if regra is None:
        disponiveis = ", ".join(verbos_suportados())
        raise UnknownVerbError(
            f"Verbo '{verbo}' fora do léxico semântico. "
            f"Verbos suportados no momento: {disponiveis}."
        )

    act = regra["act"]

    if act == "ATRANS":
        # Ex.: "Ana deu livro Maria" -> transferência de posse
        obj = tokens[2]
        origem = actor if regra.get("origin_is_actor") else "desconhecido"
        destino = tokens[-1]
        return ConceptualDependencyFrame(
            actor, act, obj, origin=origem, recipient=destino
        )

    if act == "PTRANS":
        # Regra obj_is_actor: quando o próprio ator se desloca (ex.: "foi"),
        # o objeto do movimento é o corpo do próprio ator
        obj = actor if regra.get("obj_is_actor") else tokens[2]
        destino = tokens[-1]
        return ConceptualDependencyFrame(
            actor, act, obj, origin="Local_Atual", recipient=destino
        )

    if act == "INGEST":
        obj = tokens[2]
        # Inferência do instrumento: para comer, a mão leva o objeto à boca
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

    raise NotImplementedError(f"ACT '{act}' ainda não implementado.")


if __name__ == "__main__":
    # Teste rápido de isolamento estrutural (sem depender do Streamlit)
    testes = ["Ana deu livro Maria", "Ana comeu maca", "Pedro foi para Cotia"]
    for frase in testes:
        frame = parse_sentence(frase)
        print(f"'{frase}' ->", frame.to_dict())
