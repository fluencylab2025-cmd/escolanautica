import requests
import os
import gspread
from google.oauth2.service_account import Credentials
import json
import time
from datetime import datetime

# =====================
# GOOGLE SHEETS
# =====================

creds_json = os.getenv("GOOGLE_CREDS")
creds_dict = json.loads(creds_json)

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(creds)

sheet = client.open("EEC Leads").sheet1

# =====================
# GOOGLE API
# =====================

API_KEY = os.getenv("GOOGLE_API_KEY")

# 🔎 VÁRIAS BUSCAS
queries = [
    "curso arrais amador Brasil",
    "escola náutica Brasil",
    "despachante náutico Brasil",
    "regularização embarcação Brasil"
]

# =====================
# FUNÇÃO UF
# =====================

def extrair_uf(endereco):
    estados = [
        "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
        "MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN",
        "RS","RO","RR","SC","SP","SE","TO"
    ]
    for uf in estados:
        if f"- {uf}" in endereco:
            return uf
    return "N/A"

# =====================
# LOOP PRINCIPAL
# =====================

for query in queries:
    print(f"🔎 Buscando: {query}")

    search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={API_KEY}"
    response = requests.get(search_url)
    data = response.json()
    print("RESULTADOS:", data)

    for place in data.get("results", []):
        nome = place.get("name")
        endereco = place.get("formatted_address")
        rating = place.get("rating", "N/A")
        place_id = place.get("place_id")

        uf = extrair_uf(endereco)

        # detalhes
        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number,website&key={API_KEY}"
        
        details_response = requests.get(details_url)
        details = details_response.json().get("result", {})

        telefone = details.get("formatted_phone_number", "N/A")
        site = details.get("website", "N/A")

        data_hoje = datetime.now().strftime("%Y-%m-%d")

        sheet.append_row([
            uf,
            nome,
            endereco,
            rating,
            telefone,
            site,
            data_hoje
        ])

        time.sleep(1)

print("✅ Leads completos enviados!")
