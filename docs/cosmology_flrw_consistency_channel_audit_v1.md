# FLRW Consistency Channel Audit v1

Paper 10 now records how each declared Tau Core cosmology channel touches the
standard FLRW-consistency problem.

This is not a new score and not a validation claim. It is a leakage-prevention
and model-discipline artifact: a cosmology residual must state whether it is
acting on optical/path readout, expansion/time readout, density reconstruction,
or the single-FLRW-geometry assumption.

## Manifest

```text
data/source_manifest/cosmology_flrw_consistency_channel_audit_v1.csv
```

## Axis Mapping

| Channel | Primary FLRW-consistency axis |
| --- | --- |
| `W_VOID_MATURITY` | density reconstruction |
| `W_WEB_ANISOTROPY` | density reconstruction |
| `W_PATH_PROJECTION` | distance / optical path readout |
| `W_TIME_READOUT` | expansion / time readout |

The four channels together also touch the single-FLRW-geometry assumption, but
that does not permit a single flexible absorber. Each channel still needs its
own source freeze, null controls, and baseline comparison.

## Required Controls

The manifest requires comparison against conventional absorbers such as:

```text
FLRW curvature
backreaction
ordinary dark energy
distance-expansion consistency violations
calibration / nuisance shifts
reconstruction instability
wrong-channel and shuffled controls
```

## Claim Boundary

Every row remains:

```text
current_status=FLRW_AXIS_DECLARED_NOT_SCORED
endpoint_scoring_allowed=false
physical_validation_claimed=false
```

The audit sharpens Paper 10's future endpoint design, but it does not close any
physical-promotion blocker.
