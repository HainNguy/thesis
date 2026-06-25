# Dataset Taxonomy — Benchmark Suite

**Week 2 deliverable (22–29 Jun 2026) · Phase A, Milestone M2**

Computed by `code/notebooks/dataset_selection.ipynb`.  
Four OpenML datasets selected to cover the categorical-fraction spectrum and provide the stratification axis for Phase C (Weeks 6–7).

---

## Selected Datasets

| slug | Name | OpenML ID | Rows | Features | Classes | Numerical | Categorical | Cat% | Stratum |
|------|------|-----------|-----:|--------:|--------:|----------:|------------:|-----:|---------|
| iris | Iris | 61 | 150 | 4 | 3 | 4 | 0 | **0 %** | all-numerical |
| credit-g | German Credit | 31 | 1 000 | 20 | 2 | 7 | 13 | **65 %** | high-categorical |
| car | Car Evaluation | 40975 | 1 728 | 6 | 4 | 0 | 6 | **100 %** | all-categorical |
| adult | Adult/Census Income | 1590 | 48 842 | 14 | 2 | 6 | 8 | **57 %** | high-categorical |

**Stratification axis for Phase C reporting:**
- *all-numerical* stratum: Iris (0 % categorical)
- *high-categorical* stratum: German Credit (65 %), Car Evaluation (100 %), Adult (57 %)

---

## Feature-Type Details

### Iris (iris, OpenML #61)
- **Numerical (4):** sepallength, sepalwidth, petallength, petalwidth
- **Categorical (0):** —
- All features are ratio-scale measurements. No semantic-validity concern for Gaussian noise; SCARF-style marginal corruption is safe.

### German Credit (credit-g, OpenML #31)
- **Numerical (7):** duration, credit_amount, installment_commitment, residence_since, age, existing_credits, num_dependents
- **Categorical (13):** checking_status, credit_history, purpose, savings_status, employment, personal_status, other_parties, property_magnitude, other_payment_plans, housing, job, own_telephone, foreign_worker
- 13 of 20 features are categorical. Generic numeric corruption (Gaussian noise) is inapplicable to the majority of features. Type-Aware augmentation is mandatory to avoid semantic violations.

### Car Evaluation (car, OpenML #40975)
- **Numerical (0):** —
- **Categorical (6):** buying, maint, doors, persons, lug_boot, safety
- Entirely ordinal/categorical. Applying Gaussian noise directly to ordinal-encoded integers would be semantically meaningless. This dataset is the hardest test for type-aware augmentation.

### Adult / Census Income (adult, OpenML #1590)
- **Numerical (6):** age, fnlwgt, education-num, capital-gain, capital-loss, hours-per-week
- **Categorical (8):** workclass, education, marital-status, occupation, relationship, race, sex, native-country
- The two most informative features (relationship, marital-status) are categorical. Corrupting them violates the positive-pair assumption directly. This is the thesis's primary motivating example for the semantic-validity concern.
- **Scale note:** 48 k rows may be slow on CPU. Plan B: stratified subsample to 10 k rows with `random_state=0` if Phase B training time is a blocker.

---

## Mutual Information with Class Label (top 5 per dataset)

### Iris
| Feature | Type | MI |
|---------|------|----|
| petallength | num | 0.9896 |
| petalwidth | num | 0.9749 |
| sepallength | num | 0.4739 |
| sepalwidth | num | 0.2783 |

Signal is very high and concentrated in two features. Even mild corruption risks.

### German Credit
| Feature | Type | MI |
|---------|------|----|
| checking_status | **cat** | 0.0657 |
| credit_history | **cat** | 0.0302 |
| residence_since | num | 0.0204 |
| savings_status | **cat** | 0.0195 |
| purpose | **cat** | 0.0173 |

All MI values are low. Top signal is categorical. Hard clustering task — semantic corruption will likely push signal below noise.

### Car Evaluation
| Feature | Type | MI |
|---------|------|----|
| safety | **cat** | 0.1817 |
| persons | **cat** | 0.1523 |
| buying | **cat** | 0.0669 |
| maint | **cat** | 0.0511 |
| lug_boot | **cat** | 0.0208 |

Two features carry most of the signal; all categorical.

### Adult / Census Income
| Feature | Type | MI |
|---------|------|----|
| relationship | **cat** | 0.1147 |
| marital-status | **cat** | 0.1088 |
| capital-gain | num | 0.0832 |
| age | num | 0.0683 |
| education-num | num | 0.0650 |

Categorical features lead in MI, supporting the thesis's core semantic-validity argument.

---

## Hypotheses for Phase C Stratification

**H1 (numerical stratum):** On Iris, all augmentation methods (including generic corruption) should preserve NMI/ARI well — numerical features tolerate perturbation.

**H2 (high-categorical stratum):** On German Credit, Car, and Adult, generic corruption methods (SCARF with arbitrary masking, Gaussian noise applied to categorical-encoded values) should yield lower NMI/ARI than:
- Type-Aware augmentation (categorical → marginal replacement only)
- Identity baseline (no augmentation)

**H3 (Type-Aware advantage):** The NMI/ARI gap between generic augmentation and identity baseline should be larger on datasets with higher categorical fraction.

These three hypotheses map directly to the stratified results tables in Week 7.

---

## How Augmentations Apply per Dataset

| Augmentation | Iris | German Credit | Car Evaluation | Adult |
|---|---|---|---|---|
| SCARF (marginal, any feature) | ok | corrupts 65 % cat features | corrupts all features | corrupts 57 % cat features |
| Gaussian noise | ok (num only) | inapplicable to 13 cat features | inapplicable to all 6 | inapplicable to 8 cat features |
| Feature swap | ok | risky for cat features | risky for all | risky for 8 cat features |
| **Type-Aware** | num→noise; cat→marginal | num→noise; cat→marginal | all→marginal | num→noise; cat→marginal |
| Identity | ok | ok | ok | ok |
