#!/usr/bin/env python3
from __future__ import annotations

import csv
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_preflight_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_numeric_penalty_preflight_v1.md"
BLOCKER_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_blocker_status_v1_summary.csv"
CLAIM_BOUNDARY = "joint_row_level_numeric_penalty_preflight_not_scoring_not_validation"


CHECKS = [
    ("symbolic_formula", ["python", "scripts/validate_joint_symbolic_row_level_penalty_formula_shell_v1.py"]),
    ("protocol_v4", ["python", "scripts/validate_joint_row_level_penalty_protocol_shell_v4.py"]),
    ("authorization_package", ["python", "scripts/validate_joint_row_level_numeric_penalty_authorization_review_package_v1.py"]),
    ("blocker_status", ["python", "scripts/validate_joint_row_level_numeric_penalty_blocker_status_v1.py"]),
]


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_check(name: str, cmd: list[str]) -> tuple[bool, str]:
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    output = (result.stdout or result.stderr or "").strip().replace("\n", " | ")
    return result.returncode == 0, output


def main() -> None:
    rows: list[dict[str, str]] = []
    all_passed = True
    for name, cmd in CHECKS:
        passed, output = run_check(name, cmd)
        all_passed = all_passed and passed
        rows.append(
            {
                "preflight_id": "JOINT_ROW_LEVEL_NUMERIC_PENALTY_PREFLIGHT_V1",
                "check_id": name,
                "status": "PASS" if passed else "FAIL",
                "command": " ".join(cmd),
                "output": output,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    guard = subprocess.run(
        ["python", "scripts/run_joint_row_level_numeric_penalty_values_guarded_v1.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    guard_output = (guard.stdout or guard.stderr or "").strip().replace("\n", " | ")
    blocker = read_one(BLOCKER_SUMMARY)
    expected_blocked = blocker["numeric_penalty_computation_allowed"] == "false"
    guard_status = "PASS_EXPECTED_BLOCKED" if expected_blocked and guard.returncode != 0 else "FAIL"
    all_passed = all_passed and guard_status == "PASS_EXPECTED_BLOCKED"
    rows.append(
        {
            "preflight_id": "JOINT_ROW_LEVEL_NUMERIC_PENALTY_PREFLIGHT_V1",
            "check_id": "guarded_runner_expected_block",
            "status": guard_status,
            "command": "python scripts/run_joint_row_level_numeric_penalty_values_guarded_v1.py",
            "output": guard_output,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )

    verdict = (
        "PREFLIGHT_PASS_NUMERIC_PENALTY_CORRECTLY_BLOCKED"
        if all_passed and expected_blocked
        else "PREFLIGHT_FAIL_REVIEW_REQUIRED_BEFORE_NUMERIC_VALUES"
    )
    summary = {
        "preflight_id": "JOINT_ROW_LEVEL_NUMERIC_PENALTY_PREFLIGHT_V1",
        "checks_total": str(len(rows)),
        "checks_passed": str(sum(row["status"].startswith("PASS") for row in rows)),
        "review_response_imported": blocker["review_response_imported"],
        "numeric_penalty_computation_allowed": blocker["numeric_penalty_computation_allowed"],
        "lambda_row_numeric_value_allowed": blocker["lambda_row_numeric_value_allowed"],
        "t_joint_rescoring_allowed": blocker["t_joint_rescoring_allowed"],
        "endpoint_validation_claimed": blocker["endpoint_validation_claimed"],
        "penalty_values_computed": "false",
        "verdict": verdict,
        "next_required_action": blocker["next_required_action"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(ROOT / "data/derived/joint_row_level_numeric_penalty_preflight_v1.csv", rows)
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level numeric penalty preflight v1",
                "",
                "**Doc class:** preflight guard report.",
                "**Status:** not scoring; not endpoint validation; not cosmological validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This preflight checks the symbolic formula, v4 protocol shell,",
                "authorization package, blocker status, and guarded runner. In the",
                "current repository state the correct outcome is that the guarded",
                "runner blocks numeric penalty-value computation.",
                "",
                f"- checks passed: `{summary['checks_passed']}/{summary['checks_total']}`",
                f"- review response imported: `{summary['review_response_imported']}`",
                f"- numeric penalty computation allowed: `{summary['numeric_penalty_computation_allowed']}`",
                f"- verdict: `{summary['verdict']}`",
                f"- next action: `{summary['next_required_action']}`",
                "",
            ]
        )
    )
    print(f"JOINT_ROW_LEVEL_NUMERIC_PENALTY_PREFLIGHT_V1 {verdict}")


if __name__ == "__main__":
    main()
