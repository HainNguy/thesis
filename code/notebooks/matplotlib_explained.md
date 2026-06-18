# Matplotlib Tutorial — Erklärungen

---

## §1 — The Figure / Axes Model

---

### Was ist Matplotlib?

Matplotlib ist eine Python-Bibliothek zum Erstellen von Diagrammen und Plots. Der Import sieht immer so aus:

```python
import matplotlib.pyplot as plt
```

`pyplot` ist das Modul, das du in jedem Plot verwenden wirst.

---

### Die zwei zentralen Objekte: Figure und Axes

Jeder Matplotlib-Plot besteht aus genau **zwei Objekten**:

| Objekt | Was es ist | Alltagsanalogie |
|--------|------------|-----------------|
| `Figure` | Die gesamte Leinwand / Seite | Ein leeres Blatt Papier |
| `Axes` | Ein Plot-Panel innerhalb der Leinwand | Ein Bilderrahmen auf dem Papier |

> Stell es dir wie ein DataFrame vor: die **Figure** ist der DataFrame, und die **Axes** ist eine Spalte darin.

Du kannst eine oder viele Axes auf einer Figure haben (ein Raster von Panels). In beiden Fällen erstellst du sie immer zusammen.

---

### Figure und Axes erstellen

Du verwendest `plt.subplots()`, um beide gleichzeitig zu erstellen:

```python
fig, ax = plt.subplots()
```

- `fig` ist die Figure (die Leinwand)
- `ax` ist die Axes (das Plot-Panel)

`plt.subplots()` gibt ein **Tupel** zurück — deshalb entpackst du es in zwei Variablen.

---

### `figsize` — Die Leinwandgröße steuern

```python
fig, ax = plt.subplots(figsize=(5, 3))
```

`figsize=(Breite, Höhe)` ist in **Zoll** angegeben. Für eine Bachelorarbeit ist `(6, 4)` ein guter Standard für einzelne Plots.

---

### Das OOP-Interface — Immer `ax` verwenden, nie `plt`

Matplotlib hat zwei Stile:

```python
# ❌ Funktionaler Stil — vermeiden
plt.plot([1, 2, 3], [4, 2, 5])
plt.title('Mein Plot')

# ✅ OOP-Stil — immer so machen
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 2, 5])
ax.set_title('Mein Plot')
```

Beide erzeugen bei einem einzelnen Plot dasselbe Ergebnis. Aber wenn du **mehrere Panels** hast (§6), weiß `plt.plot()` nicht, welches Panel gemeint ist. `ax.plot()` ist immer eindeutig.

**Regel: Immer über `ax` gehen.**

---

### Auf einer Axes zeichnen

Sobald du `ax` hast, rufst du Methoden darauf auf:

| Methode | Was sie tut |
|---------|-------------|
| `ax.plot(x, y)` | Liniendiagramm |
| `ax.set_title('...')` | Titel über dem Plot |
| `ax.set_xlabel('...')` | Beschriftung der x-Achse |
| `ax.set_ylabel('...')` | Beschriftung der y-Achse |

---

### Worked Example (aus dem Notebook)

```python
fig, ax = plt.subplots(figsize=(5, 3))

ax.plot([1, 2, 3], [4, 2, 5], color='steelblue', marker='o', lw=2)
ax.set_title('My first Axes')
ax.set_xlabel('x axis')
ax.set_ylabel('y axis')

plt.tight_layout()
plt.show()
```

**Zeile für Zeile:**

| Zeile | Was sie tut |
|-------|-------------|
| `plt.subplots(figsize=(5, 3))` | Erstellt eine 5×3 Zoll Leinwand mit einem Plot-Panel |
| `ax.plot([1,2,3], [4,2,5], ...)` | Zeichnet eine Linie durch die 3 Punkte |
| `color='steelblue'` | Setzt die Linienfarbe |
| `marker='o'` | Zeichnet einen Kreis an jedem Datenpunkt |
| `lw=2` | Setzt die Linienbreite auf 2 Punkte |
| `ax.set_title(...)` | Fügt einen Titel hinzu |
| `ax.set_xlabel/ylabel(...)` | Beschriftet die Achsen |
| `plt.tight_layout()` | Passt Abstände automatisch an, damit Beschriftungen nicht abgeschnitten werden |
| `plt.show()` | Rendert und zeigt die Figure an |

---

### Mehrere Axes — `plt.subplots(rows, cols)`

Du kannst ein Raster von Panels erstellen, indem du Zahlen an `plt.subplots()` übergibst:

```python
fig, axes = plt.subplots(1, 3)    # 1 Zeile, 3 Spalten → 3 nebeneinander liegende Plots
fig, axes = plt.subplots(2, 2)    # 2×2 Raster → 4 Plots
```

Bei mehreren Axes ist `axes` eine **Liste** (oder ein 2D-Array bei Rastern). Du greifst auf jede per Index zu:

```python
fig, axes = plt.subplots(1, 2)

axes[0].plot(...)    # linkes Panel
axes[1].plot(...)    # rechtes Panel
```

---

### Exercise 1 — Die Lücken füllen

Die Notebook-Übung verlangt eine 1×2-Figure mit `y = x²` links und `y = √x` rechts:

```python
x = np.linspace(0, 4, 50)          # 50 gleichmäßig verteilte Werte von 0 bis 4

fig, axes = plt.subplots(1, 2, figsize=(8, 3))   # 1 Zeile, 2 Spalten

axes[0].plot(x, x**2)              # x² links
axes[0].set_title('Left')

axes[1].plot(x, np.sqrt(x))        # √x rechts
axes[1].set_title('Right')

plt.tight_layout()
plt.show()
```

