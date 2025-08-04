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
