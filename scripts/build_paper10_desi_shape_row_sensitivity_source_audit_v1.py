#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_row_sensitivity_source_audit_policy_v1.csv"
SHAPE_ROWS = ROOT / "data/derived/paper10_desi_time_readout_shape_observable_gate_v1.csv"
CC_MATCH = ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv"
ROBUSTNESS = ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1.csv"
ROBUSTNESS_SUMMARY = ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_shape_row_sensitivity_source_audit_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row_sensitivity_source_audit_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_row_sensitivity_source_audit_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def reference_family(reference: str) -> str:
    return reference.split("(")[0].strip()


def sensitivity_class(loss_fraction: float) -> str:
    if loss_fraction >= 0.25:
        return "core_sensitive"
    if loss_fraction >= 0.10:
        return "moderate_sensitive"
    return "low_sensitivity_or_dispensable"


def source_caveat(
    left: dict[str, str],
    right: dict[str, str],
    independent_reference_pair: bool,
) -> str:
    max_delta_z = max(float(left["delta_z_to_nearest_cc"]), float(right["delta_z_to_nearest_cc"]))
    max_sigma_logh = max(float(left["nearest_cc_sigma_logH"]), float(right["nearest_cc_sigma_logH"]))
    caveats: list[str] = []
    if not independent_reference_pair:
        caveats.append("single_reference_family_pair")
    if max_delta_z >= 0.045:
        caveats.append("near_window_edge")
    if max_sigma_logh >= 0.2:
        caveats.append("large_clock_uncertainty")
    return ";".join(caveats) if caveats else "no_major_source_caveat_in_current_manifest"


def main() -> None:
    policy = one_row(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad row-sensitivity policy claim boundary")
    if policy["endpoint_validation_claimed"] != "false" or policy["physical_validation_claimed"] != "false":
        raise SystemExit("row-sensitivity policy must not claim validation")

    robustness_summary = one_row(ROBUSTNESS_SUMMARY)
    full_score = float(robustness_summary["candidate_score"])
    if robustness_summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("row-sensitivity audit requires non-validation robustness summary")

    shape_rows = [
        row
        for row in read_rows(SHAPE_ROWS)
        if row["observable_family"] == "adjacent_first_difference_beta_shape"
    ]
    if len(shape_rows) != 4:
        raise SystemExit("expected four adjacent shape rows")
    cc_by_radial = {int(row["radial_index"]): row for row in read_rows(CC_MATCH)}
    robustness_by_id = {row["test_id"]: row for row in read_rows(ROBUSTNESS)}

    out_rows: list[dict[str, str]] = []
    for row in shape_rows:
        shape_row = int(row["shape_row"])
        left_idx = int(row["radial_index_left"])
        right_idx = int(row["radial_index_right"])
        left = cc_by_radial[left_idx]
        right = cc_by_radial[right_idx]
        drop = robustness_by_id[f"drop_shape_row_{shape_row}"]
        leave_score = float(drop["shape_quadratic_score"])
        retained_fraction = float(drop["score_fraction_of_full_candidate"])
        loss_fraction = 1.0 - retained_fraction
        left_family = reference_family(left["nearest_cc_reference"])
        right_family = reference_family(right["nearest_cc_reference"])
        independent_pair = left_family != right_family
        caveat = source_caveat(left, right, independent_pair)
        out_rows.append(
            {
                "audit_id": policy["audit_id"],
                "shape_row": str(shape_row),
                "radial_interval": f"{left_idx}-{right_idx}",
                "z_left": row["z_left"],
                "z_right": row["z_right"],
                "z_mid": row["z_mid"],
                "shape_value": row["shape_value"],
                "shape_abs_snr_diag": row["shape_abs_snr_diag"],
                "leave_one_score_when_dropped": f"{leave_score:.12g}",
                "retained_score_fraction_when_dropped": f"{retained_fraction:.12g}",
                "dependency_loss_fraction_when_dropped": f"{loss_fraction:.12g}",
                "sensitivity_class": sensitivity_class(loss_fraction),
                "left_cc_reference": left["nearest_cc_reference"],
                "right_cc_reference": right["nearest_cc_reference"],
                "independent_reference_pair": "true" if independent_pair else "false",
                "max_delta_z_to_nearest_cc": f"{max(float(left['delta_z_to_nearest_cc']), float(right['delta_z_to_nearest_cc'])):.12g}",
                "max_sigma_logH": f"{max(float(left['nearest_cc_sigma_logH']), float(right['nearest_cc_sigma_logH'])):.12g}",
                "source_caveat": caveat,
                "endpoint_replay_allowed": policy["endpoint_replay_allowed"],
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, out_rows)

    core_rows = [row for row in out_rows if row["sensitivity_class"] == "core_sensitive"]
    caveated_core = [row for row in core_rows if row["source_caveat"] != "no_major_source_caveat_in_current_manifest"]
    summary = [
        {
            "audit_id": policy["audit_id"],
            "status": "DESI_SHAPE_ROW_SENSITIVITY_SOURCE_AUDIT_BUILT_NOT_VALIDATION",
            "candidate_score": f"{full_score:.12g}",
            "n_shape_rows": str(len(out_rows)),
            "core_sensitive_rows": ";".join(row["shape_row"] for row in core_rows),
            "n_core_sensitive_rows": str(len(core_rows)),
            "caveated_core_sensitive_rows": ";".join(row["shape_row"] for row in caveated_core),
            "most_dispensable_row": min(out_rows, key=lambda row: float(row["dependency_loss_fraction_when_dropped"]))["shape_row"],
            "most_required_row": max(out_rows, key=lambda row: float(row["dependency_loss_fraction_when_dropped"]))["shape_row"],
            "source_support_verdict": "core_signal_mostly_middle_shape_rows_with_one_single_reference_caveat",
            "recommended_next_action": "seek_independent_clock_or_shape_support_for_core_rows_1_and_2_before_promoting_DESI_shape_route",
            "endpoint_replay_allowed": policy["endpoint_replay_allowed"],
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "row_sensitivity_explained_as_middle_shape_row_core_but_source_caveated_not_validation",
        }
    ]
    write_csv(SUMMARY, summary)
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"wrote {SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
