#!/usr/bin/env python3
"""Validate the completed ACT caveated K_path source-design review response."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
RESPONSE = DERIVED / "act_dr6_lensing_caveated_kpath_source_design_review_response_v1.csv"
SUMMARY = DERIVED / "act_dr6_lensing_caveated_kpath_source_design_review_completed_summary_v1.csv"
NOTES = DERIVED / "act_dr6_lensing_caveated_kpath_source_design_review_notes_v1.md"
LOG = DERIVED / "act_dr6_lensing_caveated_kpath_source_design_review_validation_log_v1.txt"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    for path in (RESPONSE, SUMMARY, NOTES, LOG):
        if not path.exists():
            raise SystemExit(f"missing imported review response file: {path.relative_to(ROOT)}")

    response_rows = read_rows(RESPONSE)
    summary_rows = read_rows(SUMMARY)
    if len(response_rows) != 5:
        raise SystemExit(f"expected five response rows, found {len(response_rows)}")
    if len(summary_rows) != 1:
        raise SystemExit("completed summary must have one row")

    responses = {row["review_item"]: row["response"] for row in response_rows}
    expected_responses = {
        "source_product_status": "yes_caveated_source_proxy_only",
        "proxy_mapping_status": "yes_dimensionless_shape_proxy_only",
        "null_control_status": "yes_null_controls_must_remain",
        "leakage_status": "no_forbidden_endpoint_inputs_used",
        "overall_verdict": "ACCEPT_CAVEATED_KPATH_SOURCE_DESIGN_FOR_REVIEW_ONLY",
    }
    if responses != expected_responses:
        raise SystemExit(f"unexpected response ledger: {responses}")

    summary = summary_rows[0]
    expected_summary = {
        "artifact_id": "ACT_DR6_LENSING_CAVEATED_KPATH_SOURCE_DESIGN_REVIEW_RESPONSE_V1",
        "decision": "ACCEPT_CAVEATED_KPATH_SOURCE_DESIGN_FOR_REVIEW_ONLY",
        "review_completed": "true",
        "review_rows": "5",
        "source_rows": "424",
        "mask_positive_rows": "168",
        "source_product_status": "caveated_dimensionless_proxy_only",
        "proxy_mapping_status": "median_MAD_shape_proxy_only_not_physical_amplitude",
        "null_controls_retained": "curl_null;diff_f150_f090_null",
        "forbidden_inputs_used": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "future_permission_only_replay_review_preparation_allowed": "true",
        "current_replay_authorized_by_this_review": "false",
        "claim_boundary": "source_side_design_review_only_not_replay_not_validation",
        "completion_check": "pass",
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            raise SystemExit(f"{key}: expected {expected!r}, got {summary.get(key)!r}")

    notes = NOTES.read_text()
    for marker in (
        "not authorize endpoint replay",
        "Curl and `f150-f090` frequency-difference products must remain `K_null` controls",
        "forbidden_inputs_used=false",
    ):
        if marker not in notes:
            raise SystemExit(f"notes missing marker: {marker}")
    log = LOG.read_text()
    for marker in ("overall_verdict_ok=True", "completion_check=pass"):
        if marker not in log:
            raise SystemExit(f"validation log missing marker: {marker}")
    print("ACT_CAVEATED_KPATH_SOURCE_DESIGN_REVIEW_RESPONSE_VALIDATED")


if __name__ == "__main__":
    main()
