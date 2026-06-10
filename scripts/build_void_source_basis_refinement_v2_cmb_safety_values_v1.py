#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOW_Z_MASK = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
CMB_RUN = ROOT / "data" / "source_manifest" / "cmb_safety_lowz_support_v1.csv"
CMB_SUPPORT = ROOT / "data" / "derived" / "cmb_safety_lowz_support_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_cmb_safety_values.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_cmb_safety_values_summary.csv"

COMPONENT_ID = "V2_CMB_SAFETY"
CLAIM_BOUNDARY = "v2_cmb_safety_source_values_frozen_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: float) -> str:
    return f"{value:.12g}"


def main() -> None:
    run = read_one(CMB_RUN)
    support = read_one(CMB_SUPPORT)
    if run["status"] != "CMB_SAFETY_SUPPORT_CHECK_NOT_VALIDATION":
        raise SystemExit("unexpected CMB support run status")
    if support["passes_cmb_lowz_support_check"] != "true":
        raise SystemExit("CMB low-z support check is not passing")
    if run["endpoint_scoring_allowed"] != "false":
        raise SystemExit("CMB safety run must remain endpoint disabled")
    rows = [row for row in read_rows(LOW_Z_MASK) if row["included"] == "true"]
    z_floor = float(run["z_safety_floor"])
    z_recombination = float(run["z_recombination_proxy"])
    if not rows:
        raise SystemExit("no included low-z rows found")

    out_rows: list[dict[str, str]] = []
    for row in rows:
        z = float(row["zHD"])
        below_floor = z < z_floor
        out_rows.append(
            {
                "component_id": COMPONENT_ID,
                "channel_id": "W_PATH_PROJECTION;W_TIME_READOUT",
                "source_scope": "LOW_Z_PANTHEON_VOID_SCOPE_CANDIDATE_POLICY_V1_INCLUDED_ROWS",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "z_safety_floor": fmt(z_floor),
                "z_recombination_proxy": fmt(z_recombination),
                "low_z_below_safety_floor": str(below_floor).lower(),
                "cmb_lowz_support_passed": support["passes_cmb_lowz_support_check"],
                "cmb_map_data_used": "false",
                "cmb_likelihood_used": "false",
                "cmb_safety_off_control": "0",
                "cmb_wrong_prior_control": "1",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "contains_fit_statistics": "false",
                "contains_cmb_map_data": "false",
                "contains_cmb_likelihood": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    below_count = sum(1 for row in out_rows if row["low_z_below_safety_floor"] == "true")
    summary = [
        {
            "component_id": COMPONENT_ID,
            "status": "V2_CMB_SAFETY_VALUES_FROZEN_NOT_ENDPOINT_READY",
            "source_artifact": str(CMB_SUPPORT.relative_to(ROOT)),
            "low_z_scope_artifact": str(LOW_Z_MASK.relative_to(ROOT)),
            "output_artifact": str(OUT.relative_to(ROOT)),
            "n_rows": str(len(out_rows)),
            "rows_below_safety_floor": str(below_count),
            "z_safety_floor": fmt(z_floor),
            "z_recombination_proxy": fmt(z_recombination),
            "cmb_lowz_support_passed": support["passes_cmb_lowz_support_check"],
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "contains_endpoint_scores": "false",
            "contains_distance_residuals": "false",
            "contains_fit_statistics": "false",
            "contains_cmb_map_data": "false",
            "contains_cmb_likelihood": "false",
            "verdict": "cmb_safety_values_frozen_not_endpoint_ready",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(OUT, out_rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_CMB_SAFETY_VALUES_BUILT "
        f"rows={len(out_rows)} cmb_lowz_support_passed={support['passes_cmb_lowz_support_check']} "
        "endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
