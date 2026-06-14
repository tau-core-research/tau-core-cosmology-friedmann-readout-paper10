#!/usr/bin/env python3
from __future__ import annotations

import csv
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_response_template_v1.csv"
VALIDATOR = ROOT / "scripts/validate_joint_numeric_t_joint_control_suite_review_response_v1.py"

ACCEPTED = {
    "CSR_Q1_SCOPE": "ACCEPT_CONTROL_SUITE_REVIEW_SCOPE_NOT_ENDPOINT_SCORING",
    "CSR_Q2_SAME_STATISTIC_CONTROLS": "ACCEPT_SAME_STATISTIC_CONTROLS_NO_RETUNING",
    "CSR_Q3_CONTROL_RESULT": "ACCEPT_PREPARE_SEPARATE_ENDPOINT_AUTHORIZATION_PACKAGE",
    "CSR_Q4_CAVEATS": "ACCEPT_CAVEAT_PRESERVATION",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_validator(response: Path, summary: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python", str(VALIDATOR.relative_to(ROOT)), str(response), "--summary-out", str(summary)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="control_suite_review_gate_smoke_") as tmp_text:
        tmp = Path(tmp_text)

        blank = run_validator(TEMPLATE, tmp / "blank_summary.csv")
        if blank.returncode == 0:
            raise SystemExit("blank response template unexpectedly validated")
        if "review must be completed" not in (blank.stderr + blank.stdout):
            raise SystemExit("blank response failed for an unexpected reason")

        rows = read_rows(TEMPLATE)
        for row in rows:
            qid = row["question_id"]
            row["review_completed"] = "true"
            row["reviewer_id_or_role"] = "smoke_test_reviewer"
            row["reviewer_response"] = ACCEPTED[qid]
            row["reviewer_rationale"] = "Smoke test only: verifies accepted tokens and claim-boundary fields."
            row["forbidden_inputs_used"] = "false"
            row["endpoint_scoring_authorization_package_preparation_allowed"] = "true"
            row["endpoint_scoring_allowed"] = "false"
            row["endpoint_validation_claimed"] = "false"
            row["cosmological_validation_claimed"] = "false"
            row["physical_validation_claimed"] = "false"

        accepted_response = tmp / "accepted_response.csv"
        accepted_summary = tmp / "accepted_summary.csv"
        write_rows(accepted_response, rows)
        accepted = run_validator(accepted_response, accepted_summary)
        if accepted.returncode != 0:
            raise SystemExit((accepted.stderr or accepted.stdout).strip())
        summary = read_rows(accepted_summary)[0]
        expected_decision = "AUTHORIZE_PREPARE_ENDPOINT_SCORING_AUTHORIZATION_PACKAGE_NOT_SCORING"
        if summary["decision"] != expected_decision:
            raise SystemExit(f"unexpected accepted decision: {summary['decision']}")
        if summary["endpoint_scoring_allowed"] != "false" or summary["endpoint_validation_claimed"] != "false":
            raise SystemExit("accepted smoke response leaked scoring or validation permission")

    print("JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_REVIEW_RESPONSE_GATE_SMOKE_PASS")


if __name__ == "__main__":
    main()
