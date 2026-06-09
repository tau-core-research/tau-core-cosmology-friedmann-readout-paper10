#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_null_replay_v1.csv"
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_null_replay_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_null_replay_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    manifest = read_one(RUN_MANIFEST)
    summary = read_one(SUMMARY)
    with GRID.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if manifest["status"] != "PARTIAL_CONTROL_NULL_REPLAY_NOT_ENDPOINT_VALIDATION":
        raise SystemExit("unexpected null replay status")
    if manifest["partial_control_scoring_allowed"] != "true":
        raise SystemExit("null replay must explicitly allow partial-control scoring")
    if manifest["endpoint_scoring_allowed"] != "false":
        raise SystemExit("null replay must keep endpoint scoring disabled")
    if summary["status"] != manifest["status"]:
        raise SystemExit("null replay summary status mismatch")
    if summary["claim_boundary"] != "partial_control_null_replay_not_endpoint_not_validation":
        raise SystemExit("unexpected null replay claim boundary")
    if summary["endpoint_scoring_allowed"] != "false" or summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("null replay must not claim endpoint validation")
    if summary["uses_kids_data_vector_values_for_scoring"] != "true":
        raise SystemExit("null replay must disclose KiDS data-vector scoring use")
    if summary["uses_kids_data_vector_values_for_source_selection"] != "false":
        raise SystemExit("null replay must not use KiDS data vector for source selection")
    if summary["uses_posterior_chains"] != "false" or summary["uses_posthoc_selection"] != "false":
        raise SystemExit("null replay must not use posterior chains or posthoc selection")
    if int(summary["null_draws"]) != 1008 or len(rows) != 1008:
        raise SystemExit("null replay must contain 1008 draws")
    families = {row["control_family"] for row in rows}
    expected = {
        "sky_rotation",
        "tomographic_pair_shuffle",
        "wrong_channel_activation",
        "web_path_sign_flip",
    }
    if families != expected:
        raise SystemExit("null replay family set mismatch")
    counts = {family: sum(row["control_family"] == family for row in rows) for family in families}
    if counts["sky_rotation"] != 4:
        raise SystemExit("sky rotation draw count mismatch")
    if counts["tomographic_pair_shuffle"] != 1000:
        raise SystemExit("pair shuffle draw count mismatch")
    if counts["wrong_channel_activation"] != 2:
        raise SystemExit("wrong-channel draw count mismatch")
    if counts["web_path_sign_flip"] != 2:
        raise SystemExit("sign-flip draw count mismatch")
    observed_chi2 = float(summary["observed_chi2"])
    observed_aic = float(summary["observed_aic"])
    chi2_le = sum(float(row["chi2"]) <= observed_chi2 + 1e-10 for row in rows)
    aic_le = sum(float(row["aic"]) <= observed_aic + 1e-10 for row in rows)
    if chi2_le != int(summary["null_chi2_le_observed_count"]):
        raise SystemExit("chi2 tail count mismatch")
    if aic_le != int(summary["null_aic_le_observed_count"]):
        raise SystemExit("AIC tail count mismatch")
    expected_chi2_tail = (chi2_le + 1) / (len(rows) + 1)
    expected_aic_tail = (aic_le + 1) / (len(rows) + 1)
    if abs(float(summary["plus_one_tail_fraction_chi2_le_observed"]) - expected_chi2_tail) > 5e-13:
        raise SystemExit("chi2 plus-one tail mismatch")
    if abs(float(summary["plus_one_tail_fraction_aic_le_observed"]) - expected_aic_tail) > 5e-13:
        raise SystemExit("AIC plus-one tail mismatch")
    best = min(rows, key=lambda row: float(row["chi2"]))
    if summary["best_null_family"] != best["control_family"]:
        raise SystemExit("best null family mismatch")
    for row in rows:
        if row["claim_boundary"] != summary["claim_boundary"]:
            raise SystemExit("grid claim boundary mismatch")
        if row["endpoint_scoring_allowed"] != "false":
            raise SystemExit("grid endpoint scoring must remain disabled")
        if row["uses_kids_data_vector_values_for_scoring"] != "true":
            raise SystemExit("grid must disclose KiDS data-vector scoring use")
        if row["uses_kids_data_vector_values_for_source_selection"] != "false":
            raise SystemExit("grid must not use KiDS data vector for source selection")
        if row["uses_posterior_chains"] != "false" or row["uses_posthoc_selection"] != "false":
            raise SystemExit("grid must not use posterior chains or posthoc selection")
        if float(row["best_nonnegative_amplitude"]) < 0:
            raise SystemExit("null replay amplitudes must be nonnegative")
    for marker in [
        "kids_data_vector_values_for_source_selection",
        "posterior_chains",
        "lensing_residuals_for_source_or_branch_selection",
        "posthoc_mask_subset_selection",
        "posthoc_weight_selection",
    ]:
        if marker not in manifest["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input marker: {marker}")
    print(
        "PAPER10_KIDS1000_COSEBIS_PARTIAL_CONTROL_NULL_REPLAY_V1_VALIDATED "
        f"chi2_tail_fraction={summary['plus_one_tail_fraction_chi2_le_observed']} "
        "endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
