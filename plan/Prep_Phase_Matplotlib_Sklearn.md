# Preparation Phase — Complete Learning Plan
**Until 11 June 2026 · Official start: 15 June 2026**

| Tool | Status |
|------|--------|
| numpy | ✅ done |
| pandas | ✅ done |
| matplotlib | 7. Jun |
| scikit-learn | 10. Jun |
| Mini-Projekt | 11. Jun |

Available days: **So 7. Jun · Mi 10. Jun · Do 11. Jun**
Not available: Mo 8. Jun · Di 9. Jun

---

## So, 7. Juni — matplotlib (komplett)

Matplotlib ist API-lastig, kein tiefes Konzeptverständnis nötig — ein voller Tag reicht.

**Vormittag — Grundstruktur + Hauptplots**
- `fig, ax = plt.subplots()` — das Figure/Axes-Modell, alles läuft darüber
- `ax.scatter()` — 2D-Embeddings eingefärbt nach Cluster-Label
- `ax.plot()` — Lernkurven (Loss über Epochen)
- `ax.hist()` — Feature-Verteilungen

**Nachmittag — Mehrere Panels + Publication-ready**
- `plt.subplots(2, 3)` — Vergleichsplots über Augmentierungen (Woche 7)
- `ax.bar()` — NMI/ARI-Vergleich, die wichtigste Thesis-Grafik
- `plt.savefig('fig.pdf', dpi=300, bbox_inches='tight')` — für LaTeX-Einbindung
- Achsenbeschriftung, Legende, Titel

**Übung:** 2×2-Panel mit scatter, plot, hist, bar — als PDF speichern.

---

## Mi, 10. Juni — scikit-learn (komplett)

Alle sklearn-APIs folgen demselben Muster (`fit` / `transform` / `predict`) — ein intensiver Tag reicht.

**Block 1 — Preprocessing**
- `StandardScaler` — numerische Features (entspricht `(x - mean) / std` in numpy)
- `OneHotEncoder` — kategorische Features → Binärvektoren
- `ColumnTransformer` — verschiedene Transformer auf verschiedene Spalten
- `Pipeline(steps=[...])` — alles kapseln, `.fit_transform(X_train)` / `.transform(X_test)`

**Block 2 — Clustering + Dimensionsreduktion**
- `KMeans(n_clusters=k, random_state=42).fit(X)` → `.labels_`
- `PCA(n_components=2).fit_transform(X)` — Embeddings auf 2D reduzieren zum Plotten

**Block 3 — Metriken + Datasets**

Die Metriken kennst du konzeptuell aus dem Data-Mining-Kurs — hier nur die sklearn-API:
- `normalized_mutual_info_score(y_true, y_pred)`
- `adjusted_rand_score(y_true, y_pred)`
- `silhouette_score(X, labels)` — ohne Ground-Truth, für unlabeled Daten
- `fetch_openml(name='...')` — so lädst du später deine Thesis-Datasets

**Übung:** `load_digits()` laden → StandardScaler → KMeans → NMI/ARI/Silhouette berechnen, `n_clusters` variieren.

---

## Do, 11. Juni — Mini-Projekt (end-to-end)

> *"Cluster the Iris or Digits dataset, compute NMI/ARI, plot the embedding in 2D"*
> — direkt aus dem Thesis-Timeline-Plan, Vorbereitung auf Phase B (Woche 3)

Pipeline:

```
load_digits()
  → StandardScaler
  → PCA(2) für Plot  /  PCA(10) als KMeans-Eingabe
  → KMeans(n_clusters=10)
  → NMI, ARI, Silhouette ausgeben
  → Scatter-Plot als PDF speichern
```

- **Vormittag:** Pipeline aufbauen und zum Laufen bringen
- **Nachmittag:** Plots thesis-tauglich machen (Beschriftungen, Layout, PDF-Export) + Puffer für Debugging

**Ziel:** Ein sauberes Jupyter Notebook, das end-to-end läuft. Das ist fast identisch mit dem, was in Woche 3 real gebaut wird — später kommt nur ein MLP-Encoder zwischen Scaler und KMeans.

---

## Zeitübersicht

| Datum | Wochentag | Inhalt |
|-------|-----------|--------|
| ~~vor 7. Jun~~ | | ~~numpy~~ ✅ · ~~pandas~~ ✅ |
| **7. Jun** | So | matplotlib komplett |
| ~~8. Jun~~ | ~~Mo~~ | ~~nicht verfügbar~~ |
| ~~9. Jun~~ | ~~Di~~ | ~~nicht verfügbar~~ |
| **10. Jun** | Mi | scikit-learn komplett |
| **11. Jun** | Do | Mini-Projekt (end-to-end) |
| 12.–14. Jun | Fr–So | PyTorch-Tutorial ("Deep Learning with PyTorch: A 60 Minute Blitz") |
| **15. Jun** | Mo | Offizieller Start der Bachelorarbeit |
