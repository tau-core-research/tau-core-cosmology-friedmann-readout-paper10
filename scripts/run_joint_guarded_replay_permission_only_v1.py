#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "data/derived/joint_guarded_replay_execution_authorization_response_v1_summary.csv"
PLAN = ROOT / "data/source_manifest/joint_guarded_replay_execution_plan_v1.csv"
OUT = ROOT / "data/derived/joint_guarded_replay_permission_only_grid_v1.csv"
SUMMARY = ROOT / "data/derived/joint_guarded_replay_permission_only_summary_v1.csv"
DOC = ROOT / "docs/joint_guarded_replay_permission_only_v1.md"
KIDS = ROOT / "data/derived/kids1000_cosebis_authorized_endpoint_replay_v1_summary.csv"
OBSERVER = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv"
DESI = ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv"
CLAIM_BOUNDARY = "joint_guarded_replay_permission_only_not_validation"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
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


def require_false(row: dict[str, str], fields: list[str], label: str) -> None:
    for field in fields:
        if row.get(field) != "false":
            raise SystemExit(f"{label}: unsafe field {field}")


def main() -> None:
    auth = read_one(AUTH)
    plan = read_one(PLAN)
    if auth["decision"] != "AUTHORIZE_JOINT_GUARDED_REPLAY_PERMISSION_ONLY_EXECUTION_NOT_VALIDATION":
        raise SystemExit("joint guarded replay execution is not authorized")
    if auth["permission_only_execution_allowed"] != "true":
        raise SystemExit("permission-only execution flag is not true")
    require_false(
        auth,
        ["endpoint_validation_claimed", "cosmological_validation_claimed", "physical_validation_claimed"],
        "authorization",
    )
    if plan["status"] != "JOINT_GUARDED_REPLAY_EXECUTION_PLAN_READY_NOT_RUN":
        raise SystemExit("execution plan is not frozen in ready-not-run state")
    for field in ["endpoint_scoring_allowed", "endpoint_validation_claimed", "cosmological_validation_claimed"]:
        if plan[field] != "false":
            raise SystemExit(f"execution plan unsafe field {field}")

    kids = read_one(KIDS)
    observer = read_one(OBSERVER)
    desi = read_one(DESI)
    blocks = [
        {
            "block_id": "kids_lensing_cosebis_low_mode",
            "source_summary": str(KIDS.relative_to(ROOT)),
            "candidate_support": kids["candidate_delta_chi2_vs_baseline"],
            "control_margin": kids["plus_one_tail_fraction_chi2"],
            "survives_controls": "caveated",
            "orientation": "negative_delta_chi2_and_low_tail_support",
        },
        {
            "block_id": "observer_path_basis_low_z",
            "source_summary": str(OBSERVER.relative_to(ROOT)),
            "candidate_support": observer["delta_chi2_candidate_minus_baseline"],
            "control_margin": observer["delta_chi2_candidate_minus_best_control"],
            "survives_controls": observer["family_survives_controls"],
            "orientation": "negative_delta_chi2_and_candidate_beats_best_control",
        },
        {
            "block_id": "desi_shape_time_readout",
            "source_summary": str(DESI.relative_to(ROOT)),
            "candidate_support": desi["candidate_shape_quadratic_score"],
            "control_margin": desi["delta_candidate_minus_best_control_score"],
            "survives_controls": desi["family_survives_controls"],
            "orientation": "higher_source_native_shape_score_and_candidate_exceeds_controls",
        },
    ]
    write_csv(OUT, blocks)
    positive = sum(1 for row in blocks if row["survives_controls"] in {"true", "caveated"})
    summary = {
        "run_id": "JOINT_GUARDED_REPLAY_PERMISSION_ONLY_V1",
        "status": "JOINT_GUARDED_REPLAY_PERMISSION_ONLY_COMPLETE_NOT_VALIDATION",
        "active_block_count": str(len(blocks)),
        "positive_or_caveated_support_blocks": str(positive),
        "candidate_control_same_statistic_required": "true",
        "candidate_control_same_covariance_required": "true",
        "block_diagonal_independence_caveated": "true",
        "permission_only_execution_allowed": "true",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "joint_guarded_replay_permission_only_executed_not_validation",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint guarded replay permission-only v1",
                "",
                "This artifact records a permission-only guarded replay, not endpoint validation",
                "and not cosmological validation.",
                "",
                "The replay is allowed only when the separate execution authorization response",
                "is imported and validates `permission_only_execution_allowed=true`.",
                "",
                f"Claim boundary: `{CLAIM_BOUNDARY}`.",
                "",
            ]
        )
    )
    print("JOINT_GUARDED_REPLAY_PERMISSION_ONLY_V1_COMPLETE not_validation=true")


if __name__ == "__main__":
    main()
