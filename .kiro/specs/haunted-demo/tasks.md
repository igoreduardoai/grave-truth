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
  - _Requirements: 2.1_
