# ROTEIRO DA DEMONSTRAÇÃO — Assistente de Intenções (NLU)

Apresentação ao vivo · Disciplina de PLN · Prof. Braz Izaias da Silva Junior · Fatec Cotia
Data: terça-feira, 27/10/2026 · Autor: Anderson Capelini Andrade

**Duração:** cerca de 6 minutos, inserida **depois do slide 10 (Casos de Uso Reais)** e **antes do slide 11 (Tendências e Desafios)**.
**Link:** https://nlp-morphosyntactic-analyzer.streamlit.app (página 🤖 Assistente Intenções)
**Plano B local:** ver a seção 6.

---

## 1. A ideia em 3 frases (se esquecer tudo)

1. O assistente recebe uma frase em português e diz **em qual domínio ela cai** (alarme, clima, casa inteligente...), **quão confiante está** e dá uma **resposta simulada**.
2. É só a etapa de **NLU** do slide 3: **entender a intenção**. Ele **não gera texto, não executa nada e não é IA agêntica**.
3. Em vez de regras escritas à mão (ELIZA, slide 4), o modelo **aprendeu com exemplos**; quando não tem confiança, ele diz **"não entendi"**.

---

## 2. Antes de começar (checklist)

- [ ] `git pull` nos dois computadores (PC e notebook).
- [ ] **10 minutos antes:** abrir o link público para "acordar" o app (ele hiberna). Entrar na página 🤖 e testar uma frase.
- [ ] Rodar o ensaio da seção 5 e conferir se as confianças batem com a tabela de demonstração.
- [ ] Notebook: testar o plano B local (seção 6) uma vez, de preferência com o Wi-Fi desligado.
- [ ] Navegador com zoom em 125% (Ctrl +) e só as abas necessárias abertas.
- [ ] Clicar em **"Limpar histórico"** antes de começar.
- [ ] Abrir este roteiro em outro lugar (celular ou outra janela) para copiar e colar as frases e evitar erro de digitação.
- [ ] Capturas de tela de reserva salvas (seção 6) e carregador conectado.

---

## 3. Roteiro cronometrado

### 3.1 Transição · 0:00 a 0:20 · volta ao slide 10
> "Vimos no slide 10 que assistentes controlam a casa, agendam reuniões e cuidam de e-mails. Para mostrar como isso começa por dentro, construí um pequeno assistente que faz só a primeira etapa: **entender o que o usuário quer**, a NLU do slide 3."

*(abrir o link, página 🤖 Assistente Intenções)*

### 3.2 O que ele faz · 0:20 a 1:05
> "Eu digito uma frase em português. O assistente diz **em qual domínio** ela cai, **qual a confiança** do modelo e responde com uma **resposta simulada**. Ele **não gera texto e não executa nada de verdade**: não é IA agêntica, é só a etapa de compreensão."

### 3.3 Como funciona · 1:05 a 2:05 · ligação com os slides 4 e 5
> "No slide 4, o ELIZA e o A.L.I.C.E. funcionavam com **regras escritas à mão**: se a palavra certa não estava lá, falhavam. Aqui as regras foram trocadas por **aprendizado de máquina**. O modelo aprendeu com cerca de **6,5 mil frases** do conjunto **MASSIVE**, da Amazon, em português do Brasil. O caminho é simples: **limpo o texto**, calculo o **peso das palavras e dos pares de palavras (TF-IDF)** e uma **Regressão Logística** devolve a probabilidade de cada um dos **9 domínios**. Se a maior probabilidade for **menor que 0,35**, ele responde **'não entendi'**."

### 3.4 Demonstração · 2:05 a 4:35 · cerca de 18 segundos por frase

