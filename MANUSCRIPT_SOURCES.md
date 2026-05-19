# Fontes Oficiais e Atestação dos Manuscritos Bíblicos (AI-BIBLE)

Este documento fornece as fontes digitais oficiais, o histórico de download e a verificação acadêmica de integridade de todos os manuscritos e bases de estudo antigos incorporados ao projeto **AI-BIBLE**.

> 📌 **Nota sobre Escopo Priorizado ($300 USD)**: De acordo com a sequência de tradução atualizada, apenas as seguintes coleções serão traduzidas no período de recursos disponíveis (após Aleppo):
> 1. **Septuaginta** (Seleção: Isaías, Salmos, Deuterocanônicos)
> 2. **Ge'ez** (Seleção: Deuterocanônicos + Novo Testamento em Ge'ez Puro)
> 3. **Manuscritos do Mar Morto** (Tradução apenas do inglês)
> 4. **Targum Onkelos**, **Texto Bizantino NT**, **Peshitta NT**, **Copta NT**, **Armênio NT**
> 
> Textos pausados até novo orçamento: Leningrado (WLC), Textus Receptus, SBLGNT, Vulgata Latina, Talmud Bavli.

---

## 1. Manuscritos e Versões Bíblicas Antigas

### 0.0 Códice de Aleppo (Uso atual e avaliação)
* **Descrição**: Códice massorético medieval reconhecido como uma das testemunhas mais importantes do texto hebraico massorético.
* **Fonte usada no projeto**: Download via **Sefaria API** utilizando o módulo identificado como *"Aleppo"* (parâmetro `version="Miqra according to the Masorah"`). O script `download_manuscripts.py` automatiza essa captura.
    - Endpoint: `https://www.sefaria.org/api/texts/{Book}.{Chapter}?vhe=Miqra%20according%20to%20the%20Masorah`
* **Verificação de Qualidade (avaliação provisória)**: Alta qualidade filológica — o Códice de Aleppo é historicamente considerado das mais confiáveis testemunhas massoréticas. Entretanto, atenção: o códice sofreu perdas e lacunas documentadas (partes foram danificadas/ausentes ao longo da história). Portanto:
    - Recomendação imediata: comparar automaticamente com o `WLC` (Códice de Leningrado) para preencher lacunas e validar variantes textuais.
    - Ação pendente: realizar verificação filológica formal para documentar exatamente qual edição/versão foi usada (e se existem conversões/normalizações aplicadas pelo Sefaria que impactem a forma do texto).
* **Comparação automatizada Aleppo × WLC**: o relatório `reports/aleppo_wlc_comparison.md` já foi gerado. Ele aponta principalmente diferenças ortográficas / massoréticas, com algumas diferenças de contagem por capítulo que ainda precisam de revisão humana antes de qualquer merge automático.


