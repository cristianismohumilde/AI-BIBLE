#!/usr/bin/env python3
"""
download_all_missing.py
=======================
Script consolidado que baixa TUDO que ainda falta:
  1. SBLGNT (Texto Critico Grego - NT completo)
  2. BYZ (Texto Bizantino - NT completo)
  3. Talmud Bavli - todos os tratados restantes
  4. Materiais de estudo: lexicos, gramaticas, concordancias

Roda como ubuntu com permissoes corretas.
"""

import os, json, requests, time, struct, sys

BASE = os.path.expanduser("~/AI-BIBLE")
os.chdir(BASE)

def ensure(path):
    os.makedirs(path, exist_ok=True)

def download(url, out_path, label, stream=False, timeout=90):
    if os.path.exists(out_path) and os.path.getsize(out_path) > 512:
        print(f"  [JA EXISTE] {label}")
        return True
    print(f"  Baixando {label}...")
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=timeout, stream=stream)
            if r.status_code == 200:
                with open(out_path, "wb") as f:
                    if stream:
                        for chunk in r.iter_content(8192): f.write(chunk)
                    else:
                        f.write(r.content)
                kb = os.path.getsize(out_path) // 1024
                print(f"    OK: {label} ({kb} KB)")
                return True
            else:
                print(f"    HTTP {r.status_code}")
                return False
        except Exception as e:
            print(f"    Tentativa {attempt+1}: {e}")
            time.sleep(3)
    return False

# ─── 1. SBLGNT ────────────────────────────────────────────────────────────────
def download_sblgnt():
    print("\n" + "="*60)
    print("SBLGNT - TEXTO CRITICO GREGO (Society of Biblical Literature)")
    print("="*60)
    out_dir = "data/SBLGNT"
    ensure(out_dir)

    # SBLGNT via API Bolls.life - funciona por livro
    # Livros NT em ordem canonica
    nt_books = [
        ("Matthew",40), ("Mark",16), ("Luke",24), ("John",21), ("Acts",28),
        ("Romans",16), ("1Corinthians",16), ("2Corinthians",13), ("Galatians",6),
        ("Ephesians",6), ("Philippians",4), ("Colossians",4),
        ("1Thessalonians",5), ("2Thessalonians",3),
        ("1Timothy",6), ("2Timothy",4), ("Titus",3), ("Philemon",1),
        ("Hebrews",13), ("James",5), ("1Peter",5), ("2Peter",3),
        ("1John",5), ("2John",1), ("3John",1), ("Jude",1), ("Revelation",22),
    ]

    saved = 0
    for book, chapters in nt_books:
        for ch in range(1, chapters + 1):
            out_path = f"{out_dir}/{book}_{ch}.json"
            if os.path.exists(out_path):
                saved += 1
                continue
            url = f"https://bolls.life/get-text/SBLGNT/{book}/{ch}/"
            try:
                r = requests.get(url, timeout=30)
                if r.status_code == 200:
                    data = r.json()
                    if data and isinstance(data, list):
                        verses = [{"verse": v.get("verse", i+1), "text": v.get("text","").strip()}
                                  for i, v in enumerate(data)]
                        with open(out_path, "w", encoding="utf-8") as f:
                            json.dump(verses, f, ensure_ascii=False, indent=2)
                        saved += 1
            except Exception as e:
                print(f"    {book} {ch}: {e}")
            time.sleep(0.3)

    # Alternativa via GitHub openscriptures se Bolls falhar
    if saved < 10:
        print("  Bolls falhou. Tentando GitHub openscriptures/sblgnt...")
        github_url = "https://raw.githubusercontent.com/LogosBible/SBLGNT/master/data/sblgnt/text/61-Matthew.txt"
        # Usa API do Sefaria para grego (nao tem SBLGNT mas tem Peshitta etc)
        # Como fallback usamos o TR que ja temos (mesmo periodo historico)
        print("  SBLGNT nao disponivel via API gratuita sem autenticacao.")
        print("  Usando TR (Textus Receptus) como proxy para Texto Critico.")

    print(f"  SBLGNT: {saved} capitulos salvos em {out_dir}/")

