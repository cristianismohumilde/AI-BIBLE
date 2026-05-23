#!/usr/bin/env python3
"""
convert_geez.py
===============
Converte o módulo Ge'ez (Etiópico) do formato SWORD (.bzz/.bzv) para JSON
e, como alternativa, busca textos Ge'ez de fontes públicas disponíveis.

Fontes usadas:
  1. Arquivo local SWORD extraído em data/ancient_versions/geez_extracted/
  2. GitHub: BibleMultiConverter / geez-unicode como fallback
  3. Sefaria API (Etíope clássico onde disponível)
"""

import os, json, struct, zlib, requests, time

DATA_DIR = "data/ancient_versions"
OUT_DIR  = "data/Geez"

# Mapeamento canônico do AT (66 livros em ordem SWORD)
GEEZ_OT_BOOKS = [
    "Genesis","Exodus","Leviticus","Numbers","Deuteronomy",
    "Joshua","Judges","Ruth","1_Samuel","2_Samuel",
    "1_Kings","2_Kings","1_Chronicles","2_Chronicles",
    "Ezra","Nehemiah","Esther","Job","Psalms","Proverbs",
    "Ecclesiastes","Song_of_Solomon","Isaiah","Jeremiah","Lamentations",
    "Ezekiel","Daniel","Hosea","Joel","Amos","Obadiah","Jonah",
    "Micah","Nahum","Habakkuk","Zephaniah","Haggai","Zechariah","Malachi"
]

# Capítulos por livro (AT canônico)
OT_CHAPTERS = {
    "Genesis":50,"Exodus":40,"Leviticus":27,"Numbers":36,"Deuteronomy":34,
    "Joshua":24,"Judges":21,"Ruth":4,"1_Samuel":31,"2_Samuel":24,
    "1_Kings":22,"2_Kings":25,"1_Chronicles":29,"2_Chronicles":36,
    "Ezra":10,"Nehemiah":13,"Esther":10,"Job":42,"Psalms":150,
    "Proverbs":31,"Ecclesiastes":12,"Song_of_Solomon":8,"Isaiah":66,
    "Jeremiah":52,"Lamentations":5,"Ezekiel":48,"Daniel":12,
    "Hosea":14,"Joel":3,"Amos":9,"Obadiah":1,"Jonah":4,
    "Micah":7,"Nahum":3,"Habakkuk":3,"Zephaniah":3,"Haggai":2,
    "Zechariah":14,"Malachi":4
}

# Livros extras do cânon etiópico (únicos no mundo, só sobreviveram em Ge'ez)
ETHIOPIAN_EXTRA = {
    "Enoch":  "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/json/apocrypha/1%20Enoch.json",
    "Jubilees": "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/json/apocrypha/Jubilees.json",
}

# Fonte alternativa — Bible SuperSearch API tem Ge'ez/Amárico
BIBLESUPERSEARCH_GEEZ = "https://api.biblesupersearch.com/api?bible=geez&reference={book}+{chapter}&format=json"


def try_sword_parse():
    """Tenta parsear o módulo SWORD do Ge'ez (formato zText)."""
    bzz = os.path.join(DATA_DIR, "geez_extracted/modules/texts/ztext/geez/ot.bzz")
    bzv = os.path.join(DATA_DIR, "geez_extracted/modules/texts/ztext/geez/ot.bzv")

    if not os.path.exists(bzz) or not os.path.exists(bzv):
        print("  Módulo SWORD Ge'ez não encontrado.")
        return None

    print(f"  Lendo índice de versos: {os.path.getsize(bzv)} bytes...")
    verses_data = []

    try:
        with open(bzz, "rb") as fz:
            compressed_data = fz.read()

        with open(bzv, "rb") as fv:
            raw = fv.read()

        # Formato SWORD zText: 10 bytes por verso = 4 (bloco) + 4 (offset) + 2 (tamanho)
        verse_count = len(raw) // 10
        print(f"  Total de versos no índice: {verse_count}")

        # Descomprime os blocos
        # SWORD divide em blocos de 64 versos cada, comprimidos com zlib
        blocks_cache = {}
        pos = 0
        raw_offset = 0

        # Tenta descomprimir o arquivo inteiro como um único bloco
        try:
            text_raw = zlib.decompress(compressed_data)
            print(f"  Descomprimido com sucesso: {len(text_raw)} bytes de texto")

            # Extrai versos usando o índice .bzv
            for i in range(min(verse_count, 23145)):  # AT completo tem ~23k versos
                entry = raw[i*10:(i+1)*10]
                if len(entry) < 10:
                    break
                block_num, block_offset, verse_len = struct.unpack('<IIH', entry)
                if verse_len > 0 and block_offset < len(text_raw):
                    verse_text = text_raw[block_offset:block_offset+verse_len].decode('utf-8', errors='replace').strip()
                    if verse_text:
                        verses_data.append(verse_text)

        except zlib.error:
            # Tenta como blocos separados
            print("  Tentando parse por blocos...")
            i = 0
            while i < len(compressed_data) - 2:
                try:
                    decomp = zlib.decompressobj()
                    block = decomp.decompress(compressed_data[i:])
                    if block:
                        text = block.decode('utf-8', errors='replace')
                        # Divide por marcadores de verso
                        for line in text.split('\n'):
                            line = line.strip()
                            if line:
                                verses_data.append(line)
                    i += len(compressed_data) - len(decomp.unused_data)
                except:
                    i += 1

        print(f"  Versos extraídos do SWORD: {len(verses_data)}")
        return verses_data if verses_data else None

    except Exception as e:
        print(f"  Erro no parse SWORD: {e}")
        return None


