#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_external_photoz_calibration_closure_ledger_policy_v1.csv"
REVIEW_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_closure_ledger_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_closure_ledger_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = read_one(POLICY)
    review = read_one(REVIEW_SUMMARY)
    if policy["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_CLOSURE_LEDGER_POLICY_FROZEN":
        raise SystemExit("unexpected closure ledger policy status")
    if review["verdict"] != "completed_reviewer_response_accepted_source_side_only_endpoint_replay_still_forbidden":
        raise SystemExit("closure ledger requires accepted completed reviewer response")
    for key in ["independent_reviewer_attestation_complete", "r4_leakage_review_complete", "h1_independent_evidence_complete"]:
        if review[key] != "true":
            raise SystemExit(f"completed reviewer response must set {key}=true")
    for key in ["computes_new_scores", "contains_endpoint_data", "endpoint_replay_allowed", "endpoint_validation_claimed"]:
        if review[key] != "false":
            raise SystemExit(f"completed reviewer response must keep {key}=false")

    rows = [
        {
            "policy_id": policy["policy_id"],
            "closure_id": "R4_H1_source_side_closure",
            "parent_response_summary": str(REVIEW_SUMMARY.relative_to(ROOT)),
            "closure_status": "SOURCE_SIDE_COMPLETE",
            "independent_reviewer_attestation_complete": "true",
            "r4_leakage_review_complete": "true",
            "h1_independent_evidence_complete": "true",
            "computes_new_scores": "false",
            "contains_endpoint_data": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "next_gate": "separate_human_endpoint_replay_authorization_required",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "EXTERNAL_PHOTOZ_CALIBRATION_CLOSURE_LEDGER_BUILT_SOURCE_SIDE_ONLY",
            "closure_count": str(len(rows)),
            "r4_leakage_review_complete": "true",
            "h1_independent_evidence_complete": "true",
            "computes_new_scores": "false",
            "contains_endpoint_data": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "external_photoz_calibration_source_side_closed_endpoint_replay_still_forbidden",
            "recommended_next_action": "require_separate_human_endpoint_replay_authorization_before_any_replay",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_EXTERNAL_PHOTOZ_CALIBRATION_CLOSURE_LEDGER_V1_BUILT "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
