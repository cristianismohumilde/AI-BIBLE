"""
generate_progress.py
====================
Gera automaticamente o arquivo PROGRESS.md com o status real de traducao,
comparando os arquivos de entrada (data/) com as saidas traduzidas (output/).

Uso: python generate_progress.py
"""

import os
import sys
import json
from datetime import datetime, timezone

DATA_DIR = "data"
OUTPUT_DIR = "output"

# === BUDGET LIMIT SCOPES ($300 USD) ===
SKIP_MANUSCRIPTS = {"WLC", "DSS", "SBLGNT", "TR", "Talmud", "VUL"}
ALLOWED_NT_BOOKS = {
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", 
    "1Corinthians", "2Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", 
    "1Thessalonians", "2Thessalonians", "1Timothy", "2Timothy", "Titus", "Philemon", 
    "Hebrews", "James", "1Peter", "2Peter", "1John", "2John", "3John", "Jude", "Revelation",
    "1_Corinthians", "2_Corinthians", "1_Thessalonians", "2_Thessalonians", "1_Timothy", "2_Timothy", 
    "1_Peter", "2_Peter", "1_John", "2_John", "3_John", 
    "I Corinthians", "II Corinthians", "I Thessalonians", "II Thessalonians", "I Timothy", "II Timothy", 
    "I Peter", "II Peter", "I John", "II John", "III John", "Revelation of John"
}
ALLOWED_LXX_BOOKS = {
    "Isaiah", "Psalms", "1_Maccabees", "2_Maccabees", "3_Maccabees", "4_Maccabees", 
    "Baruch", "Bel_and_Dragon", "Judith", "Odes", "Psalms_of_Solomon", "Sirach", 
    "Susanna", "Tobit", "Wisdom_of_Solomon", "1_Esdras"
}
ALLOWED_GEEZ_BOOKS = {
    "የማቴዎስ ወንጌል", "የማርቆስ ወንጌል", "የሉቃስ ወንጌል", "የዮሐንስ ወንጌል", "የሐዋርያት ሥራ", 
    "ወደ ሮሜ ሰዎች", "1ኛ ወደ ቆሮንቶስ ሰዎች", "2ኛ ወደ ቆሮንቶስ ሰዎች", "ወደ ገላትያ ሰዎች", "ወደ ኤፌሶን ሰዎች", 
    "ወደ ፊልጵስዩስ ሰዎች", "ወደ ቆላስይስ ሰዎች", "1ኛ ወደ ተሰሎንቄ ሰዎች", "2ኛ ወደ ተሰሎንቄ ሰዎች", 
    "1ኛ ወደ ጢሞቴዎስ", "2ኛ ወደ ጢሞቴዎስ", "ወደ ቲቶ", "ወደ ፊልሞና", "ወደ ዕብራውያን", "የያዕቆብ መልእክት", 
    "1ኛ የጴጥሮስ መልእክት", "2ኛ የጴጥሮስ መልእክት", "1ኛ የዮሐንስ መልእክት", "2ዮሐ", "3ኛ የዮሐንስ መልእክት", 
    "የይሁዳ መልእክት", "የዮሐንስ ራእይ", "መጽሐፈ ሄኖክ", "መጽሐፈ ኩፋሌ"
}
# =======================================

COLLECTION_LABELS = {
    "Aleppo":          ("📜 Códice de Aleppo",          "Hebraico Massorético Antigo"),
    "WLC":             ("📜 Texto de Leningrado (WLC)",  "Hebraico Massorético"),
    "LXX":             ("🏛️ Septuaginta (LXX)",          "Grego Clássico"),
    "DSS":             ("🪨 Manuscritos do Mar Morto",   "Hebraico/Aramaico Antigo"),
    "TR":              ("✝️ Textus Receptus (TR)",        "Grego Koiné"),
    "BYZ":             ("✝️ Texto Bizantino (BYZ)",       "Grego Koiné"),
    "SBLGNT":          ("✝️ Texto Crítico (SBLGNT)",      "Grego Koiné"),
    "VUL":             ("🏛️ Vulgata Latina",              "Latim"),
    "Targum_Onkelos":  ("📜 Targum Onkelos",             "Aramaico Antigo"),
    "Peshitta_Syriac": ("📖 Peshitta Siríaca",           "Siríaco Clássico"),
    "Coptic_Sahidic":  ("🔤 Versão Copta Saídica",       "Copta Saídico"),
    "Armenian_Eastern":("🏔️ Versão Armênia Oriental",    "Armênio Clássico"),
    "Talmud":          ("📚 Talmud Bavli",               "Hebraico Mishnaico / Aramaico"),
    "Geez":            ("🇪🇹 Versão Ge'ez (Etíope)",      "Ge'ez (Etíope Clássico)"),
}


