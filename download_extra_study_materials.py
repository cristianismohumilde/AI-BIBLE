import os
import requests
import zipfile
import io

def main():
    print("=== Iniciando Download de Referências Cruzadas (OpenBible TSK) ===")
    
    dest_dir = "data/study_materials"
    os.makedirs(dest_dir, exist_ok=True)
    
    # URL oficial do arquivo compactado de referências cruzadas do OpenBible
    url = "https://a.openbible.info/data/cross-references.zip"
    
    print(f"Baixando {url}...")
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            print("Download concluído! Descompactando em memória...")
            # Descompactar em memória
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                # O arquivo zip contém um arquivo 'cross_references.txt' que é um TSV
                file_list = z.namelist()
                print("Arquivos encontrados no ZIP:", file_list)
                for file_name in file_list:
                    if file_name.endswith(".txt") or file_name.endswith(".tsv") or "cross_references" in file_name:
                        target_path = os.path.join(dest_dir, "cross_references.tsv")
                        with open(target_path, "wb") as f:
                            f.write(z.read(file_name))
                        print(f"Arquivo extraído e salvo com sucesso em: {target_path}")
                        break
        else:
            print(f"Erro {response.status_code} ao baixar o arquivo.")
    except Exception as e:
        print(f"Exceção ao fazer download/extração: {e}")

    print("=== Processo Concluído! ===")

if __name__ == "__main__":
    main()
