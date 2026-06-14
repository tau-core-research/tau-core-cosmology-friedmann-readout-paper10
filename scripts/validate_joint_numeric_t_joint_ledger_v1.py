#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_numeric_t_joint_ledger_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_ledger_v1_summary.csv"
AUTH = ROOT / "data/derived/joint_numeric_t_joint_authorization_response_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_ledger_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_ledger_not_endpoint_scoring_not_validation"


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


def f(value: str) -> float:
    return float(value)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    auth = read_one(AUTH)
    require(auth["numeric_t_joint_allowed"] == "true", "numeric T_joint was not authorized")
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(len(rows) == 3, "ledger must contain three channel contributions")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["numeric_t_joint_allowed"] == "true", "summary authorization mismatch")
    for row in rows + [summary]:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "claim boundary mismatch")
        for field in [
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
        ]:
            require(row[field] == "false", f"unsafe field {field}")
    total = sum(f(row["q_i_z_i_contribution"]) for row in rows)
    reported = f(summary["numeric_t_joint"])
    require(math.isfinite(reported), "reported T_joint is not finite")
    require(abs(total - reported) < 1e-10, "T_joint sum mismatch")
    text = DOC.read_text()
    require("not an endpoint score" in text, "doc missing endpoint-score caveat")
    print(f"JOINT_NUMERIC_T_JOINT_LEDGER_V1_VALIDATED T_joint={summary['numeric_t_joint']}")


if __name__ == "__main__":
    main()
