import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = "qwen2.5:32b"
MAX_WORKERS = 3

MAX_WORKERS = 3

DOUBLE_PASS_REVIEW = True

# === BUDGET LIMIT SCOPES ($300 USD) ===
SKIP_MANUSCRIPTS = {"WLC", "SBLGNT", "TR", "Talmud", "VUL", "Aleppo", "LXX", "Geez"}
ALLOWED_NT_BOOKS = {
    "1Corinthians", "1_Corinthians", "I Corinthians", 
    "Revelation", "Revelation of John"
}
ALLOWED_LXX_BOOKS = set()
ALLOWED_GEEZ_BOOKS = set()
ALLOWED_TARGUM_BOOKS = set()
ALLOWED_DSS_BOOKS = set()
# =======================================

import re

try:
    from transliterate import transliterate_verse
except ImportError:
    transliterate_verse = None

def load_json_file(filepath):
    """Carrega arquivos JSON de forma segura sem quebrar o pipeline em caso de arquivos vazios/corrompidos."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"\n⚠️ [ERRO] Falha ao decodificar JSON em '{filepath}' (arquivo corrompido ou vazio): {e}")
        return None
    except Exception as e:
        print(f"\n⚠️ [ERRO] Falha ao ler arquivo '{filepath}': {e}")
        return None

def add_transliteration_to_verses(verses, collection):
    """Adiciona transliteração em tempo real para os versículos recém-traduzidos. (DESABILITADO PARA POUPAR CPU)"""
    return verses

    
    # Reordena de forma bonita: verse -> original -> transliteration -> translation
    reordered = []
    for v in verses:
        entry = {"verse": v.get("verse")}
        if "original" in v:
            entry["original"] = v["original"]
        if "transliteration" in v:
            entry["transliteration"] = v["transliteration"]
        if "translation" in v:
            entry["translation"] = v["translation"]
        reordered.append(entry)
    return reordered

def clean_translation_response(text):
    if not text:
        return text
    
    # Remove blocos de código markdown se o modelo os colocou
    text = re.sub(r"```[a-zA-Z]*\n?", "", text)
    text = text.replace("```", "")
    
    # Padrões comuns de introdução ou cabeçalhos de metalinguagem de IA
    patterns_to_remove = [
        r"^(aqui está|eis a|segue a|conforme as instruções|tradução conforme).*?:?\n*",
        r"^(revisão conforme|revisado conforme|tradução corrigida|texto revisado).*?:?\n*",
        r"^versículo\s+\d+\s*:?\s*",
        r"^draft\s+\d+\s*:?\s*"
    ]
    
    lines = text.split("\n")
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append("")
            continue
        # Se bater com os padrões indesejados de introdução
        if any(re.match(pat, stripped, re.IGNORECASE) for pat in patterns_to_remove):
            continue
        # Se contiver marcadores de justificativa ou termos de metalinguagem na revisão
        if stripped.lower().startswith("revisão conforme") or stripped.lower().startswith("critérios estabelecidos"):
            continue
        cleaned_lines.append(line)
        
    cleaned_text = "\n".join(cleaned_lines).strip()
    
    # Caso o modelo tenha impresso tanto o rascunho quanto a seção de revisão separada por cabeçalho
    if "\n\nrevisão" in text.lower() or "\n\ntexto corrigido" in text.lower() or "\n\ntradução corrigida" in text.lower():
        parts = re.split(r"\n\n(?:revisão|texto corrigido|revisado|tradução corrigida).*?\n+", cleaned_text, flags=re.IGNORECASE)
        if len(parts) > 1:
            cleaned_text = parts[-1].strip()
            
    # Remove aspas redundantes envolvendo todo o texto
    if cleaned_text.startswith('"') and cleaned_text.endswith('"'):
        cleaned_text = cleaned_text[1:-1].strip()
    if cleaned_text.startswith("'") and cleaned_text.endswith("'"):
        cleaned_text = cleaned_text[1:-1].strip()
        
    return cleaned_text.strip()

def translate_text(text, source_language, target_language="Português", book=None, chapter=None, verse=None):
    lxx_instruction = ""
    context_intro = ""
    if book and chapter and verse:
        clean_book = str(book).replace('_', ' ')
        context_intro = f"Este texto pertence ao livro '{clean_book}', capítulo '{chapter}', versículo '{verse}'.\n"

    if "septuaginta" in source_language.lower() or "lxx" in source_language.lower():
        lxx_instruction = (
            f"O texto fornecido pertence ao livro '{str(book).replace('_', ' ')}', capítulo '{chapter}', versículo '{verse}' da Septuaginta (LXX).\n"
            "ATENÇÃO FILOLÓGICA CRÍTICA:\n"
            "1. O texto grego está totalmente lematizado (com verbos no infinitivo ou presente da 1ª pessoa do singular do dicionário, e substantivos na forma nominativa padrão).\n"
            "2. NÃO faça uma tradução mecânica ou literal desses lemas! Use seu conhecimento teológico e filológico avançado da Septuaginta (LXX/Rahlfs) para identificar qual é o versículo real correspondente a esta referência histórica.\n"
            "3. Traduza os nomes próprios e termos corretamente de acordo com a narrativa bíblica padrão (ex: 'ιωσίας' é o rei Josias, não 'Jesus' nem 'Josué'; 'χελκιας' é Helquias, não 'Caolho'; 'ραούμος' é Rathumus/Reum, não 'Antíoco'; 'σαμσαῖος' é Semellius/Samsai, não 'Simão').\n"
            "4. Conjugue os verbos corretamente no tempo narrativo histórico correspondente (geralmente no pretérito perfeito/imperfeito do indicativo na 3ª pessoa, ex: 'Josias celebrou a Páscoa', 'sacrificaram', 'ergueram', em vez de verbos na primeira pessoa como 'levo', 'ofereço').\n"
            "5. Certifique-se de que os números de animais e valores sejam traduzidos com exatidão matemática (ex: 'δισχίλιοι ἑξακόσιοι' é 2.600, não 260; 'τριακόσιοι' é 300, não 30; 'τρὶς χίλιοι' ou 'τρισχίλιοι' é 3.000, não 300).\n"
        )
    elif "targum" in source_language.lower():
        lxx_instruction = (
            "ATENÇÃO FILOLÓGICA: Este é um texto em Aramaico Antigo do Targum Onkelos (paráfrase clássica da Torá). "
            "Traduza com fidelidade filológica, captando as nuances interpretativas rabínicas tradicionais."
        )
    elif "peshitta" in source_language.lower() or "siríaco" in source_language.lower():
        lxx_instruction = (
            "ATENÇÃO FILOLÓGICA: Este é o texto siríaco clássico da Peshitta. "
            "Traduza com solenidade e exatidão filológica, preservando o ritmo majestoso e a teologia original."
        )
    elif "talmud" in source_language.lower():
        lxx_instruction = (
            "ATENÇÃO FILOLÓGICA: Este é o texto do Talmud (Mishna/Gemara). "
            "Traduza com extremo rigor acadêmico, preservando a estrutura de debate dialético e os termos jurídicos e exegéticos rabínicos."
        )
    elif "manuscritos do mar morto" in source_language.lower() or "dss" in source_language.lower():
        lxx_instruction = (
            "ATENÇÃO FILOLÓGICA CRÍTICA: Este é um texto dos Manuscritos do Mar Morto (DSS) em Hebraico e Aramaico de Qumran (Período do Segundo Templo, séc. III a.C. – I d.C.).\n"
            "1. O texto pode usar ortografia arcaica de Qumran (ex: 'לוא' em vez de 'לא', 'יעקוב' em vez de 'יעקב', 'כיא' em vez de 'כי'). Estas são formas autênticas, não erros — preserve o sentido original sem modernizar.\n"
            "2. Nomes próprios devem ser transliterados conforme a tradição bíblica portuguesa padrão (ex: Isaías, não 'Yeshayahu').\n"
            "3. Preserve a solenidade litúrgica e o paralelismo poético característico da poesia hebraica (especialmente nos Hinos e Salmos).\n"
            "4. Onde houver lacunas ou fragmentos incompletos no texto original (indicados por colchetes [...] ou espaços), indique com reticências ou nota mínima sem especular sobre o conteúdo perdido."
        )

    prompt = (
        f"Traduza o seguinte texto antigo ({source_language}) para o {target_language} "
        f"com extrema precisão teológica, rigor exegético e beleza literária.\n\n"
        f"{context_intro}"
        f"{lxx_instruction}\n"
        f"Importante: Forneça APENAS o texto final traduzido em português. NÃO adicione introduções, explicações, notas de rodapé, notas de tradutor, aspas ou saudações (como 'Eis a tradução' ou 'Aqui está'). "
        f"Comece a responder diretamente com o primeiro caractere do texto traduzido:\n\n{text}"
    )
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=300)
        if response.status_code == 200:
            raw = response.json().get("response", "").strip()
            return clean_translation_response(raw)
        else:
            print(f"Erro na API Ollama (Status {response.status_code}): {response.text}")
    except Exception as e:
        print(f"Erro ao conectar com o Ollama: {e}")
    
    return None

def review_translation(original_text, draft_translation, source_language, target_language="Português", book=None, chapter=None, verse=None):
    lxx_instruction = ""
    context_intro = ""
    if book and chapter and verse:
        clean_book = str(book).replace('_', ' ')
        context_intro = f"O versículo em análise é '{clean_book}', capítulo '{chapter}', versículo '{verse}'.\n"

    if "septuaginta" in source_language.lower() or "lxx" in source_language.lower():
        lxx_instruction = (
            "4. Verifique se o rascunho cometeu o erro grave de traduzir termos lematizados literalmente (como verbos na 1ª pessoa do singular 'levo', 'ofereço', ou nomes próprios errados como traduzir 'ιωσίας' (Josias) como 'Jesus' ou 'Josué', 'χελκιας' como 'Caolho', 'ραούμος' como 'Antíoco'). Se sim, corrija-os imediatamente para os nomes próprios e conjugações corretas do relato bíblico histórico real desse versículo.\n"
            "5. Verifique se as quantidades numéricas estão traduzidas com exatidão matemática.\n"
        )
    elif "targum" in source_language.lower():
        lxx_instruction = (
            "4. Certifique-se de que a tradução em português capta as nuances exegéticas e interpretativas do Targum Aramaico em comparação com o texto massorético hebraico padrão.\n"
        )
    elif "talmud" in source_language.lower():
        lxx_instruction = (
            "4. Certifique-se de que a tradução em português preserva o fluxo argumentativo e dialético típico do Talmud (Mishna/Gemara) e os termos jurídicos e exegéticos rabínicos.\n"
        )

    prompt = (
        f"Você é um revisor filológico e teológico de elite de línguas bíblicas antigas e textos rabínicos.\n\n"
        f"{context_intro}"
        f"Texto Original ({source_language}):\n{original_text}\n\n"
        f"Rascunho de Tradução para o {target_language}:\n{draft_translation}\n\n"
        f"Analise o rascunho com extremo rigor acadêmico. Verifique se:\n"
        f"1. O número gramatical (singular/plural) está perfeito (ex: 'hashamayim' deve ser traduzido no plural como 'céus').\n"
        f"2. Os verbos, preposições e substantivos foram traduzidos de forma contextualmente fiel.\n"
        f"3. O estilo linguístico em português é solene, formal e de alta qualidade teológica.\n"
        f"4. A resposta não contém introduções, saudações, aspas ou notas explicativas.\n"
        f"{lxx_instruction}\n"
        f"Se o rascunho estiver perfeito, repita EXATAMENTE o rascunho original.\n"
        f"Se houver qualquer deslize gramatical, erro de número, tradução literal de lematização ou imprecisão, ou se a resposta contiver frases introdutórias, forneça APENAS a tradução revisada e corrigida. Não dê explicações, notas de rodapé ou justificativas. Escreva apenas o texto final corrigido:"
    )
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=300)
        if response.status_code == 200:
            raw = response.json().get("response", "").strip()
            return clean_translation_response(raw)
    except Exception as e:
        print(f"Erro ao conectar com o Ollama para revisão: {e}")
    
    return draft_translation

def process_single_verse(original_text, verse_num, source_language, book=None, chapter=None):
    translated = translate_text(original_text, source_language, book=book, chapter=chapter, verse=verse_num)
    if DOUBLE_PASS_REVIEW and translated:
        translated = review_translation(original_text, translated, source_language, book=book, chapter=chapter, verse=verse_num)
    return {
        "verse": verse_num,
        "original": original_text,
        "translation": translated
    }

def translate_verses_parallel(verse_list, source_language, book=None, chapter=None):
    results = []
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(process_single_verse, text, num, source_language, book, chapter): num
            for num, text in verse_list
        }
        for future in futures:
            num = futures[future]
            try:
                res = future.result()
                if res:
                    results.append(res)
                    print(f"   -> Versículo {num} concluído!", end="\r")
            except Exception as e:
                print(f"\nErro ao traduzir versículo {num}: {e}")

    def get_sort_key(item):
        v = item.get("verse")
        if isinstance(v, int):
            return (0, v)
        try:
            return (0, int(v))
        except (ValueError, TypeError):
            # Para strings do tipo "12a" no Talmud
            num_part = "".join(c for c in str(v) if c.isdigit())
            suffix = "".join(c for c in str(v) if not c.isdigit())
            if num_part:
                return (0, int(num_part), suffix)
            return (1, str(v))

    results.sort(key=get_sort_key)
    return results



def sorting_key(filepath):
    parts = os.path.normpath(filepath).split(os.sep)
    category = parts[1] if len(parts) > 1 else ""
    book = parts[2] if len(parts) > 2 else ""
    
    filename = os.path.basename(filepath).lower()
    
    # Prioridade de tradução personalizada solicitada pelo usuário + TRANSLATION_QUEUE.md
    priority = 99
    # === ORDEM DE TRADUÇÃO ATUAL (atualizada em 21/05/2026) ===
    # 1: Targum Onkelos — Gênesis
    # 2: Aleppo Codex (concluído)
    # 3: LXX (concluído)
    # 4: Ge'ez (concluído)
    # 5: DSS — 5 rolos prioritários (1QIsa-a, 1QpHab, 1QS, 1QM, 1QH)
    # 6: Apócrifos (4 Esdras / Vulgata e outros)
    # 7: Targum Onkelos — restante da Torá
    # 8: BYZ, Peshitta, Copta, Armênio
    if category == "ancient_versions" and "targum_onkelos_genesis" in filename:
        priority = 1  # 🥇 Primeiro: Targum Onkelos — Gênesis
    elif category == "Aleppo":
        priority = 2
    elif category == "LXX":
        priority = 3
    elif category == "ancient_versions" and "geez_extracted" in parts:
        priority = 4
    elif category == "DSS":
        priority = 5  # filtrado por ALLOWED_DSS_BOOKS (1QIsa-a, 1QpHab, 1QS, 1QM, 1QH)
    elif category == "apocrypha" and filename.endswith(".json"):
        priority = 6  # 4 Esdras (Vulgata), Oração de Manassés, etc.
    elif category == "ancient_versions" and "targum_onkelos" in filename:
        priority = 7  # restante do Targum (Exodus, Leviticus, Numbers, Deuteronomy)
    elif category == "BYZ":
        priority = 8
    elif category == "ancient_versions" and "peshitta" in filename:
        priority = 9
    elif category == "ancient_versions" and "coptic" in filename:
        priority = 10
    elif category == "ancient_versions" and "armenian" in filename:
        priority = 11
    else:
        priority = 12
        
    chapter_name = os.path.splitext(os.path.basename(filepath))[0]
        
    try:
        num_part = "".join(c for c in chapter_name if c.isdigit())
        if num_part:
            chapter_num = (0, int(num_part))
        else:
            chapter_num = (1, chapter_name)
    except Exception:
        chapter_num = (1, chapter_name)
        
    return (priority, category, book, chapter_num)

def main():
    data_dir = "data"
    if not os.path.exists(data_dir):
        print(f"Diretório '{data_dir}' não encontrado. Execute o script de download primeiro.")
        return

    # Mapeamento de fontes para idiomas
    language_map = {
        "WLC": "Hebraico Antigo",
        "Aleppo": "Hebraico Antigo",
        "LXX": "Grego Antigo (Septuaginta)",
        "DSS": "Hebraico e Aramaico Antigo (Manuscritos do Mar Morto)",
        "SBLGNT": "Grego Antigo (Koiné)",
        "TR": "Grego Antigo (Koiné)",
        "BYZ": "Grego Antigo (Koiné)",
        "Targum_Onkelos": "Aramaico Antigo (Targum Onkelos)",
        "Peshitta_Syriac": "Siríaco Antigo (Peshitta)",
        "Coptic_Sahidic": "Copta Saídico",
        "Armenian_Eastern": "Armênio Oriental Antigo",
        "Talmud": "Hebraico Mishnaico e Aramaico Talmúdico",
        "Geez": "Ge'ez (Etíope Clássico)",
        "apocrypha": "Latim Clássico (Vulgata / Apócrifos)",
    }

    # Apócrifos estruturados com suporte de tradução
    # Formato: {filename: (book_name, source_language_override)}
    APOCRYPHA_BOOKS = {
        "4_esdras_vulgate.json": ("4 Esdras", "Latim Clássico (Vulgata)"),
        "prayer_of_manasseh.json": ("Oração de Manassés", "Grego Antigo (Apócrifos)"),
        "psalm_151.json": ("Salmo 151", "Hebraico Antigo (DSS)"),
    }

    # Arquivos a pular na varredura (formato incompatível, metadados, ou textos já cobertos por outras coleções)
    SKIP_FILES = {
        "mishnah_berakhot.json",   # dump de metadados da API Sefaria, não é texto traduzível
        "manifest.json",           # arquivo de manifesto estrutural
        "strongs_greek.json",      # arquivo vazio/corrompido
        "strongs_hebrew.json",     # arquivo vazio/corrompido
    }

    print("Iniciando varredura de manuscritos para tradução...")

    all_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".json"):
                all_files.append(os.path.join(root, file))

    # Ordena sequencialmente
    all_files.sort(key=sorting_key)

    for input_file in all_files:
        parts = os.path.normpath(input_file).split(os.sep)
        file = os.path.basename(input_file)

        # Pula arquivos com formato incompatível ou corrompidos
        if file in SKIP_FILES:
            continue

        # --- CASO 1.5: Apócrifos estruturados (4 Esdras Vulgata, etc.) ---
        if "apocrypha" in parts and file in APOCRYPHA_BOOKS:
            book_name, source_language = APOCRYPHA_BOOKS[file]
            data = load_json_file(input_file)
            if data is None:
                continue

            if not isinstance(data, list):
                continue  # formato inesperado

            for chapter_dict in data:
                ch_num = chapter_dict.get("chapter", 1)
                verses = chapter_dict.get("verses", [])
                if not verses:
                    continue

                output_dir = "output/Apocrypha"
                safe_book = book_name.replace(" ", "_")
                output_file = f"{output_dir}/{safe_book}_{ch_num}.json"

                if os.path.exists(output_file):
                    continue

                print(f"\n🚀 [Apócrifos] Traduzindo {book_name} {ch_num}...")
                verse_list = []
                for v in verses:
                    verse_num = v.get("verse", 1)
                    verse_text = v.get("text", "")
                    if verse_text:
                        verse_list.append((verse_num, verse_text))

                translated_verses = translate_verses_parallel(
                    verse_list, source_language, book=book_name, chapter=ch_num
                )
                translated_verses = add_transliteration_to_verses(translated_verses, "Apocrypha")

                if translated_verses:
                    os.makedirs(output_dir, exist_ok=True)
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(translated_verses, f, ensure_ascii=False, indent=2)
                    print(f"✅ [Apócrifos] {book_name} {ch_num} traduzido!")

        # --- CASO 1: Talmud ---
        elif "Talmud" in parts:
            if "Talmud" in SKIP_MANUSCRIPTS:
                continue
            book = os.path.splitext(file)[0]
            source_language = language_map["Talmud"]

            data = load_json_file(input_file)
            if data is None:
                continue

            if isinstance(data, dict) and "text" in data:
                pages = data["text"]
                for page_idx, page in enumerate(pages):
                    if not page or not isinstance(page, list) or len(page) == 0:
                        continue
                    
                    daf_num = page_idx // 2 + 1
                    daf_side = 'a' if page_idx % 2 == 0 else 'b'
                    daf_name = f"{daf_num}{daf_side}"
                    
                    output_dir = "output/Talmud"
                    output_file = f"{output_dir}/{book}_{daf_name}.json"
                    
                    if os.path.exists(output_file):
                        continue
                        
                    print(f"\n🚀 [Talmud] Traduzindo {book} Daf {daf_name}...")
                    verse_list = []
                    for i, paragraph in enumerate(page):
                        if paragraph and isinstance(paragraph, str):
                            verse_list.append((i + 1, paragraph))
                    
                    translated_verses = translate_verses_parallel(verse_list, source_language, book=book, chapter=daf_name)
                    translated_verses = add_transliteration_to_verses(translated_verses, "Talmud")

                    if translated_verses:
                        os.makedirs(output_dir, exist_ok=True)
                        with open(output_file, "w", encoding="utf-8") as f:
                            json.dump(translated_verses, f, ensure_ascii=False, indent=2)
                        print(f"✅ [Talmud] {book} Daf {daf_name} traduzido!")

        # --- CASO 2: Ancient Versions diretamente em ancient_versions/ ---
        elif "ancient_versions" in parts:
            # 2.1 Targum Onkelos
            if file.startswith("targum_onkelos_"):
                book = file.replace("targum_onkelos_", "").replace(".json", "").capitalize()
                if book not in ALLOWED_TARGUM_BOOKS:
                    continue
                source_language = language_map["Targum_Onkelos"]

                data = load_json_file(input_file)
                if data is None:
                    continue
                    
                if isinstance(data, dict) and "text" in data:
                    chapters = data["text"]
                    for ch_idx, chapter in enumerate(chapters):
                        if not chapter or not isinstance(chapter, list) or len(chapter) == 0:
                            continue
                            
                        ch_num = ch_idx + 1
                        output_dir = "output/Targum_Onkelos"
                        output_file = f"{output_dir}/{book}_{ch_num}.json"
                        
                        if os.path.exists(output_file):
                            continue
                            
                        print(f"\n🚀 [Targum Onkelos] Traduzindo {book} {ch_num}...")
                        verse_list = []
                        for i, verse in enumerate(chapter):
                            if verse and isinstance(verse, str):
                                verse_list.append((i + 1, verse))
                        
                        translated_verses = translate_verses_parallel(verse_list, source_language, book=book, chapter=ch_num)
                        translated_verses = add_transliteration_to_verses(translated_verses, "Targum_Onkelos")

                        if translated_verses:
                            os.makedirs(output_dir, exist_ok=True)
                            with open(output_file, "w", encoding="utf-8") as f:
                                json.dump(translated_verses, f, ensure_ascii=False, indent=2)
                            print(f"✅ [Targum Onkelos] {book} {ch_num} traduzido!")

            # 2.2 Syriac Peshitta, Coptic Sahidic, Armenian Eastern
            elif file in ["peshitta_syriac.json", "coptic_sahidic.json", "armenian_eastern.json"]:
                trans_key = "Peshitta_Syriac" if "peshitta" in file else ("Coptic_Sahidic" if "coptic" in file else "Armenian_Eastern")
                source_language = language_map[trans_key]

                data = load_json_file(input_file)
                if data is None:
                    continue
                    
                if isinstance(data, dict) and "books" in data:
                    for book_dict in data["books"]:
                        book_name = book_dict.get("name", "Unknown")
                        if book_name not in ALLOWED_NT_BOOKS:
                            continue
                        for ch_dict in book_dict.get("chapters", []):
                            ch_num = ch_dict.get("chapter", 1)
                            verses = ch_dict.get("verses", [])
                            
                            output_dir = f"output/{trans_key}"
                            output_file = f"{output_dir}/{book_name}_{ch_num}.json"
                            
                            if os.path.exists(output_file):
                                continue
                                
                            print(f"\n🚀 [{trans_key}] Traduzindo {book_name} {ch_num}...")
                            verse_list = []
                            for v_dict in verses:
                                verse_num = v_dict.get("verse", 1)
                                verse_text = v_dict.get("text", "")
                                if verse_text:
                                    verse_list.append((verse_num, verse_text))
                            
                            translated_verses = translate_verses_parallel(verse_list, source_language, book=book_name, chapter=ch_num)
                            translated_verses = add_transliteration_to_verses(translated_verses, trans_key)

                            if translated_verses:
                                os.makedirs(output_dir, exist_ok=True)
                                with open(output_file, "w", encoding="utf-8") as f:
                                    json.dump(translated_verses, f, ensure_ascii=False, indent=2)
                                print(f"✅ [{trans_key}] {book_name} {ch_num} traduzido!")

            # 2.3 Ge'ez (Classical Ethiopic)
            elif "geez_extracted" in parts:
                source_language = language_map["Geez"]
                book_name = file.replace(".json", "")

                if "_" in book_name:
                    book_title, ch_num = book_name.rsplit("_", 1)
                else:
                    book_title, ch_num = book_name, "1"

                if book_title not in ALLOWED_GEEZ_BOOKS:
                    continue

                output_dir = "output/Geez"
                output_file = f"{output_dir}/{book_title}_{ch_num}.json"

                if os.path.exists(output_file):
                    continue

                print(f"\n🚀 [Ge'ez] Traduzindo {book_title} {ch_num}...")

                data = load_json_file(input_file)
                if data is None:
                    continue

                verse_list = []
                if isinstance(data, dict) and "text" in data:
                    for item in data["text"]:
                        if item.strip():
                            parts_item = item.split(" ", 1)
                            if len(parts_item) == 2:
                                v_num, v_text = parts_item
                            else:
                                v_num, v_text = "1", item
                            verse_list.append((v_num.strip(), v_text.strip()))

                translated_verses = translate_verses_parallel(verse_list, source_language, book=book_title, chapter=ch_num)
                translated_verses = add_transliteration_to_verses(translated_verses, "Geez")

                if translated_verses:
                    os.makedirs(output_dir, exist_ok=True)
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(translated_verses, f, ensure_ascii=False, indent=2)
                    print(f"✅ [Ge'ez] {book_title} {ch_num} traduzido!")

        # --- CASO 3: Manuscritos Bíblicos normais (WLC, Aleppo, LXX, DSS, SBLGNT, etc.) ---
        else:
            # Suporte a estrutura plana: data/BYZ/Book_Chapter.json (len(parts) == 3)
            if len(parts) == 3:
                translation = parts[1]
                filename_base = os.path.splitext(file)[0]  # ex: "1Corinthians_1"

                if translation in SKIP_MANUSCRIPTS:
                    continue

                # Extrai book e chapter do nome do arquivo (ex: "1Corinthians_1" -> book="1Corinthians", chapter="1")
                if "_" in filename_base:
                    last_underscore = filename_base.rfind("_")
                    book = filename_base[:last_underscore]
                    chapter_name = filename_base[last_underscore + 1:]
                else:
                    book = filename_base
                    chapter_name = "1"

                if translation == "BYZ" and book not in ALLOWED_NT_BOOKS:
                    continue

                source_language = language_map.get(translation, "Idiomas Originais")
                output_dir = f"output/{translation}"
                output_file = f"{output_dir}/{book}_{chapter_name}.json"

                if os.path.exists(output_file):
                    continue

                print(f"\n🚀 [{translation}] Traduzindo {book} {chapter_name} ({source_language})...")

                data = load_json_file(input_file)
                if data is None:
                    continue

                verse_list = []
                if isinstance(data, list):
                    for item in data:
                        verse_num = item.get("verse") or item.get("pk") or "1"
                        original_text = item.get("text", "")
                        if original_text:
                            verse_list.append((verse_num, original_text))
                elif isinstance(data, dict):
                    verses = data.get("he") or data.get("text") or []
                    if isinstance(verses, list):
                        for i, original_text in enumerate(verses):
                            if original_text:
                                verse_list.append((i + 1, original_text))

                translated_verses = translate_verses_parallel(verse_list, source_language, book=book, chapter=chapter_name)
                translated_verses = add_transliteration_to_verses(translated_verses, translation)

                if translated_verses:
                    os.makedirs(output_dir, exist_ok=True)
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(translated_verses, f, ensure_ascii=False, indent=2)
                    print(f"✅ [{translation}] {book} {chapter_name} traduzido e salvo!")
                continue

            if len(parts) < 4:
                continue

            translation = parts[1]
            book = parts[2]
            chapter_name = os.path.splitext(file)[0]

            if translation in SKIP_MANUSCRIPTS:
                continue
            if translation == "LXX" and book not in ALLOWED_LXX_BOOKS:
                continue
            if translation == "BYZ" and book not in ALLOWED_NT_BOOKS:
                continue
            if translation == "DSS" and book not in ALLOWED_DSS_BOOKS:
                continue  # evita traduzir os 928 arquivos em inglês; aguarda download do ETCBC (1QS, 1QM, 1QH)

            source_language = language_map.get(translation, "Idiomas Originais")
            
            output_dir = f"output/{translation}"
            output_file = f"{output_dir}/{book}_{chapter_name}.json"

            if os.path.exists(output_file):
                continue

            print(f"\n🚀 [{translation}] Traduzindo {book} {chapter_name} ({source_language})...")

            data = load_json_file(input_file)
            if data is None:
                continue

            verse_list = []
            if isinstance(data, list):
                for item in data:
                    verse_num = item.get("verse") or item.get("pk") or "1"
                    original_text = item.get("text", "")
                    if original_text:
                        verse_list.append((verse_num, original_text))
            elif isinstance(data, dict):
                verses = data.get("he") or data.get("text") or []
                if isinstance(verses, list):
                    for i, original_text in enumerate(verses):
                        verse_num = i + 1
                        if original_text:
                            verse_list.append((verse_num, original_text))

            translated_verses = translate_verses_parallel(verse_list, source_language, book=book, chapter=chapter_name)
            translated_verses = add_transliteration_to_verses(translated_verses, translation)

            if translated_verses:
                os.makedirs(output_dir, exist_ok=True)
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(translated_verses, f, ensure_ascii=False, indent=2)
                print(f"✅ [{translation}] {book} {chapter_name} traduzido e salvo!")

if __name__ == "__main__":
    main()
