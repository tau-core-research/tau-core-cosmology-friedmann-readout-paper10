#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_numeric_t_joint_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_blocker_status_not_endpoint_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    row = read_one(OUT)
    summary = read_one(SUMMARY)
    require(DOC.exists(), "missing doc")
    for item, label in [(row, "row"), (summary, "summary")]:
        require(item["claim_boundary"] == CLAIM_BOUNDARY, f"{label}: claim boundary mismatch")
        require(item["numeric_t_joint_allowed"] in {"true", "false"}, f"{label}: bad numeric_t_joint_allowed")
        for field in [
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
        ]:
            require(item[field] == "false", f"{label}: unsafe field {field}")
    require(
        row["current_blocker"]
        in {
            "numeric_t_joint_authorization_response_missing",
            "numeric_t_joint_authorized_but_not_run",
            "numeric_t_joint_authorization_rejected_or_incomplete",
            "numeric_t_joint_ledger_built_endpoint_scoring_authorization_missing",
        },
        "unexpected blocker",
    )
    text = DOC.read_text()
    require(row["current_blocker"] in text, "doc missing current blocker")
    print(f"JOINT_NUMERIC_T_JOINT_BLOCKER_STATUS_V1_VALIDATED blocker={row['current_blocker']}")


if __name__ == "__main__":
    main()
