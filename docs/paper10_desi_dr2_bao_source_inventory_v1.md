# DESI DR2 BAO Source Inventory V1

**Doc class:** source-freeze inventory.

**Reader role:** Paper 10 BAO/time-level route auditor.

**Status:** source-side freeze only; not endpoint replay; not validation.

**Canonical parent:** `README.md`.

This inventory freezes the public DESI DR2 Gaussian BAO combined mean and
covariance files as a candidate source route for expanding the present
time-level BAO support. It is deliberately not an endpoint result. It imports
source-side BAO observables and hashes their local raw cache only.

## Files

```text
data/source_manifest/paper10_desi_dr2_bao_source_inventory_policy_v1.csv
data/raw/desi_dr2_bao/desi_gaussian_bao_ALL_GCcomb_mean.txt
data/raw/desi_dr2_bao/desi_gaussian_bao_ALL_GCcomb_cov.txt
data/derived/paper10_desi_dr2_bao_source_inventory_v1.csv
data/derived/paper10_desi_dr2_bao_source_inventory_v1_summary.csv
scripts/build_paper10_desi_dr2_bao_source_inventory_v1.py
scripts/validate_paper10_desi_dr2_bao_source_inventory_v1.py
```

## Source

The source route is the public DESI DR2 BAO likelihood product documented by
the DESI collaboration and distributed through the Cobaya `bao_data`
repository. The BAO publication is DESI DR2 Results II, arXiv:2503.14738.

The cached combined mean file contains 13 BAO rows:

- 6 radial `DH_over_rs` rows,
- 6 transverse `DM_over_rs` rows,
- 1 isotropic `DV_over_rs` row.

The covariance matrix is 13 by 13 and is hash-locked in the derived inventory.

## Claim Boundary

The claim boundary is:

```text
paper10_desi_dr2_bao_source_inventory_not_validation
```

This closes no endpoint-scoring gate by itself. It only shows that the
declared DESI public BAO expansion route is source-identifiable, cacheable, and
hash-lockable, and that it contains enough radial rows to be a candidate input
for a future time-level BAO support replay.

Forbidden inputs remain forbidden:

- Pantheon distance residuals,
- endpoint scores,
- late-time fit parameters,
- posthoc BAO source selection,
- posthoc redshift-bin selection,
- posthoc `r_d` tuning.

## Current Verdict

```text
desi_dr2_public_bao_source_frozen_but_time_level_endpoint_not_replayed
```

The next step is not to claim validation. The next step is to integrate the
frozen DESI rows into the already declared `r_d` nuisance/marginalization and
control-suite protocol, then re-run the readiness gate.
