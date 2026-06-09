#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_pure_mask_response_gate_policy_v1.csv"
NULL_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_operator_null_safety_gate_policy_v1.csv"
NULL_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_null_safety_gate_v1_summary.csv"
F_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_policy_v1.csv"
D_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_d_path_full_route_mask_load_rule_policy_v1.csv"
F_TILE = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_pixel_fraction_tile_rule_v1.csv"
D_TILE = ROOT / "data" / "derived" / "kids1000_cosebis_d_path_full_route_mask_load_tile_rule_v1.csv"
DOMAIN = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_domain_skeleton_v1.csv"
F_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1_summary.csv"
D_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_d_path_full_route_mask_load_rule_v1_summary.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_pure_mask_response_gate_v1.csv"
TILE_BASIS = ROOT / "data" / "derived" / "kids1000_cosebis_pure_mask_response_tile_basis_v1.csv"
DOMAIN_BASIS = ROOT / "data" / "derived" / "kids1000_cosebis_pure_mask_response_domain_basis_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_pure_mask_response_gate_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
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


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def float_text(value: float) -> str:
    return f"{value:.12e}"


def centered_unit_rms(values: np.ndarray) -> tuple[np.ndarray, float, float]:
    centered = values - float(values.mean())
    rms = float(math.sqrt(float(np.mean(centered * centered))))
    if rms <= 0.0:
        raise SystemExit("cannot normalize a degenerate centered mask basis")
    return centered / rms, float(values.mean()), rms


