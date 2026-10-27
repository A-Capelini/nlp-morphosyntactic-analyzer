# ROTEIRO DA DEMONSTRAÇÃO — Assistente de Intenções (NLU)

Apresentação ao vivo · Disciplina de PLN · Prof. Braz Izaias da Silva Junior · Fatec Cotia
Data: terça-feira, 27/10/2026, às 19h · Autor: Anderson Capelini Andrade
Atualizado: 26/10/2026, com o baseline por regras e os números finais.

**Duração:** cerca de 6 a 6,5 minutos, inserida **depois do slide 10 (Casos de Uso Reais)** e **antes do slide 11 (Tendências e Desafios)**.
**Link:** https://nlp-morphosyntactic-analyzer.streamlit.app (página 🤖 Assistente Intencoes)
**Plano B local:** ver a seção 6.

---

## 1. A ideia em 3 frases (se esquecer tudo)

1. O assistente recebe uma frase em português e diz **em qual domínio ela cai** (alarme, clima, casa inteligente...), **quão confiante está** e dá uma **resposta simulada**.
2. É só a etapa de **NLU** do slide 3: **entender a intenção**. Ele **não gera texto, não executa nada e não é IA agêntica**.
3. Em vez de **regras escritas à mão** (ELIZA, slide 4), o modelo **aprendeu com exemplos**: entende frases que as regras não entendem e, quando não tem confiança, diz **"não entendi"**.

---

## 2. Antes de começar (checklist)

- [ ] `git pull` nos dois computadores (PC e notebook).
- [ ] **10 minutos antes:** abrir o link público para "acordar" o app (ele hiberna). Entrar na página 🤖 e testar uma frase.
- [ ] Rodar o ensaio da seção 5 e conferir se as confianças batem com as tabelas.
- [ ] Notebook: testar o plano B local (seção 6) uma vez, de preferência com o Wi-Fi desligado.
- [ ] Navegador com zoom em 125% (Ctrl +) e só as abas necessárias abertas.
- [ ] Na aba "Assistente": **interruptor "Comparar com as regras" DESLIGADO** no início (ele só é ligado no bloco 3.5). Clicar em **"Limpar histórico"**.
- [ ] Abrir este roteiro em outro lugar (celular ou outra janela) para copiar e colar as frases e evitar erro de digitação.
- [ ] Capturas de tela de reserva salvas (seção 6) e carregador conectado.

---

## 3. Roteiro cronometrado

### 3.1 Transição · 0:00 a 0:20 · volta ao slide 10
> "Vimos no slide 10 que assistentes controlam a casa, agendam reuniões e cuidam de e-mails. Para mostrar como isso começa por dentro, construí um pequeno assistente que faz só a primeira etapa: **entender o que o usuário quer**, a NLU do slide 3."

*(abrir o link, página 🤖 Assistente Intencoes)*

### 3.2 O que ele faz · 0:20 a 1:00
> "Eu digito uma frase em português. O assistente diz **em qual domínio** ela cai, **qual a confiança** do modelo e responde com uma **resposta simulada**. Ele **não gera texto e não executa nada de verdade**: não é IA agêntica, é só a etapa de compreensão."

### 3.3 Como funciona · 1:00 a 1:50 · ligação com os slides 4 e 5
> "No slide 4, o ELIZA e o A.L.I.C.E. funcionavam com **regras escritas à mão**: se a palavra certa não estava lá, falhavam. Aqui o modelo **aprendeu com exemplos**: cerca de **6,5 mil frases** do conjunto **MASSIVE**, da Amazon, em português do Brasil. Eu **limpo o texto**, calculo o **peso das palavras e dos pares de palavras (TF-IDF)** e uma **Regressão Logística** devolve a probabilidade de cada um dos **9 domínios**. Se a maior probabilidade for **menor que 0,35**, ele responde **'não entendi'**."

### 3.4 Demonstração · 1:50 a 3:35 · cerca de 15 segundos por frase *(interruptor desligado)*

| # | Digitar | Resultado esperado | Confiança | O que dizer |
|---|---|---|---|---|
| 1 | `me acorda às seis e meia` | Alarmes | 0,75 | "Outro verbo, não só 'alarme'." |
| 2 | `liga o ar condicionado da sala` | Casa inteligente | 0,65 | "O exemplo do slide 10." |
| 3 | `agenda o dentista na terça às três` | Calendário | 0,77 | "Produtividade: agendar compromisso." |
| 4 | `envia um e-mail para a Maria` | E-mail e contatos | 0,98 | "Produtividade: e-mails." |
| 5 | `que horas são em Tóquio?` | Data e hora | 1,00 | "Pergunta simples, confiança máxima." |
| 6 | `alexa, apaga as luzes da sala` | Casa inteligente | 0,95 | "'Alexa' (slide 5, 2014) é tratada como palavra de ativação e ignorada, para o modelo não usá-la como atalho." |
| 7 | `me conta uma piada` | **Não entendi** | 0,24 | "Fora do escopo: a confiança ficou abaixo de 0,35 e ele **admite que não entendeu** em vez de chutar." |

