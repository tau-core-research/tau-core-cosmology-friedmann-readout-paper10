#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "data/source_manifest/paper10_time_level_rd_policy_selection_gate_v1.csv"
DIFF_SUMMARY = ROOT / "data/derived/paper10_bao_rd_cancelled_time_level_difference_audit_v1_summary.csv"
SUMMARY = ROOT / "data/derived/paper10_time_level_rd_policy_selection_gate_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_time_level_rd_policy_selection_gate_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(GATE)
    diff = read_one(DIFF_SUMMARY)
    require(len(rows) == 4, "rd policy gate must contain exactly four policy options")
    require(diff["verdict"] == "rd_cancels_direction_agrees_but_bao_delta_low_significance_not_endpoint", "bad differential parent")

    by_option = {row["policy_option"]: row for row in rows}
    required = {
        "rd_cancelled_differential_direction",
        "external_rd_prior",
        "analytic_rd_marginalization",
        "fit_rd_from_pantheon_residuals",
    }
    require(set(by_option) == required, "unexpected rd policy options")
    for row in rows:
        require(row["status"] == "SOURCE_SIDE_RD_POLICY_SELECTION_NOT_REPLAY_NOT_VALIDATION", "bad status")
        require(row["route_id"] == "time_level_route", "bad route id")
        require(row["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
        require(row["physical_validation_claimed"] == "false", "physical validation must remain false")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")
        forbidden = row["forbidden_inputs"]
        for marker in ["distance_residuals", "fit_statistics", "endpoint_scores", "late_time_fit_parameters"]:
            require(marker in forbidden, f"missing forbidden marker {marker}")

    current = by_option["rd_cancelled_differential_direction"]
    require(current["policy_status"] == "ACCEPT_CURRENT_SOURCE_SIDE_ONLY", "current differential policy not accepted")
    require(current["endpoint_replay_allowed"] == "false", "current differential route must not allow endpoint replay")
    require("two_point_directional_level_check" in current["allowed_current_use"], "current allowed use too broad")

    external = by_option["external_rd_prior"]
    require(external["policy_status"] == "FUTURE_ROUTE_PENDING_SOURCE_FREEZE", "external rd prior must remain pending")
    require(external["required_source_artifact"].endswith("paper10_external_rd_prior_freeze_v1.csv"), "bad external prior artifact")
    require(external["endpoint_replay_allowed"] == "false", "external prior route must not allow endpoint replay yet")

    marginal = by_option["analytic_rd_marginalization"]
    require(marginal["policy_status"] == "FUTURE_ROUTE_PENDING_PROTOCOL_FREEZE", "marginalization route must remain pending")
    require(marginal["required_source_artifact"].endswith("paper10_bao_rd_marginalization_protocol_v1.csv"), "bad marginalization artifact")
    require(marginal["endpoint_replay_allowed"] == "false", "marginalization route must not allow endpoint replay yet")

    forbidden = by_option["fit_rd_from_pantheon_residuals"]
    require(forbidden["policy_status"] == "FORBIDDEN", "residual rd fit must be forbidden")
    require(forbidden["endpoint_replay_allowed"] == "true", "forbidden option must explicitly mark replay leakage")
    require("fitted_rd_from_pantheon" in forbidden["forbidden_inputs"], "residual rd forbidden marker missing")

    summary = {
        "policy_id": rows[0]["policy_id"],
        "status": "SOURCE_SIDE_RD_POLICY_SELECTION_VALIDATED_NOT_REPLAY_NOT_VALIDATION",
        "accepted_current_policy": "rd_cancelled_differential_direction",
        "future_pending_policies": "external_rd_prior;analytic_rd_marginalization",
        "forbidden_policy": "fit_rd_from_pantheon_residuals",
        "current_endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "rd_cancelled_direction_only_currently_allowed_external_or_marginalized_rd_pending",
    }
    write_csv(SUMMARY, [summary])
    print(
        "PAPER10_TIME_LEVEL_RD_POLICY_SELECTION_GATE_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
