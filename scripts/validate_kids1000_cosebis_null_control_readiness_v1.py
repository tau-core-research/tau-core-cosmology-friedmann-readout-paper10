#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_null_control_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_readiness_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_readiness_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    expected = {
        "sky_rotation",
        "tomographic_pair_shuffle",
        "wrong_channel_activation",
        "web_path_sign_flip",
    }
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("null-control policy must remain endpoint disabled")
    if policy["current_controls_executed"] != "false":
        raise SystemExit("the policy itself must remain declared-not-run")
    if len(rows) != int(policy["control_family_count"]):
        raise SystemExit("unexpected null-control family count")
    if {row["control_family"] for row in rows} != expected:
        raise SystemExit("unexpected null-control families")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("null-control readiness must remain endpoint disabled")
    if summary["status"] != "KIDS1000_COSEBIS_NULL_CONTROL_READINESS_BUILT_THEORY_REPLAY_NOT_SCORED":
        raise SystemExit("unexpected null-control readiness status")
    if summary["current_controls_executed"] != "true":
        raise SystemExit("null-control theory replay should be executed")
    if summary["contains_theory_vector"] != "true":
        raise SystemExit("null-control readiness should expose theory-vector control digests")
    if summary["contains_control_scores"] != "false":
        raise SystemExit("null-control readiness must not contain control scores")
    if summary["control_draw_count"] != "1008":
        raise SystemExit("null-control readiness should reference 1008 replay controls")
    for key in [
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_control_selection",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")
    for row in rows:
        if row["control_status"] != "THEORY_REPLAY_EXECUTED_NOT_SCORED":
            raise SystemExit("null-control rows must record replay execution")
        if row["current_control_executed"] != "true":
            raise SystemExit("null-control rows should mark replay execution")
        if row["contains_theory_vector"] != "true":
            raise SystemExit("null-control rows should expose control theory-vector digests")
        if row["requires_seed_policy"] != "true":
            raise SystemExit("each null-control family must require a seed policy")
        if row["requires_multiplicity_policy"] != "true":
            raise SystemExit("each null-control family must require a multiplicity policy")
        if row["target_rows"] != "300":
            raise SystemExit("null controls must target the full 300-row COSEBIs vector")
    for marker in [
        "posthoc_control_selection",
        "posthoc_control_multiplicity",
        "kids_data_vector_values",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input: {marker}")
    print("PAPER10_KIDS1000_COSEBIS_NULL_CONTROL_READINESS_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
