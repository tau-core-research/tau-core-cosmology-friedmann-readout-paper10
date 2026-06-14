#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/joint_same_statistic_replay_authorization_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_same_statistic_replay_authorization_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/joint_same_statistic_replay_authorization_package_v1.zip"
SHA = ROOT / "data/derived/joint_same_statistic_replay_authorization_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_same_statistic_replay_authorization_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_same_statistic_replay_authorization_package_v1_summary.csv"
DOC = ROOT / "docs/joint_same_statistic_replay_authorization_package_v1.md"
BD_AUTH = ROOT / "data/derived/joint_block_diagonal_scoring_authorization_review_response_v1_summary.csv"
STAT_SHELL = ROOT / "data/derived/joint_single_statistic_protocol_shell_v1_summary.csv"
STAT_ROWS = ROOT / "data/derived/joint_single_statistic_protocol_shell_v1.csv"
CONTROL_READY = ROOT / "data/derived/joint_matched_control_implementation_readiness_v1_summary.csv"
CONTROL_ROWS = ROOT / "data/derived/joint_matched_control_implementation_readiness_v1.csv"
COV_PLAN = ROOT / "data/derived/joint_covariance_resolution_plan_v1_summary.csv"
CLAIM_BOUNDARY = "joint_same_statistic_replay_authorization_not_scoring_not_validation"
PACKAGE_ID = "JOINT_SAME_STATISTIC_REPLAY_AUTHORIZATION_PACKAGE_V1"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
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
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def manifest_row(path: Path) -> dict[str, str]:
    return {
        "package_id": PACKAGE_ID,
        "package_path": rel(path),
        "byte_count": str(path.stat().st_size),
        "sha256": sha256(path),
        "contains_endpoint_residuals": "false",
        "contains_new_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    bd_auth = read_one(BD_AUTH)
    stat = read_one(STAT_SHELL)
    control = read_one(CONTROL_READY)
    cov = read_one(COV_PLAN)

    if bd_auth["decision"] != "AUTHORIZE_SEPARATE_GUARDED_JOINT_PERMISSION_REPLAY_PACKAGE_NOT_SCORING_NOT_VALIDATION":
        raise SystemExit("block-diagonal authorization does not allow a separate guarded package")
    if bd_auth["direct_scoring_allowed"] != "false":
        raise SystemExit("direct scoring must remain forbidden")
    if stat["protocol_executable"] != "false":
        raise SystemExit("statistic shell must remain non-executable")
    if control["implementation_ready_for_scoring"] != "false":
        raise SystemExit("controls must not be scoring-ready")
    if cov["cross_probe_covariance_defined"] != "false":
        raise SystemExit("cross-probe covariance must remain open in this package")

    forbidden = "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks"
    rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "JSSR_Q1_SCOPE",
            "question": "May the next step prepare a separate guarded permission-only replay package using the symbolic T_joint shell?",
            "required_response": "authorize_guarded_permission_package_or_reject",
            "acceptance_condition": "Accept only if this remains package authorization, not direct scoring or validation.",
            "forbidden_inputs": forbidden,
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "JSSR_Q2_SAME_STATISTIC",
            "question": "Are candidate and controls required to use the same symbolic statistic T_joint = sum_i q_i z_i?",
            "required_response": "accept_same_statistic_binding_or_reject",
            "acceptance_condition": "Accept only if candidate and all controls share the same symbolic formula, row scope, signs, q_i weights, and standardization rule.",
            "forbidden_inputs": forbidden,
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "JSSR_Q3_COVARIANCE_CAVEAT",
            "question": "Are the caveated block-diagonal covariance caveats carried forward without claiming a source-native cross-probe covariance?",
            "required_response": "accept_caveated_covariance_binding_or_reject",
            "acceptance_condition": "Accept only if shared sky/mask, redshift-kernel, nuisance/calibration, and population-covariance caveats are preserved.",
            "forbidden_inputs": forbidden,
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "JSSR_Q4_CONTROL_READINESS",
            "question": "Is it clear that control designs exist but are not yet executable scoring controls?",
            "required_response": "accept_control_readiness_boundary_or_reject",
            "acceptance_condition": "Accept only if the six design-ready controls and two upstream-blocked controls remain non-scoring until a later replay package is built.",
            "forbidden_inputs": forbidden,
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(POLICY, rows)
    template_rows = [
        {
            **row,
            "review_completed": "false",
            "reviewer_id_or_role": "",
            "reviewer_response": "",
            "reviewer_rationale": "",
            "forbidden_inputs_used": "false",
            "permission_only_replay_package_allowed": "false",
            "direct_scoring_allowed": "false",
        }
        for row in rows
    ]
    write_csv(TEMPLATE, template_rows)

    DOC.write_text(
        "\n".join(
            [
                "# Joint same-statistic replay authorization package v1",
                "",
                "**Doc class:** external authorization handoff",
                "**Status:** package authorization only; not scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This package asks whether the next step may prepare a separate guarded",
                "permission-only replay package using the symbolic joint statistic",
                "`T_joint = sum_i q_i z_i`. It does not compute `T_joint` and does",
                "not run controls.",
                "",
                "The authorization boundary is strict: candidate and controls must share",
                "the same symbolic statistic, row scope, q_i weights, signs,",
                "standardization rule, and covariance route. The covariance route is the",
                "caveated block-diagonal surrogate, not a source-native cross-probe",
                "covariance product.",
                "",
                "Upstream status:",
                "",
                f"- block-diagonal authorization decision: `{bd_auth['decision']}`",
                f"- statistic shell verdict: `{stat['verdict']}`",
                f"- matched-control readiness verdict: `{control['verdict']}`",
                f"- covariance route verdict: `{cov['verdict']}`",
                "",
            ]
        )
    )

    package_inputs = [
        DOC,
        POLICY,
        TEMPLATE,
        BD_AUTH,
        STAT_SHELL,
        STAT_ROWS,
        CONTROL_READY,
        CONTROL_ROWS,
        COV_PLAN,
    ]
    manifest_rows = [manifest_row(path) for path in package_inputs]
    write_csv(MANIFEST, manifest_rows)
    package_rows = manifest_rows + [manifest_row(MANIFEST)]
    with zipfile.ZipFile(PACKAGE, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for row in package_rows:
            path = ROOT / row["package_path"]
            info = zipfile.ZipInfo(row["package_path"])
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    digest = sha256(PACKAGE)
    SHA.write_text(f"{digest}  {PACKAGE.name}\n")
    write_csv(
        SUMMARY,
        [
            {
                "package_id": PACKAGE_ID,
                "status": "JOINT_SAME_STATISTIC_REPLAY_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": rel(PACKAGE),
                "zip_sha256_path": rel(SHA),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "permission_only_replay_package_allowed": "false",
                "direct_scoring_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "verdict": "same_statistic_replay_authorization_package_ready_not_completed_not_scoring",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_SAME_STATISTIC_REPLAY_AUTHORIZATION_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
