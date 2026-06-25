Summary SCARF

## 1 Problem

- Self-supervised contrastive representation learning has been done little on real-world tabular datasets.



## 2 Corruption mechanism

- contrastive pre-training procedure <- generate view by selecting a random subset of its features and replacing them by random draws from the freatures's respective empirical marginal distributions.

## 3 Methodology and the idea behind InfoNCE

Encoder f -> Projection g -> classification h

g: SCARF’s projection head g ends with ℓ₂ normalization: both g(f(x)) and g(f(x~)) are normalized. InfoNCE then uses the dot product of these normalized embeddings, effectively measuring cosine similarity on the unit hypersphere.

## 4 Key results

- scarf improve classification accuracy in the fully-supervised setting, in the presence of label noise, in the semi-supervised setting
- Combining scarf pre-training with other solutions to these problems further improves them
- Proves its ability to learn effective task-asnostic representations
- scarf's way of constructing views is more effective than alternatives, scarf is less sensitive to feature scaling and it stable to various hyperparameters

## 5 Relevance to thesis

- what does "fine-tune f+h on labels" mean?
- what are self supervised learning, pre training, fine tuning
- what is softmax regarding infoNCE
- what are regularizers such as mixup, dropout, control, label smooth, distill...
- what are linear classifier?
- what are Softmax and cross‑entropy; temperature scaling (PREREQ for InfoNCE).