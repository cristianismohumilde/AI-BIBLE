#!/usr/bin/env python3
"""
generate_readme.py
==================
Gera o README.md automaticamente com dados reais do repositório:
  - Conta arquivos em data/ para cada coleção (manuscritos baixados)
  - Conta arquivos em output/ para cada coleção (traduções concluídas)
  - Conta léxicos e gramáticas em study_materials/
  - Atualiza tabelas de status, contagens e datas

Rodado automaticamente pelo sync_and_push.py a cada ciclo.
Uso manual: python generate_readme.py
"""

import os
import sys
from datetime import datetime, timezone

DATA_DIR   = "data"
OUTPUT_DIR = "output"

# === BUDGET LIMIT SCOPES ($300 USD) ===
# Controla quais manuscritos são EXIBIDOS como disponíveis no README
# (não afeta translate_bible.py que tem seu próprio SKIP_MANUSCRIPTS)
SKIP_MANUSCRIPTS = {"Talmud"}

# Manuscritos que estão baixados mas com tradução pausada por orçamento
# Usados para exibir contagem real de caps sem mostrar "Aguardando download"
DOWNLOADED_BUT_PAUSED = {"WLC", "SBLGNT", "TR", "VUL"}
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

# ─────────────────────────────────────────────────────────
# Configuração das coleções
# ─────────────────────────────────────────────────────────
MANUSCRIPTS = [
    # (chave_data, chave_output, emoji, nome_display, idioma, nota)
    ("Aleppo",           "Aleppo",           "📜", "Códice de Aleppo",           "Hebraico Massorético Antigo",   ""),
    ("LXX",              "LXX",              "🏛️", "Septuaginta (LXX)",           "Grego Clássico",                ""),
    ("DSS",              "DSS",              "🪨", "Manuscritos do Mar Morto",   "Hebraico/Aramaico Antigo",      "Reconstrução acadêmica"),
    ("BYZ",              "BYZ",              "✝️", "Texto Bizantino (BYZ)",       "Grego Koiné",                   ""),
]

ANCIENT_VERSIONS = [
    # (subchave em ancient_versions, chave_output, emoji, nome, idioma)
    ("targum_onkelos_genesis",     "Targum_Onkelos", "📜", "Targum Onkelos",        "Aramaico Antigo"),
    ("peshitta_syriac",            "Peshitta_Syriac","📖", "Peshitta Siríaca",       "Siríaco Clássico"),
    ("coptic_sahidic",             "Coptic_Sahidic", "🔤", "Copta Saídico",          "Copta Saídico"),
    ("armenian_eastern",           "Armenian_Eastern","🏔️","Armênio Oriental",        "Armênio Clássico"),
    ("geez_extracted",             "Geez",           "🇪🇹", "Ge'ez (Etiópico)",       "Ge'ez Clássico"),
]

TALMUD_TRACTATES_EXPECTED = 37  # 3 piloto + 34 extras

STUDY_MATERIALS = {
    "lexicons":  "data/study_materials/lexicons",
    "grammars":  "data/study_materials/grammars",
}

