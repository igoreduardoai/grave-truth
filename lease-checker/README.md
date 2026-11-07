# Lease checker

One of the two Grave Truth applications. It answers questions about `fixtures/sample_lease.txt` by quoting a span from that synthetic residential lease.

This is a research demo. It is not legal advice and not a review of a real tenancy. The address, dates, and dollar amounts are invented. Rent and the security deposit are both `$1,850.00` on purpose, so the checker has to cite the clause that names the subject.

```bash
python3 lease-checker/main.py
python3 lease-checker/main.py "What is the security deposit?"
```

Run these from the repository root. The script uses the shared skeleton in `src/grave_truth`. The haunted demo in `demos/haunted/` uses this same loader. A Portuguese question does not match these English clauses.
