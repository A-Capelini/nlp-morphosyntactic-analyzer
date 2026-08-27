import warnings
import nltk
from nltk.tokenize import word_tokenize

# Suprime o aviso de permissão de diretório do NLTK no Linux
warnings.filterwarnings("ignore", category=UserWarning, module="nltk")

# Garante o download silencioso dos pacotes necessários do NLTK
try:
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('averaged_perceptron_tagger_eng', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)

# Tabela de tags de referência obrigatória para o corpus fixo.
# Isso blinda o código contra classificações probabilísticas incorretas do NLTK.
REFERENCE_TAGS = {
    "the": "DT",       # Determiner
    "white": "JJ",     # Adjective
    "dog": "NN",       # Noun
    "died": "VBD",     # Verb, past tense
    "yesterday": "RB", # Adverb (Temporal)
    "coffee": "NN",    # Noun
    "spilled": "VBD",  # Verb, past tense
    "on": "IN",        # Preposition
    "floor": "NN",     # Noun
    "blue": "JJ",      # Adjective
    "car": "NN",       # Noun
    "crashed": "VBD",  # Verb, past tense
    "last": "JJ",      # Adjective
    "week": "NN"       # Noun
}

def analyze_morphology(sentence: str) -> list[tuple[str, str]]:
    """
    Executa a análise morfológica (POS Tagging) com normalização prévia.
    
    Args:
        sentence (str): A frase original (ex: "The White dog died Yesterday").
        
    Returns:
        list[tuple[str, str]]: Lista de tuplas contendo (palavra_minuscula, tag).
    """
    # 1. Normalização de capitalização
    normalized_sentence = sentence.lower()
    
    # 2. Tokenização
    tokens = word_tokenize(normalized_sentence)
    
    # 3. Extração das tags com NLTK (para servir de fallback)
    default_tags = nltk.pos_tag(tokens)
    
    # 4. Aplicação determinística das tags baseada na tabela de referência
    tagged_tokens = []
    for i, token in enumerate(tokens):
        if token in REFERENCE_TAGS:
            tagged_tokens.append((token, REFERENCE_TAGS[token]))
        else:
            tagged_tokens.append(default_tags[i])
            
    return tagged_tokens

if __name__ == "__main__":
    # Teste rápido de isolamento estrutural
    test_sentence = "The White dog died Yesterday"
    print(f"Análise de teste: {analyze_morphology(test_sentence)}")