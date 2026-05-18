# AI-BIBLE: Ultra-Precise Translation of Original Manuscripts (v2026)

This project utilizes state-of-the-art Artificial Intelligence (as of May 2026) running locally on **Oracle Cloud instances (NVIDIA A10 GPU or ARM64 A1.Flex)** to translate original biblical manuscripts directly into Portuguese and English.

## 🚀 Key Advantage: Multi-Source & Historical Fidelity
Unlike generic translators, this system processes multiple families of manuscripts simultaneously to offer a deep comparative overview:

### Old Testament (Hebrew/Greek)
- **Aleppo Codex (M)**: The highest authority in the Massoretic tradition.
- **Leningrad Codex (WLC)**: The base text for most modern Hebrew Bibles.
- **Septuagint (LXX)**: The classical Greek translation of the OT used by the apostles.
- **Dead Sea Scrolls (DSS)**: Transcriptions of the oldest biblical fragments ever found.

### New Testament (Greek)
- **Majority/Byzantine Text (RP2018)**: Represents the vast majority of historical manuscripts.
- **Textus Receptus (TR)**: The basis for the classical translations of the Reformation.
- **Critical Text (SBLGNT)**: Focuses on the oldest surviving papyri and codices (Sinaiticus, Vaticanus).
## 🎯 Scientific and Philological Precision of AI Translation

Unlike standard commercial translators or generic AI models that commit frequent exegetical slips, the **AI-BIBLE** translation pipeline operates under a strict, academically rigorous **Double-Pass Critique** protocol:

1. **Pass 1: Primary Philological Translation**: The model performs a formal equivalence translation directly from the ancient source text (Hebrew, Greek, Aramaic, or Syriac), preserving exact syntax and morpho-semantic structures.
2. **Pass 2: Peer Review Academic Critique**: A second AI agent acts as an elite philological and theological reviewer. It compares the primary draft word-by-word against the ancient manuscript, ensuring:
   - **Absolute Grammatical Rigor**: Ensuring plurals and duals are mathematically preserved (for example, translating **`הַשָּׁמַ֖יִם` (Hashamayim)** strictly in the plural as **"céus"** in Portuguese instead of the singular "céu", preventing common translation slips).
   - **Historical-Theological Fidelity**: Exact exegesis of prepositions, nouns, and verbs within the socio-cultural context of antiquity.
   - **Linguistic Solemnity**: The resulting translation is solemn, formal, and majestic, preserving the stylistic and theological grandeur of the Sacred Scriptures.

## 📂 Output Structure
Results are structured as **JSON** files by chapter, fully optimized for static web sites or application integrations:
- `output/[SOURCE]/[BOOK]_[CHAPTER].json`

## 🛠️ Technology Stack (May 2026)
- **AI**: **Qwen 2.5 (32B)** - An exceptionally capable 32-Billion parameter model running locally on Ollama with full GPU hardware acceleration.
- **Active Production Server (Frankfurt, Germany)**: **`VM.GPU.A10.1`** (15 OCPU cores, 240 GB RAM, 1x NVIDIA A10 with 24GB VRAM).
- **Environment**: Docker & Docker Compose integrated with **NVIDIA Container Toolkit**.
- **Translation Pipeline**: Double-pass academic self-reflection pipeline (`DOUBLE_PASS_REVIEW = True`) ensuring unparalleled theological and grammatical precision.

## ⚙️ How to use

1.  **Launch Infrastructure**:
    ```bash
    docker compose up -d --build
    ```

2.  **Download Manuscripts**:
    ```bash
    docker compose exec translator python download_manuscripts.py
    ```

3.  **Start Translation**:
    ```bash
    docker compose exec translator python translate_bible.py
    ```

## 🗺️ Expansion Roadmap & New Sources
We are expanding the scope of the project beyond the traditional canon to build the most complete open-source theological database in existence:

1.  **Full Sefaria Integration**: Download and translate the complete Sefaria portal database directly into Brazilian Portuguese.
2.  **Apocrypha and Pseudepigrapha**:
    - *Old Testament*: Book of Enoch, Jubilees, Testament of the Twelve Patriarchs, Tobit, Judith, Wisdom of Solomon, Sirach (Ecclesiasticus), Baruch, Maccabees.
    - *New Testament*: Gospel of Thomas, Gospel of the Hebrews, Acts of Paul, Epistle of Barnabas, Shepherd of Hermas, Didache, and other early Apostolic writings.
3.  **Additional Ancient Languages**:
    - *Aramaic*: Targum Onkelos, Targum Pseudo-Jonathan, and biblical Aramaic portions of the Tanakh.
    - *Syriac*: The Peshitta (Old and New Testaments in classical Syriac).
    - *Ge'ez (Classical Ethiopic)*: Ethiopian Orthodox canon (including Enoch and Jubilees which only survived fully in Ge'ez).
    - *Armenian*: The classical Armenian version (known philologically as the "Queen of Versions").
4.  **Concordances and Study Materials**:
    - *Treasury of Scripture Knowledge (TSK)*: 500,000+ public domain cross-references between verses.
    - *Topical concordance*: Nave's Topical Bible (20,000+ categorized topics).
    - *Lexicons & Grammars*: Strong's Dictionaries, Brown-Driver-Briggs (BDB) Extended, Thayer Greek Lexicon, Hitchcock's Bible Names Dictionary.
    - *Geographic mapping*: Open coordinates for all ancient biblical sites.

---

## 📜 Licensing and Copyright

### Software Source Code
The software source code is distributed under the **[MIT License](LICENSE)**. This is highly permissive and allows any usage, modification, or commercial distribution, provided the copyright notice remains.

### Biblical Texts, Manuscripts and Lexicons (100% Public Domain!)
Unlike modern translations protected by copyright restrictive terms (NVI, ARA, NVT), our raw data sources are in the **Public Domain**:

*   **Ancient Manuscripts & Códices**: WLC, Aleppo, Septuagint (LXX), Dead Sea Scrolls (DSS), Peshitta, Targums, and Orthodox Ethiopic Canon are in the Public Domain.
*   **Study Materials**: Strong's Dictionary, BDB Lexicon, Thayer Greek Lexicon, Matthew Henry, Albert Barnes, Nave's Topical Bible, Hitchcock's Names, and Gesenius' Grammar are in the Public Domain (published over 100 years ago).
*   **AI Translations**: The translated texts generated by our private Ollama GPU pipeline belong to the project and are released under the MIT License for 100% free use worldwide!

---

## 📊 Final Database Size Projection
Even with this colossal library, plain text JSON files are extremely optimized:

| Category | Description | Estimated Size |
| :--- | :--- | :--- |
| **Manuscript Texts** | Full Bible + Apocrypha × 8 Original Sources (JSON) | ~100 MB |
| **Lexicons & Concordances** | Strong's Dictionaries + BDB + Thayer + TSK (JSON) | ~60 MB |
| **Bible Commentaries** | Complete commentaries (Matthew Henry, Barnes, Pulpit) | ~350 MB |
| **Topical/Geographical Data**| Nave's Topical + Geographic Coordinates | ~10 MB |
| **Historical Grammars** | Gesenius + Syriac/Greek Grammars | ~30 MB |
| **Projected Total** | **Ultimate Academic Theological Database** | **~550 MB (0.55 GB)** |

*This means the entire database can be committed directly to GitHub and cloned in seconds!*
