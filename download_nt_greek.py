#!/usr/bin/env python3
"""
download_nt_greek.py
====================
Baixa SBLGNT e BYZ usando fontes alternativas que realmente funcionam.

SBLGNT: via API bolls.life com traducao alternativa como placeholder
        + download do arquivo raw do GitHub LogosBible/SBLGNT

BYZ: via arquivo completo do repositorio byztxt no GitHub
     (formato TXT, converte para JSON por livro/capitulo)
"""

import os, json, requests, time, re

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)

NT_BOOKS_CHAPTERS = [
    ("Matthew",28), ("Mark",16), ("Luke",24), ("John",21), ("Acts",28),
    ("Romans",16), ("1Corinthians",16), ("2Corinthians",13), ("Galatians",6),
    ("Ephesians",6), ("Philippians",4), ("Colossians",4),
    ("1Thessalonians",5), ("2Thessalonians",3),
    ("1Timothy",6), ("2Timothy",4), ("Titus",3), ("Philemon",1),
    ("Hebrews",13), ("James",5), ("1Peter",5), ("2Peter",3),
    ("1John",5), ("2John",1), ("3John",1), ("Jude",1), ("Revelation",22),
]

# Mapeamento nome → numero para BYZ (usa numeracao OSISbook)
BYZ_BOOK_MAP = {
    "Matthew":"MAT","Mark":"MRK","Luke":"LUK","John":"JHN","Acts":"ACT",
    "Romans":"ROM","1Corinthians":"1CO","2Corinthians":"2CO","Galatians":"GAL",
    "Ephesians":"EPH","Philippians":"PHP","Colossians":"COL",
    "1Thessalonians":"1TH","2Thessalonians":"2TH","1Timothy":"1TI","2Timothy":"2TI",
    "Titus":"TIT","Philemon":"PHM","Hebrews":"HEB","James":"JAS",
    "1Peter":"1PE","2Peter":"2PE","1John":"1JN","2John":"2JN","3John":"3JN",
    "Jude":"JUD","Revelation":"REV",
}


def download_sblgnt():
    """SBLGNT via api.getbible.net (suporta varios textos gregos)."""
    print("\n" + "="*60)
    print("SBLGNT - TEXTO CRITICO GREGO")
    print("="*60)
    out_dir = "data/SBLGNT"
    os.makedirs(out_dir, exist_ok=True)

    # Tenta bible-api.com (suporta SBLGNT como 'sblgnt')
    test = requests.get("https://bible-api.com/john+3:16?translation=SBLGNT", timeout=15)
    if test.status_code == 200 and "text" in test.json():
        print("  bible-api.com suporta SBLGNT!")
        api = "bible-api.com"
    else:
        api = None
        print("  bible-api.com nao tem SBLGNT.")

    # Alternativa: arquivo completo do GitHub LogosBible
    # O SBLGNT esta disponivel em formato OSIS XML no GitHub
    sblgnt_osis_url = "https://raw.githubusercontent.com/LogosBible/SBLGNT/master/data/sblgnt/text/sblgnt.txt"
    raw_path = f"{out_dir}/sblgnt_raw.txt"
    if not os.path.exists(raw_path) or os.path.getsize(raw_path) < 1000:
        print("  Baixando SBLGNT raw (LogosBible/SBLGNT GitHub)...")
        try:
            r = requests.get(sblgnt_osis_url, timeout=60)
            if r.status_code == 200:
                with open(raw_path, "wb") as f: f.write(r.content)
                print(f"    OK: {len(r.content)//1024} KB")
        except Exception as e:
            print(f"    Falhou: {e}")

    # Alternativa 2: morphgnt (Grego com morfologia, mesmo texto base que SBLGNT)
    print("  Tentando morphgnt (mesmo texto base do SBLGNT com morfologia)...")
    morphgnt_base = "https://raw.githubusercontent.com/morphgnt/sblgnt/master"
    # Os arquivos tem formato: 01-Matthew.txt, etc.
    morphgnt_books = [
        ("61-Mt-morphgnt","Matthew",28), ("62-Mk-morphgnt","Mark",16), ("63-Lk-morphgnt","Luke",24),
        ("64-Jn-morphgnt","John",21), ("65-Ac-morphgnt","Acts",28), ("66-Ro-morphgnt","Romans",16),
        ("67-1Co-morphgnt","1Corinthians",16), ("68-2Co-morphgnt","2Corinthians",13),
        ("69-Ga-morphgnt","Galatians",6), ("70-Eph-morphgnt","Ephesians",6),
        ("71-Php-morphgnt","Philippians",4), ("72-Col-morphgnt","Colossians",4),
        ("73-1Th-morphgnt","1Thessalonians",5), ("74-2Th-morphgnt","2Thessalonians",3),
        ("75-1Ti-morphgnt","1Timothy",6), ("76-2Ti-morphgnt","2Timothy",4),
        ("77-Tit-morphgnt","Titus",3), ("78-Phm-morphgnt","Philemon",1),
        ("79-Heb-morphgnt","Hebrews",13), ("80-Jas-morphgnt","James",5),
        ("81-1Pe-morphgnt","1Peter",5), ("82-2Pe-morphgnt","2Peter",3),
        ("83-1Jn-morphgnt","1John",5), ("84-2Jn-morphgnt","2John",1),
        ("85-3Jn-morphgnt","3John",1), ("86-Jud-morphgnt","Jude",1), ("87-Re-morphgnt","Revelation",22),
    ]

    saved = 0
    for code, book, chapters in morphgnt_books:
        book_file = f"{morphgnt_base}/{code}.txt"
        raw_book_path = f"{out_dir}/{book}_raw.txt"

        if not os.path.exists(raw_book_path) or os.path.getsize(raw_book_path) < 100:
            try:
                r = requests.get(book_file, timeout=30)
                if r.status_code == 200:
                    with open(raw_book_path, "wb") as f: f.write(r.content)
            except Exception as e:
                print(f"    {book}: {e}")
                continue
            time.sleep(0.3)

        # Parse o arquivo do morphgnt para JSON por capitulo
        # Formato: BBCCVV PPPP SSSS NNNNNNNNNN LLLLLLLL word normalized lemma
        if os.path.exists(raw_book_path) and os.path.getsize(raw_book_path) > 100:
            chapters_data = {}
            with open(raw_book_path, encoding="utf-8", errors="replace") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 6: continue
                    ref = parts[0]  # BBCCVV
                    if len(ref) >= 6:
                        ch = int(ref[2:4])
                        vv = int(ref[4:6])
                        word = parts[4] if len(parts) > 4 else ""  # palavra normalizada
                        if ch not in chapters_data:
                            chapters_data[ch] = {}
                        if vv not in chapters_data[ch]:
                            chapters_data[ch][vv] = []
                        chapters_data[ch][vv].append(word)

            for ch, verses in chapters_data.items():
                out_path = f"{out_dir}/{book}_{ch}.json"
                if os.path.exists(out_path): saved += 1; continue
                verse_list = []
                for vv in sorted(verses.keys()):
                    text = " ".join(verses[vv])
                    verse_list.append({"verse": vv, "text": text})
                if verse_list:
                    with open(out_path, "w", encoding="utf-8") as f:
                        json.dump(verse_list, f, ensure_ascii=False, indent=2)
                    saved += 1

    print(f"  SBLGNT/morphgnt: {saved} capitulos salvos em {out_dir}/")


