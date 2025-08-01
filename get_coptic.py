import os
import time
from urllib.parse import urlparse, urljoin

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def download_coptic_texts(start_urls, base_dir="data/reference_texts/alchemical_corpora/Coptic"):
    """
    Downloads normalized Coptic texts from the list of start URLs.
    
    Args:
        start_urls (list of str): List of collection URLs to crawl.
        base_dir (str): Directory where the output .txt files will be stored.
    """
    os.makedirs(base_dir, exist_ok=True)

    # Setup headless Chrome
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    try:
        for start_url in start_urls:
            print(f"\nProcessing: {start_url}")
            driver.get(start_url)
            time.sleep(2)

            # Gather all normalized links on the page
            links = driver.find_elements(By.CSS_SELECTOR, "a.text-item.norm")
            normalized_links = [link.get_attribute('href') for link in links]
            print(f"Found {len(normalized_links)} normalized pages.")

            # Download and save each normalized page
            for href in normalized_links:
                url = urljoin(start_url, href)
                print("→", url)
                driver.get(url)
                time.sleep(1)

                try:
                    container = driver.find_element(By.CSS_SELECTOR, "section#text")
                    visible_text = container.text

                    parts = urlparse(href).path.strip("/").split("/")
                    stem = "-".join(parts[-2:])
                    fn = f"{stem}.txt"
                    out_path = os.path.join(base_dir, fn)

                    with open(out_path, "w", encoding="utf-8") as f:
                        f.write(visible_text)

                    print("   saved →", out_path)
                except Exception as e:
                    print("   FAILED:", e)
    finally:
        driver.quit()
