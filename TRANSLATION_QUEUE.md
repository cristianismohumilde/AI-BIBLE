# Translation Queue — Fontes Priorizadas

Este arquivo lista a ordem priorizada de tradução e o status atual das fontes no repositório.

## 🚀 Fila Ativa de Tradução

| Ordem | Fonte | Seleção | Status | Localização |
|---:|---|---|---|---|
| 1 | **Septuaginta (LXX)** | Isaías, Salmos, Deuterocanônicos, 1 Esdras | 🚀 Em andamento | [data/LXX](data/LXX) |
| 2 | **Ge'ez (Etiópico)** | NT completo + Enoque + Jubileus | ⏳ Aguardando | [data/ancient_versions/geez_extracted](data/ancient_versions/geez_extracted) |
| 3 | **Manuscritos do Mar Morto (DSS)** | Seleção estratégica (ver abaixo) | ⏳ Aguardando | [data/DSS](data/DSS) |
| 4 | **Targum Onkelos** | Apenas Gênesis (50 caps) | ⏳ Aguardando | [data/ancient_versions/targum_onkelos_genesis.json](data/ancient_versions/targum_onkelos_genesis.json) |
| 5 | **Texto Bizantino (BYZ)** | NT completo | ⏳ Aguardando | [data/BYZ](data/BYZ) |
| 6 | **Peshitta Siríaca** | NT completo | ⏳ Aguardando | [data/ancient_versions/peshitta_syriac.json](data/ancient_versions/peshitta_syriac.json) |
| 7 | **Copta Saídico** | NT completo | ⏳ Aguardando | [data/ancient_versions/coptic_sahidic.json](data/ancient_versions/coptic_sahidic.json) |
| 8 | **Armênio Oriental** | NT completo | ⏳ Aguardando | [data/ancient_versions/armenian_eastern.json](data/ancient_versions/armenian_eastern.json) |

---

## 🪨 Seleção Estratégica — Manuscritos do Mar Morto (DSS)

Em vez de traduzir os ~928 fragmentos (maioria incompleta), priorizamos os 5 textos de maior impacto acadêmico e curiosidade para o público português:

| Prioridade | Texto | Sigla | Por que é importante |
|---:|---|---|---|
| 1 | **Rolo de Isaías Completo** | 1QIsa-a | Único livro bíblico completo nos DSS — 1.000 anos mais antigo que o Texto Massorético |
| 2 | **Regra da Comunidade** | 1QS | Estatuto da seita de Qumran — contexto essencial para entender o NT e o judaísmo do séc. I |
| 3 | **Comentário de Habacuque** | 1QpHab | Primeiro comentário bíblico da história — aplicação profética ao tempo dos essênios |
| 4 | **Rolo de Guerra** | 1QM | Texto apocalíptico — paralelos diretos com o Apocalipse de João |
| 5 | **Hinos de Ação de Graças** | 1QH | Poesia mística — paralelos com os Salmos, atribuídos ao fundador de Qumran |

> **Total estimado:** ~80–100 capítulos em vez de 928 — alta viabilidade dentro do orçamento.

---

## 📜 Seleção Estratégica — Targum Onkelos

O Targum Onkelos cobre a Torá inteira (Gênesis–Deuteronômio, 187 caps). Priorizamos:

- **Apenas Gênesis (50 caps)** — o mais estudado, onde a interpretação aramaica difere mais do hebraico (criação, patriarcas, ciclo de José). Máximo impacto com mínimo custo.
- Êxodo poderá ser incluído se sobrar orçamento após Gênesis.

---

## 📖 Apócrifos — Já Baixados, Fase 4

| Texto | Arquivo | Status |
|---|---|---|
| 4 Esdras (Vulgata Latina) | `data/apocrypha/4_esdras_vulgate.json` | ✅ Baixado — aguarda inclusão na fila |
| Livro de Enoque | `data/apocrypha/enoch_charles_edition.txt` | ✅ Baixado — Fase 4 |
| Livro dos Jubileus | `data/apocrypha/jubilees_charles_edition.pdf` | ✅ Baixado — Fase 4 |
| Testamento dos Doze Patriarcas | `data/apocrypha/testaments_twelve_patriarchs.pdf` | ✅ Baixado — Fase 4 |
| Oração de Manassés | `data/apocrypha/structured/Prayer_of_Manasseh/1.json` | ✅ Baixado — Fase 4 |
| Salmo 151 | `data/apocrypha/structured/Psalm_151/1.json` | ✅ Baixado — Fase 4 |
| Mishná: Berakhot | `data/apocrypha/mishnah_berakhot.json` | ✅ Baixado — Fase 4 |

---

## ❌ Fora do Orçamento Atual

| Texto | Razão |
|---|---|
| Talmud Bavli (37 tratados) | Custo excessivo — texto vastíssimo |
| WLC (Texto de Leningrado) | Redundante com Aleppo (mesmo texto hebraico massorético) |
| Textus Receptus (TR) | Redundante com BYZ para fins acadêmicos |
| SBLGNT | Redundante com BYZ para fins de público geral |

---

## Observações Técnicas

- Para cada item com `⏳ Aguardando`, a tradução começa automaticamente após a LXX concluir.
- Os DSS requerem lógica especial no `translate_bible.py` para identificar os 5 textos selecionados pelos seus rótulos (1QIsa-a, 1QS, 1QpHab, 1QM, 1QH).
- O 4 Esdras da Vulgata está em formato JSON por capítulo — pronto para tradução quando entrar na fila.
