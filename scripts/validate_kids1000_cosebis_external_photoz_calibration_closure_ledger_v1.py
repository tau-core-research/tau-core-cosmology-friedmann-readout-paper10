#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_external_photoz_calibration_closure_ledger_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_closure_ledger_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_closure_ledger_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    row = read_one(OUT)
    summary = read_one(SUMMARY)
    if policy["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_CLOSURE_LEDGER_POLICY_FROZEN":
        raise SystemExit("unexpected closure ledger policy status")
    if summary["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_CLOSURE_LEDGER_BUILT_SOURCE_SIDE_ONLY":
        raise SystemExit("unexpected closure ledger summary status")
    if summary["closure_count"] != "1":
        raise SystemExit("closure ledger must contain exactly one closure row")
    for key in ["r4_leakage_review_complete", "h1_independent_evidence_complete"]:
        if row[key] != "true" or summary[key] != "true":
            raise SystemExit(f"closure ledger must set {key}=true")
    for key in ["computes_new_scores", "contains_endpoint_data", "endpoint_replay_allowed", "endpoint_validation_claimed"]:
        if row[key] != "false" or summary[key] != "false":
            raise SystemExit(f"closure ledger must keep {key}=false")
    if summary["verdict"] != "external_photoz_calibration_source_side_closed_endpoint_replay_still_forbidden":
        raise SystemExit("unexpected closure ledger verdict")
    if row["claim_boundary"] != policy["claim_boundary"] or summary["claim_boundary"] != policy["claim_boundary"]:
        raise SystemExit("claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_EXTERNAL_PHOTOZ_CALIBRATION_CLOSURE_LEDGER_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
