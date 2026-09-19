"""Corpus do exercício: as 4 frases da tarefa, as frases de controle e os
exemplos do campo livre. Trocar uma frase aqui já atualiza a página inteira.

Cada frase traz o texto original (pt), a tradução para o inglês (en, o mais
fiel possível, porque o léxico do VADER é em inglês) e a emoção ESPERADA, que
é a emoção real da frase lida em contexto (leitura pragmática).
"""

FRASES = [
    {
        "categoria": "1. Triste parecendo triste",
        "pt": "Hoje perdi meu emprego e não tenho dinheiro para pagar o aluguel no fim do mês.",
        "en": "Today I lost my job and I don't have money to pay the rent at the end of the month.",
        "esperado": "negativo",
        "nota": "Relato direto de perda: o vocabulário e a emoção real apontam para o mesmo lado.",
    },
    {
        "categoria": "2. Triste parecendo alegre (sarcasmo)",
        "pt": "Que maravilha, meu carro quebrou no meio da rodovia e agora vou poder fazer "
              "uma caminhada sob o sol do meio-dia!",
        "en": "How wonderful, my car broke down in the middle of the highway and now I will "
              "get to take a walk under the midday sun!",
        "esperado": "negativo",
        "nota": "Sarcasmo: o tom entusiasmado é irônico, a emoção real é frustração.",
    },
    {
        "categoria": "3. Exaltação parecendo triste",
        "pt": "Foi com muita dor, suor e lágrimas que finalmente conquistei a tão sonhada "
              "aprovação no concurso!",
        "en": "It was with a lot of pain, sweat and tears that I finally achieved the "
              "much-dreamed-of approval in the civil service exam!",
        "esperado": "positivo",
        "nota": "Superação: a dor valoriza a conquista, a emoção real é de alegria e orgulho.",
    },
    {
        "categoria": "4. Alegre parecendo alegre",
        "pt": "Estou extremamente feliz porque acabo de ganhar uma bolsa de estudos integral "
              "para a universidade dos meus sonhos!",
        "en": "I am extremely happy because I just won a full scholarship to the "
              "university of my dreams!",
        "esperado": "positivo",
        "nota": "Alegria literal, sem ironia: vocabulário e emoção real coincidem.",
    },
]

# Testes de sensibilidade: pequenas mudanças em uma frase para descobrir POR QUE
# o VADER acertou ou errou.
FRASES_CONTROLE = [
    {
        "controle": "A",
        "idioma": "pt",
        "texto": "O relógio está no meio da sala.",
        "esperado": "neutro",
        "por_que": "Frase neutra em português com “no” (em + o). O “no” do léxico inglês "
                   "significa “não” e vale −1,2: o VADER lê negatividade onde não há.",
    },
    {
        "controle": "B",
        "idioma": "en",
        "texto": "My car broke down in the middle of the highway and now I will get to "
                 "take a walk under the midday sun!",
        "esperado": "negativo",
        "por_que": "É a frase 2 sem “How wonderful,”. Sem o marcador irônico o VADER lê "
                   "negativo: era essa palavra positiva que invertia o resultado.",
    },
    {
        "controle": "C",
        "idioma": "en",
        "texto": "It was with a lot of pain, sweat and tears that I finally won the "
                 "much-dreamed-of approval in the civil service exam!",
        "esperado": "positivo",
        "por_que": "É a frase 3 com “won” (+2,7) no lugar de “achieved” (sem valor no "
                   "léxico). Uma única palavra a mais inverte o resultado.",
    },
    {
        "controle": "D",
        "idioma": "en",
        "texto": "Today I got laid off and I cannot afford the rent at the end of the month.",
        "esperado": "negativo",
        "por_que": "É a frase 1 com outro vocabulário. “Laid off” e “cannot afford” não "
                   "estão no léxico: a mesma situação recebe escore zero.",
    },
]

# Exemplos prontos para o campo de frase livre da página.
EXEMPLOS_LIVRES = [
    {"rotulo": "Neutra em português com “no” (falso cognato)",
     "texto": "O relógio está no meio da sala.", "idioma": "pt"},
    {"rotulo": "Alegre em português (o VADER não reconhece)",
     "texto": "Estou muito feliz hoje!", "idioma": "pt"},
    {"rotulo": "Sarcasmo em inglês",
     "texto": "Oh great, another Monday morning meeting.", "idioma": "en"},
    {"rotulo": "Negação em inglês (o VADER trata)",
     "texto": "I am not happy with this service.", "idioma": "en"},
    {"rotulo": "Positiva literal em inglês",
     "texto": "I love this phone, best purchase ever!", "idioma": "en"},
]
