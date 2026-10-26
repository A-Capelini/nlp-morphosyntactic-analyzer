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
│   ├── 3_🎭_Analise_Pragmatica.py      # Tarefa 04 — Pragmática — usa sentiment_engine/
│   └── 4_🤖_Assistente_Intencoes.py    # Assistentes Virtuais — classificação de intenções (NLU) — usa intent_engine/
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
├── intent_engine/                      # Motor do Assistente de Intenções (independente dos demais; sem Streamlit)
│   ├── preprocess.py                   # Limpeza do texto (a mesma função no treino e na entrada do usuário)
│   ├── model.py                        # TF-IDF + Regressão Logística, limiar de confiança e prever()
│   ├── responses.py                    # Nomes de exibição, respostas simuladas e mensagem "não entendi"
│   └── evaluate.py                     # Avaliação no split de teste e frases próprias
├── data/intent_assistant/
│   └── massive_ptbr_subset.csv         # Recorte do MASSIVE pt-BR (versionado; o app não baixa nada)
├── scripts/
│   ├── prepare_intent_dataset.py       # Gera o CSV a partir do dataset baixado (uso único)
│   └── testar_intencoes.py             # Teste no terminal: F1 na validação e frases dentro/fora do escopo
├── docs/intent_assistant/
│   └── PROGRESSO.md                    # Registro de andamento do trabalho do assistente
├── requirements.txt                    # Dependências do deploy (Streamlit Community Cloud)
├── style.css                           # Identidade visual única do app (todas as páginas)
└── .streamlit/config.toml              # Tema fixo (claro), versionado no git
```

Cada novo trabalho do semestre entra como um novo arquivo em `pages/` (ex.: `pages/5_🔤_Novo_Trabalho.py`) com seu próprio módulo de motor (ex.: `novo_engine/`), sem alterar os arquivos dos trabalhos anteriores. A página inicial (`app.py`) só precisa ganhar um novo card/`st.page_link` apontando para ela.

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

## 🤖 Assistentes Virtuais Inteligentes — Assistente de Intenções (NLU)

Aplicação prática da apresentação **"Assistentes Virtuais Inteligentes"**, ligada aos slides sobre NLU (slide 3), a evolução de regras para aprendizado de máquina (slides 4-5) e os casos de atendimento ao cliente e casa inteligente (slide 10).

O usuário digita uma frase em português (ex.: *"acorde-me às sete da manhã"*) e o app mostra o **domínio previsto** (Alarmes), a **confiança** do modelo e uma **resposta simulada**. Quando a confiança fica abaixo do limiar (0,35), o assistente responde **"não entendi"**. O assistente **não gera texto, não executa nada de verdade e não é IA agêntica**: cada domínio tem uma resposta fixa, só para demonstrar o que viria depois da etapa de NLU.

### Como funciona

1. **Pré-processamento** (`preprocess.py`): normalização Unicode, minúsculas, remoção de acentos e pontuação, "e-mail" unificado em "email" e stopwords próprias.
2. **Vetorização:** TF-IDF com unigramas e bigramas.
3. **Classificação:** Regressão Logística, que devolve uma probabilidade para cada um dos 9 domínios.
4. **Decisão:** se a maior probabilidade (a *confiança*) é ≥ 0,35, o assistente responde com o domínio previsto; senão, diz "não entendi".

### Dataset

* **MASSIVE pt-BR** (Hugging Face: `Magurofg/massive-pt-br`), licença **CC BY 4.0** — localização para português do Brasil do MASSIVE (Amazon), um benchmark multilíngue de compreensão de linguagem natural para assistentes virtuais.
* **Tarefa:** classificar por **domínio** (coluna `scenario`), não pelas 60 intenções. Foram escolhidos **9 domínios**: alarmes, clima, reprodução de música e mídia, casa inteligente, calendário, listas, data e hora, notícias e e-mail/contatos.
* **Recorte versionado:** `data/intent_assistant/massive_ptbr_subset.csv` (9.440 linhas, colunas `texto`, `dominio` e `split`). Divisão pelos splits do próprio dataset: **treino 6.571 / validação 1.115 / teste 1.754** frases, depois de remover duplicatas no treino e frases de validação/teste idênticas às do treino.
* **O app não baixa nada em execução:** o dataset foi baixado uma vez e recortado por `scripts/prepare_intent_dataset.py`; o CSV resultante fica no repositório.

### Arquitetura (`intent_engine/`)

* **`preprocess.py`:** função `preprocessar()`, a **mesma** no treino e na frase digitada. As stopwords são uma lista própria e curta (sem baixar dados do NLTK, que falha no Streamlit Cloud), mantendo palavras que carregam intenção ("hoje", "amanhã", "não", "para"...). As palavras de ativação do dataset (*olly*, *alexa*, *siri*, *ei*, *hei*) também viram stopwords, para o modelo não usar "alexa" como atalho para casa inteligente.
* **`model.py`:** `treinar()` ajusta o modelo só com o treino (a validação serve para estudar o limiar); `prever(texto)` devolve `dominio`, `confianca`, `top3` e `entendeu`. Sem Streamlit.
* **`responses.py`:** nome de exibição e resposta simulada de cada domínio, e a mensagem de "não entendi".
* **`evaluate.py`:** o **único** lugar que lê o split de teste. Calcula acurácia, F1 macro, relatório por classe, matriz de confusão, erros mais comuns e roda 18 frases próprias (12 dentro do escopo e 6 fora). A página só exibe os resultados.

### A página `4_🤖_Assistente_Intencoes.py`

* **Aba "Assistente":** campo de texto, 6 exemplos clicáveis (um deles fora do escopo), histórico da conversa em `st.session_state` (o mais recente no topo), domínio previsto com nome de exibição, barra de confiança, resposta simulada, top-3 e o aviso de "não entendi".
* **Aba "Sobre o modelo":** métricas no conjunto de teste, interpretação em texto curto, tabela por classe, matriz de confusão, erros mais comuns, erros de maior confiança e as frases próprias.
* **Barra lateral:** domínios, dataset, licença, limiar em uso e as limitações.
* **Cache:** o modelo é treinado uma vez por servidor com `st.cache_resource`, e a avaliação roda uma vez com `st.cache_data`.

### Resultados (conjunto de teste, limiar 0,35)

| Métrica | Valor |
|---|---|
| Acurácia | 93,7% (110 erros em 1.754 frases) |
| F1 macro | 0,929 |
| Cobertura (frases com confiança ≥ 0,35) | 91,7% |
| Precisão nas frases aceitas | 96,6% |

| Domínio | F1 | | Domínio | F1 |
|---|---|---|---|---|
| E-mail e contatos | 0,974 | | Clima | 0,935 |
| Reprodução de música e mídia | 0,958 | | Calendário | 0,923 |
| Alarmes | 0,957 | | Listas | 0,915 |
| Casa inteligente | 0,949 | | Notícias | 0,904 |
| | | | Data e hora | 0,842 |

* **Principal confusão:** Calendário × Data e hora (15 frases de calendário previstas como data e hora e 7 no sentido contrário), esperada porque as frases são parecidas ("me diz as horas dos eventos", "hoje é dia de São João"). Data e hora também é a menor classe do treino (4,8%).
* **Validação × teste:** acurácia 0,934 → 0,937 e F1 macro 0,927 → 0,929, sem sinal de sobreajuste.
* **18 frases próprias:** 18 de 18 corretas (12 dentro do escopo com confiança mínima de 0,58 e 6 fora do escopo no "não entendi"). Esse resultado **não mede generalização**: o limiar 0,35 foi ajustado olhando uma dessas frases ("qual é a raiz quadrada de 144?", confiança 0,34). A medida honesta é o conjunto de teste.

### Decisões técnicas

* **Classificação por domínio** (9 classes) em vez das 60 intenções: tarefa mais simples, fácil de demonstrar e de explicar.
* **TF-IDF + Regressão Logística** com `class_weight='balanced'` e `random_state=42`: modelo leve, interpretável, sem GPU e sem deep learning. O `balanced` compensa classes pequenas (data e hora) e grandes (calendário).
* **Limiar de confiança 0,35**, escolhido com validação e frases próprias, nunca com o teste. O limiar automático da validação (0,25) deixava passar frases fora do escopo, e 0,30 ainda aceitava "qual é a raiz quadrada de 144?". Custo do 0,35: menos cobertura (na validação, 93,4% → 91,0%).
* **E-mail mantido:** F1 de 0,950 na validação, muito acima do limite de 0,80 definido como regra de saída.
* **Divisão dos dados respeitada:** treino ajusta, validação orienta o limiar e o **teste é usado uma única vez**, para medir.
* **Motor separado da interface:** nenhuma lógica de PLN dentro da página Streamlit, no mesmo padrão dos outros trabalhos.

### Limitações

* A localização para pt-BR foi feita por um **LLM**, é **parcial** (cerca de 40% das frases são idênticas ao português de Portugal) e ainda tem **resíduos de português europeu**, erros pontuais de tradução e frases truncadas. Não é tradução humana.
* O corpus tem muitas frases parecidas entre si (só as idênticas foram removidas), então o desempenho em frases realmente novas pode ser menor que o medido no teste.
* O modelo só conhece **9 domínios**; o "não entendi" depende de um limiar e não é perfeito para qualquer frase fora do escopo (testado com apenas 6 frases fora do escopo).
* Não há contexto de conversa, geração de texto nem execução de ações: é apenas a etapa de NLU.

### Reproduzir o recorte e testar no terminal

```bash
# 1) Baixe o dataset Magurofg/massive-pt-br (Hugging Face) para ~/dados/massive-pt-br
#    (train.jsonl, validation.jsonl e test.jsonl) e gere o CSV recortado:
python scripts/prepare_intent_dataset.py

