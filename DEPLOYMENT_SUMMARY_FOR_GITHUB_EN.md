# AI-BIBLE — Deploy & Test Summary (Oracle Cloud)

Executive summary of the deployment and GPU scaling status (Frankfurt).

**Purpose**
- Document the AI-BIBLE translation architecture active in the cloud and infrastructure status.

## 🚀 Infrastructure Status (05/18/2026)

*   **Active Instance**: `AI-BIBLE` in **Frankfurt (Germany Central)**.
*   **Shape**: `VM.GPU.A10.1` (15 OCPU cores, 240 GB RAM, 1x NVIDIA A10 with 24GB VRAM).
*   **Public IP**: `130.61.86.XX` (Obfuscated for security)
*   **OS**: Ubuntu 22.04 LTS.
*   **NVIDIA Drivers**: ✅ Installed and active (Driver 535.288.01, CUDA 12.2).
*   **Docker & Docker Compose**: ✅ Installed and configured with **NVIDIA Container Toolkit** for containerized GPU acceleration.

## 📂 What has been deployed and sent to the VM
- `deploy/oci/setup_vm_deps.sh` — automated script that configured all NVIDIA drivers, CUDA, Docker, and Container Toolkit on the clean VM in record time (~6 minutes).
- `docker-compose.yml` (updated) — configured to allow Ollama to utilize native GPU acceleration.
- Unzipped project in `~/AI-BIBLE` on the VM with all files ready.

## 🗺️ Expansion Roadmap (New Scope)
The project now integrates an even more ambitious philological and theological vision:
1.  **Full Sefaria Integration**: Download and translate the complete Sefaria portal database directly into Brazilian Portuguese.
2.  **Apocrypha and Pseudepigrapha**:
    - *Old Testament*: Enoch, Jubilees, Tobit, Judith, Wisdom, Sirach (Ecclesiasticus), Baruch, Maccabees.
    - *New Testament*: Gospel of Thomas, Epistle to the Hebrews, Epistle of Barnabas, Didache, Shepherd of Hermas.
3.  **Additional Ancient Languages**:
    - Portions and Targums in **Aramaic**.
    - Peshitta in **Syriac**.
    - Full Orthodox canon in **Ge'ez (Classical Ethiopic)**.
    - Classical manuscripts in **Ancient Armenian**.
4.  **Integrated Study Materials**:
    - Dictionaries/Lexicons (Strong's Greek/Hebrew, Brown-Driver-Biggs, Thayer).
    - Classic Bible commentaries (Matthew Henry, Albert Barnes, Pulpit Commentary).
    - Historical grammars (Gesenius, Robertson).

*Note: The downloads of these collections will be performed directly by the Frankfurt VM (24 Gbps network bandwidth), saving local bandwidth.*

## ⚙️ Container Quick Status
The inference and translation services are active in the background under the **Hybrid Translation Strategy**:
- **Single-Pass (Active by Default)**: High-speed translation (15-30s per chapter) running continuously in the background to minimize faturamento/API costs.
- **Double-Pass Post-Processor**: High-precision academic and theological critique executed on-demand via the script `review_existing_translations.py`, focusing strictly on highly complex books and collections (Septuagint, Aramaic, Talmud, Psalms, Isaiah etc.) after the main translations complete.

---
*Status: GPU Infrastructure successfully configured and 100% operational!*