def main() -> None:
    policy = read_one(POLICY)
    null_policy = read_one(NULL_POLICY)
    null_summary = read_one(NULL_SUMMARY)
    f_policy = read_one(F_POLICY)
    d_policy = read_one(D_POLICY)
    f_summary = read_one(F_SUMMARY)
    d_summary = read_one(D_SUMMARY)
    f_tiles = read_rows(F_TILE)
    d_tiles = read_rows(D_TILE)
    domain_rows = read_rows(DOMAIN)

    if policy["status"] != "PURE_MASK_RESPONSE_GATE_POLICY_FROZEN":
        raise SystemExit("unexpected pure-mask response gate policy status")
    if policy["parent_operator_null_safety_gate_policy"] != null_policy["policy_id"]:
        raise SystemExit("operator null-safety parent mismatch")
    if policy["parent_f_overlap_policy"] != f_policy["policy_id"]:
        raise SystemExit("F_overlap parent mismatch")
    if policy["parent_d_path_policy"] != d_policy["policy_id"]:
        raise SystemExit("D_path parent mismatch")
    for label, row in [
        ("policy", policy),
        ("null summary", null_summary),
        ("F summary", f_summary),
        ("D summary", d_summary),
    ]:
        for key in ["uses_kids_data_vector_values", "endpoint_scoring_allowed"]:
            if row.get(key) != "false":
                raise SystemExit(f"{label} must keep {key}=false")
    if null_summary["mask_null_operator_proven"] != "false":
        raise SystemExit("pure-mask response gate must start from unproven mask null operator")
    if f_summary["full_route_pixel_fraction_non_degenerate"] != "true":
        raise SystemExit("F_overlap full-route basis must be non-degenerate")
    if d_summary["d_path_full_route_mask_load_non_degenerate"] != "true":
        raise SystemExit("D_path full-route basis must be non-degenerate")
    if len(f_tiles) != 196 or len(d_tiles) != 196:
        raise SystemExit("pure-mask basis expects 196 source mask tiles")
    if len(domain_rows) != 58800:
        raise SystemExit("pure-mask domain basis expects 58,800 rows")

    f_by_tile = {row["tile_index_zero_based"]: row for row in f_tiles}
    d_by_tile = {row["tile_index_zero_based"]: row for row in d_tiles}
    if set(f_by_tile) != set(d_by_tile):
        raise SystemExit("F_overlap and D_path tile domains differ")
    tile_ids = sorted(f_by_tile, key=lambda value: int(value))

    f_values = np.array(
        [float(f_by_tile[tile]["f_overlap_full_route_pixel_fraction_value"]) for tile in tile_ids],
        dtype=float,
    )
    d_values = np.array(
        [float(d_by_tile[tile]["d_path_full_route_mask_load_value"]) for tile in tile_ids],
        dtype=float,
    )
    f_basis, f_mean, f_rms = centered_unit_rms(f_values)
    d_basis, d_mean, d_rms = centered_unit_rms(d_values)
    cosine = float(np.dot(f_basis, d_basis) / len(tile_ids))
    d_parallel = cosine * f_basis
    d_orth = d_basis - d_parallel
    d_orth_rms = float(math.sqrt(float(np.mean(d_orth * d_orth))))
    if d_orth_rms <= 0.0:
        raise SystemExit("D_path must contain a component not parallel to F_overlap")
    d_orth_basis = d_orth / d_orth_rms

    tile_rows: list[dict[str, str]] = []
    for idx, tile in enumerate(tile_ids):
        f_row = f_by_tile[tile]
        d_row = d_by_tile[tile]
        tile_rows.append(
            {
                "policy_id": policy["policy_id"],
                "tile_index_zero_based": tile,
                "tile_ra_deg_filename_proxy": f_row["tile_ra_deg_filename_proxy"] if "tile_ra_deg_filename_proxy" in f_row else "",
                "tile_dec_deg_filename_proxy": f_row["tile_dec_deg_filename_proxy"] if "tile_dec_deg_filename_proxy" in f_row else "",
                "f_overlap_value": float_text(f_values[idx]),
                "d_path_value": float_text(d_values[idx]),
                "f_overlap_centered_unit_rms": float_text(float(f_basis[idx])),
                "d_path_centered_unit_rms": float_text(float(d_basis[idx])),
                "d_path_orthogonal_to_f_overlap_unit_rms": float_text(float(d_orth_basis[idx])),
                "pure_mask_basis_constructed": "true",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_tile_selection": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    tile_basis = {row["tile_index_zero_based"]: row for row in tile_rows}
    domain_out: list[dict[str, str]] = []
    for domain in domain_rows:
        basis = tile_basis[domain["tile_index_zero_based"]]
        domain_out.append(
            {
                "policy_id": policy["policy_id"],
                "domain_row_index_zero_based": domain["domain_row_index_zero_based"],
                "target_row_index_zero_based": domain["target_row_index_zero_based"],
                "tile_index_zero_based": domain["tile_index_zero_based"],
                "pair_id": domain["pair_id"],
                "bin1": domain["bin1"],
                "bin2": domain["bin2"],
                "mode": domain["mode"],
                "f_overlap_centered_unit_rms": basis["f_overlap_centered_unit_rms"],
                "d_path_centered_unit_rms": basis["d_path_centered_unit_rms"],
                "d_path_orthogonal_to_f_overlap_unit_rms": basis[
                    "d_path_orthogonal_to_f_overlap_unit_rms"
                ],
                "pure_mask_basis_constructed": "true",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_tile_selection": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    effective_rank = 2 if d_orth_rms > 1e-8 else 1
    rows = [
        {
            "policy_id": policy["policy_id"],
            "gate_id": "P1_full_route_mask_sources_available",
            "status": "SATISFIED",
            "source_artifact": f"{rel(F_SUMMARY)};{rel(D_SUMMARY)}",
            "requirement": "The pure-mask audit must use source-frozen full-route mask observables only.",
            "current_evidence": (
                f"f_tiles={f_summary['tile_count']}; d_tiles={d_summary['tile_count']}; "
                f"f_unique={f_summary['unique_f_overlap_value_count_rounded_1e_minus_12']}; "
                f"d_unique={d_summary['unique_d_path_value_count_rounded_1e_minus_12']}"
            ),
            "operator_implication": "source_mask_basis_exists_without_endpoint_feedback",
            "dimension_check": "F_overlap_and_D_path_are_dimensionless_normalized_source_mask_observables",
            "limit_check": "uniform_mask_observable_would_fail_centered_basis_construction",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "P2_centered_pure_mask_basis_constructed",
            "status": "SATISFIED",
            "source_artifact": rel(TILE_BASIS),
            "requirement": "Construct centered unit-RMS mask-only perturbation directions before any theory-vector or endpoint use.",
            "current_evidence": (
                f"f_mean={float_text(f_mean)}; f_rms={float_text(f_rms)}; "
                f"d_mean={float_text(d_mean)}; d_rms={float_text(d_rms)}"
            ),
            "operator_implication": "pure_mask_perturbations_can_be_replayed_as_controls",
            "dimension_check": "centered_unit_rms_basis_is_dimensionless",
            "limit_check": "mean_mask_load_component_removed_before_null_response_audit",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "P3_two_direction_mask_basis_non_degenerate",
            "status": "SATISFIED_CAVEATED",
            "source_artifact": rel(TILE_BASIS),
            "requirement": "The two mask observables should not collapse to a single centered direction.",
            "current_evidence": (
                f"f_d_centered_cosine={float_text(cosine)}; "
                f"d_orthogonal_rms={float_text(d_orth_rms)}; effective_rank={effective_rank}"
            ),
            "operator_implication": "mask_control_space_has_more_than_one_source_direction_but_no_physical_operator_yet",
            "dimension_check": "orthogonalized_mask_direction_remains_dimensionless",
            "limit_check": "parallel_D_path_and_F_overlap_would_reduce_to_rank_one_control",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "P4_domain_lift_available",
            "status": "SATISFIED",
            "source_artifact": rel(DOMAIN_BASIS),
            "requirement": "The source-only pure-mask basis must be liftable to the 58,800-row target-by-tile domain.",
            "current_evidence": f"domain_rows={len(domain_out)}; target_rows=300; tile_rows={len(tile_rows)}",
            "operator_implication": "future_operator_can_test_pure_mask_directions_over_the_cosebis_domain",
            "dimension_check": "domain_lift_repeats_dimensionless_tile_basis_over_pair_and_mode_rows",
            "limit_check": "domain_lift_contains_no_KiDS_En_values_or_scores",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "P5_mapping_or_theory_vector_not_constructed",
            "status": "SATISFIED",
            "source_artifact": rel(DOMAIN_BASIS),
            "requirement": "The pure-mask basis must not be promoted into a mapping vector or theory vector in this gate.",
            "current_evidence": "contains_mapping_vector=false; contains_theory_vector=false; endpoint_scoring_allowed=false",
            "operator_implication": "basis_is_control_ready_not_endpoint_ready",
            "dimension_check": "no_lensing_units_or_endpoint_amplitude_enter",
            "limit_check": "zero_endpoint_use_preserves_no_validation_claim",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "P6_quotient_triviality_not_proven",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_pure_mask_quotient_theorem",
            "requirement": "Pure-mask perturbation directions must be shown to be quotient-trivial or explicitly controlled under the survey-native operator.",
            "current_evidence": "The basis is source-computable, but no operator maps it to a quotient-trivial response class.",
            "operator_implication": "mask_null_operator_response_blocker_remains_open",
            "dimension_check": "future_operator_must_preserve_units_and_normalization_under_mask_perturbation",
            "limit_check": "pure_mask_change_must_not_generate_positive_tau_residual",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "P7_mode_response_coupling_not_proven",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_pure_mask_mode_response_test",
            "requirement": "The same source-native operator must determine whether pure-mask perturbations leak into the COSEBIs mode response.",
            "current_evidence": "The basis is tile-level and domain-lifted, but no mode-response operator acts on it.",
            "operator_implication": "cannot_yet_rule_out_mask_leakage_into_low_mode_envelope",
            "dimension_check": "mode_response_coupling_must_keep_dimensionless_carrier_until_endpoint_amplitude",
            "limit_check": "mask_only_direction_should_not_be_misread_as_smooth_path_signal",
            "claim_boundary": policy["claim_boundary"],
        },
    ]

    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "PURE_MASK_RESPONSE_GATE_BASIS_BUILT_OPERATOR_PROOF_BLOCKED",
            "selected_statistic": policy["selected_statistic"],
            "tile_rows": str(len(tile_rows)),
            "domain_rows": str(len(domain_out)),
            "effective_centered_mask_basis_rank": str(effective_rank),
            "f_overlap_mean": float_text(f_mean),
            "f_overlap_rms": float_text(f_rms),
            "d_path_mean": float_text(d_mean),
            "d_path_rms": float_text(d_rms),
            "f_d_centered_cosine": float_text(cosine),
            "d_orthogonal_to_f_rms": float_text(d_orth_rms),
            "pure_mask_basis_constructed": "true",
            "pure_mask_domain_lift_constructed": "true",
            "pure_mask_quotient_triviality_proven": "false",
            "pure_mask_mode_response_coupling_proven": "false",
            "mask_null_operator_response_proven": "false",
            "contains_mapping_vector": "false",
            "contains_theory_vector": "false",
            "contains_predictions": "false",
            "contains_residuals": "false",
            "contains_fit_statistics": "false",
            "uses_kids_data_vector_values": "false",
            "uses_posterior_chains": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "open_blocker_count": str(sum(row["status"] == "OPEN_BLOCKER" for row in rows)),
            "verdict": "pure_mask_basis_exists_but_quotient_triviality_and_mode_coupling_remain_blocked",
            "claim_boundary": policy["claim_boundary"],
        }
    ]

    write_csv(TILE_BASIS, tile_rows)
    write_csv(DOMAIN_BASIS, domain_out)
    write_csv(LEDGER, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PURE_MASK_RESPONSE_GATE_V1_COMPLETE "
        f"rank={effective_rank} verdict={summary[0]['verdict']} "
        f"open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
