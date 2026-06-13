#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_row5_high_z_decision_gate_policy_v1.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/paper10_desi_row5_high_z_review_package_v1_summary.csv"
RESPONSE_SUMMARY = ROOT / "data/derived/paper10_desi_row5_high_z_review_response_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_row5_high_z_decision_gate_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_row5_high_z_decision_gate_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_row5_high_z_decision_gate_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = one_row(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad decision-gate claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    package = one_row(PACKAGE_SUMMARY)
    if package["status"] != "DESI_ROW5_HIGH_Z_REVIEW_PACKAGE_BUILT_NOT_COMPLETED":
        raise SystemExit("decision gate expects the row5 high-z review package")
    if package["desi_time_route_endpoint_ready"] != "false":
        raise SystemExit("package must not release the DESI time route")

    if RESPONSE_SUMMARY.exists():
        response = one_row(RESPONSE_SUMMARY)
        for field in ["row5_can_enter_replay", "endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
            if response[field] != "false":
                raise SystemExit(f"response summary {field} must remain false")
        source_reopen = response["source_reopen"] == "true"
        replay_review_required = response["replay_review_required_before_endpoint"] == "true"
        if source_reopen and replay_review_required:
            gate_status = "ROW5_SOURCE_REOPEN_REPLAY_REVIEW_REQUIRED_NOT_REPLAY"
            verdict = "row5_source_reopen_prepare_replay_review_only"
            next_action = "prepare_separate_replay_authorization_package_if_scientifically_warranted"
        elif source_reopen:
            gate_status = "ROW5_SOURCE_REOPEN_NO_REPLAY"
            verdict = "row5_source_reopen_no_replay"
            next_action = "record_source_reopen_keep_no_replay"
        else:
            gate_status = "ROW5_HIGH_Z_BLOCKER_REMAINS_NOT_REPLAY"
            verdict = "row5_high_z_blocker_remains_no_replay"
            next_action = "keep_row5_blocked_or_find_new_source"
        review_completed = "true"
        high_z_clock_source_decision = response["high_z_clock_source_decision"]
        source_native_time_readout_decision = response["source_native_time_readout_decision"]
        release_policy = response["release_policy"]
        row5_blocker_status = response["row5_blocker_status"]
    else:
        gate_status = "ROW5_HIGH_Z_REVIEW_PENDING_NOT_REPLAY"
        verdict = "row5_high_z_review_pending_no_replay"
        next_action = "wait_for_completed_external_row5_high_z_review_response"
        review_completed = "false"
        source_reopen = False
        replay_review_required = False
        high_z_clock_source_decision = "PENDING"
        source_native_time_readout_decision = "PENDING"
        release_policy = "PENDING"
        row5_blocker_status = "ROW5_HIGH_Z_REVIEW_PENDING"

    row = {
        "gate_id": policy["gate_id"],
        "gate_status": gate_status,
        "review_package_status": package["status"],
        "review_completed": review_completed,
        "high_z_clock_source_decision": high_z_clock_source_decision,
        "source_native_time_readout_decision": source_native_time_readout_decision,
        "release_policy": release_policy,
        "source_reopen": "true" if source_reopen else "false",
        "row5_blocker_status": row5_blocker_status,
        "replay_review_required_before_endpoint": "true" if replay_review_required else "false",
        "row5_can_enter_replay": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": verdict,
        "recommended_next_action": next_action,
    }
    write_csv(OUT, [row])
    write_csv(
        SUMMARY,
        [
            {
                "gate_id": policy["gate_id"],
                "status": "DESI_ROW5_HIGH_Z_DECISION_GATE_BUILT_NOT_REPLAY_NOT_VALIDATION",
                **row,
            }
        ],
    )
    print(f"PAPER10_DESI_ROW5_HIGH_Z_DECISION_GATE_BUILT gate_status={gate_status}")


if __name__ == "__main__":
    main()
