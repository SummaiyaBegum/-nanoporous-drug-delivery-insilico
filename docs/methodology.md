# Methodology — Extraction → Curation → Analysis Pipeline

This document describes how the curated nanoporous-drug-delivery dataset was built,
from literature extraction through curation to exploratory analysis.

## 1. Literature extraction

Source review (adapted under CC BY 4.0):

> Ahmed S., Mujahid M.H., Kour M., Fatima S., Ahamad S., Mishra S.K.,
> Bhat A.R., Abu-Rayyan A., Tebeje B.A. "Molecular design and therapeutic
> applications of polymeric nanoparticles for drug delivery: A comprehensive
> review." *Results in Chemistry* 28 (2026) 103459.
> https://doi.org/10.1016/j.rechem.2026.103459

First-pass candidate extraction is performed from `paper.txt` (the PDF-extracted
review text) using `src/extract_nanoporous.py`. The extractor:

* Falls back through `utf-8` → `cp1252` → `latin-1` encoding for legacy
  Windows-extracted PDF text.
* Splits two-column interleaved text into windows and de-duplicates overlapping
  spans (character-overlap threshold) so the same sentence from both columns
  isn't counted twice.
* Extracts nanometre-range particle sizes via `(\d+(?:\.\d+)?(?:\s*-\s*\d+(?:\.\d+)?)?)\s*nm`.
* Extracts encapsulation / drug-loading percentages.
* Outputs `data/raw/nanoporous_candidates.csv` (ignored by git — raw, uncurated).

Additional recent literature was retrieved locally (no hallucinated citations)
using the ClawBio Lit Synthesizer against PubMed E-utilities and bioRxiv
(query: `nanoporous nanoparticles drug delivery`, date 2026-11-21). Every paper
cited in the curated dataset carries a verifiable PMID and/or DOI.

## 2. Curation

Raw candidates are hand-curated into `data/processed/nanoporous_curated.csv`
(tracked by git). Each row contains:

| Column | Description |
|--------|-------------|
| material_type | Class of nanoporous material |
| drug_cargo | Therapeutic agent loaded |
| encapsulation_efficiency_pct | Reported drug-loading efficiency (%) |
| particle_size_nm | Reported diameter (nm) |
| release_pct | Drug released under stated conditions |
| release_time_h | Timepoint for release measurement |
| stimuli_trigger | Release trigger (pH, temperature, light, enzyme, redox, NIR) |
| disease_target | Cancer or disease context |
| reference_in_review | Bracketed citation number from review, or [PMID NNNNNNNN] |
| notes | Manual curation notes including the full bibliographic reference |

**No-hallucination rule**: numeric metrics (size, EE%, release%) are only recorded
when they appear verbatim in the source abstract/full text. Blank cells mean the
metric was not reported in the abstract and full-text review is pending. Values
are never inferred or rounded from unrelated figures.

Each row's `notes` field records the full citation (authors, journal, year, DOI)
so every entry is independently verifiable.

## 3. Analysis

Exploratory analysis is run with:

```
py -3 -I notebooks/01_nanoporous_meta_analysis.py
```

It reads `data/processed/nanoporous_curated.csv` and writes:

* `results/figures/size_distribution.png` — histogram of particle sizes (only
  generated when at least one numeric size is present).
* `results/figures/material_counts.png` — bar chart of material type counts.

Figures are tracked by git so they appear on GitHub. The analysis requires
`pandas>=2.0` and `matplotlib>=3.5` (see `requirements.txt`).

## 4. Continuous integration

`.github/workflows/analysis.yml` re-runs the analysis on every push/PR to
`main` and `init/nanoporous-meta-analysis`, installs `requirements.txt`,
verifies the curated dataset exists, and commits any regenerated figures.

## 5. Reproducibility

All code and data in this repository are CC BY 4.0, adapted from Ahmed et al.
(2026) under CC BY 4.0. To reproduce:

1. `py -3 -m pip install -r requirements.txt`
2. `py -3 -I src/extract_nanoporous.py C:\path\to\paper.txt data/raw/nanoporous_candidates.csv`
3. Hand-curate candidates into `data/processed/nanoporous_curated.csv`
4. `py -3 -I notebooks/01_nanoporous_meta_analysis.py`
