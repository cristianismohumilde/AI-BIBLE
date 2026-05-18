# AI-BIBLE — Deploy & Test Summary (Oracle Cloud)

Resumo conciso para subir no GitHub e escolher a rota amanhã.

**Propósito**
- Documentar o que foi implementado para executar o pipeline de tradução em uma instância GPU na Oracle Cloud (self‑host) e as opções de Marketplace/OCI GenAI.

**O que foi adicionado**
- `deploy/oci/Dockerfile.gpu` — imagem base com CUDA e libs de inferência.
- `deploy/oci/docker-compose.gpu.yml` — compose para container translator GPU.
- `deploy/oci/docker-compose.vllm.yml` — inicia `vLLM` (inference server) + `translator` (cliente).
- `deploy/oci/setup_gpu.sh` — script de inicialização (venv + libs).
- `deploy/oci/download_and_quantize.py` e `deploy/oci/quantize_model.sh` — helpers para baixar modelos HF e instrução de quantização 4‑bit.
- `deploy/oci/README.md` — instruções rápidas de execução.
- `deploy/oci/OCI_MARKETPLACE_CHECKLIST.md` — como validar ofertas faturadas via OCI.
- Atualizei `GPU_DEPLOYMENT_PLAN.md` com observações sobre créditos OCI, quantização/offload e recomendações.

Links rápidos (arquivos gerados)
- [deploy/oci/Dockerfile.gpu](deploy/oci/Dockerfile.gpu)
- [deploy/oci/docker-compose.gpu.yml](deploy/oci/docker-compose.gpu.yml)
- [deploy/oci/docker-compose.vllm.yml](deploy/oci/docker-compose.vllm.yml)
- [deploy/oci/setup_gpu.sh](deploy/oci/setup_gpu.sh)
- [deploy/oci/download_and_quantize.py](deploy/oci/download_and_quantize.py)
- [deploy/oci/quantize_model.sh](deploy/oci/quantize_model.sh)
- [deploy/oci/README.md](deploy/oci/README.md)
- [GPU_DEPLOYMENT_PLAN.md](GPU_DEPLOYMENT_PLAN.md)

Quick start (assumindo instância `VM.GPU.A10.1` e acesso SSH)

```bash
# build and run vLLM + translator
cd deploy/oci
docker compose -f docker-compose.vllm.yml up -d --build

# or: build minimal GPU image
docker compose -f docker-compose.gpu.yml build
docker compose -f docker-compose.gpu.yml up -d

# prepare model locally (download hint)
./quantize_model.sh <hf-repo-id> ./models/<name>

# run translator directly (example)
docker compose -f docker-compose.vllm.yml exec translator python translate_bible.py --endpoint http://vllm:8080
```

Estimativa de tempo e custo (aprox.)
- Provisionamento + build: 1–3 horas.
- Download modelo: 5 min–3 horas (depende do tamanho e região).
- Quantização 4‑bit na GPU: 10 min–2 horas.
- Tradução de todo o corpus (Bíblia + deuterocanônicos + patrística):
  - 13B quantizado em A10.1: ~12–36 horas.
  - 30–70B com offload em A10.1: ~8–24 horas.
- Custo A10.1 (≈US$1.50–2.00/h): proj.: US$12–72 para runs descritos acima. Seus ~US$300 cobrem amplamente o protótipo e testes.

Decisões a tomar amanhã (checklist)
- Escolher modelo para teste inicial (sugestões: `Llama-3-13b`, `Mistral-7B`, `meta-llama/Llama-2-13b`, `facebook/nllb-200-3.3B`).
- Confirmar rota: (A) Self‑host com quantização/offload (usa créditos OCI) ou (B) Marketplace/OCI GenAI (se houver oferta faturada via OCI).
- Confirmar que os créditos OCI estão ativos e identificar região para menor latência/custo.
- Rodar teste curto (1 capítulo) e avaliar qualidade; ajustar modelo/FT se necessário.

Próximos passos que posso executar (só pedir)
- Atualizar `translate_bible.py` para apontar por padrão para `vLLM` endpoint e executar um teste curto de throughput.
- Gerar script automático para baixar + quantizar um modelo escolhido e colocar em `/models`.
- Ajudar a lançar a instância OCI (com `oci` CLI) e executar os comandos de build/run.

Como subir para o GitHub (comandos)

```bash
git add .
git commit -m "Add OCI GPU deploy helpers and vLLM compose + docs"
git push origin main
```

Observação final
- Tudo está documentado em `deploy/oci/README.md` e o plano geral em `GPU_DEPLOYMENT_PLAN.md`. Quando acordar me diga o modelo que quer testar e eu preparo a quantização automática e atualizo `translate_bible.py` para o endpoint `vLLM`.
