# PROGRESSO — Assistente de Intenções
Atualizado: 25/10/2026, 22h10 (fim da Conversa B, Etapas 3 e 4)

## O que foi feito
- **Etapa 3:** página `pages/4_🤖_Assistente_Intencoes.py`. Duas abas: "Assistente" (formulário, 6 exemplos clicáveis, histórico em `st.session_state`, domínio previsto com nome de exibição, barra de confiança, resposta simulada, "não entendi" abaixo do limiar, top-3) e "Sobre o modelo". Barra lateral com domínios, dataset, CC BY 4.0, limiar e limitações. Modelo em `st.cache_resource`; avaliação em `st.cache_data`. Card do assistente no `app.py`.
- **Etapa 4:** `intent_engine/evaluate.py` avalia no split de TESTE (usado só aqui).
  - Teste (1.754 frases, limiar 0,35): acurácia 0,937 (110 erros); F1 macro 0,929; cobertura 91,7%; precisão nas aceitas 96,6%. (Com limiar 0,30: cobertura 94,3%, precisão 96,1%.)
  - F1 por classe: datetime 0,842; news 0,904; lists 0,915; calendar 0,923; weather 0,935; iot 0,949; alarm 0,957; play 0,958; email 0,974.
  - Erros mais comuns: calendar→datetime 15, datetime→calendar 7, iot→play 6, alarm→calendar 6, lists→play 5, calendar→news 5, lists→calendar 5.
  - Erros de maior confiança (0,99 a 0,76) são em grande parte rótulos ambíguos do dataset (ex.: "lista de rock" play→lists; "me lembra de enviar um email pro chefe" calendar→email).
  - 18 frases próprias: 18 de 18 (12/12 válidas, menor confiança 0,58; 6/6 fora do escopo no "não entendi"). Atenção: o limiar 0,35 foi escolhido olhando uma dessas frases ("raiz quadrada de 144", 0,34), então este 18/18 não mede generalização.
- Validação x teste coerentes (acurácia 0,934 → 0,937; F1 macro 0,927 → 0,929): sem sinal de sobreajuste.
- **Limiar 0,35** em `model.py`; terminal (`scripts/testar_intencoes.py`): 5/5 fora do escopo caem no "não entendi".
- **Conferido:** página 4 local (histórico, exemplos, fallback) e **link público funcionando** (aba "Sobre o modelo" carregou na nuvem).
- Commits na `main`, tudo enviado (`main` = `origin/main`): 44043dc (card + requirements), 055273c (limiar 0,35), b69a114 (progresso).

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
- **Limiar 0,35:** rejeita "raiz quadrada de 144" (0,34) e não afeta as 12 frases válidas (menor confiança 0,58). Custo: cobertura na validação 93,4% → 91,0%. Escolhido com validação + frases próprias, nunca com o teste. Base de apenas 6 frases fora do escopo: ajuste fino, não prova.
- Hipótese confirmada: calendar × datetime é a principal confusão; datetime é a classe mais fraca (menor classe, 4,8% do treino).
- Desvio do plano: houve `git push` antes da Etapa 5 (o app público redeployou com a página 4); o `requirements.txt` foi antecipado por isso.
- Cosmético (não corrigido): a barra lateral mostra o limiar com ponto ("0.35"); a barra de confiança é larga em monitor grande.

## Como rodar / comandos
conda activate nlp-analyzer
cd ~/Projetos/nlp-morphosyntactic-analyzer
streamlit run app.py
python scripts/testar_intencoes.py
python -c "from intent_engine.evaluate import avaliar_teste; print(avaliar_teste()['acuracia'])"
Link público: https://nlp-morphosyntactic-analyzer.streamlit.app (página 🤖)

## Pendências
- Etapa 5 (resta só o README): descrição, como rodar, licença CC BY 4.0, citação do MASSIVE e do massive-pt-br, limitações; atualizar a árvore do README com a página 4 e `intent_engine/`; conferir que nada baixa em execução.
- Testar a aba "Assistente" no link público (só a aba "Sobre o modelo" foi vista lá).
- Confirmar o que será entregue às 18h de segunda e onde.
- Etapa 6: roteiro (slides 3, 4-5 e 10), 6 a 8 frases de demonstração, perguntas prováveis, plano B offline (capturas/vídeo), referências ABNT. Abrir o link minutos antes para acordar o app.

## Próxima etapa
- **Conversa C (Etapa 5):** README e conferência final do deploy.
- Abrir com: "Conversa C (Etapa 5). Leia o PLANO_PROJETO.md e o PROGRESSO.md."