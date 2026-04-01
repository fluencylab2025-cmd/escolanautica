import requests
from bs4 import BeautifulSoup
import time
import re

def buscar_google(query, paginas=3):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    resultados = []

    for page in range(paginas):
        start = page * 10
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}&start={start}"

        print(f"🔎 Buscando página {page + 1}...")

        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        for g in soup.select(".tF2Cxc"):
            title = g.select_one("h3")
            link = g.select_one("a")

            if title and link:
                resultados.append({
                    "titulo": title.text,
                    "link": link["href"]
                })

        time.sleep(2)

    return resultados


def extrair_contatos(url):
    try:
        res = requests.get(url, timeout=5)
        texto = res.text

        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+", texto)
        telefones = re.findall(r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}", texto)

        return list(set(emails)), list(set(telefones))

    except:
        return [], []


# EXECUÇÃO
dados = buscar_google("escola nautica brasil", paginas=3)

for d in dados:
    print("Empresa:", d["titulo"])
    print("Site:", d["link"])

    emails, telefones = extrair_contatos(d["link"])

    print("Emails:", emails)
    print("Telefones:", telefones)
    print("==========")
