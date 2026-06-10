#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_web_combined_multiblock_endpoint_authorization_review_policy_v1.csv"
PROTOCOL = ROOT / "data" / "source_manifest" / "void_web_combined_multiblock_endpoint_protocol_v1.csv"
READINESS = ROOT / "data" / "derived" / "void_web_endpoint_readiness_after_flrw_audit_v1_summary.csv"
TEMPLATE = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_response_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_template_v1_summary.csv"

EXPECTED_QUESTIONS = {
    "Q1_protocol_integrity",
    "Q2_readiness_caveat",
    "Q3_no_leakage",
    "Q4_authorization",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def main() -> None:
    policy_rows = read_rows(POLICY)
    protocol = read_one(PROTOCOL)
    readiness = read_one(READINESS)
    template_rows = read_rows(TEMPLATE)
    summary = read_one(SUMMARY)

    if len(policy_rows) != 4:
        raise SystemExit("authorization policy must contain four rows")
    if {row["question_id"] for row in policy_rows} != EXPECTED_QUESTIONS:
        raise SystemExit("unexpected authorization policy questions")
    if {row["question_id"] for row in template_rows} != EXPECTED_QUESTIONS:
        raise SystemExit("unexpected authorization template questions")
    if protocol["status"] != "COMBINED_MULTIBLOCK_ENDPOINT_PROTOCOL_FROZEN_NOT_RUN":
        raise SystemExit("combined protocol must be frozen before authorization review")
    if protocol["scoring_allowed"] != "false":
        raise SystemExit("combined protocol must keep scoring disabled")
    if readiness["endpoint_ready_count"] != "0":
        raise SystemExit("readiness ledger must still report endpoint_ready_count=0")
    if readiness["support_ready_count"] != "1":
        raise SystemExit("readiness ledger should still preserve one CMB-safety support pass")

    for row in policy_rows:
        for marker in [
            "distance_residuals",
            "growth_residuals",
            "endpoint_scores",
            "fit_statistics",
            "posthoc_channel_promotion",
            "posthoc_block_weights",
            "posthoc_covariance_reweighting",
        ]:
            if marker not in row["forbidden_inputs"]:
                raise SystemExit(f"{row['question_id']}: missing forbidden marker {marker}")
        if row["claim_boundary"] != "combined_multiblock_endpoint_authorization_review_not_validation":
            raise SystemExit(f"{row['question_id']}: unexpected claim boundary")

    for row in template_rows:
        if row["review_completed"] != "false":
            raise SystemExit("template must not be pre-completed")
        if row["forbidden_inputs_used"] != "false":
            raise SystemExit("template must default forbidden_inputs_used=false")
        if row["endpoint_run_allowed"] != "false":
            raise SystemExit("template must not pre-authorize endpoint run")
        if row["physical_validation_claimed"] != "false":
            raise SystemExit("template must not claim physical validation")
        if row["authorization_scope"] != "single_predeclared_combined_void_web_endpoint_run_permission_only_not_validation":
            raise SystemExit("unexpected authorization scope")

    if summary["status"] != "AUTHORIZATION_REVIEW_TEMPLATE_READY_NOT_COMPLETED":
        raise SystemExit("unexpected template summary status")
    if summary["review_completed"] != "false":
        raise SystemExit("summary must keep review_completed=false")
    if summary["endpoint_run_allowed"] != "false":
        raise SystemExit("summary must keep endpoint_run_allowed=false")
    if summary["physical_validation_claimed"] != "false":
        raise SystemExit("summary must not claim physical validation")
    print(
        "PAPER10_VOID_WEB_COMBINED_MULTIBLOCK_ENDPOINT_AUTHORIZATION_REVIEW_TEMPLATE_V1_VALIDATED "
        "review_completed=false endpoint_run_allowed=false"
    )


if __name__ == "__main__":
    main()