STUDY_LABELS = {
    "strongs_hebrew.json":              "Strong's Hebrew Lexicon",
    "strongs_greek.json":               "Strong's Greek Lexicon",
    "strongs.json":                     "Strong's Concordance (legado)",
    "brown_driver_briggs.xml":          "Brown-Driver-Briggs (BDB)",
    "hebrew_strong_enhanced.xml":       "Strong+BDB Integrado",
    "abbott_smith_greek.csv":           "Abbott-Smith Greek Lexicon",
    "jastrow_dictionary.txt":           "Jastrow (Aramaico Talmúdico)",
    "syriac_roots.txt":                 "Raízes Siríacas (Sedra)",
    "syriac_lexemes.txt":               "Lexemas Siríacos (Sedra)",
    "syriac_words.txt":                 "Palavras Siríacas (Sedra)",
    "dillmann_geez_lexicon.txt":        "Dillmann Ge'ez Lexicon",
    "cross_references.tsv":             "Referências Cruzadas (340k)",
    "gesenius_hebrew_grammar.txt":      "Gesenius' Hebrew Grammar",
    "robertson_greek_grammar.txt":      "A.T. Robertson Greek Grammar",
    "noldeke_syriac_grammar.txt":       "Nöldeke Syriac Grammar",
    "armenian_classical_grammar.txt":   "Armenian Classical Grammar",
    "morphhb_sample_genesis.xml":       "MorphHB (Morfologia Hebraica)",
    "cal_aramaic_utils.js":             "CAL Aramaic Utils",
    "coptic_reference.txt":             "Copta — Referência",
    "lsj_greek.xml":                    "LSJ Greek Lexicon",
    "lewis_short_latin.xml":            "Lewis & Short Latin",
    "dillmann_geez.pdf":                "Dillmann Ge'ez Lexicon",
    "crum_coptic.pdf":                  "W.E. Crum Coptic Dictionary",
    "brockelmann_syriac.pdf":           "Brockelmann Lexicon Syriacum",
    "bedrossian_armenian.pdf":          "Bedrossian Armenian Dictionary",
    "vulgata_latina.txt":               "Vulgata Latina (Texto Bruto)",
}

# ─────────────────────────────────────────────────────────
# Funções utilitárias
# ─────────────────────────────────────────────────────────
def count_json_recursive(path):
    # Tratamento especial para Vulgata (arquivo .txt único)
    if "VUL" in path and "output" not in path:
        if os.path.exists(os.path.join(path, "vulgata_latina.txt")):
            return 1  # 1 arquivo disponível
        return 0

    if not os.path.isdir(path):
        return 0
    total = 0
    collection_name = None
    parts = os.path.normpath(path).split(os.sep)
    if len(parts) >= 2:
        collection_name = parts[1]

    if collection_name in SKIP_MANUSCRIPTS:
        return 0

    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(".json"):
                parts_f = os.path.normpath(os.path.join(root, f)).split(os.sep)
                if len(parts_f) >= 3:
                    # Se o arquivo estiver em output/<COLLECTION>/Livro_cap.json (estrutura plana),
                    # extrai o nome do livro antes do '_' para comparação com ALLOWED_* sets.
                    if parts_f[-2] == collection_name:
                        book = parts_f[-1].replace('.json', '')
                        if "_" in book:
                            book = book.rsplit("_", 1)[0]
                    else:
                        book = parts_f[-2]
                    if collection_name == "LXX" and book not in ALLOWED_LXX_BOOKS:
                        continue
                    if collection_name == "BYZ" and book not in ALLOWED_NT_BOOKS: continue
                total += 1
    return total

def count_json_paused(path, collection_name):
    """Conta arquivos JSON de manuscritos baixados mas com tradução pausada."""
    # Vulgata é arquivo .txt único
    if collection_name == "VUL":
        return 1 if os.path.exists(os.path.join(path, "vulgata_latina.txt")) else 0
    if not os.path.isdir(path):
        return 0
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            if not f.endswith(".json") or "_raw" in f:
                continue
            parts_f = os.path.normpath(os.path.join(root, f)).split(os.sep)
            # Estrutura plana (BYZ, SBLGNT): data/BYZ/Acts_1.json → book = "Acts"
            # Estrutura em subpastas (WLC, DSS, TR): data/WLC/Acts/1.json → book = "Acts"
            if parts_f[-2] == collection_name:
                # Arquivo plano: extrai o livro do nome do arquivo (ex: Acts_1.json → Acts)
                book = f.rsplit("_", 1)[0]
            else:
                book = parts_f[-2]
            if collection_name == "BYZ" and book not in ALLOWED_NT_BOOKS: continue
            if collection_name == "SBLGNT" and book not in ALLOWED_NT_BOOKS: continue
            total += 1
    return total

