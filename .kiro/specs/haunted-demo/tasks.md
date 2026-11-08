# Implementation Plan

- [x] 1. Serve the haunted page locally
  - Static HTML, CSS, and JS in `demos/haunted/`.
  - Stdlib server on 127.0.0.1 calling `DocumentAgent`.
  - _Requirements: 1.1, 1.2_

- [x] 2. Show ghosts and highlighted clauses
  - Not found and rejected claims set `ghost` and return no citations.
  - Cited and accepted claims return offsets that match the fixture slice.
  - _Requirements: 1.3, 1.4_

- [x] 3. Print the judge walkthrough
  - `scripts/demo_walkthrough.py` covers both apps.
  - Exit 0 only when the gold suite passes.
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 4. Remind before a demo claim
  - Steering in `.kiro/steering/haunted-demo.md`.
  - Hook `.kiro/hooks/walkthrough-before-demo.json`.
  - _Requirements: 3.1_

- [x] 5. Let a judge paste or pick a document
  - The page offers Sample EOB, Sample lease, and Paste a document.
  - Paste ingests the posted text with `DocumentAgent` under id `pasted-document`.
  - _Requirements: 2.2, 2.3, 2.6_

- [x] 6. Show cited claims and ghost claims
  - A proposed answer is checked sentence by sentence through the shared library.
  - Mixed answers return both kinds of claim. Ghosts have no citation.
  - _Requirements: 2.4_

- [x] 7. Reject empty and oversized input
  - Missing question and answer, a blank pasted document, and over-limit bodies return HTTP 400.
  - Covered by `tests/test_web_demo.py`.
  - _Requirements: 2.5_

- [x] 8. Document the one-command judge quickstart
  - README section `Judge quickstart` names `python3 demos/haunted/server.py`.
  - _Requirements: 2.1, 2.7_
