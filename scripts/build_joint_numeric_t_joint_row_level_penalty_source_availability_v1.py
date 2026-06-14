#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBSERVER_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv"
OBSERVER_GRID = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_grid.csv"
DESI_SUMMARY = ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv"
DESI_GRID = ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_grid.csv"
SYMMETRY = ROOT / "data/derived/joint_numeric_t_joint_channel_penalty_symmetry_gate_v1_summary.csv"
OUT = ROOT / "data/derived/joint_numeric_t_joint_row_level_penalty_source_availability_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_row_level_penalty_source_availability_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_row_level_penalty_source_availability_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_row_level_penalty_source_availability_not_scoring_not_validation"


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


def vector_len(value: str) -> int:
    if not value or value == "not_applicable":
        return 0
    return len([part for part in value.split(";") if part])


def main() -> None:
    observer = read_one(OBSERVER_SUMMARY)
    desi = read_one(DESI_SUMMARY)
    symmetry = read_one(SYMMETRY)
    observer_grid_cols = set(read_rows(OBSERVER_GRID)[0])
    desi_grid_rows = read_rows(DESI_GRID)
    desi_grid_cols = set(desi_grid_rows[0])

    if symmetry["nontrivial_row_level_penalty_available"] != "false":
        raise SystemExit("availability audit expects current penalty to remain unavailable")

    observer_row_count = vector_len(observer["source_row_indices"])
    desi_shape_rows = int(desi["n_shape_rows"])
    desi_candidate = next(row for row in desi_grid_rows if row["control_family"] == "candidate")
    desi_vector_len = vector_len(desi_candidate["shape_vector"])

    checks = [
        {
            "audit_id": "JOINT_NUMERIC_T_JOINT_ROW_LEVEL_PENALTY_SOURCE_AVAILABILITY_V1",
            "check_id": "RPA_C1_OBSERVER_SOURCE_ROWS_PRESENT",
            "status": "SATISFIED" if observer_row_count > 0 else "OPEN",
            "evidence": f"observer_source_row_count={observer_row_count}; active_family={observer['active_family']}",
            "interpretation": "observer-path route has a frozen source row scope, but not a per-row exported source feature vector in this artifact",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "JOINT_NUMERIC_T_JOINT_ROW_LEVEL_PENALTY_SOURCE_AVAILABILITY_V1",
            "check_id": "RPA_C2_DESI_SHAPE_VECTOR_PRESENT",
            "status": "SATISFIED" if desi_vector_len == desi_shape_rows else "OPEN",
            "evidence": f"desi_shape_rows={desi_shape_rows}; desi_candidate_shape_vector_len={desi_vector_len}",
            "interpretation": "DESI route has a source-native shape vector for its local route scope",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "JOINT_NUMERIC_T_JOINT_ROW_LEVEL_PENALTY_SOURCE_AVAILABILITY_V1",
            "check_id": "RPA_C3_SHARED_ROW_SPACE",
            "status": "OPEN",
            "evidence": f"observer_rows={observer_row_count}; desi_shape_rows={desi_shape_rows}; row_spaces=supernova_low_z_vs_desi_bao_shape",
            "interpretation": "the two source routes do not currently expose a common row-indexed feature space, so a cross-channel row-level penalty would be artificial",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "JOINT_NUMERIC_T_JOINT_ROW_LEVEL_PENALTY_SOURCE_AVAILABILITY_V1",
            "check_id": "RPA_C4_CANDIDATE_CONTROL_FEATURE_EXPORT",
            "status": "OPEN_CAVEATED",
            "evidence": "observer_grid_has_no_source_feature_vector_column="
            + str("source_feature_vector" not in observer_grid_cols).lower()
            + "; desi_grid_has_shape_vector="
            + str("shape_vector" in desi_grid_cols).lower(),
            "interpretation": "candidate/control symmetric per-row feature export is incomplete across the two routes",
            "numeric_t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    satisfied = sum(row["status"] == "SATISFIED" for row in checks)
    open_count = len(checks) - satisfied
    summary = {
        "audit_id": "JOINT_NUMERIC_T_JOINT_ROW_LEVEL_PENALTY_SOURCE_AVAILABILITY_V1",
        "checks_total": str(len(checks)),
        "checks_satisfied": str(satisfied),
        "checks_open_or_caveated": str(open_count),
        "observer_source_row_count": str(observer_row_count),
        "desi_shape_rows": str(desi_shape_rows),
        "desi_candidate_shape_vector_len": str(desi_vector_len),
        "shared_row_space_available": "false",
        "candidate_control_symmetric_feature_export_complete": "false",
        "nontrivial_row_level_penalty_available": "false",
        "numeric_t_joint_rescoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "ROW_LEVEL_SOURCE_FEATURES_INCOMPLETE_NO_PENALTY",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(OUT, checks)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint row-level penalty source availability v1",
                "",
                "**Doc class:** source-side availability audit.",
                "**Status:** no row-level penalty; not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This audit asks whether the observer-path and DESI shape/time routes",
                "currently expose enough frozen, residual-blind source-side structure",
                "to define a nontrivial row-level channel-distinguishability penalty.",
                "",
                "Result: the observer-path route has a frozen source row scope and the",
                "DESI route has a local shape vector, but the two routes do not expose",
                "a common row-indexed feature space. Candidate/control-symmetric",
                "per-row feature export is incomplete. A cross-channel row-level penalty",
                "would therefore be artificial at this stage.",
                "",
                f"Verdict: `{summary['verdict']}`.",
                "",
            ]
        )
    )
    print(
        "JOINT_NUMERIC_T_JOINT_ROW_LEVEL_PENALTY_SOURCE_AVAILABILITY_V1_BUILT "
        f"open={summary['checks_open_or_caveated']}"
    )


if __name__ == "__main__":
    main()
