#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data/source_manifest/paper10_bao_rd_marginalization_protocol_v1.csv"
RD_POLICY = ROOT / "data/derived/paper10_time_level_rd_policy_selection_gate_v1_summary.csv"
SUMMARY = ROOT / "data/derived/paper10_bao_rd_marginalization_protocol_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_bao_rd_marginalization_protocol_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def write_csv(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


def main() -> None:
    row = read_one(PROTOCOL)
    rd_policy = read_one(RD_POLICY)

    require(row["status"] == "SOURCE_SIDE_RD_MARGINALIZATION_PROTOCOL_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(row["route_id"] == "time_level_route", "bad route")
    require(row["nuisance_parameter"] == "beta_rd", "bad nuisance parameter")
    require("beta_rd=log(r_d)-log(c)" in row["joint_interface"], "joint interface must define beta_rd")
    require("analytic_linear_nuisance_projection" in row["allowed_marginalization"], "analytic nuisance projection missing")
    require("matched_CC_logH_support" in row["required_inputs"], "CC support requirement missing")
    require("rd_prior_response_or_broad_beta_grid_policy" in row["required_inputs"], "rd prior/grid policy missing")
    for forbidden in [
        "Pantheon_distance_residuals",
        "fit_statistics",
        "endpoint_scores",
        "late_time_fit_parameters",
        "posthoc_rd_choice",
        "posthoc_beta_grid_from_endpoint",
        "BAO_support_for_clock_slope_claim",
    ]:
        require(forbidden in row["forbidden_inputs"], f"missing forbidden input: {forbidden}")
    for control in [
        "rd_off_control",
        "external_prior_width_stress",
        "wrong_prior_control",
        "BAO_pair_drop_control",
        "CC_match_window_stress",
    ]:
        require(control in row["required_controls"], f"missing control: {control}")
    require(row["endpoint_replay_allowed"] == "false", "endpoint replay must remain false")
    require(row["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
    require(row["physical_validation_claimed"] == "false", "physical validation must remain false")
    require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")
    require(
        "analytic_rd_marginalization" in rd_policy["future_pending_policies"],
        "rd policy gate must still list marginalization as a route",
    )

    summary = {
        "protocol_id": row["protocol_id"],
        "status": "RD_MARGINALIZATION_PROTOCOL_READY_NOT_REPLAY_NOT_VALIDATION",
        "route_id": row["route_id"],
        "nuisance_parameter": row["nuisance_parameter"],
        "protocol_blocker_closed": "joint_rd_marginalization_protocol_definition",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "rd_marginalization_protocol_frozen_but_endpoint_still_blocked",
    }
    write_csv(SUMMARY, summary)
    print(f"PAPER10_BAO_RD_MARGINALIZATION_PROTOCOL_VALIDATED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()
