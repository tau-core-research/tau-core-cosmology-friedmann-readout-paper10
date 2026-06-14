#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_open_blocker_reviewer_handoff_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_open_blocker_reviewer_handoff_v1.zip.sha256"
SUMMARY = ROOT / "data/derived/joint_row_level_open_blocker_reviewer_handoff_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_open_blocker_reviewer_handoff_v1.md"

INPUTS = [
    ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_review_package_v1.zip",
    ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_review_package_v1.zip.sha256",
    ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_blocker_status_v1_summary.csv",
    ROOT / "docs/joint_row_level_cross_channel_control_alignment_blocker_status_v1.md",
    ROOT / "data/derived/joint_row_level_lambda_policy_review_package_v1.zip",
    ROOT / "data/derived/joint_row_level_lambda_policy_review_package_v1.zip.sha256",
    ROOT / "data/derived/joint_row_level_lambda_policy_blocker_status_v1_summary.csv",
    ROOT / "docs/joint_row_level_lambda_policy_blocker_status_v1.md",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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

    message = "\n".join(
        [
            "# Joint row-level open blocker reviewer handoff v1",
            "",
            "This handoff contains two independent, non-scoring reviewer packages.",
            "The reviewer does not need repository access.",
            "",
            "## What to review",
            "",
            "1. `joint_row_level_cross_channel_control_alignment_review_package_v1.zip`",
            "   - Review whether a residual-blind cross-channel control alignment is required.",
            "   - Review whether the proposed deterministic min-count index alignment is acceptable as a design.",
            "   - Do not authorize aligned control values, numeric `lambda_row`, or `T_joint` rescoring in this package.",
            "",
            "2. `joint_row_level_lambda_policy_review_package_v1.zip`",
            "   - Review whether any future `lambda_row` must be dimensionless.",
            "   - Review whether any future numeric `lambda_row` must be residual-blind.",
            "   - Do not authorize a numeric `lambda_row` or `T_joint` rescoring in this package.",
            "",
            "## Required boundary",
            "",
            "- No endpoint residuals.",
            "- No endpoint scores.",
            "- No fit-improvement feedback.",
            "- No posterior chains.",
            "- No post-score control ranks.",
            "- No endpoint validation claim.",
            "",
            "## Expected output",
            "",
            "Return the completed response CSV or ZIP from each inner package.",
            "The author-side import scripts will reject responses that authorize scoring, validation,",
            "numeric `lambda_row`, or aligned control values at this stage.",
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
    rows = [
        {
            "handoff_id": "JOINT_ROW_LEVEL_OPEN_BLOCKER_REVIEWER_HANDOFF_V1",
            "zip_path": rel(OUT),
            "zip_sha256": digest,
            "included_review_packages": "cross_channel_control_alignment;lambda_policy",
            "package_count": "2",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "numeric_lambda_authorized": "false",
            "aligned_control_values_authorized": "false",
            "t_joint_rescoring_authorized": "false",
            "verdict": "OPEN_BLOCKER_REVIEWER_HANDOFF_READY_NOT_SCORING",
            "next_required_action": "send_handoff_to_reviewer_and_import_completed_responses",
            "claim_boundary": "joint_row_level_open_blocker_handoff_not_scoring_not_validation",
        }
    ]
    write_csv(SUMMARY, rows)
    print(f"JOINT_ROW_LEVEL_OPEN_BLOCKER_REVIEWER_HANDOFF_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
