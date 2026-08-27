import nltk

# Definição da Gramática Livre de Contexto (CFG)
# ATENÇÃO TÉCNICA: A regra VP -> VBD isolada foi removida para evitar um
# "Shift-Reduce Conflict". O parser Bottom-Up do NLTK é greedy (ganancioso) 
# e reduziria o verbo prematuramente, ignorando os adjuntos adverbiais (ADVP) 
# e preposicionais (PP) logo em seguida.
GRAMMAR_STRING = """
  S -> NP VP
  NP -> DT NN | DT JJ NN
  VP -> VBD ADVP | VBD PP
  PP -> IN NP
  ADVP -> RB | JJ NN
  
  DT -> 'the'
  JJ -> 'white' | 'blue' | 'last'
  NN -> 'dog' | 'coffee' | 'floor' | 'car' | 'week'
  VBD -> 'died' | 'spilled' | 'crashed'
  RB -> 'yesterday'
  IN -> 'on'
"""

# Compila a string acima em um objeto de gramática do NLTK
cfg_grammar = nltk.CFG.fromstring(GRAMMAR_STRING)

def get_grammar():
    """
    Retorna a gramática CFG compilada.
    """
    return cfg_grammar

if __name__ == "__main__":
    # Teste estrutural para garantir que não há erros de sintaxe na string da CFG
    print("Gramática compilada com sucesso. Regras mapeadas:")
    for rule in cfg_grammar.productions():
        print(f" - {rule}")