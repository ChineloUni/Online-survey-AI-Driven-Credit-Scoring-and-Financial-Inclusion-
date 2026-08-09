"""
Step 3 — Reshape the raw extracted data into one clean, uniform structure.

The raw extraction has three separate pieces (EQ, LANGS, qLabels) that need
to be lined up correctly: qLabels is a flat list of 32 translated questions
per language, indexed 0-31 across all six sections, and has to be matched
back to the right section/question using running counts. LANGS.opts is
nested by section then by question, with `null` for questions that don't
have multiple-choice options (scale and text questions).

This script does that lineup ONCE, in code, and writes out one JSON object
per language with everything already matched correctly: question text,
options (translated if available, otherwise falling back to the English
structure for type/id/required), matched question-by-question. Nothing here
involves re-typing text — only re-indexing data that already exists.

Usage:
    python3 3_reshape_data.py extracted_data.json clean_survey_data.json
"""
import json
import sys

LANG_CODES = ['en', 'pt', 'es', 'ms', 'vi', 'bn']

def reshape(extracted_path, out_path):
    with open(extracted_path) as f:
        data = json.load(f)

    EQ = data['EQ']
    LANGS = data['LANGS']
    qLabels = data['qLabels']

    result = {}
    for lc in LANG_CODES:
        sections_out = []
        flat_idx = 0
        lang_opts = LANGS[lc]['opts']
        lang_sections_meta = LANGS[lc]['sections']

        for si, section in enumerate(EQ):
            qs_out = []
            for qi, q in enumerate(section):
                if lc == 'en':
                    qtext = q['q']
                else:
                    qtext = qLabels[lc][flat_idx] if flat_idx < len(qLabels[lc]) else q['q']

                translated_opts = None
                if lc != 'en':
                    sect_opts = lang_opts[si] if si < len(lang_opts) else None
                    if sect_opts and qi < len(sect_opts) and sect_opts[qi]:
                        translated_opts = sect_opts[qi]
                opts_final = translated_opts if translated_opts else q.get('opts')

                qs_out.append({
                    'id': q['id'], 'type': q['type'], 'req': q['req'],
                    'q': qtext, 'opts': opts_final,
                    'min': q.get('min'), 'max': q.get('max'),
                    'lo': q.get('lo'), 'hi': q.get('hi'),
                })
                flat_idx += 1

            meta = lang_sections_meta[si] if si < len(lang_sections_meta) else {'title': '', 'sub': ''}
            sections_out.append({'title': meta['title'], 'sub': meta['sub'], 'questions': qs_out})

        result[lc] = {
            'form_title': LANGS[lc]['title'],
            'form_desc': LANGS[lc]['desc'],
            'sections': sections_out,
        }

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Wrote {out_path} — {len(LANG_CODES)} languages, "
          f"{sum(len(s['questions']) for s in result['en']['sections'])} questions each")

if __name__ == '__main__':
    extracted_path = sys.argv[1] if len(sys.argv) > 1 else 'extracted_data.json'
    out_path = sys.argv[2] if len(sys.argv) > 2 else 'clean_survey_data.json'
    reshape(extracted_path, out_path)
