import re
from collections import defaultdict

# Section mapping dictionary
SECTION_MAP = {
    'T': 'Text',
    'H': 'Herbal',
    'A': 'Astronomical',
    'Z': 'Zodiac',
    'B': 'Biological',
    'C': 'Cosmological',
    'P': 'Pharmaceutical',
    'S': 'Stars'
}

def preprocess_takahashi(file_path, transcriber='H'):
    """
    Parse a Takahashi transcription file and extract records for a given transcriber.
    Returns a list of dicts with metadata and cleaned text tokens.
    Includes section information based on folio metadata.
    """
    # First pass: Extract folio-section mappings
    section_mapping = {}
    section_pattern = re.compile(r'<([^>]+)>\s*\{\$I=([A-Z])')
    
    with open(file_path, 'r', encoding='latin1') as f:
        for line in f:
            line = line.strip()
            # Skip lines that aren't section declarations
            if not line.startswith('<') or '{$I=' not in line:
                continue
                
            # Extract folio and section code
            match = section_pattern.search(line)
            if match:
                folio = match.group(1)  # e.g., "f1v"
                section_code = match.group(2)  # e.g., "H"
                section_mapping[folio] = SECTION_MAP.get(section_code, 'Unknown')
    
    # Second pass: Process transcription lines
    records = []
    prefix_pattern = re.compile(r'<([^;>]+);([^>]+)>')
    
    with open(file_path, 'r', encoding='latin1') as f:
        for line in f:
            line = line.strip()
            # 1) skip blank lines
            if not line:
                continue
            # 2) skip pure comments
            if line.startswith('#') or line.startswith('##'):
                continue
            # 3) only process lines that start with '<' AND contain your transcriber tag
            if not line.startswith('<') or f';{transcriber}>' not in line:
                continue

            # Extract prefix and transcription text
            m = prefix_pattern.match(line)
            if not m:
                continue
            locator, tx_id = m.groups()
            page, para, row = locator.split('.')  # e.g. f1r, P2, 9

            # Everything after the first '>' is the raw transcription
            raw = line.split('>', 1)[1].strip()

            # Clean & tokenize
            cleaned = raw.replace('.', ' ')
            tokens = [w.rstrip('-').rstrip('?') for w in cleaned.split()]
            
            # Get section from mapping (default to 'Unknown')
            section = section_mapping.get(page, 'Unknown')

            records.append({
                'page': page,
                'paragraph': para,
                'row': row,
                'transcriber': tx_id,
                'section': section,  # NEW FIELD
                'raw': cleaned,
                'tokens': tokens
            })

    return records

def chunk_records(records, chunk_size=5):
    """
    Group records into chunks of N records each, but only within the same 'page'.
    Returns a list of chunk dicts with section metadata.
    """
    chunks = []
    # 1) Group records by page
    records_by_page = defaultdict(list)
    for rec in records:
        records_by_page[rec['page']].append(rec)
    
    # 2) For each page, slice into chunks
    for page, recs in records_by_page.items():
        for i in range(0, len(recs), chunk_size):
            chunk = recs[i : i + chunk_size]
            combined_text = ' '.join(rec['raw'] for rec in chunk) 
            
            # Create metadata with section info
            metadata = [
                {
                    'page': rec['page'],
                    'paragraph': rec['paragraph'],
                    'row': rec['row'],
                    'section': rec['section']  # INCLUDED HERE
                }
                for rec in chunk
            ]
            
            chunks.append({
                'page': page,
                'metadata': metadata,
                'text': combined_text
            })
    return chunks


def chunk_lang_records(records, chunk_size=5):
    """
    Group records into chunks of N records each, but only within the same 'page'.
    Returns a list of chunk dicts with section metadata.
    """
    chunks = []
    # 1) Group records by page
    records_by_page = defaultdict(list)
    for rec in records:
        records_by_page[rec['page']].append(rec)
    
    # 2) For each page, slice into chunks
    for page, recs in records_by_page.items():
        for i in range(0, len(recs), chunk_size):
            chunk = recs[i : i + chunk_size]
            combined_text = ' '.join(rec['raw'] for rec in chunk) 
            
            # Create metadata with section info
            metadata = [
                {
                    'page': rec['page'],
                    'paragraph': rec['paragraph'],
                    'row': rec['row'],
                    'section': rec['section']  # INCLUDED HERE
                }
                for rec in chunk
            ]
            
            chunks.append({
                'page': page,
                'metadata': metadata,
                'text': combined_text
            })
    return chunks