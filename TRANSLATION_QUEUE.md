# 📋 Fila de Tradução Ativa — AI-BIBLE (Fase GPU Frankfurt)

Este arquivo documenta a priorização oficial da fila de tradução para a Fase GPU, detalhando o status real e atualizado de cada manuscrito/versão antiga.

> Gerado dinamicamente em: **2026-05-21 05:32 UTC**

---

## 🏆 Status Atual das Coleções

| Prioridade | Fonte | Idioma Original | Status Real | Localização | Observações |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **—** | Códice de Aleppo | Hebraico Massorético | **✅ 100% Traduzido** | `output/Aleppo/` | Concluído com sucesso na GPU A10. |
| **—** | Septuaginta (LXX) | Grego Clássico (Seleção) | **✅ 100% Traduzido** | `output/LXX/` | Seleção prioritária de Isaías, Salmos e Deuterocanônicos. |
| **—** | Ge'ez Clássico | Ge'ez (Etíope Clássico) | **✅ 100% Traduzido** | `output/Geez/` | Deuterocanônicos e Novo Testamento em Ge'ez Puro. |
| **1** | **Targum Onkelos (Gênesis)** | Aramaico Antigo | **🚀 Traduzindo (9/50 caps)** | `output/Targum_Onkelos/` | Rodando ativamente na VM (Gênesis priorizado). |
| **2** | **Manuscritos do Mar Morto (DSS)** | Hebraico/Aramaico de Qumran | **⏳ Aguardando Fila** | `data/DSS/` | Apenas Isaías e Habakkuk alinhados com o Hebraico original. |
| **3** | **Targum Onkelos (Restante)** | Aramaico Antigo | **⏳ Aguardando Fila** | `data/ancient_versions/` | Restante da Torá aramaica. |
| **4** | **Texto Bizantino (BYZ)** | Grego Koiné | **⏳ Aguardando Fila** | `data/BYZ/` | Apenas Novo Testamento. |
| **5** | **Peshitta Siríaca** | Siríaco Clássico | **⏳ Aguardando Fila** | `data/ancient_versions/` | Novo Testamento Siríaco. |
| **6** | **Copta Saídico** | Copta Saídico | **⏳ Aguardando Fila** | `data/ancient_versions/` | Novo Testamento Copta. |
| **7** | **Armênio Oriental** | Armênio Clássico | **⏳ Aguardando Fila** | `data/ancient_versions/` | Novo Testamento Armênio. |

---

## 🚫 Coleções Pausadas (Fora dos Recursos - Limite $300 USD)
As seguintes fontes estão desativadas no tradutor e não gastam orçamento até liberação de novos créditos:
- **WLC** (Códice de Leningrado) — *Hebraico Massorético*
- **SBLGNT** — *Grego Koiné Crítico*
- **Textus Receptus (TR)** — *Grego Koiné*
- **Vulgata Latina (VUL)** — *Latim Clássico*
- **Talmud Bavli** — *Hebraico Mishnaico e Aramaico Talmúdico*

---

## 🔄 Dinâmica da Sincronização
1. O tradutor da VM consome esta fila de forma sequencial com base no arquivo `translate_bible.py`.
2. As pastas marcadas como `✅ 100% Traduzido` estão bloqueadas no código (`SKIP_MANUSCRIPTS`) e não consomem processamento.
3. À medida que novos capítulos são salvos em `output/`, os arquivos `PROGRESS.md` e `TRANSLATION_QUEUE.md` são atualizados a cada 5 minutos pelo serviço automático da VM.
