#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "kids1000_cosebis_authorized_endpoint_replay_run_v1.csv"
AUTH = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_replay_authorization_review_response_v1_summary.csv"
SCORING_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_summary.csv"
SCORING_RESULTS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_results.csv"
SCORING_GRID = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_grid.csv"
SCORING_NULLS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_null_controls.csv"
SCORING_RESIDUALS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_residuals.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_authorized_endpoint_replay_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    manifest = read_one(MANIFEST)
    auth = read_one(AUTH)
    require(manifest["status"] == "AUTHORIZED_ENDPOINT_REPLAY_PERMISSION_ONLY", "unexpected replay manifest status")
    require(manifest["endpoint_replay_allowed"] == "true", "replay manifest must allow replay")
    require(manifest["endpoint_validation_claimed"] == "false", "replay manifest must not claim validation")
    require(
        auth["verdict"] == "endpoint_replay_authorized_permission_only_not_validation",
        "authorization summary must grant permission-only replay",
    )
    require(auth["endpoint_replay_allowed"] == "true", "authorization summary must allow replay")
    require(auth["endpoint_validation_claimed"] == "false", "authorization summary must not claim validation")
    require(auth["forbidden_inputs_used"] == "false", "authorization summary must keep forbidden inputs unused")

    run(["python", "scripts/run_kids1000_cosebis_endpoint_scoring_v1.py"])
    run(["python", "scripts/validate_kids1000_cosebis_endpoint_scoring_v1.py"])
    scoring = read_one(SCORING_SUMMARY)
    require(scoring["endpoint_validation_claimed"] == "false", "scoring summary must not claim validation")
    require(scoring["uses_kids_data_vector_values_for_source_selection"] == "false", "scoring must not leak data into source selection")
    require(scoring["uses_posthoc_selection"] == "false", "scoring must not use posthoc selection")

    summary = [
        {
            "replay_run_id": manifest["replay_run_id"],
            "status": "AUTHORIZED_ENDPOINT_REPLAY_COMPLETE_PERMISSION_ONLY",
            "parent_authorization_summary": manifest["parent_authorization_summary"],
            "parent_scoring_run": manifest["parent_scoring_run"],
            "selected_statistic": manifest["selected_statistic"],
            "candidate_delta_chi2_vs_baseline": scoring["candidate_delta_chi2_vs_baseline"],
            "candidate_delta_aic_vs_baseline": scoring["candidate_delta_aic_vs_baseline"],
            "candidate_rank_by_chi2": scoring["candidate_rank_by_chi2"],
            "candidate_rank_by_aic": scoring["candidate_rank_by_aic"],
            "plus_one_tail_fraction_chi2": scoring["plus_one_tail_fraction_chi2"],
            "plus_one_tail_fraction_aic": scoring["plus_one_tail_fraction_aic"],
            "null_control_count": scoring["null_control_count"],
            "endpoint_replay_executed": "true",
            "endpoint_validation_claimed": "false",
            "forbidden_inputs_used_for_source_selection": "false",
            "scoring_summary_sha256": sha256(SCORING_SUMMARY),
            "scoring_results_sha256": sha256(SCORING_RESULTS),
            "scoring_grid_sha256": sha256(SCORING_GRID),
            "scoring_null_controls_sha256": sha256(SCORING_NULLS),
            "scoring_residuals_sha256": sha256(SCORING_RESIDUALS),
            "verdict": "authorized_endpoint_replay_low_tail_signal_not_validation",
            "claim_boundary": manifest["claim_boundary"],
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_AUTHORIZED_ENDPOINT_REPLAY_V1_COMPLETE "
        f"delta_chi2={summary[0]['candidate_delta_chi2_vs_baseline']} "
        f"tail_chi2={summary[0]['plus_one_tail_fraction_chi2']} "
        "claim_boundary=permission_only_not_validation"
    )


if __name__ == "__main__":
    main()

