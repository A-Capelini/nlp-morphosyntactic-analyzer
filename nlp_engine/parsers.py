import sys
import os
import nltk

# Adiciona o diretório raiz do projeto ao path do Python para resolver as importações
# absolutas quando o script é executado diretamente via terminal.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp_engine.morphology import analyze_morphology
from nlp_engine.grammar_rules import get_grammar

def get_tokens(sentence: str) -> list[str]:
    """
    Utiliza o motor morfológico para normalizar a frase e extrair os tokens.
    Como a nossa CFG mapeia os terminais (palavras), precisamos apenas 
    da lista de palavras em minúsculas extraída das tuplas.
    """
    tagged_tokens = analyze_morphology(sentence)
    return [word for word, tag in tagged_tokens]

def run_top_down(sentence: str):
    """
    Executa a análise sintática utilizando o método Recursive Descent (Top-Down).
    """
    grammar = get_grammar()
    parser = nltk.RecursiveDescentParser(grammar)
    tokens = get_tokens(sentence)
    
    # O NLTK retorna um gerador, convertemos para lista para capturar todas as árvores possíveis
    try:
        return list(parser.parse(tokens))
    except ValueError as e:
        print(f"Erro no parser Top-Down: {e}")
        return []

def run_bottom_up(sentence: str):
    """
    Executa a análise sintática utilizando o método Shift-Reduce (Bottom-Up).
    """
    grammar = get_grammar()
    parser = nltk.ShiftReduceParser(grammar)
    tokens = get_tokens(sentence)
    
    try:
        return list(parser.parse(tokens))
    except ValueError as e:
        print(f"Erro no parser Bottom-Up: {e}")
        return []

if __name__ == "__main__":
    # Teste de integração das três sentenças do escopo acadêmico
    sentences = [
        "The White dog died Yesterday",
        "The coffee spilled on the floor",
        "The blue car crashed last week"
    ]
    
    for sent in sentences:
        print(f"\nFrase: '{sent}'")
        
        print("  [Top-Down]")
        td_trees = run_top_down(sent)
        if td_trees:
            for tree in td_trees:
                print(f"    {tree}")
        else:
            print("    Nenhuma árvore encontrada.")
            
        print("  [Bottom-Up]")
        bu_trees = run_bottom_up(sent)
        if bu_trees:
            for tree in bu_trees:
                print(f"    {tree}")
        else:
            print("    Nenhuma árvore encontrada.")