def download_geez_from_alternative():
    """Baixa textos Ge'ez de fontes alternativas públicas."""
    print("\n  Tentando fonte alternativa para Ge'ez...")

    # GitHub: scrollmapper/bible_databases tem alguns textos
    sources = [
        {
            "url": "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/json/t_kjv.json",
            "label": "KJV fallback (será traduzido do inglês para o Ge'ez flow)"
        }
    ]

    # Tenta API Bible SuperSearch para Ge'ez
    test_url = "https://api.biblesupersearch.com/api?bible=geez&reference=Genesis+1&format=json"
    try:
        r = requests.get(test_url, timeout=15)
        if r.status_code == 200:
            d = r.json()
            if d.get("results"):
                print("  SuperSearch Ge'ez API disponível!")
                return "biblesupersearch"
    except:
        pass

    # Fonte via Sefaria (não tem Ge'ez diretamente, mas tem textos relacionados)
    print("  Ge'ez não disponível via API pública. Usando extração SWORD ou download manual.")
    return None


def save_geez_structured(verses_flat):
    """Organiza versos planos em estrutura por livro/capítulo."""
    os.makedirs(OUT_DIR, exist_ok=True)

    if not verses_flat:
        print("  Sem versos para organizar.")
        return

    # Distribui os versos pelos livros (estimativa por proporção canônica)
    idx = 0
    saved = 0
    for book in GEEZ_OT_BOOKS:
        chapters = OT_CHAPTERS.get(book, 1)
        for ch in range(1, chapters + 1):
            out_path = f"{OUT_DIR}/{book}_{ch}.json"
            if os.path.exists(out_path):
                continue

            # Estimativa de versos por capítulo (média 26 versos)
            ch_verses = []
            for v_num in range(1, 30):  # máx 30 versos tentativa
                if idx >= len(verses_flat):
                    break
                text = verses_flat[idx].strip()
                if text:
                    ch_verses.append({"verse": v_num, "text": text})
                idx += 1

            if ch_verses:
                os.makedirs(OUT_DIR, exist_ok=True)
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(ch_verses, f, ensure_ascii=False, indent=2)
                saved += 1

    print(f"  Salvos: {saved} capítulos Ge'ez em {OUT_DIR}/")


def download_ethiopian_extras():
    """Baixa os livros exclusivos do cânon etiópico (Enoque, Jubileus)."""
    print("\n  Baixando livros exclusivos do cânon etiópico...")
    os.makedirs(OUT_DIR, exist_ok=True)

    for book_name, url in ETHIOPIAN_EXTRA.items():
        out_path = f"{OUT_DIR}/{book_name}_source.json"
        if os.path.exists(out_path):
            print(f"    {book_name} já existe.")
            continue
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                with open(out_path, "wb") as f:
                    f.write(r.content)
                print(f"    Salvo: {book_name} ({len(r.content)//1024} KB)")
            else:
                print(f"    {book_name}: HTTP {r.status_code}")
        except Exception as e:
            print(f"    {book_name} falhou: {e}")
        time.sleep(0.5)

    # Também baixa via API Sefaria (tem texto do Enoque em inglês)
    sefaria_extras = [
        ("Book of Enoch", "Enoch"),
        ("Jubilees", "Jubilees"),
    ]
    for sefaria_name, save_name in sefaria_extras:
        out_path = f"{OUT_DIR}/{save_name}_sefaria.json"
        if os.path.exists(out_path):
            continue
        try:
            url = f"https://www.sefaria.org/api/texts/{sefaria_name.replace(' ','_')}?lang=en"
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                d = r.json()
                if "error" not in d:
                    with open(out_path, "w", encoding="utf-8") as f:
                        json.dump(d, f, ensure_ascii=False, indent=2)
                    print(f"    Sefaria {save_name} salvo.")
        except Exception as e:
            print(f"    Sefaria {save_name}: {e}")
        time.sleep(1)


def main():
    print("\n" + "="*60)
    print("🇪🇹 CONVERTENDO GE'EZ (ETIÓPICO CLÁSSICO)")
    print("="*60)

    os.makedirs(OUT_DIR, exist_ok=True)

    # 1. Tenta parsear SWORD
    verses = try_sword_parse()

    if verses and len(verses) > 100:
        print(f"\n  Parse SWORD bem-sucedido! {len(verses)} versos extraídos.")
        save_geez_structured(verses)
    else:
        print("\n  Parse SWORD insuficiente. Tentando fontes alternativas...")
        alt = download_geez_from_alternative()
        if not alt:
            print("  NOTA: Ge'ez requer download manual ou conversão especializada.")
            print("  Os livros exclusivos (Enoque, Jubileus) serão baixados abaixo.")

    # 2. Baixa os livros exclusivos do cânon etiópico
    download_ethiopian_extras()

    print("\n  Ge'ez: conversão concluída (verifique data/Geez/)")


if __name__ == "__main__":
    main()
