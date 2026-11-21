"""
src/extract_nanoporous.py

First-pass keyword extraction from Ahmed et al. (2026) review text.
Scans the extracted PDF text for nanoporous / mesoporous / porous drug
delivery mentions and captures nearby % and nm values.

Run (from repo root):
    python -I src/extract_nanoporous.py C:\path\to\paper.txt data/raw/nanoporous_candidates.csv

Requires: Python 3 only (no external dependencies).
"""

import sys
import csv
import re
from pathlib import Path

KEYWORDS = [
    "nanoporous",
    "mesoporous",
    "porous",
    "pore",
    "pores",
    "silica",
    "mesoporous silica",
    "metal-organic",
    "MOF",
    "covalent organic",
    "COF",
    "zeolite",
    "porous polymer",
]

PCT = re.compile(r"(\d+(?:\.\d+)?)\s*%")
NM = re.compile(r"(\d+(?:\.\d+)?)\s*nm", re.IGNORECASE)


def find_matches(text, keyword, window=250):
    hits = []
    for m in re.finditer(re.escape(keyword), text, flags=re.IGNORECASE):
        start = max(0, m.start() - window)
        end = min(len(text), m.end() + window)
        snippet = text[start:end].replace("\n", " ").strip()
        hits.append(snippet)
    return hits


def extract_metrics(snippet):
    pcts = PCT.findall(snippet)
    nms = NM.findall(snippet)
    return pcts, nms


def main():
    if len(sys.argv) < 3:
        print("Usage: python -I extract_nanoporous.py <input_txt> <output_csv>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8", errors="replace")

    rows = []
    for kw in KEYWORDS:
        for snippet in find_matches(text, kw):
            pcts, nms = extract_metrics(snippet)
            rows.append(
                {
                    "keyword": kw,
                    "context": snippet,
                    "percent_values": "; ".join(pcts),
                    "nm_values": "; ".join(nms),
                    "needs_manual_check": "TRUE",
                    "source_file": input_path.name,
                    "notes": "",
                }
            )

    fieldnames = [
        "keyword",
        "context",
        "percent_values",
        "nm_values",
        "needs_manual_check",
        "source_file",
        "notes",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Extracted {len(rows)} candidate snippets -> {output_path}")
    print("Review data/raw/nanoporous_candidates.csv and curate rows into data/processed/.")


if __name__ == "__main__":
    main()
