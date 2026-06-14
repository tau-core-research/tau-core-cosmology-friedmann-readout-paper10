#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "data/derived/joint_single_statistic_binding_prerequisites_v1.csv"
ZI_SUMMARY = ROOT / "data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv"
TJOINT = ROOT / "data/derived/joint_numeric_t_joint_ledger_v1.csv"
DECOMP = ROOT / "data/derived/joint_numeric_t_joint_closest_shuffle_decomposition_v1.csv"
OUT = ROOT / "data/derived/joint_numeric_t_joint_channel_exchange_sensitivity_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_channel_exchange_sensitivity_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_channel_exchange_sensitivity_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_channel_exchange_sensitivity_not_validation"

PAIR = ("observer_path_basis_low_z", "desi_shape_time_readout")


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: float) -> str:
    return f"{value:.12e}"


def main() -> None:
    bindings = {row["channel_id"]: row for row in read_rows(BINDING)}
    zi = {row["channel_id"]: row for row in read_rows(ZI_SUMMARY) if row["channel_id"] != "all_channels"}
    tjoint = {row["channel_id"]: row for row in read_rows(TJOINT)}
    decomp = {row["target_channel"]: row for row in read_rows(DECOMP)}

    missing = [channel for channel in PAIR if channel not in bindings or channel not in zi or channel not in tjoint]
    if missing:
        raise SystemExit(f"missing channel rows: {missing}")

    rows: list[dict[str, str]] = []
    for channel in PAIR:
        other = PAIR[1] if channel == PAIR[0] else PAIR[0]
        q = float(tjoint[channel]["q_i"])
        z = float(tjoint[channel]["candidate_z_i"])
        other_z = float(tjoint[other]["candidate_z_i"])
        rows.append(
            {
                "diagnostic_id": "JOINT_NUMERIC_T_JOINT_CHANNEL_EXCHANGE_SENSITIVITY_V1",
                "channel_id": channel,
                "exchanged_with_channel_id": other,
                "source_artifact": bindings[channel]["score_source_artifact"],
                "control_source_artifact": zi[channel]["control_source_artifact"],
                "candidate_source_artifact": zi[channel]["candidate_source_artifact"],
                "native_value_definition": zi[channel]["candidate_native_value"],
                "matched_control_count": zi[channel]["matched_control_count"],
                "readiness_status": zi[channel]["readiness_status"],
                "caveat": zi[channel]["caveat"],
                "covariance_artifact": bindings[channel]["covariance_artifact"],
                "nuisance_or_amplitude_rule": bindings[channel]["nuisance_or_amplitude_rule"],
                "q_i": fmt(q),
                "candidate_z_i": fmt(z),
                "exchanged_candidate_z_i": fmt(other_z),
                "z_i_difference_from_exchange_partner": fmt(z - other_z),
                "q_weighted_difference_under_exchange": fmt(q * (z - other_z)),
                "closest_shuffle_contribution_delta": decomp[channel]["candidate_minus_control_contribution"],
                "source_distinctness_status": "distinct_source_route",
                "statistic_exchange_sensitivity_status": "thin_margin_after_shared_standardization",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    q_diff = abs(float(tjoint[PAIR[0]]["q_i"]) - float(tjoint[PAIR[1]]["q_i"]))
    z_diff = abs(float(tjoint[PAIR[0]]["candidate_z_i"]) - float(tjoint[PAIR[1]]["candidate_z_i"]))
    margin = sum(float(row["closest_shuffle_contribution_delta"]) for row in rows)
    summary = {
        "diagnostic_id": "JOINT_NUMERIC_T_JOINT_CHANNEL_EXCHANGE_SENSITIVITY_V1",
        "channel_pair": "|".join(PAIR),
        "source_routes_distinct": "true",
        "same_score_source_artifact": str(bindings[PAIR[0]]["score_source_artifact"] == bindings[PAIR[1]]["score_source_artifact"]).lower(),
        "same_control_source_artifact": str(zi[PAIR[0]]["control_source_artifact"] == zi[PAIR[1]]["control_source_artifact"]).lower(),
        "matched_control_count_pair": f"{zi[PAIR[0]]['matched_control_count']}|{zi[PAIR[1]]['matched_control_count']}",
        "q_i_absolute_difference": fmt(q_diff),
        "candidate_z_i_absolute_difference": fmt(z_diff),
        "exchange_margin_reconstructed": fmt(margin),
        "verdict": "source_routes_are_distinct_but_current_scalar_T_joint_is_thin_to_this_exchange",
        "recommended_next_check": "derive_or_audit_source_side_channel_distinguishability_penalty_before_strengthening_validation_claims",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint channel-exchange sensitivity v1",
                "",
                "**Doc class:** channel-exchange diagnostic.",
                "**Status:** not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "The observer-path low-z and DESI shape/time channels are source-distinct:",
                "they use different score artifacts, different control artifacts, different",
                "matched-control populations, and different caveats. However, after the",
                "shared signed median/MAD standardization, their positive candidate `z_i`",
                "values and frozen `q_i` weights are close enough that exchanging them",
                "produces only a thin scalar `T_joint` margin.",
                "",
                "This supports the narrow interpretation: the current scalar `T_joint`",
                "sees source-distinct channels, but it does not strongly penalize this",
                "particular lower-amplitude channel exchange. The next claim-safe check",
                "is a source-side channel-distinguishability penalty or orthogonality",
                "audit before strengthening validation language.",
                "",
            ]
        )
    )
    print(
        "JOINT_NUMERIC_T_JOINT_CHANNEL_EXCHANGE_SENSITIVITY_V1_BUILT "
        f"qdiff={summary['q_i_absolute_difference']} zdiff={summary['candidate_z_i_absolute_difference']}"
    )


if __name__ == "__main__":
    main()
