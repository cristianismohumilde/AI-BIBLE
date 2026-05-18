#!/usr/bin/env python3
"""Download a Hugging Face model and prepare a 4-bit quantized copy using bitsandbytes.

Usage: python download_and_quantize.py --model <repo_id> --out /models/<name>
"""
import argparse
import os
from huggingface_hub import snapshot_download

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help='Hugging Face repo id, e.g. "meta-llama/Llama-2-13b"')
    parser.add_argument('--out', required=True, help='Output directory to save the model files')
    args = parser.parse_args()

    print(f'Downloading {args.model}...')
    repo_dir = snapshot_download(repo_id=args.model, allow_patterns=['*'])
    print('Downloaded to', repo_dir)

    # Note: actual 4-bit conversion uses transformers + bitsandbytes during load.
    # We provide a standard pattern below; run on the GPU instance where bitsandbytes is available.
    convert_hint = f"Use the following command on the GPU instance to load the model in 4-bit and save a quantized copy:\n\n"
    convert_hint += (
        f"python -c \"from transformers import AutoModelForCausalLM, AutoTokenizer; "
        f"from transformers import BitsAndBytesConfig; "
        f"bb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype='float16'); "
        f"tok=AutoTokenizer.from_pretrained('{args.model}', use_fast=False); "
        f"m=AutoModelForCausalLM.from_pretrained('{args.model}', quantization_config=bb, device_map='auto'); "
        f"m.save_pretrained('{args.out}'); tok.save_pretrained('{args.out}')\""
    )

    print(convert_hint)
    print('Files are ready in the local cache; move or copy them to the target /models directory on the GPU instance and run the conversion there.')

if __name__ == '__main__':
    main()
