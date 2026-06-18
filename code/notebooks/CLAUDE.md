# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

This is the learning and experimentation workspace for a Bachelor's thesis titled **"Benchmarking Tabular Data Augmentation Techniques for Deep Clustering"**. The notebooks here are focused tutorials tailored to the thesis pipeline: load tabular data → preprocess numerical/categorical columns → hand off to a scikit-learn/PyTorch encoder → evaluate clustering with NMI and ARI.

## Files in this directory

| File | Purpose |
|------|---------|
| `pandas.ipynb` | Pandas tutorial — data loading, preprocessing, sklearn/PyTorch handoff |
| `numpy.ipynb` | NumPy tutorial — arrays, indexing, masking, reductions, stacking, RNG |
| `matplotlib.ipynb` | Matplotlib tutorial — scatter, line, hist, barh, subplots, savefig |
| `matplotlib_explained.md` | German-language deep-dive explanations for the matplotlib notebook |
| `pandas_cheatsheet.md` | One-page pandas reference card |
| `pandas_cheatsheet.pdf` | PDF version of the cheat sheet |
| `results.csv` | Sample experiment results table (dataset × augmentation × seed → NMI, ARI) |
| `results_digits.csv` / `.pdf` / `.png` | Results and plots for the digits dataset experiment |
| `a.py` | Scratch script (matplotlib exercise playground) |

## Running the notebooks

```bash
jupyter notebook pandas.ipynb
jupyter notebook numpy.ipynb
jupyter notebook matplotlib.ipynb
# or use jupyter lab for all three
```

Execute cells with **Shift + Enter**. None of the notebooks have external data dependencies — they use sklearn built-in datasets (`load_iris`) and small in-memory synthetic arrays/DataFrames.

## Notebook structures

### `pandas.ipynb`

1. **Setup** — imports (`numpy`, `pandas`)
2. **Loading data** — `pd.read_csv`, `load_iris(as_frame=True)`, `fetch_openml`
3. **Inspecting** — `shape`, `info()`, `describe()`, `isna().sum()`, `value_counts()`
4. **Selecting rows/columns** — bracket indexing, `iloc`, `loc`, boolean filtering
5. **Numerical vs categorical** — `select_dtypes` to separate column types for the `ColumnTransformer`
6. **Missing values** — `dropna()` and `fillna(mean/median)`
7. **Transformations** — rename, drop, add columns, cast types
8. **Feature/label split** — `df.drop(columns=["target"])` for `X`, `df["target"]` for `y`
9. **Sklearn/PyTorch handoff** — `ColumnTransformer` with `StandardScaler` + `OneHotEncoder`, then `.to_numpy()`
10. **Saving results** — `to_csv` / `read_csv` for experiment result tables (one row per `dataset × augmentation × seed`)
11. **End-to-end example** — full pipeline from raw DataFrame to preprocessed numpy array
12. **Quick reference card** — one-line cheat sheet of every method used

### `numpy.ipynb`

Uses two shared datasets: `X_small` (6 × 4, human-readable) and `X` (120 × 6, standardised, simulates post-`StandardScaler` data).

| § | Topic | Key operations |
|---|-------|---------------|
| 1 | Array creation | `np.array`, `np.zeros`, `np.arange`, `np.linspace`, `np.eye`, `np.full` |
| 2 | Indexing & slicing | `X[row, col]`, `X[row]`, `X[:, col]`, `X[2:5]`, negative indices |
| 3 | Boolean masking | `mask = labels == k`, `X[mask]`, in-place modification with masks |
| 4 | Reductions | `np.sum`, `np.mean`, `np.std`, `axis=0` (per column) vs `axis=1` (per row) |
| 5 | Stacking | `np.vstack`, `np.hstack`, `np.repeat`, `np.append` |
| 6 | Random number generation | `np.random.default_rng(seed)`, `rng.standard_normal`, `rng.multivariate_normal`, `rng.random` |
| ★ | Capstone | End-to-end: normalise `X`, mask a random 20 % of values, reconstruct labels |

### `matplotlib.ipynb`

Uses simulated embeddings (`X` 240 × 2), loss curves, feature distributions, and a `nmi`/`ari` results dict.

| § | Plot type | Where used in thesis |
|---|-----------|---------------------|
| 1 | Figure / Axes model | Foundation for every plot |
| 2 | `scatter` | Visualising 2D cluster embeddings (post-PCA) |
| 3 | `plot` (line) | Training loss curves |
| 4 | `hist` | Feature distributions (data exploration) |
| 5 | `barh` | NMI / ARI comparison across augmentation techniques |
| 6 | `subplots` | Multi-panel results figures |
| 7 | `savefig` | PDF export for inclusion in LaTeX |
| ★ | Capstone | Given results dict → `capstone_results.pdf` |

## Key pipeline pattern

The standard preprocessing block used throughout the thesis:

```python
X = df.drop(columns=["target"])
y = df["target"]

num_cols = X.select_dtypes(include="number").columns.tolist()
cat_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()

preprocess = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
])
X_prep = preprocess.fit_transform(X)   # numpy array, ready for the encoder
```

`y` is never passed to the preprocessor — it is used only for NMI/ARI evaluation after clustering.

## Results table format

`results.csv` stores one row per experiment run:

```
dataset, augmentation, seed, nmi, ari
iris,    masking,      0,    0.78, 0.74
```