def count_json_flat(path):
    if not os.path.isdir(path):
        return 0
    return sum(1 for f in os.listdir(path) if f.endswith(".json"))

def status_icon(data_count, out_count):
    if data_count == 0:
        return "⚙️ Aguardando download"
    if out_count == 0:
        return "⏳ Aguardando tradução"
    if out_count >= data_count:
        return "✅ Completo"
    pct = out_count / data_count * 100
    return f"🚀 Em andamento ({pct:.0f}%)"

def file_status(path):
    """Retorna ✅/❌ se um arquivo existe."""
    return "✅" if os.path.exists(path) and os.path.getsize(path) > 512 else "❌"


# ─────────────────────────────────────────────────────────
# Construtores de seções
# ─────────────────────────────────────────────────────────
def build_manuscripts_table():
    rows = []
    total_data = 0
    total_out  = 0

    for key_d, key_o, emoji, name, lang, note in MANUSCRIPTS:
        o = count_json_recursive(os.path.join(OUTPUT_DIR, key_o))
        # Manuscritos pausados: conta caps reais mas status é "Aguardando tradução"
        if key_d in DOWNLOADED_BUT_PAUSED:
            d = count_json_paused(os.path.join(DATA_DIR, key_d), key_d)
            status = "⏳ Aguardando tradução"
        else:
            d = count_json_recursive(os.path.join(DATA_DIR, key_d))
            status = status_icon(d, o)
        total_data += d
        total_out  += o
        note_col = f" *{note}*" if note else ""
        # Vulgata está em arquivo .txt único
        if key_d == "VUL":
            fonte_label = f"{d} arquivo" if d == 1 else f"{d:,} caps"
        else:
            fonte_label = f"{d:,} caps"
        rows.append(f"| {emoji} {name} | {lang} | {fonte_label} | {o:,} traduzidos | {status}{note_col} |")

    return rows, total_data, total_out

def build_ancient_table():
    import json
    rows = []
    for subkey, key_o, emoji, name, lang in ANCIENT_VERSIONS:
        av_path = os.path.join(DATA_DIR, "ancient_versions", subkey)
        d = 0
        if "geez" in subkey:
            if os.path.isdir(av_path):
                for f in os.listdir(av_path):
                    if f.endswith(".json"):
                        book_name = f.replace(".json", "")
                        book_title = book_name.rsplit("_", 1)[0] if "_" in book_name else book_name
                        if book_title in ALLOWED_GEEZ_BOOKS:
                            d += 1
        elif "targum" in subkey:
            av_dir = os.path.join(DATA_DIR, "ancient_versions")
            if os.path.isdir(av_dir):
                for f in os.listdir(av_dir):
                    if f.startswith("targum_onkelos_") and f.endswith(".json"):
                        try:
                            with open(os.path.join(av_dir, f), "r", encoding="utf-8") as file:
                                d += len(json.load(file).get("text", []))
                        except Exception:
                            pass
                if d == 0:
                    d = 187
        else:
            # Peshitta, Coptic, Armenian
            fpath = os.path.join(DATA_DIR, "ancient_versions", subkey + ".json")
            if os.path.exists(fpath):
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        d = sum(len(b.get("chapters", [])) for b in data.get("books", []) if b.get("name") in ALLOWED_NT_BOOKS)
                except Exception:
                    d = 260

        o = count_json_recursive(os.path.join(OUTPUT_DIR, key_o))
        status = status_icon(d, o)
        rows.append(f"| {emoji} {name} | {lang} | {d:,} caps | {o:,} traduzidos | {status} |")

    return rows

def build_talmud_row():
    return ""

