# KiDS-1000 COSEBIs `F_overlap` Filled Execution Review Validator v1

This utility validates a future filled execution-review artifact against the
frozen execution-review schema and the committed batch-0 dry-run rows.

Template smoke test:

```bash
python scripts/validate_kids1000_cosebis_f_overlap_filled_execution_review_artifact_v1.py \
  --input data/derived/kids1000_cosebis_f_overlap_execution_review_template_v1.csv \
  --mode template
```

Future filled review check:

```bash
python scripts/validate_kids1000_cosebis_f_overlap_filled_execution_review_artifact_v1.py \
  --input path/to/filled_review.csv \
  --mode filled
```

The filled mode requires matching batch identity, URL, and cache-path columns,
`fetch_mode=execute`, `fetch_status=fetched`, HTTP 200, positive byte count,
lowercase SHA-256, fetched timestamp, reviewer role, and a source-freeze review
status. It rejects any artifact that contains KiDS data-vector values,
posterior-chain use, residuals, fit-improvement flags, post-hoc tile selection,
overlap-rule computation, mapping vectors, theory vectors, predictions, fit
statistics, or endpoint scoring.
