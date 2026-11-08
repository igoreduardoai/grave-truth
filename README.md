# Grave Truth

A citation-grounded document-agent skeleton for [Kiroween 2026](https://kiroween.devpost.com/), Skeleton Crew. Every answer quotes a source span or says `not found`. A number from one clause cannot support a different subject.

Skeleton Crew here means two applications on one library, with the specs, steering, and hooks committed in `.kiro` (that directory is not gitignored). The haunted page is a third view of the same library. It does not carry a second ranker.

Two applications share that skeleton:

| App | Folder | Loader | Fixture |
|---|---|---|---|
| EOB explainer | `eob-explainer/` | `grave_truth.apps.eob` | `fixtures/sample_eob.txt` |
| Lease checker | `lease-checker/` | `grave_truth.apps.lease` | `fixtures/sample_lease.txt` |

The library is `src/grave_truth`. The folders above are the two apps. They do not copy the ranker.

This is a research demo. It is not a medical device and not legal advice. Documents in `fixtures/` are synthetic. There is no real PHI and no real lease.

## Judge quickstart

One command, from the repo root. No API key and no network:

```bash
python3 demos/haunted/server.py
```

Open the `http://127.0.0.1:8765/` URL the process prints. Pick the sample EOB or the sample lease, or paste a synthetic document. Type a question, a proposed answer, or both, then choose **Check grounding**. Examples under the form fill both and run the check.

Cited claims stay on the page, with a Cited badge, and the source clause is marked in gold. Claims with no supporting clause are ghosts: the sentence fades and a Ghost badge stays. The page posts to that local process, which calls `DocumentAgent` in `src/grave_truth`. It does not reimplement the checker and it does not send the document anywhere.

`python3 -m http.server` only serves the static files. It does not answer questions.

## How to run

Python 3.11 or newer. From the repo root:

```bash
python3 -m pip install -e ".[dev]"
python3 evals/run_evals.py
python3 -m pytest
```

Offline demo (no model API, no network):

```bash
python3 -m grave_truth eob "What is the patient responsibility?"
python3 -m grave_truth lease "What is the security deposit?"
python3 -m grave_truth reject eob "The billed amount is $180.00."
python3 eob-explainer/main.py
python3 lease-checker/main.py "How many days written notice are required to terminate?"
python3 scripts/demo_walkthrough.py
python3 demos/haunted/server.py
```

Pre-submission check (pytest, gold cases, scripted browser journeys, axe-core, Lighthouse). No model API:

```bash
sh validation/run.sh
```

Details, licenses, and the last observed run are in `validation/README.md` and `validation/reports/OBSERVED.md`.

`scripts/demo_walkthrough.py` prints a judge transcript for both apps: question, answer, quote span, and pass/fail. It exits 0 when every gold case passes. Run it before treating the demo as working.

`demos/haunted/server.py` binds to `127.0.0.1` and prints a localhost URL. Open that URL. Uncited claims fade. A cited answer highlights the source clause in the fixture. The page posts to that process, which calls `DocumentAgent`. No paid API. `python3 -m http.server` from `demos/haunted/` only serves the static files; it does not answer questions.

`eob` and `lease` with no question use a built-in demo question. `file <path> "<question>"` answers from any local text file. `--json` prints the same result as JSON.

```text
App: lease
Question: What is the security deposit?
Found: yes
Ghost: no
Answer: The security deposit is $1,850.00 and is not rent.
Citations:
- sample-lease [314:364] The security deposit is $1,850.00 and is not rent.
```

Rent is also `$1,850.00`. The citation is the deposit sentence, including "not rent". A claim that the deposit is the late fee (`$75.00`) is rejected. A question the fixture never mentions, such as an out-of-network penalty, is `not found`.

```python
from grave_truth.apps import eob

result = eob.explain("What is the patient responsibility?")
print(result.text)
print(result.citations[0].span)
```

## How it works

1. `DocumentAgent.ingest` stores a document and splits it into sentence spans. Ingesting the same id again replaces those spans.
2. `retrieve` ranks spans by token overlap. Boilerplate such as "explanation of benefits" does not outvote a subject word. A question that names a subject the file does not contain returns no spans.
3. `answer` quotes the winning span, or two spans when the question covers two subjects. A bare shared amount cites each clause that contains it. Every number in the answer text is in a cited span. Offsets slice the source.
4. `reject_ungrounded_claim` returns true when a number or id (`CLM-20481`) is missing, or when the number sits in a different clause. `$1,850.00` and `1850` are the same value. `20%` is not `20`.

Uncited claims do not survive as answers (`GroundedAnswer.ghost`).

A few question-side aliases (`doctor` → `provider`, `renter` → `resident`, `termination` → `terminate`) only help retrieval. The printed answer is still the original sentence.

## Kiro workflow

`/.kiro` is part of the repo. It is not gitignored.

Specs (requirements, design, tasks):

- `.kiro/specs/grave-truth.md` — overview
- `.kiro/specs/citation-grounding/` — spans, abstention, rejection
- `.kiro/specs/demo-apps/` — the two app folders and the CLI
- `.kiro/specs/haunted-demo/` — the local page: paste or pick a document, cited claims and ghosts
- `.kiro/specs/pre-submission-validation/` — local checks around that page. Not a third application.

Steering in `.kiro/steering/`:

- `no-invention.md`, `product.md`, `tech.md`, `structure.md` load always
- `testing-gold-cases.md` and `fixture-safety.md` load by file match
- `add-gold-case.md` loads automatically when eval work is in context
- `demo-walkthrough.md` is manual (`#demo-walkthrough`)
- `validation-stack.md` loads by file match on `validation/`

Hooks in `.kiro/hooks/`:

- `run-evals.json` — original on-save hook that runs the gold suite
- `evals-on-save.json` — Kiro v1 `PostFileSave` command hook for the same suite
- `pytest-on-save.json` — v1 command hook for pytest
- `grounding-reminder.json` — v1 agent prompt after `skeleton.py` changes
- `block-secret-files.json` — v1 `PreToolUse` command that exits 2 for `.env`, key, and `secrets/` paths (`scripts/kiro_guard_no_secrets.py`)
- `walkthrough-before-demo.json` — v1 agent prompt after `demos/haunted/` or `scripts/demo_walkthrough.py` changes, to run the walkthrough and the web demo tests before claiming the demo works

Run the hook command locally with `python3 evals/run_evals.py`. The demo check is `python3 scripts/demo_walkthrough.py`.

## Eval results

Gold cases live in `evals/gold_cases.json`.

| Expectation | Cases |
|---|---|
| cited | 33 |
| not_found | 17 |
| reject_ungrounded | 18 |
| accept_grounded | 22 |
| **Total** | **90** |

Last local run (2026-11-08), on this working tree:

- `python3 evals/run_evals.py` → **90/90 passed** (cited 33, not_found 17, reject_ungrounded 18, accept_grounded 22)
- `python3 -m pytest` → **53 passed** (39 on the judge-demo branch before the validation unit tests, plus 14 tests for the harness)
- `python3 scripts/demo_walkthrough.py` → exit 0, `passed 90/90` (accept_grounded 22, cited 33, not_found 17, reject_ungrounded 18)
- `sh validation/run.sh` → scripted browser tasks 10/10, citation 7/7, refusal 3/3, planted failure caught, LLM persona skipped, observed cost $0. See `validation/reports/OBSERVED.md`.

The gold-case table matches `evals/gold_cases.json`. The 90/90 and 39 pytest figures were re-run on commit `dca54ec` before the harness tests were added. The 53 count is the later pytest run.

## Limits

- Research demo. Not a medical device. Not legal advice. Not a coverage decision and not a contract review.
- Retrieval is lexical and offline. Paraphrases outside the small alias list abstain instead of guessing. A Portuguese question against the English-only lease is `not found` when no span matches.
- The pharmacy charge (`$18.40`) and the patient responsibility (`$42.15`) are different clauses. The late fee (`$75.00`) is not monthly rent (`$1,850.00`). Same value with a different `$` or comma form still counts as that value.
- Citations are sentences. A sentence that contains two dates is quoted whole.
- The agent quotes the file. It does not know whether the file is true outside that file.
- One synthetic document per app. No insurer, clinic, or landlord has used this software.
- Same numeric value with different `$` / comma formatting counts as one number. A different value is rejected even if it appears next to another subject.

## License

MIT. Built as a new project after 30 October 2026 for Kiroween. Igor Eduardo, Founder in Residence at Antler. Cortexa Social Inc.

Upstream licenses for the validation tooling are in `THIRD_PARTY_NOTICES.md`. The validation stack is test tooling, not a third application.
