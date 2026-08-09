"""
Step 1 — Extract the raw JavaScript data blocks from the survey HTML.

Why this step exists: the HTML file stores three separate pieces of data —
the question structure (EQ), the per-language UI text and options (LANGS),
and the translated question wording (qLabels), which sits inside a function
rather than as its own top-level variable. This script just locates and
copies out those three blocks as plain text. No translation, no re-typing —
pure text extraction by finding known markers in the file.

Usage:
    python3 1_extract_blocks.py survey.html extract.js
"""
import sys

def extract_blocks(html_path, out_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Block 1: the question structure (ids, types, required flags, English text/options)
    eq_start = content.find('const EQ = [')
    eq_end = content.find('\n];', eq_start) + 3
    eq_block = content[eq_start:eq_end]

    # Block 2: per-language UI text, section titles, and translated options
    langs_start = content.find('const LANGS = {')
    lang_var_start = content.find('\nlet lang', langs_start)
    langs_block = content[langs_start:lang_var_start]

    # Block 3: translated question wording (lives inside the dispQ render function)
    qlabels_start = content.find('const qLabels={', content.find('const dispQ'))
    qlabels_end = content.find('};', qlabels_start) + 2
    qlabels_block = content[qlabels_start:qlabels_end]

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(eq_block + '\n\n')
        f.write(langs_block + '\n\n')
        f.write(qlabels_block + '\n\n')
        # This line is the key move: dump the three variables as JSON using
        # Node's own JSON.stringify, rather than trying to read/copy the
        # JS object literals by eye. Node resolves the actual data structure;
        # we never touch the text ourselves.
        f.write('console.log(JSON.stringify({EQ, LANGS, qLabels}));')

    print(f"Wrote {out_path} ({len(eq_block)} + {len(langs_block)} + {len(qlabels_block)} chars)")

if __name__ == '__main__':
    html_path = sys.argv[1] if len(sys.argv) > 1 else 'survey.html'
    out_path = sys.argv[2] if len(sys.argv) > 2 else 'extract.js'
    extract_blocks(html_path, out_path)
