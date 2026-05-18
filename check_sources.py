#!/usr/bin/env python3
"""
check_sources.py — Verifica status dos manuscritos e materiais de estudo baixados.
"""
import os, json

DATA_DIR = "/home/ubuntu/AI-BIBLE/data"

def check_json(path, label):
    if not os.path.exists(path):
        print(f"  [FALTANDO] {label}")
        return
    size = os.path.getsize(path) / 1024
    try:
        with open(path) as f:
            d = json.load(f)
        if isinstance(d, dict):
            keys = list(d.keys())[:4]
            if "books" in d:
                n_books = len(d["books"])
                first = d["books"][0].get("name","?") if d["books"] else "?"
                print(f"  [OK] {label} ({size:.0f} KB) — {n_books} livros, primeiro: {first}")
            elif "text" in d:
                chapters = len(d["text"])
                print(f"  [OK] {label} ({size:.0f} KB) — {chapters} capítulos/páginas no 'text'")
            else:
                print(f"  [OK] {label} ({size:.0f} KB) — chaves: {keys}")
        elif isinstance(d, list):
            print(f"  [OK] {label} ({size:.0f} KB) — lista com {len(d)} entradas")
    except Exception as e:
        print(f"  [ERRO] {label}: {e}")

print("\n========================================")
print("VERIFICAÇÃO DOS MANUSCRITOS POR IDIOMA")
print("========================================")

print("\n📜 ARAMAICO (Targum Onkelos):")
for book in ["genesis","exodus","leviticus","numbers","deuteronomy"]:
    check_json(f"{DATA_DIR}/ancient_versions/targum_onkelos_{book}.json", f"Targum {book.capitalize()}")

print("\n📖 SIRÍACO (Peshitta):")
check_json(f"{DATA_DIR}/ancient_versions/peshitta_syriac.json", "Peshitta NT+AT completo")

print("\n🔤 COPTA (Saídico):")
check_json(f"{DATA_DIR}/ancient_versions/coptic_sahidic.json", "Copta Saídico completo")

print("\n🏔️ ARMÊNIO ORIENTAL:")
check_json(f"{DATA_DIR}/ancient_versions/armenian_eastern.json", "Armênio Oriental completo")

print("\n🇪🇹 GE'EZ (Etiópico):")
geez_dir = f"{DATA_DIR}/ancient_versions/geez_extracted"
if os.path.isdir(geez_dir):
    files = []
    for root, dirs, fs in os.walk(geez_dir):
        for f in fs:
            files.append(os.path.join(root,f))
    print(f"  [INFO] Pasta geez_extracted/ presente com {len(files)} arquivos")
    for f in files:
        sz = os.path.getsize(f)/1024
        print(f"    {os.path.basename(f)} ({sz:.0f} KB)")
else:
    print("  [FALTANDO] Ge'ez não encontrado!")

print("\n📚 MATERIAIS DE ESTUDO:")
sm = f"{DATA_DIR}/study_materials"
if os.path.isdir(sm):
    for root, dirs, files in os.walk(sm):
        for f in files:
            fp = os.path.join(root, f)
            sz = os.path.getsize(fp)/1024
            print(f"  [OK] {f} ({sz:.0f} KB)")
else:
    print("  [FALTANDO] Pasta study_materials não encontrada")

print("\n📚 TALMUD (Sefaria):")
talmud_dir = f"{DATA_DIR}/Talmud"
if os.path.isdir(talmud_dir):
    for f in sorted(os.listdir(talmud_dir)):
        if f.endswith(".json"):
            check_json(os.path.join(talmud_dir, f), f"Tratado {f.replace('.json','')}")
else:
    print("  [FALTANDO]")

print("\n✅ Verificação concluída!")
