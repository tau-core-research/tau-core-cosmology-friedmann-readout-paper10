#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ID = "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_AUTHORIZATION_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "act_dr6_lensing_path_weight_replay_authorization_review_not_validation"

TEMPLATE = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_replay_authorization_review_response_template_v1.csv"
TEMPLATE_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "act_dr6_lensing_path_weight_replay_authorization_review_template_v1_summary.csv"
)
DOC = ROOT / "docs" / "act_dr6_lensing_path_weight_replay_authorization_review_v1.md"
OUT_ZIP = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_replay_authorization_review_package_v1.zip"
OUT_ZIP_SHA256 = (
    ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_replay_authorization_review_package_v1.zip.sha256"
)
MANIFEST = (
    ROOT
    / "data"
    / "derived"
    / "act_dr6_lensing_path_weight_replay_authorization_review_package_v1_manifest.csv"
)
SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "act_dr6_lensing_path_weight_replay_authorization_review_package_v1_summary.csv"
)

PACKAGE_FILES = [
    "docs/act_dr6_lensing_product_v1.md",
    "docs/act_dr6_lensing_low_z_sampling_pilot_v1.md",
    "docs/act_dr6_lensing_path_weight_candidate_v1.md",
    "docs/observer_path_metric_lensing_next_gate_v1.md",
    "docs/act_dr6_lensing_path_weight_replay_authorization_review_v1.md",
    "data/source_manifest/act_dr6_lensing_product_v1.csv",
    "data/derived/act_dr6_lensing_product_v1_summary.csv",
    "data/derived/act_dr6_lensing_inventory_v1_summary.csv",
    "data/derived/act_dr6_lensing_low_z_sampling_pilot_v1_summary.csv",
    "data/derived/act_dr6_lensing_path_weight_candidate_v1.csv",
    "data/derived/act_dr6_lensing_path_weight_candidate_v1_summary.csv",
    "data/derived/observer_path_metric_lensing_next_gate_v1.csv",
    "data/derived/observer_path_metric_lensing_next_gate_v1_summary.csv",
    "data/derived/act_dr6_lensing_path_weight_replay_authorization_review_response_template_v1.csv",
    "data/derived/act_dr6_lensing_path_weight_replay_authorization_review_template_v1_summary.csv",
    "scripts/build_act_dr6_lensing_low_z_sampling_pilot_v1.py",
    "scripts/validate_act_dr6_lensing_low_z_sampling_pilot_v1.py",
    "scripts/build_act_dr6_lensing_path_weight_candidate_v1.py",
    "scripts/validate_act_dr6_lensing_path_weight_candidate_v1.py",
    "scripts/build_observer_path_metric_lensing_next_gate_v1.py",
    "scripts/validate_observer_path_metric_lensing_next_gate_v1.py",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def manifest_row(rel: str) -> dict[str, str]:
    path = ROOT / rel
    if not path.exists():
        raise SystemExit(f"missing ACT review package file: {rel}")
    return {
        "package_id": PACKAGE_ID,
        "package_path": rel,
        "byte_count": str(path.stat().st_size),
        "sha256": sha256(path),
        "contains_endpoint_residuals": "false",
        "contains_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_template() -> None:
    rows = [
        {
            "review_id": "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_AUTHORIZATION_V1",
            "question_id": "Q1_source_product",
            "question": "Does the package document the ACT DR6 source product, checksum/status, and provider route sufficiently for source-side use?",
            "allowed_answers": "accept;accept_with_caveat;reject",
            "reviewer_answer": "",
            "reviewer_notes": "",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_AUTHORIZATION_V1",
            "question_id": "Q2_sampling_and_mask",
            "question": "Is the 424-row low-z sampling pilot, including the 168 mask-positive rule and outside-mask zero policy, acceptable for a source-side candidate?",
            "allowed_answers": "accept;accept_with_caveat;reject",
            "reviewer_answer": "",
            "reviewer_notes": "",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_AUTHORIZATION_V1",
            "question_id": "Q3_normalization_rule",
            "question": "Is the mask-positive-only median/MAD normalization acceptable as a residual-blind unitless path-weight candidate rule?",
            "allowed_answers": "accept;accept_with_caveat;reject",
            "reviewer_answer": "",
            "reviewer_notes": "",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_AUTHORIZATION_V1",
            "question_id": "Q4_null_controls",
            "question": "Are curl and f150-f090 retained as adequate mandatory null-control channels for any later replay?",
            "allowed_answers": "accept;accept_with_caveat;reject",
            "reviewer_answer": "",
            "reviewer_notes": "",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_AUTHORIZATION_V1",
            "question_id": "Q5_replay_permission",
            "question": "May this candidate proceed to a separate guarded replay, without treating the package as validation or a physical path-weight derivation?",
            "allowed_answers": "authorize_replay_as_caveated_candidate;do_not_authorize_replay",
            "reviewer_answer": "",
            "reviewer_notes": "",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(TEMPLATE, rows)
    write_csv(
        TEMPLATE_SUMMARY,
        [
            {
                "package_id": PACKAGE_ID,
                "status": "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED",
                "question_count": str(len(rows)),
                "review_completed": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": "act_dr6_lensing_path_weight_review_template_ready_not_completed",
            }
        ],
    )
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# ACT DR6 lensing path-weight replay authorization review v1",
                "",
                "This package is for an external reviewer who does not have repository access.",
                "The reviewer should decide whether the ACT DR6 source-side path-weight",
                "candidate may proceed to a separate guarded replay.",
                "",
                "Review boundaries:",
                "",
                "- The package is not endpoint replay.",
                "- The package is not empirical validation.",
                "- The candidate is unitless and source-side; it is not a physical metric/lensing path-weight derivation.",
                "- Curl and f150-f090 difference channels must remain null controls in any later replay.",
                "- Endpoint residuals, endpoint scores, and fit statistics are forbidden inputs for this review.",
                "",
                f"Claim boundary: `{CLAIM_BOUNDARY}`.",
                "",
                "The reviewer should fill only the `reviewer_answer` and `reviewer_notes` columns",
                "in the response template, then return the completed CSV.",
                "",
            ]
        )
    )


def main() -> None:
    build_template()
    rows = [manifest_row(rel) for rel in PACKAGE_FILES]
    write_csv(MANIFEST, rows)
    package_rows = rows + [manifest_row(str(MANIFEST.relative_to(ROOT)))]
    OUT_ZIP.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for row in package_rows:
            path = ROOT / row["package_path"]
            info = zipfile.ZipInfo(row["package_path"])
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    zip_sha256 = sha256(OUT_ZIP)
    OUT_ZIP_SHA256.write_text(f"{zip_sha256}  {OUT_ZIP.name}\n")
    write_csv(
        SUMMARY,
        [
            {
                "package_id": PACKAGE_ID,
                "status": "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED",
                "zip_path": str(OUT_ZIP.relative_to(ROOT)),
                "zip_sha256_path": str(OUT_ZIP_SHA256.relative_to(ROOT)),
                "zip_sha256": zip_sha256,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "physical_lensing_path_weight_claimed": "false",
                "recommended_next_action": "send_zip_to_reviewer_and_validate_completed_authorization_response",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": "act_dr6_lensing_path_weight_authorization_package_ready_not_completed",
            }
        ],
    )
    print(
        "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_AUTHORIZATION_PACKAGE_V1_BUILT "
        "verdict=act_dr6_lensing_path_weight_authorization_package_ready_not_completed"
    )


if __name__ == "__main__":
    main()
