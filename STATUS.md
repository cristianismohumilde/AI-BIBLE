# Status do Projeto: IA-BIBLE (Ponto de Restauração — Fase GPU Frankfurt ATIVA)

Este arquivo serve para documentar exatamente onde o projeto está em **18 de Maio de 2026** (Sucesso na ativação da GPU em Frankfurt e automação dos serviços).

## ✅ O que já está pronto e funcional:

1. **Infraestrutura GPU Ativa (Frankfurt)**:
   - **Instância Ativa**: `AI-BIBLE` rodando sob o shape robusto **`VM.GPU.A10.1`** (15 OCPUs, 240 GB RAM, 1x GPU NVIDIA A10 de 24GB VRAM).
   - **IP Público**: `130.61.86.XX` (Ocultado por segurança)
   - **Sistema Operacional**: Ubuntu 22.04 LTS.
   - **Segurança de Acesso**: Chave SSH `frank-private.key` configurada e validada.

2. **Configuração Automatizada (NVIDIA + Docker)**:
   - Repositório local e manuscritos fontes (`data/`) submetidos com sucesso para a VM.
   - Drivers NVIDIA e CUDA instalados e validados via `nvidia-smi` (Driver 535.288.01, CUDA 12.2).
   - Docker & Docker Compose integrados perfeitamente com o **NVIDIA Container Toolkit** para aceleração total de hardware 32B.

3. **Serviços de Background Imortais**:
   - **Serviço do Tradutor (`translate_bible.service`)**: Configurado como serviço nativo do sistema (`systemd`). Roda em segundo plano sob o usuário seguro `ubuntu`, com reinício automático garantido caso falte luz, RAM ou GPU.
   - **Serviço de Sincronização (`vm_autopush.py`)**: Ativo em segundo plano (`nohup`), compilando o progresso automaticamente e empurrando-o de 5 em 5 minutos para o GitHub.
   - **Destrave de Permissões**: Resolvidos todos os cadeados de leitura/escrita antigos gerados por execuções do root na pasta `output/` e nos logs.

4. **Escopo Expandido e Dicionários**:
   - Baixados todos os léxicos acadêmicos primários solicitados (LSJ para Grego, Lewis & Short para Latim da Vulgata, Crum para Copta, Dillmann para Ge'ez/Etíope, Brockelmann para Siríaco e Bedrossian para Armênio Clássico) na pasta `data/`.
   - Baixado o léxico completo de Strong de Grego e Hebreu (~14.000 verbetes).
   - Mapeados e baixados todos os manuscritos deuterocanônicos, apócrifos e históricos (Enoque, Jubileus, Mishná, Testamentos dos Patriarcas) para tradução posterior.

5. **Estratégia Híbrida de Tradução Inteligente (Single-Pass + Double-Pass Posterior)**:
   - **Single-Pass Ativo por Padrão (`DOUBLE_PASS_REVIEW = False`)**: A VM traduz todos os manuscritos, livros, versões e materiais em passe único de altíssima velocidade (1 capítulo a cada 15-30 segundos). Isso economiza cerca de 50% do orçamento de créditos e acelera drasticamente a finalização.
   - **Polimento Crítico Posterior (`review_existing_translations.py`)**: Criado um script dedicado para fazer a revisão teológica/gramatical profunda (Passe 2 - Autocrítica) após a conclusão das traduções. O script filtra de forma inteligente e foca o processamento apenas em coleções e livros altamente complexos (como Septuaginta (LXX), Aramaico do Targum, Talmud, Peshitta, Copta, Armênio, e livros poéticos do hebraico como Salmos e Isaías), otimizando custos e tempo de GPU.

6. **Leitor Interlinear em Tempo Real (`index.html`)**:
   - Criado e implantado um portal estático premium (JAMstack) no raiz do repositório, hospedado gratuitamente via **GitHub Pages**.
   - O site exibe os textos em hebraico alinhados à direita (RTL em fonte *Cardo*) lado a lado com a tradução em português, carregando os dados dinamicamente dos JSONs à medida que a GPU faz o push, permitindo o monitoramento do projeto em tempo real!

## 📈 Status Atual da Tradução:
- **Códice de Aleppo**: Sendo traduzido ativamente! O tradutor está voando baixo e já concluiu até o capítulo **5 de 2 Reis**!
- **Total no GitHub**: **123 capítulos** totalmente traduzidos e consolidados!
- **Progresso do Códice de Aleppo**: **13.3% concluído**!
- **ETA Estimado**: Reduzido para cerca de **4 a 5 dias** com a ativação da estratégia Single-Pass!

## 🚧 Próximos Passos (Ações futuras):
1. **Varredura Completa**: Deixar o tradutor concluir o Códice de Aleppo em modo Single-Pass e prosseguir automaticamente para o Texto de Leningrado (WLC), Septuaginta (LXX), Manuscritos do Mar Morto (DSS) e Vulgata Latina.
2. **Ciclo de Polimento (Double-Pass)**: Após a tradução completa em Single-Pass, rodar o script `review_existing_translations.py` para polir os livros prioritários e manuscritos complexos usando o orçamento restante de créditos da Oracle Cloud.
3. **Integração das Variantes Textuais**: Após a tradução de cada manuscrito, iniciar a geração dos relatórios de variantes críticas com base nos dicionários multilíngues.

---
*Assinado com orgulho: Antigravity (Sua IA de programação parceira)*
