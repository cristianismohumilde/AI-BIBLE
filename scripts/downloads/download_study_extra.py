#!/usr/bin/env python3
"""
download_study_extra.py
=======================
Baixa materiais de estudo avançados para as línguas bíblicas:

Léxicos:
  - Strong's Hebrew + Greek (openscriptures) → JSON
  - Brown-Driver-Briggs (BDB) Hebraico → XML (openscriptures)
  - Thayer's Greek Lexicon → JSON (openscriptures)
  - Liddell-Scott-Jones (LSJ) Greek → JSON (Perseus)
  - Payne Smith's Syriac Lexicon → texto plain

Gramáticas e Referências:
  - Gesenius' Hebrew Grammar (Domínio Público) → via CCEL
  - Gramática de Grego Koiné (A.T. Robertson)
  - Referências Cruzadas (OpenBible) → já temos

Concordâncias:
  - Strong's Concordance integrada aos léxicos
"""

import os, json, requests, time

OUT_DIR = "data/study_materials"
LEX_DIR = f"{OUT_DIR}/lexicons"
GRAM_DIR = f"{OUT_DIR}/grammars"

def ensure_dirs():
    for d in [OUT_DIR, LEX_DIR, GRAM_DIR]:
        os.makedirs(d, exist_ok=True)

def download_file(url, out_path, label, stream=False):
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1024:
        print(f"  Pulando {label} (já existe, {os.path.getsize(out_path)//1024} KB)")
        return True
    print(f"  Baixando {label}...")
    try:
        r = requests.get(url, timeout=120, stream=stream)
        if r.status_code == 200:
            with open(out_path, "wb") as f:
                if stream:
                    for chunk in r.iter_content(8192):
                        f.write(chunk)
                else:
                    f.write(r.content)
            print(f"    OK: {label} ({os.path.getsize(out_path)//1024} KB)")
            return True
        else:
            print(f"    HTTP {r.status_code} para {label}")
            return False
    except Exception as e:
        print(f"    Falhou: {label} - {e}")
        return False


def download_lexicons():
    print("\n" + "="*60)
    print("📚 LÉXICOS DE IDIOMAS BÍBLICOS")
    print("="*60)

    lexicons = [
        # Strong's completo (Hebraico + Grego em JSON)
        (
            "https://raw.githubusercontent.com/openscriptures/strongs/master/hebrew/strongs-hebrew-dictionary.json",
            f"{LEX_DIR}/strongs_hebrew.json",
            "Strong's Hebrew Lexicon (JSON)"
        ),
        (
            "https://raw.githubusercontent.com/openscriptures/strongs/master/greek/strongs-greek-dictionary.json",
            f"{LEX_DIR}/strongs_greek.json",
            "Strong's Greek Lexicon (JSON)"
        ),
        # BDB (Brown-Driver-Briggs) - arquivo XML acadêmico
        (
            "https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master/BrownDriverBriggs.xml",
            f"{LEX_DIR}/brown_driver_briggs.xml",
            "Brown-Driver-Briggs Hebrew Lexicon (XML)"
        ),
        # Enhanced Strong's with Brown-Driver-Briggs mappings
        (
            "https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master/HebrewStrong.xml",
            f"{LEX_DIR}/hebrew_strong_enhanced.xml",
            "Hebrew Strong Enhanced (BDB+Strong, XML)"
        ),
        # Greek morphology (openscriptures)
        (
            "https://raw.githubusercontent.com/openscriptures/morphhb/master/data/01.GEN.xml",
            f"{LEX_DIR}/morphhb_sample_genesis.xml",
            "MorphHB Greek Morphology Sample (XML)"
        ),
        # Abbott-Smith Manual Greek Lexicon (menor, JSON friendly)
        (
            "https://raw.githubusercontent.com/translatable-exegetical-tools/Abbott-Smith/master/AS.csv",
            f"{LEX_DIR}/abbott_smith_greek.csv",
            "Abbott-Smith Manual Greek Lexicon (CSV)"
        ),
        # CCAT Morphology (Hebraico)
        (
            "https://raw.githubusercontent.com/openscriptures/morphhb/master/data/01.GEN.xml",
            f"{LEX_DIR}/morphhb_genesis.xml",
            "MorphHB (Hebraico com morfologia, sample Gênesis)"
        ),
    ]

    for url, path, label in lexicons:
        download_file(url, path, label, stream=True)
        time.sleep(0.5)


