#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = (
    ROOT
    / "data"
    / "source_manifest"
    / "void_source_basis_refinement_v2_sky_z_replay_authorization_review_policy_v1.csv"
)
FOLLOWUP_PACKAGE_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_observer_dependence_followup_package_v1_summary.csv"
)
SKY_FAMILY_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_sky_environment_screen_v1_family_summary.csv"
)
TEMPLATE = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_template_v1.csv"
)
SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_sky_z_replay_authorization_review_template_v1_summary.csv"
)
CLAIM_BOUNDARY = "v2_sky_z_replay_authorization_review_not_validation"
AUTH_SCOPE = "single_permission_only_12_row_W_path_x_sky_z_replay_not_validation"


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


def sky_z_row() -> dict[str, str]:
    rows = read_rows(SKY_FAMILY_SUMMARY)
    matches = [row for row in rows if row["family_id"] == "W_path_x_sky_z"]
    if len(matches) != 1:
        raise SystemExit("sky/environment family summary must contain exactly one W_path_x_sky_z row")
    return matches[0]


def main() -> None:
    policy_rows = read_rows(POLICY)
    followup = read_one(FOLLOWUP_PACKAGE_SUMMARY)
    sky_z = sky_z_row()
    if len(policy_rows) != 4:
        raise SystemExit("sky-z replay authorization policy must contain four rows")
    if followup["status"] != "V2_OBSERVER_DEPENDENCE_FOLLOWUP_PACKAGE_BUILT_NOT_COMPLETED":
        raise SystemExit("sky-z replay authorization requires the observer-dependence follow-up package")
    if followup["followup_family"] != "W_path_x_sky_z":
        raise SystemExit("observer-dependence follow-up must target W_path_x_sky_z")
    if followup["endpoint_replay_allowed"] != "false":
        raise SystemExit("observer-dependence follow-up package must not itself authorize replay")
    if followup["endpoint_validation_claimed"] != "false":
        raise SystemExit("observer-dependence follow-up package must not claim validation")
    if sky_z["survives_family_controls"] != "true":
        raise SystemExit("W_path_x_sky_z must survive its own family controls before authorization")
    if sky_z["controls_better_than_candidate_chi2"] != "0":
        raise SystemExit("W_path_x_sky_z must have zero better family controls before authorization")

    template_rows = []
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
                "authorization_scope": AUTH_SCOPE,
                "followup_family": followup["followup_family"],
                "followup_verdict": followup["verdict"],
                "sky_z_family_survives_controls": sky_z["survives_family_controls"],
                "claim_boundary": row["claim_boundary"],
            }
        )
    write_csv(TEMPLATE, template_rows)
    summary = [
        {
            "policy_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_SKY_Z_REPLAY_AUTHORIZATION_REVIEW_POLICY_V1",
            "status": "V2_SKY_Z_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED",
            "template_path": str(TEMPLATE.relative_to(ROOT)),
            "question_count": str(len(template_rows)),
            "followup_family": followup["followup_family"],
            "followup_verdict": followup["verdict"],
            "family_survives_controls": sky_z["survives_family_controls"],
            "controls_better_than_candidate_chi2": sky_z["controls_better_than_candidate_chi2"],
            "review_completed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_SKY_Z_REPLAY_AUTHORIZATION_TEMPLATE_V1_BUILT "
        "review_completed=false endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
