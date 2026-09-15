"""
Estrutura de dados do frame de Dependência Conceitual (CD).

Este módulo pertence apenas à Tarefa 2 (Dependência Conceitual) e não é
compartilhado com o `nlp_engine` usado pela Tarefa 03 (parsing sintático) —
cada trabalho mantém os seus próprios arquivos.
"""


class ConceptualDependencyFrame:
    """Representa um frame CD: ATOR -> ACT -> OBJETO, com direção e instrumento.

    Segue a notação de Schank (1972): ACTOR realiza uma primitiva ACT sobre
    um OBJECT, que se move de uma origem (FROM) para um destino (TO), podendo
    depender de um INSTRUMENT — outro frame CD encaixado (ex.: o MOVE da mão
    até a boca dentro de um INGEST).
    """

    def __init__(self, actor, act, obj=None, origin=None, recipient=None, instrument=None):
        self.actor = actor
        self.act = act
        self.obj = obj
        self.origin = origin
        self.recipient = recipient
        self.instrument = instrument

    def to_dict(self):
        """Serializa o frame em dict (pronto para `st.json` / `json.dumps`).

        Resolve o instrumento de forma recursiva quando ele também é um
        ConceptualDependencyFrame, para que o aninhamento apareça por
        completo na saída.
        """
        inst = self.instrument
        if isinstance(inst, ConceptualDependencyFrame):
            inst = inst.to_dict()

        return {
            "ACTOR": self.actor,
            "ACT": self.act,
            "OBJECT": self.obj,
            "DIRECTION": {"FROM": self.origin, "TO": self.recipient},
            "INSTRUMENT": inst,
        }

    def __repr__(self):
        return f"ConceptualDependencyFrame({self.act}, actor={self.actor!r}, obj={self.obj!r})"
