#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/sdss_bao_time_readout_observable_route_audit_policy_v1.csv"
DESIGN = ROOT / "data/derived/sdss_multitracer_bao_rsd_design_matrix_v1.csv"
OUT = ROOT / "data/derived/sdss_bao_time_readout_observable_route_audit_v1.csv"
SUMMARY = ROOT / "data/derived/sdss_bao_time_readout_observable_route_audit_v1_summary.csv"
CLAIM_BOUNDARY = "sdss_bao_time_readout_observable_route_audit_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalize(values: list[float]) -> tuple[list[float], float, float]:
    center = sum(values) / len(values)
    scale = math.sqrt(sum((value - center) ** 2 for value in values) / len(values))
    if scale <= 0:
        raise SystemExit("degenerate radial BAO route vector")
    return [(value - center) / scale for value in values], center, scale


def main() -> None:
    policy = read_one(POLICY)
    if policy["status"] != "SOURCE_SIDE_ROUTE_AUDIT_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad policy status")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"{field} must be false")
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad claim boundary")

    design = read_rows(DESIGN)
    radial_rows = [row for row in design if row["observable"] == policy["observable_selector"]]
    if len(radial_rows) != 2:
        raise SystemExit(f"expected two SDSS radial BAO rows, got {len(radial_rows)}")
    raw_values = [-math.log(float(row["observed_value"])) for row in radial_rows]
    basis, center, scale = normalize(raw_values)
    rows: list[dict[str, str]] = []
    for row, raw, value in zip(radial_rows, raw_values, basis):
        rows.append(
            {
                "audit_id": policy["audit_id"],
                "vector_index": row["vector_index"],
                "z_eff": row["z_eff"],
                "observable": row["observable"],
                "observed_DH_over_rd": row["observed_value"],
                "published_sigma": row["published_sigma"],
                "time_readout_raw_minus_log_DH_over_rd": f"{raw:.12g}",
                "W_time_bao_radial_basis": f"{value:.12g}",
                "basis_interpretation": "minus_log_DH_over_rd_proportional_to_log_H_plus_constant_rd",
                "rd_nuisance_status": "rd_not_solved_here_route_requires_future_joint_BAO_handling",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    z_values = sorted(float(row["z_eff"]) for row in radial_rows)
    summary = [
        {
            "audit_id": policy["audit_id"],
            "status": "SOURCE_SIDE_ROUTE_AUDIT_COMPLETE_NOT_REPLAY_NOT_VALIDATION",
            "input_rows": str(len(design)),
            "radial_bao_rows": str(len(radial_rows)),
            "redshift_bin_count": str(len(set(row["z_eff"] for row in radial_rows))),
            "redshift_range": f"{z_values[0]:.12g};{z_values[-1]:.12g}",
            "basis_center": f"{center:.12g}",
            "basis_scale": f"{scale:.12g}",
            "independent_from_pantheon_distance_residuals": "true",
            "independent_from_cc_clock_level_route": "true",
            "rd_nuisance_unresolved": "true",
            "underresolved_for_endpoint_route": "true",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "independent_radial_bao_time_observable_present_but_underresolved_not_replay",
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_SDSS_BAO_TIME_READOUT_ROUTE_AUDIT_BUILT "
        f"radial_bao_rows={summary[0]['radial_bao_rows']} verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
