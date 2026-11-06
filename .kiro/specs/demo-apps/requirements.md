# Requirements Document

## Introduction

Two applications demonstrate the same skeleton. The EOB explainer answers questions about `fixtures/sample_eob.txt`. The lease checker answers questions about `fixtures/sample_lease.txt`. Both are local, synthetic, and offline. Neither gives medical or legal advice.

## Requirements

### Requirement 1: Two application folders

**User Story:** As a Skeleton Crew reviewer, I want two distinct applications on one foundation, so that the skeleton is shown to be reusable.

#### Acceptance Criteria

1. WHERE the repository is checked out the system SHALL include a top-level `eob-explainer/` folder and a top-level `lease-checker/` folder.
2. WHEN either folder's `main.py` runs THEN the system SHALL call the shared `DocumentAgent` rather than a second copy of the ranker.
3. WHEN `eob-explainer/main.py` is started with no arguments THEN the system SHALL answer a patient-responsibility question from the synthetic EOB.
4. WHEN `lease-checker/main.py` is started with no arguments THEN the system SHALL answer a monthly-rent question from the synthetic lease.

### Requirement 2: Offline CLI

**User Story:** As a judge without network access to a model API, I want a command that prints the answer and the citation, so that I can see the grounding.

#### Acceptance Criteria

1. WHEN `python3 -m grave_truth eob "<question>"` runs THEN the system SHALL print whether the answer was found, the answer text, and each citation's document id and span.
2. WHEN `python3 -m grave_truth lease "<question>"` runs THEN the system SHALL do the same for the lease fixture.
3. WHEN `python3 -m grave_truth reject eob "<claim>"` runs THEN the system SHALL print whether the claim was rejected.
4. WHEN `python3 -m grave_truth file <path> "<question>"` runs THEN the system SHALL ingest that local text file and answer from it.
5. IF the path is missing THEN the system SHALL exit with a non-zero status and SHALL NOT invent an answer.
6. The CLI SHALL NOT open a network connection.

### Requirement 3: Synthetic fixtures only

**User Story:** As a maintainer, I want the demo documents to stay obviously fake, so that the project never holds real PHI or a real lease.

#### Acceptance Criteria

1. The EOB fixture SHALL remain a synthetic explanation with Riverside Clinic and the published dollar amounts, including patient responsibility `$42.15`.
2. The lease fixture SHALL remain a synthetic lease for unit 4B at 200 Harbor Street, including monthly rent `$1,850.00` and a separate security deposit of `$1,850.00`.
3. WHERE new sentences are added they SHALL be synthetic and SHALL NOT contain real account numbers or patient identifiers.
4. The apps SHALL state in their README that they are not a medical device and not legal advice.

### Requirement 4: Shared behavior

**User Story:** As a developer, I want both apps to inherit abstention and rejection, so that a feature fixed in the skeleton shows up in both demos.

#### Acceptance Criteria

1. WHEN an EOB question has no supporting span THEN the EOB app SHALL return `not found`.
2. WHEN a lease question has no supporting span THEN the lease app SHALL return `not found`.
3. WHEN a claim swaps an EOB figure onto the wrong line THEN the EOB agent SHALL reject it.
4. WHEN a claim swaps a lease figure onto the wrong line THEN the lease agent SHALL reject it.
