#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBSERVER_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv"
SKY_Z_AUDIT = ROOT / "data/derived/void_source_basis_refinement_v2_sky_z_source_audit_v1.csv"
METRIC_PATH_AUDIT = ROOT / "data/derived/low_z_pantheon_metric_lensing_path_route_audit_v1.csv"
LIFT_SUMMARY = ROOT / "data/derived/joint_non_lensing_lift_diagnostic_v1_summary.csv"
OUT = ROOT / "data/derived/observer_path_strengthening_gate_v1.csv"
SUMMARY = ROOT / "data/derived/observer_path_strengthening_gate_v1_summary.csv"
DOC = ROOT / "docs/observer_path_strengthening_gate_v1.md"
CLAIM_BOUNDARY = "observer_path_strengthening_gate_source_side_not_endpoint"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
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


def main() -> None:
    observer = read_one(OBSERVER_SUMMARY)
    sky_rows = read_rows(SKY_Z_AUDIT)
    metric_rows = read_rows(METRIC_PATH_AUDIT)
    lift = read_one(LIFT_SUMMARY)
    scope_indices = set(observer["source_row_indices"].split(";"))
    metric_scope = [row for row in metric_rows if row["source_row_index"] in scope_indices]
    metric_status = Counter(row["path_weight_value_status"] for row in metric_scope)
    coverage = Counter(row["crossmap_candidate_status"] for row in sky_rows)

    current_delta_control = float(observer["delta_chi2_candidate_minus_best_control"])
    required_lift = float(lift["required_lift_to_zero"])
    source_aligned_metric_count = sum(
        1 for row in metric_scope if row["metric_lensing_numeric_product_available_for_source"] == "true"
    )

    rows = [
        {
            "gate_id": "OBSERVER_PATH_STRENGTHENING_GATE_V1",
            "route_id": "retain_current_observer_basis",
            "route_status": "ACCEPT_AS_CURRENT_NARROW_SOURCE_FROZEN_ROUTE",
            "source_basis": "W_path_x_sky_x_x_zcenter",
            "evidence": f"survives_controls_delta_chi2={current_delta_control:.12g}",
            "allowed_next_action": "keep_as_current_joint_channel",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "OBSERVER_PATH_STRENGTHENING_GATE_V1",
            "route_id": "observer_orientation_centered_sky_z",
            "route_status": "ACCEPT_AS_SOURCE_SIDE_CONTROL_OR_SECONDARY_ROUTE_ONLY",
            "source_basis": "W_path_times_centered_sky_z",
            "evidence": f"sky_z_rows={len(sky_rows)};coverage={dict(coverage)}",
            "allowed_next_action": "use_as_control_or_predeclared_secondary_channel_before_replay",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "OBSERVER_PATH_STRENGTHENING_GATE_V1",
            "route_id": "metric_lensing_path_weight",
            "route_status": "BLOCKED_FOR_ENDPOINT_UNTIL_SOURCE_ALIGNED_NUMERIC_PRODUCT",
            "source_basis": "kappa_or_shear_or_mass_map_integral_along_path",
            "evidence": f"scope_rows={len(metric_scope)};source_aligned_metric_count={source_aligned_metric_count};status={dict(metric_status)}",
            "allowed_next_action": "acquire_source_aligned_metric_lensing_product_or_keep_disabled",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "OBSERVER_PATH_STRENGTHENING_GATE_V1",
            "route_id": "joint_non_lensing_lift_target",
            "route_status": "DIAGNOSTIC_TARGET_NOT_A_KERNEL",
            "source_basis": "joint_non_lensing_lift_diagnostic",
            "evidence": f"required_lift_to_zero={required_lift:.12g};highest_priority={lift['highest_lift_priority_channel']}",
            "allowed_next_action": "strengthen_observer_path_source_basis_without_residual_tuning",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    verdict = (
        "OBSERVER_PATH_CAN_BE_STRENGTHENED_SOURCE_SIDE_BUT_FULL_METRIC_PATH_REMAINS_BLOCKED_NOT_VALIDATION"
        if source_aligned_metric_count == 0
        else "OBSERVER_PATH_HAS_SOURCE_ALIGNED_METRIC_PATH_CANDIDATES_REVIEW_REQUIRED_NOT_VALIDATION"
    )
    summary = {
        "gate_id": "OBSERVER_PATH_STRENGTHENING_GATE_V1",
        "current_observer_family": observer["active_family"],
        "current_family_survives_controls": observer["family_survives_controls"],
        "current_delta_chi2_candidate_minus_best_control": observer["delta_chi2_candidate_minus_best_control"],
        "required_non_lensing_lift_to_zero": lift["required_lift_to_zero"],
        "sky_z_source_rows": str(len(sky_rows)),
        "metric_path_scope_rows": str(len(metric_scope)),
        "metric_path_source_aligned_numeric_count": str(source_aligned_metric_count),
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "verdict": verdict,
        "recommended_next_action": "prepare_source_aligned_observer_path_candidate_review_or_acquire_metric_lensing_products",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Observer/path strengthening gate v1",
                "",
                "**Doc class:** source-side strengthening gate",
                "**Status:** not endpoint replay; not validation",
                "",
                "This gate translates the joint non-lensing lift diagnostic into a",
                "source-side action plan for the current observer/path channel. It keeps",
                "the current narrow observer-basis replay accepted as a diagnostic, allows",
                "centered sky-z only as a predeclared secondary/control route, and keeps",
                "full metric/lensing path weighting blocked until a source-aligned numeric",
                "product is available.",
                "",
                "Summary:",
                "",
                f"- current family: `{summary['current_observer_family']}`",
                f"- current delta chi2 versus best control: `{summary['current_delta_chi2_candidate_minus_best_control']}`",
                f"- required non-lensing lift to zero: `{summary['required_non_lensing_lift_to_zero']}`",
                f"- sky-z source rows: `{summary['sky_z_source_rows']}`",
                f"- metric path source-aligned numeric count: `{summary['metric_path_source_aligned_numeric_count']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "This is a route-selection and data-acquisition gate, not a new score.",
                "",
            ]
        )
    )
    print(
        "OBSERVER_PATH_STRENGTHENING_GATE_V1_BUILT "
        f"metric_path_source_aligned_numeric_count={source_aligned_metric_count} "
        f"verdict={verdict}"
    )


if __name__ == "__main__":
    main()
