#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_best_tomographic_control_source_evidence_gate_policy_v1.csv"
HOLDOUT_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_holdout_replay_v1_summary.csv"
DISAMBIGUATION = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_control_disambiguation_v1.csv"
ROBUSTNESS_TOP = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_top_controls.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def parse_mapping(signature: str) -> dict[str, str]:
    return dict(item.split("->", 1) for item in signature.split(";"))


def pair_id(a: str, b: str) -> str:
    lo, hi = sorted((int(a), int(b)))
    return f"{lo}-{hi}"


def induced_source_bin_map(mapping: dict[str, str]) -> tuple[bool, str, str]:
    candidate: dict[str, str] = {}
    contradictions: list[str] = []
    for source_bin in ["1", "2", "3", "4", "5"]:
        target = mapping.get(f"{source_bin}-{source_bin}")
        if target is None:
            contradictions.append(f"missing_auto_{source_bin}-{source_bin}")
            continue
        left, right = target.split("-", 1)
        if left != right:
            contradictions.append(f"auto_{source_bin}-{source_bin}_maps_to_cross_{target}")
        candidate[source_bin] = left
    for source_pair, target_pair in mapping.items():
        left, right = source_pair.split("-", 1)
        expected = pair_id(candidate[left], candidate[right])
        if expected != target_pair:
            contradictions.append(f"{source_pair}_expected_{expected}_observed_{target_pair}")
    return len(contradictions) == 0, ";".join(f"{key}->{candidate[key]}" for key in sorted(candidate)), ";".join(contradictions)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = read_one(POLICY)
    holdout = read_one(HOLDOUT_SUMMARY)
    disamb_rows = read_rows(DISAMBIGUATION)
    top_rows = read_rows(ROBUSTNESS_TOP)
    require(policy["status"] == "BEST_TOMOGRAPHIC_CONTROL_SOURCE_EVIDENCE_GATE_FROZEN", "unexpected policy status")
    require(policy["computes_new_scores"] == "false", "gate must not compute new scores")
    require(policy["endpoint_validation_claimed"] == "false", "gate must not claim validation")
    require(holdout["status"] == "TOMOGRAPHIC_HOLDOUT_REPLAY_COMPLETE", "holdout replay must precede this gate")
    require(holdout["candidate_beating_control_count"] == "1", "this gate expects exactly one holdout-beating control")

    target_operator = holdout["best_branch"]
    disamb_by_operator = {row["operator"]: row for row in disamb_rows}
    top_by_operator = {row["operator"]: row for row in top_rows}
    require(target_operator in disamb_by_operator, "best holdout control missing from disambiguation ledger")
    require(target_operator in top_by_operator, "best holdout control missing from top robustness controls")
    disamb = disamb_by_operator[target_operator]
    top = top_by_operator[target_operator]
    mapping = parse_mapping(top["mapping_signature"])
    global_relabel, source_bin_map, contradictions = induced_source_bin_map(mapping)
    independent_evidence_attached = "false"
    accepted_physical = "false"
    source_systematic_candidate = "true" if global_relabel else "false"
    required_next_action = (
        "attach_independent_photoz_tomographic_evidence_before_source_systematic_promotion"
        if global_relabel
        else "retain_as_control_only_auto_cross_pair_shuffle"
    )
    status = "CONTROL_ONLY_NO_SOURCE_EVIDENCE_FOR_PHYSICAL_PROMOTION"
    row = {
        "policy_id": policy["policy_id"],
        "target_operator": target_operator,
        "target_control_family": disamb["control_family"],
        "holdout_rank": holdout["candidate_rank_by_total_holdout_delta_chi2"],
        "target_total_holdout_delta_chi2_vs_zero": holdout["best_branch_total_holdout_delta_chi2_vs_zero"],
        "candidate_total_holdout_delta_chi2_vs_zero": holdout["candidate_total_holdout_delta_chi2_vs_zero"],
        "preexisting_disambiguation_status": disamb["physical_alternative_status"],
        "mapping_signature": top["mapping_signature"],
        "is_global_source_bin_relabel": str(global_relabel).lower(),
        "induced_source_bin_map": source_bin_map,
        "global_relabel_contradictions": contradictions,
        "independent_photoz_tomographic_evidence_attached": independent_evidence_attached,
        "source_systematic_candidate_after_gate": source_systematic_candidate,
        "accepted_as_physical_alternative": accepted_physical,
        "required_next_action": required_next_action,
        "computes_new_scores": "false",
        "uses_endpoint_residual_shape_for_source_evidence": "false",
        "endpoint_validation_claimed": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    summary = {
        "policy_id": policy["policy_id"],
        "status": status,
        "target_operator": target_operator,
        "target_control_family": disamb["control_family"],
        "target_is_global_source_bin_relabel": str(global_relabel).lower(),
        "target_has_independent_source_evidence": independent_evidence_attached,
        "accepted_physical_alternative_count": "1" if accepted_physical == "true" else "0",
        "source_systematic_candidate_count": "1" if source_systematic_candidate == "true" else "0",
        "control_only_count": "0" if source_systematic_candidate == "true" else "1",
        "best_control_refutes_endpoint_signal": "false",
        "best_control_blocks_validation": "true",
        "computes_new_scores": "false",
        "uses_endpoint_residual_shape_for_source_evidence": "false",
        "endpoint_validation_claimed": "false",
        "verdict": "best_holdout_control_is_control_only_not_physical_alternative",
        "claim_boundary": policy["claim_boundary"],
    }
    write_csv(OUT, [row])
    write_csv(SUMMARY, [summary])
    print(
        "PAPER10_KIDS1000_COSEBIS_BEST_TOMOGRAPHIC_CONTROL_SOURCE_EVIDENCE_GATE_V1_BUILT "
        f"target={target_operator} global_relabel={str(global_relabel).lower()} "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
