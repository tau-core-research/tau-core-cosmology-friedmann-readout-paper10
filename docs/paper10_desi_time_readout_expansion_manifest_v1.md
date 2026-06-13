# DESI Time-Readout Expansion Manifest V1

**Doc class:** source-side expansion manifest.

**Reader role:** Paper 10 time-level route auditor.

**Status:** source-side requirements frozen; not endpoint replay; not
validation.

**Canonical parent:** `paper10_desi_time_level_negative_control_response_gate_v1.md`.

The first DESI/chronometer five-row constant-\(\beta_{r_d}\) replay was useful
as a negative-control diagnostic but was not control-resistant. This manifest
freezes what must be added before the DESI time-level route can be considered
for any future permission-only replay.

## Required Expansion Routes

```text
HIGH_Z_INDEPENDENT_CLOCK_SUPPORT
MULTI_CLOCK_SUPPORT_PER_BAO_ROW
TIME_READOUT_SHAPE_OBSERVABLE
ORDERING_CONTROL_SUITE
JOINT_COVARIANCE_AND_NUISANCE_POLICY
```

## Current Readiness

The manifest validates with:

```text
endpoint_ready_route_count = 0
missing_support_count = 3
partial_support_count = 2
```

The next primary source gate is:

```text
HIGH_Z_INDEPENDENT_CLOCK_SUPPORT
```

The next parallel source gate is:

```text
TIME_READOUT_SHAPE_OBSERVABLE
```

## Interpretation

This manifest prevents the failed five-row route from being reopened by
post-hoc row selection, smoothing, or nuisance retuning. A future DESI
time-level endpoint attempt must first source-freeze additional independent
clock support and a time/readout observable that is more informative than a
constant level offset.

## Artifacts

```text
data/source_manifest/paper10_desi_time_readout_expansion_manifest_v1.csv
data/derived/paper10_desi_time_readout_expansion_manifest_v1_summary.csv
scripts/validate_paper10_desi_time_readout_expansion_manifest_v1.py
```

## Claim Boundary

```text
paper10_desi_time_readout_expansion_manifest_not_validation
```
