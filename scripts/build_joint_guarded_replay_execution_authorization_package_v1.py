#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/joint_guarded_replay_execution_authorization_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_guarded_replay_execution_authorization_response_template_v1.csv"
SUMMARY = ROOT / "data/derived/joint_guarded_replay_execution_authorization_package_v1_summary.csv"
MANIFEST = ROOT / "data/derived/joint_guarded_replay_execution_authorization_package_v1_manifest.csv"
PACKAGE = ROOT / "data/derived/joint_guarded_replay_execution_authorization_package_v1.zip"
SHA = ROOT / "data/derived/joint_guarded_replay_execution_authorization_package_v1.zip.sha256"
DOC = ROOT / "docs/joint_guarded_replay_execution_authorization_package_v1.md"
PLAN = ROOT / "data/source_manifest/joint_guarded_replay_execution_plan_v1.csv"
PLAN_SUMMARY = ROOT / "data/derived/joint_guarded_replay_execution_plan_v1_summary.csv"
RUNNER = ROOT / "scripts/run_joint_guarded_replay_permission_only_v1.py"
RUNNER_VALIDATOR = ROOT / "scripts/validate_joint_guarded_replay_permission_only_v1.py"
BLOCKER = ROOT / "data/derived/joint_guarded_replay_execution_blocker_status_v1_summary.csv"
CLAIM_BOUNDARY = "joint_guarded_replay_execution_authorization_not_validation"
PACKAGE_ID = "JOINT_GUARDED_REPLAY_EXECUTION_AUTHORIZATION_PACKAGE_V1"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
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


def main() -> None:
    plan = read_one(PLAN)
    plan_summary = read_one(PLAN_SUMMARY)
    blocker = read_one(BLOCKER)
    if plan_summary["status"] != "JOINT_GUARDED_REPLAY_EXECUTION_PLAN_READY_NOT_RUN":
        raise SystemExit("execution plan must be ready-not-run")
    if plan_summary["runner_exists"] != "true":
        raise SystemExit("runner and validator must exist before execution authorization package")
    if blocker["current_blocker"] != "execution_authorization_response_missing":
        raise SystemExit("execution blocker is not waiting for execution authorization")
    for row, label in [(plan, "plan"), (plan_summary, "plan_summary")]:
        for field in ["direct_execution_allowed", "endpoint_scoring_allowed", "endpoint_validation_claimed", "cosmological_validation_claimed"]:
            if row[field] != "false":
                raise SystemExit(f"{label}: unsafe field {field}")

    forbidden = plan["forbidden_inputs"]
    rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "JGRE_Q1_EXECUTION_SCOPE",
            "question": "May the prepared runner be executed once as a permission-only replay under the frozen execution plan?",
            "required_response": "authorize_permission_only_execution_or_reject",
            "acceptance_condition": "Authorize only one permission-only replay; no endpoint, cosmological, or physical validation claim is allowed.",
            "forbidden_inputs": forbidden,
            "permission_only_execution_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "JGRE_Q2_RUNNER_GUARD",
            "question": "Does the runner require this completed authorization response before producing outputs?",
            "required_response": "accept_runner_guard_or_reject",
            "acceptance_condition": "Accept only if the runner fails closed without an imported authorization summary.",
            "forbidden_inputs": forbidden,
            "permission_only_execution_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "JGRE_Q3_CONTROL_AND_CAVEAT_BINDING",
            "question": "Are the same controls, statistic, block weights, and caveats retained by the runner?",
            "required_response": "accept_same_controls_and_caveats_or_reject",
            "acceptance_condition": "Accept only if the runner keeps the frozen block order, shared statistic/weights, control suite, and caveats.",
            "forbidden_inputs": forbidden,
            "permission_only_execution_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "JGRE_Q4_NO_VALIDATION",
            "question": "Must the output remain permission-only and not validation?",
            "required_response": "accept_permission_only_no_validation_or_reject",
            "acceptance_condition": "Accept only if the result is not endpoint validation, cosmological validation, or physical proof.",
            "forbidden_inputs": forbidden,
            "permission_only_execution_allowed": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_rows(POLICY, rows)
    template_rows = []
    for row in rows:
        template_rows.append(
            {
                **row,
                "review_completed": "false",
                "reviewer_id_or_role": "",
                "reviewer_response": "",
                "reviewer_rationale": "",
                "forbidden_inputs_used": "false",
            }
        )
    write_rows(TEMPLATE, template_rows)
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint guarded replay execution authorization package v1",
                "",
                "This package asks whether the prepared runner may be executed once as a",
                "permission-only replay.  It does not itself execute the runner.",
                "",
                "Any accepted result must remain permission-only, not endpoint validation,",
                "not cosmological validation, and not physical proof.",
                "",
                f"Claim boundary: `{CLAIM_BOUNDARY}`.",
                "",
            ]
        )
    )
    package_inputs = [POLICY, TEMPLATE, DOC, PLAN, PLAN_SUMMARY, RUNNER, RUNNER_VALIDATOR, BLOCKER]
    manifest_rows = []
    for path in package_inputs:
        manifest_rows.append(
            {
                "package_path": rel(path),
                "sha256": sha256(path),
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "permission_only_execution_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_rows(MANIFEST, manifest_rows)
    with zipfile.ZipFile(PACKAGE, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in package_inputs + [MANIFEST]:
            info = zipfile.ZipInfo(rel(path))
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    digest = sha256(PACKAGE)
    SHA.write_text(f"{digest}  {PACKAGE.name}\n")
    write_rows(
        SUMMARY,
        [
            {
                "run_id": PACKAGE_ID,
                "status": "JOINT_GUARDED_REPLAY_EXECUTION_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED",
                "package_path": rel(PACKAGE),
                "zip_sha256": digest,
                "package_file_count": str(len(package_inputs) + 1),
                "review_completed": "false",
                "permission_only_execution_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "verdict": "joint_guarded_replay_execution_authorization_package_ready_not_completed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_GUARDED_REPLAY_EXECUTION_AUTHORIZATION_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
