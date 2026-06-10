#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT
    / "data"
    / "source_manifest"
    / "void_source_basis_refinement_v2_observer_orientation_kernel_v2_manifest.csv"
)
SOURCE_AUDIT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_sky_z_source_audit_v1.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_observer_orientation_kernel_v2.csv"
SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_observer_orientation_kernel_v2_summary.csv"
)
CLAIM_BOUNDARY = "v2_observer_orientation_kernel_v2_source_side_not_scoring"


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


def normalized(values: list[float]) -> list[float]:
    max_abs = max(abs(v) for v in values)
    if max_abs <= 0.0:
        raise SystemExit("cannot normalize zero observer-orientation kernel")
    return [v / max_abs for v in values]


def main() -> None:
    manifest = read_one(MANIFEST)
    if manifest["status"] != "PREDECLARED_SOURCE_SIDE_KERNEL_NOT_SCORING":
        raise SystemExit("observer-orientation kernel manifest status mismatch")
    if manifest["endpoint_replay_allowed"] != "false" or manifest["endpoint_validation_claimed"] != "false":
        raise SystemExit("kernel manifest must not authorize replay or validation")
    if manifest["physical_lensing_path_weight_claimed"] != "false":
        raise SystemExit("kernel manifest must not claim physical path weight")
    rows = read_rows(SOURCE_AUDIT)
    if len(rows) != 12:
        raise SystemExit("observer-orientation kernel requires 12 source-audit rows")
    for row in rows:
        if row["claim_boundary"] != "v2_sky_z_source_audit_not_scoring_not_validation":
            raise SystemExit("source audit claim boundary mismatch")
        for key in [
            "contains_distance_residuals",
            "contains_fit_statistics",
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "physical_lensing_path_weight_claimed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"source audit row must keep {key}=false")

    sky_z_values = [float(row["sky_z"]) for row in rows]
    mean_sky_z = sum(sky_z_values) / len(sky_z_values)
    raw_reference = [float(row["W_path_source_value"]) * float(row["sky_z"]) for row in rows]
    raw_primary = [
        float(row["W_path_source_value"]) * (float(row["sky_z"]) - mean_sky_z)
        for row in rows
    ]
    raw_axis_x = [float(row["W_path_source_value"]) * float(row["sky_x"]) for row in rows]
    raw_axis_y = [float(row["W_path_source_value"]) * float(row["sky_y"]) for row in rows]
    reference = normalized(raw_reference)
    primary = normalized(raw_primary)
    axis_x = normalized(raw_axis_x)
    axis_y = normalized(raw_axis_y)

    out_rows = []
    for i, row in enumerate(rows):
        out_rows.append(
            {
                "artifact_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_OBSERVER_ORIENTATION_KERNEL_V2",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "ra_deg": row["ra_deg"],
                "dec_deg": row["dec_deg"],
                "sky_x": row["sky_x"],
                "sky_y": row["sky_y"],
                "sky_z": row["sky_z"],
                "mean_sky_z_scope": f"{mean_sky_z:.12g}",
                "centered_sky_z": f"{float(row['sky_z']) - mean_sky_z:.12g}",
                "W_path_source_value": row["W_path_source_value"],
                "K_reference_raw_W_path_times_sky_z": f"{raw_reference[i]:.12g}",
                "K_reference_normalized": f"{reference[i]:.12g}",
                "K_primary_raw_W_path_times_centered_sky_z": f"{raw_primary[i]:.12g}",
                "K_primary_normalized": f"{primary[i]:.12g}",
                "K_axis_x_reference_normalized": f"{axis_x[i]:.12g}",
                "K_axis_y_reference_normalized": f"{axis_y[i]:.12g}",
                "normalization_rule": manifest["normalization_rule"],
                "contains_distance_residuals": "false",
                "contains_fit_statistics": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    out_rows.sort(key=lambda row: int(row["source_row_index"]))
    write_csv(OUT, out_rows)
    summary = [
        {
            "artifact_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_OBSERVER_ORIENTATION_KERNEL_V2",
            "status": "OBSERVER_ORIENTATION_KERNEL_V2_BUILT_NOT_SCORING",
            "n_rows": str(len(out_rows)),
            "primary_kernel": manifest["primary_kernel"],
            "reference_kernel": manifest["reference_kernel"],
            "mean_sky_z_scope": f"{mean_sky_z:.12g}",
            "primary_positive_count": str(sum(v > 0.0 for v in raw_primary)),
            "primary_negative_count": str(sum(v < 0.0 for v in raw_primary)),
            "reference_positive_count": str(sum(v > 0.0 for v in raw_reference)),
            "reference_negative_count": str(sum(v < 0.0 for v in raw_reference)),
            "max_abs_primary_raw": f"{max(abs(v) for v in raw_primary):.12g}",
            "max_abs_reference_raw": f"{max(abs(v) for v in raw_reference):.12g}",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "recommended_next_action": "external_review_before_any_observer_orientation_v2_replay",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_OBSERVER_ORIENTATION_KERNEL_V2_BUILT "
        f"n_rows={len(out_rows)} mean_sky_z={mean_sky_z:.6g}"
    )


if __name__ == "__main__":
    main()

