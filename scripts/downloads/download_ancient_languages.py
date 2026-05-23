import os
import requests
import zipfile
import io

def download_file(url, output_path):
    print(f"Baixando: {url}...")
    try:
        response = requests.get(url, timeout=120)
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
    print("=== Iniciando Download das Coleções de Idiomas Antigos ===")
    
    dest_dir = "data/ancient_versions"
    os.makedirs(dest_dir, exist_ok=True)
    
    # 1. Copta Sahídico (CopSahBible2.json)
    coptic_url = "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/json/CopSahBible2.json"
    download_file(coptic_url, f"{dest_dir}/coptic_sahidic.json")
    
    # 2. Armênio Oriental (ArmEastern.json)
    armenian_url = "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/json/ArmEastern.json"
    download_file(armenian_url, f"{dest_dir}/armenian_eastern.json")
    
    # 3. Peshitta Siríaca (Peshitta.json)
    peshitta_url = "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/json/Peshitta.json"
    download_file(peshitta_url, f"{dest_dir}/peshitta_syriac.json")
    
    # 4. Ge'ez (Etiópico Antigo)
    # Baixar zip e descompactar
    geez_url = "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/sources_backup/gez/Geez/Geez.zip"
    print(f"Baixando Ge'ez ZIP: {geez_url}...")
    try:
        response = requests.get(geez_url, timeout=120)
        if response.status_code == 200:
            print("Download de Ge'ez concluído! Descompactando...")
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                z.extractall(f"{dest_dir}/geez_extracted")
            print(f"Ge'ez extraído com sucesso para {dest_dir}/geez_extracted")
        else:
            print(f"Erro {response.status_code} ao baixar Ge'ez ZIP")
    except Exception as e:
        print(f"Erro ao baixar/extrair Ge'ez: {e}")
        
    # 5. Targum Onkelos (Aramaico Pentateuco) - Sefaria (5 Livros da Torah)
    targum_books = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]
    for book in targum_books:
        onkelos_url = f"https://storage.googleapis.com/sefaria-export/json/Tanakh/Targum/Onkelos/Torah/Onkelos%20{book}/Hebrew/merged.json"
        download_file(onkelos_url, f"{dest_dir}/targum_onkelos_{book.lower()}.json")
    
    print("=== Download de Todas as Versões Antigas Concluído! ===")

if __name__ == "__main__":
    main()
