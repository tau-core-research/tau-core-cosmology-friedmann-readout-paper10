#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

try:
    from build_pantheon_void_web_source_native_design_matrix_v1 import (
        D_H_MPC_OVER_H,
        load_void_profile,
        load_web_profile,
        nearest_lookup,
        read_one,
    )
except ImportError:
    from scripts.build_pantheon_void_web_source_native_design_matrix_v1 import (
        D_H_MPC_OVER_H,
        load_void_profile,
        load_web_profile,
        nearest_lookup,
        read_one,
    )


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "data" / "source_manifest" / "cmb_safety_lowz_support_v1.csv"
OUT = ROOT / "data" / "derived" / "cmb_safety_lowz_support_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "cmb_safety_lowz_support_v1_summary.csv"


def evaluate(z: float, void_centers: list[float], void_values: list[float], web_centers: list[float], web_values: list[float]) -> dict[str, str]:
    r_proxy = D_H_MPC_OVER_H * z
    w_void = nearest_lookup(r_proxy, void_centers, void_values, outside_zero=True)
    w_web = nearest_lookup(z, web_centers, web_values, outside_zero=True)
    return {
        "z_probe": f"{z:.12g}",
        "r_proxy_mpc_over_h": f"{r_proxy:.12g}",
        "W_void_source_native_basis": f"{w_void:.12g}",
        "W_web_source_native_basis": f"{w_web:.12g}",
        "passes_zero_support": "true" if abs(w_void) == 0.0 and abs(w_web) == 0.0 else "false",
    }


def main() -> None:
    run = read_one(RUN)
    if run["status"] != "CMB_SAFETY_SUPPORT_CHECK_NOT_VALIDATION":
        raise SystemExit("CMB safety run status mismatch")
    if run["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("CMB safety check must remain endpoint disabled")
    forbidden = run["forbidden_inputs"]
    for marker in ["posthoc_cmb_map_selection", "late_time_fit_parameters_without_prior_check"]:
        if marker not in forbidden:
            raise SystemExit(f"CMB safety check missing forbidden marker: {marker}")
    void_centers, void_values, void_stats = load_void_profile()
    web_centers, web_values, web_stats = load_web_profile()
    z_recombination = float(run["z_recombination_proxy"])
    z_floor = float(run["z_safety_floor"])
    rows = [
        {
            "run_id": run["run_id"],
            "probe_id": "z_safety_floor",
            **evaluate(z_floor, void_centers, void_values, web_centers, web_values),
            "claim_boundary": "cmb_safety_lowz_support_check_not_validation",
        },
        {
            "run_id": run["run_id"],
            "probe_id": "z_recombination_proxy",
            **evaluate(z_recombination, void_centers, void_values, web_centers, web_values),
            "claim_boundary": "cmb_safety_lowz_support_check_not_validation",
        },
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    pass_status = all(row["passes_zero_support"] == "true" for row in rows)
    summary = {
        "run_id": run["run_id"],
        "status": run["status"],
        "n_probe_rows": str(len(rows)),
        "z_recombination_proxy": run["z_recombination_proxy"],
        "z_safety_floor": run["z_safety_floor"],
        "void_max_r": f"{void_stats['void_max_r']:.12g}",
        "web_bins": str(int(web_stats["web_bins"])),
        "web_rows_usable": str(int(web_stats["web_rows_usable"])),
        "passes_cmb_lowz_support_check": "true" if pass_status else "false",
        "endpoint_scoring_allowed": "false",
        "contains_cmb_map_data": "false",
        "contains_cmb_likelihood": "false",
        "contains_fit_statistics": "false",
        "claim_boundary": "cmb_safety_lowz_support_check_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_CMB_SAFETY_LOWZ_SUPPORT_V1_BUILT "
        f"passes={summary['passes_cmb_lowz_support_check']} "
        "claim_boundary=cmb_safety_lowz_support_check_not_validation"
    )


if __name__ == "__main__":
    main()
