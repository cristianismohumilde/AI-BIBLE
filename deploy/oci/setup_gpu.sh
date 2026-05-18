#!/usr/bin/env bash
set -euo pipefail

echo "Setting up Python venv and installing requirements..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
if [ -f requirements.txt ]; then
  pip install -r requirements.txt || true
fi
pip install --no-cache-dir vllm bitsandbytes flexgen || true

echo "Setup complete. Activate the virtualenv with: source .venv/bin/activate"
echo "Run the translator (example): . .venv/bin/activate && python translate_bible.py"
