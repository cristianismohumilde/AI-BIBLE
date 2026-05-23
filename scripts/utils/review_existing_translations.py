import os
import json
import requests
import re

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = "qwen2.5:32b"

# Lista de coleções de alta complexidade sugeridas para receber revisão prioritária (Double-Pass)
HIGH_COMPLEXITY_COLLECTIONS = [
    "LXX",               # Septuaginta (lematizada, grego clássico)
    "Targum_Onkelos",    # Aramaico do Targum (interpretações rabínicas)
    "Talmud",            # Debate dialético, aramaico e hebreu jurídico
    "Peshitta_Syriac",   # Siríaco antigo
    "Coptic_Sahidic",    # Copta Saídico
    "Armenian_Eastern",  # Armênio Clássico
    # Livros poéticos/proféticos complexos em hebraico
    "Psalms", "Job", "Song_of_Solomon", "Isaiah", "Lamentations", "Ezekiel"
]

def clean_translation_response(text):
    if not text:
        return text
    
    text = re.sub(r"```[a-zA-Z]*\n?", "", text)
    text = text.replace("```", "")
    
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
        if any(re.match(pat, stripped, re.IGNORECASE) for pat in patterns_to_remove):
            continue
        if stripped.lower().startswith("revisão conforme") or stripped.lower().startswith("critérios estabelecidos"):
            continue
        cleaned_lines.append(line)
        
    cleaned_text = "\n".join(cleaned_lines).strip()
    
    if "\n\nrevisão" in text.lower() or "\n\ntexto corrigido" in text.lower() or "\n\ntradução corrigida" in text.lower():
        parts = re.split(r"\n\n(?:revisão|texto corrigido|revisado|tradução corrigida).*?\n+", cleaned_text, flags=re.IGNORECASE)
        if len(parts) > 1:
            cleaned_text = parts[-1].strip()
            
    if cleaned_text.startswith('"') and cleaned_text.endswith('"'):
        cleaned_text = cleaned_text[1:-1].strip()
    if cleaned_text.startswith("'") and cleaned_text.endswith("'"):
        cleaned_text = cleaned_text[1:-1].strip()
        
    return cleaned_text.strip()

def review_translation(original_text, draft_translation, source_language):
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
        f"Rascunho de Tradução para o Português:\n{draft_translation}\n\n"
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

def main():
    output_dir = "output"
    if not os.path.exists(output_dir):
        print(f"Diretório '{output_dir}' não encontrado. Traduza alguns manuscritos primeiro.")
        return

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

    print("==================================================================")
    # Exibe a lista teológica prioritária sugerida
    print(f"🔍 Lista Prioritária de Alta Complexidade: {HIGH_COMPLEXITY_COLLECTIONS}")
    print("==================================================================")

    all_files = []
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".json"):
                all_files.append(os.path.join(root, file))

    total_reviewed_chapters = 0

    for filepath in all_files:
        parts = os.path.normpath(filepath).split(os.sep)
        # parts[1] será a coleção (ex: Aleppo, LXX, Targum_Onkelos)
        # parts[2] (opcional) será o livro
        collection = parts[1] if len(parts) > 1 else ""
        book = parts[2] if len(parts) > 2 else ""
        
        # Filtro: Apenas coleções ou livros altamente complexos que requerem revisão dupla
        # (Você pode comentar esta verificação se quiser forçar a revisão de TUDO)
        is_high_complexity = (collection in HIGH_COMPLEXITY_COLLECTIONS) or (book in HIGH_COMPLEXITY_COLLECTIONS)
        if not is_high_complexity:
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            verses = json.load(f)

        if not isinstance(verses, list) or len(verses) == 0:
            continue

        # Verifica se já está 100% revisado por este script
        needs_review = any(not verse.get("reviewed") for verse in verses)
        if not needs_review:
            continue

        source_language = language_map.get(collection, "Línguas Originais")
        print(f"\n✨ [Revisão Crítica] Polindo {collection} -> {book} (Idioma: {source_language})...")

        updated = False
        for idx, verse in enumerate(verses):
            if verse.get("reviewed"):
                continue

            original = verse.get("original", "")
            draft = verse.get("translation", "")
            verse_num = verse.get("verse", idx + 1)

            if not original or not draft:
                continue

            print(f"  -> Revisando Versículo {verse_num}...", end="\r")
            
            # Executa o Passe 2 (Autocrítica Filológica)
            reviewed_text = review_translation(original, draft, source_language)
            
            if reviewed_text:
                verse["translation"] = reviewed_text
                verse["reviewed"] = True
                updated = True

        if updated:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(verses, f, ensure_ascii=False, indent=2)
            total_reviewed_chapters += 1
            print(f"✅ {collection} -> {book} revisado e polido com sucesso!")

    print(f"\n🎉 Ciclo de revisão concluído! {total_reviewed_chapters} capítulos foram promovidos para Double-Pass!")

if __name__ == "__main__":
    main()
