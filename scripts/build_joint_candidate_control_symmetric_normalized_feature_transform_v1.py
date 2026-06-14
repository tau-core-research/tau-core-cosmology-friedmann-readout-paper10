#!/usr/bin/env python3
from __future__ import annotations

import csv
import gzip
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMON_EXPORT = ROOT / "data/derived/joint_common_source_feature_export_v5.csv"
NORMALIZATION = ROOT / "data/derived/joint_channel_local_source_normalization_rule_v1.csv"
NORMALIZATION_SUMMARY = ROOT / "data/derived/joint_channel_local_source_normalization_rule_v1_summary.csv"
KIDS_ROW_CONTROLS = ROOT / "data/derived/kids1000_cosebis_null_control_row_vectors_v1.csv.gz"
OUT = ROOT / "data/derived/joint_candidate_control_symmetric_normalized_feature_transform_v1.csv.gz"
SUMMARY = ROOT / "data/derived/joint_candidate_control_symmetric_normalized_feature_transform_v1_summary.csv"
DOC = ROOT / "docs/joint_candidate_control_symmetric_normalized_feature_transform_v1.md"
CLAIM_BOUNDARY = "joint_candidate_control_symmetric_normalized_feature_transform_not_scoring_not_validation"

EXCLUDED_FEATURE_PREFIXES = ("row_level_control_", "vector_")
EXCLUDED_FEATURE_NAMES = {"unique_value_count_rounded"}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one row")
    return rows[0]


def parse_float(value: str) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def is_normalizable_feature(feature_name: str, value: str) -> bool:
    if feature_name in EXCLUDED_FEATURE_NAMES:
        return False
    if feature_name.startswith(EXCLUDED_FEATURE_PREFIXES):
        return False
    return parse_float(value) is not None


def write_csv_gz(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    normalization_summary = read_one(NORMALIZATION_SUMMARY)
    if normalization_summary["source_only_normalization_frozen"] != "true":
        raise SystemExit("channel-local normalization must be frozen before transform")
    if normalization_summary["normalization_applied_to_scoring"] != "false":
        raise SystemExit("normalization must not have been applied to scoring")
    if normalization_summary["numeric_t_joint_rescoring_allowed"] != "false":
        raise SystemExit("normalization must not authorize rescoring")

    scales = {}
    for row in read_rows(NORMALIZATION):
        if row["uses_endpoint_scores_or_residuals"] != "false":
            raise SystemExit("normalization rows must be source-only")
        scale = float(row["normalization_scale"])
        if scale <= 0:
            raise SystemExit(f"invalid scale for {row['channel_id']}")
        scales[row["channel_id"]] = scale

    rows_out: list[dict[str, str]] = []
    excluded = 0

    def append_row(
        channel_id: str,
        row_type: str,
        source_row_id: str,
        feature_name: str,
        raw_value: float,
        source_artifact: str,
        control_family: str = "not_applicable",
        control_id: str = "not_applicable",
    ) -> None:
        scale = scales[channel_id]
        rows_out.append(
            {
                "transform_id": "JOINT_CANDIDATE_CONTROL_SYMMETRIC_NORMALIZED_FEATURE_TRANSFORM_V1",
                "channel_id": channel_id,
                "row_type": row_type,
                "control_family": control_family,
                "control_id": control_id,
                "source_row_id": source_row_id,
                "feature_name": feature_name,
                "raw_feature_value": f"{raw_value:.12e}",
                "normalization_scale": f"{scale:.12e}",
                "normalized_feature_value": f"{raw_value / scale:.12e}",
                "normalization_rule": "divide_by_channel_local_max_abs_source_feature",
                "uses_endpoint_scores_or_residuals": "false",
                "penalty_formula_defined": "false",
                "penalty_computed": "false",
                "numeric_t_joint_rescoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "source_artifact": source_artifact,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for row in read_rows(COMMON_EXPORT):
        channel_id = row["channel_id"]
        if channel_id not in scales:
            raise SystemExit(f"missing normalization scale for {channel_id}")
        if row["uses_endpoint_scores_or_residuals"] != "false":
            raise SystemExit("common export rows must be residual-free")
        feature_name = row["feature_name"]
        value = row["feature_value"]
        if not is_normalizable_feature(feature_name, value):
            excluded += 1
            continue
        append_row(
            channel_id,
            row["row_type"],
            row["source_row_id"],
            feature_name,
            float(value),
            row["source_artifact"],
            row["control_family"],
            row["control_id"],
        )

    for row in read_rows(KIDS_ROW_CONTROLS):
        if row["uses_kids_data_vector_values"] != "false" or row["contains_residual"] != "false":
            raise SystemExit("KiDS row-control transform input must be residual-free")
        append_row(
            "kids_lensing_cosebis_low_mode",
            "matched_control",
            f"kids_cosebis_pair_{row['pair_id']}_mode_{row['mode']}",
            "control_theory_value",
            float(row["control_theory_value"]),
            str(KIDS_ROW_CONTROLS.relative_to(ROOT)),
            row["control_family"],
            f"{row['control_family']}:{row['operator']}:{row['control_draw_index_zero_based']}",
        )

    write_csv_gz(OUT, rows_out)
    row_type_counts = {}
    for row in rows_out:
        key = f"{row['channel_id']}:{row['row_type']}"
        row_type_counts[key] = row_type_counts.get(key, 0) + 1

    summary = {
        "transform_id": "JOINT_CANDIDATE_CONTROL_SYMMETRIC_NORMALIZED_FEATURE_TRANSFORM_V1",
        "normalized_feature_rows": str(len(rows_out)),
        "channels": ";".join(sorted(scales)),
        "row_type_counts": ";".join(f"{key}={value}" for key, value in sorted(row_type_counts.items())),
        "excluded_non_numeric_or_metadata_features": str(excluded),
        "normalization_rule": "divide_by_channel_local_max_abs_source_feature",
        "candidate_control_symmetric_transform_built": "true",
        "penalty_formula_defined": "false",
        "penalty_computed": "false",
        "numeric_t_joint_rescoring_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "NORMALIZED_FEATURE_TRANSFORM_BUILT_NOT_SCORING",
        "next_required_action": "bind_transform_to_covariance_or_block_weight_shell_before_any_penalty_formula",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)

    DOC.write_text(
        "\n".join(
            [
                "# Joint candidate/control symmetric normalized feature transform v1",
                "",
                "**Doc class:** source-only normalized feature transform.",
                "**Status:** transform built; penalty not defined; not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This artifact applies the frozen channel-local normalization rule to",
                "candidate and matched-control source features using the same transform.",
                "It includes the compressed KiDS row-level null-control vectors in the",
                "same normalized feature basis as the KiDS candidate rows.",
                "",
                "The transform uses no endpoint scores, residuals, fit statistics, or",
                "posterior chains. It does not define or compute a penalty and does not",
                "permit `T_joint` rescoring.",
                "",
                f"Rows: `{summary['normalized_feature_rows']}`.",
                f"Verdict: `{summary['verdict']}`.",
                f"Next action: `{summary['next_required_action']}`.",
                "",
            ]
        )
    )
    print(
        "JOINT_CANDIDATE_CONTROL_SYMMETRIC_NORMALIZED_FEATURE_TRANSFORM_V1_BUILT "
        f"rows={summary['normalized_feature_rows']}"
    )


if __name__ == "__main__":
    main()
