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


def archive_python_files(
    source_folder: str = ".",
    output_folder: str = "archive/documentation",
    output_filename: str = "source_archive.jsonl",
    recursion: bool = False
):
    """
    Archives .py files from a folder into a JSONL file.

    Args:
        source_folder (str): Directory to search for .py files.
        output_folder (str): Destination directory for the .jsonl file.
        output_filename (str): Name of the output JSONL file.
        recursion (bool): Whether to recurse into subdirectories. Default is False.
    """
    os.makedirs(output_folder, exist_ok=True)
    archive = []

    if recursion:
        # Walk through all subdirectories
        for root, _, files in os.walk(source_folder):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        archive.append({
                            "file_name": os.path.relpath(file_path, start=source_folder),
                            "content": content
                        })
                    except Exception as e:
                        print(f"Failed to read {file_path}: {e}")
    else:
        # Only process files in the given folder
        for file in os.listdir(source_folder):
            if file.endswith(".py"):
                file_path = os.path.join(source_folder, file)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        archive.append({
                            "file_name": file,
                            "content": content
                        })
                    except Exception as e:
                        print(f"Failed to read {file_path}: {e}")

    output_path = os.path.join(output_folder, output_filename)
    try:
        with open(output_path, "w", encoding="utf-8") as out_file:
            for entry in archive:
                out_file.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"Archived {len(archive)} files to {output_path}")
    except Exception as e:
        print(f"Failed to write archive: {e}")


import os
import json
import openai

def analyze_python_functions_from_archive(
    archive_path: str = "archive/documentation/source_archive.jsonl",
    output_path: str = "archive/documentation/function_descriptions.json",
    model: str = "gpt-4",
    temperature: float = 0.3
):
    """
    Loads .py file contents from a JSONL archive, sends each to OpenAI,
    and writes a structured JSON output with per-function descriptions.

    Args:
        archive_path (str): Path to the .jsonl archive of source code.
        output_path (str): Output JSON file to save function descriptions.
        model (str): OpenAI model to use (e.g., "gpt-4").
        temperature (float): Temperature for model generation.
    """
    results = []
    
    with open(archive_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                item = json.loads(line)
                file_name = item.get("file_name")
                code = item.get("content", "")

                if not code.strip():
                    continue

                # Prepare messages
                messages = [
                    {"role": "system", "content": "You are an expert Python code analyst. Return output as structured JSON only."},
                    {"role": "user", "content": (
                        "Analyze the Python code below. Identify each function defined and return a JSON array of:\n"
                        "- function_name: the name of the function\n"
                        "- description: a short and clear description of what the function does\n\n"
                        f"Code:\n{code}"
                    )}
                ]

                # OpenAI call
                response = openai.client.responses.parse(
                    model=model,
                    messages=messages,
                    temperature=temperature
                )

                # Parse response
                content = response.choices[0].message.content.strip()
                try:
                    function_descriptions = json.loads(content)
                except json.JSONDecodeError:
                    print(f"⚠️ Failed to parse JSON response for file: {file_name}")
                    function_descriptions = []

                results.append({
                    "file_name": file_name,
                    "functions": function_descriptions
                })

            except Exception as e:
                print(f"❌ Error processing line: {e}")

    # Save final structured JSON
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(results, out_f, indent=2, ensure_ascii=False)
    
    print(f"✅ Function descriptions saved to {output_path}")
