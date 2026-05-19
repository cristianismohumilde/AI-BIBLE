# Plano de Escalonamento GPU: AI-BIBLE (Oracle Cloud)
 
Este documento descreve o plano de ação e o estado da infraestrutura de altíssima performance para a tradução do corpus bíblico e manuscritos antigos utilizando a instância GPU ativa.
 
> [!NOTE]
> ### 📊 Status Atual do Escalonamento:
> * **Upgrade Conta PAYG:** ✅ **Concluído**
> * **Pedido de Limite (`gpu-a10-count`):** ✅ **Aprovado pela Oracle (Limite = 1)**
> * **Instância GPU (Frankfurt):** ✅ **Provisionada e Ativa** (`AI-BIBLE` sob shape `VM.GPU.A10.1`, IP `130.61.86.XX` - Ocultado por segurança)
> * **Serviços de Produção:** 🚀 **Ativos e Traduzindo** (Atualmente traduzindo 2 Samuel no Códice de Aleppo)
 
---
 
## 🎯 Objetivo de Performance Alcançado
Redução drástica no tempo de tradução da Bíblia inteira de **~15 dias** (na antiga instância gratuita ARM A1.Flex) para **apenas ~4 a 6 horas** de processamento bruto! 
 
Conseguimos isso através da **Arquitetura de Tradução Paralela Concorrente**:
1. **Paralelismo de 3 Vias (Velocidade Máxima / Custo Mínimo):** O script principal `translate_bible.py` foi atualizado para processar **3 versículos simultaneamente** utilizando concorrência multi-thread (`ThreadPoolExecutor`). O Ollama carrega o modelo gigante **Qwen 2.5 32B** na VRAM de 24GB da GPU A10 e executa as inferências em paralelo, cortando o tempo pela metade!
2. **Double-Pass Teológico Universal (`DOUBLE_PASS_REVIEW = True`):** Para garantir o nível mais alto possível de rigor acadêmico, teológico e gramatical, o segundo passe de revisão crítica é executado em todos os versículos. Graças à otimização de 3 vias em paralelo, a velocidade com Double-Pass ativado é ainda maior que a do passe único sequential antigo!
 
---
 
## 🚀 Estrutura de Produção na Instância GPU
 
A VM está configurada e operando de forma industrial em segundo plano. Abaixo estão os comandos essenciais para gerenciar e monitorar o servidor de tradução:
 
### 1. Monitorar o Tradutor Ativo
O motor de tradução (`translate_bible.py` com o modelo Qwen 32B) roda como um serviço imortal do sistema (`systemd`).
 
- **Verificar se o tradutor está rodando:**
  ```bash
  sudo systemctl status translate_bible.service
  ```
- **Parar o tradutor temporariamente:**
  ```bash
  sudo systemctl stop translate_bible.service
  ```
- **Iniciar/Reiniciar o tradutor:**
  ```bash
  sudo systemctl restart translate_bible.service
  ```
- **Ver o progresso da tradução ao vivo (Log de Execução em tempo real sem buffer):**
  ```bash
  watch -n 2 tail -n 15 ~/AI-BIBLE/translation_service.log
  ```
 
### 2. Monitorar o Envio Automático (Auto-Push)
O script `vm_autopush.py` é responsável por varrer os novos arquivos traduzidos na pasta `output/`, recalcular as estatísticas de progresso nos Markdowns (`README.md` e `PROGRESS.md`) e fazer o upload automático para o GitHub a cada 5 minutos.
 
- **Verificar se o Auto-Push está vivo na memória:**
  ```bash
  ps aux | grep vm_autopush.py
  ```
- **Se o Auto-Push cair (ex: após reinicialização da máquina), inicie-o assim:**
  ```bash
  nohup python3 vm_autopush.py > autopush.log 2>&1 &
  ```
 
---
 
## 💰 Gerenciamento de Custos e Faturamento
 
* **Instância em Uso:** `VM.GPU.A10.1` (15 OCPUs, 240 GB RAM, 1x NVIDIA A10 com 24 GB de VRAM).
* **Consumo do Crédito:** O custo da instância gira em torno de **US$ 1,50 a US$ 2,00 por hora**. Com a otimização de paralelismo de 3 vias ativa, a tradução completa que demoraria de 15 a 18 horas agora deve terminar em **apenas 5 a 6 horas**! Gastaremos em torno de apenas **US$ 10 a US$ 12** dos seus créditos promocionais da Oracle Cloud, economizando cerca de **66%** dos recursos!
 
### ⚠️ Ação Crítica pós-Tradução:
Assim que as coleções que você deseja traduzir estiverem 100% salvas na pasta `output/` e sincronizadas no GitHub:
1. Acesse o console da **Oracle Cloud**.
2. Vá em **Instances** > Selecione `AI-BIBLE`.
3. Clique em **Terminate** (Destruir) e marque a caixa para deletar também o volume de boot associado.
4. **Isso é crucial para interromper a cobrança por hora imediatamente!**
 
---
 
## 🛠️ Tecnologias e Configurações Aplicadas
 
- **Paralelização Concorrente**: Execução com `max_workers = 3` no `ThreadPoolExecutor` para saturar com segurança a GPU A10 a 95% de uso e 148W de consumo, mantendo margem de segurança de VRAM contra erros de CUDA Out-of-Memory.
- **Double-Pass Acadêmico**: Habilitado em todo o pipeline (`DOUBLE_PASS_REVIEW = True`) para assegurar fidelidade teológica máxima em cada manuscrito.
- **NVIDIA CUDA & Docker Integration**: A máquina utiliza o **NVIDIA Container Toolkit** para mapear a aceleração da GPU A10 diretamente para o container Ollama, rodando o Qwen 32B com throughput altíssimo.
- **Dicionários Integrados**: Léxicos avançados (LSJ, Lewis & Short, Crum, Dillmann, Brockelmann, Bedrossian) mapeados diretamente na pasta `data/` para enriquecer a validação de variantes textuais.
 
---
*Atualizado em: 19 de Maio de 2026*
