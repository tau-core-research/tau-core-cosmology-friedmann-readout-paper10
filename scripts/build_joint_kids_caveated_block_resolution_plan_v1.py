#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPLAY_GRID = ROOT / "data/derived/joint_guarded_replay_permission_only_grid_v1.csv"
PROMOTION_SUMMARY = ROOT / "data/derived/joint_permission_replay_promotion_readiness_gate_v1_summary.csv"
KIDS_REPLAY_SUMMARY = ROOT / "data/derived/kids1000_cosebis_authorized_endpoint_replay_v1_summary.csv"
KIDS_PHYSICAL_LEDGER = ROOT / "data/derived/kids1000_cosebis_physical_promotion_blocker_ledger_v1.csv"
KIDS_DEP_ORDER = ROOT / "data/derived/kids1000_cosebis_physical_promotion_dependency_order_v1.csv"
OUT = ROOT / "data/derived/joint_kids_caveated_block_resolution_plan_v1.csv"
SUMMARY = ROOT / "data/derived/joint_kids_caveated_block_resolution_plan_v1_summary.csv"
DOC = ROOT / "docs/joint_kids_caveated_block_resolution_plan_v1.md"
CLAIM_BOUNDARY = "joint_kids_caveated_block_resolution_plan_not_validation"


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
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    grid = read_rows(REPLAY_GRID)
    promotion = read_one(PROMOTION_SUMMARY)
    kids_replay = read_one(KIDS_REPLAY_SUMMARY)
    ledger_rows = read_rows(KIDS_PHYSICAL_LEDGER)
    dep_rows = read_rows(KIDS_DEP_ORDER)

    kids_block = [row for row in grid if row["block_id"] == "kids_lensing_cosebis_low_mode"]
    if len(kids_block) != 1:
        raise SystemExit("missing unique KiDS caveated block in joint grid")
    if kids_block[0]["survives_controls"] != "caveated":
        raise SystemExit("KiDS block is not currently caveated")
    if promotion["verdict"] != "JOINT_PERMISSION_REPLAY_POSITIVE_BUT_PROMOTION_BLOCKED_NOT_VALIDATION":
        raise SystemExit("promotion gate must be positive-but-blocked")
    if kids_replay["verdict"] != "authorized_endpoint_replay_low_tail_signal_not_validation":
        raise SystemExit("unexpected KiDS replay verdict")

    open_ledger = {
        row["blocker_id"]: row for row in ledger_rows if row["status"] == "OPEN_BLOCKER"
    }
    if len(open_ledger) != 5:
        raise SystemExit(f"expected five open KiDS blockers, found {len(open_ledger)}")

    rows: list[dict[str, str]] = []
    for dep in dep_rows:
        blocker_id = dep["blocker_id"]
        if blocker_id not in open_ledger:
            raise SystemExit(f"dependency order references missing open blocker: {blocker_id}")
        ledger = open_ledger[blocker_id]
        rows.append(
            {
                "plan_id": "JOINT_KIDS_CAVEATED_BLOCK_RESOLUTION_PLAN_V1",
                "joint_block_id": "kids_lensing_cosebis_low_mode",
                "resolution_rank": dep["dependency_rank"],
                "blocker_id": blocker_id,
                "dependency_status": dep["dependency_status"],
                "minimum_exit_condition": dep["minimum_exit_condition"],
                "why_required_for_joint_promotion": ledger["promotion_implication"],
                "dimension_check": ledger["dimension_check"],
                "known_limit_check": ledger["known_limit_check"],
                "source_artifact": ledger["source_artifact"],
                "computes_new_scores": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    write_csv(OUT, rows)
    summary = {
        "plan_id": "JOINT_KIDS_CAVEATED_BLOCK_RESOLUTION_PLAN_V1",
        "joint_block_id": "kids_lensing_cosebis_low_mode",
        "current_joint_block_status": kids_block[0]["survives_controls"],
        "candidate_delta_chi2_vs_baseline": kids_replay["candidate_delta_chi2_vs_baseline"],
        "plus_one_tail_fraction_chi2": kids_replay["plus_one_tail_fraction_chi2"],
        "open_resolution_steps": str(len(rows)),
        "next_primary_proof_gate": rows[0]["blocker_id"],
        "next_parallel_proof_gate": rows[1]["blocker_id"],
        "can_promote_kids_block_to_clean_joint_support": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "KIDS_JOINT_BLOCK_HAS_SIGNAL_BUT_CAVEAT_RESOLUTION_REQUIRES_PHYSICAL_PROMOTION_PROOFS",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# Joint KiDS caveated-block resolution plan v1",
                "",
                "**Doc class:** post-replay blocker-resolution plan",
                "**Status:** not scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "The joint guarded replay keeps the KiDS/COSEBIs low-mode block as a",
                "caveated support block. The reason is not lack of a numerical low-tail",
                "signal; the blocker is physical promotion. This plan freezes the proof",
                "order required before the KiDS block can be promoted from caveated",
                "support to clean joint support.",
                "",
                "Frozen proof order:",
                "",
                "1. operator leakage theorem",
                "2. gauge quotient descent",
                "3. response unit normalization",
                "4. standard-lensing null-amplitude theorem",
                "5. survey-native operator theorem",
                "",
                "Summary:",
                "",
                f"- KiDS block status: `{summary['current_joint_block_status']}`",
                f"- candidate delta chi2: `{summary['candidate_delta_chi2_vs_baseline']}`",
                f"- tail fraction: `{summary['plus_one_tail_fraction_chi2']}`",
                f"- open resolution steps: `{summary['open_resolution_steps']}`",
                f"- next primary proof gate: `{summary['next_primary_proof_gate']}`",
                f"- next parallel proof gate: `{summary['next_parallel_proof_gate']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: the KiDS block can motivate further work, but it cannot",
                "be used as clean validation support until the physical-promotion proof",
                "chain is closed without endpoint leakage.",
                "",
            ]
        )
    )
    print(
        "JOINT_KIDS_CAVEATED_BLOCK_RESOLUTION_PLAN_V1_BUILT "
        f"steps={summary['open_resolution_steps']} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
