#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QI_SUMMARY = ROOT / "data/derived/joint_best_justified_qi_review_response_v1_summary.csv"
SCORE_SUMMARY = ROOT / "data/derived/joint_best_justified_kernel_score_v1_summary.csv"
ROBUSTNESS_SUMMARY = ROOT / "data/derived/joint_best_justified_kernel_robustness_v1_summary.csv"
MANIFEST = ROOT / "data/source_manifest/joint_best_justified_kernel_manifest_v1.csv"
POLICY = ROOT / "data/source_manifest/joint_likelihood_surrogate_requirements_policy_v1.csv"
OUT = ROOT / "data/derived/joint_likelihood_surrogate_requirements_gate_v1.csv"
SUMMARY = ROOT / "data/derived/joint_likelihood_surrogate_requirements_gate_v1_summary.csv"
DOC = ROOT / "docs/joint_likelihood_surrogate_requirements_gate_v1.md"
CLAIM_BOUNDARY = "joint_likelihood_surrogate_requirements_gate_not_scoring_not_validation"


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
    qi = read_one(QI_SUMMARY)
    score = read_one(SCORE_SUMMARY)
    robustness_rows = read_rows(ROBUSTNESS_SUMMARY)
    robustness_summary = robustness_rows[-1]
    manifest_rows = read_rows(MANIFEST)
    active_channels = [r for r in manifest_rows if r["positive_support_allowed"] == "true"]

    qi_accepted = qi["decision"] == "QI_REVIEW_ACCEPTED_OR_CAVEATED_SOURCE_SIDE_NOT_VALIDATION"
    qi_no_forbidden = all(
        qi[field] == "false"
        for field in [
            "forbidden_inputs_used",
            "endpoint_scores_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
        ]
    )
    score_positive = score["verdict"] == "BEST_JUSTIFIED_JOINT_KERNEL_POSITIVE_PREFLIGHT_NOT_VALIDATION"
    robustness_positive = robustness_summary["verdict"] == "BEST_JUSTIFIED_KERNEL_ROBUST_POSITIVE_PREFLIGHT_NOT_VALIDATION"
    active_count_ok = len(active_channels) >= 2

    policy_rows = [
        {
            "requirement_id": "JLS_REQ_01_QI_SOURCE_REVIEW",
            "requirement": "Completed Q_i source-side review accepts or caveats all active support factors without endpoint inputs.",
            "required_for": "likelihood_surrogate_preparation",
            "status": "pass" if qi_accepted and qi_no_forbidden else "blocked",
            "evidence": qi["decision"],
            "hard_blocker_if_failed": "true",
        },
        {
            "requirement_id": "JLS_REQ_02_ACTIVE_CHANNEL_SET",
            "requirement": "Positive-support channel set is frozen before scoring and excludes zero-support/control-dominated branches.",
            "required_for": "likelihood_surrogate_preparation",
            "status": "pass" if active_count_ok else "blocked",
            "evidence": ";".join(r["channel_id"] for r in active_channels),
            "hard_blocker_if_failed": "true",
        },
        {
            "requirement_id": "JLS_REQ_03_PREFLIGHT_SIGNAL",
            "requirement": "Best-justified preflight signal is positive and robustness-positive, but remains non-validation.",
            "required_for": "motivation_only",
            "status": "pass" if score_positive and robustness_positive else "blocked",
            "evidence": f"score={score['verdict']}; robustness={robustness_summary['verdict']}",
            "hard_blocker_if_failed": "false",
        },
        {
            "requirement_id": "JLS_REQ_04_COVARIANCE_MODEL",
            "requirement": "A single covariance treatment is specified for all active blocks, including cross-block or justified block-diagonal terms.",
            "required_for": "likelihood_surrogate_scoring",
            "status": "blocked",
            "evidence": "not yet defined for the joint Q_i-weighted kernel",
            "hard_blocker_if_failed": "true",
        },
        {
            "requirement_id": "JLS_REQ_05_JOINT_STATISTIC",
            "requirement": "A single predeclared joint likelihood or likelihood-surrogate statistic maps all active channel residuals into one score.",
            "required_for": "likelihood_surrogate_scoring",
            "status": "blocked",
            "evidence": "current artifacts are support-weighted preflight scores, not a likelihood surrogate",
            "hard_blocker_if_failed": "true",
        },
        {
            "requirement_id": "JLS_REQ_06_CONTROL_SUITE",
            "requirement": "Shuffled-channel, wrong-channel, sign-flip, block-drop, null/readout, and leave-one-probe controls use the same covariance/statistic.",
            "required_for": "likelihood_surrogate_scoring",
            "status": "blocked",
            "evidence": "control families are named but not yet implemented under one covariance-aware statistic",
            "hard_blocker_if_failed": "true",
        },
        {
            "requirement_id": "JLS_REQ_07_FORBIDDEN_FIELDS",
            "requirement": "Endpoint residuals, fit improvements, posterior chains, and post-score control ranks remain forbidden inputs to Q_i and channel activation.",
            "required_for": "leakage_prevention",
            "status": "pass" if qi_no_forbidden else "blocked",
            "evidence": "completed Q_i response has all forbidden/validation flags false",
            "hard_blocker_if_failed": "true",
        },
        {
            "requirement_id": "JLS_REQ_08_CLAIM_BOUNDARY",
            "requirement": "The gate itself makes no endpoint, cosmological, physical, or validation claim.",
            "required_for": "claim_safety",
            "status": "pass",
            "evidence": CLAIM_BOUNDARY,
            "hard_blocker_if_failed": "true",
        },
    ]
    for row in policy_rows:
        row.update(
            {
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    write_csv(POLICY, policy_rows)
    write_csv(OUT, policy_rows)

    passed = sum(1 for r in policy_rows if r["status"] == "pass")
    blocked = sum(1 for r in policy_rows if r["status"] == "blocked")
    hard_blockers_open = sum(1 for r in policy_rows if r["status"] == "blocked" and r["hard_blocker_if_failed"] == "true")
    scoring_allowed = hard_blockers_open == 0
    verdict = (
        "JOINT_LIKELIHOOD_SURROGATE_READY_FOR_REVIEWED_SCORING_NOT_VALIDATION"
        if scoring_allowed
        else "JOINT_LIKELIHOOD_SURROGATE_REQUIREMENTS_FROZEN_SCORING_BLOCKED"
    )
    summary = {
        "gate_id": "JOINT_LIKELIHOOD_SURROGATE_REQUIREMENTS_GATE_V1",
        "input_qi_decision": qi["decision"],
        "active_channel_count": str(len(active_channels)),
        "active_channel_order": ";".join(r["channel_id"] for r in active_channels),
        "requirements_total": str(len(policy_rows)),
        "requirements_passed": str(passed),
        "requirements_blocked": str(blocked),
        "hard_blockers_open": str(hard_blockers_open),
        "covariance_model_defined": "false",
        "joint_statistic_defined": "false",
        "control_suite_defined": "false",
        "endpoint_scoring_allowed": bool_str(scoring_allowed),
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "next_required_action": "define_covariance_aware_joint_likelihood_surrogate_and_controls_before_scoring",
        "verdict": verdict,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# Joint likelihood-surrogate requirements gate v1",
                "",
                "**Doc class:** requirements gate",
                "**Status:** not scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This gate records the next step opened by the completed Q_i source-side",
                "review. The review accepts the active support factors only as caveated",
                "source-side support; it does not authorize validation-facing promotion.",
                "Therefore the next object must be a separately frozen joint likelihood",
                "or likelihood-surrogate protocol with covariance-aware controls.",
                "",
                "Summary:",
                "",
                f"- Q_i decision: `{summary['input_qi_decision']}`",
                f"- active channels: `{summary['active_channel_order']}`",
                f"- requirements passed: `{summary['requirements_passed']}/{summary['requirements_total']}`",
                f"- hard blockers open: `{summary['hard_blockers_open']}`",
                f"- endpoint scoring allowed: `{summary['endpoint_scoring_allowed']}`",
                f"- next required action: `{summary['next_required_action']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: the Paper10 joint-kernel route is now source-side",
                "organized enough to specify the validation-facing protocol, but not to",
                "run it. The remaining blockers are the covariance model, the single joint",
                "statistic, and the matched control suite under that same statistic.",
                "",
            ]
        )
    )
    print(
        "JOINT_LIKELIHOOD_SURROGATE_REQUIREMENTS_GATE_V1_BUILT "
        f"verdict={verdict} hard_blockers_open={hard_blockers_open}"
    )


if __name__ == "__main__":
    main()
