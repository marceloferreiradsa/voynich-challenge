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

#### Note: At the end my deadline I have only got to the point where the LLM indicate the possibility of the document be a Cypher. I was at risk of losing the deadline, so I decided to deliver the result before building the second stage of the project. The objective of it would be uncover meaning tackling the problem as a cypher not a language.

## For those who want to reproduce it

Start using the 'PipelineControl.ipynb' notebook as a guide of the steps and the auto-generated Function Documentation below.

In the folder 'service_containers' you find all needed files to build the embedding model container and the llm model container for local executions. I had a bad experience with it, but you can with careful tweaking achieve a better result. 

The idea in the beggining was to be able to compare the local LLM with Gemini or OpenAI models, but the hallucinations and incoherent responses have defeated me and I had to take a more pragmatic approach to be apple to complete the project in the deadline.

# My detailed path

## How should I start?

### Some details I have used in my first thoughts

- The Voynich Manuscript was rediscovered in 1912 but, according to studies, it was dated to roughly 1404.
- Although it is composed by unintelligible script, it contains illustrations that suggest it can be an alchemical document given the subjects it seems to address.
- The sometimes strage plants and images git to it an almost aneiric characteristic and seems to have instructions or recipes of some kind
- By the rules of the challenge I must use the Takahashi transcription, so I have to find the best source for it.
- Should I make local API call or call OpenAI and Gemini - or other - from the beginning? I wanted to make local APIs to make a better cost control and also be able to compare the performance of local models with the best models available.
- I also needed to decide if I would use local embeddings or external calls for embeddings. Or even if I would use embeddings at all. 
- I see many people focusing in the mistery of the Voynich and getting lost in the 'meaning of the mistery language'. But we do not know if it is a language at all. I need to start a process that can decide what is the best approach. Part of the work is to decide if the Voynich needs to be translated or deciphered. My approach must be linguistic at first, but not to prove that the Voynich is written in a forgotten misterious language, but to see if it is a language at all.

### A. How I decided to start

1. Given the brief characteristics listed above, I have decided to gather some foundational alchemical texts from XV century and before and figure out how to compare it to the document. Why?: This approach could extract from the document any similarity in grammar structure or even meanings - although I must keep in mind it is an unsolved mistery, so I must tackle it with care and some humbleness.
2. I decided to use local models to compare later with industry standard. 
3. I also decided to use local embeddings because the quality difference between it and the most advanced models would not mean much. I was also worried about cost, although embedding models are much cheaper I was trying to think as a company with billions of tokens to process.

### B. Starting out

1. I imported an interlinear version of the Voynich (by stolf, 1998) that has many diferent transcription versions, including the Takahashi.
2. I had to build a function to extract only the Takahashi
3. Then I've looked for other alchemical texts to compare - which I refer in the project as 'reference languages'. I have researched what languages alchemists used, and I got the initial list: latin, greek, coptic, syriac, hebrew and arabic. I have spent quite sometime in this phase, so when I got greek, coptic, syriac and hebrew I've decided to speed up the process so that I could meet the deadline. 
4. After selecting languages and alchemical texts, I've built functions to import and save the texts in chunks into json and jsonl files to make it easier when I had to work with them
5. Then I've built two local models: an embedding model using 'all-mpnet-base-v2'; and one LLM model. I have used containers to be able to run the models locally without messing up with my local computer configurations and also improve software compatibility and reproducibility.
6. I have built functions to clean and embed all texts, Voynich and the reference languages

### C. First analysis

1. I've made a plot only for the Voynich chunks so that I could see the inner similarity of the language. This analysis was very interesting because we can see that the Herbal Sections have the best inner similarity with almost all their chunks embeddings being plot in the same space. 
2. Because of that I've decided to plot a heat map showing the similarities between different sections in the Voynich. This confirmed the first plot indicating that Herbal Section is the most internally coherent text.
3. I also decided to plot using PCA and later use euclidean and cosine distances for the embedded chunks of texts so that I could measure what language had the most similarity. This step is good so that we can decide if we want to keep all languages in the study, or eliminate part of them. Eliminating some we can reduce the number of tokens therefore focusing the study in the more promissing languages and, therefore, reducing costs.
4. From the start Hebrew and Greek showed more similarity, but depending on the algorithm coptic chunks also showed some similarity. 
5. Coptic is an intermediary egyptian language. It was used by egyptians when they abandoned hyerogryphs and before modern egyptian languages. I was extensively used by alchemists. So I have decided to keep it.
6. Syriac was the most different and distant. It seems to be bed, but since it was the biggest corpus I had I decided to keep it because the less similarity it had with the Voynich could be valuable to help the model understand what made the other languages more similar. It is called 'contrastive analysis' and is used in language studies
7. Then I came the time to test my local LLM. This was the most frustrating moment of my study. My local LLM - as I've said above - hasn's worked very well. I do not know if I could setup it better, but sinde I've spent some hours in this and couldn't make it improve, I've decided to abandon it. I had to be pragmatic.


### D. First ideas

1. Herbal secion is the more internally coherent. Since its symbols and 'words' are very much linked to itself, it indicates that they were not chosen by chance. They are there for one reason. Who has written them thought they should be used together in the section. As when we write a python book it will have a given pythonic syntax, or when we write about cats it will have a given vocabulary with internal logic.
2. Other sections are more entangled, but many of them we can see similarities. Astrological, Stars and Zodiac sections are entangled and even not knowing what is written, we can understand why they could be similar. Astronomy and Astrology as two very distincts objects, but both talk about stars, planets and their positions.
3. I must build prompts that helps the LLM to extract this similarities and keeps this organization in the requests. I must inform what section it is from and I'should keep the structure of chunks so that I can keep small groupings the get insights for more focused parts of the document.


