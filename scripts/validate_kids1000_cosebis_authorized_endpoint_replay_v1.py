#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "kids1000_cosebis_authorized_endpoint_replay_run_v1.csv"
AUTH = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_replay_authorization_review_response_v1_summary.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_authorized_endpoint_replay_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def finite_float(value: str, key: str) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise SystemExit(f"{key} must be finite")
    return out


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    manifest = read_one(MANIFEST)
    auth = read_one(AUTH)
    summary = read_one(SUMMARY)
    require(manifest["endpoint_replay_allowed"] == "true", "manifest must allow replay")
    require(manifest["endpoint_validation_claimed"] == "false", "manifest must not claim validation")
    require(auth["endpoint_replay_allowed"] == "true", "authorization must allow replay")
    require(auth["endpoint_validation_claimed"] == "false", "authorization must not claim validation")
    require(summary["status"] == "AUTHORIZED_ENDPOINT_REPLAY_COMPLETE_PERMISSION_ONLY", "unexpected replay status")
    require(summary["endpoint_replay_executed"] == "true", "replay must be marked executed")
    require(summary["endpoint_validation_claimed"] == "false", "replay must not claim validation")
    require(summary["forbidden_inputs_used_for_source_selection"] == "false", "replay must not use forbidden source-selection inputs")
    require(summary["claim_boundary"] == manifest["claim_boundary"], "claim boundary mismatch")
    delta = finite_float(summary["candidate_delta_chi2_vs_baseline"], "candidate_delta_chi2_vs_baseline")
    tail = finite_float(summary["plus_one_tail_fraction_chi2"], "plus_one_tail_fraction_chi2")
    require(0.0 < tail <= 1.0, "tail fraction must be in (0,1]")
    require(int(summary["null_control_count"]) == 1008, "expected 1008 null controls")
    for key in [
        "scoring_summary_sha256",
        "scoring_results_sha256",
        "scoring_grid_sha256",
        "scoring_null_controls_sha256",
        "scoring_residuals_sha256",
    ]:
        require(len(summary[key]) == 64, f"{key} must be a sha256 digest")
    print(
        "PAPER10_KIDS1000_COSEBIS_AUTHORIZED_ENDPOINT_REPLAY_V1_VALIDATED "
        f"delta_chi2={delta:.12g} tail_chi2={tail:.12g}"
    )


if __name__ == "__main__":
    main()

