#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBSERVER_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv"
OBSERVER_R5_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_r5_control_resistance_preflight_v1_summary.csv"
OBSERVER_R5_VECTORS = ROOT / "data/derived/void_source_basis_refinement_r5_control_vectors_v1.csv"
OBSERVER_R6_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_r6_completed_reviewer_response_v1_summary.csv"
DESI_GRID = ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_grid.csv"
ZI_SUMMARY = ROOT / "data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv"
OUT = ROOT / "data/derived/joint_common_source_feature_export_v3.csv"
SUMMARY = ROOT / "data/derived/joint_common_source_feature_export_v3_summary.csv"
DOC = ROOT / "docs/joint_common_source_feature_export_v3.md"
CLAIM_BOUNDARY = "joint_common_source_feature_export_v3_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parts(value: str) -> list[str]:
    if not value:
        return []
    return [part for part in value.split(";") if part]


def base_row(
    channel_id: str,
    row_type: str,
    source_row_id: str,
    feature_name: str,
    feature_value: str,
    feature_status: str,
    source_artifact: str,
    control_family: str = "not_applicable",
    control_id: str = "not_applicable",
    caveat: str = "none",
) -> dict[str, str]:
    return {
        "export_id": "JOINT_COMMON_SOURCE_FEATURE_EXPORT_V3",
        "channel_id": channel_id,
        "row_type": row_type,
        "control_family": control_family,
        "control_id": control_id,
        "source_row_id": source_row_id,
        "feature_name": feature_name,
        "feature_value": feature_value,
        "feature_status": feature_status,
        "feature_origin": "frozen_source_artifact",
        "uses_endpoint_scores_or_residuals": "false",
        "candidate_control_symmetric_schema": "true",
        "numeric_t_joint_rescoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "source_artifact": source_artifact,
        "caveat": caveat,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    zi_summary_rows = read_rows(ZI_SUMMARY)
    active_channels = [row["channel_id"] for row in zi_summary_rows if row["channel_id"] != "all_channels"]
    rows: list[dict[str, str]] = []

    observer = read_one(OBSERVER_SUMMARY)
    r5_summary = read_one(OBSERVER_R5_SUMMARY)
    r6_summary = read_one(OBSERVER_R6_SUMMARY)
    if r5_summary["control_resistance_preflight_complete"] != "true":
        raise SystemExit("observer R5 source-feature vectors are not frozen")
    if r5_summary["endpoint_replay_allowed"] != "false":
        raise SystemExit("observer R5 vectors must not authorize endpoint replay")
    if r6_summary["leakage_review_complete"] != "true" or r6_summary["source_unique_ready"] != "true":
        raise SystemExit("observer R6 source-side review is not complete")
    if r6_summary["endpoint_replay_allowed"] != "false":
        raise SystemExit("observer R6 review must not authorize endpoint replay")
    r5_by_row = {
        (row["source_row_index"], row["feature_id"]): row
        for row in read_rows(OBSERVER_R5_VECTORS)
    }
    selected_indices = set(parts(observer["source_row_indices"]))
    selected_cids = dict(zip(parts(observer["source_row_indices"]), parts(observer["cids"]), strict=True))
    observer_features = sorted({feature_id for _, feature_id in r5_by_row if _ in selected_indices})
    control_fields = [
        "zero_control",
        "wrong_sign_control",
        "deterministic_row_shuffle_control",
        "threshold_low_control",
        "threshold_high_control",
    ]
    for source_row_index in sorted(selected_indices, key=int):
        cid = selected_cids[source_row_index]
        source_row = f"pantheon_row_{source_row_index}:{cid}"
        for feature_id in observer_features:
            vector = r5_by_row[(source_row_index, feature_id)]
            rows.append(
                base_row(
                    "observer_path_basis_low_z",
                    "candidate",
                    source_row,
                    feature_id,
                    vector["candidate_source_feature"],
                    "available_r6_accepted_source_side",
                    str(OBSERVER_R5_VECTORS.relative_to(ROOT)),
                    caveat="R6_accepted_source_side_only_endpoint_replay_forbidden",
                )
            )
            for field in control_fields:
                rows.append(
                    base_row(
                        "observer_path_basis_low_z",
                        "matched_control",
                        source_row,
                        feature_id,
                        vector[field],
                        "available_r6_accepted_source_side",
                        str(OBSERVER_R5_VECTORS.relative_to(ROOT)),
                        control_family=field,
                        control_id=f"{field}:{feature_id}",
                        caveat="R6_accepted_source_side_only_endpoint_replay_forbidden",
                    )
                )

    for branch in read_rows(DESI_GRID):
        row_type = "candidate" if branch["control_family"] == "candidate" else "matched_control"
        vector = parts(branch["shape_vector"])
        for i, value in enumerate(vector, start=1):
            rows.append(
                base_row(
                    "desi_shape_time_readout",
                    row_type,
                    f"desi_shape_component_{i}",
                    "source_native_shape_component",
                    value,
                    "available",
                    str(DESI_GRID.relative_to(ROOT)),
                    control_family=branch["control_family"],
                    control_id=branch["branch"],
                )
            )

    if "kids_lensing_cosebis_low_mode" in active_channels:
        rows.append(
            base_row(
                "kids_lensing_cosebis_low_mode",
                "candidate",
                "kids_low_mode_scope",
                "row_level_lensing_feature_vector",
                "not_exported",
                "missing",
                "data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv",
                caveat="source_native_lensing_feature_export_not_yet_promoted",
            )
        )

    channels = sorted({row["channel_id"] for row in rows})
    complete_channels = sorted(
        {
            channel
            for channel in channels
            if any(row["channel_id"] == channel and row["feature_status"].startswith("available") for row in rows)
            and not any(row["channel_id"] == channel and row["feature_status"] == "missing" for row in rows)
        }
    )
    caveated_channels = sorted(
        {
            row["channel_id"]
            for row in rows
            if "caveated" in row["feature_status"] or row["feature_status"] == "missing"
        }
    )
    summary = {
        "export_id": "JOINT_COMMON_SOURCE_FEATURE_EXPORT_V3",
        "active_channel_count": str(len(active_channels)),
        "exported_channel_count": str(len(channels)),
        "total_feature_rows": str(len(rows)),
        "observer_feature_count": str(len(observer_features)),
        "observer_selected_source_rows": str(len(selected_indices)),
        "complete_or_caveated_feature_channels": ";".join(complete_channels) if complete_channels else "none",
        "caveated_or_missing_channels": ";".join(caveated_channels) if caveated_channels else "none",
        "candidate_control_symmetric_schema": "true",
        "all_channels_have_nontrivial_row_features": "false",
        "observer_path_row_features_exported": "true",
        "observer_path_r6_leakage_review_complete": "true",
        "observer_path_source_unique_ready": "true",
        "source_feature_export_complete_for_penalty": "false",
        "numeric_t_joint_rescoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "COMMON_EXPORT_V3_OBSERVER_R6_CLOSED_KIDS_STILL_BLOCKS_PENALTY",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint common source feature export v3",
                "",
                "**Doc class:** residual-blind common source-feature export.",
                "**Status:** observer R6 source-side review closed; still not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "Version 3 promotes the already frozen R5 observer-path source vectors",
                "into the common feature schema after the completed R6 source-side",
                "review accepted them as caveated source-side evidence. The review does",
                "not authorize endpoint replay or validation.",
                "",
                "DESI shape/time remains complete in the common schema. KiDS remains an",
                "explicit missing-feature marker. Therefore the common export is stronger",
                "than v2 but still does not authorize any penalty or `T_joint` rescoring.",
                "",
                f"Verdict: `{summary['verdict']}`.",
                "",
            ]
        )
    )
    print(
        "JOINT_COMMON_SOURCE_FEATURE_EXPORT_V3_BUILT "
        f"rows={summary['total_feature_rows']} observer_features={summary['observer_feature_count']}"
    )


if __name__ == "__main__":
    main()
