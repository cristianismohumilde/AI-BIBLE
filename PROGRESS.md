# 📊 PROGRESS — AI-BIBLE Translation Status

> 💰 **Crédito Oracle Cloud Disponibilizado**: **$300 USD** (~R$ 1.500) — Recurso que foi fornecido para este projeto.
> Gerado automaticamente em: **2026-05-19 13:49 UTC**
> Velocidade estimada: ~26 capítulos/hora com Double-Pass Review concorrente ativo.

---

## 📈 Progresso Geral

`██░░░░░░░░░░░░░░░░░░` 14.4%

**372** de **2,577** capítulos traduzidos.
**ETA estimado:** ~3d 12h
**Custo Computacional Restante:** ~$127 USD

---

## 📋 Detalhamento por Coleção

| Coleção | Idioma Original | Capítulos Fonte | Traduzidos | Progresso | Status | Prioridade |
| :--- | :--- | ---: | ---: | :--- | :--- | :--- |
| 📜 Códice de Aleppo | Hebraico Massorético Antigo | 928 | 372 | `████████░░░░░░░░░░░░` 40.1% | 🚀 Em andamento | ⭐⭐⭐ Atual |
| 🏛️ Septuaginta Selecionada | Grego Clássico | 120 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Próxima | ⭐⭐⭐ Nº 1 |
| 🇪🇹 Ge'ez Selecionado | Ge'ez Clássico | 90 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Planejada | ⭐⭐⭐ Nº 2 |
| 🪨 Manuscritos do Mar Morto | Hebraico/Aramaico Antigo | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ (Pesquisa) | ⚙️ Pesquisa | ⭐⭐ Nº 3 |
| 📜 Targum Onkelos | Aramaico Antigo | 187 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Planejada | ⭐⭐ Nº 4 |
| ✝️ Texto Bizantino NT | Grego Koiné | 260 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Planejada | ⭐⭐ Nº 5 |
| 📖 Peshitta Siríaca NT | Siríaco Clássico | 260 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Planejada | ⭐⭐ Nº 6 |
| 🔤 Versão Copta Sahídica NT | Copta Sahídico | 260 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Planejada | ⭐⭐ Nº 7 |
| 🏔️ Versão Armênia Oriental NT | Armênio Clássico | 260 | 0 | `░░░░░░░░░░░░░░░░░░░░` 0.0% | ⏳ Planejada | ⭐⭐ Nº 8 |
| 📜 Texto de Leningrado (WLC) | Hebraico Massorético | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ | ❌ Fora dos Recursos | ⭐ *Pausado* |
| ✝️ Textus Receptus (TR) | Grego Koiné | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ | ❌ Fora dos Recursos | ⭐ *Pausado* |
| ✝️ Texto Crítico (SBLGNT) | Grego Koiné | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ | ❌ Fora dos Recursos | ⭐ *Pausado* |
| 🏛️ Vulgata Latina | Latim | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ | ❌ Fora dos Recursos | ⭐ *Pausado* |
| 📚 Talmud Bavli | Hebraico Mishnaico / Aramaico | 0 | 0 | ░░░░░░░░░░░░░░░░░░░░ | ❌ Fora dos Recursos | ⭐ *Futuro* |

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
