# Nanoporous Nanoparticles for Drug Delivery — In Silico Meta-Analysis

Curated dataset and exploratory analysis of nanoporous / mesoporous polymeric and inorganic nanoparticles for drug delivery, derived from a systematic read of Ahmed et al. (2026).

## Attribution

This project is adapted from:

> Ahmed S., Mujahid M.H., Kour M., Fatima S., Ahamad S., Mishra S.K.,
> Bhat A.R., Abu-Rayyan A., Tebeje B.A. "Molecular design and therapeutic
> applications of polymeric nanoparticles for drug delivery: A comprehensive
> review." *Results in Chemistry* 28 (2026) 103459.
> https://doi.org/10.1016/j.rechem.2026.103459 — CC BY 4.0.

All extracted text, tables, and ideas originate from the above review under CC BY 4.0. The curated dataset, code, and new analysis in this repository are additionally licensed under CC BY 4.0.

## Repository structure

```
data/raw/           # First-pass keyword extraction (provenance — do not edit)
data/processed/     # Manually curated dataset for analysis
notebooks/          # Analysis scripts / Jupyter notebooks
src/                # Extraction utilities
results/figures/    # Generated plots
docs/               # Data dictionary and attribution notes
```

## How to run

```bash
# 1. Extract candidates from the review text
python -I src/extract_nanoporous.py C:\path\to\paper.txt data/raw/nanoporous_candidates.csv

# 2. Manually curate: data/raw/*.csv -> data/processed/nanoporous_curated.csv

# 3. Run analysis
python -I notebooks/01_nanoporous_meta_analysis.py
```

## License

CC BY 4.0
