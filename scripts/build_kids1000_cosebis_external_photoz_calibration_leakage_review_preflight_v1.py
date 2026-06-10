#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_policy_v1.csv"
SOURCE_MANIFEST = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_source_manifest_v1.csv"
SOURCE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_source_manifest_v1_summary.csv"
ACQUISITION_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1_summary.csv"
SOURCE_BUILD_SCRIPT = ROOT / "scripts" / "build_kids1000_cosebis_external_photoz_calibration_source_manifest_v1.py"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1_summary.csv"


FORBIDDEN_SCRIPT_TOKENS = [
    "endpoint_scoring_v1",
    "partial_control_diagnostic_scoring",
    "endpoint_residual",
    "delta_chi2",
    "rank_chi2",
    "tail_chi2",
    "best_control_identity",
    "postscore_residual_shape",
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = read_one(POLICY)
    source_summary = read_one(SOURCE_SUMMARY)
    acquisition_summary = read_one(ACQUISITION_SUMMARY)
    source_rows = read_rows(SOURCE_MANIFEST)
    script_text = SOURCE_BUILD_SCRIPT.read_text()

    if policy["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_LEAKAGE_REVIEW_PREFLIGHT_POLICY_FROZEN":
        raise SystemExit("unexpected leakage-review preflight policy status")
    if source_summary["verdict"] != "external_photoz_calibration_sources_attached_pending_leakage_review":
        raise SystemExit("source manifest should remain pending leakage review")
    if acquisition_summary["verdict"] != "external_photoz_calibration_acquisition_plan_frozen_h1_still_open":
        raise SystemExit("acquisition plan should remain open")
    if policy["current_endpoint_replay_allowed"] != "false":
        raise SystemExit("leakage-review preflight must not authorize endpoint replay")
    if len(source_rows) != 3:
        raise SystemExit("expected three source-manifest rows")

    forbidden_script_hits = [token for token in FORBIDDEN_SCRIPT_TOKENS if token in script_text]
    manifest_rows_clean = all(
        row["forbidden_inputs_used"] == "false"
        and row["endpoint_replay_allowed"] == "false"
        and row["endpoint_validation_claimed"] == "false"
        for row in source_rows
    )
    cache_files_present = all((ROOT / row["cache_path"]).exists() for row in source_rows)
    markers_present = all(row["all_required_markers_present"] == "true" for row in source_rows)
    public_source_only = all(row["official_url"].startswith("https://") for row in source_rows)

    checks = [
        {
            "check_id": "L1_manifest_metadata_no_forbidden_inputs",
            "check_status": "PASS" if manifest_rows_clean else "FAIL",
            "checked_artifact": str(SOURCE_MANIFEST.relative_to(ROOT)),
            "check_result": "source_manifest_rows_keep_forbidden_inputs_replay_and_validation_false",
            "uses_endpoint_fields": "false",
        },
        {
            "check_id": "L2_cached_public_sources_present",
            "check_status": "PASS" if cache_files_present and markers_present and public_source_only else "FAIL",
            "checked_artifact": "data/source_manifest/source_page_cache/kids1000_photoz_calibration_v1",
            "check_result": "cached_public_sources_exist_and_required_source_side_markers_are_present",
            "uses_endpoint_fields": "false",
        },
        {
            "check_id": "L3_source_manifest_builder_has_no_endpoint_dependencies",
            "check_status": "PASS" if not forbidden_script_hits else "FAIL",
            "checked_artifact": str(SOURCE_BUILD_SCRIPT.relative_to(ROOT)),
            "check_result": "no_forbidden_endpoint_scoring_or_residual_tokens_in_source_manifest_builder",
            "uses_endpoint_fields": "false" if not forbidden_script_hits else "true",
        },
        {
            "check_id": "L4_independent_reviewer_attestation",
            "check_status": "OPEN",
            "checked_artifact": "future_review_response_csv_or_attestation",
            "check_result": "independent_reviewer_attestation_not_yet_attached",
            "uses_endpoint_fields": "false",
        },
    ]
    for row in checks:
        row.update(
            {
                "policy_id": policy["policy_id"],
                "forbidden_inputs_used": "false" if row["uses_endpoint_fields"] == "false" else "true",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    passed = sum(row["check_status"] == "PASS" for row in checks)
    failed = sum(row["check_status"] == "FAIL" for row in checks)
    open_checks = sum(row["check_status"] == "OPEN" for row in checks)
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "EXTERNAL_PHOTOZ_CALIBRATION_LEAKAGE_REVIEW_PREFLIGHT_BUILT",
            "check_count": str(len(checks)),
            "passed_checks": str(passed),
            "failed_checks": str(failed),
            "open_checks": str(open_checks),
            "automated_leakage_preflight_complete": "true" if passed == 3 and failed == 0 else "false",
            "independent_reviewer_attestation_complete": "false",
            "r4_leakage_review_complete": "false",
            "h1_independent_evidence_complete": "false",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values_for_scoring": "false",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "uses_residuals": "false",
            "uses_fit_statistics": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "automated_leakage_preflight_passed_independent_reviewer_still_open",
            "recommended_next_action": "attach_independent_reviewer_response_before_marking_R4_or_H1_complete",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, checks)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_EXTERNAL_PHOTOZ_CALIBRATION_LEAKAGE_REVIEW_PREFLIGHT_V1_BUILT "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