| # | Digitar | Resultado esperado | Confiança aprox. | O que dizer |
|---|---|---|---|---|
| 1 | `me acorda às seis e meia` | Alarmes | 0,75 | "Frase com outro verbo, não só 'alarme'." |
| 2 | `liga o ar condicionado da sala` | Casa inteligente | 0,65 | "O exemplo do slide 10, controlar o ar condicionado." |
| 3 | `agenda o dentista na terça às três` | Calendário | 0,77 | "Produtividade: agendar compromisso." |
| 4 | `envia um e-mail para a Maria` | E-mail e contatos | 0,98 | "Produtividade: e-mails." |
| 5 | `adiciona leite na lista de compras` | Listas | 0,97 | "Anotar e organizar listas." |
| 6 | `que horas são em Tóquio?` | Data e hora | 1,00 | "Pergunta simples, confiança máxima." |
| 7 | `alexa, apaga as luzes da sala` | Casa inteligente | 0,95 | "'Alexa' (slide 5, 2014) foi tratada como palavra de ativação e ignorada, para o modelo não usá-la como atalho." |
| 8 | `me conta uma piada` | **Não entendi** | 0,24 | "Fora do escopo: a confiança ficou abaixo de 0,35 e ele **admite que não entendeu** em vez de chutar." |

**Se sobrar tempo (um erro explicado, de propósito):** `lista de rock`. O modelo previu **Listas** com confiança alta (0,99), mas o rótulo correto no dataset é **Reprodução de música**. Mostra que a confiança alta não garante o acerto e que há frases ambíguas.

### 3.5 Resultados e limitações · 4:35 a 5:35 · abrir a aba "Sobre o modelo"
> "No conjunto de **teste**, **1.754 frases que o modelo nunca viu**, ele acertou **93,7%**, com **F1 macro de 0,93**. A maior confusão é **calendário com data e hora**, porque as frases são parecidas. As limitações: a tradução do conjunto foi feita **por um LLM**, é **parcial** e ainda tem resquícios de **português de Portugal**; o modelo conhece só **9 domínios**; e o desempenho em frases realmente novas pode ser **menor** que o medido, porque o conjunto tem muitas frases parecidas."

### 3.6 Fecho · 5:35 a 6:00 · volta ao slide 11
> "Esse assistente é só a **primeira camada**. Para chegar à IA agêntica, que vimos no slide 5, falta **planejar e agir**. Ele mostra, em pequena escala, a base de tudo isso: **entender a intenção**. Obrigado."

---

## 4. Perguntas prováveis e respostas curtas

1. **Por que classificar por domínio e não pelas 60 intenções?**
   Para manter simples e fácil de demonstrar. Com 9 domínios bem distintos, o resultado é mais claro e a tarefa cabe no prazo.

2. **Por que TF-IDF + Regressão Logística e não um LLM ou BERT?**
   É leve, interpretável, roda em CPU e treina no próprio app. O objetivo é didático: mostrar a NLU de ponta a ponta. A limitação é que não entende contexto nem ordem além de pares de palavras.

3. **O que é a "confiança"?**
   É a probabilidade que o modelo dá à classe mais provável. Ela ajuda a decidir quando responder, mas **não garante** o acerto (exemplo: "lista de rock", 0,99 e errada).

4. **Como escolheu o limiar de 0,35?**
   Olhando a **validação** e frases próprias, nunca o teste. O limiar automático (0,25) deixava passar frases fora do escopo; o 0,30 ainda aceitava "qual é a raiz quadrada de 144?" (0,34). O custo do 0,35 é responder a menos frases: na validação a cobertura cai de 93,4% para 91,0%.

5. **Por que o conjunto de teste só no fim?**
   Para evitar vazamento: treino ajusta o modelo, validação orienta decisões como o limiar e o teste mede uma única vez, sem influenciar nada.

6. **Qual a diferença para o ELIZA?**
   O ELIZA seguia regras escritas à mão. Aqui o modelo **aprende pesos a partir de exemplos**. Mas continua sendo um modelo simples: não gera texto nem entende contexto como um LLM.

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

---

