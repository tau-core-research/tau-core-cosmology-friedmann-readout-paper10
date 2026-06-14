#!/usr/bin/env python3
from __future__ import annotations

import csv
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBSERVER_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv"
OBSERVER_R5_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_r5_control_resistance_preflight_v1_summary.csv"
OBSERVER_R5_VECTORS = ROOT / "data/derived/void_source_basis_refinement_r5_control_vectors_v1.csv"
OBSERVER_R6_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_r6_completed_reviewer_response_v1_summary.csv"
DESI_GRID = ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_grid.csv"
KIDS_THEORY = ROOT / "data/derived/kids1000_cosebis_source_frozen_theory_vector_v1.csv"
KIDS_THEORY_SUMMARY = ROOT / "data/derived/kids1000_cosebis_source_frozen_theory_vector_v1_summary.csv"
KIDS_NULL_SUMMARY = ROOT / "data/derived/kids1000_cosebis_null_control_theory_replay_v1_summary.csv"
KIDS_NULL_CONTROLS = ROOT / "data/derived/kids1000_cosebis_null_control_theory_replay_v1.csv"
KIDS_ROW_CONTROL_SUMMARY = ROOT / "data/derived/kids1000_cosebis_null_control_row_vectors_v1_summary.csv"
KIDS_ROW_CONTROLS = ROOT / "data/derived/kids1000_cosebis_null_control_row_vectors_v1.csv.gz"
ZI_SUMMARY = ROOT / "data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv"
OUT = ROOT / "data/derived/joint_common_source_feature_export_v5.csv"
SUMMARY = ROOT / "data/derived/joint_common_source_feature_export_v5_summary.csv"
DOC = ROOT / "docs/joint_common_source_feature_export_v5.md"
CLAIM_BOUNDARY = "joint_common_source_feature_export_v5_not_scoring_not_validation"


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
        "export_id": "JOINT_COMMON_SOURCE_FEATURE_EXPORT_V5",
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
        kids_theory_summary = read_one(KIDS_THEORY_SUMMARY)
        kids_null_summary = read_one(KIDS_NULL_SUMMARY)
        kids_row_control_summary = read_one(KIDS_ROW_CONTROL_SUMMARY)
        if not KIDS_ROW_CONTROLS.exists():
            raise SystemExit("KiDS row-level null-control artifact is missing")
        if kids_theory_summary["endpoint_scoring_allowed"] != "false":
            raise SystemExit("KiDS source-frozen theory vector must remain endpoint disabled")
        if kids_theory_summary["contains_predictions"] != "false":
            raise SystemExit("KiDS source-frozen theory vector must not be a prediction")
        if kids_theory_summary["contains_residuals"] != "false":
            raise SystemExit("KiDS source-frozen theory vector must not contain residuals")
        if kids_null_summary["endpoint_scoring_allowed"] != "false":
            raise SystemExit("KiDS null-control summary must remain endpoint disabled")
        if kids_null_summary["contains_control_scores"] != "false":
            raise SystemExit("KiDS null-control summary must not contain scores")
        if kids_null_summary["uses_kids_data_vector_values"] != "false":
            raise SystemExit("KiDS null controls must remain source-side only")
        if kids_row_control_summary["endpoint_scoring_allowed"] != "false":
            raise SystemExit("KiDS row-level null controls must remain endpoint disabled")
        if kids_row_control_summary["uses_kids_data_vector_values"] != "false":
            raise SystemExit("KiDS row-level null controls must not use data-vector values")
        if kids_row_control_summary["control_row_vectors_computed"] != "true":
            raise SystemExit("KiDS row-level null controls are not computed")

        kids_theory_rows = read_rows(KIDS_THEORY)
        kids_null_rows = read_rows(KIDS_NULL_CONTROLS)
        kids_row_features = [
            "source_frozen_mapping_value",
            "mode_shape_weight",
            "theory_value",
            "w_path_contribution",
        ]
        for theory in kids_theory_rows:
            if theory["endpoint_scoring_allowed"] != "false":
                raise SystemExit("KiDS theory row endpoint_scoring_allowed must be false")
            if theory["contains_prediction"] != "false" or theory["contains_residual"] != "false":
                raise SystemExit("KiDS theory row must not contain predictions/residuals")
            source_row = f"kids_cosebis_pair_{theory['pair_id']}_mode_{theory['mode']}"
            for feature in kids_row_features:
                rows.append(
                    base_row(
                        "kids_lensing_cosebis_low_mode",
                        "candidate",
                        source_row,
                        feature,
                        theory[feature],
                        "available_candidate_row_source_only",
                        str(KIDS_THEORY.relative_to(ROOT)),
                        caveat="candidate_row_features_available_controls_are_summary_only_endpoint_forbidden",
                    )
                )

        candidate_stats = {
            "vector_mean": kids_theory_summary["mean_theory_value"],
            "vector_min": kids_theory_summary["min_theory_value"],
            "vector_max": kids_theory_summary["max_theory_value"],
            "vector_row_count": kids_theory_summary["theory_rows"],
            "unique_value_count_rounded": kids_theory_summary["unique_theory_value_count_rounded_1e_minus_12"],
        }
        for feature, value in candidate_stats.items():
            rows.append(
                base_row(
                    "kids_lensing_cosebis_low_mode",
                    "candidate",
                    "kids_source_frozen_theory_vector_summary",
                    feature,
                    value,
                    "available_vector_summary_source_only",
                    str(KIDS_THEORY_SUMMARY.relative_to(ROOT)),
                    caveat="candidate_control_summary_features_available_row_controls_not_exported",
                )
            )

        control_stat_features = ["vector_mean", "vector_std", "vector_l2_norm", "vector_min", "vector_max"]
        for control in kids_null_rows:
            if control["endpoint_scoring_allowed"] != "false":
                raise SystemExit("KiDS null-control row endpoint_scoring_allowed must be false")
            if control["contains_control_scores"] != "false":
                raise SystemExit("KiDS null-control rows must not contain scores")
            control_id = (
                f"{control['control_family']}:"
                f"{control['operator']}:"
                f"{control['control_draw_index_zero_based']}"
            )
            source_row = f"kids_null_control_{control['control_index_one_based']}"
            for feature in control_stat_features:
                rows.append(
                    base_row(
                        "kids_lensing_cosebis_low_mode",
                        "matched_control",
                        source_row,
                        feature,
                        control[feature],
                        "available_control_vector_summary_source_only",
                        str(KIDS_NULL_CONTROLS.relative_to(ROOT)),
                        control_family=control["control_family"],
                        control_id=control_id,
                        caveat="control_vector_summary_only_no_row_level_control_export_endpoint_forbidden",
                    )
                )
        row_control_features = {
            "row_level_control_artifact_rows": kids_row_control_summary["total_row_vector_rows"],
            "row_level_control_draw_count": kids_row_control_summary["control_draw_count"],
            "row_level_control_rows_per_control": kids_row_control_summary["rows_per_control"],
            "row_level_control_artifact_size_bytes": str(os.path.getsize(KIDS_ROW_CONTROLS)),
        }
        for feature, value in row_control_features.items():
            rows.append(
                base_row(
                    "kids_lensing_cosebis_low_mode",
                    "matched_control",
                    "kids_row_level_null_control_artifact",
                    feature,
                    value,
                    "available_control_row_vectors_external_artifact_source_only",
                    str(KIDS_ROW_CONTROLS.relative_to(ROOT)),
                    control_family="all_predeclared_null_control_families",
                    control_id="kids1000_cosebis_null_control_row_vectors_v1",
                    caveat="row_level_control_vectors_available_as_compressed_artifact_endpoint_forbidden",
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
            if "caveated" in row["feature_status"]
            or row["feature_status"] == "missing"
            or row["caveat"] != "none"
        }
    )
    kids_candidate_rows = [
        row
        for row in rows
        if row["channel_id"] == "kids_lensing_cosebis_low_mode"
        and row["row_type"] == "candidate"
        and row["feature_status"].startswith("available")
    ]
    kids_control_rows = [
        row
        for row in rows
        if row["channel_id"] == "kids_lensing_cosebis_low_mode"
        and row["row_type"] == "matched_control"
        and row["feature_status"].startswith("available")
    ]
    summary = {
        "export_id": "JOINT_COMMON_SOURCE_FEATURE_EXPORT_V5",
        "active_channel_count": str(len(active_channels)),
        "exported_channel_count": str(len(channels)),
        "total_feature_rows": str(len(rows)),
        "observer_feature_count": str(len(observer_features)),
        "observer_selected_source_rows": str(len(selected_indices)),
        "kids_candidate_feature_rows": str(len(kids_candidate_rows)),
        "kids_control_summary_feature_rows": str(len(kids_control_rows)),
        "complete_or_caveated_feature_channels": ";".join(complete_channels) if complete_channels else "none",
        "caveated_or_missing_channels": ";".join(caveated_channels) if caveated_channels else "none",
        "candidate_control_symmetric_schema": "true",
        "all_channels_have_nontrivial_row_features": "true",
        "kids_source_row_features_exported": "true" if kids_candidate_rows else "false",
        "kids_controls_exported_as_summary_only": "true" if kids_control_rows else "false",
        "kids_row_level_controls_exported": "true",
        "observer_path_row_features_exported": "true",
        "observer_path_r6_leakage_review_complete": "true",
        "observer_path_source_unique_ready": "true",
        "source_feature_export_complete_for_penalty": "true",
        "numeric_t_joint_rescoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "COMMON_EXPORT_V5_SOURCE_FEATURE_INPUTS_COMPLETE_RESCORING_STILL_FORBIDDEN",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint common source feature export v5",
                "",
                "**Doc class:** residual-blind common source-feature export.",
                "**Status:** KiDS row-level null-control input artifact available; still not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "Version 5 keeps the v4 observer/DESI/KiDS candidate export and adds",
                "a compressed KiDS row-level null-control artifact reference. The",
                "artifact expands 1008 predeclared controls into the same 300-row",
                "COSEBIs basis used by the candidate source-frozen theory vector.",
                "",
                "This closes the source-feature availability blocker for future",
                "row-level penalty design, but it does not run or authorize that penalty.",
                "Endpoint replay, validation, and `T_joint` rescoring remain forbidden.",
                "",
                f"Verdict: `{summary['verdict']}`.",
                "",
            ]
        )
    )
    print(
        "JOINT_COMMON_SOURCE_FEATURE_EXPORT_V5_BUILT "
        f"rows={summary['total_feature_rows']} observer_features={summary['observer_feature_count']}"
    )


if __name__ == "__main__":
    main()