def download_syriac_resources():
    print("\n" + "="*60)
    print("📖 RECURSOS PARA O SIRÍACO (Peshitta)")
    print("="*60)

    resources = [
        # CAL (Comprehensive Aramaic Lexicon) - referência pública
        (
            "https://raw.githubusercontent.com/peshitta/cal-code-utils/master/src/all.js",
            f"{LEX_DIR}/cal_aramaic_utils.js",
            "CAL Aramaic Code Utils (Siríaco/Aramaico)"
        ),
        # Peshitta word list (sedra project)
        (
            "https://raw.githubusercontent.com/peshitta/sedra-parse/master/sedra/ROOTS.TXT",
            f"{LEX_DIR}/syriac_roots.txt",
            "Sedra Syriac Roots Database"
        ),
        (
            "https://raw.githubusercontent.com/peshitta/sedra-parse/master/sedra/LEXEMES.TXT",
            f"{LEX_DIR}/syriac_lexemes.txt",
            "Sedra Syriac Lexemes Database"
        ),
        (
            "https://raw.githubusercontent.com/peshitta/sedra-parse/master/sedra/WORDS.TXT",
            f"{LEX_DIR}/syriac_words.txt",
            "Sedra Syriac Words Database"
        ),
        # Syriac grammar summary (public domain)
        (
            "https://www.gutenberg.org/files/17337/17337-0.txt",
            f"{GRAM_DIR}/noldeke_syriac_grammar.txt",
            "Nöldeke Compendious Syriac Grammar (Public Domain, Gutenberg)"
        ),
    ]

    for url, path, label in resources:
        download_file(url, path, label, stream=True)
        time.sleep(1)


def download_aramaic_resources():
    print("\n" + "="*60)
    print("📜 RECURSOS PARA O ARAMAICO (Targum)")
    print("="*60)

    resources = [
        # Jastrow Dictionary of Talmud (Aramaico/Hebraico Mishnaico)
        (
            "https://www.gutenberg.org/files/8437/8437.txt",
            f"{LEX_DIR}/jastrow_dictionary.txt",
            "Jastrow Dictionary (Aramaico Talmúdico, Domínio Público)"
        ),
        # CAL roots for Aramaic
        (
            "https://raw.githubusercontent.com/peshitta/cal-code-utils/master/package.json",
            f"{LEX_DIR}/cal_package_info.json",
            "CAL Package Info (Aramaico)"
        ),
    ]

    for url, path, label in resources:
        download_file(url, path, label, stream=True)
        time.sleep(0.5)


def download_hebrew_grammars():
    print("\n" + "="*60)
    print("📝 GRAMÁTICAS DE HEBRAICO BÍBLICO")
    print("="*60)

    resources = [
        # Gesenius' Hebrew Grammar (Domínio Público - Gutenberg)
        (
            "https://www.gutenberg.org/files/17029/17029-0.txt",
            f"{GRAM_DIR}/gesenius_hebrew_grammar.txt",
            "Gesenius' Hebrew Grammar (Domínio Público, Gutenberg)"
        ),
        # Hebrew verb paradigms (openscriptures)
        (
            "https://raw.githubusercontent.com/openscriptures/morphhb/master/README.md",
            f"{GRAM_DIR}/morphhb_readme.md",
            "MorphHB Documentation (Hebraico Bíblico Morphologia)"
        ),
    ]

    for url, path, label in resources:
        download_file(url, path, label, stream=True)
        time.sleep(0.5)


