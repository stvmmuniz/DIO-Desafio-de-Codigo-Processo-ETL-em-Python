# ============================================================
# ETAPA 0 – CONFIGURAÇÃO DO AMBIENTE
# ============================================================

# Bibliotecas padrão
import os
import zipfile
import glob
import unicodedata

# Bibliotecas externas
import requests
import pandas as pd

# ============================================================
# ETAPA 1 – EXTRAÇÃO DOS DADOS
# ============================================================

URL = "https://portaldatransparencia.gov.br/download-de-dados/despesas-favorecidos/202511"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "data_raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data_processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(URL, headers=headers)

if response.status_code != 200:
    raise Exception(f"Erro no download | Status: {response.status_code}")

zip_path = os.path.join(RAW_DIR, "despesas_favorecidos_202511.zip")

with open(zip_path, "wb") as f:
    f.write(response.content)

print("ZIP baixado com sucesso!")

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    for member in zip_ref.namelist():
        target_path = os.path.join(RAW_DIR, member)
        if os.path.exists(target_path):
            os.remove(target_path)
        zip_ref.extract(member, RAW_DIR)

print("ZIP extraído com sucesso!")

csv_files = glob.glob(os.path.join(RAW_DIR, "*.csv"))

if not csv_files:
    raise Exception("Nenhum arquivo CSV encontrado após extração do ZIP.")

raw_file = csv_files[0]
print(f"CSV identificado: {os.path.basename(raw_file)}")

# ============================================================
# ETAPA 2 – TRANSFORMAÇÃO DOS DADOS
# ============================================================

df = pd.read_csv(
    raw_file,
    sep=';',
    encoding='latin1',
    low_memory=False
)

# ------------------------------------------------------------
# 2.1 – Padronização dos nomes das colunas
# ------------------------------------------------------------

def normalizar_coluna(col):
    col = col.strip()
    col = unicodedata.normalize("NFKD", col).encode("ascii", "ignore").decode("utf-8")
    col = col.replace(" ", "")
    return col

df.columns = [normalizar_coluna(c) for c in df.columns]

if "Anoemesdolancamento" in df.columns:
    df.rename(columns={"Anoemesdolancamento": "DataLancamento"}, inplace=True)
else:
    raise Exception("Coluna de data não encontrada no dataset.")

# ------------------------------------------------------------
# 2.2 – Conversão de valores monetários
# ------------------------------------------------------------

df["ValorRecebido"] = (
    df["ValorRecebido"]
      .astype(str)
      .str.replace(".", "", regex=False)
      .str.replace(",", ".", regex=False)
      .astype(float)
)

# ------------------------------------------------------------
# 2.3 – Conversão da coluna de data
# ------------------------------------------------------------

df["DataLancamento"] = pd.to_datetime(
    df["DataLancamento"],
    dayfirst=True,
    errors="coerce"
)

# ------------------------------------------------------------
# 2.4 – Conversão de códigos para inteiro
# ------------------------------------------------------------

colunas_inteiro = [
    "CodigoOrgaoSuperior",
    "CodigoOrgao",
    "CodigoUnidadeGestora"
]

for col in colunas_inteiro:
    df[col] = (
        df[col]
          .astype(str)
          .str.replace(".0", "", regex=False)
          .replace("nan", None)
          .astype("Int64")
    )

# ------------------------------------------------------------
# 2.5 – Padronização das colunas texto
# ------------------------------------------------------------

colunas_texto = [
    "CodigoFavorecido",
    "NomeFavorecido",
    "SiglaUF",
    "NomeMunicipio",
    "NomeOrgaoSuperior",
    "NomeOrgao",
    "NomeUnidadeGestora"
]

for col in colunas_texto:
    df[col] = df[col].astype(str).str.strip()

# ============================================================
# ETAPA 3 – PREPARAÇÃO FINAL PARA POWER BI
# ============================================================

# ------------------------------------------------------------
# 3.1 – Garantia dos tipos finais
# ------------------------------------------------------------

df["DataLancamento"] = df["DataLancamento"].dt.date
df["ValorRecebido"] = df["ValorRecebido"].astype(float)

# ------------------------------------------------------------
# 3.2 – Seleção e ordenação das colunas finais
# ------------------------------------------------------------

colunas_final = [
    "DataLancamento",
    "ValorRecebido",
    "CodigoFavorecido",
    "NomeFavorecido",
    "SiglaUF",
    "NomeMunicipio",
    "CodigoOrgaoSuperior",
    "NomeOrgaoSuperior",
    "CodigoOrgao",
    "NomeOrgao",
    "CodigoUnidadeGestora",
    "NomeUnidadeGestora"
]

df = df[colunas_final]

# ------------------------------------------------------------
# 3.3 – Exportação do dataset final
# ------------------------------------------------------------

output_file = os.path.join(
    PROCESSED_DIR,
    "despesas_favorecidos_202511_powerbi.csv"
)

df.to_csv(
    output_file,
    index=False,
    sep=';',
    encoding='latin1'
)

print("Dataset final preparado para consumo no Power BI!")
