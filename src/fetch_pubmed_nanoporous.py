"""
src/fetch_pubmed_nanoporous.py

Search PubMed for nanoporous / mesoporous drug-delivery studies and save
metadata (PMID, title, journal, year, authors, abstract) to CSV.

Run (from repo root):
    py -I src/fetch_pubmed_nanoporous.py

Requires:
    pip install biopython

NCBI requires an email address. Set it in the script or via the
ENTREZ_EMAIL environment variable before running.
"""

import csv
import os
import sys
import time
from pathlib import Path

try:
    from Bio import Entrez
    from Bio import Medline
except ImportError:
    print("ERROR: Biopython is not installed.")
    print("Install it first:  pip install biopython")
    sys.exit(1)

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
# Set your email here (required by NCBI) or set the ENTREZ_EMAIL env var.
ENTREZ_EMAIL = os.environ.get("ENTREZ_EMAIL", "your.email@example.com")
Entrez.email = ENTREZ_EMAIL

# NCBI rate limit: max 3 requests per second without an API key.
# Sleep 0.4 s between calls to stay safely under the limit.
SLEEP_SECONDS = 0.4

# Output file
OUTPUT_CSV = Path("data/raw/pubmed_nanoporous.csv")

# PubMed search queries targeting nanoporous drug delivery.
# Each query is run separately so we can track which term retrieved which paper.
SEARCH_QUERIES = [
    "nanoporous nanoparticles drug delivery",
    "mesoporous silica nanoparticles drug delivery",
    "mesoporous nanoparticles cancer therapy",
    "metal-organic framework drug delivery",
    "porous polymer nanoparticles drug delivery",
    "nanoporous drug delivery pH responsive",
    "mesoporous silica doxorubicin",
]

# How many records to fetch per query (increase for a bigger dataset)
RETMAX_PER_QUERY = 50


def search_pubmed(term, retmax=RETMAX_PER_QUERY):
    """Return a list of PubMed IDs for the given search term."""
    handle = Entrez.esearch(db="pubmed", term=term, retmax=retmax, sort="relevance")
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]


def fetch_details(id_list):
    """Fetch Medline-formatted records for a list of PMIDs."""
    if not id_list:
        return []
    ids = ",".join(id_list)
    handle = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="text")
    records = list(Medline.parse(handle))
    handle.close()
    return records


def clean_text(value):
    """Normalize whitespace in a string."""
    if value is None:
        return ""
    return " ".join(str(value).split())


def main():
    if ENTREZ_EMAIL == "your.email@example.com":
        print("WARNING: You have not set ENTREZ_EMAIL. NCBI may block requests.")
        print('Set it with:  set ENTREZ_EMAIL=your.email@example.com   (Windows)')
        print('or edit ENTREZ_EMAIL in src/fetch_pubmed_nanoporous.py\n')

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    all_records = []
    seen_pmids = set()

    for query in SEARCH_QUERIES:
        print(f"\nSearching PubMed: {query}")
        try:
            id_list = search_pubmed(query)
            print(f"  Found {len(id_list)} PMIDs")
        except Exception as exc:
            print(f"  ERROR searching '{query}': {exc}")
            time.sleep(SLEEP_SECONDS)
            continue

        # Fetch in batches to avoid huge single requests
        batch_size = 20
        for i in range(0, len(id_list), batch_size):
            batch = id_list[i:i + batch_size]
            try:
                records = fetch_details(batch)
            except Exception as exc:
                print(f"  ERROR fetching batch: {exc}")
                time.sleep(SLEEP_SECONDS * 3)
                continue

            for rec in records:
                pmid = rec.get("PMID", "")
                if not pmid or pmid in seen_pmids:
                    continue
                seen_pmids.add(pmid)

                all_records.append(
                    {
                        "PMID": pmid,
                        "Title": clean_text(rec.get("TI", "")),
                        "Journal": clean_text(rec.get("JT", "")),
                        "Year": clean_text(rec.get("DP", ""))[:4],  # first 4 chars of date
                        "Authors": clean_text("; ".join(rec.get("AU", []))),
                        "SearchQuery": query,
                        "Abstract": clean_text(rec.get("AB", "")),
                    }
                )

            time.sleep(SLEEP_SECONDS)

        time.sleep(SLEEP_SECONDS)

    # Write CSV
    fieldnames = [
        "PMID",
        "Title",
        "Journal",
        "Year",
        "Authors",
        "SearchQuery",
        "Abstract",
    ]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_records)

    print(f"\nDone. Saved {len(all_records)} unique records to {OUTPUT_CSV}")
    print("Next step: manually screen titles/abstracts and move relevant ones to")
    print("data/processed/nanoporous_curated.csv or a new analysis file.")


if __name__ == "__main__":
    main()
