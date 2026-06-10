#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1.csv"
DESIGN_SUMMARY = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1_summary.csv"
INACTIVITY = ROOT / "data" / "derived" / "void_channel_inactivity_diagnostic_v1_summary.csv"
TRANSFORM = ROOT / "data" / "source_manifest" / "void_web_source_native_transform_rule_v1.csv"
OUT_BINS = ROOT / "data" / "derived" / "void_source_basis_audit_v1_redshift_bins.csv"
OUT_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_audit_v1_summary.csv"

D_H_MPC_OVER_H = 2997.92458
Z_BINS = [
    (0.0, 0.05),
    (0.05, 0.10),
    (0.10, 0.20),
    (0.20, 0.50),
    (0.50, 1.00),
    (1.00, 3.00),
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def f(value: str) -> float:
    return float(value)


def main() -> None:
    design = read_rows(DESIGN)
    design_summary = read_one(DESIGN_SUMMARY)
    inactivity = read_one(INACTIVITY)
    transform = read_one(TRANSFORM)
    if transform["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("void/web transform must remain endpoint disabled")

    void_max_r = f(design_summary["void_max_r"])
    void_min_r = f(design_summary["void_min_r"])
    z_support_min = void_min_r / D_H_MPC_OVER_H
    z_support_max = void_max_r / D_H_MPC_OVER_H
    z_values = [f(row["zHD"]) for row in design]
    nonzero_rows = [row for row in design if f(row["W_void_source_native_basis"]) > 0.0]
    zero_rows = [row for row in design if f(row["W_void_source_native_basis"]) == 0.0]

    bin_rows: list[dict[str, str]] = []
    for lo, hi in Z_BINS:
        rows = [row for row in design if lo <= f(row["zHD"]) < hi]
        active = [row for row in rows if f(row["W_void_source_native_basis"]) > 0.0]
        mean_weight = sum(f(row["W_void_source_native_basis"]) for row in rows) / len(rows) if rows else 0.0
        bin_rows.append(
            {
                "z_bin_lo": f"{lo:.3f}",
                "z_bin_hi": f"{hi:.3f}",
                "pantheon_rows": str(len(rows)),
                "void_active_rows": str(len(active)),
                "void_active_fraction": f"{len(active) / len(rows):.12g}" if rows else "0",
                "mean_void_basis": f"{mean_weight:.12g}",
                "physical_validation_claimed": "false",
                "claim_boundary": "void_source_basis_audit_not_validation",
            }
        )
    write_csv(OUT_BINS, bin_rows)

    summary = [
        {
            "audit_id": "VOID_SOURCE_BASIS_AUDIT_V1",
            "status": "SOURCE_BASIS_AUDIT_COMPLETE_NOT_VALIDATION",
            "parent_inactivity_diagnostic": inactivity["diagnostic_id"],
            "transform_id": transform["transform_id"],
            "pantheon_rows": str(len(design)),
            "pantheon_z_min": f"{min(z_values):.12g}",
            "pantheon_z_max": f"{max(z_values):.12g}",
            "void_catalog_r_min_mpc_over_h": f"{void_min_r:.12g}",
            "void_catalog_r_max_mpc_over_h": f"{void_max_r:.12g}",
            "void_catalog_z_support_min_proxy": f"{z_support_min:.12g}",
            "void_catalog_z_support_max_proxy": f"{z_support_max:.12g}",
            "void_active_rows": str(len(nonzero_rows)),
            "void_zero_rows": str(len(zero_rows)),
            "void_active_fraction": f"{len(nonzero_rows) / len(design):.12g}",
            "void_zero_fraction": f"{len(zero_rows) / len(design):.12g}",
            "best_nonzero_void_delta_chi2_vs_zero": inactivity["best_nonzero_void_delta_chi2_vs_zero"],
            "source_basis_limitation": "low_z_volume_limited_void_catalog_mapped_to_full_pantheon_distance_block",
            "endpoint_scoring_allowed": "false",
            "physical_validation_claimed": "false",
            "recommended_next_action": "do_not_reopen_endpoint_until_void_mapping_is_rebuilt_for_declared_observable_scope",
            "claim_boundary": "void_source_basis_audit_not_validation",
        }
    ]
    write_csv(OUT_SUMMARY, summary)
    print(
        "PAPER10_VOID_SOURCE_BASIS_AUDIT_V1_BUILT "
        f"z_support_max={summary[0]['void_catalog_z_support_max_proxy']} "
        f"void_active_fraction={summary[0]['void_active_fraction']} "
        "claim_boundary=source_basis_audit_not_validation"
    )


if __name__ == "__main__":
    main()