# 2) F1 por classe na validação e teste com frases dentro e fora do escopo:
python scripts/testar_intencoes.py
```

O app em si **não precisa** do dataset original: ele usa apenas o CSV já versionado em `data/intent_assistant/`.

### Dataset, licença e citação

O dataset **massive-pt-br** é distribuído sob a licença **[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Aqui ele foi **modificado**: filtrado para 9 domínios, normalizado em Unicode e sem frases duplicadas ou repetidas entre treino e validação/teste.

FITZGERALD, Jack et al. MASSIVE: a 1M-example multilingual natural language understanding dataset with 51 typologically-diverse languages. In: ANNUAL MEETING OF THE ASSOCIATION FOR COMPUTATIONAL LINGUISTICS, 61., 2023. **Proceedings** [...]. Volume 1: Long Papers. ACL, 2023. arXiv:2204.08582.

MAGUROFG. **massive-pt-br**: localização brasileira do MASSIVE. Hugging Face, [s.d.]. Disponível em: https://huggingface.co/datasets/Magurofg/massive-pt-br. Licença CC BY 4.0. Acesso em: 25 out. 2026.

## 🚀 Como Executar Localmente

**1. Clone o repositório:**
```bash
git clone https://github.com/A-Capelini/nlp-morphosyntactic-analyzer.git
cd nlp-morphosyntactic-analyzer
```

**2. Crie e ative um ambiente virtual (recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

> Quem usa **conda** pode criar o ambiente com o conda e instalar primeiro pelo `conda-forge` (`conda install -c conda-forge streamlit nltk scikit-learn pandas unidecode`), recorrendo ao `pip` só para o que não existir lá (ex.: `svgling`, se for o caso).

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Rode a aplicação:**
```bash
streamlit run app.py
```

A aplicação abre automaticamente em `http://localhost:8501`, com a página inicial listando os trabalhos disponíveis no menu lateral.