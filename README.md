# The challenge

## Description

### Tasks:

Build a pipeline that ingests transcribed Voynich text (EVA or Takahashi transcription)
Use LLMs, embeddings, or custom models to find patterns, possible meanings, or linguistic structures
Try to match parts of the text with known languages, glyph frequencies, or hypothesized semantics
Input: Transcription file (e.g., voynich_eva.txt), Optional: XML or images from the Beinecke Library

### Output Example:

{ "section": "Herbal A", "hypothesis": "This section might describe plant properties using a symbolic language.", "translation_attempt": { "line_1": "otedy qokeedy qokedy", "meaning": "plant root soak boil" } }

#### Requirements:
Use AI reasoning to explore unknown language or construct hypotheses
Provide clear logs of your process
Explain why you believe your approach may uncover meaning

#### Bonus Features:
Visual overlay of decoded terms on manuscript images
Model fine-tuned on similar ciphered texts
Timeline of symbol usage evolution across manuscript pages


# The Solution Project

My intented approach to the solution primarily targets to find the right path for a solution, therefore
I'm not going to find meaning directly in the first place, I want to find out first what is propably the
most adequate way of tackling the Voynich mistery in the first place. I explain.

Most people already starts to tackle the problem being certain that it is a misterious language. Artificial or not, but a language. Like elfic from Tolkien. But even this initial supposition should be challenged, because the wrong approach could lead to the wrong solutions, or even increase the hypothesis of the document being just an ellaborate fraud.

## Why my approach may uncover meaning

I believe that we have two possibilities here: or the document has some meaningful content in its writings, or not. And if it has indeed any meaningful content it can be a forgotten language, or an artificial language that follows known languages instructures, or a cypher that can with the right inner rules, apparently contradict language structure rules.

Therefore, I believe my carefull approach to be able to first indicate the right path - analyse it as a language or a cypher - and then we'll be able to uncover the meaning tackling the problem with the right tools.

#### Note: At the end my deadline I have only got to the point where the LLM indicate the possibility of the document be a Cypher. I was at risk of losing the deadline, so I decided to deliver the result before building its second stage of the project. The objective of it would be uncover meaning tackling the problem as a cypher not a language.

## For those who want to reproduce it

Start using the 'PipelineControl.ipynb' notebook as a guide of the steps and the auto-generated Function Documentation below.

In the folder 'service_containers' you find all needed files to build the embedding model container and the llm model container for local executions. I had a bad experience with it, but you can with careful tweaking achieve a better result. 

The idea in the beggining was to be able to compare the local LLM with Gemini or OpenAI models, but the hallucinations and incoherent responses have defeated me and I had to take a more pragmatic approach to be apple to complete the project in the deadline.


# Function Documentation

This document was auto-generated. It describes each Python function
found in the project’s source files, along with a brief summary.

---

## `build_language_json_chunks.py`

### `jsonl_to_chunked_json`

Converts a .jsonl file into a structured JSON file by chunking records into groups of a specified size and splitting large text fields into subchunks if they exceed a maximum character limit. The function also adds metadata for each chunk and writes the output to a specified file.

---

## `chunk_texts.py`

### `chunk_txt_to_jsonl`

Splits a .txt file into a .jsonl file, where each line is a JSON object containing a chunk of text (with a specified number of lines), a language label, and a source identifier. The function reads the input text file, divides it into chunks, and writes each chunk as a JSON object to the output .jsonl file.

### `jsonl_to_chunked_json`

Converts a .jsonl file (where each line is a JSON object with text and metadata) into a structured JSON file. It groups records into chunks of a specified size, and if any text exceeds a maximum character limit, it splits it into subchunks. The output is a list of objects, each containing metadata and concatenated text, saved as a JSON file.

---

## `clean_greek_file.py`

_No functions detected in this file._

---

## `embed_client.py`

### `__init__`

Initializes an EmbedderClient instance with the specified embedding service endpoint and request timeout.

### `embed_texts`

Sends a list of text strings to the embedding service and returns their embedding vectors as lists of floats.

---

## `embed_save.py`

### `save_records_with_embeddings`

Saves a list of record dictionaries (each containing 'metadata', 'text', and 'embedding') to a JSONL file in the specified output directory. The output filename includes a UTC timestamp. Ensures the output directory exists, writes each record as a JSON line, and prints a summary message.

---

## `external_api_call.py`

