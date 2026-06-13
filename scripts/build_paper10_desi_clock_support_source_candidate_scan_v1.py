#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_clock_support_source_candidate_scan_policy_v1.csv"
ACQUISITION = ROOT / "data/derived/paper10_desi_clock_support_acquisition_manifest_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_clock_support_source_candidate_scan_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_clock_support_source_candidate_scan_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_clock_support_source_candidate_scan_not_validation"


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
        raise SystemExit("bad candidate-scan claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")
    acquisition = {row["target_id"]: row for row in read_rows(ACQUISITION)}
    expected_targets = {
        "DESI_RADIAL_ROW_4_MULTI_CLOCK_REDUNDANCY",
        "DESI_RADIAL_ROW_5_HIGH_Z_CLOCK_SUPPORT",
    }
    if set(acquisition) != expected_targets:
        raise SystemExit("candidate scan expects the two frozen acquisition targets")

    rows = [
        {
            "scan_id": policy["scan_id"],
            "target_id": "DESI_RADIAL_ROW_4_MULTI_CLOCK_REDUNDANCY",
            "candidate_id": "EBOSS_DR16_QSO_BAO_RSD_Z1P48",
            "candidate_type": "cross_probe_quasar_BAO_RSD_not_independent_clock",
            "candidate_z_or_range": "1.48",
            "candidate_value_summary": "D_H(z_eff=1.48)/r_d=13.11+-0.52;D_M/r_d=30.66+-0.88;fsigma8=0.439+-0.048",
            "source_reference": "Hou et al. 2020 MNRAS eBOSS DR16 QSO clustering",
            "source_url": "https://arxiv.org/abs/2007.08998",
            "gate_result": "RETAIN_AS_ROW4_CROSS_PROBE_CONTROL_ONLY_NOT_CLOCK_SUPPORT",
            "gate_reason": "near row4 redshift but BAO/RSD clustering route rather than independent cosmic-clock H(z); cannot provide second clock-reference family",
            "accepted_for_acquisition_target": "false",
            "control_or_context_only": "true",
            "source_fetch_status": "source_identified_not_attached_to_endpoint",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scan_id": policy["scan_id"],
            "target_id": "DESI_RADIAL_ROW_4_MULTI_CLOCK_REDUNDANCY",
            "candidate_id": "TOMASETTI_2023_VANDELS_CC_Z1P26",
            "candidate_type": "peer_reviewed_cosmic_chronometer_Hz",
            "candidate_z_or_range": "1.26",
            "candidate_value_summary": "H(z=1.26)=135+-65_km_s^-1_Mpc^-1",
            "source_reference": "Tomasetti et al. 2023 A&A 679 A96",
            "source_url": "https://arxiv.org/abs/2305.16387",
            "gate_result": "REJECT_FOR_ROW4_OUTSIDE_FROZEN_Z_WINDOW",
            "gate_reason": "abs(1.26-1.484)=0.224>0.10; useful future high-z CC context but not row4 redundancy support",
            "accepted_for_acquisition_target": "false",
            "control_or_context_only": "true",
            "source_fetch_status": "source_identified_not_attached_to_endpoint",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scan_id": policy["scan_id"],
            "target_id": "DESI_RADIAL_ROW_4_MULTI_CLOCK_REDUNDANCY",
            "candidate_id": "JIAO_2023_LEGAC_CC_Z0P8",
            "candidate_type": "peer_reviewed_cosmic_chronometer_Hz",
            "candidate_z_or_range": "0.8",
            "candidate_value_summary": "H(z=0.8)=113.1+-15.1_stat_plus_systematics",
            "source_reference": "Jiao et al. 2023 ApJS 265 48",
            "source_url": "https://arxiv.org/abs/2205.05701",
            "gate_result": "REJECT_FOR_ROW4_OUTSIDE_FROZEN_Z_WINDOW",
            "gate_reason": "abs(0.8-1.484)=0.684>0.10; not local support for row4",
            "accepted_for_acquisition_target": "false",
            "control_or_context_only": "true",
            "source_fetch_status": "source_identified_not_attached_to_endpoint",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scan_id": policy["scan_id"],
            "target_id": "DESI_RADIAL_ROW_4_MULTI_CLOCK_REDUNDANCY",
            "candidate_id": "JIMENEZ_2023_PHOTOMETRIC_CC_Z0P75",
            "candidate_type": "proof_of_principle_photometric_cosmic_chronometer_Hz",
            "candidate_z_or_range": "0.65<z<0.85;z_eff=0.75",
            "candidate_value_summary": "H(z=0.75)=105.0+-7.9_stat+-7.3_sys",
            "source_reference": "Jimenez et al. 2023 JCAP 11 047",
            "source_url": "https://arxiv.org/abs/2306.11425",
            "gate_result": "REJECT_FOR_ROW4_OUTSIDE_FROZEN_Z_WINDOW",
            "gate_reason": "photometric proof-of-principle is far below z=1.484 and not row4 redundancy support",
            "accepted_for_acquisition_target": "false",
            "control_or_context_only": "true",
            "source_fetch_status": "source_identified_not_attached_to_endpoint",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scan_id": policy["scan_id"],
            "target_id": "DESI_RADIAL_ROW_5_HIGH_Z_CLOCK_SUPPORT",
            "candidate_id": "EBOSS_DR16_LYA_BAO_Z2P33",
            "candidate_type": "cross_probe_radial_BAO_time_shape_not_independent_clock",
            "candidate_z_or_range": "2.33",
            "candidate_value_summary": "D_H(z=2.33)/r_d=8.99+-0.19;D_M(z=2.33)/r_d=37.5+-1.1",
            "source_reference": "du Mas des Bourboux et al. 2020 ApJ 901 153",
            "source_url": "https://arxiv.org/abs/2007.08995",
            "gate_result": "RETAIN_AS_CROSS_PROBE_CONTROL_ONLY_NOT_CLOCK_SUPPORT",
            "gate_reason": "covers z=2.33 but is BAO/r_d route rather than independent cosmic-clock H(z); cannot close high-z clock support gate alone",
            "accepted_for_acquisition_target": "false",
            "control_or_context_only": "true",
            "source_fetch_status": "source_identified_not_attached_to_endpoint",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scan_id": policy["scan_id"],
            "target_id": "DESI_RADIAL_ROW_5_HIGH_Z_CLOCK_SUPPORT",
            "candidate_id": "SDSS_DR17_LYA_FOREST_VAC",
            "candidate_type": "public_catalog_route_for_LyA_BAO_not_clock_measurement",
            "candidate_z_or_range": "z~2.33 BAO analysis route",
            "candidate_value_summary": "public DR17 VAC supports 3D Ly-alpha auto/cross correlations for BAO analyses",
            "source_reference": "SDSS DR17 Lyman-alpha forest VAC",
            "source_url": "https://www.sdss4.org/dr17/spectro/lyman-alpha-forest/",
            "gate_result": "RETAIN_AS_REPRODUCIBLE_ROUTE_CONTEXT_ONLY",
            "gate_reason": "catalog route documents z~2.33 Ly-alpha BAO source family but does not provide independent clock H(z)",
            "accepted_for_acquisition_target": "false",
            "control_or_context_only": "true",
            "source_fetch_status": "source_identified_not_attached_to_endpoint",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, rows)
    accepted = sum(row["accepted_for_acquisition_target"] == "true" for row in rows)
    summary = [
        {
            "scan_id": policy["scan_id"],
            "status": "DESI_CLOCK_SUPPORT_SOURCE_CANDIDATE_SCAN_BUILT_NOT_REPLAY_NOT_VALIDATION",
            "candidate_count": str(len(rows)),
            "accepted_for_acquisition_target_count": str(accepted),
            "row4_accepted_count": str(sum(row["target_id"] == "DESI_RADIAL_ROW_4_MULTI_CLOCK_REDUNDANCY" and row["accepted_for_acquisition_target"] == "true" for row in rows)),
            "row5_accepted_count": str(sum(row["target_id"] == "DESI_RADIAL_ROW_5_HIGH_Z_CLOCK_SUPPORT" and row["accepted_for_acquisition_target"] == "true" for row in rows)),
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "desi_clock_support_candidate_scan_found_cross_probe_context_but_no_gate_closing_clock_support",
            "recommended_next_action": "continue_targeted_search_for_independent_row4_clock_reference_and_high_z_clock_or_source_native_time_readout",
        }
    ]
    write_csv(SUMMARY, summary)


if __name__ == "__main__":
    main()
