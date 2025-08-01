import json
import os
import random
from pathlib import Path
import openai
import tiktoken

# Ensure your OpenAI key is set in the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Helper to render GPT prompt
def render_template(context: dict, section_text: str, format_instructions: str) -> str:
    context_yaml = json.dumps(context, ensure_ascii=False, indent=2)
    return f"""
You are an expert in the structural and statistical analysis of undeciphered scripts.

The following transcriptions are not real words; they are arbitrary Latin letters representing unknown symbols.
Analyze structural patterns, not linguistic meanings.

### CONTEXT:
{context_yaml}

### VOYNICH MANUSCRIPT SECTION (TRANSCRIBED TOKENS):
{section_text}

### FORMAT_INSTRUCTIONS:
{format_instructions}
"""

class VoynichContextManager:
    def __init__(
        self,
        embeddings_path: str,
        reference_paths: dict,
        processed_path: str = "processed_sections.json",
        responses_path: str = "responses.jsonl"
    ):
        self.embeddings_path = Path(embeddings_path)
        self.reference_paths = {lang: Path(p) for lang, p in reference_paths.items()}
        self.processed_path = Path(processed_path)
        self.responses_path = Path(responses_path)
        self.embeddings = self._load_jsonl(self.embeddings_path)
        self.references = self._load_references(self.reference_paths)
        self.processed = self._load_processed()

    def _load_jsonl(self, path: Path) -> list:
        with open(path, 'r', encoding='utf-8') as f:
            return [json.loads(line) for line in f]

    def _load_references(self, paths: dict) -> dict:
        refs = {}
        for lang, p in paths.items():
            with open(p, 'r', encoding='utf-8') as f:
                chunk = json.loads(f.readline())
                refs[lang] = chunk.get('text', '')[:200]
        return refs

    def _load_processed(self) -> set:
        if self.processed_path.exists():
            with open(self.processed_path, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        return set()

    def _save_processed(self):
        with open(self.processed_path, 'w', encoding='utf-8') as f:
            json.dump(list(self.processed), f, indent=2)

    def choose_sections(self, N: int, include_processed: bool) -> list:
        all_ids = [f"{rec['page']}::{rec['paragraph']}" for rec in self.embeddings]
        pool = all_ids if include_processed else [sid for sid in all_ids if sid not in self.processed]
        if len(pool) < N:
            raise ValueError(f"Not enough sections available ({len(pool)}) for selection of {N} sections.")
        return random.sample(pool, N)

    def build_payloads(self, selected_ids: list, format_instructions: str) -> list:
        payloads = []
        for sid in selected_ids:
            page, para = sid.split("::")
            rec = next(r for r in self.embeddings if r['page'] == page and r['paragraph'] == para)
            scores = {lang: round(random.random(), 4) for lang in self.references.keys()}
            context = {
                "A. Embedding Similarity Metrics": scores,
                "B. Reference Language Excerpts": self.references,
                "C. Structural Notes": [
                    f"Tokens: {rec['tokens'][:10]}",
                    f"Raw excerpt: {rec['raw'][:50]}..."
                ]
            }
            prompt = render_template(context, rec['raw'], format_instructions)
            payloads.append({"id": sid, "prompt": prompt})
            self.processed.add(sid)
        self._save_processed()
        return payloads

    def call_openai(self, prompt: str, model: str = "gpt-4.1-turbo", temperature: float = 0.0) -> dict:
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        content = response.choices[0].message.content
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            result = {"raw_response": content}
        with open(self.responses_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"prompt": prompt, "response": result}, ensure_ascii=False) + "\n")
        return result

    def show_responses(self, max_items: int = 5):
        if not self.responses_path.exists():
            print("No responses found.")
            return
        with open(self.responses_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"\nShowing {min(max_items, len(lines))} most recent responses:\n" + "-" * 60)
        for i, line in enumerate(reversed(lines[-max_items:]), 1):
            try:
                entry = json.loads(line)
                print(f"\n=== Response #{i} ===")
                print("Prompt (preview):", entry['prompt'][:200].replace("\n", " "), "...")
                print("Response:")
                resp = entry["response"]
                if isinstance(resp, dict):
                    for k, v in resp.items():
                        print(f"  {k}: {v}")
                else:
                    print(resp)
            except json.JSONDecodeError:
                print(f"[Error decoding response #{i}]")

    def estimate_recursive_cost(
        self,
        responses_path: str = None,
        rounds: int = 3,
        model: str = "gpt-4.1-turbo",
        output_multiplier: float = 1.0
    ) -> dict:
        path = Path(responses_path or self.responses_path)
        if not path.exists():
            raise FileNotFoundError(f"{path} not found.")
        with open(path, 'r', encoding='utf-8') as f:
            data = [json.loads(line)["response"] for line in f if line.strip()]
        summary = json.dumps(data, ensure_ascii=False)
        prompt = f"Summary of analyses:\n{summary}\nTask: refine the hypothesis."  
        try:
            enc = tiktoken.encoding_for_model(model)
        except KeyError:
            enc = tiktoken.get_encoding("cl100k_base")
        input_tokens = len(enc.encode(prompt))
        output_tokens = int(input_tokens * output_multiplier)
        total_tokens = rounds * (input_tokens + output_tokens)
        return {
            "rounds": rounds,
            "input_tokens_per_round": input_tokens,
            "estimated_output_tokens_per_round": output_tokens,
            "total_tokens": total_tokens
        }

    def recursive_voynich_refinement(
        self,
        rounds: int = 3,
        model: str = "gpt-4.1",
        temp: float = 0.3,
        max_summary_chars: int = 10000
    ) -> str:
        """
        Performs recursive refinement over saved responses.
        Each round reads all responses, aggregates, and appends a new synthesis.
        Returns the final synthesis string.
        """
        final_summary = ""
        for i in range(rounds):
            with open(self.responses_path, 'r', encoding='utf-8') as f:
                analyses = [json.loads(line)["response"] for line in f if "response" in json.loads(line)]
            summary = json.dumps(analyses, ensure_ascii=False)[:max_summary_chars]
            prompt = f"""
                You are refining your understanding of the structure and function of tokens in the Voynich manuscript.

                Previous hypotheses and analyses:
                {summary}

                TASK:
                - Reflect on these hypotheses.
                - Identify patterns, contradictions, or recurring structural cues.
                - Propose a unified theory about the grammar or symbolic logic of these tokens.
                - Include possible token roles (prefixes, suffixes, delimiters), grammatical markers, or positional patterns.
                - Output in JSON with fields: \"updated_hypothesis\", \"evidence_summary\", and \"confidence\".
                """
            print(f"\n=== RECURSIVE ROUND {i+1} ===")
            response = openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temp
            )
            content = response.choices[0].message.content
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                result = {"raw_response": content}
            with open(self.responses_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"prompt": prompt, "response": result}, ensure_ascii=False) + "\n")
            final_summary = content
        return final_summary
