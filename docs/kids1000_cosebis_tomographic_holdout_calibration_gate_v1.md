# KiDS-1000 COSEBIs Tomographic Holdout Calibration Gate V1

**Doc class:** validation-facing source-freeze gate  
**Reader role:** reviewer-facing next-step protocol after tomographic controls  
**Status:** future replay gate; no new score and no validation claim  
**Canonical parent:** `README.md`

## Purpose

The KiDS COSEBIs endpoint candidate is a low-tail diagnostic signal, but it is
not an absolute winner under stricter tomographic controls. The plausibility
audit found that better tomographic controls are not accepted as physical
alternatives in the present source state. They still block validation because
one conditional source-systematic route would require independent
photometric-redshift or tomographic-calibration support.

This gate freezes what must happen before any new endpoint replay can be used
as validation-facing evidence.

## Rule

No endpoint replay is authorized by this gate. Before a replay, a later manifest
must independently freeze:

- the photometric-redshift or tomographic-calibration evidence,
- the source-bin or tomographic-pair holdout partition,
- the rule for promoting a tomographic control to a source-systematic candidate,
- the replay candidate, null controls, amplitude rule, and covariance policy,
- a leakage validator that forbids endpoint residuals, \(\Delta\chi^2\), null
  ranks, and post-score residual shapes from entering source selection.

## Forbidden fields

The source-side holdout and calibration manifests may not use:

- observed COSEBIs values,
- endpoint residuals,
- \(\Delta\chi^2\),
- null-control rank,
- best-control identity,
- post-score residual shape.

## Verdict

`tomographic_holdout_required_before_endpoint_replay_or_validation`

In plain terms, the current signal survives as a diagnostic endpoint signal, but
the next replay must be preceded by an independent source-side tomographic
holdout/calibration freeze. Until then, the KiDS branch remains diagnostic and
not validated.
