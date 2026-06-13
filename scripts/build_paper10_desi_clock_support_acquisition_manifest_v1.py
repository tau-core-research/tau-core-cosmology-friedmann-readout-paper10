#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_clock_support_acquisition_manifest_policy_v1.csv"
MULTI_ROWS = ROOT / "data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1.csv"
MULTI_SUMMARY = ROOT / "data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1_summary.csv"
HIGH_Z_SUMMARY = ROOT / "data/derived/paper10_desi_high_z_independent_clock_support_audit_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_clock_support_acquisition_manifest_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_clock_support_acquisition_manifest_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_clock_support_acquisition_manifest_not_validation"


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
    policy = one_row(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad DESI clock acquisition claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")
    multi_summary = one_row(MULTI_SUMMARY)
    high_z = one_row(HIGH_Z_SUMMARY)
    if multi_summary["multi_clock_support_endpoint_ready"] != "false":
        raise SystemExit("acquisition manifest expects multi-clock support to be incomplete")
    if high_z["high_z_row_can_enter_replay"] != "false":
        raise SystemExit("acquisition manifest expects high-z row to remain blocked")
    multi_by_index = {row["radial_index"]: row for row in read_rows(MULTI_ROWS)}
    row4 = multi_by_index.get("4")
    if row4 is None or row4["relaxed_multi_clock_pass"] != "false":
        raise SystemExit("expected radial row 4 to be the relaxed multi-clock blocker")

    rows = [
        {
            "manifest_id": policy["manifest_id"],
            "target_id": "DESI_RADIAL_ROW_4_MULTI_CLOCK_REDUNDANCY",
            "target_role": "complete_multi_clock_support_for_authorized_shape_scope",
            "radial_index": "4",
            "target_z_eff": row4["z_eff"],
            "current_blocker": "two_relaxed_window_clock_entries_but_only_one_independent_reference",
            "current_support_summary": f"relaxed_count={row4['relaxed_clock_support_count']};relaxed_refs={row4['relaxed_independent_reference_count']};refs={row4['relaxed_references']}",
            "required_new_source": "independent_cosmic_chronometer_or_clock_readout_near_z_1p484_not_reusing_same_reference_family_as_current_blocker",
            "acceptable_source_types": "peer_reviewed_CC_Hz;public_clock_compilation;source_citable_cross_probe_time_readout",
            "minimum_quality_rule": "must_provide_z_or_bin_center;clock_value_or_Hz;uncertainty_or_covariance;method;release_id_or_doi;no_endpoint_residual_use",
            "preferred_z_window": "abs(z-1.484)<=0.10",
            "hard_no_extrapolation_rule": "true",
            "source_fetch_status": "not_fetched",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "manifest_id": policy["manifest_id"],
            "target_id": "DESI_RADIAL_ROW_5_HIGH_Z_CLOCK_SUPPORT",
            "target_role": "allow_future_consideration_of_high_z_holdout_without_CC_extrapolation",
            "radial_index": high_z["target_radial_index"],
            "target_z_eff": high_z["target_z_eff"],
            "current_blocker": f"nearest_frozen_clock_z={high_z['nearest_frozen_clock_z']};delta_z={high_z['delta_z_to_nearest_frozen_clock']};not_bracketed_without_extrapolation",
            "current_support_summary": f"cc_z_max={high_z['cc_z_max']};endpoint_ready_support_count={high_z['endpoint_ready_support_count']}",
            "required_new_source": "independent_high_z_clock_or_time_readout_support_covering_or_bracketing_z_2p33_without_extrapolation",
            "acceptable_source_types": "peer_reviewed_high_z_CC_Hz;public_high_z_clock_compilation;source_citable_cross_probe_time_readout_shape",
            "minimum_quality_rule": "must_cover_or_bracket_z_2p33;must_provide_uncertainty_or_covariance;must_be_public_or_citable;must_be_frozen_before_replay",
            "preferred_z_window": "cover_or_bracket_z_2.33_without_extrapolation",
            "hard_no_extrapolation_rule": "true",
            "source_fetch_status": "not_fetched",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, rows)
    summary = [
        {
            "manifest_id": policy["manifest_id"],
            "status": "DESI_CLOCK_SUPPORT_ACQUISITION_MANIFEST_FROZEN_NOT_FETCHED_NOT_REPLAY_NOT_VALIDATION",
            "target_count": str(len(rows)),
            "multi_clock_target_count": "1",
            "high_z_target_count": "1",
            "source_fetch_completed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "desi_clock_support_acquisition_targets_frozen_sources_not_attached",
            "recommended_next_action": "fetch_or_review_independent_clock_sources_for_row4_and_high_z_row5",
        }
    ]
    write_csv(SUMMARY, summary)


if __name__ == "__main__":
    main()
