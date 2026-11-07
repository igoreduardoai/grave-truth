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

### Requirement 2: Judge transcript

**User Story:** As a judge, I want a printed transcript, so that I can read question, answer, quote, and pass/fail without opening a browser.

#### Acceptance Criteria

1. WHEN `python3 scripts/demo_walkthrough.py` runs THEN it SHALL print a block for every gold case in both apps.
2. WHEN every gold case passes THEN the script SHALL exit 0.
3. The script SHALL NOT call a network API.
