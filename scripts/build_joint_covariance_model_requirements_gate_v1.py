#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/source_manifest/joint_best_justified_kernel_manifest_v1.csv"
JLS_SUMMARY = ROOT / "data/derived/joint_likelihood_surrogate_requirements_gate_v1_summary.csv"
KIDS_COV = ROOT / "data/derived/kids1000_cosebis_covariance_readiness_v1_summary.csv"
KIDS_INV = ROOT / "data/derived/kids1000_cosebis_covariance_inversion_readiness_v1_summary.csv"
OBSERVER = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv"
DESI = ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv"
DESI_COV = ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_covariance_v1.csv"
OUT = ROOT / "data/derived/joint_covariance_model_requirements_gate_v1.csv"
SUMMARY = ROOT / "data/derived/joint_covariance_model_requirements_gate_v1_summary.csv"
POLICY = ROOT / "data/source_manifest/joint_covariance_model_policy_v1.csv"
DOC = ROOT / "docs/joint_covariance_model_requirements_gate_v1.md"
CLAIM_BOUNDARY = "joint_covariance_model_requirements_gate_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
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


def bool_str(value: bool) -> str:
    return str(value).lower()


def main() -> None:
    manifest = read_rows(MANIFEST)
    jls = read_one(JLS_SUMMARY)
    kids_cov = read_one(KIDS_COV)
    kids_inv = read_one(KIDS_INV)
    observer = read_one(OBSERVER)
    desi = read_one(DESI)
    desi_cov_rows = read_rows(DESI_COV)
    active = [r for r in manifest if r["positive_support_allowed"] == "true"]
    active_ids = [r["channel_id"] for r in active]
    if active_ids != ["kids_lensing_cosebis_low_mode", "observer_path_basis_low_z", "desi_shape_time_readout"]:
        raise SystemExit(f"unexpected active channel order: {active_ids}")

    kids_ready = kids_cov["positive_definite"] == "true" and kids_cov["cholesky_ready"] == "true"
    kids_solve_ready = kids_inv["cholesky_ready"] == "true"
    observer_cov_ready = observer["covariance_min_eigenvalue"] != "" and float(observer["covariance_min_eigenvalue"]) > 0
    desi_diag_nonzero = sum(1 for r in desi_cov_rows if r["row_i"] == r["row_j"] and float(r["cov_minus_log_DH_over_rs"]) > 0)
    desi_ready = desi_diag_nonzero >= 3 and desi["family_survives_controls"] == "true"

    rows = [
        {
            "channel_id": "kids_lensing_cosebis_low_mode",
            "block_role": "active_positive_support",
            "covariance_status": "source_native_full_covariance_ready" if kids_ready and kids_solve_ready else "blocked",
            "covariance_dimension": kids_cov["covariance_shape"],
            "covariance_rule": "use_source_native_COVMAT_with_cholesky_solve_after_theory_vector_freeze",
            "cross_block_rule": "block_diagonal_until_shared_cross_probe_covariance_is_source_frozen",
            "hard_blocker": bool_str(not (kids_ready and kids_solve_ready)),
            "evidence": f"positive_definite={kids_cov['positive_definite']}; cholesky_ready={kids_cov['cholesky_ready']}; inversion_policy={kids_inv['inversion_policy']}",
        },
        {
            "channel_id": "observer_path_basis_low_z",
            "block_role": "active_positive_support",
            "covariance_status": "local_permission_replay_covariance_available_not_population_covariance" if observer_cov_ready else "blocked",
            "covariance_dimension": f"{observer['n_rows']}x{observer['n_rows']}",
            "covariance_rule": "use_existing_permission_replay_covariance_only_as_narrow_surrogate_block",
            "cross_block_rule": "block_diagonal_and_scope_caveated_until_population_path_covariance_exists",
            "hard_blocker": "true",
            "evidence": f"n_rows={observer['n_rows']}; min_eigenvalue={observer['covariance_min_eigenvalue']}; condition={observer['covariance_condition_number']}; scope=narrow_permission_only",
        },
        {
            "channel_id": "desi_shape_time_readout",
            "block_role": "active_positive_support",
            "covariance_status": "small_shape_route_covariance_interface_available_caveated" if desi_ready else "blocked",
            "covariance_dimension": f"{desi['n_shape_rows']}x{desi['n_shape_rows']}_shape_surrogate",
            "covariance_rule": "use_frozen_shape_route_covariance_interface_as_caveated_small_block",
            "cross_block_rule": "block_diagonal_until_desi_cross_probe_joint_covariance_is_source_frozen",
            "hard_blocker": "true",
            "evidence": f"shape_rows={desi['n_shape_rows']}; diagonal_cov_rows={desi_diag_nonzero}; family_survives_controls={desi['family_survives_controls']}; small_margin={desi['delta_candidate_minus_best_control_score']}",
        },
        {
            "channel_id": "cross_probe_joint_covariance",
            "block_role": "global_requirement",
            "covariance_status": "blocked",
            "covariance_dimension": "not_defined",
            "covariance_rule": "must_define_cross_probe_or_justify_block_diagonal_independence_before_scoring",
            "cross_block_rule": "currently_block_diagonal_is_only_a_future_surrogate_candidate_not_scoring_permission",
            "hard_blocker": "true",
            "evidence": "no source-frozen cross-probe covariance or independence attestation for KiDS/observer-path/DESI blocks",
        },
    ]
    for row in rows:
        row.update(
            {
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(POLICY, rows)
    write_csv(OUT, rows)

    channel_blocks_ready = sum(1 for r in rows[:3] if r["covariance_status"] != "blocked")
    hard_blockers_open = sum(1 for r in rows if r["hard_blocker"] == "true")
    summary = {
        "gate_id": "JOINT_COVARIANCE_MODEL_REQUIREMENTS_GATE_V1",
        "upstream_gate_verdict": jls["verdict"],
        "active_channel_count": str(len(active_ids)),
        "active_channel_order": ";".join(active_ids),
        "channel_covariance_blocks_available": str(channel_blocks_ready),
        "channel_covariance_blocks_total": "3",
        "cross_probe_covariance_defined": "false",
        "block_diagonal_surrogate_allowed_for_future_review": "true",
        "block_diagonal_surrogate_allowed_for_scoring_now": "false",
        "hard_blockers_open": str(hard_blockers_open),
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "next_required_action": "freeze_block_diagonal_independence_attestation_or_source_cross_probe_covariance_then_define_joint_statistic",
        "verdict": "JOINT_COVARIANCE_MODEL_REQUIREMENTS_PARTIAL_BLOCKS_READY_CROSS_PROBE_BLOCKED",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint covariance-model requirements gate v1",
                "",
                "**Doc class:** covariance requirements gate",
                "**Status:** not scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This gate narrows the first hard blocker from the joint likelihood-surrogate",
                "requirements ledger: the covariance treatment for the three active positive-support",
                "channels. It does not build a joint likelihood and does not permit scoring.",
                "",
                "Summary:",
                "",
                f"- active channels: `{summary['active_channel_order']}`",
                f"- channel covariance blocks available: `{summary['channel_covariance_blocks_available']}/{summary['channel_covariance_blocks_total']}`",
                f"- cross-probe covariance defined: `{summary['cross_probe_covariance_defined']}`",
                f"- block-diagonal surrogate allowed for future review: `{summary['block_diagonal_surrogate_allowed_for_future_review']}`",
                f"- block-diagonal surrogate allowed for scoring now: `{summary['block_diagonal_surrogate_allowed_for_scoring_now']}`",
                f"- hard blockers open: `{summary['hard_blockers_open']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: KiDS has a source-native full covariance block. The observer/path",
                "and DESI shape/readout blocks have narrow, caveated surrogate covariance support,",
                "but remain hard blockers for validation-facing scoring. A future reviewed",
                "block-diagonal likelihood surrogate may be prepared only if cross-probe independence",
                "is frozen explicitly or a source-native cross-probe covariance is supplied.",
                "",
            ]
        )
    )
    print(
        "JOINT_COVARIANCE_MODEL_REQUIREMENTS_GATE_V1_BUILT "
        f"blocks={summary['channel_covariance_blocks_available']}/{summary['channel_covariance_blocks_total']} "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
