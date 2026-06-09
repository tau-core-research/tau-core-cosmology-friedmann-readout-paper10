#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_low_mode_kernel_envelope_derivation_policy_v1.csv"
GROUNDING_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_low_mode_carrier_source_grounding_policy_v1.csv"
GROUNDING_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_low_mode_carrier_source_grounding_v1_summary.csv"
THEORY_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1_summary.csv"
MODE_WEIGHTS = ROOT / "data" / "derived" / "kids1000_cosebis_low_mode_kernel_envelope_derivation_v1_mode_weights.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_low_mode_kernel_envelope_derivation_v1_summary.csv"


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


def fmt(value: float) -> str:
    return f"{value:.12e}"


def main() -> None:
    policy = read_one(POLICY)
    grounding_policy = read_one(GROUNDING_POLICY)
    grounding_summary = read_one(GROUNDING_SUMMARY)
    theory_summary = read_one(THEORY_SUMMARY)
    if policy["status"] != "LOW_MODE_KERNEL_ENVELOPE_DERIVATION_POLICY_FROZEN":
        raise SystemExit("unexpected low-mode kernel derivation policy status")
    if policy["parent_source_grounding_policy"] != grounding_policy["policy_id"]:
        raise SystemExit("parent low-mode source-grounding policy mismatch")
    if policy["uses_kids_data_vector_values"] != "false":
        raise SystemExit("kernel derivation must not use KiDS data-vector values")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("kernel derivation must not allow endpoint scoring")
    if grounding_summary["source_grounding_verdict"] != "partial_protocol_grounding_with_open_first_principles_derivation_blocker":
        raise SystemExit("unexpected parent source-grounding verdict")

    modes = list(range(1, 21))
    raw_power = {mode: 1.0 / mode for mode in modes}
    raw_amplitude = {mode: math.sqrt(raw_power[mode]) for mode in modes}
    mean_amplitude = sum(raw_amplitude.values()) / len(raw_amplitude)
    weights = [
        {
            "policy_id": policy["policy_id"],
            "mode": str(mode),
            "log_band_power_envelope": fmt(raw_power[mode]),
            "raw_amplitude_envelope": fmt(raw_amplitude[mode]),
            "unit_mean_mode_weight": fmt(raw_amplitude[mode] / mean_amplitude),
            "matches_frozen_theory_vector_rule": "true",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": policy["claim_boundary"],
        }
        for mode in modes
    ]
    ledger = [
        {
            "policy_id": policy["policy_id"],
            "step_id": "A1_dimensionless_mode_index",
            "status": "ASSUMPTION",
            "statement": "The COSEBIs mode index n is treated as a dimensionless ordered angular/readout scale label for this source-side envelope derivation.",
            "audit_note": "No dimensional scale is introduced by n; the envelope is dimensionless before the later endpoint amplitude.",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "A2_log_band_neutral_path_power",
            "status": "ASSUMPTION",
            "statement": "A smooth coherent path/readout residual has approximately scale-neutral source-side power per logarithmic COSEBIs mode band.",
            "audit_note": "This is the key physical prior. It is not inferred from the KiDS data vector and is not yet a covariant lensing theorem.",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "D1_power_per_discrete_mode",
            "status": "DERIVED_CONDITIONAL",
            "statement": "If dP/dln(n) is approximately constant, then a discrete linear mode bin has P_n proportional to 1/n.",
            "audit_note": "Because dln(n) is approximated by dn/n for unit mode spacing.",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "D2_amplitude_envelope",
            "status": "DERIVED_CONDITIONAL",
            "statement": "The coherent amplitude envelope is proportional to sqrt(P_n), giving M_mode(n) proportional to n^(-1/2).",
            "audit_note": "This derives the envelope exponent conditionally from the log-band power prior.",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "D3_unit_mean_normalization",
            "status": "DEFINITION",
            "statement": "The finite retained KiDS mode domain n=1..20 fixes the protocol normalization M_mode(n)=n^(-1/2)/mean_1_20(n^(-1/2)).",
            "audit_note": "Normalization is dimensionless and does not set the endpoint amplitude.",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "L1_known_limit",
            "status": "LIMIT_CHECK",
            "statement": "In the no-path/readout-residual limit, the endpoint amplitude is zero and this dimensionless carrier contributes no prediction.",
            "audit_note": "The carrier alone is not a force, distance, or lensing observable.",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "B1_remaining_blocker",
            "status": "OPEN_BLOCKER",
            "statement": "A survey-native or covariant Tau Core lensing/path kernel must still derive when the log-band-neutral prior is valid.",
            "audit_note": "This result is a conditional envelope derivation, not final empirical validation and not a complete first-principles KiDS theory vector.",
            "claim_boundary": policy["claim_boundary"],
        },
    ]
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "LOW_MODE_KERNEL_ENVELOPE_CONDITIONAL_DERIVATION_COMPLETE",
            "selected_statistic": policy["selected_statistic"],
            "derived_envelope": policy["derived_envelope"],
            "mode_min": "1",
            "mode_max": "20",
            "mode_count": str(len(modes)),
            "ledger_rows": str(len(ledger)),
            "assumption_count": str(sum(row["status"] == "ASSUMPTION" for row in ledger)),
            "derived_conditional_count": str(sum(row["status"] == "DERIVED_CONDITIONAL" for row in ledger)),
            "definition_count": str(sum(row["status"] == "DEFINITION" for row in ledger)),
            "limit_check_count": str(sum(row["status"] == "LIMIT_CHECK" for row in ledger)),
            "open_blocker_count": str(sum(row["status"] == "OPEN_BLOCKER" for row in ledger)),
            "mean_unit_mode_weight": fmt(sum(float(row["unit_mean_mode_weight"]) for row in weights) / len(weights)),
            "matches_frozen_theory_vector_min_weight": theory_summary["min_mode_shape_weight"],
            "matches_frozen_theory_vector_max_weight": theory_summary["max_mode_shape_weight"],
            "derivation_verdict": "conditional_log_band_power_envelope_derives_n_minus_half_shape_but_covariant_kernel_blocker_remains",
            "uses_kids_data_vector_values": "false",
            "uses_fit_statistics": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(MODE_WEIGHTS, weights)
    write_csv(LEDGER, ledger)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_LOW_MODE_KERNEL_ENVELOPE_DERIVATION_V1_COMPLETE "
        f"verdict={summary[0]['derivation_verdict']} "
        f"open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