`np.linspace(0, 4, 50)` erzeugt 50 Zahlen von 0 bis 4 — ein glatter Bereich für eine Kurve.

---

### Zusammenfassung

| Konzept | Kernaussage |
|---------|-------------|
| `Figure` | Die gesamte Leinwand — eine pro Plot-Aufruf |
| `Axes` | Das zeichenbare Panel — eine oder mehrere pro Figure |
| `plt.subplots()` | Erstellt beide gleichzeitig — immer verwenden |
| `ax.methode()` | OOP-Interface — immer `ax`, nie direkt `plt` |
| `figsize=(w, h)` | Leinwandgröße in Zoll |
| `plt.tight_layout()` | Verhindert überlappende Beschriftungen — vor `show()` aufrufen |

---

## §2 — Scatter — 2D Cluster Embeddings

---

### Was ist ein Scatter Plot?

Ein Scatter Plot (Streudiagramm) zeigt **einzelne Punkte** im 2D-Raum. Jeder Punkt hat eine x- und eine y-Koordinate. In deiner Thesis verwendest du ihn, um PCA-reduzierte Embeddings zu visualisieren — also wo jeder Datenpunkt im 2D-Raum "landet" nach dem Encoder.

```python
ax.scatter(x_werte, y_werte)
```

---

### Die wichtigsten Parameter

| Parameter | Was er tut | Beispiel |
|-----------|-----------|---------|
| `color=` | Farbe aller Punkte | `color='steelblue'` |
| `c=` | Farbe pro Punkt (Array) | `c=labels` |
| `s=25` | Punktgröße (in Pixeln²) | `s=25` |
| `alpha=0.75` | Transparenz (0=unsichtbar, 1=voll) | `alpha=0.75` |
| `label=` | Name für die Legende | `label='Cluster 0'` |

---

### Cluster einfärben — der Loop-Pattern

In deiner Thesis hast du mehrere Cluster, jedes soll eine eigene Farbe bekommen. Das geht mit einer Schleife:

```python
COLORS = ['#e41a1c', '#377eb8', '#4daf4a']   # eine Farbe pro Cluster

for k in range(3):
    mask = cluster_labels == k          # boolean array: True wo Label == k
    ax.scatter(X[mask, 0], X[mask, 1],  # nur die Punkte von Cluster k
               color=COLORS[k],
               s=25, alpha=0.75,
               label=f'Cluster {k}')
```

**Was passiert hier Schritt für Schritt:**

| Zeile | Erklärung |
|-------|-----------|
| `mask = cluster_labels == k` | Erstellt ein True/False-Array — True an jeder Position wo der Label gleich `k` ist |
| `X[mask, 0]` | Wählt alle x-Koordinaten der Punkte mit Label `k` |
| `X[mask, 1]` | Wählt alle y-Koordinaten der Punkte mit Label `k` |
| `color=COLORS[k]` | Jede Iteration bekommt eine andere Farbe |
| `label=f'Cluster {k}'` | Notwendig damit die Legende den richtigen Namen zeigt |

---

### Die Legende — `ax.legend()`

Damit die Legende erscheint, brauchst du **zwei Dinge**:
1. Jedes `scatter`-Call muss ein `label=` haben
2. Du rufst am Ende `ax.legend()` auf

```python
ax.legend(frameon=False)   # frameon=False entfernt den Rahmen um die Legende
```

---

### Worked Example (aus dem Notebook)

```python
COLORS = ['#e41a1c', '#377eb8', '#4daf4a']

fig, ax = plt.subplots(figsize=(5, 4))

for k in range(3):
    mask = cluster_labels == k
    ax.scatter(X[mask, 0], X[mask, 1],
               color=COLORS[k], s=25, alpha=0.75, label=f'Cluster {k}')

ax.set_title('2D Embeddings — Feature Masking')
ax.set_xlabel('PCA dim 1')
ax.set_ylabel('PCA dim 2')
ax.legend(frameon=False)
plt.tight_layout()
plt.show()
```

**Was du siehst:** Drei farbige Punktwolken, jede repräsentiert einen Cluster. Je stärker sie sich trennen, desto besser hat das Clustering funktioniert.

---

### Exercise 2 — 4. Cluster hinzufügen

Die Lösung aus dem Notebook:

```python
rng2 = np.random.default_rng(7)
X4 = np.vstack([X, rng2.multivariate_normal((1, 4), 0.4 * np.eye(2), n)])
labels4 = np.append(cluster_labels, np.full(n, 3))

COLORS4 = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3']  # 4. Farbe ergänzt

fig, ax = plt.subplots(figsize=(5, 4))
for k in range(4):
    mask = labels4 == k
    ax.scatter(X4[mask, 0], X4[mask, 1],
               color=COLORS4[k], s=25, alpha=0.75, label=f'Cluster {k}')

ax.set_title('2D Embeddings — 4 Clusters')
ax.legend(frameon=False)
plt.tight_layout()
plt.show()
```

`np.vstack` stapelt zwei Arrays vertikal — damit werden die Punkte des 4. Clusters an `X` angehängt. `np.full(n, 3)` erstellt ein Array mit `n` mal dem Wert `3` — das sind die Labels für den neuen Cluster.

---

### Zusammenfassung

| Konzept | Kernaussage |
|---------|-------------|
| `ax.scatter(x, y)` | Zeichnet Punkte im 2D-Raum |
| `mask = labels == k` | Wählt nur die Punkte eines bestimmten Clusters |
| `alpha=0.75` | Leichte Transparenz zeigt Dichte |
| `label=` + `ax.legend()` | Beide zusammen nötig für die Legende |
| `frameon=False` | Sauberere Legende ohne Rahmen |
