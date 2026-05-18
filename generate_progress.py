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
    "Talmud":          ("📚 Talmud Bavli",               "Hebraico Mishnaico / Aramaico"),
    "Targum_Onkelos":  ("📜 Targum Onkelos",             "Aramaico Antigo"),
    "Peshitta_Syriac": ("📖 Peshitta Siríaca",           "Siríaco Clássico"),
    "Coptic_Sahidic":  ("🔤 Versão Copta Saídica",       "Copta Saídico"),
    "Armenian_Eastern":("🏔️ Versão Armênia Oriental",    "Armênio Clássico"),
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
    data_path = os.path.join(DATA_DIR, collection)
    if collection == "VUL" and os.path.exists(os.path.join(data_path, "vulgata_latina.txt")):
        return 1189
        
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

    # Estimativa de tempo restante (baseado em 19.000 versículos/dia = ~19000 capítulos/24h mas estimamos por capítulo)
    remaining = total_data - total_output
    # Velocidade aproximada: 15 capítulos por hora (sem dados reais, usamos estimativa conservadora)
    hours_remaining = remaining / 15 if remaining > 0 else 0
    days = int(hours_remaining // 24)
    hours = int(hours_remaining % 24)
    eta_str = f"~{days}d {hours}h" if remaining > 0 else "🎉 Concluído!"
    
    # Custo (assumindo ~$1.00 USD/hora na cloud)
    custo_total = int(hours_remaining * 1.00)
    custo_str = f"~${custo_total} USD" if remaining > 0 else "$0"

    md = f"""# 📊 PROGRESS — AI-BIBLE Translation Status

> Gerado automaticamente em: **{now}**
> Velocidade estimada: ~15 capítulos/hora com Double-Pass Review ativo.

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
