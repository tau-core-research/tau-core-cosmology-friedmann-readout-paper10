#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "data/derived/joint_matched_control_distribution_readiness_v1_summary.csv"
READINESS_ROWS = ROOT / "data/derived/joint_matched_control_distribution_readiness_v1.csv"
SIGNED_PROTOCOL = ROOT / "data/derived/joint_signed_zi_standardization_protocol_v1_summary.csv"
SIGNED_PROTOCOL_ROWS = ROOT / "data/derived/joint_signed_zi_standardization_protocol_v1.csv"
ZI_AUDIT = ROOT / "data/derived/joint_numeric_channel_zi_binding_audit_v1_summary.csv"
ZI_AUDIT_ROWS = ROOT / "data/derived/joint_numeric_channel_zi_binding_audit_v1.csv"
POLICY = ROOT / "data/source_manifest/joint_numeric_zi_distribution_build_authorization_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_numeric_zi_distribution_build_authorization_response_template_v1.csv"
DOC = ROOT / "docs/joint_numeric_zi_distribution_build_authorization_package_v1.md"
MANIFEST = ROOT / "data/derived/joint_numeric_zi_distribution_build_authorization_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_zi_distribution_build_authorization_package_v1_summary.csv"
PACKAGE = ROOT / "data/derived/joint_numeric_zi_distribution_build_authorization_package_v1.zip"
SHA = ROOT / "data/derived/joint_numeric_zi_distribution_build_authorization_package_v1.zip.sha256"
CLAIM_BOUNDARY = "joint_numeric_zi_distribution_build_authorization_not_scoring_not_validation"
PACKAGE_ID = "JOINT_NUMERIC_ZI_DISTRIBUTION_BUILD_AUTHORIZATION_PACKAGE_V1"


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
        "sha256": sha256(path),
        "contains_endpoint_residuals": "false",
        "contains_new_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "numeric_zi_build_allowed": "false",
        "numeric_t_joint_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    readiness = read_one(READINESS)
    signed = read_one(SIGNED_PROTOCOL)
    zi = read_one(ZI_AUDIT)
    if readiness["all_channels_ready_for_numeric_zi"] != "true":
        raise SystemExit("all channels must have distributions before z_i build authorization package")
    if readiness["center_scale_computable_now"] != "false":
        raise SystemExit("authorization package must be prepared before center/scale computation")
    if signed["signed_standardization_rule_frozen"] != "true":
        raise SystemExit("signed z_i standardization protocol must be frozen")
    if zi["numeric_channel_binding_ready"] != "false":
        raise SystemExit("z_i binding must remain blocked before authorization")

    forbidden = (
        "endpoint_residuals;new_endpoint_scores;fit_improvements;posterior_chains;"
        "posthoc_channel_selection;posthoc_sign_changes;posthoc_center_scale_selection;"
        "posthoc_control_family_removal;cosmological_validation_claims"
    )
    rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "NZD_Q1_SCOPE",
            "question": "May a numeric z_i distribution build be prepared from the frozen signed protocol and listed matched-control distributions?",
            "required_response": "authorize_distribution_build_or_reject",
            "acceptance_condition": "Accept only a center/scale distribution build; do not authorize T_joint scoring or validation.",
            "forbidden_inputs": forbidden,
            "numeric_zi_build_allowed": "false",
            "numeric_t_joint_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "NZD_Q2_CAVEATS",
            "question": "Must KiDS endpoint-score-not-validation and DESI small-N caveats remain attached to the distribution build?",
            "required_response": "accept_caveated_distribution_boundary_or_reject",
            "acceptance_condition": "Accept only if caveated channels cannot be read as population validation or physical confirmation.",
            "forbidden_inputs": forbidden,
            "numeric_zi_build_allowed": "false",
            "numeric_t_joint_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "NZD_Q3_FROZEN_RULE",
            "question": "Must center and scale be computed only from matched controls using the frozen median/MAD rule?",
            "required_response": "accept_frozen_center_scale_rule_or_reject",
            "acceptance_condition": "Accept only if candidate values cannot define center or scale and zero/unavailable scale remains a blocker.",
            "forbidden_inputs": forbidden,
            "numeric_zi_build_allowed": "false",
            "numeric_t_joint_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "NZD_Q4_NO_PROMOTION",
            "question": "Must the output remain below T_joint scoring until a separate numeric T_joint authorization is prepared?",
            "required_response": "accept_no_t_joint_promotion_or_reject",
            "acceptance_condition": "Accept only if the strongest allowed next artifact is a z_i distribution ledger, not joint scoring.",
            "forbidden_inputs": forbidden,
            "numeric_zi_build_allowed": "false",
            "numeric_t_joint_allowed": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_rows(POLICY, rows)
    template = [
        {
            **row,
            "review_completed": "false",
            "reviewer_id_or_role": "",
            "reviewer_response": "",
            "reviewer_rationale": "",
            "forbidden_inputs_used": "false",
        }
        for row in rows
    ]
    write_rows(TEMPLATE, template)
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric z_i distribution build authorization package v1",
                "",
                "**Doc class:** external authorization handoff.",
                "**Status:** prepared, not completed.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This package asks whether a numeric channel-level `z_i` distribution",
                "build may be prepared from the frozen signed standardization protocol",
                "and the currently exposed matched-control distributions.",
                "",
                "It does not authorize `T_joint` computation, endpoint scoring,",
                "cosmological validation, or physical validation.",
                "",
                "If authorized, the output must keep KiDS endpoint-score-not-validation",
                "and DESI small-N caveats attached.",
            ]
        )
        + "\n"
    )
    inputs = [POLICY, TEMPLATE, DOC, READINESS, READINESS_ROWS, SIGNED_PROTOCOL, SIGNED_PROTOCOL_ROWS, ZI_AUDIT, ZI_AUDIT_ROWS]
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
                "status": "JOINT_NUMERIC_ZI_DISTRIBUTION_BUILD_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": rel(PACKAGE),
                "zip_sha256_path": rel(SHA),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "numeric_zi_build_allowed": "false",
                "numeric_t_joint_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "verdict": "numeric_zi_distribution_build_authorization_package_ready_not_completed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_NUMERIC_ZI_DISTRIBUTION_BUILD_AUTHORIZATION_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
