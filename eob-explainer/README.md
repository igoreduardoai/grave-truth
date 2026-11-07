# EOB explainer

One of the two Grave Truth applications. It answers questions about `fixtures/sample_eob.txt` by quoting a span from that synthetic explanation of benefits.

This is a research demo. It is not a medical device and not a coverage decision. The clinic, dates, and dollar amounts are invented.

```bash
python3 eob-explainer/main.py
python3 eob-explainer/main.py "How much did the plan pay?"
```

Run these from the repository root. The script uses the shared skeleton in `src/grave_truth`. The haunted demo in `demos/haunted/` uses this same loader.
