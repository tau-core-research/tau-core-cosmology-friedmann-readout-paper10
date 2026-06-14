#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBSERVER_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv"
OBSERVER_GRID = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_grid.csv"
DESI_GRID = ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_grid.csv"
ZI_SUMMARY = ROOT / "data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv"
OUT = ROOT / "data/derived/joint_common_source_feature_export_v1.csv"
SUMMARY = ROOT / "data/derived/joint_common_source_feature_export_v1_summary.csv"
DOC = ROOT / "docs/joint_common_source_feature_export_v1.md"
CLAIM_BOUNDARY = "joint_common_source_feature_export_not_scoring_not_validation"


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
) -> dict[str, str]:
    return {
        "export_id": "JOINT_COMMON_SOURCE_FEATURE_EXPORT_V1",
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
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    zi_summary_rows = read_rows(ZI_SUMMARY)
    active_channels = [row["channel_id"] for row in zi_summary_rows if row["channel_id"] != "all_channels"]
    rows: list[dict[str, str]] = []

    # Observer-path channel: source row membership is frozen, but no per-row
    # scalar feature vector is exported by the current observer replay artifact.
    observer = read_one(OBSERVER_SUMMARY)
    observer_indices = parts(observer["source_row_indices"])
    observer_cids = parts(observer["cids"])
    if len(observer_indices) != len(observer_cids):
        raise SystemExit("observer source row indices and cids have different lengths")
    observer_controls = sorted({row["branch"] for row in read_rows(OBSERVER_GRID) if row["branch"] not in {"candidate", "baseline_only"}})
    for idx, cid in zip(observer_indices, observer_cids, strict=True):
        source_row = f"pantheon_row_{idx}:{cid}"
        rows.append(
            base_row(
                "observer_path_basis_low_z",
                "candidate",
                source_row,
                "source_scope_membership",
                "1",
                "available_scope_only",
                str(OBSERVER_SUMMARY.relative_to(ROOT)),
            )
        )
        rows.append(
            base_row(
                "observer_path_basis_low_z",
                "candidate",
                source_row,
                "row_level_observer_feature_vector",
                "not_exported",
                "missing",
                str(OBSERVER_SUMMARY.relative_to(ROOT)),
            )
        )
        for control_family in observer_controls:
            rows.append(
                base_row(
                    "observer_path_basis_low_z",
                    "matched_control",
                    source_row,
                    "source_scope_membership",
                    "1",
                    "available_scope_only",
                    str(OBSERVER_GRID.relative_to(ROOT)),
                    control_family=control_family,
                    control_id=f"{control_family}_scope",
                )
            )

    # DESI shape/time channel: a source-native shape vector is available for
    # candidate and controls. Export it under the same schema.
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

    # KiDS is active in T_joint but no source-native row feature export has been
    # promoted into this common source-feature layer yet.
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
            )
        )

    channels = sorted({row["channel_id"] for row in rows})
    complete_channels = sorted(
        {
            channel
            for channel in channels
            if any(row["channel_id"] == channel and row["feature_status"] == "available" for row in rows)
            and not any(row["channel_id"] == channel and row["feature_status"] == "missing" for row in rows)
        }
    )
    missing_channels = sorted(
        {
            row["channel_id"]
            for row in rows
            if row["feature_status"] in {"missing", "available_scope_only"}
        }
    )
    summary = {
        "export_id": "JOINT_COMMON_SOURCE_FEATURE_EXPORT_V1",
        "active_channel_count": str(len(active_channels)),
        "exported_channel_count": str(len(channels)),
        "total_feature_rows": str(len(rows)),
        "complete_feature_channels": ";".join(complete_channels) if complete_channels else "none",
        "incomplete_or_scope_only_channels": ";".join(missing_channels) if missing_channels else "none",
        "candidate_control_symmetric_schema": "true",
        "all_channels_have_nontrivial_row_features": str(len(missing_channels) == 0).lower(),
        "source_feature_export_complete_for_penalty": "false",
        "numeric_t_joint_rescoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "COMMON_SCHEMA_BUILT_FEATURE_EXPORT_INCOMPLETE_NO_RESCORING",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint common source feature export v1",
                "",
                "**Doc class:** residual-blind common source-feature export.",
                "**Status:** common schema built; incomplete feature export; not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This artifact exports source-side information under one common schema",
                "for the active joint channels. It is candidate/control symmetric at",
                "the schema level and uses only frozen source artifacts.",
                "",
                "The DESI shape/time route exports a source-native shape vector for",
                "candidate and controls. The observer-path route currently exports",
                "only frozen source-scope membership and an explicit missing marker for",
                "a row-level observer feature vector. KiDS has not yet been promoted",
                "into this common feature layer.",
                "",
                f"Verdict: `{summary['verdict']}`.",
                "",
            ]
        )
    )
    print(
        "JOINT_COMMON_SOURCE_FEATURE_EXPORT_V1_BUILT "
        f"rows={summary['total_feature_rows']} complete={summary['source_feature_export_complete_for_penalty']}"
    )


if __name__ == "__main__":
    main()
