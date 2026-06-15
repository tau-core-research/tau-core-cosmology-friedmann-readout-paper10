#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_value_gate_reviewer_handoff_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_value_gate_reviewer_handoff_v1.zip.sha256"
SUMMARY = ROOT / "data/derived/joint_row_level_value_gate_reviewer_handoff_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_value_gate_reviewer_handoff_v1.md"
CLAIM_BOUNDARY = "joint_row_level_value_gate_handoff_not_scoring_not_validation"

INPUTS = [
    ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1.zip",
    ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1.zip.sha256",
    ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1_summary.csv",
    ROOT / "docs/joint_row_level_aligned_control_value_authorization_review_package_v1.md",
    ROOT / "data/derived/joint_row_level_numeric_lambda_review_package_v1.zip",
    ROOT / "data/derived/joint_row_level_numeric_lambda_review_package_v1.zip.sha256",
    ROOT / "data/derived/joint_row_level_numeric_lambda_review_package_v1_summary.csv",
    ROOT / "docs/joint_row_level_numeric_lambda_review_package_v1.md",
    ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_blocker_status_v1_summary.csv",
    ROOT / "data/derived/joint_row_level_lambda_policy_blocker_status_v1_summary.csv",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{rel(path)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    missing = [rel(path) for path in INPUTS if not path.exists()]
    if missing:
        raise SystemExit(f"missing required handoff inputs: {missing}")

    aligned_summary = read_one(
        ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1_summary.csv"
    )
    lambda_summary = read_one(ROOT / "data/derived/joint_row_level_numeric_lambda_review_package_v1_summary.csv")
    cca_blocker = read_one(ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_blocker_status_v1_summary.csv")
    lambda_blocker = read_one(ROOT / "data/derived/joint_row_level_lambda_policy_blocker_status_v1_summary.csv")

    if aligned_summary["contains_aligned_joint_control_values"] != "false":
        raise SystemExit("aligned-control package must not contain aligned values")
    if aligned_summary["t_joint_rescoring_authorized"] != "false":
        raise SystemExit("aligned-control package must not authorize rescoring")
    if lambda_summary["contains_lambda_row_numeric_value"] != "true":
        raise SystemExit("numeric-lambda package must contain lambda candidate")
    if lambda_summary["t_joint_rescoring_authorized"] != "false":
        raise SystemExit("numeric-lambda package must not authorize rescoring")
    if cca_blocker["verdict"] != "CROSS_CHANNEL_ALIGNMENT_DESIGN_ACCEPTED_VALUES_STILL_BLOCKED":
        raise SystemExit("cross-channel blocker is not in expected state")
    if lambda_blocker["verdict"] != "LAMBDA_POLICY_ACCEPTED_NUMERIC_VALUE_STILL_BLOCKED":
        raise SystemExit("lambda blocker is not in expected state")

    message = "\n".join(
        [
            "# Joint row-level value-gate reviewer handoff v1",
            "",
            "**Doc class:** reviewer handoff without repository access.",
            "**Status:** two value-gate packages; not scoring; not validation.",
            f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
            "",
            "This handoff contains two independent review packages that follow the",
            "completed open-blocker review. The reviewer does not need repository",
            "access.",
            "",
            "## Package 1: aligned-control value authorization",
            "",
            "`joint_row_level_aligned_control_value_authorization_review_package_v1.zip`",
            "",
            "Review question: may a later script compute aligned joint-control values",
            "using only the already accepted deterministic min-count rule and the",
            "already frozen channel-local penalty values?",
            "",
            "Boundary: this package contains no aligned joint-control values and does",
            "not authorize `lambda_row`, `T_joint` rescoring, endpoint scoring, or",
            "validation.",
            "",
            "## Package 2: numeric lambda candidate",
            "",
            "`joint_row_level_numeric_lambda_review_package_v1.zip`",
            "",
            "Review question: may `lambda_row = 1` be recorded as a dimensionless,",
            "residual-blind unit-weight candidate for a later rescoring-authorization",
            "package?",
            "",
            "Boundary: this package does not apply `lambda_row`, does not rescore",
            "`T_joint`, and does not authorize endpoint scoring or validation.",
            "",
            "## Forbidden inputs for both packages",
            "",
            "- endpoint residuals",
            "- endpoint scores",
            "- fit-improvement feedback",
            "- posterior chains",
            "- post-score control ranks",
            "",
            "## Expected output",
            "",
            "Return the completed response CSV or ZIP from each inner package. The",
            "author-side import scripts must reject any response that authorizes",
            "endpoint scoring or validation at this stage.",
            "",
        ]
    )
    DOC.write_text(message)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(DOC, rel(DOC))
        for path in INPUTS:
            zf.write(path, rel(path))

    digest = sha256(OUT)
    SHA.write_text(f"{digest}  {OUT.name}\n")
    write_csv(
        SUMMARY,
        [
            {
                "handoff_id": "JOINT_ROW_LEVEL_VALUE_GATE_REVIEWER_HANDOFF_V1",
                "zip_path": rel(OUT),
                "zip_sha256": digest,
                "included_review_packages": "aligned_control_value_authorization;numeric_lambda_candidate",
                "package_count": "2",
                "aligned_control_value_computation_authorized": "false",
                "numeric_lambda_authorized": "false",
                "t_joint_rescoring_authorized": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "verdict": "VALUE_GATE_REVIEWER_HANDOFF_READY_NOT_SCORING",
                "next_required_action": "send_handoff_to_reviewer_and_import_completed_responses",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_ROW_LEVEL_VALUE_GATE_REVIEWER_HANDOFF_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
