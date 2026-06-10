#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_v2_observer_dependence_followup_policy_v1.csv"
SKY_SCREEN_FAMILY = (
    ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_sky_environment_screen_v1_family_summary.csv"
)
SKY_SCREEN_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_sky_environment_screen_v1_summary.csv"
TEMPLATE = (
    ROOT / "data" / "derived" / "void_source_basis_refinement_v2_observer_dependence_followup_response_template_v1.csv"
)
SUMMARY = (
    ROOT / "data" / "derived" / "void_source_basis_refinement_v2_observer_dependence_followup_template_v1_summary.csv"
)
CLAIM_BOUNDARY = "v2_observer_dependence_followup_not_endpoint_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy_rows = read_rows(POLICY)
    screen_summary = read_one(SKY_SCREEN_SUMMARY)
    family_rows = read_rows(SKY_SCREEN_FAMILY)
    sky_z = [row for row in family_rows if row["family_id"] == "W_path_x_sky_z"]
    if len(policy_rows) != 4:
        raise SystemExit("observer-dependence follow-up policy must contain four questions")
    if screen_summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("sky/environment screen must not claim validation")
    if screen_summary["physical_lensing_path_weight_claimed"] != "false":
        raise SystemExit("sky/environment screen must not claim physical path weight")
    if len(sky_z) != 1 or sky_z[0]["survives_family_controls"] != "true":
        raise SystemExit("W_path_x_sky_z must survive family controls before follow-up template")

    template_rows: list[dict[str, str]] = []
    for row in policy_rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{row['question_id']}: claim boundary mismatch")
        template_rows.append(
            {
                "policy_id": row["policy_id"],
                "question_id": row["question_id"],
                "question_text": row["question_text"],
                "required_response": row["required_response"],
                "acceptance_condition": row["acceptance_condition"],
                "review_completed": "false",
                "reviewer_id_or_role": "",
                "reviewer_response": "",
                "reviewer_rationale": "",
                "forbidden_inputs_used": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "followup_family": "W_path_x_sky_z",
                "allowed_next_action": "prepare_separate_W_path_x_sky_z_replay_authorization_package_only",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(TEMPLATE, template_rows)
    summary = [
        {
            "policy_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_OBSERVER_DEPENDENCE_FOLLOWUP_POLICY_V1",
            "status": "V2_OBSERVER_DEPENDENCE_FOLLOWUP_TEMPLATE_READY_NOT_COMPLETED",
            "template_path": str(TEMPLATE.relative_to(ROOT)),
            "question_count": str(len(template_rows)),
            "source_screen": "V2_PATH_SKY_ENVIRONMENT_SCREEN_V1",
            "followup_family": "W_path_x_sky_z",
            "family_survives_controls": sky_z[0]["survives_family_controls"],
            "global_screen_verdict": screen_summary["verdict"],
            "review_completed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_OBSERVER_DEPENDENCE_FOLLOWUP_TEMPLATE_V1_BUILT "
        "followup_family=W_path_x_sky_z review_completed=false"
    )


if __name__ == "__main__":
    main()