### 3.5 Contraste: regras × modelo · 3:35 a 4:30 · **ligar o interruptor "Comparar com as regras (estilo ELIZA)"**
> "Para mostrar o que o aprendizado traz em relação ao slide 4, ligo uma comparação com um assistente **por regras**, de palavras-chave, no estilo do ELIZA. Em frases que têm a palavra-chave, os dois acertam. Mas veja o que acontece quando o usuário **fala de outro jeito**."

| # | Digitar | Modelo | Regras | O que dizer |
|---|---|---|---|---|
| 8 | `vai esfriar de madrugada?` | Clima (0,95) | **não entendi** | "Não tem 'chover', 'frio' nem 'previsão'. As regras ficam mudas; o modelo entende o sentido." |
| 9 | `vou precisar de casaco amanhã?` | Clima (0,82) | **não entendi** | "Mesma coisa: nenhuma palavra-chave, mas o modelo aprendeu que isso é clima." |

*(se sobrar tempo: `deixa o quarto mais claro` → Casa inteligente 0,73 contra "não entendi"; `tenho dentista na terça?` → Calendário 0,64 contra "não entendi")*

**Se sobrar tempo (um erro explicado, de propósito):** `lista de rock`. O modelo previu **Listas** com confiança alta (0,99), mas o rótulo correto no dataset é **Reprodução de música**. Mostra que a confiança alta não garante o acerto e que há frases ambíguas.

### 3.6 Resultados e limitações · 4:30 a 5:50 · abrir a aba "Sobre o modelo"
> "No conjunto de **teste**, **1.754 frases que o modelo nunca viu**, ele acertou **93,7%**, com **F1 macro de 0,93**. Aqui está a comparação com as regras: elas respondem a **79,6%** das frases e acertam **92,9%** das que respondem, mas o total fica em **73,9%**, porque **cerca de 20% das frases ficam sem resposta** por não terem nenhuma palavra-chave. O modelo responde a mais frases e acerta mais delas. A maior confusão do modelo é **calendário com data e hora**, porque as frases são parecidas. As limitações: a tradução do conjunto foi feita **por um LLM**, é **parcial** e tem resquícios de **português de Portugal**; o modelo conhece só **9 domínios**; e o desempenho em frases realmente novas pode ser **menor** que o medido, porque o conjunto tem muitas frases parecidas. As regras também não foram otimizadas, então a comparação é ilustrativa."

### 3.7 Fecho · 5:50 a 6:20 · volta ao slide 11
> "Esse assistente é só a **primeira camada**. Para chegar à IA agêntica, que vimos no slide 5, falta **planejar e agir**. Ele mostra, em pequena escala, a base de tudo isso: **entender a intenção**, e a diferença entre seguir regras e aprender com exemplos. Obrigado."

**Se o tempo for menor que 6 minutos, corte nesta ordem:** frases 3 e 4 da demonstração; o texto de "Como funciona" (deixar só uma frase); a frase 9 do contraste.

---

## 4. Perguntas prováveis e respostas curtas

1. **Por que classificar por domínio e não pelas 60 intenções?**
   Para manter simples e fácil de demonstrar. Com 9 domínios bem distintos, o resultado é mais claro e a tarefa cabe no prazo.

2. **Por que TF-IDF + Regressão Logística e não um LLM ou BERT?**
   É leve, interpretável, roda em CPU e treina no próprio app. O objetivo é didático: mostrar a NLU de ponta a ponta. A limitação é que não entende contexto nem ordem além de pares de palavras.

3. **O que é a "confiança"?**
   É a probabilidade que o modelo dá à classe mais provável. Ela ajuda a decidir quando responder, mas **não garante** o acerto (exemplo: "lista de rock", 0,99 e errada).

4. **Como escolheu o limiar de 0,35?**
   Olhando a **validação** e frases próprias, nunca o teste. O limiar automático (0,25) deixava passar frases fora do escopo; o 0,30 ainda aceitava "qual é a raiz quadrada de 144?" (0,34). O custo do 0,35 é responder a menos frases: na validação a cobertura cai de 93,4% para 91,0%. A tabela está na aba "Sobre o modelo".

