import urllib.request
import csv
import io

url = "https://huggingface.co/datasets/yonatanlou/QumranDataset/resolve/main/qumran_labels.csv"
print("Baixando primeiras linhas do qumran_labels.csv...")

try:
    req = urllib.request.Request(url, headers={"Range": "bytes=0-10240"})
    with urllib.request.urlopen(req) as response:
        content = response.read().decode("utf-8")
        last_newline = content.rfind("\n")
        if last_newline != -1:
            content = content[:last_newline]
        
        f = io.StringIO(content)
        reader = csv.reader(f)
        header = next(reader)
        print("Colunas encontradas em qumran_labels.csv:")
        print(header)
        
        print("\nPrimeiras 5 linhas:")
        count = 0
        for row in reader:
            print(f"Row {count+1}: {row}")
            count += 1
            if count >= 5:
                break
except Exception as e:
    print(f"Erro: {e}")
