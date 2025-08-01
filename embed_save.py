import json
from pathlib import Path
from datetime import datetime, timezone

def save_records_with_embeddings(records, output_dir="data/embeddings", prefix="voynich_records_with_embeddings"):
    """
    Save the list of record dicts (each having 'metadata', 'text', and 'embedding')
    to a JSONL file in the specified output directory, with a timezone-aware UTC timestamp.
    """
    # Ensure the directory exists
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate a timezone‐aware UTC timestamp
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{prefix}_{timestamp}.jsonl"
    out_path = out_dir / filename
    
    # Write each record as a JSON line
    with open(out_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    
    print(f"Saved {len(records)} records to {out_path}")
