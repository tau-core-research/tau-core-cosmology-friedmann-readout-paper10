#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_null_control_theory_replay_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_theory_replay_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_theory_replay_v1_summary.csv"


EXPECTED = {
    "sky_rotation": 4,
    "tomographic_pair_shuffle": 1000,
    "wrong_channel_activation": 2,
    "web_path_sign_flip": 2,
}


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("null-control replay policy must remain endpoint disabled")
    if policy["current_control_scores_computed"] != "false":
        raise SystemExit("null-control replay policy must not compute scores")
    if summary["status"] != "KIDS1000_COSEBIS_NULL_CONTROL_THEORY_REPLAY_BUILT_NOT_SCORED":
        raise SystemExit("unexpected null-control replay status")
    if len(rows) != 1008 or summary["control_draw_count"] != "1008":
        raise SystemExit("null-control replay must contain 1008 controls")
    if summary["target_rows_per_control"] != "300":
        raise SystemExit("each null-control replay must target the 300-row vector")
    counts = {family: 0 for family in EXPECTED}
    digests = set()
    for row in rows:
        family = row["control_family"]
        if family not in EXPECTED:
            raise SystemExit(f"unexpected null-control family: {family}")
        counts[family] += 1
        if row["target_rows"] != "300":
            raise SystemExit("each replay row must describe a 300-row control vector")
        if len(row["vector_sha256"]) != 64:
            raise SystemExit("control replay digest must be sha256")
        digests.add(row["vector_sha256"])
        for numeric_key in ["vector_l2_norm", "vector_std"]:
            if float(row[numeric_key]) < 0:
                raise SystemExit(f"{numeric_key} must be non-negative")
        for key in [
            "contains_control_scores",
            "contains_predictions",
            "contains_residuals",
            "contains_fit_statistics",
            "uses_kids_data_vector_values",
            "uses_posterior_chains",
            "uses_posthoc_control_selection",
            "uses_posthoc_control_multiplicity",
            "endpoint_scoring_allowed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"rows must keep {key}=false")
        if row["contains_theory_vector"] != "true":
            raise SystemExit("null-control replay rows must contain control theory-vector digests")
    if counts != EXPECTED:
        raise SystemExit(f"unexpected replay family counts: {counts}")
    if int(summary["unique_control_digest_count"]) != len(digests):
        raise SystemExit("summary digest count mismatch")
    if len(digests) < 900:
        raise SystemExit("null-control replay should contain many nonidentical controls")
    for key in [
        "contains_control_scores",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_control_selection",
        "uses_posthoc_control_multiplicity",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
    if summary["contains_theory_vector"] != "true":
        raise SystemExit("summary must record control theory-vector digests")
    if summary["current_control_theory_replay_executed"] != "true":
        raise SystemExit("summary must record replay execution")
    for marker in [
        "kids_data_vector_values",
        "fit_improvement_flags",
        "posthoc_control_selection",
        "posthoc_control_multiplicity",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input: {marker}")
    print("PAPER10_KIDS1000_COSEBIS_NULL_CONTROL_THEORY_REPLAY_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
