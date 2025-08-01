import os
import glob
import json

# Configuration
INPUT_DIR = "data/reference_texts/alchemical_corpora/Syriac"
OUTPUT_FILE = "syriac_corpus.jsonl"
OUTPUT_DIR = f'{INPUT_DIR}/language_processed'

# Helpers
def extract_between_markers(lines, start_marker, end_marker):
    """Return the lines found between start_marker and end_marker."""
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i + 1
        elif end_marker in line and start_idx is not None:
            end_idx = i
            break
    if start_idx is not None and end_idx is not None:
        return lines[start_idx:end_idx]
    return None

def process_file_old(path):
    """Read a file, extract Coptic lines, and return dict or None."""
    with open(path, 'r', encoding='utf-8') as f:
        lines = [l.rstrip('\n') for l in f]
    extracted = extract_between_markers(lines, "Normalized Text", "ANNIS Metadata")
    if not extracted:
        return None
    text = "\n".join(extracted).strip()
    source = os.path.splitext(os.path.basename(path))[0]
    return {
        "language": "Syriac",
        "source": source,
        "text": text
    }
def process_file(path):
    """Read a file, extract Coptic lines, and return dict."""
    with open(path, 'r', encoding='utf-8') as f:
        lines = [l.rstrip('\n') for l in f]

    extracted = extract_between_markers(lines, "Normalized Text", "ANNIS Metadata")

    # If markers weren't found, use the whole file as the text
    if not extracted:
        extracted = lines

    text = "\n".join(extracted).strip()
    source = os.path.splitext(os.path.basename(path))[0]
    return {
        "language": "Syriac",
        "source": source,
        "text": text
    }
    
def main():
    txt_files = glob.glob(os.path.join(INPUT_DIR, "**", "*.txt"), recursive=True)
    print(f"Found {len(txt_files)} .txt files under {INPUT_DIR!r}")
    
    with open(f'{OUTPUT_DIR}/{OUTPUT_FILE}', 'w', encoding='utf-8') as out:
        count = 0
        for txt in txt_files:
            record = process_file(txt)
            if record:
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1
            else:
                print(f"  ⚠️ Skipped (markers not found): {txt}")
        print(f"Wrote {count} records to {OUTPUT_FILE!r}")

if __name__ == "__main__":
    main()
