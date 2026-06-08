# Cosmology Source-Grounding Gate v1

Paper 10 now separates three levels:

```text
source-frozen proxy
    -> activation-rule shell
    -> source-grounded Tau-side readout source
```

The first two levels already exist in the channel and activation-rule manifests.
This gate records what is still required for the third level.

## Manifest

```text
data/source_manifest/cosmology_source_grounding_gate_v1.csv
```

The manifest is deliberately non-numeric. It does not score data and it does
not validate a Tau Core cosmological signal. It records, for each channel,
the four projection-induction checks that must eventually be discharged:

```text
activation candidate
    -> quotient survival test
    -> closure stability test
    -> 4D readout survival test
```

## Channel Status

| Channel | Current source-grounding status |
| --- | --- |
| `W_VOID_MATURITY` | `SOURCE_GROUNDING_GATE_DECLARED_NOT_DERIVED` |
| `W_WEB_ANISOTROPY` | `SOURCE_GROUNDING_GATE_DECLARED_NOT_DERIVED` |
| `W_PATH_PROJECTION` | `SOURCE_GROUNDING_GATE_DECLARED_NOT_DERIVED` |
| `W_TIME_READOUT` | `SOURCE_GROUNDING_GATE_DECLARED_NOT_DERIVED` |

This status is intentional. The paper can audit source-freeze discipline and
pilot scoring infrastructure, but it does not claim that any of the four
channels has already been derived as a Tau-side cosmological closure source.

## Claim Boundary

The source-grounding gate prevents over-reading a successful future score. A
future endpoint result would still need to say which level has passed:

```text
source-frozen endpoint signal
source-grounded channel signal
full Tau-side cosmology derivation
```

Only the first is within reach of the current Paper 10 scaffold.

## Forbidden Inputs

The gate repeats the leakage protections from the channel manifests. Distance,
growth, lensing, CMB residuals, fit-improvement flags, and post-hoc labels
cannot be used to select activation candidates, quotient rules, closure tests,
or readout-survival maps.
