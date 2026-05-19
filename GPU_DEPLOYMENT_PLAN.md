# Plano de Escalonamento GPU: AI-BIBLE (Oracle Cloud)

Este documento descreve o plano de ação e o estado da infraestrutura de altíssima performance para a tradução do corpus bíblico e manuscritos antigos utilizando a instância GPU ativa.

> [!NOTE]
> ### 📊 Status Atual do Escalonamento:
> * **Upgrade Conta PAYG:** ✅ **Concluído**
> * **Pedido de Limite (`gpu-a10-count`):** ✅ **Aprovado pela Oracle (Limite = 1)**
> * **Instância GPU (Frankfurt):** ✅ **Provisionada e Ativa** (`AI-BIBLE` sob shape `VM.GPU.A10.1`, IP `130.61.86.XX` - Ocultado por segurança)
> * **Serviços de Produção:** 🚀 **Ativos e Traduzindo** (Atualmente traduzindo 1 Samuel no Códice de Aleppo)

---

## 🎯 Objetivo de Performance Alcançado
Redução drástica no tempo de tradução da Bíblia inteira de **~15 dias** (na antiga instância gratuita ARM A1.Flex) para **~20 a 30 horas**, permitindo o uso em escala do modelo gigante **Qwen 2.5 (32 Bilhões de Parâmetros)** com o sofisticado pipeline de revisão em duas etapas (**Double-Pass Review**), garantindo a mais alta precisão acadêmica.

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
- **Ver o progresso da tradução ao vivo (Log de Execução):**
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
* **Consumo do Crédito:** O custo da instância gira em torno de **US$ 1,50 a US$ 2,00 por hora**. Como a tradução completa deve durar cerca de um dia, gastaremos em torno de **US$ 30 a US$ 40** dos seus créditos, preservando a maior parte do seu saldo promocional.

### ⚠️ Ação Crítica pós-Tradução:
Assim que as coleções que você deseja traduzir estiverem 100% salvas na pasta `output/` e sincronizadas no GitHub:
1. Acesse o console da **Oracle Cloud**.
2. Vá em **Instances** > Selecione `AI-BIBLE`.
3. Clique em **Terminate** (Destruir) e marque a caixa para deletar também o volume de boot associado.
4. **Isso é crucial para interromper a cobrança por hora imediatamente!**

---

## 🛠️ Tecnologias e Configurações Aplicadas

- **Double-Pass Self-Reflection (`DOUBLE_PASS_REVIEW = True`)**: O tradutor gera um rascunho acadêmico inicial (Passo 1) e o submete a uma autocrítica teológica (Passo 2) para corrigir concordâncias complexas e terminologias de línguas mortas antes de salvar.
- **NVIDIA CUDA & Docker Integration**: A máquina utiliza o **NVIDIA Container Toolkit** para mapear a aceleração da GPU A10 diretamente para o container Ollama, rodando o Qwen 32B com throughput altíssimo.
- **Dicionários Integrados**: Léxicos avançados (LSJ, Lewis & Short, Crum, Dillmann, Brockelmann, Bedrossian) mapeados diretamente na pasta `data/` para enriquecer a validação de variantes textuais.

---
*Atualizado em: 18 de Maio de 2026*
