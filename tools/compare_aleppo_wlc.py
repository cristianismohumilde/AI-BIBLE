import os
import json
from pathlib import Path

BASE = Path("data")
ALEPPO = BASE / "Aleppo"
WLC = BASE / "WLC"
REPORTS = Path("reports")
REPORTS.mkdir(exist_ok=True)

def load_json(p):
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def normalize(s):
    if not s:
        return ""
    return " ".join(s.split()).strip()

summary = []
diffs = []

for book_dir in sorted(ALEPPO.iterdir() if ALEPPO.exists() else []):
    if not book_dir.is_dir():
        continue
    book = book_dir.name
    aleppo_files = sorted(book_dir.glob("*.json"))
    for af in aleppo_files:
        ch = af.stem
        wpath = WLC / book / f"{ch}.json"
        ajson = load_json(af)
        wjson = load_json(wpath) if wpath.exists() else None

        if wjson is None:
            summary.append((book, ch, "WLC missing"))
            continue

        # prefer Hebrew 'he' array if present, else 'text'
        a_he = ajson.get("he") if isinstance(ajson, dict) else None
        w_he = wjson.get("he") if isinstance(wjson, dict) else None

        a_list = a_he if a_he else ajson.get("text", [])
        w_list = w_he if w_he else (wjson if isinstance(wjson, list) else wjson.get("text", []))

        la = len(a_list)
        lw = len(w_list)
        if la != lw:
            summary.append((book, ch, f"count_diff Aleppo={la} WLC={lw}"))

        # collect up to 5 verse diffs per chapter
        per_ch_diffs = []
        for i in range(max(la, lw)):
            a_verse = normalize(a_list[i]) if i < la else "(missing)"
            w_verse = normalize(w_list[i].get("text", "")) if i < lw and isinstance(w_list[i], dict) else normalize(w_list[i]) if i < lw else "(missing)"
            if a_verse != w_verse:
                per_ch_diffs.append((i+1, a_verse[:200], w_verse[:200]))
            if len(per_ch_diffs) >= 5:
                break
        if per_ch_diffs:
            diffs.append((book, ch, per_ch_diffs))

        # minor progress marker
        if len(summary) % 100 == 0:
            print(f"Processed {len(summary)} differences...")

# Write report
rep = REPORTS / "aleppo_wlc_comparison.md"
with open(rep, "w", encoding="utf-8") as f:
    f.write("# Aleppo vs WLC comparison report\n\n")
    f.write(f"Generated: now\n\n")
    f.write("## Summary (chapters with issues)\n\n")
    if not summary:
        f.write("No missing chapters or count differences found.\n\n")
    else:
        for s in summary:
            f.write(f"- {s[0]} {s[1]}: {s[2]}\n")
    f.write("\n## Detailed diffs (up to 5 verse diffs per chapter)\n\n")
    if not diffs:
        f.write("No verse-level diffs found.\n")
    else:
        for book, ch, items in diffs:
            f.write(f"### {book} {ch}\n\n")
            for vnum, a_sn, w_sn in items:
                f.write(f"- Verse {vnum}:\n")
                f.write(f"  - Aleppo: {a_sn}\n")
                f.write(f"  - WLC: {w_sn}\n")
            f.write("\n")

print(f"Report written to {rep}")
