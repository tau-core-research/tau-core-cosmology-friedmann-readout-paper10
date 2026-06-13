#!/usr/bin/env python3
"""Build the Paper11-style control-veto gate for the ACT path-weight replay."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
REPLAY = DERIVED / "act_dr6_lensing_path_weight_authorized_replay_v1_summary.csv"
DIAGNOSTIC = DERIVED / "act_dr6_lensing_path_weight_control_dominance_diagnostic_v1_summary.csv"
OUT = DERIVED / "act_dr6_lensing_path_weight_paper11_control_veto_gate_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise RuntimeError(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def main() -> None:
    replay = read_one(REPLAY)
    diagnostic = read_one(DIAGNOSTIC)

    controls_better = int(replay["controls_better_than_candidate"])
    family_survives = replay["family_survives_controls"].lower() == "true"
    endpoint_claim = replay["endpoint_validation_claimed"].lower() == "true"
    physical_path_claim = replay["physical_lensing_path_weight_claimed"].lower() == "true"

    if controls_better > 0 or not family_survives:
        verdict = "PAPER11_CONTROL_VETO_ACT_PATH_WEIGHT_NOT_FAMILY_VERDICT_ELIGIBLE"
        m0_m1_claim_allowed = "false"
        dark_sector_inference_allowed = "false"
        next_gate = "source_basis_freeze_or_demote_act_path_weight"
    else:
        verdict = "PAPER11_CONTROL_VETO_PASSED_ACT_PATH_WEIGHT_FAMILY_VERDICT_ELIGIBLE"
        m0_m1_claim_allowed = "true"
        dark_sector_inference_allowed = "false"
        next_gate = "family_verdict_requires_separate_dark_sector_decision_protocol"

    row = {
        "artifact_id": "ACT_DR6_LENSING_PATH_WEIGHT_PAPER11_CONTROL_VETO_GATE_V1",
        "status": "PAPER11_STYLE_CONTROL_VETO_GATE_BUILT_NOT_VALIDATION",
        "paper11_family_frame": "M0_no_dark_tau_readout_vs_M1_tau_base_substrate_vs_M2_standard_dark_sector",
        "act_candidate_verdict": replay["verdict"],
        "control_diagnostic_verdict": diagnostic["verdict"],
        "best_control_branch": replay["best_control_branch"],
        "controls_better_than_candidate": replay["controls_better_than_candidate"],
        "family_survives_controls": replay["family_survives_controls"],
        "candidate_delta_chi2_vs_baseline": diagnostic["candidate_delta_chi2_vs_baseline"],
        "candidate_delta_chi2_vs_best_control": diagnostic["candidate_delta_chi2_vs_best_control"],
        "endpoint_validation_claimed": str(endpoint_claim).lower(),
        "physical_lensing_path_weight_claimed": str(physical_path_claim).lower(),
        "m0_or_m1_source_structure_claim_allowed": m0_m1_claim_allowed,
        "m2_dark_sector_inference_allowed": dark_sector_inference_allowed,
        "paper11_control_veto_interpretation": (
            "control dominance blocks promotion of the present ACT source basis; "
            "it does not by itself favor a standard dark-sector benchmark"
        ),
        "required_next_gate": next_gate,
        "verdict": verdict,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    main()
