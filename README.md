# AI-BIBLE — Tradução Ultra-Precisa de Manuscritos Originais

> **README gerado automaticamente em: 2026-05-21 03:27 UTC**
> Veja [PROGRESS.md](PROGRESS.md) para monitoramento detalhado em tempo real.

Este projeto utiliza o estado da arte em IA rodando em **Oracle Cloud GPU (NVIDIA A10)**
para traduzir manuscritos originais da Bíblia e textos rabínicos diretamente para o **Português do Brasil**,
com transliteração acadêmica incluída.

---

## 📊 Status Geral

| Métrica | Valor |
|---|---|
| Capítulos fonte disponíveis | **3,768** |
| Capítulos traduzidos | **1,556** (41.3%) |
| Orçamento Disponível (Oracle GPU) | **$300 USD** (~R$ 1.500) |
| Custo estimado restante | **~$127 USD** |
| ETA estimado de processamento | **~3d 13h** |
| Velocidade (com Double-Pass) | ~26 caps/hora |
| Última atualização | 2026-05-21 03:27 UTC |

---

## 📜 Manuscritos — Antigo e Novo Testamento

| Manuscrito | Idioma | Fonte | Traduzido | Status |
|:---|:---|---:|---:|:---|
| 📜 Códice de Aleppo | Hebraico Massorético Antigo | 928 caps | 928 traduzidos | ✅ Completo |
| 🏛️ Septuaginta (LXX) | Grego Clássico | 389 caps | 389 traduzidos | ✅ Completo |
| 🪨 Manuscritos do Mar Morto | Hebraico/Aramaico Antigo | 928 caps | 0 traduzidos | ⏳ Aguardando tradução |
| ✝️ Texto Bizantino (BYZ) | Grego Koiné | 260 caps | 0 traduzidos | ⏳ Aguardando tradução |

## 📖 Versões Antigas (Aramaico, Siríaco, Copta, Armênio, Ge'ez)

| Texto | Idioma | Fonte | Traduzido | Status |
|:---|:---|---:|---:|:---|
| 📜 Targum Onkelos | Aramaico Antigo | 187 caps | 0 traduzidos | ⏳ Aguardando tradução |
| 📖 Peshitta Siríaca | Siríaco Clássico | 260 caps | 0 traduzidos | ⏳ Aguardando tradução |
| 🔤 Copta Saídico | Copta Saídico | 260 caps | 0 traduzidos | ⏳ Aguardando tradução |
| 🏔️ Armênio Oriental | Armênio Clássico | 260 caps | 0 traduzidos | ⏳ Aguardando tradução |
| 🇪🇹 Ge'ez (Etiópico) | Ge'ez Clássico | 296 caps | 239 traduzidos | 🚀 Em andamento (81%) |

## 📚 Outros Textos — Fora do Orçamento Atual

| Texto | Idioma | Fonte | Status |
|:---|:---|---:|:---|
| 📖 Talmud Bavli | Aramaico / Hebraico Rabínico | 37 tratados | ❌ Sem orçamento |
| 📜 WLC (Texto de Leningrado) | Hebraico Massorético | 929 caps | ❌ Sem orçamento |
| 🏛️ Textus Receptus (TR) | Grego Koiné | 260 caps | ❌ Sem orçamento |
| 🔬 SBLGNT | Grego Koiné Crítico | 260 caps | ❌ Sem orçamento |

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
| ✅ | Brockelmann Lexicon Syriacum | `brockelmann_syriac.pdf` | 58,196 KB |
| ✅ | Brown-Driver-Briggs (BDB) | `brown_driver_briggs.xml` | 2,843 KB |
| ✅ | Strong+BDB Integrado | `hebrew_strong_enhanced.xml` | 2,684 KB |
| ✅ | Jastrow (Aramaico Talmúdico) | `jastrow_dictionary.txt` | 253 KB |
| ✅ | Lewis & Short Latin | `lewis_short_latin.xml` | 75,438 KB |
| ✅ | LSJ Greek Lexicon | `lsj_greek.xml` | 41,917 KB |
| ✅ | Strong's Greek Lexicon | `strongs_greek.json` | 1,172 KB |
| ✅ | Strong's Hebrew Lexicon | `strongs_hebrew.json` | 1,956 KB |
| ✅ | Gesenius' Hebrew Grammar | `gesenius_hebrew_grammar.txt` | 83 KB |
| ✅ | Nöldeke Syriac Grammar | `noldeke_syriac_grammar.txt` | 576 KB |
| ✅ | A.T. Robertson Greek Grammar | `robertson_greek_grammar.txt` | 70 KB |
| ✅ | INDEX.json | `INDEX.json` | 1 KB |
| ✅ | Referências Cruzadas (340k) | `cross_references.tsv` | 8,106 KB |
| ✅ | Strong's Concordance (legado) | `strongs.json` | 3,811 KB |

---

## 🗺️ Roadmap

### ✅ Fase 1 — Download (Concluída)
- Manuscritos bíblicos principais: WLC, Aleppo, LXX, DSS, TR, BYZ, SBLGNT
- Versões antigas: Peshitta, Copta, Armênio, Targum Onkelos
- Talmud piloto + download de tratados extras em andamento
- Léxicos (Strong's Hebrew+Greek, BDB, Abbott-Smith, Jastrow, Sedra, Dillmann)
- Gramáticas (Gesenius, Robertson, Nöldeke) e Referências Cruzadas

### 🚀 Fase 2 — Tradução (Em andamento — 1,556/3,768 caps (41.3%))
- GPU NVIDIA A10 traduzindo ininterruptamente (24/7)
- Double-Pass Review + Filtro Regex ativos

### ⏳ Fase 3 — Transliteração (após Fase 2)
- Script: `transliterate.py` — roda após conclusão da tradução
- Impacto: +50% do tempo de GPU (3ª chamada por versículo)

### 🗺️ Fase 4 — Expansão Futura
- Enoque, Jubileus, Testamento dos Doze Patriarcas, Didaquê
- **4 Esdras (Vulgata)** — já baixado em `data/apocrypha/4_esdras_vulgate.json`
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
{
  "verse": 1,
  "original": "בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים",
  "transliteration": "Bə-rē-šîṯ bārāʾ ʾĔlōhîm",
  "translation": "No princípio, criou Deus..."
}
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
