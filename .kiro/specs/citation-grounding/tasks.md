# Implementation Plan

- [x] 1. Preserve the public skeleton
  - Keep `DocumentAgent`, `GroundedAnswer`, `Citation`, `ingest`, `answer`, and `reject_ungrounded_claim`.
  - Replace spans when the same document id is ingested again.
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 2. Rank clauses instead of concatenating loose hits
  - Score tokens and bigrams, ignore boilerplate overlap, and return the clause that holds the subject.
  - Add a second clause only when the question still has an uncovered subject, or when a bare shared amount matches more than one clause.
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 3.1, 3.2, 5.1, 5.2, 5.3_

- [x] 3. Reject numbers that sit in the wrong clause
  - Normalize `$`, commas, and trailing zeros.
  - Keep percents distinct from plain numbers.
  - Require the subject window in front of the number, and require identifiers to appear in a matching clause.
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_

- [x] 4. Lock the contract with gold cases and property checks
  - Extend `evals/gold_cases.json` past the original cited, not-found, and rejection cases.
  - Share one grader between `evals/run_evals.py` and pytest.
  - Add generated-document checks that invented amounts are rejected and cited numbers are slices of the source.
  - _Requirements: 2.4, 3.1, 4.1, 5.1_

- [x] 5. Keep a small alias list from becoming new facts
  - Map a few question words onto words that already occur in the fixtures.
  - Quote the fixture sentence unchanged.
  - _Requirements: 3.3_
