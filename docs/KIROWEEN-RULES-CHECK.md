# Kiroween 2026 rules check

Retrieved 2026-11-17 from [https://kiroween.devpost.com/rules](https://kiroween.devpost.com/rules). The overview page [https://kiroween.devpost.com/](https://kiroween.devpost.com/) was retrieved the same day. Quotes below are the extractor’s text. Where the extractor joined sentences or collapsed whitespace, that is the text that was returned. Street-address lines on the rules page are omitted from this file.

The rules page opens with: "Updated November 16, 2026, to include residents of Australia."

## Dates

Quoted from section 1:

> Registration Period: October 13, 2026 (8:30 am Pacific Time) – December 4, 2026 (2:00 pm Pacific Time) (“Registration Period”).
>
> Submission Period: October 30, 2026 (9:00 am Pacific Time) – December 4, 2026 (2:00 pm Pacific Time) (“Submission Period”).
>
> No extensions will be granted. Late Submissions will not be accepted.
>
> Judging Period: December 16, 2026 (1:00 pm Pacific Time) – January 29, 2027 (1:00 pm Pacific Time) (“Judging Period”).

The overview page, retrieved the same day, says: "Deadline: Dec 4, 2026 @ 2:00pm PST".

2:00 pm Pacific Time on 4 December 2026 is 4:00 pm America/Chicago the same calendar day. That is a conversion of the quoted Pacific time, not a second sentence from the rules page.

## What to create

Quoted from Project Requirements:

> What to Create: Entrants must build a working software application using Kiro (IDE, CLI, Web, and/or Kiro Crew) and submit it into one of the following categories (each a “Project”). Insufficient use of Kiro will result in disqualification at the Judges’ sole discretion.
>
> - Resurrection: Bring your favorite dead technology back to life. Reimagine obsolete tech with today’s innovations or solving tomorrow's problems.
> - Frankenstein: Stitch together a chimera of technologies into one app. Bring together seemingly incompatible elements to build something unexpectedly powerful.
> - Skeleton Crew: Build a skeleton code template lean enough to be clear but flexible enough to support various use cases. Show us its versatility with two distinct applications from your foundation.
> - Costume Contest: Build any app but show us a haunting user interface that’s polished and unforgettable. Bring in spooky design elements that enhance your app’s function.
>
> Functionality: The Project must be capable of being successfully installed and running consistently on the platform for which it is intended and must function as depicted in the video and/or expressed in the text description.
>
> Platforms: A submitted Project must run on the platform for which it is intended and which is specified in the Submission Requirements.
>
> New Projects Only: Projects must be newly created by the Entrant after the start of the Hackathon Submission Period. Participants may use standard development resources, including frameworks, libraries, starter templates, but must disclose any other pre-existing code or work incorporated into the Project. The work described and submitted must have been built during the Submission Period.

This repository is entered as Skeleton Crew. The two application folders are `eob-explainer/` and `lease-checker/`. They share `src/grave_truth`.

## Submission requirements

Quoted from Submission Requirements:

> - Include a Project built using Kiro and meets the above Project Requirements.
> - Provide a URL to your functional application(s). If login credentials are needed for judges to test the project, add any necessary login credentials and instructions within the Devpost Submission Form.
> - Include a text description that explains the features and functionality of your Project.
> - Include a demonstration video of your Project. The video portion of the Submission: should be less than three (3) minutes. Judges are not required to watch beyond three minutes  should include footage that shows the Project functioning on the device for which it was built must be uploaded to and made publicly visible on YouTube and a link to the video must be provided on the submission form on the Hackathon Website; and must not include third party trademarks, or copyrighted music or other material unless the Entrant has permission to use such material.
> - Provide a public URL to your code repository on GitHub (NOT GitLab or BitBucket) for judging and testing.  The repository must contain all necessary source code, assets, and instructions required for the project to be functional. The repository must be public and open source by including an open source license file. This license should be detectable and visible at the top of the repository page (in the About section). Your repo must contain the /.kiro directory at the root of the project to show usage of Kiro such as specs, hooks, and steering. Do NOT add the /.kiro directory or sub-folders to your .gitignore, as this could disqualify your submission.
> - Identify which category and bonus category you are submitting into. For Skeleton Crew projects only: Your repo must contain 2 separate repo folders for the 2 separate applications.

The license file at the repository root is MIT (`LICENSE`). `.kiro/` is not listed in `.gitignore`. There is no demonstration video in this repository.

The same section also asks for a write-up of how Kiro was used, including specs, hooks, steering, and MCP. `docs/KIRO-CAPABILITY-MATRIX.md` is that inventory for this repository. It does not record a Kiro IDE session.

Quoted from Testing:

> Access must be provided to an Entrant’s working Project for judging and testing by providing a link to a website, functioning demo, or a test build. If Entrant's website is private, Entrant must include login credentials and testing instructions in the designated field of the Submission Form, which is visible only to the Sponsor, Administrator, and Judges. The Entrant must make the Project available free of charge and without any restriction, for testing, evaluation and use by the Sponsor, Administrator and Judges until the Judging Period ends. Judges are not required to test the Project and may choose to judge based solely on the text description, images, and video provided in the Submission.

`python3 demos/haunted/server.py` is the local demo. `site/` is a static build and was not deployed. No login is required. No API key is required.

Quoted from Language Requirements:

> All Submission materials must be in English or, if not in English, the Entrant must provide an English translation of the demonstration video, text description, and testing instructions as well as all other materials submitted.

The README and this file are in English.

## Judging criteria

Quoted from section 6:

> Stage One) The first stage will determine via pass/fail whether the ideas meet a baseline level of viability, in that the Project reasonably fits the theme and reasonably applies the required tools featured in the Hackathon.
>
> Stage Two) All Submissions that pass Stage One will be evaluated in Stage Two based on the following equally weighted criteria (the “Judging Criteria”):
>
> - Potential Impact (20% - 10 points)
> Does the project make a credible case for solving a real problem for a real audience? Does the solution address that problem based on what’s demonstrated? How useful, intuitive, and accessible is it? Would someone actually use this?
> - Technological Implementation (20% - 10 points)
> How thoroughly and skillfully does the project use Kiro? Was there a thoughtful strategy to AI development? Was a variety of Kiro tools used impactfully? Does the project show a deep understanding of Kiro features? Was there experimentation?
> - Design (20% - 10 points)
> Does the project deliver a complete, coherent product experience, not just a technical proof of concept? Is the design intuitive, polished, and intentional?
> - Innovation/Idea (20% - 10 points)
> How creative and novel is the concept, and does the project differ from existing concepts? Are any unusual technologies or public resources (like datasets) leveraged or combined in a unique way?
> - Presentation (20% - 10 points)
> Does the video clearly demonstrate the project working end-to-end? Does the pitch communicate what problem is solved, who it’s for, and why it matters? Is the overall presentation easy to follow? Is the presentation creative and memorable?

This file does not score those criteria. There is no video, and no claim here that a person would use the demo outside the synthetic fixtures.

## What this check did not read

The extractor returned the rules page through the prize and intellectual-property sections. It did not return a separate machine-readable rubric beyond the criteria quoted above. Eligibility exclusions were visible on the overview page as a list of countries and territories. This file does not restate that list and does not give eligibility advice.
