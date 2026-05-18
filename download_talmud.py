import os
import requests
import json

def download_file(url, output_path):
    print(f"Baixando Talmud: {url}...")
    try:
        response = requests.get(url, timeout=90)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Salvo com sucesso: {output_path}")
            return True
        else:
            print(f"Erro {response.status_code} ao baixar {url}")
    except Exception as e:
        print(f"Exceção ao baixar {url} -> {e}")
    return False

def main():
    print("=== Iniciando Download de Clássicos do Talmud Bavli ===")
    
    # Lista de tratados clássicos do Talmud Bavli e suas respectivas pastas (Seder)
    # Baixaremos a versão hebraico/aramaico consolidada (merged.json) do GCS do Sefaria
    talmud_tractates = [
        {"seder": "Seder Zeraim", "tractate": "Berakhot"},
        {"seder": "Seder Moed", "tractate": "Shabbat"},
        {"seder": "Seder Nezikin", "tractate": "Sanhedrin"}
    ]
    
    base_url = "https://storage.googleapis.com/sefaria-export/json/Talmud/Bavli"
    dest_dir = "data/Talmud"
    
    for item in talmud_tractates:
        seder = item["seder"]
        tractate = item["tractate"]
        
        # Url com escape de espaço
        url = f"{base_url}/{seder}/{tractate}/Hebrew/merged.json".replace(" ", "%20")
        output_file = f"{dest_dir}/{tractate}.json"
        
        download_file(url, output_file)
        
    print("=== Download do Talmud Concluído! ===")

if __name__ == "__main__":
    main()
