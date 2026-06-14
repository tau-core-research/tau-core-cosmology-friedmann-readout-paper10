#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESPONSE = ROOT / "data/derived/joint_same_statistic_replay_authorization_response_v1.csv"
RESPONSE_SUMMARY = ROOT / "data/derived/joint_same_statistic_replay_authorization_response_v1_summary.csv"
STAT_SHELL = ROOT / "data/derived/joint_single_statistic_protocol_shell_v1.csv"
STAT_SUMMARY = ROOT / "data/derived/joint_single_statistic_protocol_shell_v1_summary.csv"
CONTROL_ROWS = ROOT / "data/derived/joint_matched_control_implementation_readiness_v1.csv"
CONTROL_SUMMARY = ROOT / "data/derived/joint_matched_control_implementation_readiness_v1_summary.csv"
COV_PLAN = ROOT / "data/derived/joint_covariance_resolution_plan_v1_summary.csv"
BD_AUTH = ROOT / "data/derived/joint_block_diagonal_scoring_authorization_review_response_v1_summary.csv"
POLICY = ROOT / "data/source_manifest/joint_same_statistic_guarded_permission_replay_policy_v1.csv"
DOC = ROOT / "docs/joint_same_statistic_guarded_permission_replay_package_v1.md"
MANIFEST = ROOT / "data/derived/joint_same_statistic_guarded_permission_replay_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_same_statistic_guarded_permission_replay_package_v1_summary.csv"
PACKAGE = ROOT / "data/derived/joint_same_statistic_guarded_permission_replay_package_v1.zip"
SHA = ROOT / "data/derived/joint_same_statistic_guarded_permission_replay_package_v1.zip.sha256"
CLAIM_BOUNDARY = "joint_same_statistic_guarded_permission_replay_package_not_execution_not_scoring_not_validation"
PACKAGE_ID = "JOINT_SAME_STATISTIC_GUARDED_PERMISSION_REPLAY_PACKAGE_V1"


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


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
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
        "direct_execution_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    response = read_one(RESPONSE_SUMMARY)
    stat = read_one(STAT_SUMMARY)
    controls = read_one(CONTROL_SUMMARY)
    cov = read_one(COV_PLAN)
    bd_auth = read_one(BD_AUTH)

    if response["decision"] != "AUTHORIZE_SAME_STATISTIC_GUARDED_PERMISSION_REPLAY_PACKAGE_NOT_SCORING_NOT_VALIDATION":
        raise SystemExit("same-statistic authorization response is not accepted")
    if response["permission_only_replay_package_allowed"] != "true":
        raise SystemExit("permission-only replay package was not allowed")
    for field in [
        "direct_scoring_allowed",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
        "forbidden_inputs_used",
    ]:
        if response[field] != "false":
            raise SystemExit(f"unsafe same-statistic response field: {field}")
    if stat["protocol_executable"] != "false":
        raise SystemExit("symbolic statistic shell must remain non-executable")
    if controls["implementation_ready_for_scoring"] != "false":
        raise SystemExit("matched controls must remain non-scoring")
    if cov["cross_probe_covariance_defined"] != "false":
        raise SystemExit("cross-probe covariance must remain open/caveated")
    if bd_auth["direct_scoring_allowed"] != "false":
        raise SystemExit("upstream block-diagonal authorization must not allow direct scoring")

    policy_rows = [
        {
            "package_id": PACKAGE_ID,
            "rule_id": "JSSGPR_01_SCOPE",
            "rule": "package_preparation_only",
            "value": "true",
            "description": "This artifact prepares a permission-only replay package; it is not execution, scoring, endpoint validation, or cosmological validation.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "package_id": PACKAGE_ID,
            "rule_id": "JSSGPR_02_STATISTIC",
            "rule": "same_symbolic_statistic_for_candidate_and_controls",
            "value": "T_joint=sum_i_q_i_z_i",
            "description": "Candidate and controls must use the same symbolic statistic, same row scope, same q_i weights, same signs, and same standardization rule.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "package_id": PACKAGE_ID,
            "rule_id": "JSSGPR_03_CONTROLS",
            "rule": "matched_controls_bound_but_not_executable",
            "value": "true",
            "description": "Control designs are carried forward as frozen requirements; they are not executable scoring controls in this package.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "package_id": PACKAGE_ID,
            "rule_id": "JSSGPR_04_COVARIANCE",
            "rule": "caveated_block_diagonal_route_only",
            "value": "true",
            "description": "The covariance route remains caveated block diagonal; no source-native cross-probe covariance product is claimed.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "package_id": PACKAGE_ID,
            "rule_id": "JSSGPR_05_NEXT_GATE",
            "rule": "separate_execution_authorization_required",
            "value": "true",
            "description": "A later executable replay requires a separate run-template/execution authorization gate.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_rows(POLICY, policy_rows)

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint same-statistic guarded permission replay package v1",
                "",
                "**Doc class:** permission-only package preparation.",
                "**Status:** ready, not executed.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This artifact carries the completed same-statistic authorization into a",
                "guarded package boundary.  It does not execute the joint statistic, does",
                "not compute endpoint scores, and does not claim endpoint, cosmological,",
                "or physical validation.",
                "",
                "The package freezes the same-statistic requirement:",
                "",
                "`T_joint = sum_i q_i z_i`",
                "",
                "Any later candidate/control replay must use the same symbolic statistic,",
                "same row scope, same `q_i` weights, same signs, same standardization rule,",
                "and the same caveated block-diagonal covariance route.",
                "",
                "The matched-control suite remains a frozen requirement, not an executable",
                "scoring suite in this package.  A separate execution authorization is still",
                "required before any replay script can run.",
                "",
                "Carried caveats:",
                "- no source-native cross-probe covariance product is available;",
                "- the block-diagonal route is caveated;",
                "- shared sky/mask, redshift-kernel, nuisance/calibration, and population",
                "  covariance caveats remain active;",
                "- direct scoring and validation claims remain forbidden.",
                "",
            ]
        )
    )

    inputs = [
        POLICY,
        DOC,
        RESPONSE,
        RESPONSE_SUMMARY,
        STAT_SHELL,
        STAT_SUMMARY,
        CONTROL_ROWS,
        CONTROL_SUMMARY,
        COV_PLAN,
        BD_AUTH,
    ]
    manifest = [manifest_row(path) for path in inputs]
    write_rows(MANIFEST, manifest)
    package_rows = manifest + [manifest_row(MANIFEST)]
    with zipfile.ZipFile(PACKAGE, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for row in package_rows:
            path = ROOT / row["package_path"]
            info = zipfile.ZipInfo(row["package_path"])
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    digest = sha256(PACKAGE)
    SHA.write_text(f"{digest}  {PACKAGE.name}\n")
    write_rows(
        SUMMARY,
        [
            {
                "package_id": PACKAGE_ID,
                "status": "JOINT_SAME_STATISTIC_GUARDED_PERMISSION_REPLAY_PACKAGE_READY_NOT_EXECUTED",
                "zip_path": rel(PACKAGE),
                "zip_sha256_path": rel(SHA),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "same_statistic_bound": "true",
                "matched_controls_bound": "true",
                "permission_only_replay_package_allowed": "true",
                "direct_execution_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "next_required_action": "build_separate_run_template_or_execution_authorization_before_any_replay",
                "verdict": "same_statistic_guarded_permission_package_ready_not_executed_not_scoring_not_validation",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_SAME_STATISTIC_GUARDED_PERMISSION_REPLAY_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
