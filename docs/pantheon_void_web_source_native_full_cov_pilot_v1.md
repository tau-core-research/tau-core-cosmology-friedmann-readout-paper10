# Pantheon Void/Web Source-Native Full-Covariance Pilot V1

This pilot repeats the previous `W_void + W_web` full-covariance scoring
grammar, but replaces the redshift/scale-factor proxy bases with source-native
columns from:

- the VAST/SDSS DR7 Planck2018 maximal-void table,
- the SDSS DR17 MCPM SlimeMold galaxy catalogue.

It is run by:

```bash
python scripts/run_pantheon_void_web_source_native_full_cov_pilot_v1.py
python scripts/validate_pantheon_void_web_source_native_full_cov_pilot_v1.py
```

## Claim Boundary

This remains:

```text
VOID_WEB_SOURCE_NATIVE_FULL_COV_PILOT_NOT_VALIDATION
```

It is distance-only, Pantheon-only, and still disables `W_path` and `W_time`.
It is not a void/web detection, not empirical validation of Tau Core cosmology,
and not a replacement for a multi-probe analysis.

## Current Result

The current frozen run gives:

```text
Delta chi2(source-native void+web - baseline) = -0.50848549
Delta AIC(source-native void+web - baseline)  = +3.49151451
```

The source-native branch therefore improves chi-square more than the earlier
proxy branch, but still loses under AIC. The deterministic shuffled control also
achieves a lower chi-square than the matched source-native branch. This is a
model-selection negative result for the present distance-only shell, not a true
negative against the broader multi-probe Tau Core cosmology audit.
