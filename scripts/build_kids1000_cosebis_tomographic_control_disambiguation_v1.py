#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_control_disambiguation_policy_v1.csv"
REPLAY_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_authorized_endpoint_replay_v1_summary.csv"
ROBUSTNESS_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_summary.csv"
ROBUSTNESS_TOP = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_top_controls.csv"
PLAUSIBILITY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_control_plausibility_audit_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_control_disambiguation_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_control_disambiguation_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def moved_bins(mapping_signature: str) -> str:
    bins: set[str] = set()
    for item in mapping_signature.split(";"):
        left, right = item.split("->", 1)
        if left != right:
            bins.update(left.split("-"))
            bins.update(right.split("-"))
    return ";".join(sorted(bins, key=int))


def changed_pair_count(mapping_signature: str) -> int:
    return sum(1 for item in mapping_signature.split(";") if item.split("->", 1)[0] != item.split("->", 1)[1])


def main() -> None:
    policy = read_one(POLICY)
    replay = read_one(REPLAY_SUMMARY)
    robustness = read_one(ROBUSTNESS_SUMMARY)
    top = read_rows(ROBUSTNESS_TOP)
    plausibility = read_rows(PLAUSIBILITY)
    plaus_by_op = {row["operator"]: row for row in plausibility}

    require(policy["status"] == "TOMOGRAPHIC_CONTROL_DISAMBIGUATION_POLICY_FROZEN", "unexpected policy status")
    require(policy["computes_new_scores"] == "false", "disambiguation policy must not compute new scores")
    require(policy["endpoint_validation_claimed"] == "false", "policy must not claim validation")
    require(replay["verdict"] == "authorized_endpoint_replay_low_tail_signal_not_validation", "authorized replay must precede disambiguation")
    require(robustness["endpoint_validation_claimed"] == "false", "robustness summary must not claim validation")

    better_top = [row for row in top if row["beats_candidate_chi2"] == "true"]
    rows: list[dict[str, str]] = []
    for rank, row in enumerate(better_top, start=1):
        plaus = plaus_by_op.get(row["operator"])
        require(plaus is not None, f"missing plausibility row for {row['operator']}")
        physical_status = plaus["physical_alternative_status"]
        if physical_status == "CONTROL_ONLY":
            action = "do_not_promote_as_physical_alternative"
            interpretation = "control_only_tomographic_relabel_or_pair_shuffle"
        elif physical_status == "CONDITIONAL_SOURCE_SYSTEMATIC":
            action = "requires_independent_photoz_or_tomographic_source_evidence_before_promotion"
            interpretation = "possible_source_systematic_candidate_not_physical_alternative_yet"
        else:
            action = "review_as_possible_physical_alternative"
            interpretation = "possible_physical_alternative"
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "run_id": row["run_id"],
                "disambiguation_rank": str(rank),
                "source_control_index_one_based": row["control_index_one_based"],
                "control_family": row["control_family"],
                "operator": row["operator"],
                "beats_candidate_chi2": row["beats_candidate_chi2"],
                "beats_candidate_aic": row["beats_candidate_aic"],
                "delta_chi2_vs_baseline": row["delta_chi2_vs_baseline"],
                "candidate_delta_chi2_vs_baseline": robustness["candidate_delta_chi2_vs_baseline"],
                "mapping_changed_pair_count": str(changed_pair_count(row["mapping_signature"])),
                "moved_source_bins": moved_bins(row["mapping_signature"]),
                "physical_alternative_status": physical_status,
                "disambiguation_interpretation": interpretation,
                "required_next_action": action,
                "accepted_as_physical_alternative": "true" if physical_status == "ACCEPTED_PHYSICAL_ALTERNATIVE" else "false",
                "blocks_validation": "true",
                "refutes_endpoint_signal": "false",
                "computes_new_scores": "false",
                "uses_kids_data_vector_values_for_source_selection": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    control_only = sum(row["physical_alternative_status"] == "CONTROL_ONLY" for row in rows)
    conditional_source = sum(row["physical_alternative_status"] == "CONDITIONAL_SOURCE_SYSTEMATIC" for row in rows)
    physical = sum(row["accepted_as_physical_alternative"] == "true" for row in rows)
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "TOMOGRAPHIC_CONTROL_DISAMBIGUATION_COMPLETE",
            "selected_statistic": policy["selected_statistic"],
            "authorized_replay_verdict": replay["verdict"],
            "candidate_rank_by_chi2": robustness["candidate_rank_by_chi2"],
            "candidate_delta_chi2_vs_baseline": robustness["candidate_delta_chi2_vs_baseline"],
            "better_tomographic_control_count": str(len(rows)),
            "better_control_only_count": str(control_only),
            "better_conditional_source_systematic_count": str(conditional_source),
            "accepted_physical_alternative_count": str(physical),
            "tomographic_controls_refute_endpoint_signal": "true" if physical > 0 else "false",
            "tomographic_controls_block_validation": "true",
            "recommended_next_action": "independent_photoz_or_tomographic_holdout_replay_before_promoting_any_tomographic_alternative",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "tomographic_controls_block_validation_but_do_not_refute_endpoint_signal",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_CONTROL_DISAMBIGUATION_V1_BUILT "
        f"better_controls={len(rows)} physical_alternatives={physical}"
    )


if __name__ == "__main__":
    main()
