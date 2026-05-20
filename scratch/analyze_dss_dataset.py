import urllib.request
import csv
import io
from collections import Counter

url = "https://huggingface.co/datasets/yonatanlou/QumranDataset/resolve/main/dss_chunk_size_100_overlap_15.csv"
print("Baixando base completa do QumranDataset para análise local...")

try:
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8")
        
        f = io.StringIO(content)
        reader = csv.reader(f)
        header = next(reader)
        
        # Colunas: book, sentence_path, text_lex, text, n_words, bib, section, composition, genre
        book_col_idx = header.index('book')
        bib_col_idx = header.index('bib')
        section_col_idx = header.index('section')
        
        books = []
        bib_types = []
        sections = []
        total_rows = 0
        
        for row in reader:
            if not row:
                continue
            total_rows += 1
            books.append(row[book_col_idx])
            bib_types.append(row[bib_col_idx])
            sections.append(row[section_col_idx])
            
        print(f"Sucesso! Total de registros (chunks): {total_rows}")
        
        print("\nDivisão por tipo (bib vs nonbib):")
        for k, v in Counter(bib_types).items():
            print(f"  {k}: {v} chunks ({v/total_rows*100:.1f}%)")
            
        print("\nDivisão por Seção:")
        for k, v in Counter(sections).items():
            print(f"  {k}: {v} chunks")
            
        print("\nOs 30 Livros/Pergaminhos mais frequentes na base:")
        for k, v in Counter(books).most_common(30):
            print(f"  {k}: {v} chunks")
            
except Exception as e:
    print(f"Erro: {e}")