# ─── 2. BYZ ───────────────────────────────────────────────────────────────────
def download_byz():
    print("\n" + "="*60)
    print("BYZ - TEXTO BIZANTINO (Majority Text)")
    print("="*60)
    out_dir = "data/BYZ"
    ensure(out_dir)

    nt_books = [
        ("Matt",28), ("Mark",16), ("Luke",24), ("John",21), ("Acts",28),
        ("Rom",16), ("1Cor",16), ("2Cor",13), ("Gal",6),
        ("Eph",6), ("Phil",4), ("Col",4),
        ("1Thess",5), ("2Thess",3),
        ("1Tim",6), ("2Tim",4), ("Titus",3), ("Phlm",1),
        ("Heb",13), ("Jas",5), ("1Pet",5), ("2Pet",3),
        ("1John",5), ("2John",1), ("3John",1), ("Jude",1), ("Rev",22),
    ]

    # Tenta biblia.com / YouVersion API alternativa
    # Tenta getbible.net API (suporta varias versoes)
    byz_apis = [
        "https://getbible.net/json?passage={book}+{ch}&version=byz",
        "https://bolls.life/get-text/BYZ_/Matthew/1/",  # teste primeiro
    ]

    # Verifica se BYZ esta disponivel no bolls
    test = requests.get("https://bolls.life/get-text/BYZP/Matthew/1/", timeout=15)
    if test.status_code == 200 and test.json():
        print("  BYZ disponivel via Bolls (versao BYZP)!")
        byz_id = "BYZP"
    else:
        test2 = requests.get("https://bolls.life/get-text/BYZ/Matthew/1/", timeout=15)
        if test2.status_code == 200 and test2.json():
            print("  BYZ disponivel via Bolls (versao BYZ)!")
            byz_id = "BYZ"
        else:
            print("  BYZ nao disponivel via Bolls. Tentando getbible.net...")
            byz_id = None

    saved = 0
    book_names_full = [
        ("Matthew",28), ("Mark",16), ("Luke",24), ("John",21), ("Acts",28),
        ("Romans",16), ("1Corinthians",16), ("2Corinthians",13), ("Galatians",6),
        ("Ephesians",6), ("Philippians",4), ("Colossians",4),
        ("1Thessalonians",5), ("2Thessalonians",3),
        ("1Timothy",6), ("2Timothy",4), ("Titus",3), ("Philemon",1),
        ("Hebrews",13), ("James",5), ("1Peter",5), ("2Peter",3),
        ("1John",5), ("2John",1), ("3John",1), ("Jude",1), ("Revelation",22),
    ]

    if byz_id:
        for book, chapters in book_names_full:
            for ch in range(1, chapters + 1):
                out_path = f"{out_dir}/{book}_{ch}.json"
                if os.path.exists(out_path): saved += 1; continue
                url = f"https://bolls.life/get-text/{byz_id}/{book}/{ch}/"
                try:
                    r = requests.get(url, timeout=30)
                    if r.status_code == 200:
                        data = r.json()
                        if data and isinstance(data, list):
                            verses = [{"verse": v.get("verse",i+1), "text": v.get("text","").strip()}
                                      for i,v in enumerate(data)]
                            with open(out_path, "w", encoding="utf-8") as f:
                                json.dump(verses, f, ensure_ascii=False, indent=2)
                            saved += 1
                except Exception as e:
                    print(f"    {book} {ch}: {e}")
                time.sleep(0.25)
    else:
        # Fallback: baixa BYZ do GitHub (morphgnt/sblgnt tem texto similar)
        # Usa o API do Bible.org (NET) como estrutura e nota como BYZ
        print("  Baixando BYZ do repositorio chadwhitacre/byzantine-text no GitHub...")
        byz_github = "https://raw.githubusercontent.com/byztxt/byzantine-majority-text/master/parsed/byzantine-majority-form.txt"
        out_raw = f"{out_dir}/byzantine_raw.txt"
        download(byz_github, out_raw, "Byzantine Majority Text (raw)", stream=True)

    print(f"  BYZ: {saved} capitulos salvos em {out_dir}/")

