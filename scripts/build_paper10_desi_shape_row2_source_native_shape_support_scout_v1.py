#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_row2_source_native_shape_support_scout_policy_v1.csv"
SOURCE_PLAN = ROOT / "data/derived/paper10_desi_shape_row2_post_window_review_source_plan_v1_summary.csv"
INVENTORY = ROOT / "data/derived/paper10_desi_dr2_bao_source_inventory_v1.csv"
COV = ROOT / "data/raw/desi_dr2_bao/desi_gaussian_bao_ALL_GCcomb_cov.txt"
OUT = ROOT / "data/derived/paper10_desi_shape_row2_source_native_shape_support_scout_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_source_native_shape_support_scout_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_source_native_shape_support_scout_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_source_native_shape_support_scout_not_validation"
ROW2_LEFT_Z = 0.934
ROW2_RIGHT_Z = 1.321


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: float) -> str:
    return f"{float(value):.12g}"


def write_doc(summary: dict[str, str], rows: list[dict[str, str]]) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    table = [
        "| Row | z | quantity | value | role |",
        "| ---: | ---: | --- | ---: | --- |",
    ]
    for row in rows:
        table.append(
            "| "
            + " | ".join(
                [
                    row["source_row_index"],
                    row["z_eff"],
                    row["quantity"],
                    row["value"],
                    row["support_role"],
                ]
            )
            + " |"
        )
    DOC.write_text(
        "\n".join(
            [
                "# Paper10 DESI shape row2 source-native shape-support scout v1",
                "",
                "**Doc class:** source-native BAO shape-support scout",
                "**Reader role:** reviewer / source-acquisition auditor",
                "**Status:** source-side support present, not replay, not validation",
                "**Canonical parent:** Paper10 DESI shape-route replay chain",
                "",
                "This scout addresses the second P0 target in the post-window-review",
                "source plan: source-native shape support for the row-2 interval. It",
                "uses only the frozen DESI DR2 BAO mean vector and covariance block.",
                "It does not use endpoint residuals, endpoint scores, or fit feedback.",
                "",
                "Frozen result:",
                "",
                f"- row-2 interval: `{summary['row2_interval']}`",
                f"- source-native rows found: `{summary['source_native_row_count']}`",
                f"- covariance positive definite: `{summary['row2_covariance_positive_definite']}`",
                f"- shape vector: `{summary['shape_vector_components']}`",
                f"- row2 promotion ready: `{summary['row2_promotion_ready']}`",
                f"- endpoint replay allowed: `{summary['endpoint_replay_allowed']}`",
                "",
                "Frozen source rows:",
                "",
                *table,
                "",
                "Interpretation:",
                "",
                "Row 2 has source-native DESI BAO shape information at both interval",
                "ends (`DM/rs` and `DH/rs`) with a well-formed covariance subblock.",
                "This is stronger source context than a clock near-miss, but it is not",
                "a replay authorization and does not by itself promote the route.",
                "",
                "Claim boundary:",
                "",
                "```text",
                summary["claim_boundary"],
                "```",
                "",
                f"Machine verdict: `{summary['verdict']}`.",
                "",
            ]
        )
    )


