#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_policy_v1.csv"
PREFLIGHT = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1_summary.csv"
SOURCE_MANIFEST = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_source_manifest_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1_summary.csv"


QUESTIONS = [
    {
        "question_id": "Q1_source_identity",
        "question_text": "Do the attached cached source artifacts match the stated public KiDS-1000 photo-z/SOM-gold/tomographic calibration sources?",
        "required_response": "yes_or_no",
        "acceptance_condition": "yes_with_source_side_rationale",
    },
    {
        "question_id": "Q2_no_endpoint_fields",
        "question_text": "Did the review avoid observed COSEBIs values, endpoint residuals, endpoint scores, ranks, fit statistics, and post-score residual shapes?",
        "required_response": "yes_or_no",
        "acceptance_condition": "yes",
    },
    {
        "question_id": "Q3_route_coverage",
        "question_text": "Do the attached sources support R1 photo-z calibration, R2 SOM-gold/n(z), and R3 tomographic-bin quality context before any endpoint replay?",
        "required_response": "yes_or_no",
        "acceptance_condition": "yes_or_caveated_yes_with_missing_route_named",
    },
    {
        "question_id": "Q4_r4_decision",
        "question_text": "Can the R4 leakage review be accepted for source-side purposes without authorizing endpoint replay or validation?",
        "required_response": "ACCEPT_AS_CAVEATED_SOURCE_SIDE_REVIEW or REJECT or NEEDS_MORE_SOURCE_EVIDENCE",
        "acceptance_condition": "ACCEPT_AS_CAVEATED_SOURCE_SIDE_REVIEW",
    },
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = read_one(POLICY)
    preflight = read_one(PREFLIGHT)
    sources = read_rows(SOURCE_MANIFEST)
    if policy["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_ATTESTATION_TEMPLATE_POLICY_FROZEN":
        raise SystemExit("unexpected reviewer-attestation template policy status")
    if preflight["verdict"] != "automated_leakage_preflight_passed_independent_reviewer_still_open":
        raise SystemExit("reviewer template requires automated leakage preflight first")
    if preflight["independent_reviewer_attestation_complete"] != "false":
        raise SystemExit("template must only be built before independent attestation")
    if len(sources) != 3:
        raise SystemExit("expected three attached source artifacts")

    rows = []
    source_ids = ";".join(row["source_id"] for row in sources)
    for item in QUESTIONS:
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "question_id": item["question_id"],
                "question_text": item["question_text"],
                "review_context_artifacts": "data/derived/kids1000_cosebis_external_photoz_calibration_source_manifest_v1.csv;data/derived/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.csv",
                "attached_source_ids": source_ids,
                "required_response": item["required_response"],
                "acceptance_condition": item["acceptance_condition"],
                "reviewer_response": "",
                "reviewer_rationale": "",
                "reviewer_id_or_role": "",
                "review_completed": "false",
                "forbidden_inputs_used": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_ATTESTATION_TEMPLATE_BUILT_NOT_COMPLETED",
            "question_count": str(len(rows)),
            "review_completed": "false",
            "independent_reviewer_attestation_complete": "false",
            "r4_leakage_review_complete": "false",
            "h1_independent_evidence_complete": "false",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values_for_scoring": "false",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "uses_residuals": "false",
            "uses_fit_statistics": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "reviewer_attestation_template_ready_not_completed",
            "recommended_next_action": "send_template_to_independent_reviewer_then_validate_completed_response",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_ATTESTATION_TEMPLATE_V1_BUILT "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
