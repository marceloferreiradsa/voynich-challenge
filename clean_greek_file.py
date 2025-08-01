import os
import re
from bs4 import BeautifulSoup

# Paths
input_path = "data/reference_texts/alchemical_corpora/Greek/Hermetica.txt"
output_folder = "data/reference_texts/alchemical_corpora/Greek/language_processed"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Read and parse HTML
with open(input_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')
pre_tag = soup.find('pre')

if pre_tag:
    # Extract text from <pre>
    raw_text = pre_tag.get_text()

    # Normalize line endings
    lines = raw_text.splitlines()

    # Remove leading/trailing whitespace from each line
    lines = [line.rstrip() for line in lines]

    # Replace blocks of 15 or more blank lines with a marker
    processed_lines = []
    blank_count = 0
    for line in lines:
        if line.strip() == "":
            blank_count += 1
        else:
            if blank_count >= 15:
                processed_lines.append("===BREAK===")
            elif blank_count > 0:
                processed_lines.extend([""] * blank_count)
            blank_count = 0
            processed_lines.append(line)

    # Handle any remaining blank lines at end
    if blank_count >= 15:
        processed_lines.append("===BREAK===")
    elif blank_count > 0:
        processed_lines.extend([""] * blank_count)

    # Prepare output file path
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_folder, f"{base_name}_clean.txt")

    # Save processed file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(processed_lines))

    print(f"Processed file saved to: {output_path}")
else:
    print("No <pre> tag found in the input file.")
