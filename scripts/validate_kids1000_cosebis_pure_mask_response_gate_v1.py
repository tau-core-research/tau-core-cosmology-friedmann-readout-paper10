#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_pure_mask_response_gate_policy_v1.csv"
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


def main() -> None:
    policy = read_one(POLICY)
    summary = read_one(SUMMARY)
    ledger = read_rows(LEDGER)
    tile_rows = read_rows(TILE_BASIS)
    domain_rows = read_rows(DOMAIN_BASIS)

    if policy["status"] != "PURE_MASK_RESPONSE_GATE_POLICY_FROZEN":
        raise SystemExit("unexpected pure-mask response gate policy status")
    for key in [
        "uses_kids_data_vector_values",
        "uses_fit_statistics",
        "uses_random_noise",
        "endpoint_scoring_allowed",
    ]:
        if policy[key] != "false":
            raise SystemExit(f"policy {key} must be false")
    if summary["status"] != "PURE_MASK_RESPONSE_GATE_BASIS_BUILT_OPERATOR_PROOF_BLOCKED":
        raise SystemExit("unexpected pure-mask response gate summary status")
    if summary["verdict"] != (
        "pure_mask_basis_exists_but_quotient_triviality_and_mode_coupling_remain_blocked"
    ):
        raise SystemExit("unexpected pure-mask response gate verdict")
    if summary["tile_rows"] != "196" or len(tile_rows) != 196:
        raise SystemExit("pure-mask tile basis must contain 196 rows")
    if summary["domain_rows"] != "58800" or len(domain_rows) != 58800:
        raise SystemExit("pure-mask domain basis must contain 58,800 rows")
    if summary["effective_centered_mask_basis_rank"] != "2":
        raise SystemExit("expected a rank-2 centered pure-mask basis")
    if summary["pure_mask_basis_constructed"] != "true":
        raise SystemExit("pure-mask basis must be constructed")
    if summary["pure_mask_domain_lift_constructed"] != "true":
        raise SystemExit("pure-mask domain lift must be constructed")
    if summary["pure_mask_quotient_triviality_proven"] != "false":
        raise SystemExit("pure-mask quotient triviality must not be marked proven")
    if summary["pure_mask_mode_response_coupling_proven"] != "false":
        raise SystemExit("pure-mask mode-response coupling must not be marked proven")
    if summary["mask_null_operator_response_proven"] != "false":
        raise SystemExit("mask null operator response must not be marked proven")
    if summary["open_blocker_count"] != "2":
        raise SystemExit("expected two open pure-mask blockers")
    if abs(float(summary["f_d_centered_cosine"])) >= 1.0:
        raise SystemExit("centered F/D cosine must be finite and non-degenerate")
    if float(summary["d_orthogonal_to_f_rms"]) <= 0.0:
        raise SystemExit("D orthogonal component must be positive")

    by_gate = {row["gate_id"]: row for row in ledger}
    expected = {
        "P1_full_route_mask_sources_available",
        "P2_centered_pure_mask_basis_constructed",
        "P3_two_direction_mask_basis_non_degenerate",
        "P4_domain_lift_available",
        "P5_mapping_or_theory_vector_not_constructed",
        "P6_quotient_triviality_not_proven",
        "P7_mode_response_coupling_not_proven",
    }
    if set(by_gate) != expected:
        raise SystemExit("unexpected pure-mask gate ids")
    if by_gate["P6_quotient_triviality_not_proven"]["status"] != "OPEN_BLOCKER":
        raise SystemExit("quotient triviality must remain open")
    if by_gate["P7_mode_response_coupling_not_proven"]["status"] != "OPEN_BLOCKER":
        raise SystemExit("mode-response coupling must remain open")
    if by_gate["P5_mapping_or_theory_vector_not_constructed"]["status"] != "SATISFIED":
        raise SystemExit("non-promotion gate should be satisfied")
    for row in ledger:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
        if not row["dimension_check"]:
            raise SystemExit("missing dimension check")
        if not row["limit_check"]:
            raise SystemExit("missing limit check")

    for row in tile_rows + domain_rows[:100]:
        for key in [
            "contains_mapping_vector",
            "contains_theory_vector",
            "contains_predictions",
            "contains_residuals",
            "contains_fit_statistics",
            "uses_kids_data_vector_values",
            "uses_posterior_chains",
            "uses_posthoc_tile_selection",
            "endpoint_scoring_allowed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"{key} must be false in pure-mask basis rows")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("basis row claim boundary mismatch")
    for key in [
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary {key} must be false")
    print(
        "PAPER10_KIDS1000_COSEBIS_PURE_MASK_RESPONSE_GATE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
