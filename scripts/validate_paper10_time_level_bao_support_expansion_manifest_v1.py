#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/source_manifest/paper10_time_level_bao_support_expansion_manifest_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_time_level_bao_support_expansion_manifest_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_time_level_bao_support_expansion_manifest_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


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
    rows = read_rows(MANIFEST)
    require(len(rows) == 4, "manifest must contain one current route and three candidate routes")
    by_route = {row["route_id"]: row for row in rows}
    require("CURRENT_SDSS_DR16_MULTITRACER_RADIAL_BAO" in by_route, "current SDSS route missing")
    require(by_route["CURRENT_SDSS_DR16_MULTITRACER_RADIAL_BAO"]["current_row_count"] == "2", "current row count changed")
    candidate_routes = [
        route for route, row in by_route.items()
        if row["status"] == "CANDIDATE_SOURCE_ROUTE_PENDING_FETCH_FREEZE"
    ]
    require(len(candidate_routes) == 3, "expected three pending candidate expansion routes")
    for row in rows:
        require(row["endpoint_replay_allowed"] == "false", "endpoint replay must remain false")
        require(row["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
        require(row["physical_validation_claimed"] == "false", "physical validation must remain false")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")
        for field in ["z_eff"]:
            require(field in row["required_fields"], f"missing required field marker: {field}")
        if row["status"] == "CANDIDATE_SOURCE_ROUTE_PENDING_FETCH_FREEZE":
            for field in ["source_url_or_doi", "product_hash"]:
                require(field in row["required_fields"], f"missing required field marker: {field}")
        require(
            "uncertainty_or_covariance" in row["required_fields"]
            or "sigma_or_covariance" in row["required_fields"],
            "missing uncertainty/covariance field marker",
        )
        for forbidden in [
            "Pantheon_distance_residuals",
            "endpoint_scores",
            "late_time_fit_parameters",
            "posthoc_BAO_source_selection",
            "posthoc_redshift_bin_selection",
            "posthoc_rd_tuning",
        ]:
            require(forbidden in row["forbidden_inputs"], f"missing forbidden input: {forbidden}")

    summary = {
        "manifest_id": "PAPER10_TIME_LEVEL_BAO_SUPPORT_EXPANSION_MANIFEST_V1",
        "status": "BAO_SUPPORT_EXPANSION_MANIFEST_DECLARED_NOT_REPLAY_NOT_VALIDATION",
        "current_radial_bao_rows": by_route["CURRENT_SDSS_DR16_MULTITRACER_RADIAL_BAO"]["current_row_count"],
        "candidate_expansion_route_count": str(len(candidate_routes)),
        "protocol_target_min_independent_radial_bins": "4",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "bao_support_expansion_routes_declared_but_current_endpoint_still_two_point_blocked",
    }
    write_csv(SUMMARY, summary)
    print(f"PAPER10_TIME_LEVEL_BAO_SUPPORT_EXPANSION_MANIFEST_VALIDATED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()
