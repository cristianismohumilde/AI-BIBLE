import os
import json
import requests
import time

def download_from_sefaria(path):
    url = f"https://www.sefaria.org/api/texts/{path}"
    print(f"Baixando Sefaria: {url}...")
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro {response.status_code} ao baixar {url}")
        except Exception as e:
            print(f"Exceção na tentativa {attempt+1} para {url} -> {e}")
            time.sleep(2)
    return None

def main():
    print("=== Iniciando Download de Dados do Sefaria ===")
    
    # 1. Comentário Clássico: Rashi em Gênesis Capítulo 1
    # No Sefaria, o caminho para o comentário de Rashi em Gênesis 1 é "Rashi_on_Genesis.1"
    rashi_genesis_1 = download_from_sefaria("Rashi_on_Genesis.1")
    if rashi_genesis_1:
        os.makedirs("data/sefaria/commentaries/Rashi", exist_ok=True)
        with open("data/sefaria/commentaries/Rashi/Genesis_1.json", "w", encoding="utf-8") as f:
            json.dump(rashi_genesis_1, f, ensure_ascii=False, indent=2)
        print("Salvo: Rashi em Gênesis 1")
        
    # 2. Comentário Clássico: Ramban (Nahmanides) em Gênesis Capítulo 1
    # No Sefaria, é "Ramban_on_Genesis.1"
    ramban_genesis_1 = download_from_sefaria("Ramban_on_Genesis.1")
    if ramban_genesis_1:
        os.makedirs("data/sefaria/commentaries/Ramban", exist_ok=True)
        with open("data/sefaria/commentaries/Ramban/Genesis_1.json", "w", encoding="utf-8") as f:
            json.dump(ramban_genesis_1, f, ensure_ascii=False, indent=2)
        print("Salvo: Ramban em Gênesis 1")
        
    print("=== Sefaria Download Concluído! ===")

if __name__ == "__main__":
    main()
