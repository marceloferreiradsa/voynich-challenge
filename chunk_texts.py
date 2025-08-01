import os
import json

def chunk_txt_to_jsonl(input_path, output_path, language, lines_per_chunk):
    """
    Splits a .txt file into a .jsonl file with chunks based on a given number of lines.

    Args:
        input_path (str): Path to the input .txt file.
        output_path (str): Path to the output .jsonl file.
        language (str): Language label for the JSON objects.
        lines_per_chunk (int): Number of lines per chunk.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    chunks = [
        lines[i:i + lines_per_chunk]
        for i in range(0, len(lines), lines_per_chunk)
    ]

    count = 0
    with open(output_path, 'w', encoding='utf-8') as out_f:
        for idx, chunk in enumerate(chunks, start=1):
            text = " ".join(chunk).strip()
            if not text:
                continue
            record = {
                "language": language,
                "source": f"{base_name}_chunk_{idx}",
                "text": text.replace('\n', ' ').replace('\"', ' ')
            }
            out_f.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1

    print(f'Saved {count} chunks into "{output_path}"')


def jsonl_to_chunked_json(input_path: str, output_path: str, chunk_size: int, max_chars: int = 1000):
    """
    Converts a .jsonl file to a structured JSON file, chunking based on number of records
    and splitting large texts into subchunks if they exceed `max_chars`.

    Args:
        input_path (str): Path to input .jsonl
        output_path (str): Path to output .json
        chunk_size (int): Number of sources per output record
        max_chars (int): Max characters allowed in a source before splitting it into multiple sections
    """
    records = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            text = rec.get("text", "")
            num_parts = max(1, math.ceil(len(text) / max_chars))

            for i in range(num_parts):
                start = i * max_chars
                end = start + max_chars
                records.append({
                    "language": rec.get("language", ""),
                    "source": rec.get("source", ""),
                    "text": text[start:end].strip(),
                    "section": str(i + 1)
                })

    # Group into chunks of chunk_size
    chunks = [
        records[i:i+chunk_size]
        for i in range(0, len(records), chunk_size)
    ]

    # Build output
    output = []
    for chunk in chunks:
        metadata = []
        texts = []
        for rec in chunk:
            metadata.append({
                "language": rec["language"],
                "source": rec["source"],
                "row": "",
                "section": rec["section"]
            })
            texts.append(rec["text"])
        output.append({
            "metadata": metadata,
            "text": " ".join(texts)
        })

    # Write output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(output)} chunked records into '{output_path}'")