### 1.0 Septuaginta (LXX) — *Seleção Priorizada: Isaías, Salmos e Deuterocanônicos*
*   **Descrição**: Tradução grega do Antigo Testamento hebraico, realizada entre os séculos III-II a.C. pela comunidade judaica de Alexandria. A seleção atual prioriza os livros de Isaías, Salmos e todos os deuterocanônicos (Sabedoria, Sirácida, Baruc, Carta de Jeremias, 1-2 Macabeus, adições a Daniel e Ester).
*   **Fonte**: [Septuaginta Digital Project / Antinoopolis Papyri Collections](https://www.academia.edu/community/septuaginta-research)
*   **Link de Download**: [LXX via Sefaria API](https://www.sefaria.org/api/texts/Septuagint?lang=grc) ou diretamente [LXX Rahlfs-Hanhart Edition](https://www.academic-bible.com/en/online/sep/)
*   **Verificação de Qualidade**: **Excelente para Seleção Priorizada**. Texto crítico baseado nos manuscritos mais antigos (P.Oxy, Papiro Fouad, Códice Sinaítico). A edição Rahlfs-Hanhart é a referência acadêmica internacional.
*   **Nota Importante**: A tradução será limitada à seleção priorizada (Isaías, Salmos, Deuterocanônicos) até disponibilização de novo orçamento.

### 1.0b Deuterocanônicos ortodoxos já presentes / confirmados
* **3 Macabeus** e **4 Macabeus** já existem em `data/LXX/3_Maccabees/` e `data/LXX/4_Maccabees/`.
* **Salmo 151** já está presente em `data/LXX/Psalms/151.json`.
* **Oração de Manassés** foi confirmada como texto disponível via Sefaria (`https://www.sefaria.org/api/texts/Prayer_of_Manasseh`).
* **4 Esdras** já tem uma fonte latina pública localizada na Vulgata.org (`https://vulgate.org/ot/4esdras_1.htm` até `https://vulgate.org/ot/4esdras_16.htm`); o fallback público em inglês do Gutenberg permanece apenas para comparação.

### 1.1 Livro de Enoque (1 Enoch) — *Ge'ez Clássico (Etiópico Antigo)*
*   **Descrição**: O texto integral do Livro de Enoque que sobreviveu inteiramente apenas na língua litúrgica clássica da Etiópia (Ge'ez Clássico).
*   **Fonte**: [Repository Dead Sea Scrolls - enchantedcostumes-debug](https://github.com/enchantedcostumes-debug/dead-sea-scrolls)
*   **Link de Download**: [enoch_geez_text.json](https://raw.githubusercontent.com/enchantedcostumes-debug/dead-sea-scrolls/master/data/enoch_geez_text.json)
*   **Verificação de Qualidade**: **Excelente (Grau Museológico)**. Apresenta o caractere litúrgico clássico de dois pontos verticais (`፡`) para separação de palavras antigos.

### 1.2 Novo Testamento Etíope — *Amárico Moderno (Haile Selassie 1954)*
*   **Descrição**: O texto litúrgico contemporâneo do Novo Testamento usado pela Igreja Ortodoxa Tewahedo da Etiópia.
*   **Fonte**: [Repository Ethiopic Bible Data - biniama](https://github.com/biniama/ethiopic-bible-data)
*   **Link de Download**: [biniama/ethiopic-bible-data/data/new-testament/](https://github.com/biniama/ethiopic-bible-data/tree/main/data/new-testament)
*   **Verificação de Qualidade**: **Alta Equivalência Exegética** (em Amárico Moderno). Embora escrito em Amárico Moderno (língua viva), representa com precisão a recepção teológica da tradição ortodoxa etíope.
*   **⚠️ Nota para Priorização**: Esta fonte está em Amárico, não em Ge'ez Clássico puro. Para conformidade com a seleção priorizada que exige Ge'ez genuíno, buscar fontes alternativas em Ge'ez Clássico.

### 1.2b Novo Testamento em Ge'ez Clássico Puro — *Disponível no repositório*
*   **Descrição**: Versão do Novo Testamento em Ge'ez Clássico genuíno, distinto do Amárico moderno.
*   **Fonte**: extração já presente em `data/ancient_versions/geez_extracted/`, com livros e capítulos em Ge'ez (script etíope), incluindo Mateus, Marcos, Lucas, João e o restante do NT.
*   **Validação rápida**: o arquivo de amostra `Mateus 1` foi conferido e contém texto em Ge'ez clássico, não em Amárico.
*   **Status**: ✅ *Fonte localizada e pronta para uso na sequência priorizada*.

### 1.3 Targum Onkelos — *Aramaico Antigo (Torá)*
*   **Descrição**: A tradução/paráfrase aramaica oficial da Torá samaritana e rabínica.
*   **Fonte**: [Sefaria Project Global Export](https://www.sefaria.org)
*   **Links de Download**:
    *   [Onkelos Genesis](https://storage.googleapis.com/sefaria-export/json/Tanakh/Targum/Onkelos/Torah/Onkelos%20Genesis/Hebrew/merged.json)
    *   [Onkelos Exodus](https://storage.googleapis.com/sefaria-export/json/Tanakh/Targum/Onkelos/Torah/Onkelos%20Exodus/Hebrew/merged.json)
    *   [Onkelos Leviticus](https://storage.googleapis.com/sefaria-export/json/Tanakh/Targum/Onkelos/Torah/Onkelos%20Leviticus/Hebrew/merged.json)
    *   [Onkelos Numbers](https://storage.googleapis.com/sefaria-export/json/Tanakh/Targum/Onkelos/Torah/Onkelos%20Numbers/Hebrew/merged.json)
    *   [Onkelos Deuteronomy](https://storage.googleapis.com/sefaria-export/json/Tanakh/Targum/Onkelos/Torah/Onkelos%20Deuteronomy/Hebrew/merged.json)
*   **Verificação de Qualidade**: **Excelente**. Contém pontuação massorética clássica e vocalização aramaica limpa.

### 1.4 Peshitta Siríaca — *Siríaco Clássico (Novo Testamento)*
*   **Descrição**: A versão padrão e oficial da Bíblia siríaca clássica.
*   **Fonte**: [Scrollmapper Bible Databases](https://github.com/scrollmapper/bible_databases)
*   **Link de Download**: [Peshitta.json](https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/json/Peshitta.json)
*   **Verificação de Qualidade**: **Excelente para NT**. Texto siríaco clássico de alta fidelidade acadêmica. ⚠️ **Nota**: A fonte contém apenas o Novo Testamento; o Antigo Testamento Siríaco (Peshitta OT) requer fonte alternativa ou será traduzido apenas a partir do NT conforme priorização atual.

### 1.5 Copta Sahídico — *Copta Clássico (Novo Testamento)*
*   **Descrição**: O principal dialeto antigo do Egito cristão (Copta Sahídico).
*   **Fonte**: [Scrollmapper Bible Databases](https://github.com/scrollmapper/bible_databases)
*   **Link de Download**: [CopSahBible2.json](https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/json/CopSahBible2.json)
*   **Verificação de Qualidade**: **Excelente**. Estruturado em Unicode limpo e com dialética perfeita.

### 1.6 Armênio Oriental — *Armênio Clássico (Novo Testamento)*
*   **Descrição**: O texto bíblico em Armênio Clássico (conhecido na crítica textual como a "Rainha das Versões").
*   **Fonte**: [Scrollmapper Bible Databases](https://github.com/scrollmapper/bible_databases)
*   **Link de Download**: [ArmEastern.json](https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/json/ArmEastern.json)
*   **Verificação de Qualidade**: **Excelente**. Ideal para verificar a recepção patrística oriental dos manuscritos.

---

## 2. Textos Críticos e Tradicionais (Novo Testamento Grego)

### 2.1 SBLGNT (Society of Biblical Literature Greek New Testament)
*   **Descrição**: Texto crítico moderno refinado pelo estudioso Michael W. Holmes.
*   **Fonte**: [Bolls.life Bible API](https://bolls.life)
*   **Link de Download**: `https://bolls.life/get-text/SBLGNT/{Book}/{Chapter}/`
*   **Verificação de Qualidade**: **Excelente**. Padrão internacional para estudos filológicos modernos do NT.

### 2.2 BYZ (Texto Bizantino / Majoritário)
*   **Descrição**: Texto que reflete a vasta maioria dos manuscritos gregos sobreviventes.
*   **Fonte**: [Bolls.life Bible API](https://bolls.life)
*   **Link de Download**: `https://bolls.life/get-text/BYZP/{Book}/{Chapter}/`
*   **Verificação de Qualidade**: **Excelente**. Essencial para análise comparativa em crítica textual.

---

## 3. Grandes Compilações Rabínicas e de Estudo

### 3.1 Talmud Bavli (Talmud da Babilônia)
*   **Descrição**: A compilação monumental de debates jurídicos e exegéticos rabínicos (Mishna e Gemara).
*   **Fonte**: [Sefaria API](https://www.sefaria.org)
*   **Link de Download**: `https://www.sefaria.org/api/texts/{Tractate_Name}?lang=he&commentary=0`
*   **Verificação de Qualidade**: **Excelente**. Texto em Hebraico Mishnaico e Aramaico da Babilônia direto dos servidores acadêmicos do Sefaria.

---

## 4. Materiais de Estudo Auxiliares (Léxicos e Gramáticas)

*   **Strong's Hebrew Lexicon**: [strongs-hebrew-dictionary.json](https://raw.githubusercontent.com/openscriptures/strongs/master/hebrew/strongs-hebrew-dictionary.json) (OpenScriptures)
*   **Strong's Greek Lexicon**: [strongs-greek-dictionary.json](https://raw.githubusercontent.com/openscriptures/strongs/master/greek/strongs-greek-dictionary.json) (OpenScriptures)
*   **Brown-Driver-Briggs (BDB) Hebrew Lexicon**: [BrownDriverBriggs.xml](https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master/BrownDriverBriggs.xml)
*   **Gramática de Gesenius (Hebraico)**: [gesenius_hebrew_grammar.txt](https://www.gutenberg.org/files/17029/17029-0.txt) (Project Gutenberg)
*   **Gramática de Robertson (Grego)**: [robertson_greek_grammar.txt](https://www.gutenberg.org/files/44606/44606-0.txt) (Project Gutenberg)
*   **Dicionário de Jastrow (Aramaico)**: [jastrow_sefaria.json](https://raw.githubusercontent.com/sefaria/Sefaria-Data/master/sources/Jastrow/jastrow_dict.json) (Sefaria Data)