def download_byz():
    """BYZ via repositório byztxt/byzantine-majority-text no GitHub."""
    print("\n" + "="*60)
    print("BYZ - TEXTO BIZANTINO (Majority Text)")
    print("="*60)
    out_dir = "data/BYZ"
    os.makedirs(out_dir, exist_ok=True)

    existing = {f for f in os.listdir(out_dir) if f.endswith(".json")}

    byztxt_base = "https://raw.githubusercontent.com/byztxt/byzantine-majority-text/master/csv-unicode/ccat/no-variants"

    byz_books = [
        ("MAT","Matthew",28), ("MAR","Mark",16), ("LUK","Luke",24), ("JOH","John",21),
        ("ACT","Acts",28), ("ROM","Romans",16), ("1CO","1Corinthians",16), ("2CO","2Corinthians",13),
        ("GAL","Galatians",6), ("EPH","Ephesians",6), ("PHP","Philippians",4), ("COL","Colossians",4),
        ("1TH","1Thessalonians",5), ("2TH","2Thessalonians",3), ("1TI","1Timothy",6), ("2TI","2Timothy",4),
        ("TIT","Titus",3), ("PHM","Philemon",1), ("HEB","Hebrews",13), ("JAM","James",5),
        ("1PE","1Peter",5), ("2PE","2Peter",3), ("1JO","1John",5), ("2JO","2John",1),
        ("3JO","3John",1), ("JUD","Jude",1), ("REV","Revelation",22),
    ]

    saved = 0
    import csv

    for filename, book, chapters in byz_books:
        url = f"{byztxt_base}/{filename}.csv"
        raw_path = f"{out_dir}/{book}_raw.csv"

        if not os.path.exists(raw_path) or os.path.getsize(raw_path) < 100:
            try:
                r = requests.get(url, timeout=30)
                if r.status_code == 200:
                    with open(raw_path, "wb") as f: f.write(r.content)
                    print(f"  OK: {book} raw ({len(r.content)//1024} KB)")
                else:
                    print(f"  {book}: HTTP {r.status_code} - {url}")
                    continue
            except Exception as e:
                print(f"  {book}: {e}")
                continue
            time.sleep(0.3)

        if os.path.exists(raw_path) and os.path.getsize(raw_path) > 100:
            chapters_data = {}
            with open(raw_path, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for row in reader:
                    if len(row) >= 3:
                        try:
                            ch = int(row[0])
                            vv = int(row[1])
                            text = row[2].strip()
                            if ch not in chapters_data:
                                chapters_data[ch] = {}
                            if text:
                                chapters_data[ch][vv] = text
                        except ValueError:
                            continue

            for ch, verses in chapters_data.items():
                out_path = f"{out_dir}/{book}_{ch}.json"
                if out_path.replace(out_dir+"/","") in existing:
                    saved += 1; continue
                verse_list = []
                for vv in sorted(verses.keys()):
                    verse_list.append({"verse": vv, "text": verses[vv]})
                if verse_list:
                    with open(out_path, "w", encoding="utf-8") as f:
                        json.dump(verse_list, f, ensure_ascii=False, indent=2)
                    saved += 1

    print(f"  BYZ: {saved} capitulos salvos em {out_dir}/")


def download_missing_study():
    """Baixa materiais de estudo que tiveram 404 na tentativa anterior."""
    print("\n" + "="*60)
    print("MATERIAIS DE ESTUDO - Fontes Corrigidas")
    print("="*60)

    lex_dir  = "data/study_materials/lexicons"
    gram_dir = "data/study_materials/grammars"
    os.makedirs(lex_dir, exist_ok=True)
    os.makedirs(gram_dir, exist_ok=True)

    items = [
        # Strong's via openscriptures (URLs corretas)
        ("https://raw.githubusercontent.com/openscriptures/strongs/master/hebrew/strongs-hebrew-dictionary.js",
         f"{lex_dir}/strongs_hebrew.json", "Strong's Hebrew"),
        ("https://raw.githubusercontent.com/openscriptures/strongs/master/greek/strongs-greek-dictionary.js",
         f"{lex_dir}/strongs_greek.json", "Strong's Greek"),
        # BDB via openscriptures HebrewLexicon
        ("https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master/BrownDriverBriggs.xml",
         f"{lex_dir}/brown_driver_briggs.xml", "BDB Hebraico"),
        ("https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master/HebrewStrong.xml",
         f"{lex_dir}/hebrew_strong_enhanced.xml", "Hebrew Strong Enhanced"),
        # Abbott-Smith via unicode repos
        ("https://raw.githubusercontent.com/morphgnt/abbott-smith/master/abbott-smith.tei.xml",
         f"{lex_dir}/abbott_smith_greek.xml", "Abbott-Smith Greek"),
        # Sedra Siríaco - repositório correto (agora no peshitta.org raw?)
        # Trocando sedra temporariamente por Jastrow que ja existe

        # Gesenius - Gutenberg URL correta
        ("https://www.gutenberg.org/cache/epub/17029/pg17029.txt",
         f"{gram_dir}/gesenius_hebrew_grammar.txt", "Gesenius Hebrew Grammar"),
        # Noldeke - Gutenberg
        ("https://www.gutenberg.org/cache/epub/17337/pg17337.txt",
         f"{gram_dir}/noldeke_syriac_grammar.txt", "Noldeke Syriac Grammar"),
        # Robertson Greek Grammar
        ("https://www.gutenberg.org/cache/epub/44606/pg44606.txt",
         f"{gram_dir}/robertson_greek_grammar.txt", "Robertson Greek Grammar"),
    ]

    for url, path, label in items:
        if os.path.exists(path) and os.path.getsize(path) > 512:
            print(f"  [JA EXISTE] {label} ({os.path.getsize(path)//1024} KB)")
            continue
        print(f"  Baixando {label}...")
        try:
            r = requests.get(url, timeout=120)
            if r.status_code == 200:
                with open(path, "wb") as f: f.write(r.content)
                print(f"    OK: {label} ({len(r.content)//1024} KB)")
            else:
                print(f"    HTTP {r.status_code}: {url}")
        except Exception as e:
            print(f"    Erro: {e}")
        time.sleep(0.5)

    # Recria INDEX
    index = {"lexicons":{}, "grammars":{}}
    for d, cat in [(lex_dir,"lexicons"), (gram_dir,"grammars")]:
        if not os.path.isdir(d): continue
        for fn in sorted(os.listdir(d)):
            fp = os.path.join(d, fn)
            if os.path.isfile(fp):
                index[cat][fn] = {"size_kb": os.path.getsize(fp)//1024}
    with open("data/study_materials/INDEX.json","w") as f:
        json.dump(index, f, indent=2)
    print("  INDEX.json atualizado.")


if __name__ == "__main__":
    print("="*60)
    print("BAIXANDO SBLGNT, BYZ E MATERIAIS DE ESTUDO")
    print("="*60)
    download_sblgnt()
    download_byz()
    download_missing_study()
    print("\nCONCLUIDO!")
