import requests
import gzip
import io
import os

""" 
# Download the gzipped EVA transcription
url = "https://www.ic.unicamp.br/~stolfi/voynich/98-12-28-interln16e6/text16e6.evt.gz"
response = requests.get(url)
compressed_file = io.BytesIO(response.content)

# Extract and save the .evt file
with gzip.open(compressed_file, 'rt', encoding='latin1') as f:
    eva_content = f.read()
    
with open(r"data\raw\voynich_eva.txt", "w", encoding="utf-8") as f:
    f.write(eva_content)
"""
    


def download_and_extract_eva(
    url: str = "https://www.ic.unicamp.br/~stolfi/voynich/98-12-28-interln16e6/text16e6.evt.gz",
    output_path: str = "data/raw/voynich_eva.txt"
    ) -> str:
    """
    Downloads the gzipped EVA transcription of the Voynich manuscript,
    extracts the .evt file content, and saves it to the specified path.

    Parameters:
        url (str): URL to the .gz EVA transcription file.
        output_path (str): File path to save the decompressed text.

    Returns:
        str: The path to the saved file.
    """
    # Make sure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Download and decompress
    response = requests.get(url)
    compressed_file = io.BytesIO(response.content)

    with gzip.open(compressed_file, 'rt', encoding='latin1') as f:
        eva_content = f.read()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(eva_content)

    return output_path
