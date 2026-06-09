#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_low_mode_carrier_source_grounding_policy_v1.csv"
THEORY_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_source_frozen_theory_vector_policy_v1.csv"
MODE_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_mode_policy_v1.csv"
MODECUT_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mask_modecut_policy_v1.csv"
STRESS_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_mode_shape_stress_policy_v1.csv"
LOCALIZATION_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_mode_localization_v1_summary.csv"
STRESS_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_mode_shape_stress_v1_summary.csv"
THEORY_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1_summary.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_low_mode_carrier_source_grounding_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_low_mode_carrier_source_grounding_v1_summary.csv"


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
    theory_policy = read_one(THEORY_POLICY)
    mode_policy = read_one(MODE_POLICY)
    modecut_policy = read_one(MODECUT_POLICY)
    stress_policy = read_one(STRESS_POLICY)
    localization = read_one(LOCALIZATION_SUMMARY)
    stress = read_one(STRESS_SUMMARY)
    theory = read_one(THEORY_SUMMARY)

    if policy["status"] != "LOW_MODE_CARRIER_SOURCE_GROUNDING_POLICY_FROZEN":
        raise SystemExit("unexpected low-mode source-grounding policy status")
    if policy["parent_theory_vector_policy"] != theory_policy["policy_id"]:
        raise SystemExit("parent theory-vector policy mismatch")
    if policy["parent_mode_shape_stress_policy"] != stress_policy["policy_id"]:
        raise SystemExit("parent mode-shape stress policy mismatch")
    if policy["parent_mode_localization_policy"] != localization["policy_id"]:
        raise SystemExit("parent mode-localization policy mismatch")
    if policy["uses_kids_data_vector_values_for_grounding"] != "false":
        raise SystemExit("source-grounding policy must not use KiDS data vector values")
    if policy["allows_endpoint_validation_claim"] != "false":
        raise SystemExit("source-grounding policy must forbid validation claims")
    if theory_policy["mode_shape_rule"] != policy["carrier_under_review"]:
        raise SystemExit("carrier under review must match frozen theory-vector policy")
    if theory["mean_mode_shape_weight"] != "1.000000000000e+00":
        raise SystemExit("frozen mode carrier must remain unit-mean normalized")
    if mode_policy["expected_modes_per_pair"] != "20" or modecut_policy["retained_mode_range"] != "1:20":
        raise SystemExit("unexpected COSEBIs retained mode domain")

    rows = [
        {
            "policy_id": policy["policy_id"],
            "criterion_id": "source_independence",
            "criterion_status": "PASS",
            "source_or_parent_artifact": str(THEORY_POLICY.relative_to(ROOT)),
            "rationale": "The n^-1/2 mode carrier was frozen in the source-side theory-vector policy before endpoint scoring and forbids KiDS data-vector values, residuals, posterior chains, and post-hoc mode-shape choice.",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "criterion_id": "coherent_path_readout_prior",
            "criterion_status": "PARTIAL_PASS",
            "source_or_parent_artifact": str(MODE_POLICY.relative_to(ROOT)),
            "rationale": "A path/readout residual is expected to be broad and coherent across the COSEBIs mode hierarchy rather than high-frequency-only; this supports low-mode preference as a protocol prior, not as a derived lensing theorem.",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "criterion_id": "no_posthoc_mode_cut",
            "criterion_status": "PASS",
            "source_or_parent_artifact": str(MODECUT_POLICY.relative_to(ROOT)),
            "rationale": "All modes 1 through 20 and all 15 tomographic pairs are retained; the carrier does not remove high modes by a post-score mode cut.",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "criterion_id": "diagnostic_consistency_with_mode_localization",
            "criterion_status": "SUPPORTING_DIAGNOSTIC",
            "source_or_parent_artifact": str(LOCALIZATION_SUMMARY.relative_to(ROOT)),
            "rationale": "The independent post-score localization diagnostic finds that the endpoint signal is low-mode localized, with low modes 1 to 5 carrying the improvement. This supports the carrier direction but cannot ground it by itself.",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "criterion_id": "mode_shape_stress_support",
            "criterion_status": "SUPPORTING_DIAGNOSTIC",
            "source_or_parent_artifact": str(STRESS_SUMMARY.relative_to(ROOT)),
            "rationale": "The stress family shows that flat weighting still improves while high-mode weighting fails, and the frozen n^-1/2 carrier is best in the small declared family. This limits the carrier-artifact concern without proving the final shape.",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "criterion_id": "missing_first_principles_mode_kernel_derivation",
            "criterion_status": "OPEN_BLOCKER",
            "source_or_parent_artifact": "future_covariant_lensing_path_kernel_derivation",
            "rationale": "The n^-1/2 exponent is still a source-frozen protocol carrier, not a first-principles Tau Core lensing/path theorem. External covariance, scale-cut, and mock tests remain required before validation language.",
            "claim_boundary": policy["claim_boundary"],
        },
    ]

    pass_count = sum(row["criterion_status"] == "PASS" for row in rows)
    partial_count = sum(row["criterion_status"] == "PARTIAL_PASS" for row in rows)
    diagnostic_count = sum(row["criterion_status"] == "SUPPORTING_DIAGNOSTIC" for row in rows)
    blocker_count = sum(row["criterion_status"] == "OPEN_BLOCKER" for row in rows)
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "LOW_MODE_CARRIER_SOURCE_GROUNDING_PARTIAL_COMPLETE",
            "selected_statistic": policy["selected_statistic"],
            "carrier_under_review": policy["carrier_under_review"],
            "ledger_rows": str(len(rows)),
            "pass_count": str(pass_count),
            "partial_pass_count": str(partial_count),
            "supporting_diagnostic_count": str(diagnostic_count),
            "open_blocker_count": str(blocker_count),
            "source_grounding_verdict": "partial_protocol_grounding_with_open_first_principles_derivation_blocker",
            "uses_kids_data_vector_values_for_grounding": "false",
            "uses_kids_data_vector_values_for_scoring": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(LEDGER, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_LOW_MODE_CARRIER_SOURCE_GROUNDING_V1_COMPLETE "
        f"verdict={summary[0]['source_grounding_verdict']} "
        f"open_blockers={blocker_count}"
    )


if __name__ == "__main__":
    main()