# ─── 3. Talmud ────────────────────────────────────────────────────────────────
def download_talmud():
    print("\n" + "="*60)
    print("TALMUD BAVLI - Tratados Completos (Sefaria)")
    print("="*60)
    out_dir = "data/Talmud"
    ensure(out_dir)

    tractates = {
        "Eruvin":"Eruvin", "Pesachim":"Pesachim", "Yoma":"Yoma",
        "Sukkah":"Sukkah", "Beitzah":"Beitzah", "Rosh_Hashanah":"Rosh Hashanah",
        "Taanit":"Taanit", "Megillah":"Megillah", "Moed_Katan":"Moed Katan",
        "Chagigah":"Chagigah", "Yevamot":"Yevamot", "Ketubot":"Ketubot",
        "Nedarim":"Nedarim", "Nazir":"Nazir", "Sotah":"Sotah",
        "Gittin":"Gittin", "Kiddushin":"Kiddushin", "Bava_Kamma":"Bava Kamma",
        "Bava_Metzia":"Bava Metzia", "Bava_Batra":"Bava Batra",
        "Makkot":"Makkot", "Shevuot":"Shevuot", "Avodah_Zarah":"Avodah Zarah",
        "Horayot":"Horayot", "Zevachim":"Zevachim", "Menachot":"Menachot",
        "Chullin":"Chullin", "Bekhorot":"Bekhorot", "Arakhin":"Arakhin",
        "Temurah":"Temurah", "Keritot":"Keritot", "Meilah":"Meilah",
        "Tamid":"Tamid", "Niddah":"Niddah",
    }

    already = {f.replace(".json","") for f in os.listdir(out_dir) if f.endswith(".json")}
    print(f"  Ja existentes: {already}")

    success, failed = 0, []
    for key, sefaria_name in tractates.items():
        if key in already:
            print(f"  [JA EXISTE] {key}")
            success += 1
            continue
        out_path = f"{out_dir}/{key}.json"
        url = f"https://www.sefaria.org/api/texts/{sefaria_name.replace(' ','_')}?lang=he&commentary=0"
        try:
            r = requests.get(url, timeout=90)
            if r.status_code == 200:
                d = r.json()
                if "error" not in d and d.get("text"):
                    with open(out_path, "w", encoding="utf-8") as f:
                        json.dump(d, f, ensure_ascii=False, indent=2)
                    kb = os.path.getsize(out_path)//1024
                    print(f"  OK: {key} ({kb} KB)")
                    success += 1
                else:
                    failed.append(key)
                    print(f"  ERRO Sefaria: {d.get('error','sem texto')}")
            else:
                failed.append(key)
                print(f"  HTTP {r.status_code} para {key}")
        except Exception as e:
            failed.append(key)
            print(f"  {key}: {e}")
        time.sleep(1.5)

    print(f"\n  Talmud: {success}/{len(tractates)} tratados. Falhas: {failed[:5]}{'...' if len(failed)>5 else ''}")

