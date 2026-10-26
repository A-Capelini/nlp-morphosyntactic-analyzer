# PROGRESSO — Assistente de Intenções
Atualizado: 25/10/2026, 20h52 (fim da Conversa A, Etapas 1 e 2)

## O que foi feito
- **Etapa 1:** `scripts/prepare_intent_dataset.py` gerou `data/intent_assistant/massive_ptbr_subset.csv` (9.440 linhas, 494 KB; colunas `texto`, `dominio`, `split`).
  - Linhas lidas: treino 10.948, validação 1.929, teste 2.930. Nos 9 domínios: 6.863 / 1.198 / 1.877.
  - Removidas: 292 duplicatas no treino; 83 frases da validação e 123 do teste iguais às do treino. Nenhuma frase vazia. 1 frase do treino com rótulo conflitante (só contada).
  - Resultado final: treino 6.571, validação 1.115, teste 1.754.
  - Desbalanceamento no treino: calendar 23,4%, play 19,5%, email 14,1%, iot 9,8%, lists 8,0%, weather 7,6%, news 7,1%, alarm 5,6%, datetime 4,8%.
- **Etapa 2:** motor `intent_engine/` pronto e testado no terminal (sem Streamlit).
  - `preprocess.py`: NFKC, minúsculas, sem acentos (unidecode), "e-mail"/"e mail" unificado em "email", pontuação removida, stopwords próprias (inclui olly, alexa, siri, ei, hei).
  - `model.py`: TF-IDF (1-2 gramas) + Regressão Logística (`class_weight='balanced'`, `random_state=42`); `treinar()` usa só treino + validação; `prever(texto)` devolve domínio, confiança, top-3 e `entendeu`.
  - `responses.py`: nomes de exibição, respostas simuladas e mensagem "não entendi".
  - `scripts/testar_intencoes.py`: F1 por classe na validação, regra do e-mail e teste de terminal com 13 frases.
- **Resultados na validação (1.115 frases):** acurácia 0,934; F1 macro 0,927.
  - F1 por classe: news 0,873; datetime 0,881; calendar 0,920; lists 0,927; alarm 0,939; iot 0,944; weather 0,946; email 0,950; play 0,961.
- **Teste de terminal:** 8 de 8 frases válidas corretas (inclui "lê meu último e‑mail" com hífen U+2011 → email 0,84; "alexa, apaga as luzes da sala" → iot; "alexa, que horas são?" → datetime 1,00) e 5 de 5 frases fora do escopo no "não entendi".

## Arquivos criados ou alterados (caminhos)
Todos dentro de `~/Projetos/nlp-morphosyntactic-analyzer/`:
- `scripts/prepare_intent_dataset.py`
- `data/intent_assistant/massive_ptbr_subset.csv`
- `intent_engine/preprocess.py`
- `intent_engine/model.py`
- `intent_engine/responses.py`
- `scripts/testar_intencoes.py` (novo, não previsto no plano)
- `docs/intent_assistant/PROGRESSO.md` (este arquivo)
- Nenhum arquivo dos outros trabalhos do app foi alterado. Commits locais na `main`; nenhum `git push`.

## Decisões e motivos
- **E-mail MANTIDO:** F1 0,950 (2º melhor), muito acima do limite de 0,80. Ele só se confunde pontualmente com calendar, lists, play, news e weather.
- **Limiar de confiança fixado em 0,30** (`LIMIAR_MANUAL` em `model.py`). O limiar automático da validação (0,25, precisão ≥ 95%) deixava passar "como faço um bolo de chocolate?" (0,27 → e-mail). Com 0,30, as 5 frases fora do escopo caem no "não entendi". Na validação: cobertura 93,4%, precisão 96,2%. Base de apenas 5 frases fora do escopo; revalidar na Etapa 4. Próximo valor, se houver falsos aceites: 0,35 (cobertura 91,0%).
- **"acorde-me às sete da manhã" tem só 0,47 de confiança** (efeito do `class_weight='balanced'`). Por isso o limiar não deve passar de 0,50.
- **"e-mail" → "email" antes de remover a pontuação**, senão o "e" vira stopword e sobra "mail".
- **`token_pattern` aceita tokens de 1 caractere** (ex.: "7" em horários).
- **Duplicatas comparadas por texto exato** (não por minúsculas/pontuação); quase-duplicatas ainda podem existir entre treino e validação/teste.
- Stopwords próprias (sem NLTK), por causa do deploy no Streamlit Cloud.
- Ambiente: `unidecode` instalado via conda-forge. `pandas` está no ambiente como pacote do pip (`pypi_0`) e funciona. `scikit-learn` e `matplotlib` instalados via conda-forge nesta conversa.

## Como rodar / comandos
```bash
conda activate nlp-analyzer
cd ~/Projetos/nlp-morphosyntactic-analyzer
python scripts/prepare_intent_dataset.py     # regenera o CSV (reexecutável)
python scripts/testar_intencoes.py           # F1 por classe, regra do e-mail e teste de terminal
python -c "from intent_engine.model import prever; print(prever('vai chover amanhã?'))"
```

## Pendências
- Confirmar o que será entregue às 18h de segunda (link, repositório, relatório, apresentação ao vivo) e onde.
- Conferir em `app.py` como as páginas são registradas (descoberta automática por `pages/` é o esperado) e ver as ~40 primeiras linhas de `pages/2_🧠_Dependencia_Conceitual.py` (padrão de layout e `style.css`) antes da Etapa 3.
- Revalidar o limiar 0,30 na Etapa 4 com 15 a 20 frases próprias (incluindo mais fora do escopo).
- Verificar as confusões de datetime (menor precisão: 0,814) na análise de erros da Etapa 4; a hipótese do plano é calendar × datetime.
- Etapa 5: acrescentar `scikit-learn`, `pandas`, `unidecode` (e `matplotlib`) ao `requirements.txt`. Opcional: reinstalar o `pandas` pelo conda-forge no ambiente local.
- O split de teste (1.754 frases) ainda não foi usado: só na Etapa 4.

## Próxima etapa
- **Conversa B (Etapas 3 e 4), segunda 26/10, 08:00-10:30:** página `pages/4_🤖_Assistente_Intencoes.py` (entrada, domínio previsto com nome de exibição, barra de confiança, resposta simulada, "não entendi", barra lateral com limitações, modelo em `st.cache_resource`) e avaliação no split de teste (acurácia, F1 macro, `classification_report`, matriz de confusão simples, análise de erros, seção "Sobre o modelo").
- Abrir a Conversa B com: "Conversa B (Etapas 3 e 4). Leia o PLANO_PROJETO.md e o PROGRESSO.md." Cole também as ~40 primeiras linhas de `pages/2_🧠_Dependencia_Conceitual.py` e o trecho de `app.py` que registra as páginas.