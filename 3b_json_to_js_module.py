"""
Step 3b — Convert clean_survey_data.json into a JS module.

docx-js runs under Node, so the build script needs the data as a `require`-able
JS file rather than a JSON file it has to read and parse separately. This is
a pure format conversion — json.dumps() writing valid JS object syntax to
a .js file. No text is read or re-typed here either.

Usage:
    python3 3b_json_to_js_module.py clean_survey_data.json survey_data_for_docx.js
"""
import json
import sys

def convert(json_path, js_path):
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write('const SURVEY_DATA = ' + json.dumps(data, ensure_ascii=False) + ';\n')
        f.write('module.exports = SURVEY_DATA;\n')
    print(f"Wrote {js_path}")

if __name__ == '__main__':
    json_path = sys.argv[1] if len(sys.argv) > 1 else 'clean_survey_data.json'
    js_path = sys.argv[2] if len(sys.argv) > 2 else 'survey_data_for_docx.js'
    convert(json_path, js_path)
