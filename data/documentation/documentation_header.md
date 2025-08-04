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