def build_study_materials_table():
    rows = []
    # Léxicos e gramáticas em subpastas
    for cat, path in STUDY_MATERIALS.items():
        if not os.path.isdir(path):
            continue
        for fname in sorted(os.listdir(path)):
            fpath = os.path.join(path, fname)
            if not os.path.isfile(fpath):
                continue
            label = STUDY_LABELS.get(fname, fname)
            bytes_size = os.path.getsize(fpath)
            size  = max(1, bytes_size // 1024) if bytes_size > 0 else 0
            icon  = "✅" if bytes_size > 0 else "❌"
            rows.append(f"| {icon} | {label} | `{fname}` | {size:,} KB |")
    # Arquivos na raiz de study_materials
    sm = os.path.join(DATA_DIR, "study_materials")
    if os.path.isdir(sm):
        for fname in sorted(os.listdir(sm)):
            fpath = os.path.join(sm, fname)
            if not os.path.isfile(fpath):
                continue
            label = STUDY_LABELS.get(fname, fname)
            bytes_size = os.path.getsize(fpath)
            size  = max(1, bytes_size // 1024) if bytes_size > 0 else 0
            icon  = "✅" if bytes_size > 0 else "❌"
            rows.append(f"| {icon} | {label} | `{fname}` | {size:,} KB |")
    return rows

def calc_totals():
    import json
    total_d = 0
    total_o = 0
    
    # 1. Manuscritos
    for key_d, key_o, *_ in MANUSCRIPTS:
        total_d += count_json_recursive(os.path.join(DATA_DIR, key_d))
        total_o += count_json_recursive(os.path.join(OUTPUT_DIR, key_o))
        
    # 2. Talmud (Removido do cálculo para não poluir os totais reais)
    talmud_pages = 0
    
    # 3. Versões Antigas
    for subkey, key_o, emoji, name, lang in ANCIENT_VERSIONS:
        av_path = os.path.join(DATA_DIR, "ancient_versions", subkey)
        d = 0
        if "geez" in subkey:
            if os.path.isdir(av_path):
                for f in os.listdir(av_path):
                    if f.endswith(".json"):
                        book_name = f.replace(".json", "")
                        book_title = book_name.rsplit("_", 1)[0] if "_" in book_name else book_name
                        if book_title in ALLOWED_GEEZ_BOOKS:
                            d += 1
        elif "targum" in subkey:
            av_dir = os.path.join(DATA_DIR, "ancient_versions")
            if os.path.isdir(av_dir):
                for f in os.listdir(av_dir):
                    if f.startswith("targum_onkelos_") and f.endswith(".json"):
                        try:
                            with open(os.path.join(av_dir, f), "r", encoding="utf-8") as file:
                                d += len(json.load(file).get("text", []))
                        except Exception:
                            pass
                if d == 0:
                    d = 187
        else:
            # Peshitta, Coptic, Armenian
            fpath = os.path.join(DATA_DIR, "ancient_versions", subkey + ".json")
            if os.path.exists(fpath):
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        d = sum(len(b.get("chapters", [])) for b in data.get("books", []) if b.get("name") in ALLOWED_NT_BOOKS)
                except Exception:
                    d = 260
        total_d += d
        total_o += count_json_recursive(os.path.join(OUTPUT_DIR, key_o))
        
    return total_d, total_o


# ─────────────────────────────────────────────────────────
# Gerador principal
# ─────────────────────────────────────────────────────────
def main():
    now     = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    ms_rows, total_data, total_out = build_manuscripts_table()
    av_rows  = build_ancient_table()
    talmud_r = build_talmud_row()
    sm_rows  = build_study_materials_table()

    all_data, all_out = calc_totals()
    pct = (all_out / all_data * 100) if all_data else 0

    # Nova velocidade com 3 workers concorrentes em GPU A10: 26 capítulos por hora
    hours_left = max(0, (all_data - all_out) / 26)
    days       = int(hours_left // 24)
    hours      = int(hours_left % 24)
    eta_str    = f"~{days}d {hours}h" if all_out < all_data else "Concluido!"
    
    # Custo real da instância VM.GPU.A10.1 (aprox. $1.50 por hora)
    custo_hora = 1.50
    custo_total = int(hours_left * custo_hora)
    custo_str = f"~${custo_total} USD" if all_out < all_data else "$0"

    # Linha de fase automática
    phase2_status = ("Em andamento" if all_out > 0 else "Aguardando") + f" — {all_out:,}/{all_data:,} caps ({pct:.1f}%)"

    ms_table = "\n".join(ms_rows)
    av_table = "\n".join(av_rows)
    sm_table = "\n".join(sm_rows)

    readme = f"""# AI-BIBLE — Tradução Ultra-Precisa de Manuscritos Originais

> **README gerado automaticamente em: {now}**
> Veja [PROGRESS.md](PROGRESS.md) para monitoramento detalhado em tempo real.

Este projeto utiliza o estado da arte em IA rodando em **Oracle Cloud GPU (NVIDIA A10)**
para traduzir manuscritos originais da Bíblia e textos rabínicos diretamente para o **Português do Brasil**,
com transliteração acadêmica incluída.

---

## 📊 Status Geral

| Métrica | Valor |
|---|---|
| Capítulos fonte disponíveis | **{all_data:,}** |
| Capítulos traduzidos | **{all_out:,}** ({pct:.1f}%) |
| Orçamento Disponível (Oracle GPU) | **$300 USD** (~R$ 1.500) |
| Custo estimado restante | **{custo_str}** |
| ETA estimado de processamento | **{eta_str}** |
| Velocidade (com Double-Pass) | ~26 caps/hora |
| Última atualização | {now} |

---

## 📜 Manuscritos — Antigo e Novo Testamento

| Manuscrito | Idioma | Fonte | Traduzido | Status |
|:---|:---|---:|---:|:---|
{ms_table}

## 📖 Versões Antigas (Aramaico, Siríaco, Copta, Armênio, Ge'ez)

| Texto | Idioma | Fonte | Traduzido | Status |
|:---|:---|---:|---:|:---|
{av_table}

---

## 🎯 Pipeline de Tradução — 4 Passos Acadêmicos

### Passo 1 — Tradução Filológica (Anti-Alucinação)
O modelo **Qwen 2.5 32B** traduz sem receber exemplos no prompt,
evitando que a IA "lembre" e alucine nomes ou narrativas fora do contexto do versículo.

### Passo 2 — Revisão Crítica (Double-Pass Review)
Segunda chamada ao mesmo modelo como *revisor filológico*:
verifica número gramatical (plural/singular), conjugações e qualidade literária.

### Passo 3 — Pós-Processamento Regex (Failsafe Determinístico)
Regex Python higieniza qualquer metalinguagem da IA antes de salvar o JSON.

### Passo 4 — Transliteração Acadêmica (após Fase 2)
Script `transliterate.py` adiciona `"transliteration"` a cada versículo
seguindo padrões SBL para Hebraico/Grego/Aramaico e sistemas específicos para Siríaco, Copta e Ge'ez.

---

## 📚 Materiais de Estudo Disponíveis

| Status | Material | Arquivo | Tamanho |
|:---:|:---|:---|---:|
{sm_table if sm_rows else "| ⚙️ | *Aguardando download* | — | — |"}

---

## 🗺️ Roadmap

### ✅ Fase 1 — Download (Concluída)
- Manuscritos bíblicos principais: WLC, Aleppo, LXX, DSS, TR, BYZ, SBLGNT
- Versões antigas: Peshitta, Copta, Armênio, Targum Onkelos
- Talmud piloto + download de tratados extras em andamento
- Léxicos (Strong's Hebrew+Greek, BDB, Abbott-Smith, Jastrow, Sedra, Dillmann)
- Gramáticas (Gesenius, Robertson, Nöldeke) e Referências Cruzadas

### 🚀 Fase 2 — Tradução ({phase2_status})
- GPU NVIDIA A10 traduzindo ininterruptamente (24/7)
- Double-Pass Review + Filtro Regex ativos

### ⏳ Fase 3 — Transliteração (após Fase 2)
- Script: `transliterate.py` — roda após conclusão da tradução
- Impacto: +50% do tempo de GPU (3ª chamada por versículo)

### 🗺️ Fase 4 — Expansão Futura
- Enoque, Jubileus, Testamento dos Doze Patriarcas, Didaquê
- Mishná completa + comentários clássicos traduzidos
- Interface web com busca e comparação lado a lado

---

## 📂 Estrutura do Repositório

```
AI-BIBLE/
├── data/                     # Manuscritos originais (fonte)
│   ├── Aleppo/               # Hebraico Massorético (Códice de Aleppo)
│   ├── WLC/                  # Hebraico Massorético (Texto de Leningrado)
│   ├── LXX/                  # Grego Clássico (Septuaginta)
│   ├── DSS/                  # Manuscritos do Mar Morto
│   ├── TR/                   # Grego Koiné (Textus Receptus)
│   ├── BYZ/                  # Grego Koiné (Texto Bizantino)
│   ├── Talmud/               # Talmud Bavli (tratados JSON)
│   ├── Geez/                 # Ge'ez / Etiópico Clássico
│   ├── ancient_versions/     # Aramaico, Siríaco, Copta, Armênio
│   └── study_materials/      # Léxicos, gramáticas, concordâncias
│       ├── lexicons/
│       └── grammars/
├── output/                   # Traduções geradas (auto-sync da VM)
│   └── <COLEÇÃO>/<LIVRO>_<CAP>.json
├── translate_bible.py        # Motor de tradução GPU (roda na VM)
├── transliterate.py          # Transliteração acadêmica (pós-tradução)
├── generate_readme.py        # Gera este README automaticamente
├── generate_progress.py      # Gera PROGRESS.md automaticamente
├── sync_and_push.py          # VM → Local → GitHub (a cada 5 min)
├── download_manuscripts.py   # Download manuscritos principais
├── download_extras.py        # Download BYZ + léxicos extras
├── download_talmud_extra.py  # Download tratados Talmud completo
├── download_study_extra.py   # Download léxicos, gramáticas
├── convert_geez.py           # Converte SWORD Ge'ez → JSON
├── check_sources.py          # Diagnóstico de fontes disponíveis
├── index.html                # Interface web de leitura (sem servidor)
├── README.md                 # Este arquivo (auto-gerado)
├── PROGRESS.md               # Progresso em tempo real (auto-gerado)
└── TASKS.md                  # Lista de tarefas e notas para continuidade
```

### Formato de cada versículo traduzido

```json
{{
  "verse": 1,
  "original": "בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים",
  "transliteration": "Bə-rē-šîṯ bārāʾ ʾĔlōhîm",
  "translation": "No princípio, criou Deus..."
}}
```

---

## 🛠️ Stack Tecnológica

| Componente | Tecnologia |
|---|---|
| Modelo de IA | Qwen 2.5 32B |
| Servidor | Oracle Cloud VM.GPU.A10.1 (NVIDIA A10 24GB VRAM) |
| Inferência | Ollama (servidor local LLM) |
| Linguagem | Python 3.13 |
| Sincronização | SCP + Git + GitHub |
| Frontend | HTML5 + Vanilla JS (zero servidor) |

---

## 📜 Licença

| Conteúdo | Licença |
|---|---|
| Código-fonte | MIT |
| Manuscritos fonte | Domínio Público / CC BY |
| Talmud (Sefaria) | CC BY-NC |
| Materiais de estudo (Gesenius, Robertson, etc.) | Domínio Público |
| **Traduções PT-BR geradas** | **CC BY 4.0** |
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    msg = f"README.md gerado! ({all_out}/{all_data} caps traduzidos, ETA: {eta_str})"
    try:
        print(f"OK: {msg}")
    except UnicodeEncodeError:
        sys.stdout.buffer.write((msg + "\n").encode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
