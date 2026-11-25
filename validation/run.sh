#!/bin/sh
# One local pre-submission run. No model API. No deploy.
set -eu
cd "$(dirname "$0")/.."
if ! python3 -c "import playwright" >/dev/null 2>&1; then
  python3 -m pip install -e ".[validation]"
fi
python3 -m playwright install chromium
if [ ! -f validation/node_modules/axe-core/axe.min.js ] || [ ! -f validation/node_modules/lighthouse/cli/index.js ]; then
  npm install --prefix validation --no-fund --no-audit
fi
python3 -m validation run
