import urllib.request
import csv
import io

def main():
    url = "https://huggingface.co/datasets/yonatanlou/QumranDataset/resolve/main/dss_chunk_size_100_overlap_15.csv"
    print("Baixando base para analisar mapeamentos bíblicos...")
    
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode("utf-8")
            
            f = io.StringIO(content)
            reader = csv.reader(f)
            header = next(reader)
            
            book_idx = header.index('book')
            bib_idx = header.index('bib')
            comp_idx = header.index('composition')
            text_idx = header.index('text')
            
            mapped = {}
            for row in reader:
                if not row:
                    continue
                if row[bib_idx] == "bib":
                    b = row[book_idx]
                    c = row[comp_idx]
                    t = row[text_idx]
                    
                    if (b, c) not in mapped:
                        mapped[(b, c)] = []
                    mapped[(b, c)].append(t)
            
            print(f"Total de combinações (book, composition): {len(mapped)}")
            
            # Print those with empty composition
            empty_comp = {k: v for k, v in mapped.items() if k[1] == ""}
            print(f"\nCombinações com composition vazia (total: {len(empty_comp)}):")
            for (b, c), texts in empty_comp.items():
                print(f"  Scroll: {b} | Chunks: {len(texts)} | Sample text: {texts[0][:150]}...")
                
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