5. **Por que o conjunto de teste só no fim?**
   Para evitar vazamento: o treino ajusta o modelo, a validação orienta decisões como o limiar e o teste mede uma única vez, sem influenciar nada.

6. **Qual a diferença para o ELIZA?** *(resposta com dados)*
   O ELIZA seguia regras escritas à mão. Fiz um baseline desse tipo, com palavras-chave por domínio, e comparei no mesmo teste: as regras respondem a 79,6% das frases e acertam 92,9% das que respondem, mas o total é 73,9%. O modelo, que aprende pesos a partir de exemplos, chega a 93,7%. Frases como "vai esfriar de madrugada?" ficam sem resposta nas regras e o modelo entende. Mas o modelo continua simples: não gera texto nem entende contexto como um LLM.

7. **Isso é IA agêntica?**
   Não. A resposta de cada domínio é fixa. Não planeja nem executa tarefas em várias etapas.

8. **93,7% é um bom número?**
   É bom para um modelo simples, mas deve ser lido com cuidado: o corpus tem muitas frases parecidas e a tradução é parcial, então em frases novas pode ser menor. Também **não é comparável** aos 88,2% da página do dataset, que são de outro modelo, com 60 intenções.

9. **Os dados são seus? Qual a licença?**
   Não. O MASSIVE é da Amazon; a versão em português do Brasil é do autor Magurofg, no Hugging Face, sob **CC BY 4.0**. Aqui foi modificado: filtrado para 9 domínios e sem frases duplicadas. Citado no README.

10. **Por que a tradução é um problema?**
    Foi feita por um LLM, sem revisão humana. Cerca de 40% das frases são idênticas ao português de Portugal e há construções europeias e frases truncadas. É uma limitação declarada.

11. **Quais são os erros mais comuns?**
    Calendário previsto como data e hora (15 frases) e o inverso (7 frases). Exemplos: "me diz as horas dos eventos", "hoje é dia de São João".

12. **Por que "alexa" foi removida?**
    Das 107 frases com "alexa" no treino, 36 eram de casa inteligente. O modelo poderia usar a palavra como atalho em vez de entender o pedido.

13. **O que acontece com uma frase sem sentido?**
    "asdfgh qwerty" tem confiança baixa (0,19) e cai no "não entendi". Se a frase some inteira na limpeza (ex.: "por favor"), também.

14. **O baseline por regras foi feito olhando o conjunto de teste?**
    Não. As palavras-chave foram escritas a partir do conhecimento dos domínios, sem consultar o teste e sem otimização. Os números são parecidos na validação (72,6%) e no teste (73,9%), sem ajuste. Com mais esforço manual as regras melhorariam; a comparação é ilustrativa.

15. **As regras são ruins?**
    Não: quando respondem, acertam 92,9%. O problema é a **cobertura** (79,6%): se a frase não tem nenhuma palavra-chave, elas ficam mudas. No clima, por exemplo, menos da metade das frases (recall 0,455 na validação) tem alguma das palavras-chave.

16. **Por que o modelo com limiar tem acurácia menor (88,6%) que o modelo sem limiar (93,7%)?**
    Porque na coluna de acurácia o "não entendi" conta como erro. O limiar troca **cobertura por precisão**: o assistente responde a menos frases (91,7%), mas acerta mais das que responde (96,6%).

17. **Por que "põe aquele som que eu gosto" não foi entendida?**
    A confiança foi 0,34, um centésimo abaixo do limiar de 0,35. É o trade-off do limiar: ele evita respostas erradas, ao custo de perder alguns acertos. Expressões que não aparecem nos exemplos de treino ("bota um sambinha aí", "me tira da cama às cinco") também ficam abaixo do limiar.

---

## 5. Ensaio: conferir as confianças reais (no PC ou no notebook)

```bash
cd ~/projetos/nlp-morphosyntactic-analyzer      # no PC: ~/Projetos/nlp-morphosyntactic-analyzer
conda activate nlp-analyzer
python - <<'PY'
from intent_engine.model import prever
from intent_engine.responses import nome_exibicao
from intent_engine.rules_baseline import prever_regras
FRASES = [
    "me acorda às seis e meia", "liga o ar condicionado da sala",
    "agenda o dentista na terça às três", "envia um e-mail para a Maria",
    "que horas são em Tóquio?", "alexa, apaga as luzes da sala", "me conta uma piada",
    "vai esfriar de madrugada?", "vou precisar de casaco amanhã?",
    "deixa o quarto mais claro", "tenho dentista na terça?", "lista de rock",
]
for f in FRASES:
    m, r = prever(f), prever_regras(f)
    ml = (f"{nome_exibicao(m['dominio'])} ({m['confianca']:.2f})" if m["entendeu"]
          else f"não entendi ({m['confianca']:.2f})")
    rg = nome_exibicao(r["dominio"]) if r["dominio"] else "não entendi"
    print(f"{f!r}\n   modelo: {ml} | regras: {rg}")
PY
```

