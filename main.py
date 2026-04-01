import os
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Pega credenciais do GitHub Secrets
creds_json = os.environ.get("GOOGLE_CREDENTIALS")
creds_dict = json.loads(creds_json)

# Autenticação
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(credentials)

# Abre planilha
sheet = client.open("EEC Leads").sheet1

# Dado de teste (depois vamos automatizar)
data = [
    "SP",
    "Escola Náutica Exemplo",
    "São Paulo",
    "(11) 99999-9999",
    "Teste",
    datetime.now().strftime("%Y-%m-%d")
]

# Insere linha
sheet.append_row(data)

print("✅ Dado enviado para planilha!")
