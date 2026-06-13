#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "data/source_manifest/joint_best_justified_qi_review_requirements_v1.csv"
DEFAULT_RESPONSE = ROOT / "data/derived/joint_best_justified_qi_review_response_v1.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/joint_best_justified_qi_review_response_v1_summary.csv"
DOC = ROOT / "docs/joint_best_justified_qi_review_response_gate_v1.md"

CLAIM_BOUNDARY = "qi_review_response_source_side_only_not_scoring"
ALLOWED_COMPLETED_RESPONSES = {
    "accept_source_side",
    "accept_with_caveats_source_side",
    "reject",
    "needs_more_context",
}
FORBIDDEN_INPUTS = {
    "endpoint_residuals",
    "fit_improvements",
    "posterior_chains",
    "post_score_control_ranks",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a joint best-justified Q_i source-side review response."
    )
    parser.add_argument("response", nargs="?", default=str(DEFAULT_RESPONSE))
    parser.add_argument("--summary-out", default=str(DEFAULT_SUMMARY))
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    return path


def rel_or_abs(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {rel_or_abs(path)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_one(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(value: str) -> str:
    return value.strip().lower()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def is_false(value: str) -> bool:
    return norm(value) == "false"


def main() -> None:
    args = parse_args()
    response_path = resolve(args.response)
    summary_out = resolve(args.summary_out)

    req_rows = read_rows(REQUIREMENTS)
    response_rows = read_rows(response_path)
    requirement_ids = [row["requirement_id"] for row in req_rows]
    requirement_set = set(requirement_ids)

    require(len(requirement_ids) == 7, "Q_i response gate expects seven requirements")
    require(len(response_rows) == len(requirement_ids), "response row count mismatch")
    require(DOC.exists(), f"missing {DOC.relative_to(ROOT)}")

    req_by_id = {row["requirement_id"]: row for row in req_rows}
    response_by_id = {row["requirement_id"]: row for row in response_rows}
    require(set(response_by_id) == requirement_set, "response requirement ids mismatch")

    for row in req_rows:
        forbidden = set(row["forbidden_inputs"].split(";"))
        require(forbidden == FORBIDDEN_INPUTS, f"{row['requirement_id']}: bad forbidden inputs")
        require(row["endpoint_scoring_allowed"] == "false", f"{row['requirement_id']}: scoring allowed")
        require(row["endpoint_validation_claimed"] == "false", f"{row['requirement_id']}: endpoint validation claimed")
        require(row["cosmological_validation_claimed"] == "false", f"{row['requirement_id']}: cosmological validation claimed")

    completed_flags: list[bool] = []
    response_values: list[str] = []
    notes_missing = 0
    for requirement_id in requirement_ids:
        row = response_by_id[requirement_id]
        require(row["review_id"].startswith("QI_REVIEW_RESPONSE_"), f"{requirement_id}: bad review id")
        require(is_false(row["forbidden_inputs_used"]), f"{requirement_id}: forbidden inputs used")
        require(is_false(row["endpoint_scores_allowed"]), f"{requirement_id}: endpoint scores allowed")
        require(is_false(row["endpoint_validation_claimed"]), f"{requirement_id}: endpoint validation claimed")
        require(is_false(row["cosmological_validation_claimed"]), f"{requirement_id}: cosmological validation claimed")

        value = norm(row["response"])
        response_values.append(value)
        if value:
            require(value in ALLOWED_COMPLETED_RESPONSES, f"{requirement_id}: unsupported response {value}")
            if not row["reviewer_notes"].strip():
                notes_missing += 1
            completed_flags.append(True)
        else:
            completed_flags.append(False)

    completed_count = sum(completed_flags)
    require(completed_count in {0, len(requirement_ids)}, "response must be either blank template or fully completed")
    if completed_count == len(requirement_ids):
        require(notes_missing == 0, "completed response rows require reviewer_notes")

    accept_count = sum(value == "accept_source_side" for value in response_values)
    caveated_count = sum(value == "accept_with_caveats_source_side" for value in response_values)
    reject_count = sum(value == "reject" for value in response_values)
    needs_context_count = sum(value == "needs_more_context" for value in response_values)

    if completed_count == 0:
        decision = "QI_REVIEW_RESPONSE_TEMPLATE_READY_NOT_COMPLETED"
        qi_source_side_review_status = "not_completed"
        future_gate_preparation_allowed = "false"
    elif reject_count:
        decision = "QI_REVIEW_REJECTED_SOURCE_SIDE_NOT_SCORING"
        qi_source_side_review_status = "rejected"
        future_gate_preparation_allowed = "false"
    elif needs_context_count:
        decision = "QI_REVIEW_NEEDS_MORE_CONTEXT_SOURCE_SIDE_NOT_SCORING"
        qi_source_side_review_status = "needs_more_context"
        future_gate_preparation_allowed = "false"
    else:
        decision = "QI_REVIEW_ACCEPTED_OR_CAVEATED_SOURCE_SIDE_NOT_VALIDATION"
        qi_source_side_review_status = "accepted_or_caveated"
        future_gate_preparation_allowed = "true"

    doc_text = DOC.read_text()
    for marker in [
        "SOURCE_SIDE_RESPONSE_GATE_NOT_SCORING",
        "does not compute",
        "joint endpoint",
    ]:
        require(marker in doc_text, f"response gate doc missing marker: {marker}")

    summary = {
        "run_id": "JOINT_BEST_JUSTIFIED_QI_REVIEW_RESPONSE_V1",
        "response_path": rel_or_abs(response_path),
        "response_sha256": sha256(response_path),
        "requirement_count": str(len(requirement_ids)),
        "completed_response_rows": str(completed_count),
        "accept_source_side_count": str(accept_count),
        "accept_with_caveats_source_side_count": str(caveated_count),
        "reject_count": str(reject_count),
        "needs_more_context_count": str(needs_context_count),
        "forbidden_inputs_used": "false",
        "endpoint_scores_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "future_gate_preparation_allowed": future_gate_preparation_allowed,
        "qi_source_side_review_status": qi_source_side_review_status,
        "decision": decision,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_one(summary_out, summary)
    print(
        "JOINT_BEST_JUSTIFIED_QI_REVIEW_RESPONSE_V1_VALIDATED "
        f"decision={decision}"
    )


if __name__ == "__main__":
    main()