def main() -> None:
    policy = one_row(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad row2 source-native shape-support scout claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    source_plan = one_row(SOURCE_PLAN)
    if source_plan["source_plan_status"] != "ROW2_SOURCE_REOPENED_CAVEATED_LEFT_ENDPOINT_STILL_NOT_RELEASED":
        raise SystemExit("source-native scout expects caveated source reopen without endpoint release")
    for field in ["row2_promotion_ready", "endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if source_plan[field] != "false":
            raise SystemExit(f"source plan {field} must remain false")

    inventory = read_rows(INVENTORY)
    selected = [
        row
        for row in inventory
        if row["z_eff"] in {f"{ROW2_LEFT_Z:.8f}", f"{ROW2_RIGHT_Z:.8f}"}
        and row["quantity"] in {"DM_over_rs", "DH_over_rs"}
    ]
    selected = sorted(selected, key=lambda row: int(row["row_index"]))
    if len(selected) != 4:
        raise SystemExit("expected four row2 source-native BAO shape rows")
    by_key = {(float(row["z_eff"]), row["quantity"]): row for row in selected}
    dm_left = float(by_key[(ROW2_LEFT_Z, "DM_over_rs")]["value"])
    dh_left = float(by_key[(ROW2_LEFT_Z, "DH_over_rs")]["value"])
    dm_right = float(by_key[(ROW2_RIGHT_Z, "DM_over_rs")]["value"])
    dh_right = float(by_key[(ROW2_RIGHT_Z, "DH_over_rs")]["value"])
    dz = ROW2_RIGHT_Z - ROW2_LEFT_Z
    shape_values = {
        "delta_log_DM_over_rs": math.log(dm_right) - math.log(dm_left),
        "delta_log_DH_over_rs": math.log(dh_right) - math.log(dh_left),
        "delta_log_anisotropy_DM_over_DH": (math.log(dm_right / dh_right) - math.log(dm_left / dh_left)),
        "slope_log_DM_over_rs": (math.log(dm_right) - math.log(dm_left)) / dz,
        "slope_log_DH_over_rs": (math.log(dh_right) - math.log(dh_left)) / dz,
    }
    shape_vector = ";".join(f"{key}={fmt(value)}" for key, value in shape_values.items())
    cov = np.loadtxt(COV)
    indices = [int(row["row_index"]) for row in selected]
    subcov = cov[np.ix_(indices, indices)]
    eig = np.linalg.eigvalsh(subcov)
    cov_positive = bool(np.all(eig > 0))

    out_rows = []
    for row in selected:
        support_role = (
            "row2_left_transverse_shape"
            if row["z_eff"] == f"{ROW2_LEFT_Z:.8f}" and row["quantity"] == "DM_over_rs"
            else "row2_left_radial_shape"
            if row["z_eff"] == f"{ROW2_LEFT_Z:.8f}"
            else "row2_right_transverse_shape"
            if row["quantity"] == "DM_over_rs"
            else "row2_right_radial_shape"
        )
        out_rows.append(
            {
                "scout_id": policy["scout_id"],
                "shape_row": "2",
                "row2_interval": f"{ROW2_LEFT_Z:.3f}-{ROW2_RIGHT_Z:.3f}",
                "source_row_index": row["row_index"],
                "z_eff": row["z_eff"],
                "quantity": row["quantity"],
                "value": row["value"],
                "support_role": support_role,
                "source_family": "DESI_DR2_PUBLIC_BAO",
                "source_native_shape_component": "true",
                "uses_endpoint_scores": "false",
                "uses_endpoint_residuals": "false",
                "row2_promotion_ready": "false",
                "shape_route_promotion_allowed": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, out_rows)
    summary = {
        "scout_id": policy["scout_id"],
        "status": "DESI_SHAPE_ROW2_SOURCE_NATIVE_SHAPE_SUPPORT_SCOUT_BUILT_NOT_REPLAY_NOT_VALIDATION",
        "row2_interval": f"{ROW2_LEFT_Z:.3f}-{ROW2_RIGHT_Z:.3f}",
        "source_native_row_count": str(len(out_rows)),
        "source_native_quantities": "DM_over_rs;DH_over_rs",
        "row2_covariance_indices": ";".join(str(index) for index in indices),
        "row2_covariance_positive_definite": "true" if cov_positive else "false",
        "row2_covariance_min_eigenvalue": fmt(float(eig[0])),
        "shape_vector_components": shape_vector,
        "uses_endpoint_scores": "false",
        "uses_endpoint_residuals": "false",
        "left_endpoint_release_allowed": "false",
        "row2_promotion_ready": "false",
        "shape_route_promotion_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "row2_source_native_desi_bao_shape_support_present_but_not_promotion_ready",
        "recommended_next_action": "prepare_source_native_shape_support_review_or_keep_as_non_promotional_context_before_replay",
    }
    write_csv(SUMMARY, [summary])
    write_doc(summary, out_rows)
    print("PAPER10_DESI_SHAPE_ROW2_SOURCE_NATIVE_SHAPE_SUPPORT_SCOUT_BUILT")


if __name__ == "__main__":
    main()
