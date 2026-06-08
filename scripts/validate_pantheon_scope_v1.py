#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PANTHEON_DATA = ROOT / "data" / "raw" / "pantheon_plus" / "pantheon_plus_mu_covariance" / "Pantheon+SH0ES.dat"
PANTHEON_COV = ROOT / "data" / "raw" / "pantheon_plus" / "pantheon_plus_mu_covariance" / "Pantheon+SH0ES_STAT+SYS.cov"
SCOPE = ROOT / "data" / "source_manifest" / "pantheon_endpoint_scope_v1.csv"
ROW_MASK = ROOT / "data" / "derived" / "pantheon_scope_v1_row_mask.csv"
SUMMARY = ROOT / "data" / "derived" / "pantheon_scope_v1_summary.csv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    scope_rows = read_rows(SCOPE)
    summary_rows = read_rows(SUMMARY)
    mask_rows = read_rows(ROW_MASK)
    if len(scope_rows) != 1:
        raise SystemExit("Pantheon scope must have exactly one scope row")
    if len(summary_rows) != 1:
        raise SystemExit("Pantheon scope summary must have exactly one row")
    scope = scope_rows[0]
    summary = summary_rows[0]
    if scope["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("Pantheon scope endpoint scoring must remain false")
    if summary["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("Pantheon summary endpoint scoring must remain false")
    forbidden = scope["forbidden_inputs"]
    for marker in [
        "distance_residuals",
        "fit_improvement_flags",
        "Tau_residual_parameters",
        "late_time_activation_fit",
    ]:
        if marker not in forbidden:
            raise SystemExit(f"Pantheon scope missing forbidden marker: {marker}")
    included = [row for row in mask_rows if row["included"] == "true"]
    excluded = [row for row in mask_rows if row["included"] == "false"]
    if int(summary["included_rows"]) != len(included):
        raise SystemExit("included row count mismatch")
    if int(summary["excluded_rows"]) != len(excluded):
        raise SystemExit("excluded row count mismatch")
    if summary["pantheon_data_sha256"] != sha256(PANTHEON_DATA):
        raise SystemExit("Pantheon data sha mismatch")
    if summary["pantheon_cov_sha256"] != sha256(PANTHEON_COV):
        raise SystemExit("Pantheon covariance sha mismatch")
    if summary["row_mask_sha256"] != sha256(ROW_MASK):
        raise SystemExit("Pantheon row mask sha mismatch")
    if not included:
        raise SystemExit("Pantheon scope includes no rows")
    if any(row["IS_CALIBRATOR"] == "1" for row in included):
        raise SystemExit("Pantheon scope includes calibrators")
    if any(float(row["zHD"]) < float(summary["zHD_min"]) for row in included):
        raise SystemExit("Pantheon scope includes rows below zHD_min")
    print(
        "PAPER10_PANTHEON_SCOPE_V1_VALIDATED "
        f"included={len(included)} excluded={len(excluded)} "
        "endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()
