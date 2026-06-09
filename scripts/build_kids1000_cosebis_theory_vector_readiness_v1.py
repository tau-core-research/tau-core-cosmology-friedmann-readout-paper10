#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_theory_vector_policy_v1.csv"
TOMO = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_mode_inventory_v1_summary.csv"
MASK = ROOT / "data" / "derived" / "kids1000_cosebis_mask_modecut_inventory_v1_summary.csv"
COV_INV = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_inversion_readiness_v1_summary.csv"
SOURCE_THEORY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_readiness_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_readiness_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    tomo = read_one(TOMO)
    mask = read_one(MASK)
    cov_inv = read_one(COV_INV)
    source_theory = read_one(SOURCE_THEORY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("COSEBIs theory-vector policy must remain endpoint disabled")
    if policy["current_theory_vector_computed"].lower() != "false":
        raise SystemExit("parent COSEBIs theory-vector policy must remain scoring-disabled and declarative")
    if source_theory["theory_vector_computed"] != "true":
        raise SystemExit("source-frozen theory-vector shell must be built before readiness can pass")
    if source_theory["endpoint_scoring_allowed"] != "false":
        raise SystemExit("source-frozen theory-vector shell must keep endpoint scoring disabled")
    if cov_inv["requires_frozen_theory_vector"].lower() != "true":
        raise SystemExit("covariance inversion readiness must require a frozen theory vector")
    expected_rows = policy["expected_theory_vector_rows"]
    if tomo["data_vector_rows"] != expected_rows or mask["retained_rows"] != expected_rows:
        raise SystemExit("COSEBIs theory-vector expected row count does not match retained data-vector rows")

    row = {
        "policy_id": policy["policy_id"],
        "parent_policy": policy["parent_policy"],
        "selected_statistic": policy["selected_statistic"],
        "expected_theory_vector_rows": expected_rows,
        "retained_data_vector_rows": mask["retained_rows"],
        "n_tomographic_pairs": tomo["n_tomographic_pairs"],
        "n_modes_per_pair": tomo["n_modes_per_pair"],
        "active_channels": policy["active_channels"],
        "disabled_channels": policy["disabled_channels"],
        "theory_vector_status": "computed_from_source_frozen_mapping",
        "current_theory_vector_computed": "true",
        "source_frozen_theory_vector_artifact": "data/derived/kids1000_cosebis_source_frozen_theory_vector_v1_summary.csv",
        "contains_theory_vector": "true",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": "kids1000_cosebis_theory_vector_readiness_not_validation",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)
    summary = dict(row)
    summary["status"] = "KIDS1000_COSEBIS_THEORY_VECTOR_READINESS_BUILT_SOURCE_FROZEN_NOT_SCORED"
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_THEORY_VECTOR_READINESS_V1_BUILT "
        f"rows={expected_rows} theory_vector_computed=true endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