### `choose_sections`

Selects a specified number of section IDs from the dataset, optionally including already-processed sections based on the user's choice.

### `build_payloads`

Constructs prompt payloads for each selected section, incorporating a formatting instruction for downstream analysis.

### `call_openai`

Sends a prompt to the OpenAI API (or similar LLM service) using a specified model and returns the model's response.

---

## `external_api_functions.py`

### `render_template`

Renders a prompt for GPT by formatting the context, section text, and format instructions into a structured string for analysis of undeciphered scripts.

### `__init__`

Initializes the VoynichContextManager object, loading embeddings, reference texts, and processed section IDs from files.

### `_load_jsonl`

Loads a JSONL (JSON Lines) file from the given path and returns a list of parsed JSON objects.

### `_load_references`

Loads reference language excerpts from provided file paths, extracting the first 200 characters of the 'text' field for each language.

### `_load_processed`

Loads the set of already processed section IDs from a JSON file, or returns an empty set if the file does not exist.

### `_save_processed`

Saves the current set of processed section IDs to a JSON file.

### `choose_sections`

Randomly selects N section IDs from all available or unprocessed sections, depending on the include_processed flag.

### `build_payloads`

Builds a list of payloads for selected section IDs, each containing a prompt for GPT and updates the processed set.

### `call_openai`

Sends a prompt to the OpenAI API, saves the prompt and response to a file, and returns the parsed response as a dictionary.

### `show_responses`

Displays up to max_items most recent responses from the responses file, printing both the prompt and the response content.

### `estimate_recursive_cost`

Estimates the total token cost for running recursive refinement rounds over the saved responses, based on model and output multiplier.

### `recursive_voynich_refinement`

Performs multiple rounds of recursive synthesis over saved responses, each time aggregating and refining hypotheses, and appends new syntheses to the responses file.

### `_load_all_responses`

Reads all lines from the responses file and returns a list of the 'response' objects from each entry.

### `summarize_all_responses`

Sends all raw responses to the LLM and requests a cohesive summary, returning the parsed JSON output or raw content on error.

---

## `folder.py`

_No functions detected in this file._

---

## `get_coptic.py`

### `download_coptic_texts`

Downloads normalized Coptic texts from a list of collection URLs using Selenium, and saves each text as a .txt file in the specified directory. It navigates through each start URL, finds all normalized text links, visits each, extracts the visible text, and writes it to disk.

---

## `get_greek_and_hebrew.py`

_No functions detected in this file._

---

## `get_syriac.py`

### `slugify`

Converts a given text string into a URL- and filename-safe slug by normalizing Unicode characters, removing non-alphanumeric characters, converting to lowercase, and replacing whitespace with underscores.

---

## `helper_functions.py`

### `load_embeddings`

Loads embedding records from a JSONL file at the given path. Returns a list of parsed JSON objects, printing errors if the file is missing or contains invalid JSON.

### `extract_section`

Extracts the most common 'section' value from a list of metadata dictionaries. Returns 'Unknown' if no valid section is found.

### `clean_labels`

Cleans a list of label strings, mapping digit labels to zodiac names, stripping whitespace, and replacing invalid entries with 'Unknown'.

### `annotate_group`

Annotates a matplotlib axis with the group label and symbol at the mean position of all points with that label. Returns the center position or None if no points are found.

### `report_dist`

Computes and prints the cosine distance between the embeddings of two labels, using their first occurrence in the cleaned_labels list.

---

## `ingest_voynich.py`

### `download_and_extract_eva`

Downloads the gzipped EVA transcription of the Voynich manuscript from a specified URL, extracts the .evt file content, and saves it as a UTF-8 text file to the given output path. Returns the path to the saved file.

---

## `local_llm_call.py`

### `llm_call_old`

Sends a prompt to a local LLM API endpoint, prints the generated response and timing, and returns the length of the response string. Returns 0 on error.

### `llm_call`

Sends a prompt to a local LLM API endpoint, prints the generated response and timing, and returns the response string. Returns an empty string on error.

### `save_llm_response`

Saves an LLM response and its metadata to a file in a specified output folder. Supports saving as either a .jsonl (one record per line) or .json file. Returns the file path.

### `append_llm_response`

Appends an LLM response and its metadata as a new line to a .jsonl file in a specified output folder. Returns the file path.

### `print_gpu_report`

