# Requirements: workflow file

## Introduction

The check ends in a file a person can download. The file is a synthetic dispute letter for the sample bill, or a clause list for the sample lease. Every cited claim names the span that supports it. Every other claim says not found.

## Requirements

### Requirement 1: Deterministic file

**User Story:** As a person reading the synthetic bill, I want a letter I can save, so that each claim I might dispute is tied to a sentence or marked not found.

#### Acceptance Criteria

1. WHEN the sample bill is exported THEN the system SHALL write the same markdown on every run.
2. WHEN a claim is cited THEN the markdown SHALL include the document id, the start offset, the end offset, and the span text.
3. WHEN a claim is not supported THEN the markdown SHALL say `not found` and SHALL NOT include a citation.
4. The file SHALL state that a live model was not called, and that this is not a medical device and not legal advice.

### Requirement 2: Same rule for the lease

**User Story:** As a person reading the synthetic lease, I want a clause list, so that a swapped fee is not written down as a finding.

#### Acceptance Criteria

1. WHEN the sample lease is exported THEN cited claims SHALL slice the lease text and rejected claims SHALL say `not found`.
2. The lease file SHALL be a different filename from the bill file.

### Requirement 3: Judge path and health

**User Story:** As a reviewer without an API key, I want one URL and a health check, so that I can see the letter without a second click and without a model.

#### Acceptance Criteria

1. WHEN the page is opened with `?judge=1` THEN the page SHALL check the synthetic bill and fill the letter without waiting for another click.
2. WHEN `GET /health` is requested THEN the response SHALL be static JSON and SHALL say the live model is unimplemented.
3. A static build SHALL be writable to `site/` without deploying it.
