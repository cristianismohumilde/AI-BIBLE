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
}


def count_files_recursive(directory):
    """Conta recursivamente todos os arquivos .json em um diretório."""
    if not os.path.isdir(directory):
        return 0
    count = 0
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(".json"):
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
    Para coleções com livros em sub-pastas (WLC, LXX, Aleppo etc.),
    percorre recursivamente. Para arquivos planos na pasta raiz, conta direto.
    """
    if collection == "VUL":
        if os.path.exists(os.path.join(DATA_DIR, "VUL", "vulgata_latina.txt")):
            return 1189

    # Mapeamento para as Versões Antigas em data/ancient_versions/
    ancient_map = {
        "Targum_Onkelos": "targum_onkelos_genesis",
        "Peshitta_Syriac": "peshitta_syriac",
        "Coptic_Sahidic": "coptic_sahidic",
        "Armenian_Eastern": "armenian_eastern"
    }

    if collection in ancient_map:
        subkey = ancient_map[collection]
        av_path = os.path.join(DATA_DIR, "ancient_versions", subkey)
        if os.path.isdir(av_path):
            total = count_files_recursive(av_path)
            return total if total > 0 else (1 if os.path.exists(av_path) else 0)
        else:
            candidates = [av_path + ".json", av_path]
            found = any(os.path.exists(c) and os.path.getsize(c) > 512 for c in candidates)
            if collection == "Targum_Onkelos":
                av_dir = os.path.join(DATA_DIR, "ancient_versions")
                return sum(1 for f in os.listdir(av_dir) if f.startswith("targum_onkelos") and f.endswith(".json")) if os.path.isdir(av_dir) else 0
            return 1 if found else 0

    data_path = os.path.join(DATA_DIR, collection)
    if not os.path.isdir(data_path):
        return 0
    # Conta todos os .json recursivamente
    total = 0
    for root, dirs, files in os.walk(data_path):
        for f in files:
            if f.endswith(".json"):
                total += 1
    return total


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
