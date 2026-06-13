#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
W_TIME_SUMMARY = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_candidate_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1_summary.csv"
RESPONSE_SUMMARY = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_v1_summary.csv"
RUN_TEMPLATE = ROOT / "data/source_manifest/low_z_pantheon_w_time_uncertainty_basis_replay_run_template_v1.csv"
OUT = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1_summary.csv"
CLAIM_BOUNDARY = "w_time_uncertainty_basis_gate_status_ledger_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def gate_row(
    gate_id: str,
    status: str,
    artifact: str,
    endpoint_replay_allowed: str,
    endpoint_validation_claimed: str,
    blocker: str,
    next_action: str,
) -> dict[str, str]:
    return {
        "ledger_id": "LOW_Z_PANTHEON_W_TIME_UNCERTAINTY_BASIS_GATE_STATUS_LEDGER_V1",
        "gate_id": gate_id,
        "status": status,
        "artifact": artifact,
        "endpoint_replay_allowed": endpoint_replay_allowed,
        "endpoint_validation_claimed": endpoint_validation_claimed,
        "physical_validation_claimed": "false",
        "blocker": blocker,
        "next_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    w_time = read_one(W_TIME_SUMMARY)
    package = read_one(PACKAGE_SUMMARY)
    run_template = read_one(RUN_TEMPLATE)
    response_exists = RESPONSE_SUMMARY.exists()
    response = read_one(RESPONSE_SUMMARY) if response_exists else None

    rows = [
        gate_row(
            "G1_SOURCE_SIDE_W_TIME_BASIS",
            "PASS_SOURCE_SIDE_CANDIDATE_FROZEN",
            str(W_TIME_SUMMARY.relative_to(ROOT)),
            w_time["endpoint_replay_allowed"],
            w_time["endpoint_validation_claimed"],
            "none_at_source_side_basis_level",
            "retain_candidate_as_frozen_input_to_authorization_review",
        ),
        gate_row(
            "G2_REVIEW_PACKAGE",
            "PASS_PACKAGE_READY_NOT_COMPLETED",
            str(PACKAGE_SUMMARY.relative_to(ROOT)),
            package["endpoint_replay_allowed"],
            package["endpoint_validation_claimed"],
            "completed_external_review_response_missing",
            "send_package_to_reviewer_or_import_completed_response",
        ),
        gate_row(
            "G3_COMPLETED_REVIEW_RESPONSE",
            "PASS_COMPLETED_GO_RESPONSE"
            if response and response.get("endpoint_replay_allowed") == "true"
            else "BLOCKED_RESPONSE_MISSING_OR_NOT_GO",
            str(RESPONSE_SUMMARY.relative_to(ROOT)),
            response["endpoint_replay_allowed"] if response else "false",
            response["endpoint_validation_claimed"] if response else "false",
            "none" if response and response.get("endpoint_replay_allowed") == "true" else "completed_GO_response_missing",
            "run_authorized_replay"
            if response and response.get("endpoint_replay_allowed") == "true"
            else "validate_and_import_completed_reviewer_csv",
        ),
        gate_row(
            "G4_REPLAY_RUN_TEMPLATE",
            "PASS_READY_FOR_PERMISSION_REPLAY"
            if response and response.get("endpoint_replay_allowed") == "true"
            else "READY_BUT_LOCKED_BY_G3",
            str(RUN_TEMPLATE.relative_to(ROOT)),
            "true" if response and response.get("endpoint_replay_allowed") == "true" else run_template["endpoint_replay_allowed"],
            run_template["endpoint_validation_claimed"],
            "none" if response and response.get("endpoint_replay_allowed") == "true" else "G3_completed_GO_response_required",
            "run_authorized_replay"
            if response and response.get("endpoint_replay_allowed") == "true"
            else "do_not_run_until_G3_passes",
        ),
    ]
    write_csv(OUT, rows)
    scoring_ready = all(
        row["gate_id"] != "G3_COMPLETED_REVIEW_RESPONSE" or row["status"] == "PASS_COMPLETED_GO_RESPONSE"
        for row in rows
    )
    summary = [
        {
            "ledger_id": "LOW_Z_PANTHEON_W_TIME_UNCERTAINTY_BASIS_GATE_STATUS_LEDGER_V1",
            "status": "SCORING_READY_PERMISSION_ONLY" if scoring_ready else "SCORING_BLOCKED_AWAITING_REVIEW_RESPONSE",
            "gate_count": str(len(rows)),
            "passed_gate_count": str(sum("PASS" in row["status"] for row in rows)),
            "blocked_gate_count": str(sum("BLOCKED" in row["status"] or "LOCKED" in row["status"] for row in rows)),
            "completed_review_response_exists": str(response_exists).lower(),
            "endpoint_replay_allowed": "true" if scoring_ready else "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "recommended_next_action": "run_authorized_replay" if scoring_ready else "obtain_completed_reviewer_response",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_W_TIME_GATE_STATUS_LEDGER_BUILT "
        f"status={summary[0]['status']} "
        f"completed_review_response_exists={summary[0]['completed_review_response_exists']}"
    )


if __name__ == "__main__":
    main()
