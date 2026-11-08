# Implementation plan

- [x] 1. Keep pytest and gold as a layer
  - `validation/gold.py` runs the existing commands and parses their summaries.
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 2. Add a per-app config and a local allowlist
  - `validation/apps/grave-truth.json` lists the pilot profiles.
  - Public allowlist hosts are rejected.
  - _Requirements: 5.3, 6.3_

- [x] 3. Run scripted Playwright journeys
  - Profiles cover select, paste, citation, billed versus allowed, not-found, empty input, and keyboard.
  - Each profile uses a clean context. The kind is `scripted_profile`.
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 4. Run axe-core and Lighthouse
  - axe-core 4.14.0 on the initial page and a cited EOB state.
  - Lighthouse 13.6.0 as a laboratory diagnostic, not a gate.
  - _Requirements: 3.1, 3.2, 3.3_

- [x] 5. Adapt one persona loop
  - ux-swarm step shape, MIT license retained, model call behind opt-in.
  - The checked-in run uses a replay double and records the LLM layer as skipped.
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 6. Catch planted failures
  - Wrong citation page and the example.com link.
  - _Requirements: 5.1, 5.2_

- [x] 7. Disclose provenance
  - `THIRD_PARTY_NOTICES.md`, `validation/NOTICE`, and `validation/third_party/ux-swarm/LICENSE`.
  - Quickstart: `sh validation/run.sh`.
  - _Requirements: 6.1, 6.2, 6.3_
