import os
from pathlib import Path

# Define base structure
base_dirs = [
    "voynich-challenge/data/raw",
    "voynich-challenge/data/processed",
    "voynich-challenge/data/embeddings",
    "voynich-challenge/models/gpt2-small/run-01-lr5e-5-ep10",
    "voynich-challenge/models/gpt2-small/run-02-lr1e-4-ep5",
    "voynich-challenge/models/gpt2-medium/run-01-lr5e-5-ep10",
    "voynich-challenge/notebooks",
    "voynich-challenge/src",
    "voynich-challenge/logs"
]

# Create directories
for dir_path in base_dirs:
    Path(dir_path).mkdir(parents=True, exist_ok=True)

# Create placeholder files
placeholder_files = {
    "voynich-challenge/data/embeddings/eva-20250713-embed.pkl": "",
    "voynich-challenge/data/embeddings/takahashi-20250714-embed.pkl": "",
    "voynich-challenge/models/gpt2-small/run-01-lr5e-5-ep10/config.json": "{}",
    "voynich-challenge/models/gpt2-small/run-01-lr5e-5-ep10/pytorch_model.bin": "",
    "voynich-challenge/models/gpt2-small/run-01-lr5e-5-ep10/metrics.json": "{}",
    "voynich-challenge/notebooks/01-ingest-and-embed.ipynb": "",
    "voynich-challenge/notebooks/02-prototype-llm-prompts.ipynb": "",
    "voynich-challenge/src/ingest.py": "# ingest script",
    "voynich-challenge/src/embed.py": "# embed script",
    "voynich-challenge/src/train.py": "# train script",
    "voynich-challenge/src/evaluate.py": "# evaluate script",
    "voynich-challenge/README.md": "# Voynich Challenge\n\nProject overview."
}

for file_path, content in placeholder_files.items():
    with open(file_path, 'w') as f:
        f.write(content)

print("Folder structure and placeholder files created successfully.")
