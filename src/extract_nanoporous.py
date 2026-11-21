r"""
src/extract_nanoporous.py

First-pass keyword extraction from Ahmed et al. (2026) review text.
Scans the extracted PDF text for nanoporous / mesoporous / porous drug
delivery mentions and captures nearby %, nm values, size ranges, and
encapsulation / drug-loading percentages.

Run (from repo root):
    python -I src/extract_nanoporous.py C:\path\to\paper.txt data/raw/nanoporous_candidates.csv

Requires: Python 3 only (no external dependencies).

Notes
-----
PDF-extracted text on Windows is often legacy single-byte encoded (e.g.
Windows-1252) rather than UTF-8. This script tries UTF-8 first and falls
back to cp1252 / latin-1 so accented characters and special symbols are
decoded instead of replaced with U+FFFD.

Two-column review text interleaves left/right columns, so snippets can look
scrambled. Near-duplicate snippets (same window matching several keywords)
are collapsed so each distinct mention is reported once.
"""

import sys
import csv
import re
from pathlib import Path

KEYWORDS = [
    "nanoporous",
    "mesoporous",
    "mesoporous silica",
    "porous",
    "pore",
    "pores",
    "silica",
    "metal-organic",
    "MOF",
    "covalent organic",
    "COF",
    "zeolite",
    "porous polymer",
    "encapsulation",
    "drug loading",
]

# Percentages: 87, 93.2, 7.2
PCT = re.compile(r"(\d+(?:\.\d+)?)\s*%")
# Nanometre values and ranges: 100 nm, 10-50 nm, 2-50 nm, 190-450 nm
NM = re.compile(r"(\d+(?:\.\d+)?(?:\s*-\s*\d+(?:\.\d+)?)?)\s*nm", re.IGNORECASE)
# Encapsulation / drug-loading efficiency phrases
EE = re.compile(
    r"(?:encapsulation(?:\s+efficiency)?|drug\s+loading)\s*(?:of)?\s*"
    r"\(?(\d+(?:\.\d+)?)\s*%\)?",
    re.IGNORECASE,
)

CANDIDATE_ENCODINGS = ["utf-8", "utf-8-sig", "cp1252", "latin-1"]


def read_text(path):
    """Read a file, trying UTF-8 first then common legacy Windows encodings."""
    raw = path.read_bytes()
    last_err = None
    for enc in CANDIDATE_ENCODINGS:
        try:
            return raw.decode(enc)
        except UnicodeDecodeError as exc:
            last_err = exc
    # Last resort: best-effort with replacement characters
    return raw.decode("utf-8", errors="replace")


def normalize_whitespace(snippet):
    return re.sub(r"\s+", " ", snippet).strip()


def find_matches(text, keyword, window=260):
    hits = []
    for m in re.finditer(re.escape(keyword), text, flags=re.IGNORECASE):
        start = max(0, m.start() - window)
        end = min(len(text), m.end() + window)
        snippet = normalize_whitespace(text[start:end])
        hits.append(snippet)
    return hits


def extract_metrics(snippet):
    pcts = PCT.findall(snippet)
    nms = NM.findall(snippet)
    ees = EE.findall(snippet)
    return pcts, nms, ees


def is_near_duplicate(a, b, threshold=0.85):
    """Crude character-overlap dedup for two-column-interleaved text."""
    if not a or not b:
        return False
    set_a = set(a)
    set_b = set(b)
    if not set_a or not set_b:
        return False
    overlap = len(set_a & set_b)
    return overlap / max(len(set_a), len(set_b)) >= threshold


def main():
    if len(sys.argv) < 3:
        print("Usage: python -I extract_nanoporous.py <input_txt> <output_csv>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        sys.exit(1)

    text = read_text(input_path)

    rows = []
    seen_snippets = []
    for kw in KEYWORDS:
        for snippet in find_matches(text, kw):
            # Collapse near-duplicate windows caused by overlapping keywords
            if any(is_near_duplicate(snippet, old) for old in seen_snippets):
                continue
            seen_snippets.append(snippet)

            pcts, nms, ees = extract_metrics(snippet)
            rows.append(
                {
                    "keyword": kw,
                    "context": snippet,
                    "percent_values": "; ".join(pcts),
                    "nm_values": "; ".join(nms),
                    "encapsulation_loading_pct": "; ".join(ees),
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
        "encapsulation_loading_pct",
        "needs_manual_check",
        "source_file",
        "notes",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Extracted {len(rows)} candidate snippets -> {output_path}")
    print("Review data/raw/nanoporous_candidates.csv and curate rows into data/processed/.")


if __name__ == "__main__":
    main()
