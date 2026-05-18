import requests

def main():
    print("=== Buscando Arquivos da Septuaginta (LXX/Grego) no scrollmapper ===")
    url = "https://api.github.com/repos/scrollmapper/bible_databases/git/trees/master?recursive=1"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            tree = data.get("tree", [])
            print(f"Total de arquivos na árvore: {len(tree)}")
            matches = []
            for item in tree:
                path = item.get("path", "")
                if any(x in path.lower() for x in ["lxx", "sept", "greek", "grk"]):
                    matches.append(path)
            
            print(f"\nArquivos gregos encontrados ({len(matches)}):")
            for m in matches:
                print(f"- {m}")
        else:
            print(f"Erro {r.status_code} ao buscar árvore")
    except Exception as e:
        print(f"Exceção ao buscar árvore: {e}")

if __name__ == "__main__":
    main()
