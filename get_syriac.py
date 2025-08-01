import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import unicodedata
import time

# Configuration
BASE_URL = "https://syriaccorpus.org/"
OUTPUT_DIR = r"data\reference_texts\alchemical_corpora\Syriac"
START_ID = 1
END_ID = 2
DELAY = 0.5   # seconds between requests to be polite

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Helpers
def slugify(text):
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode()
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s]+", "_", text)

pagebreak_re = re.compile(r'^\s*pb\.\s*\d+\s*$', re.IGNORECASE)
syr_char_re = re.compile(r'[\u0710-\u072F\u08A0-\u08FF]')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

for pid in range(START_ID, END_ID + 1):
    url = f"{BASE_URL}{pid}"
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
    except requests.HTTPError as e:
        print(f"[{pid}] Skipping (HTTP {e.response.status_code})")
        continue

    soup = BeautifulSoup(resp.text, "html.parser")

    # Extract English title
    title_el = soup.select_one("span.tei-title.title-analytic[lang='en']")
    if title_el:
        eng_title = title_el.get_text(separator=" ", strip=True).split(" - ")[0]
    else:
        print(f"[{pid}] No English title found, skipping")
        continue

    slug = slugify(eng_title)
    out_path = os.path.join(OUTPUT_DIR, f"{slug}.txt")

    # Extract Syriac body
    body = soup.select_one("div.mssBody div.tei-text div.body")
    if not body:
        print(f"[{pid}] No Syriac body found, skipping")
        continue

    runs = []
    for tag in body.select("[lang='syr']"):
        text = tag.get_text(strip=True)
        if pagebreak_re.match(text):
            continue
        if not syr_char_re.search(text):
            continue
        runs.append(text)

    if not runs:
        print(f"[{pid}] No Syriac runs extracted, skipping")
        continue

    full_text = "\n".join(runs)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"[{pid}] Saved: {out_path}")
    time.sleep(DELAY)
