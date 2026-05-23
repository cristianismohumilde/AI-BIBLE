#!/usr/bin/env python3
"""
transliterate.py
================
Adiciona a chave "transliteration" a cada versículo nos arquivos JSON
de output/ que já foram traduzidos, usando a biblioteca Python `anyascii`.

Esta abordagem é 10.000x mais rápida que usar o LLM local, operando nativamente
para converter Hebraico, Grego, Siríaco, Armênio e Etíope para caracteres latinos
de forma instantânea.

Uso: python transliterate.py
"""

import os
import json
import time

try:
    from anyascii import anyascii
except ImportError:
    print("A biblioteca 'anyascii' não está instalada. Instalando agora...")
    os.system("pip install anyascii")
    from anyascii import anyascii

OUTPUT_DIR  = "output"

def transliterate_verse(original_text):
    if not original_text:
        return ""
    
    # Usa a biblioteca anyascii para converter qualquer alfabeto para ASCII
    return anyascii(original_text)

def process_collection(collection):
    """Processa todos os JSONs de uma coleção, adicionando/atualizando transliteração."""
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

        modified = False
        for v in verses:
            # Força a transliteração usando anyascii, reescrevendo qualquer transliteração antiga
            # que possa ter falhado ou estar incompleta.
            original = v.get("original", "")
            
            # Se já foi processado por esse script rápido, você poderia querer pular,
            # mas como a conversão é instântanea, compensa sempre rodar para atualizar.
            # Vamos gerar e comparar. Se já for igual, não conta como modified.
            new_translit = transliterate_verse(original)
            
            if v.get("transliteration") != new_translit:
                v["transliteration"] = new_translit
                modified = True

        if modified:
            # Reordena chaves: verse → original → transliteration → translation
            reordered = []
            for v in verses:
                entry = {"verse": v.get("verse")}
                if "original" in v:
                    entry["original"] = v["original"]
                entry["transliteration"] = v.get("transliteration", "")
                if "translation" in v:
                    entry["translation"] = v["translation"]
                reordered.append(entry)

            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(reordered, f, ensure_ascii=False, indent=2)
            done += 1
        else:
            skipped += 1

    return done, skipped


def main():
    print("=" * 60)
    print("TRANSLITERATOR AI-BIBLE (Modo Rápido com AnyAscii)")
    print("Adiciona transliteração a todos os versículos instantaneamente")
    print("=" * 60)

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

    start_time = time.time()

    for col in collections:
        print(f"Processando [{col}]...", end=" ")
        done, skipped = process_collection(col)
        total_done += done
        total_skipped += skipped
        print(f"Atualizados: {done} | Mantidos: {skipped}")

    elapsed = time.time() - start_time

    print("\n" + "=" * 60)
    print(f"Transliteração concluída em {elapsed:.2f} segundos!")
    print(f"  Arquivos atualizados: {total_done}")
    print(f"  Arquivos já atualizados: {total_skipped}")
    print("=" * 60)

if __name__ == "__main__":
    main()
