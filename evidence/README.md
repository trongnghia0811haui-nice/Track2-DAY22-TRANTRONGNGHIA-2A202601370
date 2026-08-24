# Day 22 Evidence Summary

## Required evidence status

| Evidence | Status | Verified content |
|---|---|---|
| `01_langsmith_traces.png` | PASS | LangSmith `rag-query` runs with input/output; 50 runs visibly selected |
| `02_prompt_hub.png` | PASS | Both named prompt versions are visible in Prompt Hub |
| `02_ab_routing_log.txt` | PASS | 50 queries total: V1=19, V2=31; both prompts pulled from Hub; no fallback/error |
| `03_ragas_scores.png` | PASS | Terminal comparison contains all four metrics for V1 and V2 |
| `03_ragas_report.json` | PASS | Valid submission JSON corresponding to the score screenshot |
| `04_pii_demo_log.txt` | PASS | Six PII cases including clean and multi-PII inputs |
| `04_json_demo_log.txt` | PASS | Five JSON cases including repair and irreparable-input fallback |

## LangSmith tracing and Prompt Hub

The read-only LangSmith API audit found:

- 100 root runs named `rag-query`.
- 200 root runs named `ab-rag-query`.
- 0 root errors across those two run groups.
- Sample traces from both groups contain retrieved-context markers.

Public trace URL (verified without an authenticated browser session, HTTP 200):

[Open the public LangSmith trace after V2 tuning](https://smith.langchain.com/public/8c0cade9-6a70-4555-90f1-7fc5586a1371/r/01a03374-addf-7c22-b586-cf1a8ff5741a?start_time=2026-08-24T11%3A07%3A59.838278Z)

The Prompt Hub contains:

- `tran-trong-nghia-rag-prompt-v1`
- `tran-trong-nghia-rag-prompt-v2`

The official A/B run contains exactly 50 labeled queries. MD5 routing produced 19 V1 queries and 31 V2 queries, with no local fallback.

## RAGAS comparison

| Metric | V1 | V2 | Winner |
|---|---:|---:|---|
| Faithfulness | 0.9646 | 0.9878 | V2 |
| Answer relevancy | 0.9107 | 0.9153 | V2 |
| Context recall | 1.0000 | 1.0000 | Tie |
| Context precision | 0.9383 | 0.9450 | V2 |

Both versions exceed the required faithfulness threshold of 0.9 for the quality bonus. V2 is now the preferred version because it has higher faithfulness, answer relevancy, and context precision while matching V1's perfect context recall.

The retrieval layer remains strong: both versions have context recall of 1.0 and context precision near 0.94. The V2 tuning removed mandatory confidence statements and reduced the answer to 2–3 concise, explicitly grounded sentences. This change reduced unsupported elaboration while preserving the expert response style. Compared with V1, tuned V2 improved faithfulness by 0.0232, answer relevancy by 0.0047, and context precision by 0.0067.

The terminal output also reports that the evaluator returned one generation instead of the requested three for some RAGAS calls. RAGAS still completed 200/200 evaluations and wrote all metrics, but this limitation should be considered when interpreting small score differences.

## Guardrails results

The custom PII validator successfully handled:

- Email
- Phone number, including parenthesized area code
- SSN
- Credit card number
- Multi-PII input
- Clean input

The custom JSON validator successfully handled:

- Valid JSON
- Markdown code fences
- Single quotes
- Trailing commas
- Irreparable input using a valid fallback JSON object

Both validators use `OnFailAction.FIX` through the validator constructor. PII and repaired/fallback JSON outputs use `FailResult(fix_value=...)`, which is required for Guardrails 0.11 to apply the corrected output.

## Report integrity and security

- `data/ragas_report.json` remains an ignored local generated artifact, as directed by the starter `.gitignore` comment.
- `evidence/03_ragas_report.json` is the authoritative final tuning report and corresponds to `03_ragas_scores.png`.
- The local data report and submission evidence currently have the same SHA-256: `80AFE584D35D95090C9EF864E75B86643AA93847168EA840E9951AFD5AA6D9AA`.
- `.env` and `.venv` are ignored and are not tracked or staged.
- The repository scan found no API-key pattern outside `.env` and `.env.example`.

The current LangSmith UI supports public sharing for individual traces rather than the entire tracing project. The public trace above is the anonymous-access evidence associated with project `day22-lab`.
