import requests
import os
import json
import time

BOLLS_BOOKS = {
    # Old Testament
    1: "Genesis", 2: "Exodus", 3: "Leviticus", 4: "Numbers", 5: "Deuteronomy",
    6: "Joshua", 7: "Judges", 8: "Ruth", 9: "1_Samuel", 10: "2_Samuel",
    11: "1_Kings", 12: "2_Kings", 13: "1_Chronicles", 14: "2_Chronicles",
    15: "Ezra", 16: "Nehemiah", 17: "Esther", 18: "Job", 19: "Psalms",
    20: "Proverbs", 21: "Ecclesiastes", 22: "Song_of_Solomon", 23: "Isaiah",
    24: "Jeremiah", 25: "Lamentations", 26: "Ezekiel", 27: "Daniel",
    28: "Hosea", 29: "Joel", 30: "Amos", 31: "Obadiah", 32: "Jonah",
    33: "Micah", 34: "Nahum", 35: "Habakkuk", 36: "Zephaniah", 37: "Haggai",
    38: "Zechariah", 39: "Malachi",
    # New Testament
    40: "Matthew", 41: "Mark", 42: "Luke", 43: "John", 44: "Acts",
    45: "Romans", 46: "1_Corinthians", 47: "2_Corinthians", 48: "Galatians",
    49: "Ephesians", 50: "Philippians", 51: "Colossians", 52: "1_Thessalonians",
    53: "2_Thessalonians", 54: "1_Timothy", 55: "2_Timothy", 56: "Titus",
    57: "Philemon", 58: "Hebrews", 59: "James", 60: "1_Peter", 61: "2_Peter",
    62: "1_John", 63: "2_John", 64: "3_John", 65: "Jude", 66: "Revelation",
    # Apocrypha / Deuterocanonical (LXX)
    67: "1_Esdras", 68: "Tobit", 69: "Judith", 70: "Wisdom_of_Solomon",
    71: "Sirach", 72: "Judges_LXX", 73: "Baruch", 74: "1_Maccabees",
    75: "2_Maccabees", 76: "3_Maccabees", 77: "Tobit_LXX_S", 78: "Susanna",
    79: "Bel_and_Dragon", 80: "4_Maccabees", 81: "Esther_LXX", 82: "Daniel_LXX",
    83: "Jeremiah_LXX", 84: "Ester_LXX_Additions", 85: "Psalms_of_Solomon",
    86: "Odes"
}

OT_CHAPTERS = {
    "Genesis": 50, "Exodus": 40, "Leviticus": 27, "Numbers": 36, "Deuteronomy": 34,
    "Joshua": 24, "Judges": 21, "Ruth": 4, "1_Samuel": 31, "2_Samuel": 24,
    "1_Kings": 22, "2_Kings": 25, "1_Chronicles": 29, "2_Chronicles": 36,
    "Ezra": 10, "Nehemiah": 13, "Esther": 10, "Job": 42, "Psalms": 150,
    "Proverbs": 31, "Ecclesiastes": 12, "Song_of_Solomon": 8, "Isaiah": 66,
    "Jeremiah": 52, "Lamentations": 5, "Ezekiel": 48, "Daniel": 12,
    "Hosea": 14, "Joel": 3, "Amos": 9, "Obadiah": 1, "Jonah": 4,
    "Micah": 7, "Nahum": 3, "Habakkuk": 3, "Zephaniah": 3, "Haggai": 2,
    "Zechariah": 14, "Malachi": 4
}

def download_from_bolls(translation, book_id, chapter):
    url = f"https://bolls.life/get-text/{translation}/{book_id}/{chapter}/"
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                print(f"Bolls API retornou {response.status_code} para {url}")
        except Exception as e:
            print(f"Tentativa {attempt+1} falhou para {translation} {book_id}:{chapter} -> {e}")
            time.sleep(2)
    return None

def download_from_sefaria(book_name, chapter, version="Aleppo Codex"):
    encoded_version = requests.utils.quote(version)
    # Sefaria usa algarismos romanos ou nomes normais. Vamos ajustar nomes com número
    sefaria_name = book_name
    if book_name == "1_Samuel": sefaria_name = "I_Samuel"
    elif book_name == "2_Samuel": sefaria_name = "II_Samuel"
    elif book_name == "1_Kings": sefaria_name = "I_Kings"
    elif book_name == "2_Kings": sefaria_name = "II_Kings"
    elif book_name == "1_Chronicles": sefaria_name = "I_Chronicles"
    elif book_name == "2_Chronicles": sefaria_name = "II_Chronicles"

    url = f"https://www.sefaria.org/api/texts/{sefaria_name}.{chapter}?vhe={encoded_version}"
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                res = response.json()
                if "error" not in res:
                    return res
        except Exception as e:
            print(f"Tentativa {attempt+1} falhou Sefaria {book_name} {chapter} ({version}) -> {e}")
            time.sleep(2)
    return None

def save_chapter(translation, book_name, chapter, data):
    dir_path = f"data/{translation}/{book_name}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    with open(f"{dir_path}/{chapter}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def setup():
    # Traduções alvo no Bolls Bible (e equivalentes)
    translations = ["LXX", "SBLGNT", "WLC", "TR", "BYZ"]
    
    for trans in translations:
        print(f"\nObtendo lista de livros de {trans} no Bolls API...")
        url = f"https://bolls.life/get-books/{trans}/"
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                books = r.json()
                print(f"Total de livros disponíveis em {trans}: {len(books)}")
                for b in books:
                    book_id = b.get("bookid")
                    chapters_count = b.get("chapters")
                    book_name = BOLLS_BOOKS.get(book_id)
                    
                    if not book_name:
                        print(f"Aviso: Livro ID {book_id} não mapeado em BOLLS_BOOKS. Ignorando.")
                        continue
                        
                    print(f"Baixando {book_name} ({chapters_count} capítulos) para {trans}...")
                    for ch in range(1, chapters_count + 1):
                        # Verifica se já foi baixado
                        file_path = f"data/{trans}/{book_name}/{ch}.json"
                        if os.path.exists(file_path):
                            continue
                            
                        data = download_from_bolls(trans, book_id, ch)
                        if data:
                            save_chapter(trans, book_name, ch, data)
                            print(f"  Salvo: {trans} {book_name} {ch}/{chapters_count}")
                        time.sleep(0.1) # Evitar rate limit, download rápido
            else:
                print(f"Erro {r.status_code} ao buscar livros de {trans}")
        except Exception as e:
            print(f"Erro ao obter livros de {trans}: {e}")

    # Manuscritos Especiais via Sefaria (DSS e Aleppo)
    sefaria_versions = {"Aleppo": "Miqra according to the Masorah", "DSS": "Dead Sea Scrolls"}
    for trans_name, version in sefaria_versions.items():
        print(f"\nProcessando Sefaria: {trans_name} ({version})...")
        for book_name, total_ch in OT_CHAPTERS.items():
            print(f"Baixando {book_name} ({total_ch} capítulos) do Sefaria ({trans_name})...")
            for ch in range(1, total_ch + 1):
                file_path = f"data/{trans_name}/{book_name}/{ch}.json"
                if os.path.exists(file_path):
                    continue
                    
                data = download_from_sefaria(book_name, ch, version)
                if data:
                    save_chapter(trans_name, book_name, ch, data)
                    print(f"  Salvo: {trans_name} {book_name} {ch}/{total_ch}")
                time.sleep(0.2)

if __name__ == "__main__":
    setup()
