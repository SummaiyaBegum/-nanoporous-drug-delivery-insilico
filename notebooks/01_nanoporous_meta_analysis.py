"""
notebooks/01_nanoporous_meta_analysis.py

Exploratory analysis of the curated nanoporous dataset.

Run (from repo root):
    python -I notebooks/01_nanoporous_meta_analysis.py
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

DATA_PATH = Path("data/processed/nanoporous_curated.csv")
FIG_DIR = Path("results/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    if not DATA_PATH.exists():
        print(f"Curated data not found: {DATA_PATH}")
        print("Create data/processed/nanoporous_curated.csv first (see README).")
        return None
    return pd.read_csv(DATA_PATH)


def plot_size_distribution(df):
    if "particle_size_nm" not in df.columns:
        return
    sizes = pd.to_numeric(df["particle_size_nm"], errors="coerce").dropna()
    if sizes.empty:
        return
    plt.figure(figsize=(6, 4))
    plt.hist(sizes, bins=15, edgecolor="black", color="#4c78a8")
    plt.xlabel("Particle size (nm)")
    plt.ylabel("Count")
    plt.title("Nanoporous nanoparticle sizes from curated review data")
    plt.tight_layout()
    out = FIG_DIR / "size_distribution.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Saved {out}")


def plot_material_counts(df):
    if "material_type" not in df.columns:
        return
    counts = df["material_type"].value_counts().head(10)
    if counts.empty:
        return
    plt.figure(figsize=(6, 4))
    counts.plot(kind="bar", color="#4c78a8", edgecolor="black")
    plt.xlabel("Material type")
    plt.ylabel("Count")
    plt.title("Top nanoporous material types in curated dataset")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    out = FIG_DIR / "material_counts.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Saved {out}")


def main():
    df = load_data()
    if df is None:
        return
    print(df.head())
    print("\nColumn summary:")
    print(df.info())
    print("\nMaterial type counts:")
    print(df["material_type"].value_counts() if "material_type" in df.columns else "N/A")

    plot_size_distribution(df)
    plot_material_counts(df)


if __name__ == "__main__":
    main()
