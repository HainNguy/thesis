# Speaking Script — Preliminary Presentation
**Hai Nguyen · LMU Munich · 12 June 2026**
*Target duration: 9:00 – 9:45 min*

---

## [→ SLIDE 1 — Title]

Good morning, Professor Seidl, Mamdouh. Thank you for the time. My name is Hai Nguyen, and I'm here to present my bachelor's thesis topic: Benchmarking Tabular Data Augmentation Techniques for Deep Clustering. Over the next ten minutes I'll walk you through the motivation, the research question, the approach I'm taking, and where I currently stand. I'll also be direct about the challenges I'm anticipating. Let's get started.

**[~0:30]**

---

## [→ SLIDE 2 — Introduction]

Let me start with the context. In many real-world applications — customer segmentation, medical records, sensor logs — we want to find structure in data, but we don't have labels. No one has sat down and told us "this sample belongs to group A, this one to group B." Clustering is the natural tool for this: it finds groupings without supervision.

The problem is that classical clustering — k-means being the most common — often fails on raw tabular data. Tabular datasets mix numerical and categorical features, they contain noise, and the relationship between features and cluster membership is frequently nonlinear. K-means assumes roughly spherical clusters in Euclidean space, which is simply not what tabular data looks like in practice.

Deep clustering is the response to this. Instead of clustering raw features directly, we first train a neural network to learn a compact latent representation — a space where the clusters become more separable — and then we cluster there.

**[~1:45]**

---

## [→ SLIDE 3 — Motivation]

So we're using a neural network to help with clustering. The natural question is: how do we train it without labels? This is where contrastive learning comes in.

The idea is elegant. Take one data point, create two slightly different versions of it — two "views" — and train the network to produce similar representations for those two views, while pushing representations of different points apart. The network learns what is structurally important about a sample, not what is superficially different.

This works extremely well in computer vision. If you have an image of a dog, you can randomly crop it, flip it, change the brightness — you still have a dog. Those augmentations are cheap, well-understood, and they don't change the semantic content.

Tabular data is different. There is no established equivalent. If you add random noise to a numerical feature, does the sample still belong to the same cluster? If you corrupt a categorical feature, have you created a meaningful view, or just noise? The research community has not reached a consensus. That is the gap this thesis addresses.

**[~3:15]**

---

## [→ SLIDE 4 — Research Question]

Which brings me to the research question.

*(pause two seconds — let the room settle)*

"Which tabular augmentation techniques are most effective for learning cluster-friendly representations with contrastive learning, and how do they impact deep clustering performance?"

The key phrase is *cluster-friendly*. I'm not asking which augmentations produce good representations in general — I'm asking which ones preserve the cluster structure we actually care about. The evaluation is always grounded in clustering quality: NMI and ARI.

**[~4:15]**

---

## [→ SLIDE 5 — Approach]

Here is how I'll answer that question.

*[point to the leftmost box]* We start with raw tabular data — numerical and categorical features together, loaded from OpenML or UCI. *[point to second box]* That data goes through an augmentation step, which I'll come back to in a moment. *[point to third box]* The augmented views are passed through an MLP encoder — a small multi-layer perceptron — which outputs a fixed-size embedding. *[point to fourth box]* We run k-means on those embeddings. *[point to fifth box]* And we evaluate the resulting clusters against ground-truth labels using NMI and ARI.

The critical design point is that this pipeline is identical for every augmentation. Only the second box changes. That is what makes it a benchmark — a controlled comparison.

The three techniques I'll compare are these. *[gesture toward the bullets below the diagram]* Feature masking, in the SCARF style, randomly replaces a fraction of features with values drawn from the marginal distribution of that feature. Gaussian noise adds small random perturbations to numerical features. And feature swapping exchanges feature values between randomly chosen samples in the same batch.

**[~6:00]**

---

## [→ SLIDE 6 — Timeline]

Let me show you where I stand and where this is heading.

The official thesis period runs from June 15th to August 23rd — ten weeks. The preparation phase, which ends this Sunday, was deliberately designed to move all tool onboarding out of the official period. The logic is simple: I arrive at week one with a working environment and solid Python skills, so that none of the ten official weeks is spent on pure setup.

*[gesture at the table]* The five phases break down like this. Weeks one and two are literature review and methodology — reading SCARF and the augmentation survey carefully, and agreeing the final method and datasets with Mamdouh. Weeks three through five are implementation, building the benchmark pipeline. Weeks six and seven are experiments and sensitivity studies. And the final three weeks are writing and submission, with the hard deadline of August 23rd.

I've defined three milestones to keep progress verifiable. *[point to the gold cells]* M1 at the end of week one: PyTorch ready and literature reviewed. M3 at the end of week four: a minimal working pipeline producing first clustering results. And M6 is the submission itself.

**[~7:30]**

---

## [→ SLIDE 7 — Expected Challenges]

I want to be direct about the challenges I'm anticipating, because each one is already reflected in the plan.

The first is the PyTorch learning curve. Implementing a contrastive loss — NT-Xent or InfoNCE — and a full training loop is new to me. This is exactly why the preparation phase exists: PyTorch onboarding happens before June 15th, not during the official period.

The second is mixed feature types. Gaussian noise works naturally on numerical columns, but applying it blindly to categorical features produces meaningless values. The augmentation modules need to handle both types correctly from the start.

Third, dataset selection is not trivial. NMI and ARI both require ground-truth labels, which many real tabular datasets simply do not provide. Choosing three or four appropriate datasets — ones that have labels, vary in size and dimensionality, and are genuinely representative — is a deliberate design decision I'll finalize in week two with Mamdouh.

And fourth, there is a real risk of negative transfer. An augmentation that improves representation learning on one dataset may destroy meaningful cluster boundaries on another. This is not a failure case to avoid — investigating exactly when and why that happens is one of the core contributions of the thesis.

**[~9:00]**

---

## [→ SLIDE 8 — Summary]

To wrap up. The research question is which tabular augmentation techniques best support cluster-friendly representations under contrastive learning. The approach is a controlled benchmark: three techniques, a fixed pipeline, evaluated by NMI and ARI across multiple datasets. The timeline runs ten official weeks from June 15th to August 23rd, with the preparation phase completing this weekend.

Thank you — I'm happy to take questions.

**[~9:40]**

---

## Opening energy note

Before you say a word, plant your feet, take one slow breath, and make eye contact with Professor Seidl first — since he knows you less, landing his attention early anchors the whole room before your voice fills it.