**Valores já conferidos em ensaios anteriores:** "vai esfriar de madrugada?" Clima 0,95 (regras: não entendi); "vou precisar de casaco amanhã?" Clima 0,82 (regras: não entendi); "deixa o quarto mais claro" Casa inteligente 0,73 (regras: não entendi); "tenho dentista na terça?" Calendário 0,64 (regras: não entendi); "me conta uma piada" não entendi 0,24 (regras: não entendi). Nas frases 1 a 6 da demonstração, **espera-se** que as regras também acertem (têm palavra-chave); confirme no ensaio.

---

## 6. Plano B (se o link ou a internet falharem)

**Nível 1: link público** (abrir 10 minutos antes).

**Nível 2: local no notebook** (a página 🤖 **não precisa de internet**: o CSV está no repositório):

```bash
cd ~/projetos/nlp-morphosyntactic-analyzer      # no PC: ~/Projetos/nlp-morphosyntactic-analyzer
git pull
conda activate nlp-analyzer
streamlit run app.py        # abrir http://localhost:8501
```

As páginas 1 (Parsing) e 3 (VADER) baixam dados do NLTK na primeira execução. **Abra-as uma vez com internet** para que fiquem em cache, caso o professor peça para vê-las.

**Nível 3: capturas de tela salvas fora do repositório** (celular e notebook):
1. Página inicial com os 4 cards.
2. Página 🤖 com 3 respostas, incluindo um "não entendi".
3. Aba "Assistente" com o interruptor ligado, mostrando "Clima" × "Regras: não entendi" (frase `vai esfriar de madrugada?`).
4. Aba "Sobre o modelo": as 4 métricas e a tabela "Regras × modelo".
5. Matriz de confusão e erros mais comuns.
6. Frases próprias (18 de 18).

Se der tempo, um vídeo curto da demonstração.

---

## 7. Números para memorizar

| Item | Valor |
|---|---|
| Dataset | MASSIVE pt-BR (Magurofg), CC BY 4.0 |
| Domínios | 9 |
| Treino / validação / teste | 6.571 / 1.115 / 1.754 frases |
| Acurácia do modelo no teste | 93,7% (110 erros) |
| F1 macro | 0,929 |
| Limiar de confiança | 0,35 |
| Cobertura / precisão nas aceitas | 91,7% / 96,6% |
| Acurácia do modelo com limiar (não entendi = erro) | 88,6% |
| Melhor / pior F1 | E-mail e contatos 0,974 / Data e hora 0,842 |
| Principal confusão | Calendário → Data e hora (15), inverso (7) |
| Regras (estilo ELIZA), teste | acurácia 73,9% · F1 macro 0,811 · cobertura 79,6% · precisão nas respondidas 92,9% |
| Regras, validação | acurácia 72,6% · cobertura 78,1% · precisão 92,9% |
| Pior classe das regras | Clima (recall 0,455 na validação) |
| Frases próprias | 18/18 (não mede generalização: o limiar foi ajustado olhando uma delas) |
| Tradução | feita por LLM; ~40% das frases idênticas ao português de Portugal |

---

## 8. Referências (ABNT)

FITZGERALD, Jack et al. MASSIVE: a 1M-example multilingual natural language understanding dataset with 51 typologically-diverse languages. In: ANNUAL MEETING OF THE ASSOCIATION FOR COMPUTATIONAL LINGUISTICS, 61., 2023. **Proceedings** [...]. Volume 1: Long Papers. ACL, 2023. arXiv:2204.08582.

MAGUROFG. **massive-pt-br**: localização brasileira do MASSIVE. Hugging Face, [s.d.]. Disponível em: https://huggingface.co/datasets/Magurofg/massive-pt-br. Licença CC BY 4.0. Acesso em: 25 out. 2026.

PEDREGOSA, Fabian et al. Scikit-learn: machine learning in Python. **Journal of Machine Learning Research**, v. 12, p. 2825-2830, 2011.

SPARCK JONES, Karen. A statistical interpretation of term specificity and its application in retrieval. **Journal of Documentation**, v. 28, n. 1, p. 11-21, 1972.

WEIZENBAUM, Joseph. ELIZA — a computer program for the study of natural language communication between man and machine. **Communications of the ACM**, New York, v. 9, n. 1, p. 36-45, jan. 1966.