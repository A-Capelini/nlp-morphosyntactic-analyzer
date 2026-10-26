# PROGRESSO — Assistente de Intenções
Atualizado: 25/10/2026, 22h50 (fim da Conversa B, Etapas 3 e 4, com a Etapa 5 antecipada)

## O que foi feito
- **Etapa 3:** página `pages/4_🤖_Assistente_Intencoes.py`. Duas abas: "Assistente" (formulário, 6 exemplos clicáveis, histórico em `st.session_state`, domínio previsto com nome de exibição, barra de confiança, resposta simulada, "não entendi" abaixo do limiar, top-3) e "Sobre o modelo". Barra lateral com domínios, dataset, CC BY 4.0, limiar e limitações. Modelo em `st.cache_resource`; avaliação em `st.cache_data`. Card do assistente no `app.py`. Conferido no navegador local.
- **Etapa 4:** `intent_engine/evaluate.py` avalia no split de TESTE (usado só aqui).
  - Teste (1.754 frases, limiar 0,35): acurácia 0,937 (110 erros), F1 macro 0,929, cobertura 91,7%, precisão nas aceitas 96,6%.
  - F1 por classe: datetime 0,842; news 0,904; lists 0,915; calendar 0,923; weather 0,935; iot 0,949; alarm 0,957; play 0,958; email 0,974.
  - Erros mais comuns: calendar→datetime 15, datetime→calendar 7, iot→play 6, alarm→calendar 6, lists→play 5, calendar→news 5, lists→calendar 5. Os erros de maior confiança são em boa parte rótulos ambíguos do dataset (ex.: "lista de rock" play→lists, 0,99).
  - 18 frases próprias: 18/18 (12/12 válidas, menor confiança 0,58; 6/6 fora do escopo no "não entendi"). Não mede generalização: o limiar 0,35 foi escolhido olhando uma dessas frases ("raiz quadrada de 144", 0,34).
  - Validação x teste coerentes (acurácia 0,934 → 0,937; F1 macro 0,927 → 0,929): sem sinal de sobreajuste.
- **Etapa 5 (antecipada):**
  - `requirements.txt` atualizado (+ scikit-learn, pandas, unidecode).
  - README completo: árvore com a página 4, `intent_engine/`, `data/`, `scripts/`, `docs/`, `setup/`; seção do assistente (fluxo, dataset, arquitetura, resultados, decisões, limitações, CC BY 4.0, citações ABNT); "Como Executar" com conda-forge/conda como Opção 1 e venv + pip como Opção 2.
  - `setup/environment.yml` para reproduzir o ambiente local. Validado: criado como `nlp-analyzer-teste`, app rodado e ambiente removido.
  - Deploy: o log do Cloud (26/10, 00h59 UTC) mostra instalação pelo `requirements.txt` com `uv` em Python 3.14.9 e três redeploys sem erro. Link público conferido: a aba "Sobre o modelo" carregou na nuvem.
- **Git:** tudo na `main` e enviado (`main` = `origin/main`). Commits: 44043dc (card + requirements), 055273c (limiar 0,35), b69a114 (progresso), 8fd90fe (README), 2755178 (`setup/environment.yml`), c314860 (README conda/venv). O commit 4dfa431 "Added Dev Container Folder" veio do GitHub (adiciona `.devcontainer/devcontainer.json`, 33 linhas); o primeiro push foi recusado por isso e foi resolvido com `git pull --rebase`, sem conflito.

## Arquivos criados ou alterados (caminhos)
Todos dentro de `~/Projetos/nlp-morphosyntactic-analyzer/`:
- `intent_engine/evaluate.py` (novo)
- `pages/4_🤖_Assistente_Intencoes.py` (novo)
- `app.py` (alterado com autorização: card 4, "quatro projetos", `intent_engine` no rodapé)
- `requirements.txt` (alterado: + scikit-learn, pandas, unidecode)
- `intent_engine/model.py` (alterado: LIMIAR_MANUAL 0,30 → 0,35 e comentário)
- `setup/environment.yml` (novo)
- `README.md` (alterado)
- `docs/intent_assistant/PROGRESSO.md` (este arquivo)
- `.devcontainer/devcontainer.json` (criado pelo GitHub, não por nós)
- Nenhum arquivo dos outros trabalhos foi alterado.

