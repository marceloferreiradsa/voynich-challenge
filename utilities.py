import os
import json


def build_folder_tree_dict(base_path):
    tree = {}
    for entry in os.listdir(base_path):
        if entry.startswith('_') or entry.startswith('.'):
            continue  # skip folders starting with '_' or '.'
        path = os.path.join(base_path, entry)
        if os.path.isdir(path):
            tree[entry] = build_folder_tree_dict(path)
    return tree


def load_language_embeddings(path, language_name):
    """Load embeddings from JSONL files with error handling"""
    records = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON in {path}: {e}")
        print(f"Loaded {len(records)} records for {language_name}")
    except FileNotFoundError:
        print(f"File not found: {path}")
    except Exception as e:
        print(f"Error loading {path}: {str(e)}")
    return records

