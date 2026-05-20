# 📊 PROGRESS — AI-BIBLE Translation Status

> Gerado automaticamente em: **2026-05-20 07:02 UTC**
> Velocidade estimada: ~26 capítulos/hora com Double-Pass Review concorrente ativo.

---

## 📈 Progresso Geral

`███████░░░░░░░░░░░░░` 36.4%

**939** de **2,580** capítulos traduzidos.
**ETA estimado:** ~2d 15h
**Custo Computacional Restante:** ~$94 USD

---

## 📋 Detalhamento por Coleção

| Coleção | Idioma Original | Capítulos Fonte | Traduzidos | Progresso | Status |
| :--- | :--- | ---: | ---: | :--- | :--- |
| 📜 Códice de Aleppo | Hebraico Massorético Antigo | 928 | 928 | `████████████████████` 100.0% | ✅ Completo |
| 📜 Texto de Leningrado (WLC) | Hebraico Massorético | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |
| 🏛️ Septuaginta (LXX) | Grego Clássico | 389 | 11 | `░░░░░░░░░░░░░░░░░░░░` 2.8% | 🚀 Em andamento |
| 🪨 Manuscritos do Mar Morto | Hebraico/Aramaico Antigo | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |
| ✝️ Textus Receptus (TR) | Grego Koiné | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |
| ✝️ Texto Bizantino (BYZ) | Grego Koiné | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |
| ✝️ Texto Crítico (SBLGNT) | Grego Koiné | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |
| 🏛️ Vulgata Latina | Latim | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |
| 📜 Targum Onkelos | Aramaico Antigo | 187 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| 📖 Peshitta Siríaca | Siríaco Clássico | 260 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| 🔤 Versão Copta Saídica | Copta Saídico | 260 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| 🏔️ Versão Armênia Oriental | Armênio Clássico | 260 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |
| 📚 Talmud Bavli | Hebraico Mishnaico / Aramaico | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (sem dados) | ❌ Sem dados |
| 🇪🇹 Versão Ge'ez (Etíope) | Ge'ez (Etíope Clássico) | 296 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Aguardando |

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
