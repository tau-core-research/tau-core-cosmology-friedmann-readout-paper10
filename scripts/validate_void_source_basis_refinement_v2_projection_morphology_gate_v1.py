#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_v2_projection_morphology_policy.csv"
GATE = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_projection_morphology_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_projection_morphology_gate_v1_summary.csv"

REQUIRED_COMPONENTS = {
    "V2_VOID_MORPHOLOGY",
    "V2_WEB_MORPHOLOGY",
    "V2_OBSERVER_PATH_PROJECTION",
    "V2_TIME_READOUT_PROJECTION",
    "V2_CMB_SAFETY",
    "V2_MULTI_CHANNEL_COUPLING",
}
REQUIRED_CHANNELS = {
    "W_VOID_MATURITY",
    "W_WEB_ANISOTROPY",
    "W_PATH_PROJECTION",
    "W_TIME_READOUT",
}
REQUIRED_FORBIDDEN_MARKERS = {
    "distance_residuals",
    "fit_statistics",
    "endpoint_scores",
    "posthoc_source_basis_selection",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy_rows = read_rows(POLICY)
    gate_rows = read_rows(GATE)
    summary = read_one(SUMMARY)
    require({row["component_id"] for row in policy_rows} == REQUIRED_COMPONENTS, "policy component set mismatch")
    require({row["component_id"] for row in gate_rows} == REQUIRED_COMPONENTS, "gate component set mismatch")
    channel_blob = ";".join(row["channel_id"] for row in gate_rows)
    for channel in REQUIRED_CHANNELS:
        require(channel in channel_blob, f"missing required channel {channel}")
    for row in policy_rows:
        forbidden = set(item for item in row["forbidden_inputs"].split(";") if item)
        require(REQUIRED_FORBIDDEN_MARKERS <= forbidden, f"{row['component_id']} missing forbidden markers")
        require(row["endpoint_replay_allowed"] == "false", "policy must not allow endpoint replay")
        require(row["endpoint_validation_claimed"] == "false", "policy must not claim validation")
        require(
            row["claim_boundary"] == "void_source_basis_refinement_v2_projection_morphology_gate_not_scoring_not_validation",
            "policy claim boundary mismatch",
        )
    for row in gate_rows:
        require(row["endpoint_replay_allowed"] == "false", "gate rows must keep endpoint replay blocked")
        require(row["endpoint_validation_claimed"] == "false", "gate rows must not claim validation")
        require(row["source_available"] in {"true", "false"}, "source_available must be boolean")
        require(row["gate_status"] in {"READY", "SOURCE_PRESENT_BUT_NOT_ENDPOINT_READY", "SOURCE_MISSING_OR_PARTIAL"}, "bad gate status")
        require(row["minimum_next_artifact"].startswith("data/derived/"), "minimum next artifact must be derived path")
        require(
            row["claim_boundary"] == "void_source_basis_refinement_v2_projection_morphology_gate_not_scoring_not_validation",
            "gate claim boundary mismatch",
        )
    require(summary["status"] == "V2_PROJECTION_MORPHOLOGY_SOURCE_BASIS_DECLARED_ENDPOINT_BLOCKED", "bad summary status")
    require(summary["all_components_tracked"] == "true", "all V2 components must be tracked")
    require(summary["components_required"] == "6", "component requirement count changed")
    require(summary["components_tracked"] == "6", "tracked component count changed")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["endpoint_replay_allowed"] == "false", "V2 gate should remain blocked until all source values are frozen")
    require(int(summary["components_blocking"]) > 0, "V2 should still have blocking components")
    require(
        summary["verdict"] == "missing_projection_morphology_components_accounted_endpoint_still_blocked",
        "unexpected V2 verdict",
    )
    require(
        summary["claim_boundary"] == "void_source_basis_refinement_v2_projection_morphology_gate_not_scoring_not_validation",
        "summary claim boundary mismatch",
    )
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_V2_PROJECTION_MORPHOLOGY_GATE_V1_VALIDATED "
        f"blocking={summary['components_blocking']} endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
