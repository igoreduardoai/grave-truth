# Requirements Document

## Introduction

Grave Truth answers questions about an ingested plain-text document by quoting spans. If the document does not support the question, the answer is `not found`. A proposed claim that attaches a number to the wrong clause is rejected. This spec is the contract for the shared skeleton. The EOB and lease apps are specified separately and only supply documents.

## Requirements

### Requirement 1: Ingest cited spans

**User Story:** As a developer building a document agent, I want each document split into spans I can point at, so that an answer can be checked against the source bytes.

#### Acceptance Criteria

1. WHEN a non-empty document id and non-empty text are ingested THEN the system SHALL store sentence spans such that `text[start:end]` equals the span.
2. IF the document id is blank OR the text is blank THEN the system SHALL raise `ValueError`.
3. WHEN the same document id is ingested again THEN the system SHALL drop the previous spans for that id and keep the new text.
4. WHILE more than one document is loaded the system SHALL keep each span's document id.

### Requirement 2: Answer only from retrieved spans

**User Story:** As a person reading a synthetic bill or lease, I want the answer to be a sentence from the file, so that I can see where the figure came from.

#### Acceptance Criteria

1. WHEN a question shares no usable tokens or numbers with the ingested text THEN the system SHALL return `found=false`, text `not found`, and no citations.
2. WHEN a question matches one clause THEN the system SHALL return that clause as the answer and a citation whose span is that clause.
3. WHEN a question names two subjects that live in different clauses THEN the system SHALL cite each of those clauses.
4. WHEN an answer is returned THEN every number string in the answer text SHALL appear in at least one cited span.
5. IF the citation offsets do not slice the stored document THEN the system SHALL return `not found` instead of a broken quote.
6. WHEN the answer is returned with citations THEN `GroundedAnswer.ghost` SHALL be false; WHEN the answer is `not found` THEN `ghost` SHALL be true.

### Requirement 3: Abstain instead of guessing

**User Story:** As a reviewer, I want missing topics to abstain, so that a gap in the file is not filled with a nearby dollar amount.

#### Acceptance Criteria

1. WHEN the question is about a topic the document never mentions THEN the system SHALL return `not found`.
2. IF the only overlapping words are boilerplate such as "explanation of benefits" AND the question's subject word is absent THEN the system SHALL NOT cite the boilerplate sentence in place of the subject.
3. WHERE a small alias list maps `doctor` to `provider` or `renter` to `resident` the system SHALL still quote the original sentence and SHALL NOT insert the alias word as a new fact.

### Requirement 4: Reject ungrounded numbers and ids

**User Story:** As a reviewer, I want invented or swapped figures flagged, so that a true number from another line cannot bless a false claim.

#### Acceptance Criteria

1. WHEN a claim contains a number that never occurs in the document THEN `reject_ungrounded_claim` SHALL return true.
2. WHEN a claim's number occurs only in a different subject's clause THEN `reject_ungrounded_claim` SHALL return true.
3. WHEN every number in the claim occurs in a clause whose preceding words match the claim's subject THEN `reject_ungrounded_claim` SHALL return false.
4. WHEN a claim contains an identifier of the form `LETTERS-DIGITS` that is not in a matching clause THEN `reject_ungrounded_claim` SHALL return true.
5. IF a claim mixes one supported figure with one unsupported figure THEN the system SHALL reject the whole claim.
6. WHERE formatting differs only by `$`, commas, or trailing zeros (`$1,850.00` versus `1850`) the system SHALL treat the values as the same number.
7. IF one value is a percent and the other is not THEN the system SHALL treat them as different.

### Requirement 5: Shared amounts stay ambiguous until the subject is named

**User Story:** As a reader of the lease, I want rent and the security deposit distinguished even though both are `$1,850.00`.

#### Acceptance Criteria

1. WHEN the question asks for the security deposit THEN the cited span SHALL contain `security deposit` and SHALL NOT be the monthly-rent sentence alone.
2. WHEN the question asks for monthly rent THEN the cited span SHALL contain `Monthly rent`.
3. WHEN the question is only the shared amount `$1,850.00` THEN the system SHALL cite both clauses rather than pick one silently.
