import requests
import pandas as pd
import time
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv
import os

load_dotenv()

# === Configurações ===
API_KEY = os.getenv("TMDB_API_KEY")
INPUT_CSV = Path("data/amazon_prep_v2.csv")
OUTPUT_CSV = Path("data/teste.csv") # mudar o nome do arquivo ❗❗
ERROR_LOG = Path("logs/errors.log")
CHECKPOINT_EVERY = 100

# === Criação de pastas se necessário ===
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
ERROR_LOG.parent.mkdir(parents=True, exist_ok=True)

# === Carrega dados e mantém progresso ===
if OUTPUT_CSV.exists():
    df = pd.read_csv(OUTPUT_CSV)
    print("✔️  Continuação detectada. Retomando progresso anterior.")
else:
    df = pd.read_csv(INPUT_CSV)
    df["release_year"] = None

# === Funções utilitárias ===
def get_media_type(row):
    if row["type"].lower() == "movie":
        return "movie"
    elif row["type"].lower() == "tv show":
        return "tv"
    return "movie"

def get_release_year(title, media_type):
    url = f"https://api.themoviedb.org/3/search/{media_type}"
    params = {
        "api_key": API_KEY,
        "query": title,
        "language": "pt-BR"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        results = data.get("results")
        if results:
            date_field = "release_date" if media_type == "movie" else "first_air_date"
            date = results[0].get(date_field)
            if date and len(date) >= 4:
                return int(date[:4])
        return None
    except Exception as e:
        with open(ERROR_LOG, "a", encoding="utf-8") as log:
            log.write(f"{title} ({media_type}) → ERRO: {e}\n")
        return None

# === Loop com progresso e checkpoint ===
start_index = df[df["release_year"].isna()].index.min()
for i in tqdm(range(start_index, len(df)), desc="🔍 Buscando anos", unit="item"):
    if pd.notna(df.at[i, "release_year"]):
        continue

    title = df.at[i, "title"]
    media_type = get_media_type(df.loc[i])
    year = get_release_year(title, media_type)

    df.at[i, "release_year"] = year
    time.sleep(0.25)  # Limita ~4 req/s (240/min)

    # Checkpoint incremental
    if (i + 1) % CHECKPOINT_EVERY == 0:
        df.to_csv(OUTPUT_CSV, index=False)

# === Salvamento final ===
df.to_csv(OUTPUT_CSV, index=False)
print(f"\n✅ Arquivo salvo com anos corrigidos: {OUTPUT_CSV}")
print(f"📄 Erros registrados em: {ERROR_LOG}")
