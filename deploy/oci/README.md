# GPU deploy (Oracle Cloud) — AI-BIBLE

This folder contains helper artifacts to run the translation pipeline on an OCI GPU instance (example: `VM.GPU.A10.1`, 24GB VRAM) using quantization/offload tooling.

Quick steps

1. SSH into your OCI GPU instance and clone this repo.
2. Build the GPU image:

```bash
cd deploy/oci
docker compose -f docker-compose.gpu.yml build
```

3. Run the container (it will run `setup_gpu.sh`):

```bash
docker compose -f docker-compose.gpu.yml up -d
```

Notes and best practices for `VM.GPU.A10.1` (24GB VRAM)

- Use quantized models (4‑bit) via `bitsandbytes` when possible to fit 13B–30B models.
- Use `vLLM` or `FlexGen` for NVMe offload if the model cannot fit in VRAM.
- For highest quality on large models (≥70B) prefer multi‑GPU instances (A100/H100) or model sharding.

Recommended runtime flags (example for `vLLM` server):

```bash
# run vLLM with quantization/offload hints (example)
vllm --model /path/to/model --quantization bitsandbytes --num-gpus 1
```

If you want, I can generate a ready `docker-compose` service that launches a `vLLM` inference server and a separate `translator` service that calls it.

I created an example `docker-compose.vllm.yml` that launches a `vllm` service and a `translator` service. To run it:

```bash
cd deploy/oci
docker compose -f docker-compose.vllm.yml up -d --build
```

To prepare a quantized model locally (download + hint for on‑GPU quantization):

```bash
cd deploy/oci
./quantize_model.sh <hf-repo-id> ./models/<name>
```

If you want, I can: (A) update `translate_bible.py` to call the `vLLM` server endpoint by default, and (B) trigger a small test run using a short chapter to measure throughput on your target instance (you'll need to give me access or run the commands locally).


