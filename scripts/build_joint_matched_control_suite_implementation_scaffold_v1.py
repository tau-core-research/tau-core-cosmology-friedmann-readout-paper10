#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQ = ROOT / "data/derived/joint_matched_control_suite_requirements_gate_v1.csv"
REQ_SUMMARY = ROOT / "data/derived/joint_matched_control_suite_requirements_gate_v1_summary.csv"
OUT = ROOT / "data/derived/joint_matched_control_suite_implementation_scaffold_v1.csv"
SUMMARY = ROOT / "data/derived/joint_matched_control_suite_implementation_scaffold_v1_summary.csv"
DOC = ROOT / "docs/joint_matched_control_suite_implementation_scaffold_v1.md"
CLAIM_BOUNDARY = "joint_matched_control_suite_implementation_scaffold_not_scoring_not_validation"


IMPLEMENTATION_SPECS = {
    "JMC_REQ_01_SHUFFLED_CHANNEL": {
        "future_builder": "scripts/build_joint_control_shuffle_channel_labels_v1.py",
        "future_validator": "scripts/validate_joint_control_shuffle_channel_labels_v1.py",
        "future_artifact": "data/derived/joint_control_shuffle_channel_labels_v1.csv",
        "required_freeze_input": "active_channel_order; row_scope; random_seed_manifest; single_joint_statistic_id",
        "minimum_control_count_rule": ">=1000 deterministic shuffles or exhaustive if smaller",
    },
    "JMC_REQ_02_WRONG_CHANNEL": {
        "future_builder": "scripts/build_joint_control_wrong_channel_family_v1.py",
        "future_validator": "scripts/validate_joint_control_wrong_channel_family_v1.py",
        "future_artifact": "data/derived/joint_control_wrong_channel_family_v1.csv",
        "required_freeze_input": "active_channel_order; allowed_wrong_family_manifest; single_joint_statistic_id",
        "minimum_control_count_rule": "one source-compatible wrong family per active channel where available",
    },
    "JMC_REQ_03_SIGN_FLIP": {
        "future_builder": "scripts/build_joint_control_sign_flip_v1.py",
        "future_validator": "scripts/validate_joint_control_sign_flip_v1.py",
        "future_artifact": "data/derived/joint_control_sign_flip_v1.csv",
        "required_freeze_input": "active_channel_order; sign_flip_enumeration_rule; single_joint_statistic_id",
        "minimum_control_count_rule": "complete nontrivial sign-flip enumeration for active blocks",
    },
    "JMC_REQ_04_BLOCK_DROP": {
        "future_builder": "scripts/build_joint_control_block_drop_v1.py",
        "future_validator": "scripts/validate_joint_control_block_drop_v1.py",
        "future_artifact": "data/derived/joint_control_block_drop_v1.csv",
        "required_freeze_input": "active_channel_order; block_partition_manifest; single_joint_statistic_id",
        "minimum_control_count_rule": "all leave-one-active-probe and one all-but-lensing diagnostic",
    },
    "JMC_REQ_05_NULL_READOUT": {
        "future_builder": "scripts/build_joint_control_null_readout_v1.py",
        "future_validator": "scripts/validate_joint_control_null_readout_v1.py",
        "future_artifact": "data/derived/joint_control_null_readout_v1.csv",
        "required_freeze_input": "source_frozen_null_readout_manifest; single_joint_statistic_id",
        "minimum_control_count_rule": "all predeclared null/readout-trivial channels",
    },
    "JMC_REQ_06_SCOPE_AND_LEAKAGE": {
        "future_builder": "scripts/build_joint_control_scope_leakage_ledger_v1.py",
        "future_validator": "scripts/validate_joint_control_scope_leakage_ledger_v1.py",
        "future_artifact": "data/derived/joint_control_scope_leakage_ledger_v1.csv",
        "required_freeze_input": "forbidden_field_schema; row_scope; label_freeze_artifacts; single_joint_statistic_id",
        "minimum_control_count_rule": "one complete leakage ledger row per active channel and control family",
    },
    "JMC_REQ_07_SHARED_STATISTIC_BINDING": {
        "future_builder": "scripts/build_joint_single_statistic_binding_v1.py",
        "future_validator": "scripts/validate_joint_single_statistic_binding_v1.py",
        "future_artifact": "data/derived/joint_single_statistic_binding_v1.csv",
        "required_freeze_input": "single_joint_statistic_protocol; nuisance_rule; row_scope",
        "minimum_control_count_rule": "exactly one statistic id shared by candidate and every control",
    },
    "JMC_REQ_08_COVARIANCE_BINDING": {
        "future_builder": "scripts/build_joint_covariance_binding_v1.py",
        "future_validator": "scripts/validate_joint_covariance_binding_v1.py",
        "future_artifact": "data/derived/joint_covariance_binding_v1.csv",
        "required_freeze_input": "reviewed_cross_probe_covariance_or_reviewed_block_diagonal_independence_response",
        "minimum_control_count_rule": "one reviewed covariance object shared by candidate and every control",
    },
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
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
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    req_rows = read_rows(REQ)
    req_summary = read_one(REQ_SUMMARY)
    if req_summary["verdict"] != "JOINT_MATCHED_CONTROL_SUITE_REQUIREMENTS_FROZEN_IMPLEMENTATION_BLOCKED":
        raise SystemExit("requirements gate must be frozen and implementation-blocked first")
    if req_summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("requirements gate unexpectedly allows endpoint scoring")

    rows: list[dict[str, str]] = []
    for req in req_rows:
        spec = IMPLEMENTATION_SPECS.get(req["control_id"])
        if spec is None:
            raise SystemExit(f"missing implementation spec for {req['control_id']}")
        hard_blocked = req["status"] == "blocked"
        scaffold_status = "blocked_by_upstream_gate" if hard_blocked else "planned_not_implemented"
        rows.append(
            {
                "scaffold_id": req["control_id"].replace("JMC_REQ", "JMC_IMPL"),
                "source_requirement_id": req["control_id"],
                "control_family": req["control_family"],
                "future_builder": spec["future_builder"],
                "future_validator": spec["future_validator"],
                "future_artifact": spec["future_artifact"],
                "required_freeze_input": spec["required_freeze_input"],
                "minimum_control_count_rule": spec["minimum_control_count_rule"],
                "scaffold_status": scaffold_status,
                "upstream_blocker": req["implementation_blocker"],
                "candidate_and_control_same_statistic_required": "true",
                "candidate_and_control_same_covariance_required": "true",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    write_csv(OUT, rows)
    summary = {
        "scaffold_id": "JOINT_MATCHED_CONTROL_SUITE_IMPLEMENTATION_SCAFFOLD_V1",
        "parent_gate": req_summary["gate_id"],
        "parent_verdict": req_summary["verdict"],
        "control_families": str(len(rows)),
        "planned_not_implemented": str(sum(1 for row in rows if row["scaffold_status"] == "planned_not_implemented")),
        "blocked_by_upstream_gate": str(sum(1 for row in rows if row["scaffold_status"] == "blocked_by_upstream_gate")),
        "future_builders_declared": str(sum(1 for row in rows if row["future_builder"])),
        "future_validators_declared": str(sum(1 for row in rows if row["future_validator"])),
        "implementation_ready": "false",
        "single_joint_statistic_required": "true",
        "reviewed_covariance_or_independence_required": "true",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "next_required_action": "complete_block_diagonal_or_covariance_review_then_build_single_statistic_binding",
        "verdict": "JOINT_MATCHED_CONTROL_SUITE_IMPLEMENTATION_SCAFFOLD_FROZEN_NOT_RUN",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# Joint matched control-suite implementation scaffold v1",
                "",
                "**Doc class:** implementation scaffold",
                "**Status:** not run; not scoring; not endpoint validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This scaffold turns the frozen matched-control requirements into a",
                "future implementation checklist. It declares future builder names,",
                "validators, output artifacts, required freeze inputs, and minimum",
                "control-count rules. It does not create control vectors, residuals,",
                "likelihoods, fit statistics, or endpoint scores.",
                "",
                "The two binding rows remain hard-blocked:",
                "",
                "- single-statistic binding: no final joint statistic is defined yet;",
                "- covariance binding: no reviewed cross-probe covariance or reviewed",
                "  block-diagonal independence response is available yet.",
                "",
                "Summary:",
                "",
                f"- control families: `{summary['control_families']}`",
                f"- planned but not implemented: `{summary['planned_not_implemented']}`",
                f"- blocked by upstream gate: `{summary['blocked_by_upstream_gate']}`",
                f"- implementation ready: `{summary['implementation_ready']}`",
                f"- endpoint scoring allowed: `{summary['endpoint_scoring_allowed']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
            ]
        )
    )
    print(
        "JOINT_MATCHED_CONTROL_SUITE_IMPLEMENTATION_SCAFFOLD_V1_BUILT "
        f"verdict={summary['verdict']} controls={summary['control_families']}"
    )


if __name__ == "__main__":
    main()
