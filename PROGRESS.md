# 📊 PROGRESS — AI-BIBLE Translation Status

> Gerado automaticamente em: **2026-05-22 17:30 UTC**
> Velocidade estimada: ~26 capítulos/hora com Double-Pass Review concorrente ativo.

---

## 📈 Progresso Geral

`████████████████░░░░` 80.9%

**2,415** de **2,985** capítulos traduzidos.
**ETA estimado:** ~0d 21h
**Custo Computacional Restante:** ~$32 USD

---

## 📋 Detalhamento por Coleção

| Coleção | Idioma Original | Capítulos Fonte | Traduzidos | Progresso | Status |
| :--- | :--- | ---: | ---: | :--- | :--- |
| 📜 Códice de Aleppo | Hebraico Massorético Antigo | 928 | 928 | `████████████████████` 100.0% | ✅ Completo |
| 🏛️ Septuaginta (LXX) | Grego Clássico | 389 | 389 | `████████████████████` 100.0% | ✅ Completo |
| 🪨 Manuscritos do Mar Morto | Hebraico/Aramaico Antigo | 127 | 127 | `████████████████████` 100.0% | ✅ Completo |
| 📜 Apócrifos (4 Esdras / VUL) | Latim Clássico (Vulgata) | 18 | 16 | `█████████████████░░░` 88.9% | 🚀 Em andamento |
| ✝️ Texto Bizantino (BYZ) | Grego Koiné | 260 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| 📜 Targum Onkelos | Aramaico Antigo | 187 | 50 | `█████░░░░░░░░░░░░░░░` 26.7% | 🚀 Em andamento |
| 📖 Peshitta Siríaca | Siríaco Clássico | 260 | 260 | `████████████████████` 100.0% | ✅ Completo |
| 🔤 Versão Copta Saídica | Copta Saídico | 260 | 260 | `████████████████████` 100.0% | ✅ Completo |
| 🏔️ Versão Armênia Oriental | Armênio Clássico | 260 | 89 | `██████░░░░░░░░░░░░░░` 34.2% | 🚀 Em andamento |
| 🇪🇹 Versão Ge'ez (Etíope) | Ge'ez (Etíope Clássico) | 296 | 296 | `████████████████████` 100.0% | ✅ Completo |
| 📖 Talmud Bavli | Aramaico / Hebraico Rabínico | — | — | `░░░░░░░░░░░░░░░░░░░░` — | ❌ Sem orçamento |
| 📜 WLC (Texto de Leningrado) | Hebraico Massorético | 929 | — | `░░░░░░░░░░░░░░░░░░░░` — | ❌ Sem orçamento |
| 🏛️ Textus Receptus (TR) | Grego Koiné | 260 | — | `░░░░░░░░░░░░░░░░░░░░` — | ❌ Sem orçamento |
| 🔬 SBLGNT | Grego Koiné Crítico | 260 | — | `░░░░░░░░░░░░░░░░░░░░` — | ❌ Sem orçamento |

---

## 📜 Manuscritos Apócrifos e Históricos (Fase 4)
Os seguintes textos já estão baixados e preservados na pasta `data/apocrypha/` aguardando expansão do projeto:
- **Livro de Enoque** (Edição Crítica de R.H. Charles)
- **Livro dos Jubileus** (Etiópico Clássico)
- **Testamento dos Doze Patriarcas** (Grego Antigo)
- **4 Esdras (Vulgata)** (já estruturado em JSON)
- **Mishná: Berakhot** (Sefaria API)
*(A Didaquê está programada para download)*

---

## 🔄 Como atualizar este arquivo

```bash
python generate_progress.py
```

O arquivo é atualizado automaticamente pelo `vm_autopush.py` a cada ciclo de sincronização.

---

## 📂 Estrutura de Saída

Cada capítulo traduzido é salvo como:
```
output/<COLEÇÃO>/<LIVRO>_<CAPITULO>.json
```

Cada versículo dentro do arquivo JSON tem o formato:
```json
{
  "verse": 1,
  "original": "texto no idioma original (Hebraico, Grego, etc.)",
  "translation": "tradução em Português do Brasil"
}
```
