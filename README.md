# AI-BIBLE: Tradução Ultra-Precisa de Manuscritos Originais (v2026)

Este projeto utiliza o estado da arte em IA (Maio de 2026) rodando localmente em instâncias **Oracle Cloud (GPU NVIDIA A10 ou ARM64 A1)** para traduzir manuscritos originais da Bíblia diretamente para o Português e Inglês.

## 🚀 Diferencial: Multi-Fonte & Fidelidade Histórica
Diferente de tradutores comuns, este sistema processa múltiplas famílias de manuscritos para oferecer uma visão comparativa profunda:

### Antigo Testamento (Hebraico/Grego)
- **Códice Aleppo (M)**: A maior autoridade da tradição Massorética.
- **Códice Leningrado (WLC)**: O texto base da maioria das bíblias hebraicas.
- **Septuaginta (LXX)**: A tradução grega clássica do AT usada pelos apóstolos.
- **Manuscritos do Mar Morto (DSS)**: Fragmentos dos textos bíblicos mais antigos já encontrados.

### Novo Testamento (Grego)
- **Texto Bizantino (RP2018)**: Representa a maioria dos manuscritos históricos.
- **Textus Receptus (TR)**: A base das traduções clássicas da Reforma.
- **Texto Crítico (SBLGNT)**: Focado nos manuscritos mais antigos (Papiros, Sinaítico).
## 🎯 Precisão Científica e Filológica da Tradução por IA

Diferente de tradutores comuns ou modelos generativos genéricos que cometem deslizes exegéticos, a pipeline de tradução do **AI-BIBLE** opera sob um protocolo acadêmico rígido de **Duplo-Passo (Double-Pass Critique)**:

1. **Passo 1: Tradução Filológica Primária**: O modelo traduz o texto focando na equivalência formal e na fidelidade morfológica à língua antiga original (Hebraico, Grego, Aramaico ou Siríaco).
2. **Passo 2: Revisão Crítica Acadêmica (Peer Review por IA)**: Um segundo agente de IA assume o papel de um revisor filológico e teológico de elite. Ele confronta a tradução primária com o texto manuscrito original para verificar:
   - **Rigor Gramatical Absoluto**: Garantia de que termos no plural ou dual sejam preservados com precisão gramatical matemática (como traduzir **`הַשָּׁמַ֖יִם` (Hashamayim)** no plural exato como **"céus"** em vez de "céu" no singular, evitando deslizes comuns).
   - **Fidelidade Histórico-Teológica**: Exegese precisa de preposições, verbos e substantivos no contexto cultural da época.
   - **Solenidade Linguística**: O português resultante é solene, formal e imponente, mantendo a grandiosidade estilística e teológica das Escrituras.

## 📂 Estrutura de Saída
Os resultados são arquivos **JSON** por capítulo, prontos para uso em sites estáticos:
- `output/[FONTE]/[LIVRO]_[CAPITULO].json`

## 🛠️ Stack Tecnológica (Maio 2026)
- **IA**: **Qwen 2.5 (32B)** - Modelo de altíssima precisão rodando localmente no Ollama com aceleração de GPU.
- **Servidor Ativo (Alemanha)**: **`VM.GPU.A10.1`** (15 cores OCPU, 240 GB de RAM, 1x NVIDIA A10 com 24GB de VRAM).
- **Ambiente Local**: Docker & Docker Compose com **NVIDIA Container Toolkit** integrado.
- **Linguagem**: Python 3.13 / Go (para pipelines escaláveis).

## ⚙️ Como usar

1.  **Subir a infraestrutura**:
    ```bash
    docker compose up -d --build
    ```

2.  **Baixar os manuscritos**:
    ```bash
    docker compose exec translator python download_manuscripts.py
    ```

3.  **Iniciar a tradução**:
    ```bash
    docker compose exec translator python translate_bible.py
    ```

## 🗺️ Roadmap de Expansão & Novas Fontes