## 5. Ensaio: conferir as confianças reais (no PC ou no notebook)

```bash
cd ~/Projetos/nlp-morphosyntactic-analyzer
conda activate nlp-analyzer
python - <<'PY'
from intent_engine.model import prever
from intent_engine.responses import nome_exibicao
FRASES = [
    "me acorda às seis e meia", "liga o ar condicionado da sala",
    "agenda o dentista na terça às três", "envia um e-mail para a Maria",
    "adiciona leite na lista de compras", "que horas são em Tóquio?",
    "alexa, apaga as luzes da sala", "me conta uma piada", "lista de rock",
]
for f in FRASES:
    r = prever(f)
    nome = nome_exibicao(r["dominio"]) if r["dominio"] else "-"
    estado = "ok " if r["entendeu"] else "NÃO ENTENDI"
    print(f"{r['confianca']:.2f} {estado} | {f!r} -> {nome}")
PY
```

Se alguma confiança destoar muito da tabela, ajuste a coluna do roteiro.

---

## 6. Plano B (se o link ou a internet falharem)

**Nível 1: link público** (abrir 10 minutos antes).

**Nível 2: local no notebook** (a página 🤖 **não precisa de internet**: o CSV está no repositório):

```bash
cd ~/Projetos/nlp-morphosyntactic-analyzer
git pull
conda activate nlp-analyzer
streamlit run app.py        # abrir http://localhost:8501
```

As páginas 1 (Parsing) e 3 (VADER) baixam dados do NLTK na primeira execução. **Abra-as uma vez com internet** para que fiquem em cache, caso o professor peça para vê-las.

**Nível 3: capturas de tela salvas fora do repositório** (celular e notebook):
1. Página inicial com os 4 cards.
2. Página 🤖 com 3 respostas, incluindo um "não entendi".
3. Aba "Sobre o modelo": as 4 métricas e o texto de interpretação.
4. Matriz de confusão e erros mais comuns.
5. Frases próprias (18 de 18).

Se der tempo, um vídeo curto da demonstração.

---

## 7. Números para memorizar

| Item | Valor |
|---|---|
| Dataset | MASSIVE pt-BR (Magurofg), CC BY 4.0 |
| Domínios | 9 |
| Treino / validação / teste | 6.571 / 1.115 / 1.754 frases |
| Acurácia no teste | 93,7% (110 erros) |
| F1 macro | 0,929 |
| Limiar de confiança | 0,35 |
| Cobertura / precisão nas aceitas | 91,7% / 96,6% |
| Melhor / pior F1 | E-mail e contatos 0,974 / Data e hora 0,842 |
| Principal confusão | Calendário → Data e hora (15), inverso (7) |
| Frases próprias | 18/18 (não mede generalização: o limiar foi ajustado olhando uma delas) |
| Tradução | feita por LLM; ~40% das frases idênticas ao português de Portugal |

---

## 8. Referências (ABNT)

FITZGERALD, Jack et al. MASSIVE: a 1M-example multilingual natural language understanding dataset with 51 typologically-diverse languages. In: ANNUAL MEETING OF THE ASSOCIATION FOR COMPUTATIONAL LINGUISTICS, 61., 2023. **Proceedings** [...]. Volume 1: Long Papers. ACL, 2023. arXiv:2204.08582.

MAGUROFG. **massive-pt-br**: localização brasileira do MASSIVE. Hugging Face, [s.d.]. Disponível em: https://huggingface.co/datasets/Magurofg/massive-pt-br. Licença CC BY 4.0. Acesso em: 25 out. 2026.

PEDREGOSA, Fabian et al. Scikit-learn: machine learning in Python. **Journal of Machine Learning Research**, v. 12, p. 2825-2830, 2011.

SPARCK JONES, Karen. A statistical interpretation of term specificity and its application in retrieval. **Journal of Documentation**, v. 28, n. 1, p. 11-21, 1972.