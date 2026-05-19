import os
import json
import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = "qwen2.5:32b"

DOUBLE_PASS_REVIEW = False

import re

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

def translate_text(text, source_language, target_language="Português"):
    lxx_instruction = ""
    if "septuaginta" in source_language.lower() or "lxx" in source_language.lower():
        lxx_instruction = (
            "ATENÇÃO FILOLÓGICA: O texto grego pode estar lematizado (com verbos no infinitivo ou presente da 1ª pessoa do singular do dicionário, e substantivos na forma nominativa padrão). "
            "NÃO faça uma tradução mecânica ou literal desses termos lematizados. Use sua memória teológica e filológica profunda da Septuaginta (LXX/Rahlfs) para reconstruir mentalmente o significado original do versículo em grego flexionado (histórico). "
            "Traduza os verbos com base em seu real sentido conjugado no contexto do relato histórico (geralmente na 3ª pessoa do pretérito, ex: 'aconteceu', 'sacrificaram', 'celebraram' em vez de 'sou', 'ofereço', 'levo'). "
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

    prompt = (
        f"Traduza o seguinte texto antigo ({source_language}) para o {target_language} "
        f"com extrema precisão teológica, rigor exegético e beleza literária. "
        f"{lxx_instruction}"
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

def review_translation(original_text, draft_translation, source_language, target_language="Português"):
    lxx_instruction = ""
    if "septuaginta" in source_language.lower() or "lxx" in source_language.lower():
        lxx_instruction = (
            "4. Verifique se o rascunho cometeu o erro de traduzir termos lematizados literalmente (como verbos na 1ª pessoa 'levo', 'ofereço' ou o pronome 'sou eu' a partir do grego lematizado). Se sim, corrija-o imediatamente para a terceira pessoa narrativa histórica do versículo real da Septuaginta.\n"
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

def sorting_key(filepath):
    parts = os.path.normpath(filepath).split(os.sep)
    category = parts[1] if len(parts) > 1 else ""
    book = parts[2] if len(parts) > 2 else ""
    chapter_file = parts[3] if len(parts) > 3 else ""
    chapter_name = os.path.splitext(chapter_file)[0]
    
    try:
        # Extrair números de capítulo ou daf para ordenação correta
        # Ex: "1", "12a", etc.
        num_part = "".join(c for c in chapter_name if c.isdigit())
        chapter_num = int(num_part) if num_part else chapter_name
    except ValueError:
        chapter_num = chapter_name
        
    return (category, book, chapter_num)

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
        "Talmud": "Hebraico Mishnaico e Aramaico Talmúdico"
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

        # --- CASO 1: Talmud ---
        if "Talmud" in parts:
            book = os.path.splitext(file)[0]
            source_language = language_map["Talmud"]
            
            with open(input_file, "r", encoding="utf-8") as f:
                data = json.load(f)

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
                    translated_verses = []
                    
                    for i, paragraph in enumerate(page):
                        if not paragraph or not isinstance(paragraph, str):
                            continue
                        para_num = i + 1
                        print(f"  -> Parágrafo {para_num}...", end="\r")
                        translated = translate_text(paragraph, source_language)
                        if DOUBLE_PASS_REVIEW and translated:
                            translated = review_translation(paragraph, translated, source_language)
                        translated_verses.append({
                            "verse": para_num,
                            "original": paragraph,
                            "translation": translated
                        })
                        
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
                source_language = language_map["Targum_Onkelos"]
                
                with open(input_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
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
                        translated_verses = []
                        
                        for i, verse in enumerate(chapter):
                            if not verse or not isinstance(verse, str):
                                continue
                            verse_num = i + 1
                            print(f"  -> Versículo {verse_num}...", end="\r")
                            translated = translate_text(verse, source_language)
                            if DOUBLE_PASS_REVIEW and translated:
                                translated = review_translation(verse, translated, source_language)
                            translated_verses.append({
                                "verse": verse_num,
                                "original": verse,
                                "translation": translated
                            })
                            
                        if translated_verses:
                            os.makedirs(output_dir, exist_ok=True)
                            with open(output_file, "w", encoding="utf-8") as f:
                                json.dump(translated_verses, f, ensure_ascii=False, indent=2)
                            print(f"✅ [Targum Onkelos] {book} {ch_num} traduzido!")

            # 2.2 Syriac Peshitta, Coptic Sahidic, Armenian Eastern
            elif file in ["peshitta_syriac.json", "coptic_sahidic.json", "armenian_eastern.json"]:
                trans_key = "Peshitta_Syriac" if "peshitta" in file else ("Coptic_Sahidic" if "coptic" in file else "Armenian_Eastern")
                source_language = language_map[trans_key]
                
                with open(input_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                if isinstance(data, dict) and "books" in data:
                    for book_dict in data["books"]:
                        book_name = book_dict.get("name", "Unknown")
                        for ch_dict in book_dict.get("chapters", []):
                            ch_num = ch_dict.get("chapter", 1)
                            verses = ch_dict.get("verses", [])
                            
                            output_dir = f"output/{trans_key}"
                            output_file = f"{output_dir}/{book_name}_{ch_num}.json"
                            
                            if os.path.exists(output_file):
                                continue
                                
                            print(f"\n🚀 [{trans_key}] Traduzindo {book_name} {ch_num}...")
                            translated_verses = []
                            
                            for v_dict in verses:
                                verse_num = v_dict.get("verse", 1)
                                verse_text = v_dict.get("text", "")
                                if not verse_text:
                                    continue
                                print(f"  -> Versículo {verse_num}...", end="\r")
                                translated = translate_text(verse_text, source_language)
                                if DOUBLE_PASS_REVIEW and translated:
                                    translated = review_translation(verse_text, translated, source_language)
                                translated_verses.append({
                                    "verse": verse_num,
                                    "original": verse_text,
                                    "translation": translated
                                })
                                
                            if translated_verses:
                                os.makedirs(output_dir, exist_ok=True)
                                with open(output_file, "w", encoding="utf-8") as f:
                                    json.dump(translated_verses, f, ensure_ascii=False, indent=2)
                                print(f"✅ [{trans_key}] {book_name} {ch_num} traduzido!")

        # --- CASO 3: Manuscritos Bíblicos normais (WLC, Aleppo, LXX, DSS, SBLGNT, etc.) ---
        else:
            if len(parts) < 4:
                continue

            translation = parts[1]
            book = parts[2]
            chapter_name = os.path.splitext(file)[0]

            source_language = language_map.get(translation, "Idiomas Originais")
            
            output_dir = f"output/{translation}"
            output_file = f"{output_dir}/{book}_{chapter_name}.json"

            if os.path.exists(output_file):
                continue

            print(f"\n🚀 [{translation}] Traduzindo {book} {chapter_name} ({source_language})...")

            with open(input_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            translated_verses = []

            if isinstance(data, list):
                for item in data:
                    verse_num = item.get("verse") or item.get("pk") or "1"
                    original_text = item.get("text", "")
                    if original_text:
                        print(f"  -> Versículo {verse_num}...", end="\r")
                        translated = translate_text(original_text, source_language)
                        if DOUBLE_PASS_REVIEW and translated:
                            translated = review_translation(original_text, translated, source_language)
                        translated_verses.append({
                            "verse": verse_num,
                            "original": original_text,
                            "translation": translated
                        })
            elif isinstance(data, dict):
                verses = data.get("he") or data.get("text") or []
                if isinstance(verses, list):
                    for i, original_text in enumerate(verses):
                        verse_num = i + 1
                        if original_text:
                            print(f"  -> Versículo {verse_num}...", end="\r")
                            translated = translate_text(original_text, source_language)
                            if DOUBLE_PASS_REVIEW and translated:
                                translated = review_translation(original_text, translated, source_language)
                            translated_verses.append({
                                "verse": verse_num,
                                "original": original_text,
                                "translation": translated
                            })

            if translated_verses:
                os.makedirs(output_dir, exist_ok=True)
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(translated_verses, f, ensure_ascii=False, indent=2)
                print(f"✅ [{translation}] {book} {chapter_name} traduzido e salvo!")

if __name__ == "__main__":
    main()