Estamos expandindo o escopo do projeto para ir além do cânon tradicional, integrando:
1. **Integração Integral com o Sefaria**: Tradução completa dos textos e comentários do portal acadêmico Sefaria diretamente para o Português do Brasil.
2. **Textos Apócrifos e Pseudoepígrafos**:
   - **Antigo Testamento**: Livro de Enoque, Jubileus, Testamento dos Doze Patriarcas, Tobias, Judite, Sabedoria de Salomão, Eclesiástico (Sirácida), Baruque e os livros de Macabeus.
   - **Novo Testamento**: Evangelho de Tomé, Evangelho de Hebreus, Atos de Paulo, Epístola de Barnabé, Pastor de Hermas, Didaquê e outros escritos patrísticos primitivos.
3. **Idiomas Históricos Multilíngues**:
   - **Aramaico**: Targum Onkelos, Targum Pseudo-Jonathan e porções aramaicas do Tanakh.
   - **Siríaco**: A Peshitta (Antigo e Novo Testamento em Siríaco clássico).
   - **Ge'ez (Etiópico clássico)**: Manuscritos etiopes contendo o cânon ortodoxo etíope completo (incluindo Enoque e Jubileus que só sobreviveram integralmente nesta língua).
   - **Armênio**: A clássica versão armênia antiga (conhecida como a "Rainha das Versões" pela sua elegância filológica).

O download dessas novas coleções será feito diretamente pela nossa instância virtual na nuvem, aproveitando a conexão gigabit de alta velocidade para indexação e tradução em lote!

## 📜 Licença e Direitos Autorais

### Código-Fonte (Software)
O código-fonte deste projeto está licenciado sob a **[Licença MIT](LICENSE)**. Esta é a licença de código aberto mais permissiva e amplamente utilizada, permitindo que você use, copie, modifique, mescle, publique, distribua, sublicencie e/ou venda cópias do software para quaisquer fins (comerciais ou pessoais), exigindo apenas que o aviso de direitos autorais seja mantido.

### Textos e Manuscritos Bíblicos (Atuais & Planejados)
Diferente das traduções modernas protegidas por copyright restritivo (como NVI, ARA, NVT), as fontes primárias do nosso projeto estão em **Domínio Público** ou sob licenças de uso acadêmico livre:

*   **Antigo Testamento (Hebraico, Aramaico e Grego)**:
    *   **Códice de Leningrado (WLC)**: O manuscrito massorético completo mais antigo (Domínio Público).
    *   **Códice de Aleppo (Aleppo)**: Versão massorética de alta autoridade histórica (Domínio Público, via Sefaria).
    *   **Septuaginta (LXX)**: Tradução grega do AT do século III a.C. (Domínio Público).
    *   **Manuscritos do Mar Morto (DSS)**: Fragmentos sectários e bíblicos de Qumran (Domínio Público, via Sefaria).
    *   **Targum Onkelos & Pseudo-Jonathan (Aramaico)**: Traduções e paráfrases aramaicas antigas do Pentateuco (Domínio Público).
*   **Novo Testamento (Grego Koiné)**:
    *   **Textus Receptus (TR)**: O texto grego compilado por Erasmo, usado nas traduções da Reforma (Domínio Público).
    *   **Texto Majoritário/Bizantino (BYZ / RP2018)**: Representação da maioria dos manuscritos históricos sobreviventes (Domínio Público).
    *   **Texto Crítico (SBLGNT)**: Edição acadêmica moderna baseada nos manuscritos mais antigos (Licenciado abertamente pela *Society of Biblical Literature* para livre uso).
