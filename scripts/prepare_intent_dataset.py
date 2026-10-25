"""
Prepara o recorte do MASSIVE pt-BR para o assistente de intenções.

Lê os .jsonl de ~/dados/massive-pt-br, filtra os 9 domínios escolhidos,
limpa o mínimo necessário (strip + Unicode), remove duplicatas e vazamento
treino -> validação/teste, e salva data/intent_assistant/massive_ptbr_subset.csv.

Reexecutável: rodar de novo sempre sobrescreve o CSV com o mesmo resultado.
Uso (a partir da raiz do repositório):  python scripts/prepare_intent_dataset.py
"""
import json
import unicodedata
from pathlib import Path

import pandas as pd

# --- Caminhos -------------------------------------------------------------
PASTA_DADOS = Path.home() / "dados" / "massive-pt-br"      # fora do repositório
RAIZ = Path(__file__).resolve().parents[1]                  # raiz do repositório
ARQ_SAIDA = RAIZ / "data" / "intent_assistant" / "massive_ptbr_subset.csv"

# --- Domínios escolhidos (tabela 4.3 do plano): scenario -> código ---------
# Regra de saída do e-mail: se o F1 na validação ficar < 0,80, basta apagar
# a linha 7 deste dicionário e rodar o script de novo.
DOMINIOS = {
    16: "alarm",
    17: "weather",
    3: "play",
    8: "iot",
    2: "calendar",
    11: "lists",
    5: "datetime",
    4: "news",
    7: "email",
}

SPLITS = ["train", "validation", "test"]


def normalizar(texto: str) -> str:
    """Texto bruto: só normalização Unicode (NFKC) e strip.
    O NFKC troca o hífen não separável (U+2011) de 'e‑mail' por hífen comum.
    A limpeza pesada fica em intent_engine/preprocess.py."""
    return unicodedata.normalize("NFKC", texto or "").strip()


def ler_split(nome: str) -> pd.DataFrame:
    """Lê um .jsonl e devolve só as colunas necessárias: utt_br e scenario."""
    caminho = PASTA_DADOS / f"{nome}.jsonl"
    registros = []
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            reg = json.loads(linha)
            # int() porque scenario é um id numérico (aceita número ou texto)
            registros.append({"utt_br": reg["utt_br"], "scenario": int(reg["scenario"])})
    return pd.DataFrame(registros)


def main() -> None:
    resumo = {}          # contagens para mostrar no final
    dfs = {}             # um DataFrame por split, já filtrado e normalizado

    # 1) Ler, filtrar domínios, normalizar texto e remover textos vazios
    for split in SPLITS:
        df = ler_split(split)
        lidas = len(df)
        df = df[df["scenario"].isin(DOMINIOS)].copy()
        nos_dominios = len(df)

        df["texto"] = df["utt_br"].map(normalizar)
        df = df[df["texto"] != ""]
        df["dominio"] = df["scenario"].map(DOMINIOS)
        df["split"] = split

        resumo[split] = {
            "linhas lidas": lidas,
            "nos 9 dominios": nos_dominios,
            "removidas (vazias)": nos_dominios - len(df),
        }
        dfs[split] = df[["texto", "dominio", "split"]]

    # 2) Treino: remover frases duplicadas (mantém a primeira ocorrência)
    treino = dfs["train"]
    # frase igual com domínios diferentes seria um rótulo conflitante: só contamos
    conflitos = int((treino.groupby("texto")["dominio"].nunique() > 1).sum())
    antes = len(treino)
    treino = treino.drop_duplicates(subset="texto", keep="first")
    dfs["train"] = treino
    resumo["train"]["removidas (duplicatas)"] = antes - len(treino)

    # 3) Validação e teste: remover frases idênticas às do treino (vazamento)
    frases_treino = set(treino["texto"])
    for split in ["validation", "test"]:
        antes = len(dfs[split])
        dfs[split] = dfs[split][~dfs[split]["texto"].isin(frases_treino)]
        resumo[split]["removidas (iguais ao treino)"] = antes - len(dfs[split])

    # 4) Juntar tudo e salvar
    final = pd.concat([dfs[s] for s in SPLITS], ignore_index=True)
    ARQ_SAIDA.parent.mkdir(parents=True, exist_ok=True)
    final.to_csv(ARQ_SAIDA, index=False, encoding="utf-8")

    # --- Relatório ---------------------------------------------------------
    print("\n=== Linhas removidas / mantidas por split ===")
    print(pd.DataFrame(resumo).fillna(0).astype(int).to_string())
    print(f"\nFrases do treino com rótulo conflitante (mesmo texto, 2+ domínios): {conflitos}")

    print("\n=== Contagem por domínio e split ===")
    tabela = pd.crosstab(final["dominio"], final["split"], margins=True, margins_name="total")
    print(tabela[SPLITS + ["total"]].to_string())

    print("\n=== Proporção de cada domínio no treino (desbalanceamento) ===")
    prop = (final[final["split"] == "train"]["dominio"].value_counts(normalize=True) * 100).round(1)
    print(prop.to_string())

    tamanho_kb = ARQ_SAIDA.stat().st_size / 1024
    print(f"\nCSV salvo em: {ARQ_SAIDA}  ({len(final)} linhas, {tamanho_kb:.0f} KB)")


if __name__ == "__main__":
    main()