import os
import requests
from bs4 import BeautifulSoup

# URLs for each language corpus
languages = {
    "Greek": "https://archive.org/stream/bib_fict_4102600/bib_fict_4102600_djvu.txt",  # Hermetica in Greek
    "Hebrew": "https://he.wikisource.org/wiki/ספר_יצירה"  # Sefer Yetzirah (HTML)
}

root_dir = "data/reference_texts/alchemical_corpora/"
os.makedirs(root_dir, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0'}

for lang, url in languages.items():
    lang_dir = os.path.join(root_dir, lang)
    os.makedirs(lang_dir, exist_ok=True)
    file_path = os.path.join(lang_dir, f"{lang.lower()}_sample.txt")

    try:
        print(f"Downloading {lang} corpus from {url}…")
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Force UTF-8 decoding
        response.encoding = 'utf-8'

        # Decide whether to scrape HTML or take plain text
        if url.endswith(('.txt', '.completed')):
            # Direct plain-text download
            text = response.text

        else:
            # HTML scraping
            soup = BeautifulSoup(response.text, 'html.parser')

            if 'latinlibrary' in url:
                # The Latin Library uses a div.text wrapper
                text = soup.find('div', {'class': 'text'}).get_text(separator="\n", strip=True)

            elif 'wikisource' in url:
                # Wikisource: grab paragraphs and divs
                paras = []
                for el in soup.find_all(['p', 'div']):
                    txt = el.get_text(strip=True)
                    if txt:
                        paras.append(txt)
                text = "\n\n".join(paras)

            else:
                # Fallback: grab all visible text
                text = soup.get_text(separator="\n", strip=True)

        # Write out as UTF-8
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"✔ {lang} saved to {file_path}")

    except Exception as e:
        print(f"✖ Error downloading {lang}: {e}")