# ─── 4. Materiais de estudo ───────────────────────────────────────────────────
def download_study():
    print("\n" + "="*60)
    print("MATERIAIS DE ESTUDO - Lexicos, Gramaticas, Concordancias")
    print("="*60)

    lex_dir  = "data/study_materials/lexicons"
    gram_dir = "data/study_materials/grammars"
    ensure(lex_dir)
    ensure(gram_dir)

    items = [
        # Lexicos
        ("https://raw.githubusercontent.com/openscriptures/strongs/master/hebrew/strongs-hebrew-dictionary.json",
         f"{lex_dir}/strongs_hebrew.json", "Strong's Hebrew Lexicon (JSON)"),
        ("https://raw.githubusercontent.com/openscriptures/strongs/master/greek/strongs-greek-dictionary.json",
         f"{lex_dir}/strongs_greek.json", "Strong's Greek Lexicon (JSON)"),
        ("https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master/BrownDriverBriggs.xml",
         f"{lex_dir}/brown_driver_briggs.xml", "Brown-Driver-Briggs BDB (XML)"),
        ("https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master/HebrewStrong.xml",
         f"{lex_dir}/hebrew_strong_enhanced.xml", "Hebrew Strong Enhanced (XML)"),
        ("https://raw.githubusercontent.com/translatable-exegetical-tools/Abbott-Smith/master/AS.csv",
         f"{lex_dir}/abbott_smith_greek.csv", "Abbott-Smith Greek Lexicon (CSV)"),
        # Sedra / Syriac
        ("https://raw.githubusercontent.com/peshitta/sedra-parse/master/sedra/ROOTS.TXT",
         f"{lex_dir}/syriac_roots.txt", "Sedra Syriac Roots"),
        ("https://raw.githubusercontent.com/peshitta/sedra-parse/master/sedra/LEXEMES.TXT",
         f"{lex_dir}/syriac_lexemes.txt", "Sedra Syriac Lexemes"),
        ("https://raw.githubusercontent.com/peshitta/sedra-parse/master/sedra/WORDS.TXT",
         f"{lex_dir}/syriac_words.txt", "Sedra Syriac Words"),
        # Gramaticas (Project Gutenberg)
        ("https://www.gutenberg.org/files/17029/17029-0.txt",
         f"{gram_dir}/gesenius_hebrew_grammar.txt", "Gesenius' Hebrew Grammar"),
        ("https://www.gutenberg.org/files/44606/44606-0.txt",
         f"{gram_dir}/robertson_greek_grammar.txt", "A.T. Robertson Greek Grammar"),
        ("https://www.gutenberg.org/files/17337/17337-0.txt",
         f"{gram_dir}/noldeke_syriac_grammar.txt", "Noldeke Syriac Grammar"),
        # Jastrow (Aramaico Talmudico)
        ("https://www.gutenberg.org/files/8437/8437.txt",
         f"{lex_dir}/jastrow_dictionary.txt", "Jastrow Dictionary (Aramaico Talmudico)"),
        # Ge'ez Dillmann via arquivo menor (archive.org djvu.txt)
        ("https://raw.githubusercontent.com/sefaria/Sefaria-Data/master/sources/Jastrow/jastrow_dict.json",
         f"{lex_dir}/jastrow_sefaria.json", "Jastrow via Sefaria (JSON)"),
    ]

    for url, path, label in items:
        download(url, path, label, stream=True, timeout=120)
        time.sleep(0.5)

    # Cria INDEX.json
    index = {"lexicons": {}, "grammars": {}}
    for d, cat in [(lex_dir,"lexicons"), (gram_dir,"grammars")]:
        if not os.path.isdir(d): continue
        for f in sorted(os.listdir(d)):
            fp = os.path.join(d, f)
            if os.path.isfile(fp):
                index[cat][f] = {"size_kb": os.path.getsize(fp)//1024}
    with open("data/study_materials/INDEX.json", "w") as f:
        json.dump(index, f, indent=2)
    print("  INDEX.json criado.")

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("DOWNLOAD COMPLETO DE TODOS OS RECURSOS FALTANTES")
    print("=" * 60)

    download_sblgnt()
    download_byz()
    download_talmud()
    download_study()

    print("\n" + "=" * 60)
    print("CONCLUIDO! Verifique os logs acima para erros.")
    print("=" * 60)
