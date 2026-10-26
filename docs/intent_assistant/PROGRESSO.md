# PROGRESSO — Assistente de Intenções
Atualizado: 25/10/2026, 21h50 (fim da Conversa B, Etapas 3 e 4)

## O que foi feito
- **Etapa 3:** página `pages/4_🤖_Assistente_Intencoes.py` criada. Duas abas: "Assistente" (formulário, 6 exemplos clicáveis, histórico em `st.session_state`, domínio previsto com nome de exibição, barra de confiança, resposta simulada, "não entendi" abaixo do limiar, top-3) e "Sobre o modelo". Barra lateral com domínios, dataset, CC BY 4.0, limiar e limitações. Modelo em `st.cache_resource`; avaliação em `st.cache_data`. Card do assistente adicionado ao `app.py` (conferido no navegador local: card e item no menu lateral aparecem).
- **Etapa 4:** `intent_engine/evaluate.py` avalia no split de TESTE (usado só aqui).
  - Teste (1.754 frases): acurácia 0,937 (110 erros), F1 macro 0,929. Esses dois números não dependem do limiar.
  - Com o limiar 0,30 (medido antes da troca): cobertura 94,3% e precisão nas aceitas 96,1%. Com o limiar 0,35 estes dois valores mudam e aparecem na aba "Sobre o modelo" (não foram registrados aqui).
  - F1 por classe: datetime 0,842; news 0,904; lists 0,915; calendar 0,923; weather 0,935; iot 0,949; alarm 0,957; play 0,958; email 0,974.
  - Erros mais comuns: calendar→datetime 15, datetime→calendar 7, iot→play 6, alarm→calendar 6, lists→play 5, calendar→news 5, lists→calendar 5.
  - 18 frases próprias (medidas com limiar 0,30): 17 corretas (12/12 válidas, menor confiança 0,58; 5 de 6 fora do escopo rejeitadas). Falha: "qual é a raiz quadrada de 144?" → clima, 0,34.
- Validação x teste coerentes (acurácia 0,934 → 0,937; F1 macro 0,927 → 0,929): sem sinal de sobreajuste.
- **Limiar trocado para 0,35** em `model.py`. Teste de terminal (`scripts/testar_intencoes.py`) após a troca: as 5 frases fora do escopo caem no "não entendi" (confianças de 0,19 a 0,27) e não apareceu nenhum ERRO nas linhas conferidas.
- `requirements.txt` atualizado (Etapa 5 antecipada) e push feito (commit 44043dc).

## Arquivos criados ou alterados (caminhos)
Todos dentro de `~/Projetos/nlp-morphosyntactic-analyzer/`:
- `intent_engine/evaluate.py` (novo)
- `pages/4_🤖_Assistente_Intencoes.py` (novo)
- `app.py` (alterado com autorização: card 4, "quatro projetos", `intent_engine` no rodapé)
- `requirements.txt` (alterado: + scikit-learn, pandas, unidecode)
- `intent_engine/model.py` (alterado: LIMIAR_MANUAL 0,30 → 0,35 e comentário)
- `docs/intent_assistant/PROGRESSO.md` (este arquivo)
- Nenhum arquivo dos outros trabalhos foi alterado.

## Decisões e motivos
- Métricas no motor (`evaluate.py`); a página só exibe. Matriz de confusão como tabela pandas (sem matplotlib, sem dependência nova).
- Formulário em vez de `st.chat_input`, porque o `chat_input` fica fixo no rodapé e apareceria nas duas abas.
- O teste foi usado uma única vez e não serviu para ajustar nada.
- **Limiar 0,35:** rejeita "qual é a raiz quadrada de 144?" (0,34) e não afeta as 12 frases válidas (menor confiança 0,58; "acorde-me às sete da manhã" tem 0,47). Custo: cobertura na validação 93,4% → 91,0%. Escolhido com validação + frases próprias, nunca com o teste. Base de apenas 6 frases fora do escopo: ajuste fino, não prova.
- Hipótese confirmada: calendar × datetime é a principal confusão; datetime é a classe mais fraca (menor classe, 4,8% do treino).
- Desvio do plano: houve `git push` antes da Etapa 5 (o app público redeploya com a página 4); por isso o `requirements.txt` foi antecipado.

## Como rodar / comandos
conda activate nlp-analyzer
cd ~/Projetos/nlp-morphosyntactic-analyzer
streamlit run app.py
python scripts/testar_intencoes.py
python -c "from intent_engine.evaluate import avaliar_teste; print(avaliar_teste()['acuracia'])"

## Pendências
- Conferir a página 4 no navegador local (6 exemplos, histórico, "Limpar histórico", aba "Sobre o modelo"). Ainda não conferido.
- Conferir o link público (a página 4 carrega após o redeploy; se falhar, ver o log em "Manage app"). Ainda não conferido.
- Anotar cobertura e precisão do teste com o limiar 0,35 (aparecem na aba "Sobre o modelo") e conferir a frase "raiz quadrada" no "não entendi".
- Etapa 5: README (descrição, como rodar, CC BY 4.0, citação do MASSIVE e do massive-pt-br; árvore com a página 4 e o `intent_engine/`), conferir que nada baixa em execução.
- Confirmar o que será entregue às 18h de segunda e onde.
- Etapa 6: roteiro, frases de demonstração, perguntas prováveis, plano B offline, referências ABNT.

## Próxima etapa
- **Conversa C (Etapa 5):** README, conferência do deploy e do link público.
- Abrir com: "Conversa C (Etapa 5). Leia o PLANO_PROJETO.md e o PROGRESSO.md."