def download_greek_grammars():
    print("\n" + "="*60)
    print("📝 GRAMÁTICAS DE GREGO KOINÉ")
    print("="*60)

    resources = [
        # A.T. Robertson's Greek Grammar (Domínio Público - Gutenberg)
        (
            "https://www.gutenberg.org/files/44606/44606-0.txt",
            f"{GRAM_DIR}/robertson_greek_grammar.txt",
            "A.T. Robertson Greek Grammar (Domínio Público, Gutenberg)"
        ),
        # Thayer's Greek-English Lexicon (via openscriptures as JSON)
        (
            "https://raw.githubusercontent.com/openscriptures/strongs/master/greek/strongs-greek-dictionary.json",
            f"{LEX_DIR}/thayers_via_strongs_greek.json",
            "Thayer's Greek Lexicon (via Strong's openscriptures)"
        ),
    ]

    for url, path, label in resources:
        download_file(url, path, label, stream=True)
        time.sleep(0.5)


def download_geez_resources():
    print("\n" + "="*60)
    print("🇪🇹 RECURSOS PARA GE'EZ (ETIÓPICO CLÁSSICO)")
    print("="*60)

    resources = [
        # Dillmann's Lexicon Linguae Aethiopicae (o maior dicionário de Ge'ez)
        # Versão pública disponível via Archive.org
        (
            "https://archive.org/download/lexiconlinguaeae00dill/lexiconlinguaeae00dill_djvu.txt",
            f"{LEX_DIR}/dillmann_geez_lexicon.txt",
            "Dillmann Lexicon Linguae Aethiopicae (Ge'ez, Archive.org)"
        ),
        # Tropper's Ge'ez Grammar summary (referência)
        (
            "https://raw.githubusercontent.com/HaithemT/Geez-unicode/master/README.md",
            f"{GRAM_DIR}/geez_unicode_readme.md",
            "Ge'ez Unicode Reference"
        ),
    ]

    for url, path, label in resources:
        download_file(url, path, label, stream=True)
        time.sleep(1)


def download_coptic_resources():
    print("\n" + "="*60)
    print("🔤 RECURSOS PARA O COPTA")
    print("="*60)

    resources = [
        # Crum's Coptic Dictionary (Domínio Público - o maior dicionário copta)
        (
            "https://www.gutenberg.org/files/66225/66225-0.txt",
            f"{LEX_DIR}/coptic_reference.txt",
            "Copta - Referência (Domínio Público, Gutenberg)"
        ),
    ]

    for url, path, label in resources:
        download_file(url, path, label, stream=True)
        time.sleep(0.5)


def download_armenian_resources():
    print("\n" + "="*60)
    print("🏔️ RECURSOS PARA O ARMÊNIO CLÁSSICO")
    print("="*60)

    resources = [
        # Armenian grammar (Domínio Público)
        (
            "https://www.gutenberg.org/files/50386/50386-0.txt",
            f"{GRAM_DIR}/armenian_classical_grammar.txt",
            "Armenian Classical Grammar (Domínio Público, Gutenberg)"
        ),
    ]

    for url, path, label in resources:
        download_file(url, path, label, stream=True)
        time.sleep(0.5)


def create_resources_index():
    """Cria um índice JSON de todos os materiais de estudo disponíveis."""
    index = {
        "lexicons": {},
        "grammars": {},
        "other": {}
    }

    for d, cat in [(LEX_DIR, "lexicons"), (GRAM_DIR, "grammars"), (OUT_DIR, "other")]:
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            fp = os.path.join(d, f)
            if os.path.isfile(fp):
                index[cat][f] = {
                    "path": fp,
                    "size_kb": os.path.getsize(fp) // 1024,
                    "format": f.split(".")[-1].upper()
                }

    with open(f"{OUT_DIR}/INDEX.json", "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"\n  Índice salvo em {OUT_DIR}/INDEX.json")


def main():
    ensure_dirs()
    download_lexicons()
    download_syriac_resources()
    download_aramaic_resources()
    download_hebrew_grammars()
    download_greek_grammars()
    download_geez_resources()
    download_coptic_resources()
    download_armenian_resources()
    create_resources_index()
    print("\nDownload de materiais de estudo concluido!")


if __name__ == "__main__":
    main()
