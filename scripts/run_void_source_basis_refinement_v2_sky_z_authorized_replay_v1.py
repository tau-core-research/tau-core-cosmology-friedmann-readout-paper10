#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = (
    ROOT
    / "data"
    / "source_manifest"
    / "void_source_basis_refinement_v2_sky_z_authorized_replay_run_v1.csv"
)
AUTH_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1_summary.csv"
)
SCREEN_GRID = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_sky_environment_screen_v1_grid.csv"
)
SCREEN_FAMILY_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_sky_environment_screen_v1_family_summary.csv"
)
GRID = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_sky_z_authorized_replay_v1_grid.csv"
)
SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_sky_z_authorized_replay_v1_summary.csv"
)
CLAIM_BOUNDARY = "v2_sky_z_authorized_replay_permission_only_not_validation"
SOURCE_CLAIM_BOUNDARY = "v2_path_sky_environment_screen_not_endpoint_not_validation"
FAMILY_ID = "W_path_x_sky_z"


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
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def best(rows: list[dict[str, str]], branch: str | None = None) -> dict[str, str]:
    scope = rows if branch is None else [row for row in rows if row["branch"] == branch]
    if not scope:
        raise SystemExit(f"missing replay branch: {branch}")
    return min(scope, key=lambda row: float(row["chi2_sky_z_replay"]))


def main() -> None:
    run = read_one(RUN_MANIFEST)
    auth = read_one(AUTH_SUMMARY)
    family_rows = read_rows(SCREEN_FAMILY_SUMMARY)
    if run["status"] != "V2_SKY_Z_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION":
        raise SystemExit("sky-z replay run status mismatch")
    if run["active_family"] != FAMILY_ID:
        raise SystemExit("sky-z replay run active family mismatch")
    if auth["decision"] != "GO_SKY_Z_REPLAY_PERMISSION_ONLY":
        raise SystemExit("sky-z replay is not authorized")
    if auth["endpoint_replay_allowed"] != "true" or auth["endpoint_validation_claimed"] != "false":
        raise SystemExit("authorization summary must be permission-only and non-validation")
    if auth["physical_lensing_path_weight_claimed"] != "false":
        raise SystemExit("authorization must not claim physical lensing-path weight")
    for marker in [
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
    ]:
        if marker not in run["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden marker: {marker}")
    family = [row for row in family_rows if row["family_id"] == FAMILY_ID]
    if len(family) != 1:
        raise SystemExit("family summary must contain exactly one W_path_x_sky_z row")
    if family[0]["survives_family_controls"] != "true":
        raise SystemExit("W_path_x_sky_z must survive family controls")
    if family[0]["controls_better_than_candidate_chi2"] != "0":
        raise SystemExit("W_path_x_sky_z must have zero better family controls")

    screen_rows = [
        row
        for row in read_rows(SCREEN_GRID)
        if row["family_id"] in {FAMILY_ID, "baseline_flat_lcdm"}
    ]
    if not screen_rows:
        raise SystemExit("missing screen rows for sky-z replay")
    replay_rows: list[dict[str, str]] = []
    for row in screen_rows:
        if row["claim_boundary"] != SOURCE_CLAIM_BOUNDARY:
            raise SystemExit("source screen claim boundary mismatch")
        replay_rows.append(
            {
                "run_id": run["run_id"],
                "source_screen_id": row["screen_id"],
                "family_id": row["family_id"],
                "branch": row["branch"],
                "omega_m": row["omega_m"],
                "omega_coupling": row["omega_coupling"],
                "offset": row["offset"],
                "chi2_sky_z_replay": row["chi2_screen"],
                "aic_sky_z_replay": row["aic_screen"],
                "n_rows": row["n_rows"],
                "k_eff": row["k_eff"],
                "normalization_rule": row["normalization_rule"],
                "source_claim_boundary": row["claim_boundary"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(GRID, replay_rows)

    baseline = best([row for row in replay_rows if row["family_id"] == "baseline_flat_lcdm"])
    candidate_rows = [row for row in replay_rows if row["family_id"] == FAMILY_ID]
    candidate = best(candidate_rows, "candidate")
    controls = [row for row in candidate_rows if row["branch"] != "candidate"]
    best_control = best(controls)
    better_controls = [
        row for row in controls if float(row["chi2_sky_z_replay"]) < float(candidate["chi2_sky_z_replay"])
    ]
    candidate_rank = 1 + len(
        [
            row
            for row in controls
            if float(row["chi2_sky_z_replay"]) < float(candidate["chi2_sky_z_replay"])
        ]
    )
    summary = [
        {
            "run_id": run["run_id"],
            "status": run["status"],
            "authorization_decision": auth["decision"],
            "active_family": FAMILY_ID,
            "n_rows": candidate["n_rows"],
            "grid_rows": str(len(replay_rows)),
            "baseline_best_chi2_sky_z_replay": baseline["chi2_sky_z_replay"],
            "baseline_best_aic_sky_z_replay": baseline["aic_sky_z_replay"],
            "baseline_best_omega_m": baseline["omega_m"],
            "candidate_best_chi2_sky_z_replay": candidate["chi2_sky_z_replay"],
            "candidate_best_aic_sky_z_replay": candidate["aic_sky_z_replay"],
            "candidate_best_omega_m": candidate["omega_m"],
            "candidate_best_omega_coupling": candidate["omega_coupling"],
            "best_control_branch": best_control["branch"],
            "best_control_chi2_sky_z_replay": best_control["chi2_sky_z_replay"],
            "best_control_aic_sky_z_replay": best_control["aic_sky_z_replay"],
            "delta_chi2_candidate_minus_baseline": f"{float(candidate['chi2_sky_z_replay']) - float(baseline['chi2_sky_z_replay']):.12g}",
            "delta_aic_candidate_minus_baseline": f"{float(candidate['aic_sky_z_replay']) - float(baseline['aic_sky_z_replay']):.12g}",
            "delta_chi2_candidate_minus_best_control": f"{float(candidate['chi2_sky_z_replay']) - float(best_control['chi2_sky_z_replay']):.12g}",
            "candidate_rank_by_chi2_among_candidate_and_controls": str(candidate_rank),
            "controls_better_than_candidate_chi2": str(len(better_controls)),
            "family_survives_controls": "true" if not better_controls else "false",
            "endpoint_replay_allowed": "true",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "disabled_channels": run["disabled_channels"],
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "sky_z_permission_replay_family_control_survives_not_validation"
            if not better_controls
            else "sky_z_permission_replay_not_control_resistant_not_validation",
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_SKY_Z_AUTHORIZED_REPLAY_V1_BUILT "
        f"verdict={summary[0]['verdict']} "
        f"delta_chi2_baseline={summary[0]['delta_chi2_candidate_minus_baseline']}"
    )


if __name__ == "__main__":
    main()
