#!/usr/bin/env python3
from __future__ import annotations

import csv
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_time_route_closure_status_policy_v1.csv"
ROW4 = ROOT / "data/derived/paper10_desi_row4_window_decision_gate_v1_summary.csv"
ROW5 = ROOT / "data/derived/paper10_desi_row5_high_z_decision_gate_v1_summary.csv"
NEGATIVE_CONTROL = ROOT / "data/derived/paper10_desi_time_level_negative_control_response_gate_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_time_route_closure_status_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_time_route_closure_status_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_time_route_closure_status_not_validation"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the DESI time-route source-closure status gate.")
    parser.add_argument("--policy", default=str(POLICY))
    parser.add_argument("--row4", default=str(ROW4))
    parser.add_argument("--row5", default=str(ROW5))
    parser.add_argument("--negative-control", default=str(NEGATIVE_CONTROL))
    parser.add_argument("--out", default=str(OUT))
    parser.add_argument("--summary-out", default=str(SUMMARY))
    return parser.parse_args()


def resolve_path(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    return path


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
    args = parse_args()
    policy_path = resolve_path(args.policy)
    row4_path = resolve_path(args.row4)
    row5_path = resolve_path(args.row5)
    negative_path = resolve_path(args.negative_control)
    out_path = resolve_path(args.out)
    summary_path = resolve_path(args.summary_out)
    policy = one_row(policy_path)
    row4 = one_row(row4_path)
    row5 = one_row(row5_path)
    negative = one_row(negative_path)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad closure claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")
        if row4[field] != "false":
            raise SystemExit(f"row4 {field} must remain false")
        if row5[field] != "false":
            raise SystemExit(f"row5 {field} must remain false")
        if negative[field] != "false":
            raise SystemExit(f"negative-control {field} must remain false")

    row4_ready = row4["source_reopen_caveated"] == "true" and row4["review_completed"] == "true"
    row5_ready = row5["source_reopen"] == "true" and row5["review_completed"] == "true"
    negative_route_status = negative.get("route_status", "")
    negative_control_blocks = "BLOCKED" in negative_route_status or "blocks_replay" in negative.get("verdict", "")

    if row4["gate_status"] == "ROW4_WINDOW_REVIEW_PENDING_NOT_REPLAY":
        row4_status = "ROW4_PENDING_EXTERNAL_WINDOW_REVIEW"
    elif row4_ready:
        row4_status = "ROW4_CAVEATED_SOURCE_REOPENED_REPLAY_REVIEW_STILL_REQUIRED"
    else:
        row4_status = "ROW4_BLOCKER_REMAINS"

    if row5["gate_status"] == "ROW5_HIGH_Z_REVIEW_PENDING_NOT_REPLAY":
        row5_status = "ROW5_PENDING_EXTERNAL_HIGH_Z_REVIEW"
    elif row5_ready:
        row5_status = "ROW5_SOURCE_REOPENED_REPLAY_REVIEW_STILL_REQUIRED"
    else:
        row5_status = "ROW5_HIGH_Z_CLOCK_SUPPORT_MISSING"

    if row4_ready and row5_ready and not negative_control_blocks:
        closure_status = "DESI_TIME_ROUTE_SOURCE_READY_BUT_REPLAY_REVIEW_REQUIRED"
        verdict = "desi_time_route_source_ready_replay_review_required_not_validation"
        next_action = "prepare_separate_endpoint_replay_authorization_package"
    else:
        closure_status = "DESI_TIME_ROUTE_CLOSED_PENDING_SOURCE_BLOCKERS_NOT_REPLAY"
        verdict = "desi_time_route_closed_pending_row4_or_row5_or_richer_clock_readout_support"
        next_action = "resolve_row4_window_review_and_row5_high_z_clock_support_before_any_replay"

    row = {
        "closure_id": policy["closure_id"],
        "closure_status": closure_status,
        "row4_gate_status": row4["gate_status"],
        "row4_status": row4_status,
        "row4_review_completed": row4["review_completed"],
        "row4_source_reopen_caveated": row4["source_reopen_caveated"],
        "row5_gate_status": row5["gate_status"],
        "row5_verdict": row5["verdict"],
        "row5_status": row5_status,
        "negative_control_verdict": negative["verdict"],
        "negative_control_blocks_replay": "true" if negative_control_blocks else "false",
        "row4_can_enter_replay": "false",
        "row5_can_enter_replay": row5["row5_can_enter_replay"],
        "desi_time_route_endpoint_ready": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": verdict,
        "recommended_next_action": next_action,
    }
    write_csv(out_path, [row])
    write_csv(
        summary_path,
        [
            {
                "closure_id": policy["closure_id"],
                "status": "DESI_TIME_ROUTE_CLOSURE_STATUS_BUILT_NOT_REPLAY_NOT_VALIDATION",
                **row,
            }
        ],
    )
    print(f"PAPER10_DESI_TIME_ROUTE_CLOSURE_STATUS_BUILT closure_status={closure_status}")


if __name__ == "__main__":
    main()
