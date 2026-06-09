#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mask_mode_leakage_audit_policy_v1.csv"
PURE_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_pure_mask_response_gate_policy_v1.csv"
PURE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_pure_mask_response_gate_v1_summary.csv"
TILE_BASIS = ROOT / "data" / "derived" / "kids1000_cosebis_pure_mask_response_tile_basis_v1.csv"
SPECTRUM_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mode_response_spectrum_attempt_policy_v1.csv"
SPECTRA = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_spectrum_attempt_v1_spectra.csv"
SPECTRUM_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_spectrum_attempt_v1_summary.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_mask_mode_leakage_audit_v1.csv"
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_mask_mode_leakage_audit_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mask_mode_leakage_audit_v1_summary.csv"


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


def rms(values: np.ndarray) -> float:
    return float(math.sqrt(float(np.mean(values * values))))


def main() -> None:
    policy = read_one(POLICY)
    pure_policy = read_one(PURE_POLICY)
    pure_summary = read_one(PURE_SUMMARY)
    spectrum_policy = read_one(SPECTRUM_POLICY)
    spectrum_summary = read_one(SPECTRUM_SUMMARY)
    tile_rows = read_rows(TILE_BASIS)
    spectra_rows = read_rows(SPECTRA)

    if policy["status"] != "MASK_MODE_LEAKAGE_AUDIT_POLICY_FROZEN":
        raise SystemExit("unexpected mask-mode leakage policy status")
    if policy["parent_pure_mask_response_gate_policy"] != pure_policy["policy_id"]:
        raise SystemExit("pure-mask parent policy mismatch")
    if policy["parent_mode_response_spectrum_attempt_policy"] != spectrum_policy["policy_id"]:
        raise SystemExit("spectrum parent policy mismatch")
    for label, row in [
        ("policy", policy),
        ("pure summary", pure_summary),
        ("spectrum summary", spectrum_summary),
    ]:
        for key in ["uses_kids_data_vector_values", "endpoint_scoring_allowed"]:
            if row.get(key) != "false":
                raise SystemExit(f"{label} must keep {key}=false")
    if pure_summary["pure_mask_basis_constructed"] != "true":
        raise SystemExit("pure-mask basis must be built first")
    if spectrum_summary["mode_response_operator_derived"] != "false":
        raise SystemExit("mask-mode leakage audit must not mark operator derived")
    if len(tile_rows) != 196:
        raise SystemExit("mask-mode leakage audit expects 196 tile basis rows")

    basis_columns = {
        "f_overlap_centered": "f_overlap_centered_unit_rms",
        "d_path_centered": "d_path_centered_unit_rms",
        "d_path_orthogonal_to_f_overlap": "d_path_orthogonal_to_f_overlap_unit_rms",
    }
    basis_values = {
        basis_id: np.asarray([float(row[column]) for row in tile_rows], dtype=float)
        for basis_id, column in basis_columns.items()
    }
    for basis_id, values in basis_values.items():
        if abs(float(values.mean())) > 1.0e-10:
            raise SystemExit(f"{basis_id} must be centered over route tiles")
        if abs(rms(values) - 1.0) > 1.0e-10:
            raise SystemExit(f"{basis_id} must have unit RMS over route tiles")

    weights_by_family: dict[str, np.ndarray] = {}
    for family in sorted({row["spectrum_family"] for row in spectra_rows}):
        rows = sorted(
            [row for row in spectra_rows if row["spectrum_family"] == family],
            key=lambda row: int(row["mode"]),
        )
        if len(rows) != 20:
            raise SystemExit(f"spectrum family {family} must contain 20 modes")
        weights_by_family[family] = np.asarray([float(row["unit_mean_weight"]) for row in rows], dtype=float)

    grid: list[dict[str, str]] = []
    for basis_id, values in basis_values.items():
        uniform_tile_mean = float(values.mean())
        route_tile_rms = rms(values)
        route_tile_abs_mean = float(np.mean(np.abs(values)))
        for family, weights in weights_by_family.items():
            uniform_collapse_norm = abs(uniform_tile_mean) * rms(weights)
            rms_envelope_norm = route_tile_rms * rms(weights)
            abs_mean_envelope_norm = route_tile_abs_mean * rms(weights)
            grid.append(
                {
                    "policy_id": policy["policy_id"],
                    "basis_id": basis_id,
                    "spectrum_family": family,
                    "uniform_tile_mean": float_text(uniform_tile_mean),
                    "route_tile_rms": float_text(route_tile_rms),
                    "route_tile_abs_mean": float_text(route_tile_abs_mean),
                    "mode_weight_rms": float_text(rms(weights)),
                    "uniform_collapse_norm": float_text(uniform_collapse_norm),
                    "rms_envelope_norm": float_text(rms_envelope_norm),
                    "abs_mean_envelope_norm": float_text(abs_mean_envelope_norm),
                    "uniform_collapse_is_null": str(uniform_collapse_norm < 1.0e-10).lower(),
                    "leakage_risk_if_operator_uses_rms_or_abs_mask_load": str(rms_envelope_norm > 0.0).lower(),
                    "contains_theory_vector": "false",
                    "contains_predictions": "false",
                    "contains_residuals": "false",
                    "contains_fit_statistics": "false",
                    "uses_kids_data_vector_values": "false",
                    "uses_posterior_chains": "false",
                    "endpoint_scoring_allowed": "false",
                    "endpoint_validation_claimed": "false",
                    "claim_boundary": policy["claim_boundary"],
                }
            )

    low_mode_rows = [
        row
        for row in grid
        if row["spectrum_family"] == spectrum_summary["conditional_primary_spectrum"]
    ]
    max_uniform = max(float(row["uniform_collapse_norm"]) for row in grid)
    max_low_mode_rms_envelope = max(float(row["rms_envelope_norm"]) for row in low_mode_rows)
    ledger = [
        {
            "policy_id": policy["policy_id"],
            "gate_id": "L1_centered_mask_uniform_collapse",
            "status": "PASS",
            "source_artifact": rel(TILE_BASIS),
            "requirement": "Centered pure-mask directions should collapse to zero under uniform tile averaging.",
            "current_evidence": f"max_uniform_collapse_norm={float_text(max_uniform)}",
            "operator_implication": "uniform_tile_average_would_kill_pure_mask_basis",
            "dimension_check": "centered_mask_basis_and_mode_weights_are_dimensionless",
            "limit_check": "uniform_operator_limit_maps_pure_mask_basis_to_zero",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "L2_nonuniform_operator_leakage_risk",
            "status": "RISK_RECORDED",
            "source_artifact": rel(GRID),
            "requirement": "A non-uniform operator may couple mask-only tile amplitudes to the low-mode envelope unless null-safety is proven.",
            "current_evidence": f"max_low_mode_rms_envelope_norm={float_text(max_low_mode_rms_envelope)}",
            "operator_implication": "mask_only_to_low_mode_leakage_not_ruled_out",
            "dimension_check": "risk_norm_is_dimensionless_and_not_a_lensing_prediction",
            "limit_check": "risk_vanishes_only_for_uniform_tile_collapse_not_for_arbitrary_operator",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "L3_no_endpoint_or_data_vector_use",
            "status": "PASS",
            "source_artifact": f"{rel(POLICY)};{rel(SPECTRA)}",
            "requirement": "The leakage audit must not use KiDS En values, residuals, scores, posterior chains, or fit statistics.",
            "current_evidence": "uses_kids_data_vector_values=false; contains_fit_statistics=false; endpoint_scoring_allowed=false",
            "operator_implication": "leakage_risk_audit_is_source_side_only",
            "dimension_check": "no_observed_lensing_units_enter_the_audit",
            "limit_check": "audit_can_be_rebuilt_without_endpoint_data",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "L4_operator_level_leakage_theorem",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_survey_native_operator_leakage_theorem",
            "requirement": "The future survey-native operator must prove that mask-only directions do not masquerade as the physical low-mode path signal.",
            "current_evidence": "Only a source-side leakage-risk norm is available; no operator theorem is present.",
            "operator_implication": "mode_response_coupling_blocker_remains_open",
            "dimension_check": "future_operator_must_map_dimensionless_mask_basis_to_quotient_trivial_or_controlled_response",
            "limit_check": "pure_mask_nonuniformity_should_not_create_positive_tau_residual",
            "claim_boundary": policy["claim_boundary"],
        },
    ]
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "MASK_MODE_LEAKAGE_AUDIT_SOURCE_SIDE_COMPLETE_OPERATOR_BLOCKED",
            "selected_statistic": policy["selected_statistic"],
            "basis_count": str(len(basis_values)),
            "spectrum_family_count": str(len(weights_by_family)),
            "grid_rows": str(len(grid)),
            "conditional_primary_spectrum": spectrum_summary["conditional_primary_spectrum"],
            "max_uniform_collapse_norm": float_text(max_uniform),
            "uniform_collapse_all_null": str(max_uniform < 1.0e-10).lower(),
            "max_low_mode_rms_envelope_norm": float_text(max_low_mode_rms_envelope),
            "leakage_risk_recorded": "true",
            "operator_level_leakage_theorem_proven": "false",
            "mode_response_operator_derived": "false",
            "contains_theory_vector": "false",
            "contains_predictions": "false",
            "contains_residuals": "false",
            "contains_fit_statistics": "false",
            "uses_kids_data_vector_values": "false",
            "uses_posterior_chains": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "open_blocker_count": str(sum(row["status"] == "OPEN_BLOCKER" for row in ledger)),
            "verdict": "uniform_mask_collapse_is_null_but_nonuniform_operator_leakage_remains_open",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(GRID, grid)
    write_csv(LEDGER, ledger)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_MASK_MODE_LEAKAGE_AUDIT_V1_COMPLETE "
        f"verdict={summary[0]['verdict']} open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
