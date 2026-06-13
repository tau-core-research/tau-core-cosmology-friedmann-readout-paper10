# DESI DR2 Radial BAO Time-Level Interface V1

**Doc class:** source-side time-level observable interface.

**Reader role:** Paper 10 time/readout route auditor.

**Status:** source-side interface only; not endpoint replay; not validation.

**Canonical parent:** `paper10_desi_dr2_bao_source_inventory_v1.md`.

This artifact converts the source-frozen DESI DR2 radial BAO rows into the
time-level observable used by the Paper 10 route:

```text
y := -log(D_H / r_d) = log H(z) + beta_rd
beta_rd := log(r_d) - log(c)
```

The nuisance parameter `beta_rd` is not treated as a Tau Core signal. It must
be handled later by the frozen `r_d` marginalization/prior protocol.

## Files

```text
data/source_manifest/paper10_desi_dr2_radial_bao_time_interface_policy_v1.csv
data/derived/paper10_desi_dr2_radial_bao_time_interface_v1.csv
data/derived/paper10_desi_dr2_radial_bao_time_interface_covariance_v1.csv
data/derived/paper10_desi_dr2_radial_bao_time_interface_v1_summary.csv
scripts/build_paper10_desi_dr2_radial_bao_time_interface_v1.py
scripts/validate_paper10_desi_dr2_radial_bao_time_interface_v1.py
```

## Covariance Transform

For each radial row \(x_i = D_H/r_d\), the transformed observable is
\(y_i=-\log x_i\). First-order covariance propagation uses

```text
C_y,ij = C_x,ij / (x_i x_j)
```

because the Jacobian is \(J_i=-1/x_i\). This preserves the radial DESI
covariance subblock in the transformed source-side interface.

## Current Verdict

```text
desi_radial_bao_time_interface_frozen_but_endpoint_replay_still_blocked
```

The interface contains six radial rows and a 6 by 6 transformed covariance
block. Endpoint replay remains blocked until matched CC support, `r_d`
nuisance handling, and a predeclared control seed manifest are all present.
