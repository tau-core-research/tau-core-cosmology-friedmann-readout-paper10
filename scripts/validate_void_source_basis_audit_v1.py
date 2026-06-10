#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_audit_v1_summary.csv"
BINS = ROOT / "data" / "derived" / "void_source_basis_audit_v1_redshift_bins.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    summary = read_one(SUMMARY)
    bins = read_rows(BINS)
    require(summary["status"] == "SOURCE_BASIS_AUDIT_COMPLETE_NOT_VALIDATION", "status mismatch")
    require(summary["endpoint_scoring_allowed"] == "false", "audit must not allow endpoint scoring")
    require(summary["physical_validation_claimed"] == "false", "audit must not claim validation")
    require(summary["claim_boundary"] == "void_source_basis_audit_not_validation", "claim boundary mismatch")
    require(
        summary["source_basis_limitation"] == "low_z_volume_limited_void_catalog_mapped_to_full_pantheon_distance_block",
        "source-basis limitation changed",
    )
    require(float(summary["void_catalog_z_support_max_proxy"]) < 0.2, "void catalogue support should be low-z")
    require(float(summary["pantheon_z_max"]) > 2.0, "Pantheon scope should remain full high-z scope")
    require(float(summary["void_active_fraction"]) < 0.5, "void active fraction should remain limited")
    require(float(summary["best_nonzero_void_delta_chi2_vs_zero"]) > 0.0, "nonzero void should remain disfavored")
    require({row["physical_validation_claimed"] for row in bins} == {"false"}, "bin rows must not claim validation")
    high_z_bins = [row for row in bins if float(row["z_bin_lo"]) >= 0.2]
    require(high_z_bins, "expected high-z bins")
    require(all(float(row["void_active_fraction"]) == 0.0 for row in high_z_bins), "high-z bins must have zero void support")
    print(
        "PAPER10_VOID_SOURCE_BASIS_AUDIT_V1_VALIDATED "
        f"z_support_max={summary['void_catalog_z_support_max_proxy']} "
        f"void_active_fraction={summary['void_active_fraction']} "
        "claim_boundary=source_basis_audit_not_validation"
    )


if __name__ == "__main__":
    main()