def count_files_recursive(directory, collection_name=None):
    """Conta recursivamente todos os arquivos .json em um diretório, respeitando os limites."""
    if collection_name in SKIP_MANUSCRIPTS:
        return 0
    if not os.path.isdir(directory):
        return 0
    count = 0
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(".json"):
                parts = os.path.normpath(os.path.join(root, f)).split(os.sep)
                if len(parts) >= 3:
                    book = parts[-2] if not parts[-2] == collection_name else parts[-1].replace('.json', '')
                    if collection_name == "LXX" and book not in ALLOWED_LXX_BOOKS: continue
                    if collection_name == "BYZ" and book not in ALLOWED_NT_BOOKS: continue
                count += 1
    return count


def count_output_files(collection):
    """Conta os arquivos JSON traduzidos em output/<collection>/."""
    out_path = os.path.join(OUTPUT_DIR, collection)
    if not os.path.isdir(out_path):
        return 0
    return sum(1 for f in os.listdir(out_path) if f.endswith(".json"))


def count_data_files(collection):
    """Conta os arquivos JSON de entrada em data/<collection>/.
    Para coleções com livros em sub-pastas, percorre recursivamente.
    Para as versões antigas compactadas em arquivos únicos, abre os JSONs e conta dinamicamente os capítulos.
    """
    if collection == "VUL":
        if collection in SKIP_MANUSCRIPTS:
            return 0
        if os.path.exists(os.path.join(DATA_DIR, "VUL", "vulgata_latina.txt")):
            return 1189

    if collection == "Geez":
        geez_dir = os.path.join(DATA_DIR, "ancient_versions", "geez_extracted")
        if os.path.isdir(geez_dir):
            count = 0
            for f in os.listdir(geez_dir):
                if f.endswith(".json"):
                    book_name = f.replace(".json", "")
                    book_title = book_name.rsplit("_", 1)[0] if "_" in book_name else book_name
                    if book_title in ALLOWED_GEEZ_BOOKS:
                        count += 1
            return count
        return 0

    ancient_map = {
        "Peshitta_Syriac": "peshitta_syriac.json",
        "Coptic_Sahidic": "coptic_sahidic.json",
        "Armenian_Eastern": "armenian_eastern.json"
    }

    if collection in ancient_map:
        fpath = os.path.join(DATA_DIR, "ancient_versions", ancient_map[collection])
        if os.path.exists(fpath):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return sum(len(b.get("chapters", [])) for b in data.get("books", []) if b.get("name") in ALLOWED_NT_BOOKS)
            except Exception:
                return 260
        return 0

    if collection == "Targum_Onkelos":
        av_dir = os.path.join(DATA_DIR, "ancient_versions")
        if os.path.isdir(av_dir):
            total_ch = 0
            for f in os.listdir(av_dir):
                if f.startswith("targum_onkelos_") and f.endswith(".json"):
                    try:
                        with open(os.path.join(av_dir, f), "r", encoding="utf-8") as file:
                            data = json.load(file)
                            total_ch += len(data.get("text", []))
                    except Exception:
                        pass
            return total_ch if total_ch > 0 else 187
        return 0

    if collection == "Talmud":
        data_path = os.path.join(DATA_DIR, "Talmud")
        if not os.path.isdir(data_path):
            return 0
        total_pages = 0
        for f in os.listdir(data_path):
            if f.endswith(".json"):
                try:
                    with open(os.path.join(data_path, f), "r", encoding="utf-8") as file:
                        data = json.load(file)
                        pages = data.get("text", [])
                        valid_pages = sum(1 for p in pages if p and isinstance(p, list) and len(p) > 0)
                        total_pages += valid_pages
                except Exception:
                    pass
        if collection in SKIP_MANUSCRIPTS:
            return 0
        return total_pages if total_pages > 0 else 36

    data_path = os.path.join(DATA_DIR, collection)
    if not os.path.isdir(data_path):
        return 0
    # Conta todos os .json recursivamente
    return count_files_recursive(data_path, collection)


