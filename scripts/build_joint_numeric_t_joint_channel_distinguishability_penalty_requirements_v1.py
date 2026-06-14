#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCHANGE = ROOT / "data/derived/joint_numeric_t_joint_channel_exchange_sensitivity_v1_summary.csv"
EXCHANGE_ROWS = ROOT / "data/derived/joint_numeric_t_joint_channel_exchange_sensitivity_v1.csv"
OUT = ROOT / "data/derived/joint_numeric_t_joint_channel_distinguishability_penalty_requirements_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_channel_distinguishability_penalty_requirements_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_channel_distinguishability_penalty_requirements_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_channel_distinguishability_penalty_requirements_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    exchange = read_one(EXCHANGE)
    rows_in = read_rows(EXCHANGE_ROWS)
    if exchange["source_routes_distinct"] != "true":
        raise SystemExit("source routes are not distinct; no penalty requirement gate can be built")

    min_controls = min(int(row["matched_control_count"]) for row in rows_in)
    caveated_small_n = any("SMALL_N" in row["readiness_status"] or int(row["matched_control_count"]) < 20 for row in rows_in)

    rows = [
        {
            "gate_id": "JOINT_NUMERIC_T_JOINT_CHANNEL_DISTINGUISHABILITY_PENALTY_REQUIREMENTS_V1",
            "requirement_id": "CDP_R1_SOURCE_ROUTE_DISTINCTNESS",
            "status": "SATISFIED",
            "evidence": f"same_score_source_artifact={exchange['same_score_source_artifact']}; same_control_source_artifact={exchange['same_control_source_artifact']}",
            "required_for_penalty": "source routes must be distinct before any channel-exchange penalty is meaningful",
            "forbidden_shortcut": "do_not_use_endpoint_margin_to_define_route_distinctness",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "JOINT_NUMERIC_T_JOINT_CHANNEL_DISTINGUISHABILITY_PENALTY_REQUIREMENTS_V1",
            "requirement_id": "CDP_R2_SOURCE_NATIVE_SEPARATION_METRIC",
            "status": "OPEN",
            "evidence": "no frozen source-native distance/overlap metric between observer-path and DESI shape/time source spaces",
            "required_for_penalty": "derive a residual-blind distance, overlap, or orthogonality measure between source routes",
            "forbidden_shortcut": "do_not_set_penalty_from_T_joint_margin_or_endpoint_score",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "JOINT_NUMERIC_T_JOINT_CHANNEL_DISTINGUISHABILITY_PENALTY_REQUIREMENTS_V1",
            "requirement_id": "CDP_R3_SMALL_N_BALANCE",
            "status": "OPEN_CAVEATED" if caveated_small_n else "SATISFIED",
            "evidence": f"matched_control_count_pair={exchange['matched_control_count_pair']}; min_controls={min_controls}",
            "required_for_penalty": "penalty must not overweight the small-N DESI shape/time route relative to the larger observer-path control population",
            "forbidden_shortcut": "do_not_treat_6_control_DESI_route_as_population-grade_without_a_caveat",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "JOINT_NUMERIC_T_JOINT_CHANNEL_DISTINGUISHABILITY_PENALTY_REQUIREMENTS_V1",
            "requirement_id": "CDP_R4_CANDIDATE_CONTROL_SYMMETRY",
            "status": "REQUIRED_NOT_BUILT",
            "evidence": "penalty candidate/control symmetry has not been implemented",
            "required_for_penalty": "same distinguishability rule must be computable for candidate and all controls from frozen source manifests",
            "forbidden_shortcut": "do_not_apply_penalty_only_to_shuffled_controls_or_only_after_seeing_winner",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    open_count = sum(row["status"] != "SATISFIED" for row in rows)
    summary = {
        "gate_id": "JOINT_NUMERIC_T_JOINT_CHANNEL_DISTINGUISHABILITY_PENALTY_REQUIREMENTS_V1",
        "channel_pair": exchange["channel_pair"],
        "requirements_total": str(len(rows)),
        "requirements_satisfied": str(sum(row["status"] == "SATISFIED" for row in rows)),
        "requirements_open_or_caveated": str(open_count),
        "source_route_distinctness_satisfied": "true",
        "source_native_penalty_admissible_now": "false",
        "numeric_t_joint_rescoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": "PENALTY_NOT_ADMISSIBLE_YET_REQUIREMENTS_FROZEN",
        "next_required_action": "build_residual_blind_source_native_overlap_metric_then_review_before_any_rescoring",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint channel-distinguishability penalty requirements v1",
                "",
                "**Doc class:** penalty requirements gate.",
                "**Status:** requirements frozen; penalty not admissible yet; not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This gate prevents the thin shuffled-channel margin from being fixed",
                "by an endpoint-driven penalty. It records that the observer-path and",
                "DESI shape/time channels are source-distinct, but that source-route",
                "distinctness alone is not enough to modify `T_joint`.",
                "",
                "Before any channel-distinguishability penalty can be used, a residual-blind",
                "source-native separation metric must be built, small-N imbalance must remain",
                "caveated, and the same rule must apply symmetrically to candidate and controls.",
                "",
                f"Verdict: `{summary['verdict']}`.",
                f"Next action: `{summary['next_required_action']}`.",
                "",
            ]
        )
    )
    print(
        "JOINT_NUMERIC_T_JOINT_CHANNEL_DISTINGUISHABILITY_PENALTY_REQUIREMENTS_V1_BUILT "
        f"open={summary['requirements_open_or_caveated']}"
    )


if __name__ == "__main__":
    main()
