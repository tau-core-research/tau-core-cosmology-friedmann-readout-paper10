#!/usr/bin/env python3
from __future__ import annotations

import csv
import gzip
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMON_EXPORT = ROOT / "data/derived/joint_common_source_feature_export_v5.csv"
COMMON_SUMMARY = ROOT / "data/derived/joint_common_source_feature_export_v5_summary.csv"
KIDS_ROW_CONTROLS = ROOT / "data/derived/kids1000_cosebis_null_control_row_vectors_v1.csv.gz"
OUT = ROOT / "data/derived/joint_channel_local_source_normalization_rule_v1.csv"
SUMMARY = ROOT / "data/derived/joint_channel_local_source_normalization_rule_v1_summary.csv"
DOC = ROOT / "docs/joint_channel_local_source_normalization_rule_v1.md"
CLAIM_BOUNDARY = "joint_channel_local_source_normalization_rule_not_scoring_not_validation"

EXCLUDED_FEATURE_PREFIXES = ("row_level_control_", "vector_")
EXCLUDED_FEATURE_NAMES = {
    "vector_row_count",
    "unique_value_count_rounded",
}


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


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_float(value: str) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def robust_stats(values: list[float]) -> dict[str, str]:
    if not values:
        raise SystemExit("cannot normalize an empty value list")
    abs_values = sorted(abs(value) for value in values)
    max_abs = max(abs_values)
    median_abs = abs_values[len(abs_values) // 2]
    nonzero_abs = [value for value in abs_values if value > 0]
    min_nonzero_abs = min(nonzero_abs) if nonzero_abs else 0.0
    scale = max_abs if max_abs > 0 else 1.0
    return {
        "source_feature_count": str(len(values)),
        "normalization_scale": f"{scale:.12e}",
        "max_abs_source_feature": f"{max_abs:.12e}",
        "median_abs_source_feature": f"{median_abs:.12e}",
        "min_nonzero_abs_source_feature": f"{min_nonzero_abs:.12e}",
    }


def main() -> None:
    common_summary = read_one(COMMON_SUMMARY)
    if common_summary["source_feature_export_complete_for_penalty"] != "true":
        raise SystemExit("source-feature export must be complete before normalization rule")
    if common_summary["numeric_t_joint_rescoring_allowed"] != "false":
        raise SystemExit("common export must not authorize rescoring")

    by_channel: dict[str, list[float]] = defaultdict(list)
    excluded_count = 0
    for row in read_rows(COMMON_EXPORT):
        if row["uses_endpoint_scores_or_residuals"] != "false":
            raise SystemExit("common source features must be residual blind")
        feature_name = row["feature_name"]
        if feature_name in EXCLUDED_FEATURE_NAMES or feature_name.startswith(EXCLUDED_FEATURE_PREFIXES):
            excluded_count += 1
            continue
        value = parse_float(row["feature_value"])
        if value is None:
            excluded_count += 1
            continue
        by_channel[row["channel_id"]].append(value)

    kids_values = []
    for row in read_rows(KIDS_ROW_CONTROLS):
        if row["uses_kids_data_vector_values"] != "false" or row["contains_residual"] != "false":
            raise SystemExit("KiDS row controls must be source-side and residual-free")
        value = parse_float(row["control_theory_value"])
        if value is not None:
            kids_values.append(value)
    by_channel["kids_lensing_cosebis_low_mode"].extend(kids_values)

    rows = []
    for channel_id in sorted(by_channel):
        stats = robust_stats(by_channel[channel_id])
        rows.append(
            {
                "normalization_id": "JOINT_CHANNEL_LOCAL_SOURCE_NORMALIZATION_RULE_V1",
                "channel_id": channel_id,
                "normalization_scope": "channel_local_source_features",
                "normalization_rule": "divide_by_max_abs_source_feature_with_unit_fallback",
                "normalization_status": "FROZEN_NOT_APPLIED_TO_SCORING",
                **stats,
                "excluded_non_numeric_or_metadata_features": str(excluded_count if channel_id == "all_channels" else 0),
                "uses_endpoint_scores_or_residuals": "false",
                "candidate_control_symmetric_transform_required_next": "true",
                "penalty_formula_defined": "false",
                "penalty_computed": "false",
                "numeric_t_joint_rescoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    summary = {
        "normalization_id": "JOINT_CHANNEL_LOCAL_SOURCE_NORMALIZATION_RULE_V1",
        "channel_count": str(len(rows)),
        "channels": ";".join(row["channel_id"] for row in rows),
        "normalization_rule": "divide_by_max_abs_source_feature_with_unit_fallback",
        "source_only_normalization_frozen": "true",
        "normalization_applied_to_scoring": "false",
        "candidate_control_symmetric_transform_built": "false",
        "penalty_formula_defined": "false",
        "penalty_computed": "false",
        "numeric_t_joint_rescoring_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "excluded_non_numeric_or_metadata_features_total": str(excluded_count),
        "verdict": "CHANNEL_LOCAL_SOURCE_NORMALIZATION_FROZEN_NOT_SCORING",
        "next_required_action": "build_candidate_control_symmetric_normalized_feature_transform_without_endpoint_fields",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint channel-local source normalization rule v1",
                "",
                "**Doc class:** source-only normalization rule.",
                "**Status:** normalization frozen; not applied to scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This artifact freezes the first channel-local normalization rule for",
                "future row-level penalty design. For each active channel, normalizable",
                "source features are scaled by the maximum absolute residual-blind",
                "source-feature value in that channel, with a unit fallback for an all-zero",
                "channel. Metadata features such as artifact size are excluded.",
                "",
                "The rule uses no endpoint scores, residuals, fit statistics, posterior",
                "chains, or post-hoc endpoint ordering. It does not compute a penalty and",
                "does not permit `T_joint` rescoring.",
                "",
                f"Verdict: `{summary['verdict']}`.",
                f"Next action: `{summary['next_required_action']}`.",
                "",
            ]
        )
    )
    print(
        "JOINT_CHANNEL_LOCAL_SOURCE_NORMALIZATION_RULE_V1_BUILT "
        f"channels={summary['channel_count']}"
    )


if __name__ == "__main__":
    main()
