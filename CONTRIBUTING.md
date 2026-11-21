# Contributing

Thank you for helping improve the nanoporous drug delivery in silico
meta-analysis! This project curates verifiable, citable metrics from the
nanoporous/mesoporous drug-delivery literature (adapted from Ahmed et al. 2026,
CC BY 4.0).

## How to add a curated row

1. **Find the paper.** Use a real source (PubMed, bioRxiv, or the publisher's
   site). Record the title, authors, journal, year, DOI/PMID, and URL. Do not
   invent citations.

2. **Extract metrics from the source.** Only record values that appear verbatim
   in the abstract or full text:
   * particle size (nm)
   * encapsulation / drug-loading efficiency (%)
   * release (%)
   * release time (h)
   * material type, drug cargo, stimuli trigger, disease target

   Leave a cell blank if the metric is not reported — never guess or infer it.

3. **Edit `data/processed/nanoporous_curated.csv`.** Append one row with these
   columns in this order:

   `material_type,drug_cargo,encapsulation_efficiency_pct,particle_size_nm,
   release_pct,release_time_h,stimuli_trigger,disease_target,
   reference_in_review,notes`

   In the `notes` field, include the full bibliographic reference (authors,
   journal, year, DOI) so the row is independently verifiable.

4. **Run the analysis** to regenerate figures:

   ```
   py -3 -I notebooks/01_nanoporous_meta_analysis.py
   ```

5. **Commit** the updated CSV and any changed figures, and push to your branch.

## No-hallucination rule

Every curated row must be traceable to a real paper with a verifiable DOI or
PMID. Numeric values must come from the source text, not from memory or
estimation. If you cannot verify a number from the source, leave it blank and
note that full-text review is needed.

## License

All contributions are licensed under CC BY 4.0, consistent with the rest of the
repository and the source review (Ahmed et al. 2026, CC BY 4.0).

## Questions

Open an issue on GitHub or contact the repository owner.
