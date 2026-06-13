#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESPONSE = ROOT / "data/derived/observer_path_metric_product_requirements_review_response_v1.csv"
SUMMARY = ROOT / "data/derived/observer_path_metric_product_requirements_review_completed_summary_v1.csv"
NOTES = ROOT / "docs/observer_path_metric_product_requirements_review_notes_v1.md"
LOG = ROOT / "data/derived/observer_path_metric_product_requirements_review_validation_log_v1.txt"
CLAIM_BOUNDARY = "observer_path_metric_product_requirements_not_endpoint_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def is_false(value: str) -> bool:
    return value.strip().lower() == "false"


def is_true(value: str) -> bool:
    return value.strip().lower() == "true"


def main() -> None:
    rows = read_rows(RESPONSE)
    if len(rows) != 4:
        raise SystemExit("response must contain four rows")
    if {row["reviewer_response"] for row in rows} != {"ACCEPT_REQUIREMENTS_ONLY"}:
        raise SystemExit("review response must accept requirements only")
    for row in rows:
        if not is_true(row["review_completed"]):
            raise SystemExit(f"{row['question_id']} not completed")
        for field in [
            "forbidden_inputs_used",
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "physical_lensing_path_weight_claimed",
        ]:
            if not is_false(row[field]):
                raise SystemExit(f"{row['question_id']} unsafe field {field}")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{row['question_id']} claim boundary mismatch")

    summary = read_one(SUMMARY)
    checks = {
        "decision": "ACCEPT_REQUIREMENTS_ONLY",
        "review_rows": "4",
        "accepted_requirements_only_rows": "4",
        "request_detail_rows": "0",
        "rejected_leakage_risk_rows": "0",
        "active_observer_path_scope_rows": "12",
        "low_z_route_audit_rows": "424",
        "source_aligned_metric_product_count": "0",
        "metric_path_branch_status": "BLOCKED_FOR_ENDPOINT_UNTIL_SOURCE_ALIGNED_NUMERIC_PRODUCT",
        "claim_boundary": CLAIM_BOUNDARY,
        "completion_check": "pass",
    }
    for key, expected in checks.items():
        if summary[key] != expected:
            raise SystemExit(f"summary {key} mismatch: {summary[key]} != {expected}")
    for field in [
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
        "physical_lensing_path_weight_claimed",
    ]:
        if not is_false(summary[field]):
            raise SystemExit(f"summary unsafe field {field}")

    notes = NOTES.read_text()
    for marker in [
        "ACCEPT_REQUIREMENTS_ONLY",
        "does not authorize endpoint replay",
        "does not provide the product",
    ]:
        if marker not in notes:
            raise SystemExit(f"notes missing marker: {marker}")
    log = LOG.read_text()
    for marker in [
        "all_accepted_requirements_only: True",
        "endpoint_replay_allowed_all_false: True",
        "completion_check: pass",
    ]:
        if marker not in log:
            raise SystemExit(f"log missing marker: {marker}")

    print(
        "OBSERVER_PATH_METRIC_PRODUCT_REQUIREMENTS_REVIEW_RESPONSE_VALIDATED "
        "decision=ACCEPT_REQUIREMENTS_ONLY product_count=0"
    )


if __name__ == "__main__":
    main()
