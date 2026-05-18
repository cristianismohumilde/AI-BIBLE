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

BASE = os.path.expanduser("~/AI-BIBLE")
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
        ("01-Matthew","Matthew",28), ("02-Mark","Mark",16), ("03-Luke","Luke",24),
        ("04-John","John",21), ("05-Acts","Acts",28), ("06-Romans","Romans",16),
        ("07-1Corinthians","1Corinthians",16), ("08-2Corinthians","2Corinthians",13),
        ("09-Galatians","Galatians",6), ("10-Ephesians","Ephesians",6),
        ("11-Philippians","Philippians",4), ("12-Colossians","Colossians",4),
        ("13-1Thessalonians","1Thessalonians",5), ("14-2Thessalonians","2Thessalonians",3),
        ("15-1Timothy","1Timothy",6), ("16-2Timothy","2Timothy",4),
        ("17-Titus","Titus",3), ("18-Philemon","Philemon",1),
        ("19-Hebrews","Hebrews",13), ("20-James","James",5),
        ("21-1Peter","1Peter",5), ("22-2Peter","2Peter",3),
        ("23-1John","1John",5), ("24-2John","2John",1),
        ("25-3John","3John",1), ("26-Jude","Jude",1), ("27-Revelation","Revelation",22),
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

    # byztxt no GitHub tem arquivos por livro em formato tabular
    byztxt_base = "https://raw.githubusercontent.com/byztxt/byzantine-majority-text/master/parsed"

    # Formato disponivel: arquivos .txt com referencia e texto
    byz_books = [
        ("B01___Matthew_Byzantine_Parsed.txt","Matthew",28),
        ("B02___Mark_Byzantine_Parsed.txt","Mark",16),
        ("B03___Luke_Byzantine_Parsed.txt","Luke",24),
        ("B04___John_Byzantine_Parsed.txt","John",21),
        ("B05___Acts_Byzantine_Parsed.txt","Acts",28),
        ("B06___Romans_Byzantine_Parsed.txt","Romans",16),
        ("B07___1Corinthians_Byzantine_Parsed.txt","1Corinthians",16),
        ("B08___2Corinthians_Byzantine_Parsed.txt","2Corinthians",13),
        ("B09___Galatians_Byzantine_Parsed.txt","Galatians",6),
        ("B10___Ephesians_Byzantine_Parsed.txt","Ephesians",6),
        ("B11___Philippians_Byzantine_Parsed.txt","Philippians",4),
        ("B12___Colossians_Byzantine_Parsed.txt","Colossians",4),
        ("B13___1Thessalonians_Byzantine_Parsed.txt","1Thessalonians",5),
        ("B14___2Thessalonians_Byzantine_Parsed.txt","2Thessalonians",3),
        ("B15___1Timothy_Byzantine_Parsed.txt","1Timothy",6),
        ("B16___2Timothy_Byzantine_Parsed.txt","2Timothy",4),
        ("B17___Titus_Byzantine_Parsed.txt","Titus",3),
        ("B18___Philemon_Byzantine_Parsed.txt","Philemon",1),
        ("B19___Hebrews_Byzantine_Parsed.txt","Hebrews",13),
        ("B20___James_Byzantine_Parsed.txt","James",5),
        ("B21___1Peter_Byzantine_Parsed.txt","1Peter",5),
        ("B22___2Peter_Byzantine_Parsed.txt","2Peter",3),
        ("B23___1John_Byzantine_Parsed.txt","1John",5),
        ("B24___2John_Byzantine_Parsed.txt","2John",1),
        ("B25___3John_Byzantine_Parsed.txt","3John",1),
        ("B26___Jude_Byzantine_Parsed.txt","Jude",1),
        ("B27___Revelation_Byzantine_Parsed.txt","Revelation",22),
    ]

    saved = 0
    for filename, book, chapters in byz_books:
        url = f"{byztxt_base}/{filename}"
        raw_path = f"{out_dir}/{book}_raw.txt"

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

        # Parse: cada linha tem referencia e forma da palavra
        # Formato tipico: MAT 1:1 BBBBCCCVVV word ...
        if os.path.exists(raw_path) and os.path.getsize(raw_path) > 100:
            chapters_data = {}
            with open(raw_path, encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"): continue
                    parts = line.split()
                    if len(parts) < 2: continue
                    # Tenta encontrar referencia no formato XXX 1:1 ou 1:1
                    ref_match = re.search(r'(\d+):(\d+)', line)
                    if ref_match:
                        ch = int(ref_match.group(1))
                        vv = int(ref_match.group(2))
                        # Pega a ultima coluna como a palavra grega
                        word = parts[-1] if parts else ""
                        if ch not in chapters_data:
                            chapters_data[ch] = {}
                        if vv not in chapters_data[ch]:
                            chapters_data[ch][vv] = []
                        if word and re.search(r'[\u0370-\u03ff\u1f00-\u1fff]', word):
                            chapters_data[ch][vv].append(word)

            for ch, verses in chapters_data.items():
                out_path = f"{out_dir}/{book}_{ch}.json"
                if out_path.replace(out_dir+"/","") in existing:
                    saved += 1; continue
                verse_list = []
                for vv in sorted(verses.keys()):
                    text = " ".join(verses[vv])
                    if text.strip():
                        verse_list.append({"verse": vv, "text": text})
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
        ("https://raw.githubusercontent.com/openscriptures/strongs/master/hebrew/strongs-hebrew-dictionary.json",
         f"{lex_dir}/strongs_hebrew.json", "Strong's Hebrew"),
        ("https://raw.githubusercontent.com/openscriptures/strongs/master/greek/strongs-greek-dictionary.json",
         f"{lex_dir}/strongs_greek.json", "Strong's Greek"),
        # BDB via openscriptures HebrewLexicon
        ("https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master/BrownDriverBriggs.xml",
         f"{lex_dir}/brown_driver_briggs.xml", "BDB Hebraico"),
        ("https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master/HebrewStrong.xml",
         f"{lex_dir}/hebrew_strong_enhanced.xml", "Hebrew Strong Enhanced"),
        # Abbott-Smith via translatable-exegetical-tools
        ("https://raw.githubusercontent.com/translatable-exegetical-tools/Abbott-Smith/master/AS.csv",
         f"{lex_dir}/abbott_smith_greek.csv", "Abbott-Smith Greek"),
        # Sedra Siríaco - repositório correto
        ("https://raw.githubusercontent.com/peshitta/sedra-db/master/sedra/ROOTS.TXT",
         f"{lex_dir}/syriac_roots.txt", "Sedra Syriac Roots"),
        ("https://raw.githubusercontent.com/peshitta/sedra-db/master/sedra/LEXEMES.TXT",
         f"{lex_dir}/syriac_lexemes.txt", "Sedra Syriac Lexemes"),
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
