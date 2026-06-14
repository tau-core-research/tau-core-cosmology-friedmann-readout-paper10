#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "data/derived/joint_single_statistic_protocol_shell_v1.csv"
PROMOTION = ROOT / "data/derived/joint_numeric_t_joint_promotion_gate_v1_summary.csv"
OUT = ROOT / "data/derived/joint_numeric_channel_zi_binding_audit_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_channel_zi_binding_audit_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_channel_zi_binding_audit_v1.md"
CLAIM_BOUNDARY = "joint_numeric_channel_zi_binding_audit_not_scoring_not_validation"


FIELD_MAP = {
    "kids_lensing_cosebis_low_mode": {
        "candidate_numeric_field": "candidate_delta_chi2_vs_baseline",
        "candidate_numeric_source": "data/derived/kids1000_cosebis_endpoint_scoring_v1_summary.csv",
        "native_direction": "more_negative_is_better_vs_baseline",
        "source_status": "numeric_field_present_endpoint_score_not_validation",
        "standardization_status": "blocked_requires_shared_z_i_scale_rule",
    },
    "observer_path_basis_low_z": {
        "candidate_numeric_field": "delta_chi2_candidate_minus_best_control",
        "candidate_numeric_source": "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv",
        "native_direction": "more_negative_is_better_vs_best_control",
        "source_status": "numeric_field_present_permission_only_not_validation",
        "standardization_status": "blocked_requires_shared_z_i_scale_rule",
    },
    "desi_shape_time_readout": {
        "candidate_numeric_field": "delta_candidate_minus_best_control_score",
        "candidate_numeric_source": "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv",
        "native_direction": "more_positive_is_better_vs_best_control",
        "source_status": "numeric_field_present_permission_only_not_validation",
        "standardization_status": "blocked_requires_shared_z_i_scale_rule",
    },
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
    shell_rows = read_rows(SHELL)
    promotion = read_one(PROMOTION)
    if promotion["numeric_t_joint_promotion_ready"] != "false":
        raise SystemExit("z_i binding audit expects numeric promotion to remain blocked")

    rows: list[dict[str, str]] = []
    for shell in shell_rows:
        channel_id = shell["channel_id"]
        if channel_id not in FIELD_MAP:
            raise SystemExit(f"missing FIELD_MAP entry for {channel_id}")
        spec = FIELD_MAP[channel_id]
        source_path = ROOT / spec["candidate_numeric_source"]
        source = read_one(source_path)
        field = spec["candidate_numeric_field"]
        if field not in source:
            raise SystemExit(f"{source_path.relative_to(ROOT)} missing field {field}")
        rows.append(
            {
                "audit_id": "JOINT_NUMERIC_CHANNEL_ZI_BINDING_AUDIT_V1",
                "channel_order": shell["channel_order"],
                "channel_id": channel_id,
                "q_i": shell["q_i"],
                "candidate_numeric_source": spec["candidate_numeric_source"],
                "candidate_numeric_field": field,
                "candidate_numeric_value": source[field],
                "native_direction": spec["native_direction"],
                "source_status": spec["source_status"],
                "standardization_status": spec["standardization_status"],
                "numeric_z_i_defined": "false",
                "numeric_z_i_value": "not_computed",
                "signed_standardization_rule_frozen": "false",
                "same_rule_for_candidate_and_controls": "false",
                "computes_numeric_statistic_now": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    numeric_fields_present = sum(row["candidate_numeric_value"] not in {"", "nan"} for row in rows)
    summary = {
        "audit_id": "JOINT_NUMERIC_CHANNEL_ZI_BINDING_AUDIT_V1",
        "active_channel_count": str(len(rows)),
        "numeric_candidate_fields_present": str(numeric_fields_present),
        "numeric_z_i_defined_channels": "0",
        "signed_standardization_rule_frozen": "false",
        "same_rule_for_candidate_and_controls": "false",
        "numeric_channel_binding_ready": "false",
        "computes_numeric_statistic_now": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "next_required_action": "freeze_shared_signed_z_i_standardization_rule_for_candidate_and_controls_before_numeric_T_joint",
        "verdict": "NUMERIC_CHANNEL_FIELDS_PRESENT_ZI_STANDARDIZATION_BLOCKED",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric channel z_i binding audit v1",
                "",
                "**Doc class:** numeric-channel binding audit",
                "**Status:** numeric source fields present; z_i standardization blocked",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This audit maps each active channel to a candidate numeric source field",
                "that could later feed the shared statistic `T_joint = sum_i q_i z_i`.",
                "It intentionally does not compute `z_i`, because the common signed",
                "standardization rule for candidate and controls has not yet been frozen.",
                "",
                "Current result:",
                "",
                f"- active channels: `{summary['active_channel_count']}`",
                f"- numeric candidate fields present: `{summary['numeric_candidate_fields_present']}`",
                f"- numeric z_i defined channels: `{summary['numeric_z_i_defined_channels']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
            ]
        )
    )
    print(
        "JOINT_NUMERIC_CHANNEL_ZI_BINDING_AUDIT_V1_BUILT "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
