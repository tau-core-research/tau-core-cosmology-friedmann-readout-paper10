# Paper 10 time-level route external-r_d readiness gate v1

**Doc class:** source-side readiness/closure gate
**Status:** not endpoint replay, not validation
**Canonical parent:** Paper 10 external r_d prior freeze response

This gate checks what changes after the Planck2018 \(r_d\) source-freeze
response.

Closed source-side blockers:

```text
external_rd_prior_source_freeze
joint_rd_marginalization_protocol_definition
endpoint_control_suite_definition
bao_support_expansion_manifest_declared
desi_dr2_public_bao_source_inventory_frozen
desi_dr2_radial_bao_time_interface_frozen
desi_dr2_radial_bao_cc_match_ledger_frozen
desi_dr2_high_z_row_policy_frozen
desi_time_level_control_seed_manifest_frozen
```

Retained diagnostic, not an active DESI endpoint blocker:

```text
low_significance_current_sdss_bao_difference
```

Remaining endpoint blocker:

```text
time_level_endpoint_authorization_review_missing
```

Therefore the external-prior and marginalization-interface pieces are
source-side ready, the endpoint-control family list is declared, the future
BAO-support expansion routes are predeclared, and the deterministic control
seeds for the first five-row DESI/CC-matched route are frozen. The DESI DR2
public BAO source inventory is frozen source-side, with six candidate radial
`DH_over_rs` rows and a 13 by 13 covariance block.
The DESI radial BAO time-level interface is also frozen source-side, converting
the six `DH_over_rs` rows into `-log(DH_over_rs)=logH+beta_rd` and propagating
the radial covariance subblock.
The DESI radial BAO to cosmic-chronometer support ledger is frozen source-side:
five rows match within the frozen CC redshift range, while the `z=2.33` row is
blocked as outside CC coverage with no extrapolation.

The high-redshift `z=2.33` DESI Ly-alpha row now has a predeclared policy:
exclude it from the first CC-matched endpoint and retain it as high-z holdout or
future independent-clock support. The control seed manifest freezes seven
control families over the first five-row DESI/CC-matched route with deterministic
seeds 41001--41007.

The time-level route is still not endpoint-ready because no endpoint
authorization/replay review has been completed. The older two-point SDSS-only
BAO difference also remains recorded as a low-significance diagnostic, but it is
not an active blocker for the DESI route.

Updated remaining blockers:

```text
time_level_endpoint_authorization_review_missing
```

Updated verdict:

```text
desi_time_cc_matched_scope_and_controls_frozen_but_endpoint_authorization_missing
```