def progress_bar(done, total, width=20):
    """Gera uma barra de progresso em texto."""
    if total == 0:
        return "░" * width + " (sem dados)"
    ratio = done / total
    filled = int(ratio * width)
    bar = "█" * filled + "░" * (width - filled)
    pct = ratio * 100
    return f"`{bar}` {pct:.1f}%"


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Coleções de dados principais
    collections = list(COLLECTION_LABELS.keys())

    rows = []
    total_data = 0
    total_output = 0

    for col in collections:
        label, lang = COLLECTION_LABELS[col]
        data_count = count_data_files(col)

        # Para Talmud e ancient_versions, output usa nomes customizados
        out_count = count_output_files(col)

        total_data += data_count
        total_output += out_count

        bar = progress_bar(out_count, data_count)
        status = "✅ Completo" if data_count > 0 and out_count >= data_count else (
            "🚀 Em andamento" if out_count > 0 else (
            "⏳ Aguardando" if data_count > 0 else "❌ Sem dados"))

        rows.append(
            f"| {label} | {lang} | {data_count:,} | {out_count:,} | {bar} | {status} |"
        )

    overall_bar = progress_bar(total_output, total_data)

    # Estimativa de tempo restante (Nova velocidade com 3 workers concorrentes em GPU A10: 26 capítulos por hora)
    remaining = total_data - total_output
    hours_remaining = remaining / 26 if remaining > 0 else 0
    days = int(hours_remaining // 24)
    hours = int(hours_remaining % 24)
    eta_str = f"~{days}d {hours}h" if remaining > 0 else "🎉 Concluído!"
    
    # Custo real da instância VM.GPU.A10.1 (aprox. $1.50 por hora)
    custo_total = int(hours_remaining * 1.50)
    custo_str = f"~${custo_total} USD" if remaining > 0 else "$0"

    md = f"""# 📊 PROGRESS — AI-BIBLE Translation Status

> Gerado automaticamente em: **{now}**
> Velocidade estimada: ~26 capítulos/hora com Double-Pass Review concorrente ativo.

---

## 📈 Progresso Geral

{overall_bar}

**{total_output:,}** de **{total_data:,}** capítulos traduzidos.
**ETA estimado:** {eta_str}
**Custo Computacional Restante:** {custo_str}

---

## 📋 Detalhamento por Coleção

| Coleção | Idioma Original | Capítulos Fonte | Traduzidos | Progresso | Status |
| :--- | :--- | ---: | ---: | :--- | :--- |
{chr(10).join(rows)}

---

## 📜 Manuscritos Apócrifos e Históricos (Fase 4)
Os seguintes textos já estão baixados e preservados na pasta `data/apocrypha/` aguardando expansão do projeto:
- **Livro de Enoque** (Edição Crítica de R.H. Charles)
- **Livro dos Jubileus** (Etiópico Clássico)
- **Testamento dos Doze Patriarcas** (Grego Antigo)
- **Mishná: Berakhot** (Sefaria API)
*(A Didaquê está programada para download)*

---

## 🔄 Como atualizar este arquivo

```bash
python generate_progress.py
```

O arquivo é atualizado automaticamente pelo `sync_and_push.py` a cada ciclo de sincronização.

---

## 📂 Estrutura de Saída

Cada capítulo traduzido é salvo como:
```
output/<COLEÇÃO>/<LIVRO>_<CAPITULO>.json
```

Cada versículo dentro do arquivo JSON tem o formato:
```json
{{
  "verse": 1,
  "original": "texto no idioma original (Hebraico, Grego, etc.)",
  "translation": "tradução em Português do Brasil"
}}
```
"""

    with open("PROGRESS.md", "w", encoding="utf-8") as f:
        f.write(md)

    safe_msg = f"PROGRESS.md gerado! ({total_output}/{total_data} capitulos traduzidos, ETA: {eta_str})"
    try:
        print(f"OK: {safe_msg}")
    except UnicodeEncodeError:
        sys.stdout.buffer.write((safe_msg + "\n").encode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
