# Multi-language survey extraction pipeline

## What this is for

Your survey's HTML file (`survey.html` / `ai_credit_survey_multilingual.html`)
already contains fully translated question text and answer options for all
6 languages, stored inside JavaScript data structures. This pipeline pulls
that data out and turns it into a clean Word document (or any other format
you want) **without a human — or an AI — ever reading and re-typing the
translated text.**

## Why this matters: the transcription error problem

If you (or I) manually opened the HTML file, read a Bengali question, and
typed it into a Word document, there's a real chance of small errors —
skipped characters, wrong diacritics, a word dropped. This is especially
risky for scripts neither of us reads fluently (Bengali, Vietnamese) — an
error would be invisible to a proofread but could confuse a respondent or
break comparability between language versions.

**The fix: never let a human or an AI transcribe the text. Let the real
JavaScript interpreter resolve it instead.**

The HTML file's translations aren't stored as ready-to-read text — they're
built by JavaScript logic (matching flat question indices to sections,
falling back to English where no translation exists, etc.). The only way to
get the *exact* text the live survey would actually show is to run that
logic for real. That's what Node.js does in Step 2: it executes the actual
code from the survey file and dumps the fully-resolved result as JSON. What
comes out is provably identical to what a respondent would see in their
browser — not a re-typed approximation of it.

Every step after that is pure data reshaping (matching arrays up correctly,
converting JSON to a different file format) — never re-reading or re-typing
the actual translated words.

## Requirements

- **Node.js** (any reasonably recent version — no extra packages needed for
  steps 1-3; step 4 needs the `docx` npm package, usually preinstalled)
- **Python 3**

## The pipeline, step by step

```
survey.html
    │
    ▼  (1_extract_blocks.py)
extract.js                  — raw JS blocks copied out, unmodified
    │
    ▼  (2_run_extraction.sh — runs `node extract.js`)
extracted_data.json         — the real, executed result: EQ + LANGS + qLabels
    │
    ▼  (3_reshape_data.py)
clean_survey_data.json      — one clean object per language, questions matched
    │                          to their translated text and options
    ▼  (3b_json_to_js_module.py)
survey_data_for_docx.js     — same data, reformatted for Node to `require()`
    │
    ▼  (4_build_docx.js — run with `node`)
Google_Forms_Build_Guide_All_Languages.docx
```

### Run it end to end

```bash
cd translation_pipeline

# Step 1: pull the three JS data blocks out of the HTML file
python3 1_extract_blocks.py ../survey.html extract.js

# Step 2: execute that JS for real, dump the resolved data as JSON
chmod +x 2_run_extraction.sh
./2_run_extraction.sh

# Step 3: reshape into one clean object per language
python3 3_reshape_data.py extracted_data.json clean_survey_data.json

# Step 3b: convert to a JS module the docx script can require()
python3 3b_json_to_js_module.py clean_survey_data.json survey_data_for_docx.js

# Step 4: generate the Word document
node 4_build_docx.js
```

Each step's output is a plain, inspectable file — open `extracted_data.json`
or `clean_survey_data.json` yourself at any point to spot-check the actual
text, if you want to verify anything by eye before it reaches the final
document.

## Reusing this later

If you ever edit `survey.html` — add a question, fix a translation, change
an option — just re-run all four steps in order. The whole pipeline takes a
few seconds and regenerates the Word document from whatever is currently in
the HTML file, so the build guide can never silently drift out of sync with
the real, live survey.

## Files in this folder

| File | What it does |
|---|---|
| `1_extract_blocks.py` | Pulls the 3 raw JS data blocks out of the HTML |
| `2_run_extraction.sh` | Runs that JS through Node, dumps resolved JSON |
| `3_reshape_data.py` | Matches translations to questions correctly |
| `3b_json_to_js_module.py` | Converts JSON to a `require()`-able JS file |
| `4_build_docx.js` | Builds the final Word document via the `docx` npm package |
