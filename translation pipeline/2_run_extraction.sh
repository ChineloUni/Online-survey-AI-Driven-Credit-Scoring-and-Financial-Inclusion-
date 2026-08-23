#!/bin/bash
# Step 2 — Actually run the extracted JavaScript through Node.
#
# This is the step that actually prevents transcription errors. `extract.js`
# is real, executable JavaScript — the exact same code the survey page runs
# in a browser. Instead of a human (or an AI) reading the file and typing
# out what it seems to say, Node.js parses and executes it for real, then
# JSON.stringify dumps the fully-resolved data structure. Whatever comes out
# is provably identical to what the live survey page would use — there is
# no "read it and copy it" step where a character could be mistyped.
#
# Usage:
#   ./2_run_extraction.sh
#
# Requires: Node.js (any reasonably recent version — no npm packages needed,
# this only uses built-in JSON.stringify).

set -e
node extract.js > extracted_data.json
echo "Wrote extracted_data.json ($(wc -c < extracted_data.json) bytes)"
