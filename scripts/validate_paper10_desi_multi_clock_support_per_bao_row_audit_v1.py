#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_multi_clock_support_per_bao_row_audit_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_multi_clock_support_per_bao_row_audit_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def main() -> None:
    policy = one_row(POLICY)
    rows = read_rows(OUT)
    summary = one_row(SUMMARY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY or summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad multi-clock support audit claim boundary")
    if len(rows) != 5:
        raise SystemExit("multi-clock audit must contain the five authorized DESI rows")
    expected_indices = {"0", "1", "2", "3", "4"}
    if {row["radial_index"] for row in rows} != expected_indices:
        raise SystemExit("multi-clock audit authorized radial indices changed")
    for row in rows + [policy, summary]:
        if row["endpoint_replay_allowed"] != "false":
            raise SystemExit("multi-clock support audit must not authorize replay")
        if row["endpoint_validation_claimed"] != "false" or row["physical_validation_claimed"] != "false":
            raise SystemExit("multi-clock support audit must not claim validation")
    if {row["claim_boundary"] for row in rows} != {CLAIM_BOUNDARY}:
        raise SystemExit("bad multi-clock row claim boundary")
    if summary["status"] != "DESI_MULTI_CLOCK_SUPPORT_PER_BAO_ROW_AUDIT_BUILT_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad multi-clock support audit status")
    if summary["authorized_row_count"] != "5":
        raise SystemExit("multi-clock audit must stay on five authorized rows")
    if abs(float(summary["strict_delta_z_window"]) - float(policy["strict_delta_z_window"])) > 1e-12:
        raise SystemExit("strict window mismatch")
    if abs(float(summary["relaxed_delta_z_window"]) - float(policy["relaxed_delta_z_window"])) > 1e-12:
        raise SystemExit("relaxed window mismatch")
    if summary["minimum_clock_entries"] != policy["minimum_clock_entries"]:
        raise SystemExit("minimum clock entry mismatch")
    if summary["minimum_independent_references"] != policy["minimum_independent_references"]:
        raise SystemExit("minimum independent reference mismatch")
    if summary["strict_multi_clock_pass_count"] != "3":
        raise SystemExit("strict support pass count changed")
    if summary["relaxed_multi_clock_pass_count"] != "4":
        raise SystemExit("relaxed support pass count changed")
    if summary["relaxed_multi_clock_failed_radial_indices"] != "4":
        raise SystemExit("expected radial row 4 to remain the relaxed multi-clock blocker")
    if summary["multi_clock_support_endpoint_ready"] != "false":
        raise SystemExit("multi-clock support must not be endpoint-ready")
    if summary["verdict"] != "desi_multi_clock_support_incomplete_not_endpoint_ready":
        raise SystemExit("bad multi-clock support verdict")
    by_index = {row["radial_index"]: row for row in rows}
    if by_index["4"]["relaxed_independent_reference_count"] != "1":
        raise SystemExit("row 4 should fail because relaxed supports are not independently referenced")
    print("paper10_desi_multi_clock_support_per_bao_row_audit_v1: OK")


if __name__ == "__main__":
    main()
