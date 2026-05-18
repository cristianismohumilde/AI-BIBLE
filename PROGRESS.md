# 📊 PROGRESS — AI-BIBLE Translation Status

> Gerado automaticamente em: **2026-05-18 23:03 UTC**
> Velocidade estimada: ~15 capítulos/hora com Double-Pass Review ativo.

---

## 📈 Progresso Geral

`░░░░░░░░░░░░░░░░░░░░` 1.1%

**47** de **4,475** capítulos traduzidos.
**ETA estimado:** ~12d 7h

---

## 📋 Detalhamento por Coleção

| Coleção | Idioma Original | Capítulos Fonte | Traduzidos | Progresso | Status |
| :--- | :--- | ---: | ---: | :--- | :--- |
| 📜 Códice de Aleppo | Hebraico Massorético Antigo | 928 | 47 | `█░░░░░░░░░░░░░░░░░░░` 5.1% | 🚀 Em andamento |
| 📜 Texto de Leningrado (WLC) | Hebraico Massorético | 928 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| 🏛️ Septuaginta (LXX) | Grego Clássico | 1,135 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| 🪨 Manuscritos do Mar Morto | Hebraico/Aramaico Antigo | 928 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| ✝️ Textus Receptus (TR) | Grego Koiné | 260 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| ✝️ Texto Bizantino (BYZ) | Grego Koiné | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |
| ✝️ Texto Crítico (SBLGNT) | Grego Koiné | 260 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| 📚 Talmud Bavli | Hebraico Mishnaico / Aramaico | 36 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| 📜 Targum Onkelos | Aramaico Antigo | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |
| 📖 Peshitta Siríaca | Siríaco Clássico | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |
| 🔤 Versão Copta Saídica | Copta Saídico | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |
| 🏔️ Versão Armênia Oriental | Armênio Clássico | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |

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
{
  "verse": 1,
  "original": "texto no idioma original (Hebraico, Grego, etc.)",
  "translation": "tradução em Português do Brasil"
}
```
