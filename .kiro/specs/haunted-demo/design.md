# Design

## Page

`demos/haunted/index.html`, `app.js`, and `style.css` are static. The judge picks Sample EOB, Sample lease, or Paste a document. The form has a labeled question and a labeled proposed answer. The browser posts JSON to `/api/ask` on the same origin.

A ghost claim uses the `ghost-claim` class, which fades, and a text badge that says Ghost. A cited claim has a badge that says Cited. The source view wraps each returned span in `mark.clause` only when the offsets slice that exact text. Labels, a skip link, visible focus, and `prefers-reduced-motion` keep the page usable without a pointer. Color is not the only signal.

## Request

`app` is `eob`, `lease`, or `paste`. `paste` requires `document`. A question alone uses `DocumentAgent.answer`. A proposed answer is split on sentence boundaries and each sentence is passed to `DocumentAgent.reject_ungrounded_claim` and, when that call accepts it, `DocumentAgent.answer`. The page does not rank spans itself.

Empty question-and-answer text, an empty pasted document, a body over `MAX_BODY`, and a document over `MAX_DOCUMENT` return HTTP 400 with `{"error": "..."}`. The process stays on `127.0.0.1`. Pasted text is not written to disk and is not sent off the machine.

## Server

`demos/haunted/server.py` is a stdlib `ThreadingHTTPServer` bound to `127.0.0.1`. Fixture picks load `grave_truth.apps.eob` or `grave_truth.apps.lease`, which ingest `fixtures/sample_eob.txt` and `fixtures/sample_lease.txt`. A paste builds a new `DocumentAgent` and ingests the posted text as `pasted-document`. The process does not open an outbound socket.

`python3 -m http.server` can serve the static files and will not answer `/api/ask`. The supported command is `python3 demos/haunted/server.py`.

## Walkthrough

`scripts/demo_walkthrough.py` reads `evals/gold_cases.json` and scores each case with `grave_truth.grading.evaluate_case`. The printed answer is the library output. Pass/fail is the grader. Rejected and accepted claims print `Quote: none` because the rejection check does not invent a supporting span for a claim it refuses.

## Hook

`.kiro/hooks/walkthrough-before-demo.json` reminds the agent, after the demo or the script changes, to run the walkthrough and `tests/test_web_demo.py` before claiming the demo works. Steering for the same files is `.kiro/steering/haunted-demo.md`.
