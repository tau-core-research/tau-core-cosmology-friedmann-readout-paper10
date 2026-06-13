# Low-z Pantheon+ W-time uncertainty-basis gate status ledger v1

**Doc class:** gate status ledger
**Status:** non-scoring; not validation
**Canonical parent:** `docs/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_v1.md`

This ledger records whether the `W_time_uncertainty_basis` path is ready for a
permission-only replay.

The current expected state is:

```text
G1 source-side W_time basis: pass
G2 reviewer package: pass
G3 completed reviewer response: blocked until external GO CSV is imported
G4 replay run template: ready but locked by G3
```

Run:

```bash
python scripts/build_low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1.py
python scripts/validate_low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1.py
```

Outputs:

- `data/derived/low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1.csv`
- `data/derived/low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1_summary.csv`

Claim boundary:

```text
w_time_uncertainty_basis_gate_status_ledger_not_scoring_not_validation
```
