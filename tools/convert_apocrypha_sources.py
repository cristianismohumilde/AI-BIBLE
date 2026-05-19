#!/usr/bin/env python3
"""Convert downloaded apocrypha source JSON files into chapter-based verse JSON.

This script keeps the conversion automated and consistent with the project's
existing chapter-per-file layout.
"""

from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "data" / "apocrypha"
OUTPUT_DIR = SOURCE_DIR / "structured"


TARGETS = [
    ("prayer_of_manasseh.json", "Prayer_of_Manasseh", 1),
    ("psalm_151.json", "Psalm_151", 1),
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def build_verse_list(source_data):
    english = ensure_list(source_data.get("text"))
    hebrew = ensure_list(source_data.get("he"))

    verse_count = max(len(english), len(hebrew))
    verses = []
    for index in range(verse_count):
        text = None
        if index < len(hebrew) and hebrew[index]:
            text = hebrew[index]
        elif index < len(english) and english[index]:
            text = english[index]

        if text:
            verses.append({
                "verse": index + 1,
                "text": text,
            })

    return verses


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest = []
    for source_name, book_name, chapter_number in TARGETS:
        source_path = SOURCE_DIR / source_name
        if not source_path.exists():
            print(f"Skipping missing source: {source_path}")
            continue

        source_data = load_json(source_path)
        verses = build_verse_list(source_data)

        target_dir = OUTPUT_DIR / book_name
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / f"{chapter_number}.json"

        with target_path.open("w", encoding="utf-8") as handle:
            json.dump(verses, handle, ensure_ascii=False, indent=2)

        manifest.append({
            "source": source_name,
            "book": book_name,
            "chapter": chapter_number,
            "verse_count": len(verses),
            "output": str(target_path.relative_to(BASE_DIR)).replace("\\", "/"),
        })
        print(f"Wrote {target_path}")

    manifest_path = OUTPUT_DIR / "manifest.json"
    with manifest_path.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)

    print(f"Manifest written to {manifest_path}")


if __name__ == "__main__":
    main()