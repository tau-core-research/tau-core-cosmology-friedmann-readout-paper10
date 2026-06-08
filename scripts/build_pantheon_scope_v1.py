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

Z_MIN = 0.023


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_covariance_dimension(path: Path) -> int:
    with path.open() as f:
        first = f.readline().strip()
    return int(float(first))


def include_row(row: dict[str, str]) -> tuple[bool, str]:
    if row["IS_CALIBRATOR"] == "1":
        return False, "calibrator_excluded"
    if float(row["zHD"]) < Z_MIN:
        return False, "below_zHD_min"
    return True, "included"


def main() -> None:
    with PANTHEON_DATA.open() as f:
        rows = list(csv.DictReader(f, delimiter=" ", skipinitialspace=True))
    cov_dim = read_covariance_dimension(PANTHEON_COV)
    if len(rows) != cov_dim:
        raise SystemExit(f"Pantheon table/cov mismatch: rows={len(rows)} cov_dim={cov_dim}")
    with SCOPE.open(newline="") as f:
        scope_rows = list(csv.DictReader(f))
    if len(scope_rows) != 1:
        raise SystemExit("expected exactly one Pantheon scope row")
    scope = scope_rows[0]
    if scope["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("scope must not allow endpoint scoring")

    ROW_MASK.parent.mkdir(parents=True, exist_ok=True)
    mask_rows: list[dict[str, str]] = []
    included = 0
    z_values: list[float] = []
    for idx, row in enumerate(rows):
        is_included, reason = include_row(row)
        if is_included:
            included += 1
            z_values.append(float(row["zHD"]))
        mask_rows.append(
            {
                "scope_id": scope["scope_id"],
                "source_row_index": str(idx),
                "CID": row["CID"],
                "zHD": row["zHD"],
                "IS_CALIBRATOR": row["IS_CALIBRATOR"],
                "USED_IN_SH0ES_HF": row["USED_IN_SH0ES_HF"],
                "included": str(is_included).lower(),
                "exclusion_reason": reason,
            }
        )

    with ROW_MASK.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "scope_id",
                "source_row_index",
                "CID",
                "zHD",
                "IS_CALIBRATOR",
                "USED_IN_SH0ES_HF",
                "included",
                "exclusion_reason",
            ],
        )
        writer.writeheader()
        writer.writerows(mask_rows)

    excluded = len(rows) - included
    summary = {
        "scope_id": scope["scope_id"],
        "status": scope["status"],
        "row_rule_id": scope["row_rule_id"],
        "zHD_min": str(Z_MIN),
        "total_rows": str(len(rows)),
        "included_rows": str(included),
        "excluded_rows": str(excluded),
        "covariance_dimension": str(cov_dim),
        "min_included_zHD": f"{min(z_values):.6g}" if z_values else "",
        "max_included_zHD": f"{max(z_values):.6g}" if z_values else "",
        "pantheon_data_sha256": sha256(PANTHEON_DATA),
        "pantheon_cov_sha256": sha256(PANTHEON_COV),
        "row_mask_sha256": sha256(ROW_MASK),
        "endpoint_scoring_allowed": "false",
        "forbidden_inputs_checked": scope["forbidden_inputs"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

    print(
        "PAPER10_PANTHEON_SCOPE_V1_BUILT "
        f"total={len(rows)} included={included} endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()
