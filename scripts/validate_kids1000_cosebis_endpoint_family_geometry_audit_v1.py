#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_family_geometry_audit_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_family_geometry_audit_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_family_geometry_audit_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("endpoint-family geometry policy must remain endpoint disabled")
    if summary["status"] != "KIDS1000_COSEBIS_ENDPOINT_FAMILY_GEOMETRY_AUDIT_BUILT_NOT_SCORED":
        raise SystemExit("unexpected endpoint-family geometry audit status")
    if len(rows) != 1009 or summary["family_vector_count"] != "1009":
        raise SystemExit("endpoint-family geometry audit must contain candidate plus 1008 controls")
    if summary["target_rows"] != "300":
        raise SystemExit("endpoint-family geometry audit must target 300 rows")
    if int(summary["raw_effective_rank_tol_1e_minus_8"]) < 2:
        raise SystemExit("raw endpoint-family rank should be non-degenerate")
    if int(summary["covariance_metric_effective_rank_tol_1e_minus_8"]) < 2:
        raise SystemExit("covariance-metric endpoint-family rank should be non-degenerate")
    if summary["endpoint_family_geometry_passed"] != "true":
        raise SystemExit("endpoint-family geometry gate should pass")
    families = {row["vector_family"] for row in rows}
    if families != {
        "candidate",
        "sky_rotation",
        "tomographic_pair_shuffle",
        "wrong_channel_activation",
        "web_path_sign_flip",
    }:
        raise SystemExit("unexpected endpoint-family vector families")
    if sum(row["vector_family"] == "candidate" for row in rows) != 1:
        raise SystemExit("endpoint-family geometry audit must contain exactly one candidate")
    for key in [
        "contains_control_scores",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_selection",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")
    if summary["contains_theory_vector"] != "true":
        raise SystemExit("summary should expose source-frozen theory/control vectors")
    if summary["uses_kids_covariance_for_metric_only"] != "true":
        raise SystemExit("covariance use must be metric-only")
    for row in rows:
        if row["target_rows"] != "300":
            raise SystemExit("each family vector must target 300 rows")
        if len(row["vector_sha256"]) != 64:
            raise SystemExit("each family vector must include a sha256 digest")
        if row["uses_kids_covariance_for_metric_only"] != "true":
            raise SystemExit("row covariance use must be metric-only")
    for marker in [
        "kids_data_vector_values",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_weight_selection",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input: {marker}")
    print("PAPER10_KIDS1000_COSEBIS_ENDPOINT_FAMILY_GEOMETRY_AUDIT_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
