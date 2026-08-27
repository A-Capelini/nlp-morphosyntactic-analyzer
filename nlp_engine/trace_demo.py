import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nltk
from nlp_engine.grammar_rules import get_grammar
from nlp_engine.morphology import analyze_morphology

def show_step_by_step():
    sentence = "The White dog died Yesterday"
    grammar = get_grammar()
    tokens = [word for word, tag in analyze_morphology(sentence)]

    print("\n" + "="*50)
    print(" 🏗️ PASSO A PASSO: TOP-DOWN (Desenhando a Planta)")
    print("="*50)
    td_parser = nltk.RecursiveDescentParser(grammar, trace=2)
    list(td_parser.parse(tokens))

    print("\n" + "="*50)
    print(" 🧱 PASSO A PASSO: BOTTOM-UP (Empilhando Tijolos)")
    print("="*50)
    bu_parser = nltk.ShiftReduceParser(grammar, trace=2)
    list(bu_parser.parse(tokens))

if __name__ == "__main__":
    show_step_by_step()
