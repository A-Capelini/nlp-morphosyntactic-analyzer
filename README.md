# NLP Morphosyntactic Analyzer

Aplicação interativa em Python para a disciplina de Processamento de Linguagem Natural (PLN) — FATEC Cotia. Estruturada como um **app multipágina**: cada trabalho do semestre vive em sua própria página dentro de `pages/`, com seus próprios módulos de análise — sem compartilhar código entre trabalhos.

🔗 **Acesse a aplicação online:** [nlp-morphosyntactic-analyzer.streamlit.app](https://nlp-morphosyntactic-analyzer.streamlit.app/)

## 🗂️ Estrutura do projeto

```
.
├── app.py                              # Página inicial (navegação entre trabalhos)
├── pages/
│   ├── 1_📚_Parsing_Sintatico.py       # Tarefa 03 — usa nlp_engine/
│   ├── 2_🧠_Dependencia_Conceitual.py  # Tarefa 1 e 2 — usa cd_engine/
│   └── 3_🎭_Analise_Pragmatica.py      # Tarefa 04 — Pragmática — usa sentiment_engine/
├── nlp_engine/                         # Motor da Tarefa 03 (fechado, não é tocado pelos próximos trabalhos)
│   ├── grammar_rules.py
│   ├── morphology.py
│   ├── parsers.py
│   └── tree_renderer.py
├── cd_engine/                          # Motor da Tarefa 1/2 (independente de nlp_engine)
│   ├── frames.py                       # Estrutura de dados do frame CD
│   ├── lexicon.py                      # Léxico semântico + tokenização
│   └── parser.py                       # parse_sentence(): fases 2–4 da CD
├── sentiment_engine/                   # Motor do exercício de Pragmática (independente dos demais)
│   ├── corpus.py                       # Frases do exercício, frases de controle e exemplos livres
│   └── vader_core.py                   # Carrega o VADER, classifica e lista as palavras reconhecidas
├── style.css                           # Identidade visual única do app (todas as páginas)
└── .streamlit/config.toml              # Tema fixo (claro), versionado no git
```

Cada novo trabalho do semestre entra como um novo arquivo em `pages/` (ex.: `pages/4_🔤_Novo_Trabalho.py`) com seu próprio módulo de motor (ex.: `novo_engine/`), sem alterar os arquivos dos trabalhos anteriores. A página inicial (`app.py`) só precisa ganhar um novo card/`st.page_link` apontando para ela.

## 📚 Tarefa 03 — Parsing Sintático (Top-Down vs Bottom-Up)

Realiza a normalização, análise morfológica (POS Tagging) e o parsing sintático estrutural de um corpus fechado, comparando visualmente as abordagens **Top-Down** e **Bottom-Up**.

### Escopo do Corpus

O motor de análise (`nlp_engine/`) foi ajustado com uma Gramática Livre de Contexto (CFG) customizada para processar rigorosamente as seguintes sentenças:
1. *The White dog died Yesterday*
2. *The coffee spilled on the floor*
3. *The blue car crashed last week*

### Arquitetura e Decisões Técnicas

* **Módulo Morfológico (`nlp_engine/morphology.py`):** Normaliza a capitalização das frases antes do processamento, evitando que o `averaged_perceptron_tagger` do NLTK classifique adjetivos e advérbios como substantivos próprios de forma errônea.
* **Módulo Sintático (`nlp_engine/parsers.py`):** Implementa os dois algoritmos clássicos de validação gramatical. A árvore sintática evita o *Shift-Reduce Conflict* adequando a precedência dos adjuntos adverbiais (ADVP).
* **Renderização Vetorial (`nlp_engine/tree_renderer.py`):** Substitui a dependência gráfica do `Tkinter` (incompatível com ambientes de deploy *headless*) pela biblioteca `svgling`, gerando SVGs nativos para a interface, com fonte ampliada (22px) para melhor legibilidade.
* **Cache de Execução:** Os resultados de parsing são cacheados com `st.cache_data`, já que o corpus é fechado (3 frases fixas), evitando reprocessar a mesma frase repetidamente.
* **Interface Didática:** Além das árvores, a tela traz uma explicação de cada método (o que é, pra que serve, como funciona) e uma legenda das siglas do log de trace do NLTK (`E`/`M`/`+` no Top-Down, `S`/`R` no Bottom-Up).

### Teoria dos Algoritmos de Parsing

**Top-Down (Recursive Descent):** inicia a análise pelo nó raiz (`S`) e tenta expandir as regras gramaticais de forma recursiva até chegar às palavras folha. Exaustivo — busca todas as derivações possíveis; pode entrar em loop com recursão à esquerda.

**Bottom-Up (Shift-Reduce):** parte das palavras da frase e agrupa (reduz) tokens em categorias gramaticais cada vez maiores até consolidar a estrutura no nó raiz. Ganancioso (*greedy*) — sem *backtracking*, falha silenciosamente diante de ambiguidades mal resolvidas.

## 🧠 Tarefa 1 e 2 — Dependência Conceitual (CD)

Implementa o método de **Dependência Conceitual** de Roger Schank (1972): converte uma frase em português (ordem Ator-Verbo-Complemento) em um *frame* semântico ATOR → ACT → OBJETO, com resolução de instrumentos e destinos inferidos.

### Arquitetura (`cd_engine/`)

* **`frames.py`:** classe `ConceptualDependencyFrame` — estrutura de dados do frame (ator, ACT, objeto, direção, instrumento), com serialização recursiva em `to_dict()`.
* **`lexicon.py`:** `SEMANTIC_LEXICON` mapeia verbos de superfície para as **9 primitivas ACT** da teoria (`ATRANS`, `PTRANS`, `PROPEL`, `MOVE`, `GRASP`, `INGEST`, `EXPEL`, `MTRANS`, `MBUILD`) — 58 verbos cadastrados ao todo (4 a 11 por primitiva), incluindo o presente de alguns verbos irregulares (`dá`, `vai`, `come`) ao lado do passado. Também define `STOPWORDS` (artigos/preposições) e `tokenize()`/`content_tokens()` (Fase 1).
* **`parser.py`:** `locate_verb()` faz a Fase 2 (busca tolerante do verbo, ignorando artigos/preposições e sem exigir posição fixa); `parse_sentence()` implementa as Fases 3–4 (extração de slots e resolução de inferências) para cada uma das 9 primitivas.

### Tarefa 2 — Demonstração ao vivo

A página `2_🧠_Dependencia_Conceitual.py` permite digitar (ou escolher entre exemplos) uma frase e ver, em tempo real: os tokens da Fase 1 (com e sem artigos/preposições), o ACT mapeado na Fase 2, e o frame final com os slots preenchidos (Fases 3–4) — tanto em uma visualização gráfica quanto em JSON.

Como "o professor escolhe a frase na hora" é parte do enunciado da Tarefa 2, o parser tolera variações razoáveis de fraseado — "Ana deu livro Maria" e "A Ana deu o livro para a Maria" produzem o mesmo frame — em vez de exigir a ordem rígida Ator-Verbo-Complemento sem nada entre os tokens. O que o parser **não** faz é reconhecer verbos fora do léxico ou flexões não cadastradas (ex.: "comia"/"comendo" em vez de "comeu"/"come"): isso é tratado como um erro amigável, com a explicação de que a Dependência Conceitual trabalha com um conjunto fechado de primitivas — uma característica da própria teoria de Schank, não uma limitação deste código.

> Ampliar o vocabulário suportado é só adicionar uma entrada em `cd_engine/lexicon.py` — o parser não precisa ser alterado, desde que o ACT correspondente já tenha um ramo implementado em `parser.py`.

## 🎭 Tarefa 04 — Pragmática — Análise de sentimentos com VADER

Avalia se o **VADER** (analisador de sentimentos baseado em léxico e regras, do NLTK) consegue captar intenção e contexto em quatro frases emocionalmente ambíguas — *triste parecendo triste*, *triste parecendo alegre* (sarcasmo), *exaltação parecendo triste* e *alegre parecendo alegre* — ou se faz apenas uma leitura literal das palavras.

### Arquitetura (`sentiment_engine/`)

* **`corpus.py`:** as 4 frases (original em português + tradução para o inglês + emoção esperada), as frases de controle (testes de sensibilidade A–D) e os exemplos do campo livre. Trocar uma frase aqui atualiza a página inteira.
* **`vader_core.py`:** `carregar_analisador()` baixa o léxico do VADER na primeira execução; `analisar()` devolve um `Resultado` (neg/neu/pos/compound, rótulo, palavras reconhecidas e se o acerto foi acidental). Sem HTML e sem Streamlit.

### A página `3_🎭_Analise_Pragmatica.py`

* Mostra cada frase em **português e inglês lado a lado**, com o escore `compound` numa escala visual, as palavras que o VADER realmente reconheceu e se o resultado coincide com a emoção esperada.
* **Resumo comparativo** das 4 frases e **campo de frase livre** (com exemplos prontos), para testar ao vivo.
* **Testes de sensibilidade** (controles A–D) que explicam *por que* o VADER acertou ou errou, e um resumo da leitura crítica.

### Decisões técnicas

* **Léxico em inglês:** o VADER não tem português. Em português, as únicas palavras reconhecidas são coincidências com o léxico inglês (ex.: “no” = “não” em inglês, “sob” = “soluçar”); por isso a página sinaliza esses casos como **acertos acidentais**.
* **Cache:** o analisador é criado uma vez por servidor com `st.cache_resource`, e o `vader_lexicon` é baixado só se ainda não existir.
* **Segurança:** todo texto digitado pelo usuário passa por `html.escape` antes de entrar no HTML da página.
* **Sem `transformers` no deploy:** modelos como BERT/RoBERTa (a melhoria sugerida na análise crítica) são pesados demais para o Streamlit Community Cloud e não fazem parte do `requirements.txt`.

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

A aplicação abre automaticamente em `http://localhost:8501`, com a página inicial listando os trabalhos disponíveis no menu lateral.
