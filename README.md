# NLP Morphosyntactic Analyzer

Aplicação interativa desenvolvida em Python para análise de Processamento de Linguagem Natural (PLN). O projeto realiza a normalização, análise morfológica (POS Tagging) e o parsing sintático estrutural de um corpus fechado, comparando visualmente as abordagens **Top-Down** e **Bottom-Up**.

Projeto acadêmico estruturado para consolidar fundamentos de algoritmos de parsing em pipelines de Engenharia de Dados.

🔗 **Acesse a aplicação online:** [nlp-morphosyntactic-analyzer.streamlit.app](https://nlp-morphosyntactic-analyzer.streamlit.app/)

## 🎯 Escopo do Corpus

O motor de análise foi ajustado com uma Gramática Livre de Contexto (CFG) customizada para processar rigorosamente as seguintes sentenças:
1. *The White dog died Yesterday*
2. *The coffee spilled on the floor*
3. *The blue car crashed last week*

## ⚙️ Arquitetura e Decisões Técnicas

* **Módulo Morfológico (`morphology.py`):** Normaliza a capitalização das frases antes do processamento, evitando que o `averaged_perceptron_tagger` do NLTK classifique adjetivos e advérbios como substantivos próprios de forma errônea.
* **Módulo Sintático (`parsers.py`):** Implementa os dois algoritmos clássicos de validação gramatical. A árvore sintática evita o *Shift-Reduce Conflict* adequando a precedência dos adjuntos adverbiais (ADVP).
* **Renderização Vetorial (`tree_renderer.py`):** Substitui a dependência gráfica do `Tkinter` (incompatível com ambientes de deploy *headless*) pela biblioteca `svgling`, gerando SVGs nativos para a interface, com fonte ampliada (22px) para melhor legibilidade.
* **Design Universal (`style.css` + `.streamlit/config.toml`):** Camada de apresentação focada em acessibilidade, alto contraste e tipografia limpa. O tema claro é fixado via `config.toml` para garantir que a paleta de cores renderize sempre como planejado, independente do tema do dispositivo de quem acessa. Cada método de parsing recebe uma cor de destaque própria (azul para Top-Down, âmbar para Bottom-Up) — combinação escolhida por ter bom contraste e ser segura para daltonismo.
* **Cache de Execução (`app.py`):** Os resultados de parsing são cacheados com `st.cache_data`, já que o corpus é fechado (3 frases fixas), evitando reprocessar a mesma frase repetidamente.
* **Interface Didática (`app.py`):** Além das árvores, a tela traz uma explicação de cada método (o que é, pra que serve, como funciona) e uma legenda das siglas do log de trace do NLTK (`E`/`M`/`+` no Top-Down, `S`/`R` no Bottom-Up), pensada para quem está vendo os algoritmos pela primeira vez.

## 🧠 Teoria dos Algoritmos de Parsing

### 1. Top-Down (Recursive Descent)
Inicia a análise pelo nó raiz (`S` - Sentença) e tenta expandir as regras gramaticais de forma recursiva até chegar às palavras folha (terminais). 
* **Característica:** Exaustivo. Busca todas as derivações possíveis.
* **Limitação:** Pode entrar em loop infinito se a gramática contiver regras recursivas à esquerda.

### 2. Bottom-Up (Shift-Reduce)
Faz o caminho inverso. Começa pelas palavras da frase (folhas) e tenta agrupá-las e reduzi-las às categorias gramaticais superiores (nós pais), até consolidar toda a estrutura no nó raiz (`S`).
* **Característica:** Ganancioso (*greedy*).
* **Limitação:** Não possui *backtracking*. Se tomar uma decisão de redução precipitada por ambiguidades estruturais, o algoritmo falha silenciosamente.

> Essas mesmas explicações, de forma resumida, também aparecem diretamente na interface, ao lado de cada árvore gerada.

## 🚀 Como Executar Localmente

**1. Clone o repositório:**
```bash
git clone https://github.com/SEU_USUARIO/nlp-morphosyntactic-analyzer.git
cd nlp-morphosyntactic-analyzer
```

**2. Crie e ative um ambiente virtual (recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Rode a aplicação:**
```bash
streamlit run app.py
```

A aplicação abre automaticamente em `http://localhost:8501`.
