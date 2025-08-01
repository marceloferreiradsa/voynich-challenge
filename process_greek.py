import os
import json

# Configuration
input_file = "data/reference_texts/alchemical_corpora/Greek/language_processed/Hermetica_clean.txt"
output_file = "data/reference_texts/alchemical_corpora/Greek/language_processed/Hermetica.jsonl"
language = "Greek"  

# Read input file
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Split into chunks by break marker
chunks = content.split("===BREAK===")

# Write each chunk to a JSONL row
with open(output_file, 'w', encoding='utf-8') as out_f:
    for i, chunk in enumerate(chunks):
        cleaned = chunk.strip()
        if not cleaned:
            continue  # skip empty chunks
        record = {
            "language": language,
            "source": f"break_{i+1}",
            "text": cleaned.replace("\n", " ")
        }
        out_f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"Saved {len(chunks)} chunks to {output_file}")
