# PROGRESSO — Assistente de Intenções
Atualizado: 26/10/2026, 22h (código congelado; falta só ensaio e conferências)

## O que foi feito
- **Etapa 3:** página `pages/4_🤖_Assistente_Intencoes.py`. Duas abas: "Assistente" (formulário, 6 exemplos clicáveis, histórico em `st.session_state`, domínio previsto com nome de exibição, barra de confiança, resposta simulada, "não entendi" abaixo do limiar, top-3, interruptor "Comparar com as regras") e "Sobre o modelo". Barra lateral com domínios, dataset, CC BY 4.0, limiar e limitações. Modelo em `st.cache_resource`; avaliação em `st.cache_data`. Card do assistente no `app.py`. Conferido local e no link público.
- **Etapa 4:** `intent_engine/evaluate.py` avalia no split de TESTE (usado só aqui).
  - Teste (1.754 frases, limiar 0,35): acurácia 0,937 (110 erros), F1 macro 0,929, cobertura 91,7%, precisão nas aceitas 96,6%.
  - F1 por classe: datetime 0,842; news 0,904; lists 0,915; calendar 0,923; weather 0,935; iot 0,949; alarm 0,957; play 0,958; email 0,974.
  - Erros mais comuns: calendar→datetime 15, datetime→calendar 7, iot→play 6, alarm→calendar 6, lists→play 5, calendar→news 5, lists→calendar 5. Os erros de maior confiança são em boa parte rótulos ambíguos (ex.: "lista de rock" play→lists, 0,99).
  - 18 frases próprias: 18/18. Não mede generalização: o limiar 0,35 foi escolhido olhando uma delas ("raiz quadrada de 144", 0,34).
  - Validação x teste coerentes (acurácia 0,934 → 0,937; F1 macro 0,927 → 0,929): sem sinal de sobreajuste.
- **Etapa 5:** `requirements.txt`, README completo e `setup/environment.yml` (validado em ambiente descartável). Deploy conferido: log do Cloud com instalação pelo `requirements.txt` (Python 3.14.9). Link público conferido com a versão final (26/10, 21h43): aba "Sobre o modelo" com números em vírgula e aba "Assistente" com o interruptor das regras.
- **Baseline por regras (26/10):**
  - `intent_engine/rules_baseline.py`: radicais por domínio, vence o domínio com mais palavras casadas, sem palavra-chave não responde; empate decidido pela ordem da lista. Escrito sem consultar o teste e sem otimização.
  - `evaluate.py`: `avaliar_baseline(split)`, que aceita "validation" ou "test".
  - Página 4: interruptor "Comparar com as regras (estilo ELIZA)", seção "Regras × modelo", tabela "Por que o limiar é 0,35?" (validação), vírgula decimal e barra de confiança mais estreita.
  - Teste: regras com acurácia 73,9%, F1 macro 0,811, cobertura 79,6%, precisão nas respondidas 92,9%. Validação: 72,6%, 0,802, 78,1%, 92,9% (quase igual ao teste, sem ajuste). Modelo sem limiar: 93,7% / 0,929 / 100% / 93,7%. Modelo com limiar 0,35: acurácia 88,6% (acertos ÷ todas as frases), cobertura 91,7%, precisão 96,6%.
  - Leitura: as regras são precisas quando respondem, mas ficam mudas em cerca de 20% das frases (Clima: recall 0,455 na validação); o modelo com limiar responde a mais frases e acerta mais delas. A acurácia do modelo com limiar é menor que a sem limiar porque "não entendi" conta como erro.
  - Contraste conferido (modelo × regras): "vai esfriar de madrugada?" Clima 0,95 × não entendi; "vou precisar de casaco amanhã?" Clima 0,82 × não entendi; "deixa o quarto mais claro" Casa inteligente 0,73 × não entendi; "tenho dentista na terça?" Calendário 0,64 × não entendi. Ficam abaixo do limiar nos dois: "me tira da cama às cinco" 0,19, "bota um sambinha aí" 0,21, "põe aquele som que eu gosto" 0,34.
