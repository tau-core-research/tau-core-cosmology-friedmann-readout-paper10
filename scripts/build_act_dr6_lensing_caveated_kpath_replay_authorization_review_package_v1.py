#!/usr/bin/env python3
"""Build the caveated ACT K_path replay-authorization review package.

This package follows the accepted source-design review.  It asks an external
reviewer whether a separate permission-only guarded replay may be prepared.  It
does not itself authorize replay, validation, or physical K_path promotion.
"""

from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
PACKAGE_ID = "ACT_DR6_LENSING_CAVEATED_KPATH_REPLAY_AUTHORIZATION_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "act_dr6_lensing_caveated_kpath_replay_authorization_review_not_validation"

TEMPLATE = DERIVED / "act_dr6_lensing_caveated_kpath_replay_authorization_review_response_template_v1.csv"
INSTRUCTIONS = DERIVED / "act_dr6_lensing_caveated_kpath_replay_authorization_review_instructions_v1.md"
OUT_ZIP = DERIVED / "act_dr6_lensing_caveated_kpath_replay_authorization_review_package_v1.zip"
OUT_ZIP_SHA256 = DERIVED / "act_dr6_lensing_caveated_kpath_replay_authorization_review_package_v1.zip.sha256"
MANIFEST = DERIVED / "act_dr6_lensing_caveated_kpath_replay_authorization_review_package_v1_manifest.csv"
SUMMARY = DERIVED / "act_dr6_lensing_caveated_kpath_replay_authorization_review_package_v1_summary.csv"

PACKAGE_FILES = [
    "data/source_manifest/act_dr6_lensing_caveated_kpath_source_design_v1.csv",
    "data/derived/act_dr6_lensing_caveated_kpath_source_design_v1_summary.csv",
    "data/derived/act_dr6_lensing_caveated_kpath_source_design_review_response_v1.csv",
    "data/derived/act_dr6_lensing_caveated_kpath_source_design_review_completed_summary_v1.csv",
    "data/derived/act_dr6_lensing_caveated_kpath_source_design_review_notes_v1.md",
    "data/source_manifest/act_dr6_lensing_next_source_basis_design_scaffold_v1.csv",
    "data/derived/act_dr6_lensing_next_source_basis_design_scaffold_v1_summary.csv",
    "data/derived/act_dr6_lensing_reopen_closure_ledger_v1_summary.csv",
    "data/derived/act_dr6_lensing_path_weight_candidate_v1_summary.csv",
    "data/derived/act_dr6_lensing_path_weight_authorized_replay_v1_summary.csv",
    "data/source_manifest/act_dr6_lensing_path_weight_replay_run_template_v1.csv",
    "data/derived/act_dr6_lensing_path_weight_replay_run_template_v1_summary.csv",
    "scripts/run_act_dr6_lensing_path_weight_authorized_replay_v1.py",
    "scripts/validate_act_dr6_lensing_path_weight_authorized_replay_v1.py",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def package_manifest_row(rel: str) -> dict[str, str]:
    path = ROOT / rel
    if not path.exists():
        raise SystemExit(f"missing caveated replay package input: {rel}")
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


def build_review_files() -> None:
    response_rows = [
        {
            "review_id": "ACT_DR6_LENSING_CAVEATED_KPATH_REPLAY_AUTHORIZATION_V1",
            "question_id": "Q1_source_design_acceptance",
            "question": (
                "Does the imported source-design response accept the ACT K_path design only as "
                "a caveated dimensionless source-side proxy?"
            ),
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
            "review_id": "ACT_DR6_LENSING_CAVEATED_KPATH_REPLAY_AUTHORIZATION_V1",
            "question_id": "Q2_controls_required",
            "question": (
                "Are off, baseline-only, curl-null, frequency-difference-null, wrong-sign, "
                "deterministic-shuffle, rank-reverse, and source-basis-recenter controls required "
                "for any replay?"
            ),
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
            "review_id": "ACT_DR6_LENSING_CAVEATED_KPATH_REPLAY_AUTHORIZATION_V1",
            "question_id": "Q3_old_branch_quarantine",
            "question": (
                "Is the previous ACT endpoint result kept as control-dominated/quarantined rather "
                "than used as evidence for the new replay?"
            ),
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
            "review_id": "ACT_DR6_LENSING_CAVEATED_KPATH_REPLAY_AUTHORIZATION_V1",
            "question_id": "Q4_forbidden_inputs",
            "question": (
                "Does the package forbid endpoint residuals, endpoint scores, fit statistics, "
                "fitted amplitudes, winner labels, post-hoc row dropping, and dropping the curl control?"
            ),
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
            "review_id": "ACT_DR6_LENSING_CAVEATED_KPATH_REPLAY_AUTHORIZATION_V1",
            "question_id": "Q5_permission_only_replay",
            "question": (
                "May a separate permission-only guarded replay package be prepared from this source "
                "design, without validation or physical K_path promotion?"
            ),
            "allowed_answers": "authorize_permission_only_replay_package;do_not_authorize",
            "reviewer_answer": "",
            "reviewer_notes": "",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(TEMPLATE, response_rows)
    INSTRUCTIONS.write_text(
        "\n".join(
            [
                "# ACT DR6 caveated K_path replay-authorization review v1",
                "",
                "The reviewer does not need repository access.",
                "",
                "This package follows a completed source-design review that accepted the ACT",
                "baseline kappa route only as a caveated, dimensionless K_path-shape proxy.",
                "The present review asks whether a separate permission-only guarded replay",
                "package may be prepared.",
                "",
                "This review cannot authorize validation, physical K_path promotion, a dark-sector",
                "claim, or a family verdict. It can only authorize preparation of a separate",
                "guarded replay package that retains all null controls.",
                "",
                "Allowed final answers for Q5:",
                "",
                "- authorize_permission_only_replay_package",
                "- do_not_authorize",
                "",
                f"Claim boundary: `{CLAIM_BOUNDARY}`.",
                "",
            ]
        )
    )


def main() -> None:
    build_review_files()
    package_rows = [package_manifest_row(rel) for rel in PACKAGE_FILES]
    package_rows.extend(
        [
            package_manifest_row(str(TEMPLATE.relative_to(ROOT))),
            package_manifest_row(str(INSTRUCTIONS.relative_to(ROOT))),
        ]
    )
    write_csv(MANIFEST, package_rows)

    zip_rows = package_rows + [package_manifest_row(str(MANIFEST.relative_to(ROOT)))]
    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for row in zip_rows:
            path = ROOT / row["package_path"]
            info = zipfile.ZipInfo(row["package_path"])
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())

    zip_hash = sha256(OUT_ZIP)
    OUT_ZIP_SHA256.write_text(f"{zip_hash}  {OUT_ZIP.name}\n")
    write_csv(
        SUMMARY,
        [
            {
                "package_id": PACKAGE_ID,
                "status": "CAVEATED_KPATH_REPLAY_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": str(OUT_ZIP.relative_to(ROOT)),
                "zip_sha256_path": str(OUT_ZIP_SHA256.relative_to(ROOT)),
                "zip_sha256": zip_hash,
                "package_file_count": str(len(zip_rows)),
                "source_design_review_decision": "ACCEPT_CAVEATED_KPATH_SOURCE_DESIGN_FOR_REVIEW_ONLY",
                "review_completed": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "future_permission_only_replay_package_authorization_pending": "true",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": "ACT_CAVEATED_KPATH_REPLAY_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED",
            }
        ],
    )


if __name__ == "__main__":
    main()
