#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
SUMMARY = DERIVED / "joint_row_level_penalized_t_joint_endpoint_scoring_v1_summary.csv"
ROWS = DERIVED / "joint_row_level_penalized_t_joint_endpoint_scoring_v1.csv"
AUTH = DERIVED / "joint_row_level_penalized_t_joint_endpoint_authorization_review_completed_summary_v1.csv"
LOG = DERIVED / "joint_row_level_penalized_t_joint_endpoint_scoring_v1_validation_log.txt"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> None:
    errors: list[str] = []
    auth = read_one(AUTH)
    summary = read_one(SUMMARY)
    rows = read_rows(ROWS)

    if auth.get("guarded_endpoint_scoring_replay_authorized") != "true":
        fail(errors, "completed authorization does not authorize guarded endpoint replay")
    if auth.get("endpoint_scoring_run_by_this_review") != "false":
        fail(errors, "authorization review must not run scoring")
    if summary.get("status") != "GUARDED_ENDPOINT_SCORING_COMPLETE_NOT_VALIDATION":
        fail(errors, "unexpected scoring status")
    if summary.get("aligned_control_count") != "6":
        fail(errors, "aligned control count must be 6")
    if summary.get("controls_beating_or_equal_candidate") != "0":
        fail(errors, "candidate is not above all aligned controls")
    if summary.get("control_scope") != "six_deterministically_aligned_row_level_controls_only":
        fail(errors, "control scope is not the frozen aligned row-level scope")
    if summary.get("endpoint_scoring_allowed_by_completed_review") != "true":
        fail(errors, "summary does not record completed-review scoring authorization")
    for field in ["endpoint_validation_claimed", "cosmological_validation_claimed", "physical_validation_claimed"]:
        if summary.get(field) != "false":
            fail(errors, f"unsafe summary field {field}")

    if len(rows) != 6:
        fail(errors, f"expected six scoring rows, got {len(rows)}")
    for idx, row in enumerate(rows, start=1):
        for field in ["same_penalty_formula", "same_lambda_row", "same_alignment_rule"]:
            if row.get(field) != "true":
                fail(errors, f"row {idx}: {field} must be true")
        for field in ["endpoint_validation_claimed", "cosmological_validation_claimed", "physical_validation_claimed"]:
            if row.get(field) != "false":
                fail(errors, f"row {idx}: unsafe field {field}")
        if row.get("control_beats_or_equals_candidate") != "false":
            fail(errors, f"row {idx}: control beats/equal candidate")

    if errors:
        LOG.write_text("FAILED\n" + "\n".join(errors) + "\n", encoding="utf-8")
        raise SystemExit("\n".join(errors))
    LOG.write_text(
        "PASSED\n"
        "Penalized endpoint scoring is complete under completed authorization; not validation.\n",
        encoding="utf-8",
    )
    print("PASSED")


if __name__ == "__main__":
    main()
