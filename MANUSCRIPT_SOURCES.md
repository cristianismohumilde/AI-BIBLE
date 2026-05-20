# Fontes Oficiais e Atestação dos Manuscritos Bíblicos (AI-BIBLE)

Este documento fornece as fontes digitais oficiais, o histórico de download e a verificação acadêmica de integridade de todos os manuscritos e bases de estudo antigos incorporados ao projeto **AI-BIBLE**.

> 📌 **Nota sobre Escopo Priorizado ($300 USD)**: De acordo com a sequência de tradução atualizada, apenas as seguintes coleções serão traduzidas no período de recursos disponíveis (após Aleppo):
> 1. **Septuaginta** (Seleção: Isaías, Salmos, Deuterocanônicos)
> 2. **Ge'ez** (Seleção: Deuterocanônicos + Novo Testamento em Ge'ez Puro)
> 3. **Manuscritos do Mar Morto** (Tradução direta do original em Hebraico/Aramaico de Qumran)
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
* **Salmo 151** já está presente em `data/LXX/Psalms/151.json` — [Link de Download Sefaria API](https://www.sefaria.org/api/texts/Psalm_151?context=0).
* **Oração de Manassés** foi confirmada como texto disponível via Sefaria — [Link de Download Sefaria API](https://www.sefaria.org/api/texts/Prayer_of_Manasseh?context=0).
* **4 Esdras** já tem uma fonte latina pública localizada na Vulgata.org (`https://vulgate.org/ot/4esdras_1.htm` até `https://vulgate.org/ot/4esdras_16.htm`); o fallback público em inglês do Gutenberg permanece apenas para comparação.

### 1.1 Livro de Enoque (1 Enoch) — *Ge'ez Clássico (Etiópico Antigo)*
*   **Descrição**: O texto integral do Livro de Enoque que sobreviveu inteiramente apenas na língua litúrgica clássica da Etiópia (Ge'ez Clássico).
*   **Fonte**: [Repository Dead Sea Scrolls - enchantedcostumes-debug](https://github.com/enchantedcostumes-debug/dead-sea-scrolls)
*   **Link de Download**: [enoch_geez_text.json](https://raw.githubusercontent.com/enchantedcostumes-debug/dead-sea-scrolls/master/data/enoch_geez_text.json)
*   **Verificação de Qualidade**: **Excelente (Grau Museológico)**. Apresenta o caractere litúrgico clássico de dois pontos verticais (`፡`) para separação de palavras antigos.

### 1.1b Manuscritos do Mar Morto (DSS) — *Hebraico e Aramaico Antigo de Qumran (Original)*
*   **Descrição**: Transcrições fiéis e morfológicas diretas dos manuscritos e fragmentos originais em Hebraico e Aramaico de Qumran (incluindo o Grande Rolo de Isaías `1Qisaa`, a Regra da Comunidade `1QS`, o Rolo da Guerra `1QM`, os Hinos de Ação de Graças `1QHa`, o Rolo do Templo `11Q19`, o Documento de Damasco `CD`, etc.).
*   **Fontes Principais**:
    *   **ETCBC/dss Repository**: Banco de dados morfológico oficial baseado nas transcrições fundamentais de *Martin Abegg*, mantido pelo *Eep Talstra Centre for Bible and Computer* no GitHub.
        - Link: [ETCBC/dss no GitHub](https://github.com/ETCBC/dss)
    *   **yonatanlou/QumranDataset (Hugging Face)**: Versão estruturada e consolidada de altíssima qualidade do corpus de Qumran contendo todas as transcrições limpas em hebraico/aramaico em formato CSV simples, ideal para uso e integração imediata.
        - Link: [yonatanlou/QumranDataset no Hugging Face](https://huggingface.co/datasets/yonatanlou/QumranDataset)
        - Arquivo principal: [dss_chunk_size_100_overlap_15.csv](https://huggingface.co/datasets/yonatanlou/QumranDataset/resolve/main/dss_chunk_size_100_overlap_15.csv)
*   **Verificação de Qualidade**: **Excepcional (Grau Crítico/Acadêmico)**. Mantém a ortografia autêntica do Período do Segundo Templo (ex: `כיa` ao invés de `כי`, `לוא` ao invés de `לא`, `יעקוב` ao invés de `יעקב`), o que é fundamental para a exegese e para uma tradução sem filtros ou modernizações anacrônicas.
*   **Nota de Uso**: Substitui completamente o fallback anterior em inglês baixado da API do Sefaria (que estava em inglês devido ao Sefaria não hospedar a transcrição hebraica do DSS sob a licença pública).


### 1.2 Novo Testamento Etíope — *Amárico Moderno (Haile Selassie 1954)*
*   **Descrição**: O texto litúrgico contemporâneo do Novo Testamento usado pela Igreja Ortodoxa Tewahedo da Etiópia.
*   **Fonte**: [Repository Ethiopic Bible Data - biniama](https://github.com/biniama/ethiopic-bible-data)
*   **Link de Download**: [biniama/ethiopic-bible-data/data/new-testament/](https://github.com/biniama/ethiopic-bible-data/tree/main/data/new-testament)
*   **Verificação de Qualidade**: **Alta Equivalência Exegética** (em Amárico Moderno). Embora escrito em Amárico Moderno (língua viva), representa com precisão a recepção teológica da tradição ortodoxa etíope.
*   **⚠️ Nota para Priorização**: Esta fonte está em Amárico, não em Ge'ez Clássico puro. Para conformidade com a seleção priorizada que exige Ge'ez genuíno, buscar fontes alternativas em Ge'ez Clássico.

### 1.2b Novo Testamento em Ge'ez Clássico Puro — *Disponível no repositório*
*   **Descrição**: Versão do Novo Testamento em Ge'ez Clássico genuíno, distinto do Amárico moderno.
*   **Fonte**: extração já presente em `data/ancient_versions/geez_extracted/`, com livros e capítulos em Ge'ez (script etíope), incluindo Mateus, Marcos, Lucas, João e o restante do NT.
*   **Link de Download da Fonte Primária**: [Geez.zip (Scrollmapper)](https://raw.githubusercontent.com/scrollmapper/bible_databases/master/sources_backup/gez/Geez/Geez.zip)
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

### 1.7 Apócrifos, Pseudepígrafos e Textos Históricos (Fase 4)
*   **Descrição**: Textos históricos e apócrifos adicionados para estudo exegético e histórico profundo.
*   **Links de Download**:
    *   **Livro de Enoque (Tradução em Inglês por R.H. Charles)**: [Project Gutenberg](https://www.gutenberg.org/cache/epub/43125/pg43125.txt)
    *   **Livro dos Jubileus**: [Archive.org PDF](https://archive.org/download/bookofjubileesor00char/bookofjubileesor00char.pdf)
    *   **Testamento dos Doze Patriarcas**: [Archive.org PDF](https://archive.org/download/testamentsoftwel00char/testamentsoftwel00char.pdf)
    *   **Didaquê (O Ensino dos Doze)**: [Archive.org PDF](https://archive.org/download/didachetexttrans00alle/didachetexttrans00alle.pdf)
    *   **Mishná (Tratado Berakhot - Sefaria API)**: [Sefaria API](https://www.sefaria.org/api/texts/Mishnah_Berakhot.1?context=0)
    *   **3/4 Macabeus + 4 Esdras (Charles Vol. II)**: [Archive.org Text](https://archive.org/stream/apocryphapseudep02char/apocryphapseudep02char_djvu.txt)
    *   **4 Esdras (Fallback Gutenberg)**: [Project Gutenberg](https://www.gutenberg.org/cache/epub/2435/pg2435.txt)

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
*   **Link de Download**: `https://bolls.life/get-text/BYZP/{Book}/{Chapter}/` (Alternativo: `BYZ`)
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
*   **Abbott-Smith Greek Lexicon**: [AS.csv](https://raw.githubusercontent.com/translatable-exegetical-tools/Abbott-Smith/master/AS.csv)
*   **SEDRA Syriac Lexicon Roots**: [ROOTS.TXT](https://raw.githubusercontent.com/peshitta/sedra-parse/master/sedra/ROOTS.TXT)
*   **SEDRA Syriac Lexicon Lexemes**: [LEXEMES.TXT](https://raw.githubusercontent.com/peshitta/sedra-parse/master/sedra/LEXEMES.TXT)
*   **SEDRA Syriac Lexicon Words**: [WORDS.TXT](https://raw.githubusercontent.com/peshitta/sedra-parse/master/sedra/WORDS.TXT)
*   **Gramática de Gesenius (Hebraico)**: [gesenius_hebrew_grammar.txt](https://www.gutenberg.org/files/17029/17029-0.txt) (Project Gutenberg)
*   **Gramática de Gesenius (Hebraico - Link Extra)**: [gesenius_hebrew_grammar_ext.txt](https://www.gutenberg.org/files/17337/17337-0.txt) (Project Gutenberg)
*   **Gramática de Robertson (Grego)**: [robertson_greek_grammar.txt](https://www.gutenberg.org/files/44606/44606-0.txt) (Project Gutenberg)
*   **Bible Treasury**: [bible_treasury.txt](https://www.gutenberg.org/files/8437/8437.txt) (Project Gutenberg)
*   **Dicionário de Jastrow (Aramaico)**: [jastrow_sefaria.json](https://raw.githubusercontent.com/sefaria/Sefaria-Data/master/sources/Jastrow/jastrow_dict.json) (Sefaria Data)
*   **Cruzamento de Referências Bíblicas (Cross References - OpenBible)**: [cross-references.zip](https://a.openbible.info/data/cross-references.zip)
