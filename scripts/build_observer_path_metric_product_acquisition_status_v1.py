#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENV_SUMMARY = ROOT / "data/derived/observer_path_metric_environment_product_v1_summary.csv"
REQ_REVIEW = ROOT / "data/derived/observer_path_metric_product_requirements_review_completed_summary_v1.csv"
OUT = ROOT / "data/derived/observer_path_metric_product_acquisition_status_v1.csv"
SUMMARY = ROOT / "data/derived/observer_path_metric_product_acquisition_status_v1_summary.csv"
DOC = ROOT / "docs/observer_path_metric_product_acquisition_status_v1.md"
CLAIM_BOUNDARY = "observer_path_metric_product_acquisition_status_not_endpoint_not_validation"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    env = read_one(ENV_SUMMARY)
    review = read_one(REQ_REVIEW)
    if review["decision"] != "ACCEPT_REQUIREMENTS_ONLY":
        raise SystemExit("requirements review must be accepted before acquisition status")
    if env["metric_environment_product_available_count"] != "12":
        raise SystemExit("metric-environment product must cover the 12-row scope")
    routes = [
        {
            "route_id": "caveated_metric_environment_path_proxy",
            "route_status": "AVAILABLE_SOURCE_ALIGNED_CAVEATED_PRODUCT",
            "source_aligned_numeric_product_count": env["metric_environment_product_available_count"],
            "physical_lensing_product_count": "0",
            "can_support_future_caveated_replay_authorization": "true",
            "can_support_physical_lensing_path_claim": "false",
            "next_action": "prepare_separate_replay_authorization_if_using_caveated_metric_environment_product",
        },
        {
            "route_id": "physical_kappa_shear_mass_map_product",
            "route_status": "STILL_MISSING",
            "source_aligned_numeric_product_count": "0",
            "physical_lensing_product_count": "0",
            "can_support_future_caveated_replay_authorization": "false",
            "can_support_physical_lensing_path_claim": "false",
            "next_action": "acquire_source_aligned_kappa_shear_or_mass_map_product",
        },
    ]
    for row in routes:
        row.update(
            {
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, routes)
    summary = [
        {
            "artifact_id": "OBSERVER_PATH_METRIC_PRODUCT_ACQUISITION_STATUS_V1",
            "status": "CAVEATED_METRIC_ENVIRONMENT_PRODUCT_AVAILABLE_PHYSICAL_LENSING_PRODUCT_MISSING",
            "requirements_review_decision": review["decision"],
            "observer_path_scope_rows": review["active_observer_path_scope_rows"],
            "caveated_metric_environment_product_count": env["metric_environment_product_available_count"],
            "physical_kappa_shear_mass_map_product_count": "0",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "CAVEATED_METRIC_ENVIRONMENT_DATA_ACQUIRED_BUT_PHYSICAL_LENSING_PATH_STILL_BLOCKED",
        }
    ]
    write_csv(SUMMARY, summary)
    DOC.write_text(
        "# Observer/path metric-product acquisition status v1\n\n"
        "**Doc class:** acquisition status gate\n"
        "**Status:** not endpoint replay; not validation\n\n"
        "The requirements-only reviewer response accepted the data requirement. "
        "A caveated source-aligned metric-environment path proxy has now been "
        "built for the active 12-row observer/path scope. This changes the data "
        "status from no source-aligned metric/path observable to a caveated "
        "metric-environment observable.\n\n"
        "It does not provide a physical kappa, shear, or mass-map product. "
        "Therefore the physical lensing-path route remains blocked, and any "
        "future use of the new product requires a separate replay-authorization "
        "package.\n\n"
        f"Verdict: `{summary[0]['verdict']}`.\n\n"
        f"Claim boundary: `{CLAIM_BOUNDARY}`.\n"
    )
    print(
        "OBSERVER_PATH_METRIC_PRODUCT_ACQUISITION_STATUS_V1_BUILT "
        f"caveated_count={summary[0]['caveated_metric_environment_product_count']} "
        f"physical_count={summary[0]['physical_kappa_shear_mass_map_product_count']}"
    )


if __name__ == "__main__":
    main()
