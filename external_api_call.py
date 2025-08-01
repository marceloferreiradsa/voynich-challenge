from external_api_functions import VoynichContextManager
import json

# Initialize with your file paths
env_paths = {
    'Greek':  'data/reference_texts/alchemical_corpora/Greek/language_processed/Hermetica_20250727T161004Z.jsonl',
    'Hebrew': 'data/reference_texts/alchemical_corpora/Hebrew/language_processed/SeferYetzira_20250727T161004Z.jsonl',
    'Coptic': 'data/reference_texts/alchemical_corpora/Coptic/language_processed/coptic_chunks_20250727T161001Z.jsonl',
    'Syriac': 'data/reference_texts/alchemical_corpora/Syriac/language_processed/syriac_corpus_20250727T161033Z.jsonl'
}

manager = VoynichContextManager(
    embeddings_path="data/embeddings/voynich_records_with_embeddings_20250727T125656Z.jsonl",
    reference_paths=env_paths,
    processed_path="processed_sections.json"
)

# User parameters

N = int(input("How many sections to select? "))
include_processed = input("Include already-processed? (y/N) ").lower().startswith("y")


#N = 3  # number of sections to analyze
#include_processed = False  # or True
format_instr = (
    "Please return a JSON object with the following keys:\n"
    "- 'token_structure_analysis': observations on structural patterns in tokens "
    "(e.g. prefix/suffix/delimiter organization, character clustering)\n"
    "- 'possible_function': what functional or grammatical role these patterns may play "
    "(e.g. sentence marker, label, connector, emphasis)\n"
    "- 'delimiter_notes': any structural implications of symbols like '=', '-', or repeated characters\n"
    "- 'confidence': a float between 0 and 1 indicating your confidence in the analysis\n\n"
    "Avoid linguistic translations or semantic analogies to known languages unless explicitly structural."
)

# Select sections and build prompts
section_ids = manager.choose_sections(N, include_processed)
payloads = manager.build_payloads(section_ids, format_instr)

# Call GPT for each
for p in payloads:
    print(f"Analyzing section {p['id']}")
    result = manager.call_openai(p['prompt'], model="gpt-4.1")
    print(json.dumps(result, indent=2, ensure_ascii=False))
