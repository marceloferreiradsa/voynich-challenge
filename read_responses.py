from archive.external_api_functions import VoynichContextManager

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

# Show the last 5 responses
manager.show_responses(max_items=50)

#cost = manager.estimate_recursive_cost(rounds=3, output_multiplier=1.2)
#print(cost)

