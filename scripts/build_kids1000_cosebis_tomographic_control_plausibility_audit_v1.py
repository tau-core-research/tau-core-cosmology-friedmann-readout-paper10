#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_control_plausibility_audit_policy_v1.csv"
TOMO = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_summary.csv"
TOP = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_top_controls.csv"
ZINV = ROOT / "data" / "derived" / "kids1000_cosebis_redshift_kernel_inventory_v1.csv"

OUT = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_control_plausibility_audit_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_control_plausibility_audit_v1_summary.csv"

PAIRS = [f"{i}-{j}" for i in range(1, 6) for j in range(i, 6)]


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


def parse_mapping(signature: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in signature.split(";"):
        src, dst = part.split("->")
        out[src] = dst
    if set(out) != set(PAIRS) or any(dst not in PAIRS for dst in out.values()):
        raise SystemExit("invalid mapping signature")
    return out


def pair_bins(pair: str) -> tuple[int, int]:
    a, b = pair.split("-")
    return int(a), int(b)


def pair_mean_z(pair: str, zmean: dict[int, float]) -> float:
    a, b = pair_bins(pair)
    return 0.5 * (zmean[a] + zmean[b])


def pair_sep_z(pair: str, zmean: dict[int, float]) -> float:
    a, b = pair_bins(pair)
    return abs(zmean[a] - zmean[b])


def is_global_bin_permutation(mapping: dict[str, str], operator: str) -> tuple[bool, str]:
    if operator.startswith("bin_perm_"):
        perm = operator.removeprefix("bin_perm_")
        if sorted(perm) != ["1", "2", "3", "4", "5"]:
            raise SystemExit(f"invalid bin permutation operator: {operator}")
        return True, perm

    inferred: dict[int, int] = {}
    for src, dst in mapping.items():
        a, b = pair_bins(src)
        c, d = pair_bins(dst)
        for x, y in [(a, c), (b, d)]:
            if x in inferred and inferred[x] != y:
                return False, "none"
            inferred[x] = y
    if set(inferred) != {1, 2, 3, 4, 5} or set(inferred.values()) != {1, 2, 3, 4, 5}:
        return False, "none"
    expected = {src: "-".join(str(x) for x in sorted((inferred[pair_bins(src)[0]], inferred[pair_bins(src)[1]]))) for src in PAIRS}
    if expected != mapping:
        return False, "none"
    return True, "".join(str(inferred[i]) for i in range(1, 6))


def main() -> None:
    policy = read_one(POLICY)
    tomo = read_one(TOMO)
    top = read_rows(TOP)
    zrows = read_rows(ZINV)

    if policy["status"] != "TOMOGRAPHIC_CONTROL_PLAUSIBILITY_AUDIT_POLICY_FROZEN":
        raise SystemExit("unexpected plausibility audit policy status")
    if policy["computes_new_scores"] != "false":
        raise SystemExit("plausibility audit must not compute scores")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("plausibility audit must not claim validation")
    if tomo["status"] != "KIDS1000_COSEBIS_TOMOGRAPHIC_STRUCTURE_ROBUSTNESS_COMPLETE":
        raise SystemExit("tomographic robustness must be complete")
    if len(top) < int(policy["top_control_rows_audited"]):
        raise SystemExit("not enough top controls to audit")
    zmean = {int(row["source_bin"]): float(row["mean_z"]) for row in zrows}
    if set(zmean) != {1, 2, 3, 4, 5}:
        raise SystemExit("unexpected redshift-bin set")

    rows: list[dict[str, str]] = []
    for row in top[: int(policy["top_control_rows_audited"])]:
        mapping = parse_mapping(row["mapping_signature"])
        is_global, global_perm = is_global_bin_permutation(mapping, row["operator"])
        changed = sum(src != dst for src, dst in mapping.items())
        auto_to_auto = sum(pair_bins(src)[0] == pair_bins(src)[1] and pair_bins(dst)[0] == pair_bins(dst)[1] for src, dst in mapping.items())
        cross_to_cross = sum(pair_bins(src)[0] != pair_bins(src)[1] and pair_bins(dst)[0] != pair_bins(dst)[1] for src, dst in mapping.items())
        dz = [abs(pair_mean_z(src, zmean) - pair_mean_z(dst, zmean)) for src, dst in mapping.items()]
        dsep = [abs(pair_sep_z(src, zmean) - pair_sep_z(dst, zmean)) for src, dst in mapping.items()]
        mean_abs_dz = sum(dz) / len(dz)
        max_abs_dz = max(dz)
        mean_abs_dsep = sum(dsep) / len(dsep)

        if row["control_family"] == "bin_label_permutation" and is_global:
            if global_perm in {"13245", "21345", "12354"}:
                interpretation = "source_label_systematic_candidate_requires_independent_photoz_support"
                physical_alternative_status = "CONDITIONAL_SOURCE_SYSTEMATIC"
            else:
                interpretation = "global_bin_relabel_control_not_accepted_without_source_calibration_evidence"
                physical_alternative_status = "CONTROL_ONLY"
        elif row["control_family"] == "auto_cross_preserving_shuffle":
            interpretation = "non_global_pair_shuffle_preserves_pair_type_but_breaks_source_order_geometry"
            physical_alternative_status = "CONTROL_ONLY"
        else:
            interpretation = "tomographic_control_not_promoted_to_physical_alternative"
            physical_alternative_status = "CONTROL_ONLY"

        rows.append(
            {
                "policy_id": policy["policy_id"],
                "run_id": row["run_id"],
                "null_rank_by_chi2": row["control_index_one_based"],
                "control_family": row["control_family"],
                "operator": row["operator"],
                "beats_candidate_chi2": row["beats_candidate_chi2"],
                "delta_chi2_vs_baseline": row["delta_chi2_vs_baseline"],
                "is_global_bin_permutation": str(is_global).lower(),
                "global_bin_permutation": global_perm,
                "changed_pair_count": str(changed),
                "auto_to_auto_count": str(auto_to_auto),
                "cross_to_cross_count": str(cross_to_cross),
                "mean_abs_pair_mean_z_shift": f"{mean_abs_dz:.12e}",
                "max_abs_pair_mean_z_shift": f"{max_abs_dz:.12e}",
                "mean_abs_pair_separation_shift": f"{mean_abs_dsep:.12e}",
                "physical_alternative_status": physical_alternative_status,
                "interpretation": interpretation,
                "uses_kids_data_vector_values_for_scoring": "true",
                "uses_kids_data_vector_values_for_source_selection": "false",
                "computes_new_scores": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    better_rows = [row for row in rows if row["beats_candidate_chi2"] == "true"]
    conditional_source_systematics = [
        row for row in better_rows if row["physical_alternative_status"] == "CONDITIONAL_SOURCE_SYSTEMATIC"
    ]
    control_only_better = [row for row in better_rows if row["physical_alternative_status"] == "CONTROL_ONLY"]
    verdict = (
        "better_tomographic_controls_are_control_only_or_source_systematic_candidates_not_physical_alternatives"
    )
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "TOMOGRAPHIC_CONTROL_PLAUSIBILITY_AUDIT_BUILT",
            "selected_statistic": policy["selected_statistic"],
            "audited_top_control_count": str(len(rows)),
            "better_than_candidate_audited_count": str(len(better_rows)),
            "better_control_only_count": str(len(control_only_better)),
            "better_conditional_source_systematic_count": str(len(conditional_source_systematics)),
            "accepted_physical_alternative_count": "0",
            "candidate_tomographic_caveat_active": "true",
            "tomographic_controls_refute_endpoint_signal": "false",
            "tomographic_controls_block_validation": "true",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values_for_scoring": "true",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "endpoint_validation_claimed": "false",
            "verdict": verdict,
            "recommended_next_action": "freeze_independent_photoz_or_tomographic_calibration_holdout_before_promoting_any_tomographic_alternative",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_CONTROL_PLAUSIBILITY_AUDIT_V1_BUILT "
        f"verdict={verdict} accepted_physical_alternatives=0"
    )


if __name__ == "__main__":
    main()
