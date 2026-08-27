# NLP Morphosyntactic Analyzer

Aplicação interativa desenvolvida em Python para análise de Processamento de Linguagem Natural (PLN). O projeto realiza a normalização, análise morfológica (POS Tagging) e o parsing sintático estrutural de um corpus fechado, comparando visualmente as abordagens **Top-Down** e **Bottom-Up**.

Projeto acadêmico estruturado para consolidar fundamentos de algoritmos de parsing em pipelines de Engenharia de Dados.

## 🎯 Escopo do Corpus

O motor de análise foi ajustado com uma Gramática Livre de Contexto (CFG) customizada para processar rigorosamente as seguintes sentenças:
1. *The White dog died Yesterday*
2. *The coffee spilled on the floor*
3. *The blue car crashed last week*

## ⚙️ Arquitetura e Decisões Técnicas

* **Módulo Morfológico (`morphology.py`):** Normaliza a capitalização das frases antes do processamento, evitando que o `averaged_perceptron_tagger` do NLTK classifique adjetivos e advérbios como substantivos próprios de forma errônea.
* **Módulo Sintático (`parsers.py`):** Implementa os dois algoritmos clássicos de validação gramatical. A árvore sintática evita o *Shift-Reduce Conflict* adequando a precedência dos adjuntos adverbiais (ADVP).
* **Renderização Vetorial (`tree_renderer.py`):** Substitui a dependência gráfica do `Tkinter` (incompatível com ambientes de deploy *headless*) pela biblioteca `svgling`, gerando SVGs nativos para a interface.
* **Design Universal (`style.css`):** Camada de apresentação focada em acessibilidade, alto contraste e tipografia limpa.

## 🧠 Teoria dos Algoritmos de Parsing

### 1. Top-Down (Recursive Descent)
Inicia a análise pelo nó raiz (`S` - Sentença) e tenta expandir as regras gramaticais de forma recursiva até chegar às palavras folha (terminais). 
* **Característica:** Exaustivo. Busca todas as derivações possíveis.
* **Limitação:** Pode entrar em loop infinito se a gramática contiver regras recursivas à esquerda.

### 2. Bottom-Up (Shift-Reduce)
Faz o caminho inverso. Começa pelas palavras da frase (folhas) e tenta agrupá-las e reduzi-las às categorias gramaticais superiores (nós pais), até consolidar toda a estrutura no nó raiz (`S`).
* **Característica:** Ganancioso (*greedy*).
* **Limitação:** Não possui *backtracking*. Se tomar uma decisão de redução precipitada por ambiguidades estruturais, o algoritmo falha silenciosamente.

## 🚀 Como Executar Localmente

**1. Clone o repositório:**
```bash
git clone https://github.com/SEU_USUARIO/nlp-morphosyntactic-analyzer.git
cd nlp-morphosyntactic-analyzer