Fetches and prints the current GPU status from a local API endpoint, including device info, CUDA version, memory usage, and nvidia-smi statistics if available.

---

## `pre_processing.py`

### `preprocess_takahashi`

Parses a Takahashi transcription file and extracts records for a given transcriber. It returns a list of dictionaries containing metadata (such as page, paragraph, row, transcriber, section) and cleaned text tokens. The function also maps folios to section names using metadata found in the file.

### `chunk_records`

Groups a list of record dictionaries into chunks of a specified size, but only within the same 'page'. Each chunk is a dictionary containing the page, metadata for each record in the chunk, and the combined text of the chunk.

### `chunk_lang_records`

Groups a list of record dictionaries into chunks of a specified size, but only within the same 'page'. Each chunk is a dictionary containing the page, metadata for each record in the chunk, and the combined text of the chunk. This function is functionally identical to chunk_records.

---

## `process_coptic.py`

### `extract_between_markers`

Returns the lines found between the specified start_marker and end_marker in a list of lines. If the markers are not found, returns None.

### `process_file_old`

Reads a file, extracts the lines between 'Normalized Text' and 'ANNIS Metadata' markers, and returns a dictionary with language, source, and text fields. Returns None if markers are not found.

### `process_file`

Reads a file, extracts the lines between 'Normalized Text' and 'ANNIS Metadata' markers (or the whole file if markers are not found), and returns a dictionary with language, source, and text fields.

### `main`

Finds all .txt files in the input directory, processes each file to extract Coptic text, and writes the results as JSON lines to the output file. Prints progress and summary information.

---

## `process_greek.py`

_No functions detected in this file._

---

## `process_hebrew.py`

### `chunk_txt_to_jsonl`

Reads a text file, splits it into chunks (likely of a specified size), processes it for a given language, and writes the result to a JSONL file. The function is imported from the chunk_texts module and is used here to process a Hebrew text file into a chunked JSONL format.

---

## `process_syriac.py`

### `extract_between_markers`

Returns the lines found between the specified start_marker and end_marker in a list of lines. If the markers are not found, returns None.

### `process_file_old`

Reads a file, extracts the lines between 'Normalized Text' and 'ANNIS Metadata' markers, and returns a dictionary with language, source, and text fields. Returns None if the markers are not found.

### `process_file`

Reads a file, extracts the lines between 'Normalized Text' and 'ANNIS Metadata' markers, and returns a dictionary with language, source, and text fields. If the markers are not found, uses the entire file as the text.

### `main`

Finds all .txt files in the input directory, processes each file to extract text, and writes the results as JSON lines to the output file. Prints progress and summary information.

---

## `read_responses.py`

### `show_responses`

Displays the last N responses stored by the VoynichContextManager. The number of responses shown is controlled by the max_items parameter.

### `estimate_recursive_cost`

Estimates the computational or financial cost of running recursive operations within the VoynichContextManager. The cost is calculated based on the number of rounds and an output multiplier.

---

## `recursive_call.py`

### `recursive_voynich_refinement`

Performs a multi-round refinement process on Voynich manuscript data, likely using embeddings and reference texts, to iteratively improve or analyze the data. The number of refinement rounds is specified by the 'rounds' parameter.

---

## `render_to_docx.py`

### `render_summary_to_docx_old`

Renders a summary dictionary (with specific keys like 'summary_hypothesis', 'key_patterns', etc.) into a structured .docx file, using headings and bullet/numbered lists for different sections. Saves the document to the specified output path.

### `render_dict_to_docx`

Renders any nested dictionary into a structured .docx file, using dictionary keys as headings and recursively formatting lists and sub-dictionaries. Saves the document to the specified output path.

### `render_section`

A nested helper function inside render_dict_to_docx that recursively renders content (dict, list, or primitive types) into the .docx document, using appropriate heading levels and list styles.

---

## `start_embedding_container.py`

_No functions detected in this file._

---

## `start_llm_container.py`

_No functions detected in this file._

---

## `utilities.py`

### `build_folder_tree_dict`

Recursively builds a dictionary representing the folder structure starting from the given base path, skipping folders that start with '_' or '.'.

### `load_language_embeddings`

Loads records from a JSONL file at the specified path, handling JSON parsing errors and file not found errors, and returns a list of parsed records.

### `archive_python_files`

Archives all .py files from a source folder (optionally recursively) into a JSONL file in the specified output folder, with error handling for file reading and writing.
