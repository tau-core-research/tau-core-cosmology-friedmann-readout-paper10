#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_numeric_zi_distribution_ledger_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv"
AUTH = ROOT / "data/derived/joint_numeric_zi_distribution_build_authorization_response_v1_summary.csv"
CLAIM_BOUNDARY = "joint_numeric_zi_distribution_ledger_not_tjoint_not_scoring_not_validation"


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


def as_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def as_float(value: str) -> float:
    return float(value)


def main() -> None:
    auth = read_one(AUTH)
    if auth["numeric_zi_build_allowed"] != "true":
        raise SystemExit("numeric z_i build not authorized")
    if auth["numeric_t_joint_allowed"] != "false":
        raise SystemExit("unexpected T_joint authorization")

    rows = read_rows(OUT)
    summary = read_rows(SUMMARY)
    channel_rows = [row for row in summary if row["channel_id"] != "all_channels"]
    aggregate = [row for row in summary if row["channel_id"] == "all_channels"]
    if len(channel_rows) != 3 or len(aggregate) != 1:
        raise SystemExit("summary must contain three channel rows and one aggregate row")
    if not rows:
        raise SystemExit("ledger rows missing")

    for row in rows + summary:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit("claim boundary mismatch")
        for field in [
            "computes_t_joint_now",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
        ]:
            if row[field] != "false":
                raise SystemExit(f"unsafe field {field}")

    for row in channel_rows:
        if row["scale_status"] != "ok":
            raise SystemExit(f"{row['channel_id']}: scale blocked")
        if not as_bool(row["numeric_z_i_defined"]):
            raise SystemExit(f"{row['channel_id']}: z_i not defined")
        if as_float(row["scale_i_mad1p4826"]) <= 0:
            raise SystemExit(f"{row['channel_id']}: non-positive scale")
        z_value = as_float(row["candidate_z_i"])
        if not math.isfinite(z_value):
            raise SystemExit(f"{row['channel_id']}: non-finite candidate z_i")

    if aggregate[0]["numeric_z_i_defined"] != "true":
        raise SystemExit("aggregate summary must mark numeric z_i defined")
    print("JOINT_NUMERIC_ZI_DISTRIBUTION_LEDGER_V1_VALIDATED channels=3 computes_t_joint_now=false")


if __name__ == "__main__":
    main()
