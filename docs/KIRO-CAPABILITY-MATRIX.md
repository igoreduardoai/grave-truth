# Kiro capability matrix

Date: 2026-11-17. This inventory is what is in the repository. This run did not record a Kiro IDE session. The numbers are assertions in the tests named below. They are not a recording of the IDE, and they are not a quality score.

A live model was not called. The evaluator and critic under `validation/adjudication` are scripted simulations, not independent judgment.

## Capabilities

| Capability | Role on the critical path | File that proves it | With | Without | Test |
|---|---|---|---|---|---|
| Steering: cite or abstain | The answer path quotes a span or returns `not found`. A number from another sentence is not used. | `.kiro/steering/cite-or-abstain.md`, enforced by `src/grave_truth/skeleton.py` | 0 of 17 not-found gold cases receive a citation | Quoting the first sentence of the fixture cites 17 of 17 | `tests/test_capability_contrast.py` |
| Specs | Requirements, design, and tasks for the downloadable file name the module the export tests run | `.kiro/specs/workflow-artifact/` (`requirements.md`, `design.md`, `tasks.md`) linked from `.kiro/specs/grave-truth.md` | 3 spec files, and `src/grave_truth/artifact.py` exists | Those paths are absent until added; the export tests fail on import without the module | `tests/test_kiro_loadbearing.py` |
| Hook | After a save that matches the hook, the gold suite and the held-out snapshot are checked. The holdout files are not edited | `.kiro/hooks/gold-holdout-on-save.json` runs `evals/run_gold_and_holdout.py` | Command prints `90/90 passed` and `holdout 7/7`, exit 0 | The command is not started, so this test records 0 new checks from a skipped run | `tests/test_kiro_loadbearing.py` |
| MCP, keyless fixture reader (unexpected) | An editor can list and read the two synthetic documents without an API key. Any other name returns no bytes | `.kiro/settings/mcp.json` and `scripts/fixture_mcp.py` | `sample-eob` returns the fixture text. The byte count equals the file (424 bytes) | `../README.md` and `sample-eob.txt` return 0 bytes and an error | `tests/test_fixture_mcp.py` |

The sponsor pages for this hackathon describe specs, hooks, steering, and MCP as ways to build. The unexpected piece in this repository is the keyless fixture server: it only loads the two synthetic documents the checker already uses, and it is wired as MCP config rather than as a third application.

The 0-of-17 and 17-of-17 counts are the with/without number for the cite-or-abstain rule. The 4 spans on the default workflow files, against 0 spans if those claims are copied with an empty citation list, are measured in the same contrast test.

## What is not claimed

- The code was not shown to have been authored inside the Kiro IDE. The `.kiro/` files are load-bearing for the tests above. That is the evidence.
- No paid model or provider was called.
- The static build in `site/` was not deployed.
