# 📊 PROGRESS — AI-BIBLE Translation Status

<<<<<<< HEAD
> Gerado automaticamente em: **2026-05-23 17:38 UTC**
> O servidor de tradução via GPU (Frankfurt) encontra-se agora offline.
=======
> Gerado automaticamente em: **2026-05-23 02:27 UTC**
> Velocidade estimada: ~26 capítulos/hora com Double-Pass Review concorrente ativo.
>>>>>>> 539ec19bcd5d1c3e674ea0205b7aba4b60d1cf5a

---

## 📈 Progresso Geral

`████████████░░░░░░░░` 63.3%

<<<<<<< HEAD
**2,423** de **3,844** capítulos traduzidos.
**ETA estimado:** 🛑 Operações Encerradas (VM Offline)
**Custo Computacional Restante:** $0 (Servidor Desligado)
=======
**2,432** de **3,844** capítulos traduzidos.
**ETA estimado:** 🛑 Encerrando operações
**Custo Computacional Restante:** $0 (Operação Finalizando)
>>>>>>> 539ec19bcd5d1c3e674ea0205b7aba4b60d1cf5a

---

## 📋 Detalhamento por Coleção

| Coleção | Idioma Original | Capítulos Fonte | Traduzidos | Progresso | Status |
| :--- | :--- | ---: | ---: | :--- | :--- |
| 📜 Códice de Aleppo | Hebraico Massorético Antigo | 928 | 928 | `████████████████████` 100.0% | ✅ Concluído |
| 🏛️ Septuaginta (LXX) | Grego Clássico | 389 | 389 | `████████████████████` 100.0% | ✅ Concluído |
| 🪨 Manuscritos do Mar Morto | Hebraico/Aramaico Antigo | 986 | 127 | `██░░░░░░░░░░░░░░░░░░` 12.9% | ❌ Sem orçamento |
<<<<<<< HEAD
| 📜 Apócrifos (4 Esdras / VUL) | Latim Clássico (Vulgata) | 18 | 17 | `██████████████████░░` 94.4% | ❌ Sem orçamento |
| ✝️ Texto Bizantino (BYZ) | Grego Koiné | 260 | 7 | `░░░░░░░░░░░░░░░░░░░░` 2.7% | 🚀 Finalizando últimos livros... |
=======
| 📜 Apócrifos (4 Esdras / VUL) | Latim Clássico (Vulgata) | 18 | 16 | `█████████████████░░░` 88.9% | ❌ Sem orçamento |
| ✝️ Texto Bizantino (BYZ) | Grego Koiné | 260 | 17 | `█░░░░░░░░░░░░░░░░░░░` 6.5% | 🚀 Finalizando últimos livros... |
>>>>>>> 539ec19bcd5d1c3e674ea0205b7aba4b60d1cf5a
| 📜 Targum Onkelos | Aramaico Antigo | 187 | 50 | `█████░░░░░░░░░░░░░░░` 26.7% | ❌ Sem orçamento (Pausado) |
| 📖 Peshitta Siríaca | Siríaco Clássico | 260 | 260 | `████████████████████` 100.0% | 🚀 Finalizando últimos livros... |
| 🔤 Versão Copta Saídica | Copta Saídico | 260 | 260 | `████████████████████` 100.0% | 🚀 Finalizando últimos livros... |
| 🏔️ Versão Armênia Oriental | Armênio Clássico | 260 | 89 | `██████░░░░░░░░░░░░░░` 34.2% | 🚀 Finalizando últimos livros... |
| 🇪🇹 Versão Ge'ez (Etíope) | Ge'ez (Etíope Clássico) | 296 | 296 | `████████████████████` 100.0% | ✅ Concluído |
| 📖 Talmud Bavli | Aramaico / Hebraico Rabínico | 36 | — | `░░░░░░░░░░░░░░░░░░░░` — | ❌ Sem orçamento |
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
