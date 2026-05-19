# AI-BIBLE — Resumo de Implantação e Testes (Oracle Cloud)

Resumo executivo do status de implantação e escalonamento para GPU na nuvem de Frankfurt.

**Propósito**
- Documentar a arquitetura ativa de tradução da IA-BIBLE na nuvem e o status atual da infraestrutura.

## 🚀 Status da Infraestrutura (18/05/2026)

*   **Instância Ativa**: `AI-BIBLE` em **Frankfurt (Alemanha Central)**.
*   **Shape**: `VM.GPU.A10.1` (15 núcleos OCPU, 240 GB RAM, 1x GPU NVIDIA A10 com 24GB de VRAM).
*   **IP Público**: `130.61.86.XX` (Ocultado por segurança)
*   **SO**: Ubuntu 22.04 LTS.
*   **Drivers NVIDIA**: ✅ Instalados e ativos (Driver 535.288.01, CUDA 12.2).
*   **Docker & Docker Compose**: ✅ Instalados e configurados com o **NVIDIA Container Toolkit** para aceleração nativa de hardware em containers.

## 📂 O que foi implantado e configurado na VM
- `deploy/oci/setup_vm_deps.sh` — script automatizado que configurou todos os drivers NVIDIA, CUDA, Docker e Container Toolkit na VM limpa em tempo recorde (~6 minutos).
- `docker-compose.yml` (atualizado) — configurado para permitir que o Ollama utilize a aceleração nativa da GPU.
- Código do repositório extraído em `~/AI-BIBLE` na VM com todas as dependências e manuscritos prontos.
- **Serviço de Produção Imortal**: Configurado o serviço de sistema `translate_bible.service` rodando em segundo plano (`systemd`) para garantir execução ininterrupta.
- **Serviço de Auto-Envio**: Configurado o script `vm_autopush.py` para sincronizar e atualizar o progresso no GitHub automaticamente a cada 5 minutos.

## 🗺️ Mapa de Expansão (Novo Escopo)
O projeto agora integra uma visão filológica e teológica ainda mais ambiciosa:
1.  **Integração Completa da Sefaria**: Download e tradução de toda a base de dados do portal Sefaria diretamente para o português brasileiro.
2.  **Apócrifos e Deuterocanônicos**:
    - *Antigo Testamento*: Enoque, Jubileus, Tobias, Judite, Sabedoria, Eclesiástico, Baruque, Macabeus.
    - *Novo Testamento*: Evangelho de Tomé, Epístola aos Hebreus, Epístola de Barnabé, Didaqué, Pastor de Hermas.
3.  **Idiomas Antigos Adicionais**:
    - Porções e Targums em **Aramaico**.
    - Peshitta em **Siríaco**.
    - Cânon Ortodoxo Completo em **Ge'ez (Etíope Clássico)**.
    - Manuscritos clássicos em **Armênio Clássico**.
4.  **Materiais de Estudo Integrados**:
    - Dicionários/Léxicos (Grego/Hebraico de Strong, Brown-Driver-Briggs, Thayer).
    - Comentários bíblicos clássicos (Matthew Henry, Albert Barnes, Pulpit Commentary).
    - Gramáticas históricas (Gesenius, Robertson).

*Nota: Os downloads dessas coleções são realizados diretamente pela VM de Frankfurt (largura de banda de rede de 24 Gbps), economizando largura de banda local.*

## ⚙️ Status Rápido dos Serviços
A tradução e os containers de inferência estão operando em segundo plano. O tradutor está traduzindo ativamente sob o processo acadêmico de revisão em duas etapas (**Double-Pass Review**)!

---
*Status: Infraestrutura de GPU configurada com sucesso e 100% operacional!*
