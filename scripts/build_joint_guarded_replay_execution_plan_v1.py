#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/source_manifest/joint_guarded_replay_execution_plan_v1.csv"
SUMMARY = ROOT / "data/derived/joint_guarded_replay_execution_plan_v1_summary.csv"
DOC = ROOT / "docs/joint_guarded_replay_execution_plan_v1.md"
TEMPLATE = ROOT / "data/source_manifest/joint_guarded_replay_run_template_v1.csv"
TEMPLATE_AUTH_RESPONSE = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_response_v1_summary.csv"
BLOCKER = ROOT / "data/derived/joint_guarded_replay_execution_blocker_status_v1_summary.csv"
CLAIM_BOUNDARY = "joint_guarded_replay_execution_plan_not_run_not_scoring_not_validation"
RUNNER = ROOT / "scripts/run_joint_guarded_replay_permission_only_v1.py"
RUNNER_VALIDATOR = ROOT / "scripts/validate_joint_guarded_replay_permission_only_v1.py"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
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


def main() -> None:
    template = read_one(TEMPLATE)
    auth = read_one(TEMPLATE_AUTH_RESPONSE)
    blocker = read_one(BLOCKER)
    if auth["decision"] != "AUTHORIZE_JOINT_GUARDED_REPLAY_EXECUTION_PLAN_PREPARATION_ONLY_NOT_EXECUTION_NOT_SCORING_NOT_VALIDATION":
        raise SystemExit("run-template authorization response does not allow execution-plan preparation")
    if auth["next_action"] != "build_separate_executable_replay_plan_and_validator_before_any_run":
        raise SystemExit("run-template authorization response does not point to execution-plan preparation")
    if auth["template_authorized_for_later_permission_replay"] != "true":
        raise SystemExit("template is not authorized for later permission-only replay planning")
    if blocker["current_blocker"] not in {
        "execution_plan_builder_not_yet_prepared",
        "guarded_runner_and_execution_authorization_not_yet_prepared",
        "execution_authorization_response_missing",
    }:
        raise SystemExit("execution blocker is not at an execution-plan-compatible stage")
    for row, label in [(template, "template"), (auth, "authorization_response")]:
        for field in ["direct_execution_allowed", "endpoint_scoring_allowed", "endpoint_validation_claimed", "cosmological_validation_claimed"]:
            if row[field] != "false":
                raise SystemExit(f"{label}: unsafe field {field}")

    active_blocks = template["active_block_order"].split(";")
    controls = template["required_controls"].split(";")
    caveats = template["required_caveats"].split(";")
    forbidden = template["forbidden_inputs"].split(";")
    future_outputs = [
        "data/derived/joint_guarded_replay_permission_only_grid_v1.csv",
        "data/derived/joint_guarded_replay_permission_only_summary_v1.csv",
        "docs/joint_guarded_replay_permission_only_v1.md",
    ]
    runner_exists = RUNNER.exists() and RUNNER_VALIDATOR.exists()
    row = {
        "run_id": "JOINT_GUARDED_REPLAY_EXECUTION_PLAN_V1",
        "status": "JOINT_GUARDED_REPLAY_EXECUTION_PLAN_READY_NOT_RUN",
        "active_block_order": template["active_block_order"],
        "statistic_rule": template["statistic_rule"],
        "block_weight_rule": template["block_weight_rule"],
        "covariance_rule": template["covariance_rule"],
        "required_controls": template["required_controls"],
        "required_caveats": template["required_caveats"],
        "forbidden_inputs": template["forbidden_inputs"],
        "future_runner_script": "scripts/run_joint_guarded_replay_permission_only_v1.py",
        "future_validator_script": "scripts/validate_joint_guarded_replay_permission_only_v1.py",
        "future_outputs": ";".join(future_outputs),
        "execution_plan_only": "true",
        "runner_exists": "true" if runner_exists else "false",
        "direct_execution_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "next_required_action": "build_guarded_permission_only_runner_and_validator_then_get_separate_execution_authorization",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, [row])
    write_csv(
        SUMMARY,
        [
            {
                "run_id": row["run_id"],
                "status": row["status"],
                "active_block_count": str(len(active_blocks)),
                "required_control_count": str(len(controls)),
                "required_caveat_count": str(len(caveats)),
                "forbidden_input_count": str(len(forbidden)),
                "execution_plan_only": "true",
                "runner_exists": "true" if runner_exists else "false",
                "direct_execution_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "authorization_decision": auth["decision"],
                "verdict": "joint_guarded_replay_execution_plan_ready_not_run_not_scoring_not_validation",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint guarded replay execution plan v1",
                "",
                "This artifact is an execution-plan gate, not an executable replay.",
                "It creates no endpoint scores, no residuals, and no cosmological validation claim.",
                "",
                "It freezes the future runner/validator names, future output artifact names,",
                "active block order, identical statistic/weight/covariance/caveat discipline,",
                "and mandatory controls for a later permission-only replay.",
                "",
                "The future runner must not exist or run until a separate execution authorization",
                "gate is built, reviewed, imported, and validated.",
                "",
                "Required controls:",
                "",
                *[f"- `{item}`" for item in controls],
                "",
                "Required caveats:",
                "",
                *[f"- `{item}`" for item in caveats],
                "",
                f"Claim boundary: `{CLAIM_BOUNDARY}`.",
                "",
            ]
        )
    )
    print("JOINT_GUARDED_REPLAY_EXECUTION_PLAN_V1_BUILT status=ready_not_run")


if __name__ == "__main__":
    main()
