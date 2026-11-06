# Implementation Plan

- [x] 1. Keep the in-package app loaders
  - `grave_truth.apps.eob` and `grave_truth.apps.lease` still ingest the shared fixtures.
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 2. Add two top-level application folders
  - `eob-explainer/main.py` and `lease-checker/main.py` call the shared CLI.
  - Each folder has a short README with the demo limit.
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 3.4_

- [x] 3. Add an offline CLI
  - `python3 -m grave_truth` answers, rejects, or reads a local file.
  - Plain text shows the span. `--json` is available for tests.
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

- [x] 4. Extend the synthetic fixtures without replacing them
  - Keep the original EOB and lease sentences.
  - Add a claim number, service date, lease term, and guest stay so near-miss amounts and dates have gold cases.
  - _Requirements: 3.1, 3.2, 3.3_