- **Etapa 6:** `docs/intent_assistant/ROTEIRO_APRESENTACAO.md` atualizado (bloco de ~6 min, depois do slide 10 e antes do slide 11; contraste regras × modelo; 17 perguntas prováveis; plano B; números; referências ABNT).
- **Git:** tudo na `main` e enviado, conforme conferido até 07614f8 e f6dcb86 (README e progresso). O commit do roteiro atualizado precisa ser conferido com `git status -sb`. O commit 4dfa431 "Added Dev Container Folder" veio do GitHub. O trabalho roda também no notebook (clonado via SSH, `git pull` antes de trabalhar).

## Arquivos criados ou alterados (caminhos)
Todos dentro do repositório `nlp-morphosyntactic-analyzer/`:
- `intent_engine/evaluate.py`, `intent_engine/rules_baseline.py` (novo), `intent_engine/model.py`
- `pages/4_🤖_Assistente_Intencoes.py`
- `app.py` (alterado com autorização: card 4, "quatro projetos", `intent_engine` no rodapé)
- `requirements.txt`, `setup/environment.yml`, `README.md`
- `docs/intent_assistant/PROGRESSO.md` e `docs/intent_assistant/ROTEIRO_APRESENTACAO.md`
- `.devcontainer/devcontainer.json` (criado pelo GitHub, não por nós)
- Nenhum arquivo dos outros trabalhos foi alterado.

## Decisões e motivos
- Métricas no motor (`evaluate.py`); a página só exibe. Matriz de confusão como tabela pandas. Formulário em vez de `st.chat_input`.
- O teste foi usado uma única vez para o modelo e uma única vez para as regras, sem ajustar nada com ele.
- **Limiar 0,35:** rejeita "raiz quadrada de 144" (0,34) e não afeta as 12 frases válidas. Custo: cobertura na validação 93,4% → 91,0%. Escolhido com validação + frases próprias, nunca com o teste. Base de apenas 6 frases fora do escopo: ajuste fino, não prova.
- **`environment.yml` em `setup/`, não na raiz:** o Streamlit Cloud dá prioridade ao `environment.yml` sobre o `requirements.txt`; em `setup/` ele não é detectado.
- **`.yml`:** conda-forge e defaults; `python=3.10`; só o `svgling` entra por `pip:` (não existe no conda-forge nem no defaults).
- **Baseline por regras:** dá número ao argumento "regras (slide 4) → aprendizado (slide 5)". Aditivo: não muda o modelo nem as métricas dele. As regras **não foram ajustadas** depois de medidas: mexer agora mudaria README, roteiro e este arquivo.
- **Código congelado** desde a noite de 26/10. Só correções de bug, se aparecer algum.
- Desvio do plano (resolvido): houve `git push` antes da Etapa 5; o `requirements.txt` foi antecipado.

## Como rodar / comandos
git pull                                        # sempre ao sentar em um dos computadores
conda activate nlp-analyzer
streamlit run app.py
python scripts/testar_intencoes.py
Link público: https://nlp-morphosyntactic-analyzer.streamlit.app (página 🤖)
Plano B local: notebook, `git pull` e `streamlit run app.py` (a página 🤖 não precisa de internet).

## Pendências
- Conferir com `git status -sb` que o roteiro atualizado foi commitado e enviado.
- Substituir o `PROGRESSO.md` dos arquivos do Project no claude.ai por este.
- Decidir se o `.devcontainer/` fica (o Cloud não o usa).
- Manter `requirements.txt` e `setup/environment.yml` em sincronia, se algo mudar.
- **27/10, 16h às 18h (sem código novo):** `git pull` nos dois computadores; ensaio da seção 5 do roteiro; capturas de tela de reserva (seção 6); duas rodadas cronometradas do bloco; plano B local no notebook com o Wi-Fi desligado; abrir o link antes de sair, para acordar o app.
- **Na apresentação (27/10, 19h):** começar com o interruptor "Comparar com as regras" desligado e o histórico limpo; ligar o interruptor só no bloco de contraste (3.5 do roteiro).

## Próxima etapa
- Não há etapa de código pendente. A próxima conversa só é necessária se algo falhar no ensaio. Nesse caso, abrir com: "Conversa D (Etapa 6). Leia o PLANO_PROJETO.md e o PROGRESSO.md."