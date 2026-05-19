#!/usr/bin/env python3
"""
download_apocrypha.py
=====================
Baixa os manuscritos apócrifos, históricos e da tradição para a pasta data/apocrypha.
Esses textos serão processados na Fase 4 (Expansão).

Livros incluídos:
- Livro de Enoque (Etiópico/Grego)
- Livro dos Jubileus (Etiópico)
- Didaquê (Grego)
- Testamento dos Doze Patriarcas (Grego)
"""

import os
import time
import requests
import json

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)

APOCRYPHA_DIR = "data/apocrypha"
os.makedirs(APOCRYPHA_DIR, exist_ok=True)

# URLs atualizadas para evitar bloqueios de login no Archive.org
TEXTS = [
    ("Livro de Enoque (R.H. Charles)", "https://www.gutenberg.org/cache/epub/43125/pg43125.txt", "enoch_charles_edition.txt"),
    ("Livro dos Jubileus", "https://archive.org/download/bookofjubileesor00char/bookofjubileesor00char.pdf", "jubilees_charles_edition.pdf"),
    ("Didaquê (O Ensino dos Doze)", "https://archive.org/download/didachetexttrans00alle/didachetexttrans00alle.pdf", "didache_greek.pdf"),
    ("Testamento dos Doze Patriarcas", "https://archive.org/download/testamentsoftwel00char/testamentsoftwel00char.pdf", "testaments_twelve_patriarchs.pdf"),
    ("Prayer of Manasseh", "https://www.sefaria.org/api/texts/Prayer_of_Manasseh?context=0", "prayer_of_manasseh.json"),
    ("Psalm 151", "https://www.sefaria.org/api/texts/Psalm_151?context=0", "psalm_151.json"),
    ("3/4 Maccabees + 4 Esdras (Charles vol. II)", "https://archive.org/stream/apocryphapseudep02char/apocryphapseudep02char_djvu.txt", "charles_apocrypha_vol2_djvu.txt"),
    ("4 Esdras (fallback Gutenberg)", "https://www.gutenberg.org/cache/epub/2435/pg2435.txt", "4_esdras_gutenberg.txt"),
    ("Mishná (Berakhot - Sefaria API)", "https://www.sefaria.org/api/texts/Mishnah_Berakhot.1?context=0", "mishnah_berakhot.json")
]

def download_all():
    print("\n" + "="*60)
    print("BAIXANDO MANUSCRITOS APÓCRIFOS E HISTÓRICOS (FASE 4)")
    print("="*60)

    for label, url, filename in TEXTS:
        out_path = os.path.join(APOCRYPHA_DIR, filename)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 1024:
            print(f"  [JA EXISTE] {label} -> {filename}")
            continue
        
        print(f"  Baixando {label}...")
        try:
            r = requests.get(url, timeout=120)
            if r.status_code == 200:
                with open(out_path, "wb") as f:
                    f.write(r.content)
                print(f"    OK: {filename} ({len(r.content)//1024} KB)")
            else:
                print(f"    Erro HTTP {r.status_code} para {url}")
        except Exception as e:
            print(f"    Falha na conexão: {e}")
        time.sleep(1)
        
    print("\nCONCLUIDO! Arquivos salvos em data/apocrypha/")

if __name__ == "__main__":
    download_all()