## Decisões e motivos
- Métricas no motor (`evaluate.py`); a página só exibe. Matriz de confusão como tabela pandas (sem matplotlib, sem dependência nova). Formulário em vez de `st.chat_input` (o `chat_input` ficaria fixo nas duas abas).
- O teste foi usado uma única vez e não serviu para ajustar nada.
- **Limiar 0,35:** rejeita "raiz quadrada de 144" (0,34) e não afeta as 12 frases válidas (menor confiança 0,58). Custo: cobertura na validação 93,4% → 91,0%. Escolhido com validação + frases próprias, nunca com o teste. Base de apenas 6 frases fora do escopo: ajuste fino, não prova.
- Hipótese confirmada: calendar × datetime é a principal confusão; datetime é a classe mais fraca (menor classe, 4,8% do treino).
- **`environment.yml` em `setup/`, não na raiz:** o Streamlit Community Cloud procura dependências na pasta do `app.py` e na raiz e dá prioridade ao `environment.yml` sobre o `requirements.txt`; em `setup/` ele não é detectado e o deploy segue pelo `requirements.txt`.
- **`.yml`:** canais conda-forge e depois defaults; `python=3.10` (versão local testada); `streamlit`, `nltk`, `scikit-learn`, `pandas`, `unidecode` e `huggingface_hub` pelo conda-forge. O `svgling` é o único em `pip:`, porque `conda search` não o encontrou no conda-forge nem no defaults. O `streamlit` existe no conda-forge (até a 1.66.1). O `huggingface_hub` serve só para baixar o dataset.
- Python local 3.10 e Cloud 3.14: o app roda nas duas versões.
- Desvio do plano: houve `git push` antes da Etapa 5 (o app público redeployou com a página 4); por isso o `requirements.txt` foi antecipado.
- Cosmético (não corrigido): a barra lateral mostra o limiar com ponto ("0.35"); a barra de confiança é larga em monitor grande.

## Como rodar / comandos
conda env create -f setup/environment.yml      # ou usar o ambiente nlp-analyzer existente
conda activate nlp-analyzer
cd ~/Projetos/nlp-morphosyntactic-analyzer
streamlit run app.py
python scripts/testar_intencoes.py
python -c "from intent_engine.evaluate import avaliar_teste; print(avaliar_teste()['acuracia'])"
Link público: https://nlp-morphosyntactic-analyzer.streamlit.app (página 🤖)

## Pendências
- Conferir o log do Cloud depois do push c314860 (linha de dependências instaladas pelo `requirements.txt`) e abrir a página 🤖 no link público, incluindo a aba "Assistente" (só a aba "Sobre o modelo" foi vista lá).
- Conferir que o README renderiza a árvore e as tabelas no GitHub.
- Olhar o `.devcontainer/devcontainer.json` e decidir se fica (o Cloud não o usa).
- Manter `requirements.txt` e `setup/environment.yml` em sincronia ao mudar dependências.
- Confirmar o que será entregue às 18h de segunda e onde.
- Etapa 6: roteiro de 5 a 7 min (slides 3, 4-5 e 10), 6 a 8 frases de demonstração, perguntas prováveis, plano B offline (capturas/vídeo), referências ABNT. Abrir o link minutos antes para acordar o app.

## Próxima etapa
- **Conversa D (Etapa 6):** apresentação e demonstração. A Etapa 5 está praticamente fechada; falta só a conferência do deploy acima.
- Abrir com: "Conversa D (Etapa 6). Leia o PLANO_PROJETO.md e o PROGRESSO.md."