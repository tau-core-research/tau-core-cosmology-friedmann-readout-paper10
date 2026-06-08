# Multi-Probe Full-Covariance Scoring Plan v1

The current Paper 10 pilots are full-covariance only within the Pantheon+
distance block. The target endpoint is stricter:

```text
distance + growth + lensing + CMB-safety
```

under one predeclared covariance/likelihood grammar.

## Required Blocks

| Block | Required before scoring |
| --- | --- |
| Distance | Pantheon+/DESI/SNe/H(z) row rule and covariance policy |
| Void | source-frozen void maturity catalogue and mask |
| Web | source-frozen cosmic-web/environment labels |
| Growth | RSD/growth compilation with covariance or documented diagonal policy |
| Lensing | weak-lensing/CMB-lensing product with mask and covariance policy |
| CMB safety | early-universe prior/safety summary, not post-hoc residual map selection |

## Channel Order

The staged order remains:

```text
1. W_void + W_web
2. add W_path only after path source products are frozen
3. add W_time only after non-overlapping clock/readout evidence is frozen
4. run multi-probe full-covariance scoring
```

## Claim Boundary

The present repository has not reached this endpoint. The two-channel
Pantheon-only pilot is a scoring-grammar stress test. It cannot validate the
multi-probe Tau Core cosmology hypothesis.
