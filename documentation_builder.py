import os
import json
from pydantic import BaseModel
from openai import OpenAI

# ──────────────────────────────────────────────────────────────────────────────
# 1) Define your Pydantic schemas

class FunctionDesc(BaseModel):
    function_name: str
    description: str

class FunctionsList(BaseModel):
    functions: list[FunctionDesc]


# ──────────────────────────────────────────────────────────────────────────────
# 2) The main analysis function

def analyze_python_functions_from_archive(
    archive_path: str = "archive/documentation/source_archive.jsonl",
    output_path: str = "archive/documentation/function_descriptions.json",
    model: str = "gpt-4o-2024-08-06",
    temperature: float = 0.0
):
    """
    Reads each .py entry from a JSONL archive and, for each file:
      1. Sends the code to the OpenAI Responses API with a structured prompt.
      2. Parses the model's reply into a FunctionsList Pydantic object.
      3. Writes out [{"file_name": ..., "functions": [...]}, ...] to JSON.
    """
    # Initialize the Responses client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    results = []

    with open(archive_path, "r", encoding="utf-8") as infile:
        for line in infile:
            entry     = json.loads(line)
            file_name = entry.get("file_name", "<unknown>")
            code      = entry.get("content", "").strip()
            if not code:
                continue

            # Build the user prompt
            prompt = (
                "You are an expert Python code analyst.\n"
                "Identify each function in the code below and return a JSON object with a single key "
                "`functions`, whose value is an array of objects each having:\n"
                "  - function_name (string)\n"
                "  - description   (string)\n\n"
                f"```python\n{code}\n```"
            )

            # Call the Responses API and parse directly into FunctionsList
            response = client.responses.parse(
                model=model,
                input=[{"role": "user", "content": prompt}],
                temperature=temperature,
                text_format=FunctionsList
            )

            parsed: FunctionsList = response.output_parsed
            results.append({
                "file_name": file_name,
                "functions": [f.dict() for f in parsed.functions]
            })

    # Write the combined output as JSON
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(results, out_f, indent=2, ensure_ascii=False)

    print(f"✅ Function descriptions saved to {output_path}")


# ──────────────────────────────────────────────────────────────────────────────
# 3) Optional CLI entry point

if __name__ == "__main__":
    # Example: override model via environment or command-line args if you like
    analyze_python_functions_from_archive()
