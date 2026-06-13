#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JLS_SUMMARY = ROOT / "data/derived/joint_likelihood_surrogate_requirements_gate_v1_summary.csv"
COV_SUMMARY = ROOT / "data/derived/joint_covariance_model_requirements_gate_v1_summary.csv"
BDI_SUMMARY = ROOT / "data/derived/joint_block_diagonal_independence_review_response_v1_summary.csv"
MANIFEST = ROOT / "data/source_manifest/joint_best_justified_kernel_manifest_v1.csv"
POLICY = ROOT / "data/source_manifest/joint_matched_control_suite_requirements_policy_v1.csv"
OUT = ROOT / "data/derived/joint_matched_control_suite_requirements_gate_v1.csv"
SUMMARY = ROOT / "data/derived/joint_matched_control_suite_requirements_gate_v1_summary.csv"
DOC = ROOT / "docs/joint_matched_control_suite_requirements_gate_v1.md"
CLAIM_BOUNDARY = "joint_matched_control_suite_requirements_gate_not_scoring_not_validation"


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


def main() -> None:
    jls = read_one(JLS_SUMMARY)
    cov = read_one(COV_SUMMARY)
    bdi = read_one(BDI_SUMMARY)
    manifest = read_rows(MANIFEST)
    active = [row for row in manifest if row["positive_support_allowed"] == "true"]
    active_ids = [row["channel_id"] for row in active]
    if active_ids != ["kids_lensing_cosebis_low_mode", "observer_path_basis_low_z", "desi_shape_time_readout"]:
        raise SystemExit(f"unexpected active channel order: {active_ids}")
    if jls["verdict"] != "JOINT_LIKELIHOOD_SURROGATE_REQUIREMENTS_FROZEN_SCORING_BLOCKED":
        raise SystemExit("joint likelihood-surrogate gate not in expected blocked state")
    if cov["endpoint_scoring_allowed"] != "false":
        raise SystemExit("covariance gate unexpectedly allows scoring")
    if bdi["endpoint_scoring_allowed"] != "false":
        raise SystemExit("block-diagonal response gate unexpectedly allows scoring")

    rows = [
        {
            "control_id": "JMC_REQ_01_SHUFFLED_CHANNEL",
            "control_family": "shuffled_channel_labels",
            "required_question": "Does the matched active-channel assignment outperform source-blind channel-label shuffles?",
            "required_binding": "same_active_rows_same_covariance_same_statistic",
            "status": "specified_not_implemented",
            "implementation_blocker": "single_joint_statistic_and_reviewed_covariance_not_defined",
            "evidence": "preflight shuffles exist, but not under one covariance-aware joint likelihood surrogate",
        },
        {
            "control_id": "JMC_REQ_02_WRONG_CHANNEL",
            "control_family": "wrong_channel_or_wrong_family_controls",
            "required_question": "Does each active readout contribution beat source-incompatible channel/family replacements?",
            "required_binding": "same_covariance_same_statistic_same_channel_scope",
            "status": "specified_not_implemented",
            "implementation_blocker": "wrong-channel replacements must be frozen after joint statistic definition",
            "evidence": "single-channel wrong-family controls exist in places, but not as a matched joint suite",
        },
        {
            "control_id": "JMC_REQ_03_SIGN_FLIP",
            "control_family": "sign_flip_controls",
            "required_question": "Does the joint signal survive deterministic sign-flip controls for the active blocks?",
            "required_binding": "same_covariance_same_statistic_complete_sign_flip_enumeration",
            "status": "specified_not_implemented",
            "implementation_blocker": "existing sign-flips are preflight contribution controls, not covariance-aware likelihood controls",
            "evidence": "joint preflight sign-flip controls exist and must be re-run under the final statistic",
        },
        {
            "control_id": "JMC_REQ_04_BLOCK_DROP",
            "control_family": "leave_one_probe_or_block_drop",
            "required_question": "Is the joint result not carried by a single active probe after leave-one-probe/block-drop tests?",
            "required_binding": "same_covariance_same_statistic_recomputed_for_each_block_drop",
            "status": "specified_not_implemented",
            "implementation_blocker": "requires final covariance/statistic and per-block contribution vectors",
            "evidence": "leave-one checks exist for preflight scores; final joint block-drop remains unimplemented",
        },
        {
            "control_id": "JMC_REQ_05_NULL_READOUT",
            "control_family": "null_readout_controls",
            "required_question": "Do null/readout-trivial channels fail under the same statistic?",
            "required_binding": "same_covariance_same_statistic_source_frozen_nulls",
            "status": "specified_not_implemented",
            "implementation_blocker": "null readout set must be source-frozen against the final active-channel vector",
            "evidence": "several null/control branches are preserved, but not yet bound into the final joint suite",
        },
        {
            "control_id": "JMC_REQ_06_SCOPE_AND_LEAKAGE",
            "control_family": "scope_and_forbidden_input_controls",
            "required_question": "Are row scope, labels, controls, and nuisance rules frozen without endpoint residual leakage?",
            "required_binding": "same_rows_same_masks_no_endpoint_residuals_no_post_score_ranks",
            "status": "specified_not_implemented",
            "implementation_blocker": "final scoring protocol not defined; leakage validator must be attached to it",
            "evidence": "current Q_i and BDI gates keep forbidden fields false",
        },
        {
            "control_id": "JMC_REQ_07_SHARED_STATISTIC_BINDING",
            "control_family": "single_statistic_binding",
            "required_question": "Are all controls evaluated by exactly the same joint statistic as the candidate?",
            "required_binding": "single_predeclared_statistic_required_before_any_scoring",
            "status": "blocked",
            "implementation_blocker": "joint_statistic_defined=false",
            "evidence": jls["joint_statistic_defined"],
        },
        {
            "control_id": "JMC_REQ_08_COVARIANCE_BINDING",
            "control_family": "covariance_binding",
            "required_question": "Are all controls evaluated with the same reviewed covariance or block-diagonal surrogate as the candidate?",
            "required_binding": "reviewed_covariance_or_reviewed_block_diagonal_surrogate_required",
            "status": "blocked",
            "implementation_blocker": "cross_probe_covariance_or_independence_not_closed",
            "evidence": f"cross_probe_covariance_defined={cov['cross_probe_covariance_defined']}; block_diagonal_response={bdi['decision']}",
        },
    ]
    for row in rows:
        row.update(
            {
                "active_channel_order": ";".join(active_ids),
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(POLICY, rows)
    write_csv(OUT, rows)

    specified = sum(1 for row in rows if row["status"] in {"specified_not_implemented", "blocked"})
    implemented = sum(1 for row in rows if row["status"] == "implemented")
    blocked = sum(1 for row in rows if row["status"] == "blocked")
    summary = {
        "gate_id": "JOINT_MATCHED_CONTROL_SUITE_REQUIREMENTS_GATE_V1",
        "upstream_likelihood_gate_verdict": jls["verdict"],
        "upstream_covariance_gate_verdict": cov["verdict"],
        "upstream_block_diagonal_response_decision": bdi["decision"],
        "active_channel_count": str(len(active_ids)),
        "active_channel_order": ";".join(active_ids),
        "required_control_families": str(len(rows)),
        "specified_control_families": str(specified),
        "implemented_control_families": str(implemented),
        "blocked_control_families": str(blocked),
        "single_joint_statistic_defined": jls["joint_statistic_defined"],
        "covariance_or_independence_closed": "false",
        "control_suite_defined": "true",
        "control_suite_implemented_under_joint_statistic": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "next_required_action": "complete_covariance_or_independence_review_then_build_single_joint_statistic_protocol",
        "verdict": "JOINT_MATCHED_CONTROL_SUITE_REQUIREMENTS_FROZEN_IMPLEMENTATION_BLOCKED",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint matched control-suite requirements gate v1",
                "",
                "**Doc class:** matched-control requirements gate",
                "**Status:** not scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This gate freezes the control families required before any Paper10 joint",
                "likelihood-surrogate scoring attempt. It does not run controls and does",
                "not define the final joint statistic. The controls must later be evaluated",
                "under exactly the same reviewed covariance/statistic as the candidate.",
                "",
                "Required control families:",
                "",
                "- shuffled channel labels",
                "- wrong-channel / wrong-family controls",
                "- deterministic sign flips",
                "- leave-one-probe / block-drop controls",
                "- null/readout controls",
                "- scope and leakage controls",
                "- shared-statistic binding",
                "- covariance binding",
                "",
                "Summary:",
                "",
                f"- active channels: `{summary['active_channel_order']}`",
                f"- specified control families: `{summary['specified_control_families']}/{summary['required_control_families']}`",
                f"- implemented under joint statistic: `{summary['control_suite_implemented_under_joint_statistic']}`",
                f"- scoring allowed: `{summary['endpoint_scoring_allowed']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: the matched controls are now named and bound to a future",
                "single-statistic/covariance discipline, but they remain implementation-blocked",
                "until the covariance/independence gate and single-statistic gate are closed.",
                "",
            ]
        )
    )
    print(
        "JOINT_MATCHED_CONTROL_SUITE_REQUIREMENTS_GATE_V1_BUILT "
        f"verdict={summary['verdict']} controls={summary['specified_control_families']}/{summary['required_control_families']}"
    )


if __name__ == "__main__":
    main()
