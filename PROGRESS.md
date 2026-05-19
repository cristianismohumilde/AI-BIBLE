# 📊 PROGRESS — AI-BIBLE Translation Status

> Gerado automaticamente em: **2026-05-19 00:54 UTC**
> Velocidade estimada: ~15 capítulos/hora com Double-Pass Review ativo.

---

## 📈 Progresso Geral

`░░░░░░░░░░░░░░░░░░░░` 1.3%

**77** de **5,924** capítulos traduzidos.
**ETA estimado:** ~16d 5h
**Custo Computacional Restante:** ~$389 USD

---

## 📋 Detalhamento por Coleção

| Coleção | Idioma Original | Capítulos Fonte | Traduzidos | Progresso | Status |
| :--- | :--- | ---: | ---: | :--- | :--- |
| 📜 Códice de Aleppo | Hebraico Massorético Antigo | 928 | 77 | `█░░░░░░░░░░░░░░░░░░░` 8.3% | 🚀 Em andamento |
| 📜 Texto de Leningrado (WLC) | Hebraico Massorético | 928 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| 🏛️ Septuaginta (LXX) | Grego Clássico | 1,135 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| 🪨 Manuscritos do Mar Morto | Hebraico/Aramaico Antigo | 928 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| ✝️ Textus Receptus (TR) | Grego Koiné | 260 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| ✝️ Texto Bizantino (BYZ) | Grego Koiné | 260 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| ✝️ Texto Crítico (SBLGNT) | Grego Koiné | 260 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| 🏛️ Vulgata Latina | Latim | 1,189 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| 📜 Targum Onkelos | Aramaico Antigo | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |
| 📖 Peshitta Siríaca | Siríaco Clássico | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |
| 🔤 Versão Copta Saídica | Copta Saídico | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |
| 🏔️ Versão Armênia Oriental | Armênio Clássico | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |
| 📚 Talmud Bavli | Hebraico Mishnaico / Aramaico | 36 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |

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
{
  "verse": 1,
  "original": "texto no idioma original (Hebraico, Grego, etc.)",
  "translation": "tradução em Português do Brasil"
}
```
