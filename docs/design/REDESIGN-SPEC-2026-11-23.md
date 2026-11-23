# Grave Truth redesign spec (2026-11-23)

Author: Igor Eduardo. Same quality bar as the hackathon design standard v1, with its own dark Kiroween palette.

## What was wrong
- Serif display type (Palatino) at 4rem, an all-caps gold eyebrow, gold pill buttons of equal weight.
- The first screen ended before any result; the result panel said "Ask a question".
- Source, workflow file and buttons had no hierarchy; the dispute-letter link and the build button looked the same as the main action.

## Decisions
- Palette (solid colors only, so the contrast test can resolve every background): bg #0C0C12, surface #15151E, surface-2 #1C1C28, line #2C2C3B, ink #F3F3F6, muted #AEAEBF, primary pumpkin #F59E0B with #1A1205 text, focus #93C5FD. Status: cited #86EFAC on #0F2A1C, ghost #C4B5FD on #1F1B36, rejected #FCA5A5 on #2E1515, mixed #FCD34D on #2B210A.
- Type: Inter (self-hosted `inter.woff2`, OFL), system mono for real code only. No serif, no all-caps.
- Top bar: ghost mark + name + event pill (sentence case).
- Hero: one sentence claim, one line of lede, three numbered step cards (Input, Check, Result).
- Result first: the default question is answered on page load (no focus jump), so the cited verdict and the highlighted clause are on the first screen. On phones the result card moves above the form and the step cards hide.
- One primary action: "Check grounding" (full-width pumpkin). Download and Build are secondary outline buttons. Presets are small chips under an "Examples" label.
- Document picker is a segmented control.
- Workflow file is a bounded, focusable scroll box.

## Not changed
Grounding library, server routes (one new static route for the font file), hosted-copy anchors, judge mode, evals, gold and holdout files.
