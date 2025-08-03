import os
import json
from pathlib import Path
from typing import Any, Union
import openai

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




def render_functions_to_readme(
    json_path: str = "archive/documentation/function_descriptions.json",
    output_path: str = "README.md",
    readme_head_path: str = "archive/documentation/readme_head.md",
    project_title: str = "Function Documentation"
):
    """
    Reads a JSON file containing:
      [
        {
          "file_name": "foo.py",
          "functions": [
            {"function_name": "do_x", "description": "..."},
            ...
          ]
        },
        ...
      ]
    Also prepends the contents of a Markdown head section before appending function docs.

    The resulting README.md looks like:

    [readme_head.md content]

    # Project Title
    Description...
    ## foo.py
    ### do_x
    description...
    ...
    """
    # Load the structured JSON
    with open(json_path, "r", encoding="utf-8") as f:
        files_info = json.load(f)

    # Read optional README head content
    head_lines = []
    readme_head_path = Path(readme_head_path)
    if readme_head_path.exists():
        with readme_head_path.open("r", encoding="utf-8") as head_file:
            head_lines = head_file.read().splitlines()
        head_lines.append("\n---\n")  # Visual separator between head and auto-generated section

    # Start building function documentation content
    doc_lines = []
    doc_lines.append(f"# {project_title}\n")
    doc_lines.append("This document was auto-generated. It describes each Python function\n"
                     "found in the project’s source files, along with a brief summary.\n")

    for entry in files_info:
        file_name = entry.get("file_name", "unknown")
        functions = entry.get("functions", [])

        doc_lines.append(f"---\n")
        doc_lines.append(f"## `{file_name}`\n")
        if not functions:
            doc_lines.append("_No functions detected in this file._\n")
            continue

        for fn in functions:
            fn_name = fn.get("function_name", "<unnamed>")
            desc = fn.get("description", "").strip()
            doc_lines.append(f"### `{fn_name}`\n")
            doc_lines.append(f"{desc}\n")

    # Ensure output directory exists
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write everything to the README
    with open(output_path, "w", encoding="utf-8") as out:
        out.write("\n".join(head_lines + doc_lines))

    print(f"✅ README generated at {output_path}")
