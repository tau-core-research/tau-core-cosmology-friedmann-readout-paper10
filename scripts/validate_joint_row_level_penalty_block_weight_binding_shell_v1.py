#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_penalty_block_weight_binding_shell_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_penalty_block_weight_binding_shell_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_penalty_block_weight_binding_shell_v1.md"
CLAIM_BOUNDARY = "joint_row_level_penalty_block_weight_binding_shell_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary_rows = read_rows(SUMMARY)
    require(len(rows) == 3, "expected exactly three channel binding rows")
    require(len(summary_rows) == 1, "summary must contain exactly one row")
    summary = summary_rows[0]

    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["candidate_control_symmetric_transform_built"] == "true", "transform should be built")
    require(summary["binding_frozen_for_future_penalty_design"] == "true", "binding should be frozen")
    require(summary["block_weight_policy"] == "equal_channel_preweight_shell_only", "unexpected block-weight policy")
    require(summary["penalty_formula_defined"] == "false", "penalty formula must remain undefined")
    require(summary["penalty_computed"] == "false", "penalty must not be computed")
    require(summary["numeric_t_joint_rescoring_allowed"] == "false", "rescoring must remain forbidden")
    require(summary["endpoint_replay_allowed"] == "false", "endpoint replay must remain forbidden")
    require(summary["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
    require(summary["verdict"] == "BLOCK_WEIGHT_BINDING_SHELL_FROZEN_NOT_SCORING", "unexpected verdict")

    channels = set()
    for row in rows:
        channels.add(row["channel_id"])
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["binding_frozen_for_future_penalty_design"] == "true", "row binding should be frozen")
        require(row["future_row_penalty_block_weight_policy"] == "equal_channel_preweight_shell_only", "row policy mismatch")
        require(row["candidate_control_same_transform_required"] == "true", "candidate/control transform symmetry required")
        require(row["candidate_control_same_block_weight_required"] == "true", "candidate/control block-weight symmetry required")
        require(row["candidate_control_same_covariance_required"] == "true", "candidate/control covariance symmetry required")
        require(row["penalty_formula_defined"] == "false", "row penalty formula must remain undefined")
        require(row["penalty_computed"] == "false", "row penalty must not be computed")
        require(row["numeric_t_joint_rescoring_allowed"] == "false", "row rescoring must remain forbidden")
        require(row["endpoint_replay_allowed"] == "false", "row endpoint replay must remain forbidden")
        require(row["endpoint_validation_claimed"] == "false", "row endpoint validation must remain false")
        require(int(row["candidate_rows_in_transform"]) > 0, "candidate rows must be present")
        require(int(row["matched_control_rows_in_transform"]) > 0, "matched-control rows must be present")

    require(
        channels == {
            "desi_shape_time_readout",
            "kids_lensing_cosebis_low_mode",
            "observer_path_basis_low_z",
        },
        f"unexpected channels: {sorted(channels)}",
    )

    text = DOC.read_text()
    for marker in [
        CLAIM_BOUNDARY,
        "penalty not defined",
        "does not modify",
        "separate authorization gate",
    ]:
        require(marker in text, f"doc missing marker: {marker}")

    print(
        "JOINT_ROW_LEVEL_PENALTY_BLOCK_WEIGHT_BINDING_SHELL_V1_VALIDATED "
        f"channels={len(channels)}"
    )


if __name__ == "__main__":
    main()
