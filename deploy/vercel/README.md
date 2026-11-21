# Vercel demo (free Hobby tier)

Public URL: https://grave-truth.vercel.app/ (judge link: https://grave-truth.vercel.app/?judge=1, health: https://grave-truth.vercel.app/health).

The hosted demo runs `demos/haunted/server.py` unchanged inside one Python function. `api/index.py` only restores the original request path, because `vercel.json` rewrites every path to `/api/index?__p=<path>`. There is no model call, no API key, and no database.

Deployed on 2026-11-21 from the PR #9 branch `cursor/mid-gate-demo-pages-10eb` (head `2aa041f`), not from `main`.

To redeploy, copy `src/`, `demos/`, `fixtures/`, `docs/` and `LICENSE` next to `api/` and `vercel.json` in a scratch folder, add an empty `requirements.txt`, and run `vercel deploy --prod --name grave-truth` there.

Note: the hosted page still carries the local-only wording ("LOCAL ONLY", "Nothing is sent off this machine"). On this host a pasted document is posted to the Vercel function and is not stored. That copy should be updated before submission.
