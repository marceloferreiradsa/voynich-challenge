from external_api_functions_new import VoynichContextManager
import json

# Match these paths to your setup
reference_paths = {
    'Greek':  'data/reference_texts/alchemical_corpora/Greek/language_processed/Hermetica_20250727T161004Z.jsonl',
    'Hebrew': 'data/reference_texts/alchemical_corpora/Hebrew/language_processed/SeferYetzira_20250727T161004Z.jsonl',
    'Coptic': 'data/reference_texts/alchemical_corpora/Coptic/language_processed/coptic_chunks_20250727T161001Z.jsonl',
    'Syriac': 'data/reference_texts/alchemical_corpora/Syriac/language_processed/syriac_corpus_20250727T161033Z.jsonl'
}

manager = VoynichContextManager(
    embeddings_path="data/embeddings/voynich_records_with_embeddings_20250727T125656Z.jsonl",
    reference_paths=reference_paths,
    processed_path="processed_sections.json",
    responses_path="responses.jsonl"
)

with open("responses.jsonl", "r", encoding="utf-8") as f:
    all_analyses = [json.loads(line)["response"] for line in f]

final_result = manager.recursive_voynich_refinement(rounds=3)

