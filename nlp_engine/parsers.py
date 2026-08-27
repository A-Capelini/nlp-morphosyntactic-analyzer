import io
import nltk
from contextlib import redirect_stdout

from nlp_engine.morphology import analyze_morphology
from nlp_engine.grammar_rules import get_grammar

def get_tokens(sentence: str) -> list[str]:
    tagged_tokens = analyze_morphology(sentence)
    return [word for word, tag in tagged_tokens]

def run_top_down(sentence: str):
    """
    Retorna uma tupla contendo: (lista_de_arvores, string_do_log)
    """
    grammar = get_grammar()
    parser = nltk.RecursiveDescentParser(grammar, trace=2) # trace=2 ativa o log
    tokens = get_tokens(sentence)
    
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            trees = list(parser.parse(tokens))
        except ValueError as e:
            print(f"Erro no parser Top-Down: {e}")
            trees = []
            
    return trees, f.getvalue()

def run_bottom_up(sentence: str):
    """
    Retorna uma tupla contendo: (lista_de_arvores, string_do_log)
    """
    grammar = get_grammar()
    parser = nltk.ShiftReduceParser(grammar, trace=2) # trace=2 ativa o log
    tokens = get_tokens(sentence)
    
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            trees = list(parser.parse(tokens))
        except ValueError as e:
            print(f"Erro no parser Bottom-Up: {e}")
            trees = []
            
    return trees, f.getvalue()

if __name__ == "__main__":
    # sys.path só precisa ser mexido quando este arquivo roda como script
    # isolado (fora do pacote nlp_engine). Import feito aqui dentro para não
    # afetar o app.py quando este módulo é apenas importado normalmente.
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    sentences = ["The White dog died Yesterday"]
    for sent in sentences:
        print(f"\nFrase: '{sent}'")
        td_trees, td_log = run_top_down(sent)
        print("Log Top-Down capturado com sucesso.")
