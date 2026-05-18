#!/usr/bin/env python3
"""
transliterate.py
================
Adiciona a chave "transliteration" a cada versículo nos arquivos JSON
de output/ que já foram traduzidos, usando o mesmo modelo Qwen 2.5 32B.

IMPORTANTE: Este script é projetado para rodar APÓS translate_bible.py
terminar (ou em paralelo em uma segunda instância). Ele NÃO modifica
os arquivos que estão sendo gerados pelo translate_bible.py ao mesmo tempo,
pois percorre apenas arquivos já finalizados e pula os que já têm transliteração.

Uso: python transliterate.py

Sistema de transliteração:
  - Hebraico/Aramaico: SBL Hebrew Transliteration (com diacríticos ā, ō, š, ṭ, etc.)
  - Grego: SBL Greek Transliteration (ex: pneuma, logos, christos)
  - Siríaco: Transliteração acadêmica padrão (Sedra/CAL)
  - Copta: Sistema acadêmico copta (letras gregas + especiais)
  - Armênio: Transliteração ISO 9985
  - Ge'ez: Sistema Eritreo/Etíope padrão (ISO 1986)
"""

import os
import json
import requests
import time

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME  = "qwen2.5:32b"
OUTPUT_DIR  = "output"

# Mapeamento coleção → sistema de transliteração
TRANSLITERATION_SYSTEMS = {
    "Aleppo":           "SBL Hebraico (diacríticos: ā, ē, ō, š, ṣ, ṭ, ḥ, ʿ, ʾ)",
    "WLC":              "SBL Hebraico (diacríticos: ā, ē, ō, š, ṣ, ṭ, ḥ, ʿ, ʾ)",
    "DSS":              "SBL Hebraico/Aramaico (mantendo lacunas [ ] e ...)",
    "LXX":              "SBL Grego (ex: Bíblos → Biblos, Θεός → Theos)",
    "TR":               "SBL Grego Koiné (ex: Χριστός → Christos)",
    "BYZ":              "SBL Grego Koiné (ex: Κύριος → Kyrios)",
    "SBLGNT":           "SBL Grego Koiné",
    "Targum_Onkelos":   "SBL Aramaico (sistema CAL — Comprehensive Aramaic Lexicon)",
    "Peshitta_Syriac":  "Transliteração Siríaca acadêmica (Sedra/CAL — ex: ܡܪܝܐ → Maryā)",
    "Coptic_Sahidic":   "Transliteração Copta acadêmica (ex: ⲡⲛⲉⲩⲙⲁ → pneuma)",
    "Armenian_Eastern": "ISO 9985 Armênio (ex: Ասroel → Asroel)",
    "Talmud":           "SBL Hebraico Mishnaico + Aramaico Babilônico",
    "Geez":             "Sistema Etíope padrão (ex: አምላክ → ʾAmlāk)",
}


def transliterate_verse(original_text, collection):
    system = TRANSLITERATION_SYSTEMS.get(collection, "sistema acadêmico padrão para o idioma")

    prompt = (
        f"Translitere o seguinte texto bíblico antigo para o alfabeto latino "
        f"usando o sistema: {system}.\n"
        f"IMPORTANTE:\n"
        f"- Responda APENAS com a transliteração. Nada mais.\n"
        f"- NÃO traduza. NÃO explique. NÃO adicione notas.\n"
        f"- Preserve pontuação canônica e marcações de lacuna ([ ], ...) se presentes.\n"
        f"- Comece diretamente com o primeiro caractere da transliteração.\n\n"
        f"Texto:\n{original_text}"
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        r = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=180)
        if r.status_code == 200:
            result = r.json().get("response", "").strip()
            # Higienização mínima
            for prefix in ["Transliteração:", "Transliteration:", "Result:", "Answer:"]:
                if result.lower().startswith(prefix.lower()):
                    result = result[len(prefix):].strip()
            return result
    except Exception as e:
        print(f"  Erro Ollama: {e}")

    return None


def process_collection(collection):
    """Processa todos os JSONs de uma coleção, adicionando transliteração."""
    col_dir = os.path.join(OUTPUT_DIR, collection)
    if not os.path.isdir(col_dir):
        return 0, 0

    files = sorted([f for f in os.listdir(col_dir) if f.endswith(".json")])
    done = 0
    skipped = 0

    for fname in files:
        fpath = os.path.join(col_dir, fname)

        with open(fpath, "r", encoding="utf-8") as f:
            try:
                verses = json.load(f)
            except json.JSONDecodeError:
                print(f"  ERRO ao ler {fname}, pulando.")
                continue

        if not isinstance(verses, list) or not verses:
            continue

        # Verifica se TODOS os versículos já têm transliteração
        already_done = all("transliteration" in v for v in verses)
        if already_done:
            skipped += 1
            continue

        modified = False
        for v in verses:
            if "transliteration" in v and v["transliteration"]:
                continue  # Já tem
            original = v.get("original", "")
            if not original:
                v["transliteration"] = ""
                modified = True
                continue

            print(f"  [{collection}] {fname} v.{v.get('verse','?')}...", end="\r")
            translit = transliterate_verse(original, collection)
            if translit:
                v["transliteration"] = translit
                modified = True

        if modified:
            # Reordena chaves: verse → original → transliteration → translation
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

            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(reordered, f, ensure_ascii=False, indent=2)
            done += 1

    return done, skipped


def main():
    print("=" * 60)
    print("TRANSLITERATOR AI-BIBLE")
    print("Adiciona transliteração acadêmica a todos os versículos traduzidos")
    print("=" * 60)
    print(f"Host Ollama: {OLLAMA_HOST}")
    print(f"Modelo: {MODEL_NAME}")
    print()

    if not os.path.isdir(OUTPUT_DIR):
        print(f"Diretório '{OUTPUT_DIR}' não encontrado. Execute translate_bible.py primeiro.")
        return

    collections = sorted([
        d for d in os.listdir(OUTPUT_DIR)
        if os.path.isdir(os.path.join(OUTPUT_DIR, d))
    ])

    print(f"Coleções encontradas: {collections}\n")

    total_done = 0
    total_skipped = 0

    for col in collections:
        system = TRANSLITERATION_SYSTEMS.get(col, "padrão")
        print(f"\n[{col}] Sistema: {system}")
        done, skipped = process_collection(col)
        total_done += done
        total_skipped += skipped
        print(f"  Concluídos: {done} arquivos | Já tinham: {skipped}")

    print("\n" + "=" * 60)
    print(f"Transliteração concluída!")
    print(f"  Arquivos atualizados: {total_done}")
    print(f"  Arquivos já completos: {total_skipped}")
    print("=" * 60)


if __name__ == "__main__":
    main()
