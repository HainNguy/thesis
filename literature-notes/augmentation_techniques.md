# Augmentation Technique Selection — Literature-Grounded Justification

**Week 2 deliverable (22–29 Jun 2026) · Phase A, Milestone M2**  
Feeds directly into the Week 3 augmentation module and the supervisor meeting (M2).

> **BibTeX note**: Only `bahriSCARFSelfSupervisedContrastive2022` is currently in `bib-refs.bib`. Add VIME and SubTab via Zotero → "Add by Identifier" with their arXiv IDs before writing the Related Work chapter.
> - VIME: arXiv 2003.08009 (Yoon et al., NeurIPS 2020)
> - SubTab: arXiv 2110.04361 (Ucar et al., NeurIPS 2021)

---

## 1 Summary — Final Technique Selection

Five conditions are benchmarked. Exactly one (TypeAware) is the thesis's novel contribution; the other four situate the thesis in the existing literature.

| Label | Mechanism (short) | Num features | Cat features | Source |
|-------|-------------------|-------------|-------------|--------|
| **Identity** | Row passed twice unchanged | unchanged | unchanged | thesis addition |
| **SCARF** | Replace random p % of features with marginal draws | marginal draw | marginal draw | \parencite{bahriSCARFSelfSupervisedContrastive2022} |
| **GaussNoise** | Add N(0, σ²) per numerical feature | +Gaussian noise | unchanged | classical; used as baseline in VIME \parencite{yoonVIMEExtending2020} |
| **FeatureSwap** | Replace random p % of features with same feature's value from another row | row-swapped | row-swapped | variant of VIME corruption \parencite{yoonVIMEExtending2020} |
| **TypeAware** | Marginal draws for categorical; Gaussian noise for numerical | +Gaussian noise | marginal draw | thesis contribution |

Corruption rate for all stochastic techniques: **p = 0.3** (30 % of features corrupted per view).  
Gaussian noise scale: **σ = 0.1 × per-feature standard deviation** (computed on the training split).

---

## 2 Technique Details

### 2.1 Identity (baseline)

**Mechanism**

```
x̃ = x      # both views are the same row, unchanged
```

The encoder receives `(x, x)` as the positive pair. No corruption is applied.

**Feature-type handling**: N/A — nothing is modified.

**Semantic-validity**: Perfect. This is the theoretical upper bound for semantic preservation: both views are provably the same entity. Any augmentation that outperforms Identity has learned invariances beyond exact repetition; any augmentation that underperforms Identity has damaged cluster-relevant structure.

**Why it belongs**: Every deep clustering benchmark needs a no-augmentation baseline to establish whether contrastive pretraining with a given corruption actually helps or hurts relative to the null case. Without it, you cannot distinguish "augmentation improves over nothing" from "augmentation merely recovers what corruption damaged." \parencite{bahriSCARFSelfSupervisedContrastive2022} does not include this baseline; its absence is a gap this thesis fills.

**Result table label**: Identity  
**Hyperparameters**: none

---

### 2.2 SCARF — Marginal Replacement

**Source**: \parencite{bahriSCARFSelfSupervisedContrastive2022}

**Mechanism**

```
for each feature j in 1..d:
    if Uniform(0,1) < p:
        x̃[j] = sample from empirical marginal distribution of feature j
    else:
        x̃[j] = x[j]
```

Corrupted features are replaced by independent draws from the feature's empirical marginal distribution (computed over the training set). On average, floor(p × d) features are replaced per view.

**Feature-type handling**:
- Numerical: the marginal draw is a real value from the training distribution of that feature.
- Categorical: the marginal draw is a category label sampled proportionally to its frequency in the training set. This is semantically conservative — the corrupted value is at least a valid category, just drawn from the wrong row.

