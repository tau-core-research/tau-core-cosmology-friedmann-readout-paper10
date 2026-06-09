#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_log_band_prior_eligibility_gate_policy_v1.csv"
DERIVATION_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_low_mode_kernel_envelope_derivation_policy_v1.csv"
DERIVATION_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_low_mode_kernel_envelope_derivation_v1_summary.csv"
MODECUT_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mask_modecut_policy_v1.csv"
MODE_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_mode_policy_v1.csv"
PATH_PREFLIGHT = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_source_preflight_v1_summary.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_log_band_prior_eligibility_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_log_band_prior_eligibility_gate_v1_summary.csv"


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
    policy = read_one(POLICY)
    derivation_policy = read_one(DERIVATION_POLICY)
    derivation_summary = read_one(DERIVATION_SUMMARY)
    modecut_policy = read_one(MODECUT_POLICY)
    mode_policy = read_one(MODE_POLICY)
    path_preflight = read_one(PATH_PREFLIGHT)

    if policy["status"] != "LOG_BAND_PRIOR_ELIGIBILITY_GATE_FROZEN":
        raise SystemExit("unexpected log-band prior eligibility policy status")
    if policy["parent_kernel_envelope_derivation_policy"] != derivation_policy["policy_id"]:
        raise SystemExit("parent kernel derivation policy mismatch")
    if policy["uses_kids_data_vector_values"] != "false" or policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("eligibility gate must remain data-vector-free and non-scoring")
    if derivation_summary["open_blocker_count"] != "1":
        raise SystemExit("parent derivation must preserve open blocker")

    retained_all_modes = modecut_policy["retained_mode_range"] == "1:20" and modecut_policy["expected_retained_rows"] == "300"
    mode_domain_ordered = mode_policy["expected_modes_per_pair"] == "20" and mode_policy["expected_data_vector_rows"] == "300"
    path_mapping_ready = path_preflight["mapping_ready"] == "true"

    rows = [
        {
            "policy_id": policy["policy_id"],
            "condition_id": "C1_ordered_dimensionless_mode_domain",
            "status": "PASS" if mode_domain_ordered else "FAIL",
            "source_artifact": str(MODE_POLICY.relative_to(ROOT)),
            "criterion": "COSEBIs modes must provide an ordered dimensionless mode hierarchy on the retained statistic.",
            "current_evidence": f"expected_modes_per_pair={mode_policy['expected_modes_per_pair']}; expected_data_vector_rows={mode_policy['expected_data_vector_rows']}",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "condition_id": "C2_no_posthoc_mode_cut",
            "status": "PASS" if retained_all_modes else "FAIL",
            "source_artifact": str(MODECUT_POLICY.relative_to(ROOT)),
            "criterion": "All retained modes must remain available; low-mode preference cannot be introduced by deleting high modes after scoring.",
            "current_evidence": f"retained_mode_range={modecut_policy['retained_mode_range']}; expected_retained_rows={modecut_policy['expected_retained_rows']}",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "condition_id": "C3_source_side_path_mapping_exists",
            "status": "PASS" if path_mapping_ready else "FAIL",
            "source_artifact": str(PATH_PREFLIGHT.relative_to(ROOT)),
            "criterion": "A source-side path/readout mapping shell must exist before a path/readout envelope prior can be attached to the theory vector.",
            "current_evidence": f"mapping_ready={path_preflight['mapping_ready']}; endpoint_scoring_allowed={path_preflight['endpoint_scoring_allowed']}",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "condition_id": "C4_smooth_coherent_path_residual",
            "status": "ASSUMPTION_NOT_SOURCE_PROVEN",
            "source_artifact": "future_survey_native_path_kernel_or_mock_suite",
            "criterion": "The path/readout residual must be smooth and coherent enough that log-band power neutrality is physically justified.",
            "current_evidence": "Not directly source-proven in the current release; only encoded as a Tau Core-inspired prior.",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "condition_id": "C5_no_high_frequency_only_source_claim",
            "status": "PASS_AS_PROTOCOL_GUARDRAIL",
            "source_artifact": str(DERIVATION_POLICY.relative_to(ROOT)),
            "criterion": "The derivation must not claim a high-frequency-only or localized oscillatory source process while using a low-mode envelope.",
            "current_evidence": "Parent derivation explicitly assumes broad coherent path/readout residual power, not a high-frequency-only source.",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "condition_id": "C6_covariant_or_survey_native_kernel",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_covariant_or_survey_native_lensing_path_kernel",
            "criterion": "A complete theory claim requires deriving the log-band-neutral prior from a covariant or survey-native Tau Core lensing/path kernel.",
            "current_evidence": "Not available in the current release.",
            "claim_boundary": policy["claim_boundary"],
        },
    ]
    pass_like = {"PASS", "PASS_AS_PROTOCOL_GUARDRAIL"}
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "LOG_BAND_PRIOR_ELIGIBILITY_GATE_PARTIAL_PASS",
            "selected_statistic": policy["selected_statistic"],
            "conditions": str(len(rows)),
            "pass_count": str(sum(row["status"] in pass_like for row in rows)),
            "assumption_not_source_proven_count": str(sum(row["status"] == "ASSUMPTION_NOT_SOURCE_PROVEN" for row in rows)),
            "open_blocker_count": str(sum(row["status"] == "OPEN_BLOCKER" for row in rows)),
            "eligibility_verdict": "protocol_eligible_for_conditional_envelope_but_not_full_kernel_validated",
            "uses_kids_data_vector_values": "false",
            "uses_fit_statistics": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(LEDGER, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_LOG_BAND_PRIOR_ELIGIBILITY_GATE_V1_COMPLETE "
        f"verdict={summary[0]['eligibility_verdict']} "
        f"open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
