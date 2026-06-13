#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "source_manifest" / "act_dr6_lensing_path_weight_replay_run_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_replay_run_template_v1_summary.csv"
DOC = ROOT / "docs" / "act_dr6_lensing_path_weight_replay_run_template_v1.md"
CLAIM_BOUNDARY = "act_dr6_lensing_path_weight_replay_run_template_not_validation"


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    forbidden = [
        "distance_residual_driven_activation",
        "lensing_residual_driven_activation",
        "posthoc_sky_direction_selection",
        "posthoc_path_projection_labels",
        "posthoc_path_weight_tuning",
        "posthoc_row_selection",
        "posthoc_amplitude_tuning",
        "posthoc_covariance_reweighting",
        "endpoint_score_claims",
        "physical_lensing_path_weight_claims",
        "physical_validation_claims",
    ]
    rows = [
        {
            "run_id": "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_RUN_TEMPLATE_V1",
            "status": "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_PREPARED_AUTH_REQUIRED_NOT_VALIDATION",
            "active_channel_family": "ACT_DR6_LENSING_PATH_WEIGHT_CANDIDATE",
            "candidate_basis_path": "data/derived/act_dr6_lensing_path_weight_candidate_v1.csv",
            "authorization_summary_required": (
                "data/derived/act_dr6_lensing_path_weight_replay_authorization_review_response_v1_summary.csv"
            ),
            "omega_m_grid": "0.20:0.40:0.02",
            "omega_path_grid": "-0.20:0.20:0.02",
            "control_branches": "off;wrong_sign;curl_null;diff_f150_f090_null;deterministic_shuffle;rank_reverse",
            "disabled_channels": (
                "W_VOID_SOURCE_BASIS_REFINEMENT;W_WEB_ANISOTROPY;W_TIME;FULL_OBSERVER_PATH_KERNEL;"
                "PHYSICAL_LENSING_PATH_WEIGHT_CLAIM"
            ),
            "forbidden_inputs": ";".join(forbidden),
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(OUT, rows)
    write_csv(
        SUMMARY,
        [
            {
                "run_id": rows[0]["run_id"],
                "status": rows[0]["status"],
                "candidate_basis_path": rows[0]["candidate_basis_path"],
                "authorization_summary_required": rows[0]["authorization_summary_required"],
                "control_branch_count": str(len(rows[0]["control_branches"].split(";"))),
                "forbidden_input_count": str(len(forbidden)),
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": "act_dr6_lensing_path_weight_replay_template_ready_auth_required_not_validation",
            }
        ],
    )
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# ACT DR6 lensing path-weight replay run template v1",
                "",
                "This is a guarded replay template, not a replay execution.",
                "It freezes the candidate basis, authorization summary requirement,",
                "parameter grid, mandatory null-control branches, disabled channels,",
                "and forbidden inputs for a possible later permission-only replay.",
                "",
                "The template does not authorize endpoint replay and does not claim",
                "validation or a physical lensing path-weight derivation.",
                "",
                f"Claim boundary: `{CLAIM_BOUNDARY}`.",
                "",
            ]
        )
    )
    print(
        "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_RUN_TEMPLATE_V1_BUILT "
        "status=auth_required_not_validation"
    )


if __name__ == "__main__":
    main()