**Semantic-validity**: Partial. SCARF treats all features identically regardless of semantic type. For numerical features, a marginal draw from (e.g.) `age` produces a plausible age. For categorical features like `marital-status`, a marginal draw produces a valid marital status — but it may not belong to the same person. The positive-pair assumption is weakened for features that carry irreducible semantic identity (the thesis's central concern).

**Why it belongs**: SCARF is the central methodological reference for the thesis. It defines the contrastive pretraining paradigm on tabular data and is the technique all others are measured against.

**Result table label**: SCARF  
**Hyperparameters**: corruption rate p = 0.3

---

### 2.3 GaussNoise — Gaussian Noise

**Source**: Classical data augmentation; used as a comparison baseline in \parencite{yoonVIMEExtending2020} (Table 2).

**Mechanism**

```
for each numerical feature j:
    x̃[j] = x[j] + ε,   ε ~ N(0, σ_j²)
for each categorical feature j:
    x̃[j] = x[j]        # left unchanged
```

where σ_j = 0.1 × std(feature j, training set).

**Feature-type handling**:
- Numerical: perturbed by additive Gaussian noise scaled to 10 % of the feature's standard deviation.
- Categorical: left completely unchanged. GaussNoise cannot meaningfully perturb a categorical feature without changing its type.

**Semantic-validity**: High for numerical features (a small perturbation to `age` or `credit_amount` preserves the entity's identity). Perfect for categorical features (they are not touched). This technique is the most semantically conservative of the corrupting methods.

**Why it belongs**: GaussNoise represents the "classical" view of data augmentation applied naively to tabular data — only numerical features are touched, categoricals are ignored. It serves as the lower bound of the spectrum between TypeAware (semantically principled) and SCARF (feature-agnostic marginal replacement). The gap between GaussNoise and TypeAware on high-categorical datasets isolates the contribution of categorical-aware augmentation.

**Result table label**: GaussNoise  
**Hyperparameters**: noise scale σ = 0.1 × per-feature std (training set)

---

### 2.4 FeatureSwap — Row-Level Feature Substitution

**Source**: Variant of the corruption mechanism in \parencite{yoonVIMEExtending2020}. VIME uses x_bar drawn from the marginal; FeatureSwap draws the replacement from a specific randomly chosen other row. The distinction: marginal sampling may produce combinations never seen in the data; row-swapping always produces a real row's value, but in the wrong context.

**Mechanism**

```
for each sample x in the batch:
    pick a random other row x' from the dataset (x' ≠ x)
    for each feature j in 1..d:
        if Uniform(0,1) < p:
            x̃[j] = x'[j]   # take feature j's value from x'
        else:
            x̃[j] = x[j]
```

**Feature-type handling**:
- Numerical: replaced with the same numerical feature's value from another row — always a valid number, but from a different data point.
- Categorical: replaced with the same categorical feature's value from another row — always a valid category, but from a different entity.

**Semantic-validity**: Low to medium. The corrupted view mixes features from two different entities. For categorical features, this is as semantically disruptive as SCARF (a different entity's `marital-status` is placed in the current row). For high-categorical datasets, FeatureSwap is expected to perform similarly to SCARF — both destroy inter-feature correlations — but FeatureSwap may preserve marginal statistics better because values always come from real rows.

**Why it belongs**: FeatureSwap is a distinct corruption family from marginal replacement (SCARF) — the source of the replacement is a specific row rather than the marginal distribution. This matters: on datasets where the marginal distribution is heavily skewed (e.g., `capital-gain` in Adult is zero for most rows), SCARF collapses many replacements to zero, whereas FeatureSwap picks any row's actual value. Including both allows the thesis to distinguish whether the source of the corruption (marginal vs. row-level) affects clustering quality.

**Result table label**: FeatureSwap  
**Hyperparameters**: corruption rate p = 0.3

---

### 2.5 TypeAware — Feature-Type-Aware Augmentation (thesis contribution)

**Source**: Thesis contribution. Combines GaussNoise (for numerical) and SCARF-style marginal replacement (for categorical) based on a pre-computed feature-type mask.

**Mechanism**

```
# build once on the training set:
num_mask = [True if feature j is numerical else False for j in 1..d]
cat_mask = [not m for m in num_mask]
marginal_distributions = {j: training_values[j] for j in cat_features}
feature_stds = {j: std(training_values[j]) for j in num_features}

# at augmentation time:
for each numerical feature j:
    x̃[j] = x[j] + ε,   ε ~ N(0, (0.1 × σ_j)²)
for each categorical feature j:
    x̃[j] = sample from marginal_distributions[j]
```

Every feature is corrupted — numerical features by calibrated Gaussian noise, categorical features by marginal replacement — but never in a semantically incoherent way (no Gaussian noise on a category, no arbitrary corruption of a numerical value).

**Feature-type handling**:
- Numerical: same as GaussNoise — additive N(0, σ²) noise.
- Categorical: same as SCARF — marginal replacement. The replacement is a valid category value.

**Semantic-validity**: This is the most semantically principled of the corrupting methods. Numerical perturbation preserves entity identity (a small noise on `age` still describes the same person). Categorical marginal replacement produces a plausible but potentially wrong value — the weakest violation the thesis permits.

**Why it belongs**: TypeAware is the thesis's central methodological claim: that feature-type-aware augmentation preserves more cluster-relevant structure than type-agnostic methods, particularly on high-categorical datasets. The comparison TypeAware vs. SCARF vs. FeatureSwap on datasets with different categorical fractions (Iris 0 %, German Credit 65 %, Car 100 %, Adult 57 %) is the core experimental finding.

**Result table label**: TypeAware  
**Hyperparameters**: corruption rate p = 0.3 (for categorical); σ = 0.1 × feature std (for numerical)

---

## 3 Rejected Candidates

| Candidate | Rejection reason |
|-----------|-----------------|
| **VIME full** (Bernoulli mask + marginal draw) | Mechanistically equivalent to SCARF; including both would duplicate the experimental signal without adding a new comparison axis. SCARF subsumes it. |
| **SubTab** (feature subsetting) | Creates views by hiding entire feature subsets (variable-width input), which is architecturally incompatible with the fixed MLP encoder backbone. Would require a different encoder per subset. |
| **Mixup** (λ·xᵢ + (1−λ)·xⱼ) | Linear interpolation is undefined for categorical features ("0.6 × married + 0.4 × single" has no semantic meaning). Requires special-casing that defeats the point of a clean comparative benchmark. |
| **Masking to zero / cutout** | Zero is a semantically meaningful value for most tabular features (age = 0, capital-gain = 0). Marginal replacement (SCARF) is strictly preferable and already included. |

---

## 4 Implementation Notes for Week 3

The Week 3 augmentation module (`augment.py` or equivalent) must implement a single class or function with the following interface:

```python
def augment(x: np.ndarray, technique: str, num_mask: np.ndarray,
            marginals: dict, stds: np.ndarray, p: float = 0.3) -> np.ndarray:
    """
    x         : (d,) preprocessed feature vector (post-StandardScaler/OneHotEncoder)
    technique : one of 'identity', 'scarf', 'gaussnoise', 'featureswap', 'typeaware'
    num_mask  : boolean array, True for numerical features
    marginals : {feature_idx: array of training values} for each feature
    stds      : per-feature standard deviation (training set)
    p         : corruption rate (used by scarf, featureswap, typeaware)
    returns   : corrupted view x̃ of same shape as x
    """
```

Key implementation decisions:
- **num_mask** is computed once from `X.select_dtypes(include='number')` (same logic as `dataset_selection.ipynb`).
- **marginals** are stored as the raw training column values; sampling uses `np.random.choice(marginals[j])`.
- **stds** are computed on the training split only (no data leakage from test/eval rows).
- **FeatureSwap** needs access to the full training set, not just the current row. Pass it as an additional argument or store it on a stateful augmenter object.
- For **TypeAware**, numerical features use GaussNoise logic; categorical features use SCARF marginal logic. The feature-type mask determines which path each feature takes — no per-feature if/else inside the loop is needed; use vectorized NumPy masking instead.

Corruption rate p = 0.3 and σ-scale = 0.1 are thesis defaults. Both should be configurable via a config dict so Week 7 sensitivity studies can sweep them without code changes.
