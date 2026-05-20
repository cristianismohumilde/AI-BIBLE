import urllib.request
import csv
import io

url = "https://huggingface.co/datasets/yonatanlou/QumranDataset/resolve/main/dss_chunk_size_100_overlap_15.csv"
print("Baixando primeiras linhas do CSV usando bibliotecas padrão...")

req = urllib.request.Request(url, headers={"Range": "bytes=0-10240"})
try:
    with urllib.request.urlopen(req) as response:
        content = response.read().decode("utf-8")
        last_newline = content.rfind("\n")
        if last_newline != -1:
            content = content[:last_newline]
        
        f = io.StringIO(content)
        reader = csv.reader(f)
        header = next(reader)
        print("Colunas encontradas:")
        print(header)
        
        print("\nPrimeiras 3 linhas:")
        count = 0
        for row in reader:
            print(f"Row {count+1}:")
            for col, val in zip(header, row):
                # Truncate values for cleaner output
                print(f"  {col}: {val[:100]}..." if len(val) > 100 else f"  {col}: {val}")
            count += 1
            if count >= 3:
                break
except Exception as e:
    print(f"Erro: {e}")
