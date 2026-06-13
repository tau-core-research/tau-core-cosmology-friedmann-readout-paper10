#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "source_manifest" / "act_dr6_lensing_path_weight_replay_run_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_replay_run_template_v1_summary.csv"
DOC = ROOT / "docs" / "act_dr6_lensing_path_weight_replay_run_template_v1.md"
CLAIM_BOUNDARY = "act_dr6_lensing_path_weight_replay_run_template_not_validation"
REQUIRED_FORBIDDEN = {
    "distance_residual_driven_activation",
    "lensing_residual_driven_activation",
    "posthoc_path_weight_tuning",
    "posthoc_row_selection",
    "posthoc_amplitude_tuning",
    "endpoint_score_claims",
    "physical_lensing_path_weight_claims",
    "physical_validation_claims",
}
REQUIRED_CONTROLS = {
    "off",
    "wrong_sign",
    "curl_null",
    "diff_f150_f090_null",
    "deterministic_shuffle",
    "rank_reverse",
}


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {path.relative_to(ROOT)}")
    return rows[0]


def main() -> None:
    row = read_one(OUT)
    summary = read_one(SUMMARY)
    if row["claim_boundary"] != CLAIM_BOUNDARY or summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("claim boundary mismatch")
    if row["status"] != "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_PREPARED_AUTH_REQUIRED_NOT_VALIDATION":
        raise SystemExit("bad run-template status")
    for key in (
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
        "physical_lensing_path_weight_claimed",
        "physical_validation_claimed",
    ):
        if row[key] != "false" or summary[key] != "false":
            raise SystemExit(f"{key} must remain false")
    if not (ROOT / row["candidate_basis_path"]).exists():
        raise SystemExit("candidate basis path is missing")
    controls = set(row["control_branches"].split(";"))
    if not REQUIRED_CONTROLS.issubset(controls):
        raise SystemExit("missing mandatory null/control branches")
    forbidden = set(row["forbidden_inputs"].split(";"))
    if not REQUIRED_FORBIDDEN.issubset(forbidden):
        raise SystemExit("missing required forbidden input markers")
    text = DOC.read_text()
    for marker in ["not a replay execution", "mandatory null-control branches", CLAIM_BOUNDARY]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    if summary["verdict"] != "act_dr6_lensing_path_weight_replay_template_ready_auth_required_not_validation":
        raise SystemExit("unexpected summary verdict")
    print("ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_RUN_TEMPLATE_V1_VALIDATED endpoint=false")


if __name__ == "__main__":
    main()
