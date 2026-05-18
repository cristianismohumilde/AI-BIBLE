#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <hf-repo-id> <output-dir>"
  exit 1
fi

MODEL=$1
OUTDIR=$2

mkdir -p "$OUTDIR"
python download_and_quantize.py --model "$MODEL" --out "$OUTDIR"

echo "Now ssh into the GPU instance, place the downloaded cache into /models/<name> and run the recommended Python conversion command there (see printed hint)."
