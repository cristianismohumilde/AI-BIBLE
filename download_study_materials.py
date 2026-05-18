import os
import json
import requests

def download_file(url, output_path):
    print(f"Baixando: {url}...")
    try:
        response = requests.get(url, timeout=60)
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
    print("=== Iniciando Download de Materiais de Estudo Bíblico (Domínio Público) ===")
    
    # Criar pasta de destino
    dest_dir = "data/study_materials"
    os.makedirs(dest_dir, exist_ok=True)
    
    # 1. Dicionário Strong (Grego e Hebraico integrados)
    # Fonte: Mormon Documentation Project contendo dados compilados de Open Scriptures
    strongs_url = "https://raw.githubusercontent.com/mormon-documentation-project/strongs/master/strongs.json"
    download_file(strongs_url, f"{dest_dir}/strongs.json")
    
    print("=== Download Concluído! Materiais salvos em data/study_materials ===")

if __name__ == "__main__":
    main()
