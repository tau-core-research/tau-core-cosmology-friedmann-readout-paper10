# KiDS-1000 COSEBIs Null-Control Theory Replay v1

This artifact executes the predeclared null-control transformations against the
source-frozen unit-amplitude COSEBIs theory-vector shell.

It is not endpoint scoring. It does not compare against the KiDS data vector,
does not compute residuals, and does not compute control scores. Instead, it
records a compact replay index for the future endpoint scorer:

- 4 sky-rotation proxy controls, represented as deterministic cyclic
  tomographic-pair shifts;
- 1000 seeded tomographic-pair shuffles;
- 2 wrong-channel zero controls;
- 2 web/path sign or removal controls.

For each replay control the artifact stores the deterministic operator, seed,
basic vector statistics, and a SHA-256 digest of the regenerated 300-row control
theory vector. This keeps the null-control family reproducible without storing a
large control matrix.

Claim boundary:

```text
kids1000_cosebis_null_control_theory_replay_not_scoring_not_validation
```
