#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/source_manifest/joint_guarded_replay_run_template_v1.csv"
SUMMARY = ROOT / "data/derived/joint_guarded_replay_run_template_v1_summary.csv"
DOC = ROOT / "docs/joint_guarded_replay_run_template_v1.md"
AUTH_SUMMARY = ROOT / "data/derived/joint_guarded_permission_replay_authorization_response_v1_summary.csv"
SCORING_AUTH_SUMMARY = ROOT / "data/derived/joint_block_diagonal_scoring_authorization_review_response_v1_summary.csv"
CLAIM_BOUNDARY = "joint_guarded_replay_run_template_not_execution_not_scoring_not_validation"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required upstream artifact: {path.relative_to(ROOT)}")
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


def main() -> None:
    auth = read_one(AUTH_SUMMARY)
    scoring_auth = read_one(SCORING_AUTH_SUMMARY)
    if auth["decision"] != "AUTHORIZE_GUARDED_PERMISSION_REPLAY_PACKAGE_PREPARATION_ONLY_NOT_EXECUTION_NOT_SCORING_NOT_VALIDATION":
        raise SystemExit("guarded permission authorization is not in preparation-only accepted state")
    if auth["next_action"] != "build_separate_guarded_replay_run_template_and_validator_before_any_executable_replay":
        raise SystemExit("guarded authorization does not point to run-template construction")
    if scoring_auth["decision"] != "AUTHORIZE_SEPARATE_GUARDED_JOINT_PERMISSION_REPLAY_PACKAGE_NOT_SCORING_NOT_VALIDATION":
        raise SystemExit("scoring authorization response is not in permission-only accepted state")
    for row, label in [(auth, "guarded authorization"), (scoring_auth, "scoring authorization")]:
        for field in ["endpoint_scoring_allowed", "endpoint_validation_claimed", "cosmological_validation_claimed"]:
            if row[field] != "false":
                raise SystemExit(f"{label} unsafe field {field}")

    active_blocks = [
        "kids_lensing_cosebis_low_mode",
        "observer_path_basis_low_z",
        "desi_shape_time_readout",
    ]
    controls = [
        "shuffled_channel_labels",
        "wrong_channel_assignment",
        "sign_flip",
        "block_drop",
        "null_readout",
        "leakage_audit",
        "shared_statistic_control",
        "covariance_binding_control",
    ]
    caveats = [
        "no_source_native_cross_probe_covariance_product",
        "block_diagonal_independence_caveated",
        "shared_sky_overlap_caveat",
        "shared_mask_selection_caveat",
        "shared_redshift_kernel_caveat",
        "shared_cosmology_nuisance_caveat",
        "shared_calibration_population_caveat",
    ]
    forbidden = [
        "endpoint_residuals",
        "new_endpoint_scores",
        "fit_improvements",
        "posterior_chains",
        "post_score_control_ranks",
        "posthoc_channel_selection",
        "posthoc_block_weight_tuning",
        "posthoc_covariance_reweighting",
        "cosmological_validation_claims",
    ]
    dependency_paths = [
        "data/derived/joint_guarded_permission_replay_authorization_response_v1_summary.csv",
        "data/derived/joint_block_diagonal_scoring_authorization_review_response_v1_summary.csv",
        "data/derived/joint_cross_probe_covariance_source_requirements_v1_summary.csv",
        "data/derived/joint_single_statistic_binding_prerequisites_v1_summary.csv",
        "data/derived/joint_matched_control_suite_requirements_gate_v1_summary.csv",
        "data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1_summary.csv",
    ]

    row = {
        "run_id": "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_V1",
        "status": "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_READY_NOT_EXECUTED",
        "active_block_order": ";".join(active_blocks),
        "statistic_rule": "same_frozen_block_diagonal_statistic_for_candidate_and_all_controls",
        "block_weight_rule": "same_frozen_block_weights_for_candidate_and_all_controls",
        "covariance_rule": "same_declared_block_covariance_or_same_caveated_block_diagonal_independence_for_candidate_and_controls",
        "required_controls": ";".join(controls),
        "required_caveats": ";".join(caveats),
        "forbidden_inputs": ";".join(forbidden),
        "dependency_summaries": ";".join(dependency_paths),
        "run_template_only": "true",
        "direct_execution_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "next_required_action": "external_authorization_of_this_run_template_before_any_executable_replay",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, [row])
    write_csv(
        SUMMARY,
        [
            {
                "run_id": row["run_id"],
                "status": row["status"],
                "active_block_count": str(len(active_blocks)),
                "required_control_count": str(len(controls)),
                "required_caveat_count": str(len(caveats)),
                "forbidden_input_count": str(len(forbidden)),
                "run_template_only": "true",
                "direct_execution_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "authorization_decision": auth["decision"],
                "scoring_authorization_decision": scoring_auth["decision"],
                "verdict": "joint_guarded_replay_run_template_ready_not_executed_not_scoring_not_validation",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint guarded replay run template v1",
                "",
                "This artifact is a run-template gate, not an executable replay,",
                "not endpoint scoring, and not cosmological validation.",
                "",
                "The completed guarded-permission response authorizes only",
                "preparation of this separate template.  It keeps direct execution",
                "disabled until this template is independently authorized.",
                "",
                "The template freezes the active block order, the shared",
                "block-diagonal statistic, the same block-weight rule, and the",
                "matched control suite.  Candidate and controls must be evaluated",
                "under identical statistic, covariance, caveat, and block-weight",
                "conditions in any later replay.",
                "",
                "Required controls:",
                "",
                *[f"- `{item}`" for item in controls],
                "",
                "Required caveats:",
                "",
                *[f"- `{item}`" for item in caveats],
                "",
                f"Claim boundary: `{CLAIM_BOUNDARY}`.",
                "",
            ]
        )
    )
    print("JOINT_GUARDED_REPLAY_RUN_TEMPLATE_V1_BUILT status=not_executed")


if __name__ == "__main__":
    main()
