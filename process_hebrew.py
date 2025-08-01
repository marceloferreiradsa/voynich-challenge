from chunk_texts import chunk_txt_to_jsonl


chunk_txt_to_jsonl(r"data\reference_texts\alchemical_corpora\Hebrew\SeferYetzira.txt",
                   r"data\reference_texts\alchemical_corpora\Hebrew\language_processed\SeferYetzira.jsonl",
                   "Hebrew",
                   25)