# 📋 Fila de Tradução Ativa — AI-BIBLE (Fase GPU Frankfurt)

Este arquivo documenta a priorização oficial da fila de tradução para a Fase GPU, detalhando o status real e atualizado de cada manuscrito/versão antiga.

> Gerado dinamicamente em: **2026-05-22 20:04 UTC**

---

## 🏆 Status Atual das Coleções

| Prioridade | Fonte | Idioma Original | Status Real | Localização | Observações |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **—** | Códice de Aleppo | Hebraico Massorético | **✅ 100% Traduzido** | `output/Aleppo/` | Concluído com sucesso na GPU A10. |
| **—** | Septuaginta (LXX) | Grego Clássico (Seleção) | **✅ 100% Traduzido** | `output/LXX/` | Seleção prioritária de Isaías, Salmos e Deuterocanônicos. |
| **—** | Ge'ez Clássico | Ge'ez (Etíope Clássico) | **✅ 100% Traduzido** | `output/Geez/` | Deuterocanônicos e Novo Testamento em Ge'ez Puro. |
| **1** | **Targum Onkelos (Gênesis)** | Aramaico Antigo | **✅ 100% Traduzido** | `output/Targum_Onkelos/` | Rodando ativamente na VM (Gênesis priorizado). |
| **2** | **Manuscritos do Mar Morto (DSS)** | Hebraico/Aramaico de Qumran | **✅ 100% Traduzido** | `data/DSS/` | 5 rolos prioritários: 1QIsa-a, 1QpHab, 1QS, 1QM, 1QH. |
| **3** | **Apócrifos — 4 Esdras (Vulgata)** | Latim Clássico | **🚀 Traduzindo (16/18 caps)** | `data/apocrypha/` | 16 capítulos. Já estruturado em JSON. |
| **4** | **Texto Bizantino (BYZ)** | Grego Koiné | **🚀 Traduzindo (3/260 caps)** | `data/BYZ/` | Apenas Novo Testamento. |
| **5** | **Peshitta Siríaca** | Siríaco Clássico | **✅ 100% Traduzido** | `data/ancient_versions/` | Novo Testamento Siríaco. |
| **6** | **Copta Saídico** | Copta Saídico | **✅ 100% Traduzido** | `data/ancient_versions/` | Novo Testamento Copta. |
| **7** | **Armênio Oriental** | Armênio Clássico | **🚀 Traduzindo (89/260 caps)** | `data/ancient_versions/` | Novo Testamento Armênio. |

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

## 🔤 Fase de Transliteração (Pós-Tradução)

Após a conclusão de todas as traduções, os 3 workers da VM executarão `transliterate.py` automaticamente para adicionar a transliteração acadêmica a cada versículo de todos os manuscritos. A chave `"transliteration"` será inserida nos arquivos JSON de `output/` ao lado de `"original"` e `"translation"`.

| Sistema | Coleções | Status |
| :--- | :--- | :---: |
| SBL Hebraico (ā, ē, ō, š, ṣ, ṭ, ḥ, ʿ, ʾ) | Aleppo, DSS, Targum Onkelos | **🔤 Transliterando (3/2402 arquivos)** |
| SBL Grego Koiné (ex: Κύριος → Kyrios) | LXX, BYZ | **🔤 Transliterando (3/2402 arquivos)** |
| CAL Aramaico (ex: Sedra/CAL) | Targum Onkelos, Peshitta Siríaca | **🔤 Transliterando (3/2402 arquivos)** |
| Etíope padrão (ex: አምላክ → ʾAmlāk) | Ge'ez | **🔤 Transliterando (3/2402 arquivos)** |
| Copta acadêmico (ex: ⲡⲛⲉⲩⲙⲁ → pneuma) | Coptic Sahidic | **🔤 Transliterando (3/2402 arquivos)** |
| ISO 9985 Armênio | Armenian Eastern | **🔤 Transliterando (3/2402 arquivos)** |

**Progresso geral:** 3/2402 arquivos transliterados.

---

## 🚫 Coleções Pausadas (Fora dos Recursos - Limite $300 USD)
As seguintes fontes estão desativadas no tradutor e não gastam orçamento até liberação de novos créditos:
- **WLC** (Códice de Leningrado) — *Hebraico Massorético*
- **SBLGNT** — *Grego Koiné Crítico*
- **Textus Receptus (TR)** — *Grego Koiné*
- **Vulgata Latina (VUL)** — *Latim Clássico*
- **Talmud Bavli** — *Hebraico Mishnaico e Aramaico Talmúdico*
- **Targum Onkelos (Êxodo → Deuteronômio)** — *Aramaico Antigo — 137 caps restantes após Gênesis*
- **DSS (Textos Bíblicos Menores)** — *Gênesis, Salmos, Samuel, etc. (Pausados para focar nos 5 Rolos Principais)*

---

## 🔄 Dinâmica da Sincronização
1. O tradutor da VM consome esta fila de forma sequencial com base no arquivo `translate_bible.py`.
2. As pastas marcadas como `✅ 100% Traduzido` estão bloqueadas no código (`SKIP_MANUSCRIPTS`) e não consomem processamento.
3. Após **todas** as traduções concluírem, `transliterate.py` é acionado automaticamente com 3 workers paralelos.
4. À medida que novos capítulos são salvos em `output/`, os arquivos `PROGRESS.md` e `TRANSLATION_QUEUE.md` são atualizados a cada 5 minutos pelo serviço automático da VM.
