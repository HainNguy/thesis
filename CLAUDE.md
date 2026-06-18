# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this workspace is

Research workspace for the bachelor's thesis **"Benchmarking Tabular Data Augmentation Techniques for Deep Clustering"** (LMU Munich, 16 Jun – 25 Aug 2026). This is not a software project — there are no build or test commands at the root level. The work is split across literature, code experiments, and a LaTeX thesis document.

## Directory layout

| Path | Contents |
|------|----------|
| `code/notebooks/` | Learning notebooks (numpy, pandas, matplotlib, sklearn) and experiment scripts. Has its own `CLAUDE.md` with full details. |
| `literature-notes/` | One `.md` file per paper (e.g. `scarf.md`). 5-section structure: Problem · Corruption mechanism · Loss · Key results · Relevance to thesis. |
| `bib-refs.bib` | BibTeX bibliography. **Managed automatically by Zotero + Better BibTeX — do not edit manually.** Add papers via Zotero by arXiv ID; the file auto-syncs. |
| `plan/` | Thesis timeline PDF and tracker. The authoritative weekly plan is `Thesis_Timeline_10_Weeks_EN_updated.pdf`. |
| `Literatur/` | PDF copies of all papers. |

## Bibliography

`bib-refs.bib` is auto-exported by the Better BibTeX (BBT) Zotero plugin. Cite key format: `auth.lower + shorttitle.lower + year` (e.g. `bahriscarfselfsupervised2022`). To add a new source: paste the arXiv ID into Zotero's "Add by Identifier" → the `.bib` file updates automatically.

In LaTeX, the project uses `biblatex` + `biber` with `bibstyle=alphabetic`. Citation commands: `\parencite{key}` (parenthetical) and `\textcite{key}` (inline).

## LaTeX build

The thesis LaTeX project uses `latexmk`. From the thesis project root:

```bash
latexmk -pdf main.tex       # full build (runs biber automatically)
latexmk -pdf -pvc main.tex  # continuous preview mode
```

Manual build order if needed: `pdflatex → biber main → pdflatex → pdflatex`.

## Core experiment pipeline

The central data flow that all code in this thesis follows:

```python
# 1. Load & split
X = df.drop(columns=["target"])
y = df["target"]

# 2. Preprocess (numerical + categorical)
num_cols = X.select_dtypes(include="number").columns.tolist()
cat_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()
preprocess = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
])
X_prep = preprocess.fit_transform(X)   # numpy array → encoder input

# 3. Augment → encode → cluster → evaluate
# augmentation(X_prep) → MLP encoder → embeddings → KMeans → NMI/ARI
```

`y` is never passed to the encoder or augmentation — it is used only for NMI/ARI evaluation after clustering.

## Results format

Experiment results are stored as CSV with one row per run:

```
dataset, augmentation, seed, nmi, ari
iris,    masking,      0,    0.78, 0.74
```

## Thesis methodology (key design decisions)

- **Augmentation techniques benchmarked:** SCARF-style marginal sampling, Gaussian noise, feature swapping, identity (no-augmentation baseline)
- **Feature-type-aware augmentation:** categorical features → marginal-distribution replacement only; numerical → Gaussian noise or scaling. This is labelled "Type-Aware" in result tables.
- **Encoder:** fixed MLP backbone across all augmentation conditions
- **Clustering:** k-means on embeddings; evaluated by NMI and ARI
- **Datasets:** 3–4 OpenML/UCI tabular datasets with ground-truth labels, stratified by fraction of categorical features
- **No-augmentation baseline:** each row passed twice unchanged (identity augmentation) — the theoretical upper bound for semantic preservation; labelled "Identity" in all result tables
