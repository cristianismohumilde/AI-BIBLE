import requests

def main():
    print("=== Buscando Caminho de Targum Onkelos em books.json ===")
    url = "https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/books.json"
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            data = r.json()
            books = data.get("books", [])
            print(f"Total de livros listados: {len(books)}")
            matches = []
            for b in books:
                title = b.get("title", "")
                if "Onkelos" in title or "Jonathan" in title:
                    matches.append({
                        "title": title,
                        "language": b.get("language"),
                        "json_url": b.get("json_url"),
                        "categories": b.get("categories")
                    })
            
            print(f"\nEncontrados {len(matches)} livros correspondentes:")
            for m in matches[:15]:  # print first 15 matches
                print(f"- Título: {m['title']}")
                print(f"  Idioma: {m['language']}")
                print(f"  Categorias: {m['categories']}")
                print(f"  URL JSON: {m['json_url']}")
                print("-" * 40)
        else:
            print(f"Erro {r.status_code} ao buscar books.json")
    except Exception as e:
        print(f"Exceção ao buscar books.json: {e}")

if __name__ == "__main__":
    main()
