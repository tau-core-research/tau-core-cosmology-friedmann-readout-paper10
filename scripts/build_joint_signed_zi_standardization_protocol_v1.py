#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZI_AUDIT = ROOT / "data/derived/joint_numeric_channel_zi_binding_audit_v1.csv"
ZI_SUMMARY = ROOT / "data/derived/joint_numeric_channel_zi_binding_audit_v1_summary.csv"
OUT = ROOT / "data/derived/joint_signed_zi_standardization_protocol_v1.csv"
SUMMARY = ROOT / "data/derived/joint_signed_zi_standardization_protocol_v1_summary.csv"
DOC = ROOT / "docs/joint_signed_zi_standardization_protocol_v1.md"
CLAIM_BOUNDARY = "joint_signed_zi_standardization_protocol_not_scoring_not_validation"


SIGN_BY_DIRECTION = {
    "more_negative_is_better_vs_baseline": "-1",
    "more_negative_is_better_vs_best_control": "-1",
    "more_positive_is_better_vs_best_control": "+1",
}


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
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    audit_rows = read_rows(ZI_AUDIT)
    audit_summary = read_one(ZI_SUMMARY)
    if audit_summary["numeric_candidate_fields_present"] != "3":
        raise SystemExit("all numeric candidate fields must be present before freezing sign protocol")
    if audit_summary["numeric_z_i_defined_channels"] != "0":
        raise SystemExit("signed protocol must be frozen before z_i is computed")

    rows: list[dict[str, str]] = []
    for row in audit_rows:
        direction = row["native_direction"]
        if direction not in SIGN_BY_DIRECTION:
            raise SystemExit(f"unknown native direction: {direction}")
        sign = SIGN_BY_DIRECTION[direction]
        rows.append(
            {
                "protocol_id": "JOINT_SIGNED_ZI_STANDARDIZATION_PROTOCOL_V1",
                "channel_order": row["channel_order"],
                "channel_id": row["channel_id"],
                "native_numeric_field": row["candidate_numeric_field"],
                "native_direction": direction,
                "support_positive_sign": sign,
                "signed_raw_evidence_formula": f"e_i = ({sign}) * native_value",
                "center_rule": "median_of_matched_controls_only",
                "scale_rule": "MAD1p4826_of_matched_controls_only_else_declared_blocker",
                "z_i_formula": "z_i = (e_i - center_i) / scale_i",
                "candidate_may_define_center_or_scale": "false",
                "same_rule_for_candidate_and_controls": "true",
                "requires_numeric_control_distribution": "true",
                "signed_standardization_rule_frozen": "true",
                "numeric_z_i_defined": "false",
                "numeric_z_i_value": "not_computed",
                "computes_numeric_statistic_now": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    summary = {
        "protocol_id": "JOINT_SIGNED_ZI_STANDARDIZATION_PROTOCOL_V1",
        "active_channel_count": str(len(rows)),
        "signed_standardization_rule_frozen": "true",
        "same_rule_for_candidate_and_controls": "true",
        "center_rule": "median_of_matched_controls_only",
        "scale_rule": "MAD1p4826_of_matched_controls_only_else_declared_blocker",
        "candidate_may_define_center_or_scale": "false",
        "numeric_control_distribution_required": "true",
        "numeric_z_i_defined_channels": "0",
        "numeric_t_joint_ready": "false",
        "computes_numeric_statistic_now": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "next_required_action": "build_numeric_matched_control_distributions_under_this_frozen_signed_z_i_protocol",
        "verdict": "SIGNED_ZI_STANDARDIZATION_PROTOCOL_FROZEN_NUMERIC_ZI_BLOCKED",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint signed z_i standardization protocol v1",
                "",
                "**Doc class:** signed standardization protocol",
                "**Status:** rule frozen; numeric z_i blocked; not scoring; not validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This protocol freezes the sign convention and future standardization",
                "rule for channel-level evidence before any numeric `T_joint` scoring.",
                "For each channel, the native source value is first mapped to a",
                "support-positive raw evidence value `e_i`. The future `z_i` may only",
                "be standardized using the matched-control distribution, not the",
                "candidate value.",
                "",
                "Frozen rule:",
                "",
                "```text",
                "e_i = sign_i * native_value",
                "center_i = median(e_i over matched controls only)",
                "scale_i = MAD1.4826(e_i over matched controls only)",
                "z_i = (e_i - center_i) / scale_i",
                "```",
                "",
                "If the matched-control scale is zero or unavailable, the channel remains",
                "blocked rather than being rescued by a fitted scale.",
                "",
                "Current result:",
                "",
                f"- active channels: `{summary['active_channel_count']}`",
                f"- signed standardization rule frozen: `{summary['signed_standardization_rule_frozen']}`",
                f"- numeric z_i defined channels: `{summary['numeric_z_i_defined_channels']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
            ]
        )
    )
    print(
        "JOINT_SIGNED_ZI_STANDARDIZATION_PROTOCOL_V1_BUILT "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
