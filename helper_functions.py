import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import matplotlib.patches as mpatches
from collections import Counter
import json
import re
import os

# =====================
# CONFIGURATION SECTION
# =====================
VOYNICH_PATH = r"data\embeddings\voynich_chunks_H_20250727T150741Z.jsonl"

LANGUAGES_CONFIG = {
    "Coptic": {
        "path": r"data\reference_texts\alchemical_corpora\Coptic\language_processed\coptic_chunks_20250727T150738Z.jsonl",
        "color": "black",
        "symbol": "𓆎"
    },
    "Greek": {
        "path": r"data\reference_texts\alchemical_corpora\Greek\language_processed\Hermetica_20250727T152401Z.jsonl",
        "color": "cyan",
        "symbol": "Δ"
    },
    "Hebrew": {
         "path": r"data\reference_texts\alchemical_corpora\Hebrew\language_processed\SeferYetzira_20250727T155303Z.jsonl",
         "color": "gray",
         "symbol": "W"
    },
    "Syriac": {
        "path": r"data\reference_texts\alchemical_corpora\Syriac\language_processed\syriac_corpus_20250727T161033Z.jsonl",
        "color": "magenta",
        "symbol": "W"
    }
}

SECTION_COLORS = {
    'Herbal': 'green', 'Astronomical': 'blue', 'Biological': 'red',
    'Zodiac': 'purple', 'Cosmological': 'orange', 'Pharmaceutical': 'brown',
    'Stars': 'pink', 'Text': 'gray', 'Unknown': 'silver'
}

ZODIAC_MAP = {
    '1': 'Aries', '2': 'Taurus', '3': 'Gemini', '4': 'Cancer',
    '5': 'Leo', '6': 'Virgo', '7': 'Libra', '8': 'Scorpio',
    '9': 'Sagittarius', '10': 'Capricorn', '11': 'Aquarius', '12': 'Pisces'
}

PLOT_SIZE = (16, 12)
PLOT_DPI = 300
OUTPUT_FILENAME = "voynich_language_comparison.png"

# =====================
# FUNCTION DEFINITIONS
# =====================

def load_embeddings(path, source_name):
    records = []
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        print(f"  JSON decode error in {path}")
            print(f"Loaded {len(records)} records from {source_name}")
        else:
            print(f"File not found: {path}")
    except Exception as e:
        print(f"Error loading {source_name}: {str(e)}")
    return records


def extract_section(metadata):
    if not isinstance(metadata, list):
        return 'Unknown'
    sections = []
    for item in metadata:
        if isinstance(item, dict):
            section = item.get('section')
            if section and isinstance(section, str):
                sections.append(section)
    return Counter(sections).most_common(1)[0][0] if sections else 'Unknown'


def clean_labels(labels):
    cleaned = []
    for label in labels:
        if isinstance(label, str) and label.isdigit():
            cleaned.append(ZODIAC_MAP.get(label, 'Zodiac'))
        elif isinstance(label, str):
            clean_label = re.sub(r'\s+', ' ', label).strip()
            cleaned.append(clean_label)
        else:
            cleaned.append('Unknown')
    return cleaned


def annotate_group(ax, label, color, positions, symbol=""):
    indices = [i for i, lbl in enumerate(cleaned_labels) if lbl == label]
    if indices:
        center = np.mean(positions[indices], axis=0)
        ax.annotate(f"{symbol}{label}", center,
                    fontsize=10, ha='center', color=color,
                    bbox=dict(boxstyle="round,pad=0.3", fc='white', ec=color, alpha=0.8))
        return center
    return None

# =====================
# MAIN PROCESSING
# =====================
print("===== Loading Data =====")
voynich_records = load_embeddings(VOYNICH_PATH, "Voynich")
reference_records = {}
for lang, config in LANGUAGES_CONFIG.items():
    reference_records[lang] = load_embeddings(config["path"], lang)

print("\n===== Preparing Data =====")
all_records = voynich_records.copy()
all_labels, all_sources, all_embeddings = [], [], []

# Voynich
for chunk in voynich_records:
    try:
        section = extract_section(chunk.get('metadata', []))
        all_embeddings.append(chunk["embedding"])
        all_labels.append(section)
        all_sources.append('Voynich')
    except Exception as e:
        print(f"Skipping Voynich chunk: {str(e)}")

# References
for lang, records in reference_records.items():
    for record in records:
        try:
            all_embeddings.append(record["embedding"])
            all_labels.append(lang)
            all_sources.append(lang)
            all_records.append(record)
        except Exception as e:
            print(f"Skipping {lang} record: {str(e)}")

cleaned_labels = clean_labels(all_labels)
label_counter = Counter(cleaned_labels)
print("\nLabel distribution:")
for label, count in label_counter.most_common():
    print(f"- {label}: {count}")