### E. Calling the external LLM

1. I was worried about cost, so I've built a module to simulate the cost of the calling. It counted tokens and applied a simple formula to calculate the input cost. It also simulated an output cost but expecting the worst scenario, a long 5k+ token response.
2. I've built a call function what gathered the processed texts and the voynich, the embeddings and classified it by similarity and used it for the calls.
3. I've also build a 'recursive call' function that would make N rounds of recursive calls to the LLM: it would take a selected number of responses from the LLM and send it back asking the LLM to analyse the earlier answers and refine hypothesis.


### F. Hypothesis and Justification

In approaching the Voynich manuscript, I prioritized structural and statistical analysis over speculative translation. Based on embedding comparisons, token morphology, and delimiter patterns, I hypothesize that the text represents a constructed or ciphered symbolic system, not a natural language with direct lexical equivalents.

The manuscript exhibits strong internal regularity: tokens are modular and often consist of identifiable roots, prefixes, and suffixes. Common suffixes such as -aiin, -ol, and -in, and recurrent prefixes like ke-, cho-, and pch- suggest a system of agglutination or inflection. The consistent use of a final delimiter (=) across tokens implies a structural function—possibly delimiting semantic or syntactic units, akin to labels or section markers.

Embedding analyses show no direct lexical matches with Syriac, Coptic, Greek, or Hebrew, although phonotactic - the EVA alphabet was designed to preserve those patterns (e.g., vowel-consonant sequences) -  and structural echoes suggest influence rather than equivalence. This reinforces the hypothesis that the manuscript encodes meaning through symbolic or cipher-like conventions rather than using natural language words.

For this reason, I did not attempt a literal translation. To do so without evidence of lexical mapping or a deciphered key would risk producing misleading or arbitrary results. Instead, my approach aims to model the internal logic of the writing system and identify features (e.g., token structure, affix function, delimiter roles) that could inform future decipherment efforts.

By framing the text as a self-contained symbolic system, this analysis opens a path for interpreting function and structure, even in the absence of traditional translation. The next steps would involve testing hypotheses about affix roles, examining structural repetition, and exploring alignment between text regions and manuscript illustrations.


### G. Example of output from the LLM after recursive analysis

#### Response structure:

```json
{
  "summary_hypothesis": "The Voynich manuscript employs a highly structured, modular writing system in which tokens are constructed from roots, prefixes, and suffixes, frequently terminated by a distinctive delimiter (most often '='). These tokens serve as grammatical or structural units—such as headers, labels, or inflected words—rather than direct lexical items from known languages. Recurring suffixes (e.g., '-aiin', '-y', '-ol', '-in') and initial clusters/prefixes (e.g., 'ke-', 'cho-', 'pch-') indicate a system of agglutination or inflection, encoding grammatical or semantic roles such as case, number, or category. The delimiter '=' consistently marks the end of a token, functioning as a section or field boundary, analogous to a header or label in structured data, and is not used as an internal separator. Statistical and embedding analyses show fluctuating similarity to Syriac, Coptic, and Greek, but the lack of direct lexical matches and the unique structural logic suggest the system is a constructed or ciphered language, possibly inspired by these scripts but with its own internal grammar and symbolic conventions.",
  "key_patterns": [
    "Tokens are typically 6-8 characters long, composed of a root, optional prefixes and/or suffixes, and sometimes end with a delimiter ('=').",
    "Frequent recurring suffixes such as '-aiin', '-y', '-ol', and '-in' are observed, likely serving as grammatical or morphological markers.",
    "Initial clusters or prefixes (e.g., 'ke-', 'cho-', 'pch-', 'qof-') are common and may denote grammatical class, category, or thematic role.",
    "The delimiter '=' is consistently used at the end of tokens, functioning as a strong boundary or section/header marker, not as an internal separator.",
    "Internal delimiters (e.g., '!', '-') and repeated characters (e.g., 'eee', 'ii') occasionally appear, possibly indicating compounds, emphasis, or continuation.",
    "Tokens do not directly match words in Syriac, Hebrew, Greek, or Coptic, supporting the idea of a unique, constructed, or ciphered system.",
    "Tokens with '=' often appear at the start of sections or before blocks of content, reinforcing their role as structural markers.",
    "Phonotactic patterns include consonant-vowel alternation and open syllables, reminiscent of Coptic/Greek, while morphological repetition echoes Semitic systems."
  ],
  "possible_language_influences": ["Syriac", "Coptic", "Greek", "Hebrew"],
  "conclusion_type": "constructed_language",
  "open_questions": [
    "What specific grammatical or semantic roles do the recurring suffixes and prefixes encode?",
    "Is the '=' delimiter always a section/header marker, or does it serve additional syntactic or semantic functions?",
    "Can the internal delimiters ('!', '-') and repeated characters be systematically mapped to known grammatical or structural features?",
    "Is there an underlying natural language being encoded, or is the entire system a cipher or an artificial/constructed language?",
    "How are token boundaries and hierarchical structure determined in longer passages without explicit delimiters?",
    "What is the relationship between the observed statistical patterns and the actual content or meaning of the manuscript?"
  ]
}
```


---

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
