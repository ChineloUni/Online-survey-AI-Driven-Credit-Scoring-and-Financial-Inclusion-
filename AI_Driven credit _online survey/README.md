# AI Credit Scoring & Financial Inclusion — Online Survey

Part of a PhD research study (Lincoln University, New Zealand) examining how AI-driven
credit scoring affects financial inclusion across nine developing economies: Bangladesh,
Brazil, Ghana, Kenya, Malaysia, Mexico, Nigeria, Peru, and Vietnam.

## Files in this repo

| File | Purpose |
|---|---|
| `ai_credit_survey_multilingual.html` | **The live survey.** 32 questions across 6 sections, available in English, Portuguese, Spanish, Bahasa Malaysia, Vietnamese, and Bengali. This is the file the live URL below serves. |
| `AI_Credit_Score_Financial_Inclusion_Online_survey.xlsx` | Full survey documentation: question-by-question content per section, the language/translation reference, and a dated Change Log of every edit made to the survey (see below). |
| `README.md` | This file. |

## Live survey

**[chinelouni.github.io/.../ai_credit_survey_multilingual.html](https://chinelouni.github.io/Online-survey-AI-Driven-Credit-Scoring-and-Financial-Inclusion-/ai_credit_survey_multilingual.html)**

**Not yet open for real data collection** — pending Lincoln University Human Ethics
Committee (HEC) approval.

## How responses are collected

Every submission is sent to two places independently:

1. **Formspree** (form ID `mykaeprq`) — the primary, verified channel. Confirmed working
   from the live hosted URL, with real submissions landing correctly.
2. **A backend Google Form** (32 fields matching the survey exactly) — intended as a
   free, uncapped, private secondary data store. **Currently not working correctly** —
   see Known Issues below.

Neither channel depends on the other; if one fails, the respondent's experience and the
other channel are unaffected.

## Known issues

**Google Form submissions are not being recorded correctly.** The response count
increases with each submission, but individual field data is not being captured — every
question shows "0 responses." Three different submission techniques have been tried
(a standard `fetch()` call, a `fetch()` call without a manually-set Content-Type header,
and a real hidden-form POST into a hidden iframe) and all three fail identically, which
rules out the submission technique itself as the cause. Browser caching was investigated
and ruled out as the explanation for this specific issue (it was confirmed to be the
cause of a separate, since-resolved Formspree issue, but Google Forms still failed even
after that was fixed). **Leading hypothesis, not yet confirmed:** the 32 `entry.XXXXXXXXX`
field IDs currently wired into the submission code may no longer match the form's actual
current fields. Formspree remains fully reliable in the meantime.

## Development log

Dates are day-level precision except where a specific verified timestamp is noted.
Entries dated "reconstructed" are inferred from GitHub's commit history and file
listing, not a direct contemporaneous record, since that work predates this log.

### ~June 2026 (reconstructed from GitHub commit history)
- Repository created (`README.md`, initial commit)
- Initial survey files uploaded: `ai_credit_scoring_survey.html`,
  `ai_credit_survey_multilingual_english_response(...)`, `ai_credit_survey_multilingual.html`
  (original version), `proposal_guide.html` — appears to be the original build of the
  6-language survey

### ~June–July 2026 (reconstructed from commit message)
- Formspree integration added ("Update survey with Formspree endpoint") — form ID,
  submission code, and linked Google Sheet already working prior to 9 Aug 2026

### 9 Aug 2026
- Removed the "Other" option from the country dropdown across all 6 languages (English,
  Portuguese "Outro", Spanish "Otro", Bahasa Malaysia "Lain-lain", Vietnamese "Khác",
  Bengali "অন্যান্য") — case selection is fixed to exactly 9 countries; an open option
  risked out-of-scope responses
- Fixed a silent-failure bug where the survey showed a "Success" message to respondents
  even when a submission genuinely failed to send
- Corrected the stated completion time from "8–10 minutes" to "15–20 minutes," matching
  the actual 32-question count
- Built a backend Google Form (32 fields) and extracted all 32 `entry.XXXXXXXXX` field
  IDs via two rounds of pre-fill link generation
- Three attempts made at Google Forms dual-submission (see Known Issues above) — all
  three failed identically
- Discovered the live GitHub Pages URL was serving a version ~2 months out of date;
  corrected, including recovering from an accidental duplicate file caused by a hidden
  file-extension error during renaming
- Diagnosed and resolved a Formspree issue where hosted submissions weren't appearing —
  root cause was browser caching, not a Formspree configuration problem. **Confirmed
  fixed**: a real test submission was verified in the Formspree inbox, timestamped
  **9 Aug 2026, 12:17 (UTC)**, correctly logged with full response data
- Re-tested Google Form submission from the same fixed, cache-cleared live URL — issue
  persists, confirmed to be a separate problem from the Formspree caching issue

## Next steps

- Diagnose the Google Form entry ID mismatch (compare a freshly-generated pre-fill link
  against the IDs currently in the code, and/or inspect the browser Network tab response
  for the `docs.google.com` submission request directly)
- Lincoln HEC ethics approval before any real data collection begins
