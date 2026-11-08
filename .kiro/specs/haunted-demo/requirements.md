# Requirements Document

## Introduction

The haunted demo shows the same citation rule as the two apps. An uncited claim fades. A cited answer highlights the clause it quoted. The judge walkthrough prints that result for every gold case.

## Requirements

### Requirement 1: Local page

**User Story:** As a reviewer offline, I want a page that shows ghosts and highlighted clauses, so that grounding is visible without a model API.

#### Acceptance Criteria

1. WHERE the repository is checked out the system SHALL include `demos/haunted/` with static HTML, CSS, and JS plus a stdlib server.
2. WHEN the server answers a question THEN it SHALL call `DocumentAgent` on the synthetic fixture for the selected app.
3. WHEN the answer is not found or the claim is rejected THEN the response SHALL mark the claim as a ghost and SHALL NOT include a citation.
4. WHEN the answer is cited or the claim is accepted THEN the response SHALL include span offsets that slice the fixture text.

### Requirement 2: Judge web demo

**User Story:** As a judge, I want one local page where I can pick a fixture or paste a synthetic document and check a question or a proposed answer, so that cited claims and ghost claims are visible in the browser.

#### Acceptance Criteria

1. WHEN `python3 demos/haunted/server.py` runs THEN the process SHALL print a `127.0.0.1` URL and SHALL NOT open an outbound connection.
2. WHEN the page picks the EOB or the lease THEN the server SHALL call `DocumentAgent` on that synthetic fixture.
3. WHEN the page pastes a document THEN the server SHALL ingest that text with `DocumentAgent` and SHALL NOT substitute a fixture.
4. WHEN a proposed answer has more than one sentence THEN the server SHALL check each sentence with `DocumentAgent`. A sentence with no citation SHALL be a ghost. A cited sentence SHALL include span offsets that slice the document.
5. IF the question and the answer are both empty, or the pasted document is empty, or the body or the document is over the size limit THEN the server SHALL respond with HTTP 400 and an error message and SHALL NOT invent an answer.
6. The page SHALL name the document choice, the pasted document, the question, and the proposed answer with labels, and SHALL be usable from the keyboard.
7. The README SHALL document that one command as the judge quickstart.

### Requirement 3: Judge transcript

**User Story:** As a judge, I want a printed transcript, so that I can read question, answer, quote, and pass/fail without opening a browser.

#### Acceptance Criteria

1. WHEN `python3 scripts/demo_walkthrough.py` runs THEN it SHALL print a block for every gold case in both apps.
2. WHEN every gold case passes THEN the script SHALL exit 0.
3. The script SHALL NOT call a network API.