# Prepare arrays
X = np.array(all_embeddings)
# PCA for visualization only
X2d = PCA(n_components=2).fit_transform(X)

print("\n===== Creating Visualization =====")
color_map = SECTION_COLORS.copy()
for lang, config in LANGUAGES_CONFIG.items():
    color_map[lang] = config["color"]
colors = [color_map.get(lbl, 'silver') for lbl in cleaned_labels]
sizes = [20 if src=='Voynich' else 40 for src in all_sources]
alphas = [0.7 if src=='Voynich' else 0.9 for src in all_sources]

fig, ax = plt.subplots(figsize=PLOT_SIZE)
ax.scatter(X2d[:,0], X2d[:,1], c=colors, s=sizes, alpha=alphas)

# Legend
handles = []
for label, color in color_map.items():
    cnt = cleaned_labels.count(label)
    if cnt:
        symbol = LANGUAGES_CONFIG.get(label, {}).get("symbol", "")
        handles.append(mpatches.Patch(color=color, label=f"{symbol}{label} ({cnt})"))
unknown_cnt = cleaned_labels.count('Unknown')
if unknown_cnt:
    handles.append(mpatches.Patch(color='silver', label=f"Unknown ({unknown_cnt})"))
ax.legend(handles=handles, title="Sections & Languages", loc='upper left', bbox_to_anchor=(1,1), fontsize=9)

# Annotations
centers = {}
for lang, conf in LANGUAGES_CONFIG.items():
    centers[lang] = annotate_group(ax, lang, conf["color"], X2d, conf.get("symbol",""))
for section in ['Herbal','Astronomical','Biological','Zodiac']:
    centers[section] = annotate_group(ax, section, SECTION_COLORS.get(section,'silver'), X2d)

# Connections
for section in ['Herbal', 'Astronomical']:
    section_center = centers.get(section)
    if section_center is not None:
        for lang in LANGUAGES_CONFIG:
            lang_center = centers.get(lang)
            if lang_center is not None:
                ls = '-' if section == 'Herbal' else '--'
                ax.plot(
                    [section_center[0], lang_center[0]],
                    [section_center[1], lang_center[1]],
                    color=color_map[lang],
                    linestyle=ls,
                    alpha=0.3,
                    linewidth=1.5
                )

# Distance annotations (cosine distance)
for base in ['Herbal', 'Astronomical']:
    base_center = centers.get(base)
    if base_center is None:
        continue

    for idx, lang in enumerate(LANGUAGES_CONFIG):
        lang_center = centers.get(lang)
        if lang_center is None:
            continue

        # compute cosine distance
        sim = cosine_similarity(
            [base_center],
            [lang_center]
        )[0][0]
        dist = 1 - sim

        ax.text(
            0.05,
            0.95 - 0.05 * idx,
            f"{base}-{lang} CosDist: {dist:.2f}",
            transform=ax.transAxes,
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.7)
        )


ax.set_title("Voynich Manuscript Linguistic Comparison", fontsize=18)
ax.set_xlabel("Principal Component 1", fontsize=12)
ax.set_ylabel("Principal Component 2", fontsize=12)
ax.grid(alpha=0.1)
plt.tight_layout()
plt.savefig(OUTPUT_FILENAME, dpi=PLOT_DPI, bbox_inches='tight')
print(f"Plot saved as '{OUTPUT_FILENAME}'")
plt.show()

# Helper to compute and print Cosine Distance between two indices
def report_dist(label_a, label_b):
    idx_a = cleaned_labels.index(label_a)
    idx_b = cleaned_labels.index(label_b)
    sim = cosine_similarity([X[idx_a]], [X[idx_b]])[0][0]
    print(f"{label_a} to {label_b}: CosDist={1 - sim:.4f}")

# Herbal
if 'Herbal' in cleaned_labels:
    for lang in LANGUAGES_CONFIG:
        if lang in cleaned_labels:
            report_dist('Herbal', lang)

# Astronomical
if 'Astronomical' in cleaned_labels:
    for lang in LANGUAGES_CONFIG:
        if lang in cleaned_labels:
            report_dist('Astronomical', lang)

print("\n===== Closest Voynich Sections to Languages =====")
for lang in LANGUAGES_CONFIG:
    lang_indices = [i for i,lbl in enumerate(cleaned_labels) if lbl==lang]
    voy_indices = [i for i,src in enumerate(all_sources) if src=='Voynich']
    if lang_indices and voy_indices:
        nn = NearestNeighbors(n_neighbors=3, metric='cosine').fit(X[voy_indices])
        dists, idxs = nn.kneighbors([X[lang_indices[0]]])
        print(f"\nClosest Voynich sections to {lang}:")
        for d,i in zip(dists[0], idxs[0]):
            sec = cleaned_labels[voy_indices[i]]
            print(f"  - {sec} (cosDist: {d:.4f})")
