# Plano de Escalonamento GPU: AI-BIBLE (Oracle Cloud)

Este documento descreve o plano de ação para escalar a tradução da Bíblia inteira utilizando os **$300 de créditos iniciais** da Oracle Cloud, saindo da limitação de processamento por CPU (Always Free) para o uso de Placas de Vídeo (GPU) de altíssima performance.

> [!NOTE]
> ### 📊 Status Atual do Escalonamento:
> * **Upgrade Conta PAYG:** ✅ **Concluído**
> * **Pedido de Limite (`gpu-a10-count`):** 📩 **Enviado ao Suporte (17/05/2026) - Em Análise**
> * **Status Geral:** ⏳ **Aguardando Liberação da GPU pela Oracle**

## 🎯 Objetivo
Reduzir o tempo de tradução da Bíblia inteira de **~15 dias** (na instância gratuita A1.Flex) para **menos de 10 horas**, permitindo o uso do modelo gigante **Qwen 2.5 (32 Bilhões de Parâmetros)**, garantindo a mais alta precisão acadêmica.

## 💰 Análise de Custos e Créditos
* **Instância Alvo:** `VM.GPU.A10.1` (Contém 1x NVIDIA A10 com 24 GB de VRAM).
* **Custo Estimado da Nuvem:** US$ 1,50 a US$ 2,00 por hora.
* **Consumo do Crédito:** Como a tradução completa deve levar apenas um dia ou menos, gastaremos em torno de **US$ 15 a US$ 20** dos seus US$ 300 disponíveis, preservando quase todo o seu saldo.

---

## 🚀 Passo a Passo da Implementação

### 1. Criar a Instância GPU (e Solução se o Shape GPU não aparecer)

> [!IMPORTANT]
> **Por que o shape `VM.GPU.A10.1` não aparece na lista?**
> Por padrão, contas no nível **Free Trial** (mesmo com os $300 de créditos ativos) possuem o limite de serviço para GPUs definido como **0** pela Oracle. Para que os shapes de GPU fiquem visíveis e possam ser criados, você precisa atualizar sua conta para **Pay As You Go (PAYG)**.
> 
> * **Os créditos de $300 serão perdidos?** **NÃO!** Ao migrar para PAYG, seus créditos restantes do Free Trial continuam válidos pelos 30 dias originais e serão consumidos primeiro.
> * **Como migrar:** No painel da Oracle Cloud, clique no banner de upgrade ou vá em **Upgrade Account** no menu da sua conta.
> * **Como verificar os limites:** Vá em **Governance & Administration** > **Limits, Quotas and Usage**, filtre pelo serviço **Compute** e procure pelo shape `VM.GPU.A10` ou similar para ver seu limite atual.

1. Acesse o painel da Oracle Cloud.
2. Crie uma nova instância Compute.
3. Clique em **Change Shape**.
4. Selecione a aba **Specialty and previous generation**.
5. Em **Shape series**, procure por **GPU** e selecione `VM.GPU.A10.1` (placa NVIDIA A10, 24 GB de VRAM).
6. Em **Image**, escolha **Canonical Ubuntu 22.04** (ou Ubuntu 22.04 LTS GPU Optimized se disponível na sua região).
7. Em **Boot Volume**, especifique no mínimo **100 GB** para comportar o sistema operacional, drivers CUDA e o modelo Qwen (19 GB).
8. Adicione sua chave SSH e crie a instância.

### 2. Configurar o Ambiente
Faça o acesso via SSH (`ssh ubuntu@IP_DA_GPU`) e instale o Docker e os drivers essenciais (a imagem padrão de GPU do Ubuntu na Oracle geralmente já vem com os drivers da NVIDIA instalados).
Faça o upload do projeto (`AI-BIBLE.zip`) ou clone o repositório do GitHub e extraia os arquivos.

### 3. Restabelecer o Modelo de 32B
Abra o arquivo `translate_bible.py` com o comando `nano translate_bible.py` e altere a variável do modelo novamente para a versão de 32 Bilhões de parâmetros (que agora vai caber e voar nos 24GB de VRAM da placa de vídeo):

```python
# Mudar de:
MODEL_NAME = "qwen2.5:7b"
# Para:
MODEL_NAME = "qwen2.5:32b"
```

### 4. Subir e Traduzir
Execute o processo padrão de deploy, idêntico ao ambiente de testes:

```bash
# Sobe a infraestrutura (O Docker vai usar automaticamente a GPU se disponível)
docker compose up -d --build

# Baixa todos os manuscritos brutos das APIs (BollsLife e Sefaria)
docker compose exec translator python download_manuscripts.py

# Puxa o modelo de 19GB (na nuvem com link gigabit, leva uns 5 minutos)
docker compose exec ollama ollama pull qwen2.5:32b
```

Inicie a tradução em uma sessão protegida (`tmux`):
```bash
tmux
docker compose exec translator python translate_bible.py
```
*Lembre-se: `Ctrl+B`, depois `D` para sair.*

