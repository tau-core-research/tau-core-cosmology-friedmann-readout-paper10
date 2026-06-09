#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_scoring_protocol_v1.csv"
READINESS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_readiness_v1_summary.csv"

FORBIDDEN_SCORE_ARTIFACTS = [
    ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_results.csv",
    ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_residuals.csv",
    ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_grid.csv",
    ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_null_controls.csv",
    ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_summary.csv",
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def main() -> None:
    protocol = read_one(PROTOCOL)
    readiness = read_one(READINESS)

    if protocol["status"] != "SCORING_PROTOCOL_FROZEN_NOT_RUN":
        raise SystemExit("KiDS endpoint scoring protocol must remain frozen-not-run")
    if protocol["scoring_allowed"] != "false":
        raise SystemExit("KiDS endpoint scoring protocol must keep scoring_allowed=false")
    if protocol["parent_readiness_policy"] != readiness["policy_id"]:
        raise SystemExit("KiDS endpoint scoring protocol parent readiness policy mismatch")
    if readiness["endpoint_scoring_allowed"] != "false":
        raise SystemExit("parent readiness ledger must keep endpoint scoring disabled")
    if readiness["first_blocker"] != "D_path":
        raise SystemExit("D_path must be the first blocker after F_overlap source support")
    if readiness["blocking_component_count"] != "6":
        raise SystemExit("KiDS endpoint scoring protocol should remain blocked by six components")
    if "chi2=" not in protocol["primary_score"]:
        raise SystemExit("primary score must declare a chi-square shell")
    for marker in [
        "baseline_only",
        "web_path_candidate",
        "wrong_channel_controls",
        "shuffled_or_rotated_nulls",
        "AIC_delta",
        "control_rank",
    ]:
        if marker not in protocol["comparison_outputs"]:
            raise SystemExit(f"comparison output missing: {marker}")
    for marker in [
        "source-ready",
        "non-degenerate source-frozen mapping",
        "controls executed",
        "predeclared null controls",
        "endpoint leakage flags",
    ]:
        if marker not in protocol["pass_condition_shell"]:
            raise SystemExit(f"pass-condition shell missing: {marker}")
    for marker in [
        "kids_data_vector_values_for_source_selection",
        "posterior_chains",
        "fit_improvement_flags",
        "lensing_residuals",
        "posthoc_channel_activation",
        "posthoc_mode_cuts",
        "posthoc_tomographic_selection",
        "posthoc_sky_direction_selection",
        "posthoc_web_environment_labels",
        "posthoc_path_projection_labels",
        "posthoc_weight_selection",
    ]:
        if marker not in protocol["forbidden_inputs"]:
            raise SystemExit(f"forbidden input marker missing: {marker}")
    existing_forbidden = [str(path.relative_to(ROOT)) for path in FORBIDDEN_SCORE_ARTIFACTS if path.exists()]
    if existing_forbidden:
        raise SystemExit(
            "KiDS endpoint scoring protocol freeze cannot coexist with score artifacts: "
            + ",".join(existing_forbidden)
        )
    print("PAPER10_KIDS1000_COSEBIS_ENDPOINT_SCORING_PROTOCOL_V1_VALIDATED scoring_allowed=false")


if __name__ == "__main__":
    main()
