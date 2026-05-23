# GPU Scaling Plan: AI-BIBLE (Oracle Cloud)

This document describes the action plan to scale the translation of the entire Bible utilizing the **US$ 300 free trial credits** of Oracle Cloud, moving from CPU processing (Always Free limits) to high-performance Graphics Processing Units (GPU).

> [!NOTE]
> ### 📊 Current Scaling Status:
> * **PAYG Account Upgrade:** ✅ **Completed**
> * **Service Limit Request (`gpu-a10-count`):** ✅ **Approved (05/18/2026)**
> * **GPU Instance (Frankfurt):** ✅ **Active (130.61.86.XX)** (Obfuscated for security)
> * **General Status:** 🚀 **Ready to initiate High-Speed Translation!**

## 🎯 Objective & Performance Optimization
Reduce the translation time of the entire Bible from **~15 days** (on the free A1.Flex CPU instance) to **only ~10 to 15 hours**, achieved via a highly strategic **Hybrid Translation Strategy**:
1. **Single-Pass Translation (Warp Speed / Low Cost):** The primary script `translate_bible.py` translates the entire corpus directly (`DOUBLE_PASS_REVIEW = False`), running at an amazing speed of **1 chapter every 15 to 30 seconds** on the GPU A10. This cuts costs by 50%.
2. **Selective Double-Pass Post-Processor (`review_existing_translations.py`):** We created a post-processing script that executes the second theological/linguistic critique (Self-Reflection Pass) *after* the initial translation is done, and **only on highly complex books** (Septuagint (LXX), Targum Aramaic, Talmud, Peshitta Syriac, Coptic, Armenian, and poetic Hebrew books like Psalms and Isaiah), saving massive cloud credits.

## 💰 Cost and Credit Analysis
* **Target Shape:** `VM.GPU.A10.1` (Contains 1x NVIDIA A10 with 24 GB of VRAM).
* **Estimated Cloud Cost:** US$ 1.50 to US$ 2.00 per hour.
* **Credit Consumption:** Since the full translation should take a day or less, we will spend around **US$ 15 to US$ 20** of your US$ 300 available, preserving almost all of your balance.

---

## 🚀 Step-by-Step Implementation

### 1. GPU Instance Creation (and Solution if GPU Shape is Hidden)

> [!IMPORTANT]
> **Why doesn't the `VM.GPU.A10.1` shape appear in the list?**
> By default, Free Trial accounts (even with active $300 credits) have their GPU service limits set to **0** by Oracle. To make GPU shapes visible and create them, you must upgrade your account to **Pay As You Go (PAYG)**.
> 
> * **Will I lose my $300 credits?** **NO!** When migrating to PAYG, your remaining Free Trial credits remain valid for the original 30 days and will be consumed first.
> * **How to migrate:** In the Oracle Cloud dashboard, click the upgrade banner or go to **Upgrade Account** under your account menu.
> * **How to verify limits:** Go to **Governance & Administration** > **Limits, Quotas and Usage**, filter by the **Compute** service, and search for the `VM.GPU.A10` shape to view your current limit.

1. Access the Oracle Cloud dashboard.
2. Create a new Compute instance.
3. Click on **Change Shape**.
4. Select the **Specialty and previous generation** tab.
5. Under **Shape series**, select **GPU** and select `VM.GPU.A10.1` (NVIDIA A10 card, 24 GB VRAM).
6. Under **Image**, select **Canonical Ubuntu 22.04**.
7. Under **Boot Volume**, specify at least **100 GB** to accommodate the OS, CUDA drivers, and the Qwen model (19 GB).
8. Add your SSH key and launch the instance.

### 2. Configure the Environment
Access the VM via SSH (`ssh ubuntu@IP_OF_GPU`) and install Docker and essential drivers (the default Ubuntu GPU image on Oracle usually comes with NVIDIA drivers pre-installed).
Upload the project (`AI-BIBLE.zip`) or clone the GitHub repository and extract the files.

### 3. Set the 32B Model
Open the `translate_bible.py` file and modify the model variable to utilize the 32 Billion Parameters version (which easily fits and flies on the A10's 24GB of VRAM):

```python
MODEL_NAME = "qwen2.5:32b"
```

### 4. Deploy and Translate
Execute the deployment process:

```bash
# Start infrastructure
docker compose up -d --build

# Pull the 19GB model
docker compose exec ollama ollama pull qwen2.5:32b
```

Start the translation under a protected session (`tmux`):
```bash
tmux
sudo docker exec -d -e PYTHONUNBUFFERED=1 bible-translator sh -c 'python -u translate_bible.py > translate.log 2>&1'
```
Monitor logs:
```bash
tail -f translate.log
```

### 5. Download Outputs and Terminate (CRITICAL)
Once the JSONs are completed under the `output/` folder:
1. Use `scp` (or WinSCP) on your local machine to download the generated files.
2. After making 100% sure that the translations are safely saved on your local PC, go to the Oracle Cloud dashboard.
3. Click **Terminate** on the GPU instance to **STOP the hourly charging**!

---

## 📌 Billing, Marketplace, and OCI Credit Notes

- OCI Credits: Oracle's promotional credits cover services and resources inside the OCI account (Compute, Block/Object Storage, etc.). They DO NOT pay for external API calls (e.g. OpenAI, Anthropic).
- Marketplace / OCI Generative AI: Oracle offers managed models inside OCI. These services will consume your credits.

## ⚙️ Recommended Strategies for Self-Host GPU

- Self-host on OCI GPU instance (full control, uses only OCI credits):
	- Host open-source models on `VM.GPU.*` and pay only for infrastructure with credits.
	- For models larger than VRAM, employ 4-bit quantization (`bitsandbytes`) and optimization frameworks (`vLLM`, `DeepSpeed`).

## 🧭 Models and Licensing Notes

- Direct translation: `NLLB` for supported languages; neural parallel translation models can be combined with LLMs for post-editing.
- LLMs for contextualization: `Llama-3`, `Mistral`, `Mixtral`, and `Qwen`.
- For Aramaic, Syriac, Coptic, Armenian, and Ge'ez, fine-tuning and parallel corpora will be necessary.

---

*Status: GPU Infrastructure successfully configured and 100% operational!*
