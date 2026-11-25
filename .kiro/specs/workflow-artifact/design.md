# Design: workflow file

`build_artifact` in `src/grave_truth/artifact.py` loads the sample bill or the sample lease through the existing app loaders. Those loaders ingest the fixture with `DocumentAgent`.

For each fixed claim, the function calls `reject_ungrounded_claim`. Only when that returns false, and `answer` returns a found, non-conflict result with citations, does the claim become `cited`. Otherwise the verdict is `not_found` and the citation list is empty. A rejected claim is not replaced with a different figure from `answer`.

The markdown is a pure function of those items. It has no timestamp. `GET /api/export` on `demos/haunted/server.py` returns that JSON, or the markdown when `format=markdown`. `GET /health` returns `HEALTH_BODY` from `src/grave_truth/health.py`.

`?judge=1` in `demos/haunted/app.js` posts the synthetic bill check and then requests the export. `scripts/build_static.py` writes `site/`, including a pre-rendered `judge.html`, and does not deploy it.

The on-save hook `.kiro/hooks/gold-holdout-on-save.json` runs `evals/run_gold_and_holdout.py`. That command runs the gold suite and compares `evals/holdout_observed.json`. It does not write the holdout files.

`.kiro/settings/mcp.json` starts `scripts/fixture_mcp.py`, which serves two fixture names and refuses every other name. No API key is read.