### 5. Salvar e Destruir (CRÍTICO)
Assim que os JSONs estiverem prontos na pasta `output/`:
1. Use o `scp` (ou WinSCP) na sua máquina local para baixar a pasta com os dados gerados.
2. Após ter 100% de certeza de que as traduções estão salvas no seu PC, vá no painel web da Oracle Cloud.
3. Clique em **Terminate** (Destruir) na instância GPU para **PARAR a cobrança por hora**!
4. O resultado final (JSONs) volta a ser hospedado na sua maquininha pequena Always Free!

---

## 📌 Observações sobre faturamento, Marketplace e uso de créditos OCI

- Créditos OCI: os créditos promocionais da Oracle (ex.: US$300) cobrem serviços e recursos dentro da conta OCI (Compute, Block/Object Storage, serviços gerenciados e soluções contratadas via Oracle Cloud Marketplace). Eles NÃO pagam diretamente chamadas a APIs externas (ex.: OpenAI, Anthropic) a menos que o fornecedor ofereça a integração através do Oracle Cloud Marketplace e permita faturamento via OCI.
- `OCI Generative AI` / Marketplace: a Oracle oferece serviços e imagens de modelos dentro do OCI (por exemplo, modelos gerenciados ou imagens de fornecedores no Marketplace). Serviços e soluções contratadas e cobradas via a sua conta OCI normalmente consomem seus créditos.

## ⚙️ Estratégias recomendadas quando quer gastar somente com créditos OCI

- Self‑host em instância OCI GPU (controle total, usa apenas créditos OCI):
	- Hospede modelos open‑source em `VM.GPU.*` e pague somente infraestrutura com seus créditos.
	- Para modelos maiores que a VRAM, empregue quantização 4‑bit (`bitsandbytes`) e frameworks de offload/otimização (`vLLM`, `FlexGen`, `DeepSpeed`) para rodar 13B–70B em GPUs com 24–48GB de VRAM com trade‑offs de qualidade/custo.

- Usar soluções via Oracle Marketplace / OCI Generative AI (mais simples, usa créditos OCI se a oferta estiver integrada ao Marketplace):
	- Se um provedor publicar o modelo no Oracle Cloud Marketplace e permitir faturamento via OCI, a cobrança é feita na sua conta Oracle (portanto usando créditos).
	- Nem todo fornecedor oferece faturamento via OCI — confirme na página do produto no Marketplace.

## 🔧 Ferramentas e técnicas de inferência

- Quantização: `bitsandbytes` (4‑bit) para reduzir VRAM.
- Servidores de inferência: `vLLM`, `FlexGen` (NVMe offload), `DeepSpeed‑Inference`.
- Indexação/RAG: `FAISS`/`Milvus`/`Weaviate` para recuperar notas críticas e usar o modelo para pós‑edição.

## 🧭 Modelos e notas de licença

- Tradução direta: `NLLB` para línguas com suporte; modelos de tradução neural paralela podem ser combinados com LLMs para pós‑edição.
- LLMs para contextualização: `Llama‑3`, `Mistral`, `Mixtral` e `Qwen` (verifique licenças; alguns pesos são proprietários).
- Para textos aramaicos, siríacos, copta, armênio e ge'ez será necessário fine‑tuning e corpora paralelos; espere trabalho de curadoria e validação acadêmica.

## ✅ Conclusão prática

- Gastando somente créditos OCI: prefira self‑host (instâncias GPU + quantização/offload) ou contratar modelos publicados no Oracle Marketplace/OCI GenAI que aceitem faturamento via OCI.
- Se preferir usar OpenAI/Anthropic, esses serviços exigirão pagamento externo (cartão) e não usarão seus créditos OCI.

---

## Próximos passos sugeridos

1. Verificar na sua conta OCI se há ofertas relevantes em `Oracle Cloud Marketplace` e ativar `OCI Generative AI` quando disponível.
2. Decidir: (a) self‑host + quantização/offload (usa créditos OCI) ou (b) contratar oferta no Marketplace/OCI GenAI (se disponível e faturada via OCI).
3. Se escolher self‑host, posso gerar os scripts de setup (Docker + vLLM/FlexGen + bitsandbytes) otimizados para `VM.GPU.A10.1`.

4. Implementação: criei os artefatos em `deploy/oci/` (Dockerfile, compose, scripts e docs).

---

## Implementação aplicada

- Adicionados artefatos em `deploy/oci/` para facilitar o deploy self‑host:
	- `Dockerfile.gpu`, `docker-compose.gpu.yml`, `setup_gpu.sh`
	- `docker-compose.vllm.yml` — inicia `vllm` + `translator`
	- `download_and_quantize.py`, `quantize_model.sh` — helpers para baixar e preparar modelos
	- `README.md` e `OCI_MARKETPLACE_CHECKLIST.md` com instruções rápidas

Use esses arquivos como ponto de partida para executar um servidor de inferência local na sua instância GPU OCI.

---

Status atual: scripts e compose para self‑host gerados em `deploy/oci/`.

