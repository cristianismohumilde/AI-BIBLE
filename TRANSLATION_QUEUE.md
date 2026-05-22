# 📋 Fila de Tradução Ativa — AI-BIBLE (Fase GPU Frankfurt)

Este arquivo documenta a priorização oficial da fila de tradução para a Fase GPU, detalhando o status real e atualizado de cada manuscrito/versão antiga.

> Atualizado manualmente em: **2026-05-22 17:31 UTC**

---

## 🏆 Status Atual das Coleções

| Prioridade | Fonte | Idioma Original | Capítulos | Status Real | Observações |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **—** | Códice de Aleppo | Hebraico Massorético | 928/928 | **✅ 100% Concluído** | `output/Aleppo/` |
| **—** | Septuaginta (LXX) | Grego Clássico | 389/389 | **✅ 100% Concluído** | `output/LXX/` |
| **—** | Ge'ez Clássico | Ge'ez (Etíope Clássico) | 296/296 | **✅ 100% Concluído** | `output/Geez/` |
| **—** | Manuscritos do Mar Morto (DSS) | Hebraico/Aramaico Qumran | 127/127 | **✅ 100% Concluído** | `output/DSS/` |
| **—** | Peshitta Siríaca | Siríaco Clássico | 260/260 | **✅ 100% Concluído** | `output/Peshitta_Syriac/` |
| **—** | Versão Copta Saídica | Copta Saídico | 260/260 | **✅ 100% Concluído** | `output/Coptic_Sahidic/` |
| **1** | **Apócrifos (4 Esdras / VUL)** | Latim Clássico (Vulgata) | 16/18 | **🚀 88.9% — Em andamento** | 2 capítulos restantes |
| **2** | **Texto Bizantino (BYZ)** | Grego Koiné | 0/260 | **🚀 Iniciado agora** | Traduzindo a partir de 1Coríntios 1 |
| **3** | **Armênio Oriental** | Armênio Clássico | 89/260 | **🚀 34.2% — Em andamento** | 171 capítulos restantes |
| **4** | **Targum Onkelos** | Aramaico Antigo | 50/187 | **🚀 26.7% — Em andamento** | Apenas Gênesis (50 caps). Êxodo–Deuteronômio pausado. |

---

## 📊 Progresso Geral

`████████████████░░░░` **80.9%** — 2.415 de 2.985 capítulos traduzidos

**ETA estimado:** ~21 horas restantes ao ritmo atual (~26 cap/hora com Double-Pass)

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

> **Total traduzido:** 127 capítulos dos 5 rolos prioritários ✅

---

## 🔤 Fase de Transliteração (Em Paralelo)

A transliteração está rodando **em paralelo às traduções** via `transliterate.py` em background. Processa os arquivos já traduzidos à medida que ficam prontos.

| Sistema | Coleções | Status |
| :--- | :--- | :---: |
| SBL Hebraico (ā, ē, ō, š, ṣ, ṭ, ḥ, ʿ, ʾ) | Aleppo, DSS, Targum Onkelos | **🔄 Rodando em background** |
| SBL Grego Koiné (ex: Κύριος → Kyrios) | LXX, BYZ | **🔄 Rodando em background** |
| CAL Aramaico (ex: Sedra/CAL) | Targum Onkelos, Peshitta Siríaca | **🔄 Rodando em background** |
| Etíope padrão (ex: አምላክ → ʾAmlāk) | Ge'ez | **🔄 Rodando em background** |
| Copta acadêmico (ex: ⲡⲛⲉⲩⲙⲁ → pneuma) | Coptic Sahidic | **🔄 Rodando em background** |
| ISO 9985 Armênio | Armenian Eastern | **🔄 Rodando em background** |

> Novos capítulos traduzidos já saem com a chave `"transliteration"` embutida diretamente (`add_transliteration_to_verses` em tempo real).

---

## 🚫 Coleções Pausadas (Fora do Orçamento — Limite $300 USD)

As seguintes fontes estão desativadas no tradutor (`SKIP_MANUSCRIPTS`) e não consomem processamento:

- **WLC** (Códice de Leningrado) — *Hebraico Massorético*
- **SBLGNT** — *Grego Koiné Crítico*
- **Textus Receptus (TR)** — *Grego Koiné*
- **Vulgata Latina (VUL)** — *Latim Clássico*
- **Talmud Bavli** — *Hebraico Mishnaico e Aramaico Talmúdico*
- **Targum Onkelos (Êxodo → Deuteronômio)** — *137 caps restantes após Gênesis*
- **DSS (textos bíblicos menores)** — *Gênesis, Salmos, Samuel, etc. — pausados para focar nos 5 Rolos Principais*

---

## 🔄 Dinâmica da Sincronização

1. O tradutor da VM (`translate_bible.service`) consome a fila com **3 workers paralelos** (Double-Pass Review ativo).
2. `vm_autopush.py` sincroniza via `git pull/push` a cada **5 minutos** e garante que `transliterate.py` está rodando.
3. Transliterações são geradas **em tempo real** para novos capítulos e em **catch-up** para os já traduzidos.
4. Os arquivos `PROGRESS.md` e `TRANSLATION_QUEUE.md` são regenerados automaticamente a cada ciclo.