*   **Outras Versões Multilíngues de Alta Antiguidade**:
    *   **Peshitta Siríaca (Siríaco clássico)**: Manuscrito histórico siríaco (Domínio Público).
    *   **Cânon Ortodoxo Etíope (Ge'ez)**: Incluindo Livro de Enoque e Jubileus completos (Domínio Público).
    *   **Versão Clássica Armênia (Armênio Antigo)**: Conhecida filologicamente como a "Rainha das Versões" (Domínio Público).

---

### 📚 Materiais de Estudo Bíblico (Léxicos, Comentários & Gramáticas)
Para equipar o ecossistema open-source com o melhor aparato crítico, estamos integrando e traduzindo sistematicamente para o Português:

1.  **Léxicos (Dicionários de Idiomas Originais)**:
    *   **Strong's Greek Lexicon**: Léxico grego com códigos de concordância correspondentes (Domínio Público).
    *   **Strong's Hebrew Lexicon**: Léxico hebraico e aramaico correspondente (Domínio Público).
    *   **Brown-Driver-Briggs (BDB)**: O mais respeitado dicionário acadêmico de Hebraico Bíblico (Domínio Público).
    *   **Thayer's Greek-English Lexicon**: Dicionário clássico de Grego do Novo Testamento (Domínio Público).
2.  **Comentários Teológicos & Históricos Clássicos**:
    *   **Matthew Henry's Commentary on the Whole Bible**: O mais famoso comentário expositivo devocional (Domínio Público).
    *   **Albert Barnes' Notes on the Whole Bible**: Notas exegéticas e explicativas profundas versículo a versículo (Domínio Público).
    *   **The Pulpit Commentary**: Uma das maiores enciclopédias de homilética e exegese já criadas (Domínio Público).
3.  **Gramáticas de Idiomas Bíblicos**:
    *   **Gesenius' Hebrew Grammar**: A gramática de hebraico clássica de referência acadêmica (Domínio Público).
    *   **Gramáticas de Grego Koiné Clássicas**: ex: A.T. Robertson (Domínio Público).

---

### ⚖️ Análise Legal & Distribuição Open Source (100% Livre de Copyright!)
Muitas pessoas se perguntam: **Este material pode ficar exposto publicamente no nosso repositório Open Source do GitHub?**

**A resposta é SIM, 100% SEGURO!** Por três motivos legais sólidos:
1.  **As Obras Originais Estão em Domínio Público**: Todas as fontes primárias (Códices antigos) e os materiais de apoio (Strong, BDB, Thayer, Matthew Henry, Barnes, Gesenius) foram criados e publicados há mais de 100 anos. Pela lei de direitos autorais internacional (e a Lei 9.610/98 brasileira, que estipula o domínio público 70 anos após a morte do autor), **o direito autoral comercial dessas obras expirou**. Elas pertencem à humanidade!
2.  **A Tradução é de Nossa Autoria (IA)**: A tradução para o Português do Brasil é gerada através do nosso pipeline privado com a IA Qwen 2.5 32B. Como criadores e operadores deste pipeline, você possui total direito sobre a distribuição dos textos gerados.
3.  **Licença Aberta (MIT)**: Todo o código, dados estruturados e textos traduzidos estão protegidos e distribuídos sob a **Licença MIT**, permitindo que qualquer desenvolvedor, igreja, pesquisador ou ministério utilize os dados livremente para criar aplicativos, sites ou estudos sem pagar royalties ou sofrer processos de grandes editoras.

---

### 📊 Estimativa de Tamanho do Banco de Dados no Final
Mesmo com esse volume colossal de materiais e manuscritos, arquivos de texto JSON são **extremamente otimizados**. Veja a projeção final de tamanho do repositório:

| Categoria | Descrição | Tamanho Estimado |
| :--- | :--- | :--- |
| **Manuscritos de Texto** | Bíblia Completa + Apócrifos × 8 Versões Originais (JSON) | ~100 MB |
| **Léxicos e Dicionários** | Dicionário Strong Grego/Hebraico + BDB + Thayer (JSON) | ~40 MB |
| **Comentários Bíblicos** | Comentários Expositivos de Gênesis a Apocalipse (JSON) | ~350 MB |
| **Gramáticas Históricas** | Gesenius + Gramáticas de Grego e Siríaco | ~30 MB |
| **Total Projetado** | **Ecossistema Teológico Completo e Traduzido** | **~520 MB (0.52 GB)** |

*Isso significa que todo o ecossistema caberá perfeitamente no GitHub, baixando em menos de 10 segundos em qualquer conexão moderna!*

**Vantagem principal:** Você pode utilizar as traduções finais geradas por nossa IA de forma totalmente livre em sites, aplicativos, estudos e projetos para a sua comunidade, sem medo de infringir direitos autorais (copyright) de terceiros!
