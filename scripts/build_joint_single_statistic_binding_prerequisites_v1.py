#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/source_manifest/joint_best_justified_kernel_manifest_v1.csv"
JLS_SUMMARY = ROOT / "data/derived/joint_likelihood_surrogate_requirements_gate_v1_summary.csv"
SCAFFOLD_SUMMARY = ROOT / "data/derived/joint_matched_control_suite_implementation_scaffold_v1_summary.csv"
OUT = ROOT / "data/derived/joint_single_statistic_binding_prerequisites_v1.csv"
SUMMARY = ROOT / "data/derived/joint_single_statistic_binding_prerequisites_v1_summary.csv"
DOC = ROOT / "docs/joint_single_statistic_binding_prerequisites_v1.md"
CLAIM_BOUNDARY = "joint_single_statistic_binding_prerequisites_not_scoring_not_validation"


CHANNEL_BINDINGS = {
    "kids_lensing_cosebis_low_mode": {
        "row_scope_artifact": "data/derived/kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1_summary.csv",
        "score_source_artifact": "data/derived/kids1000_cosebis_endpoint_scoring_v1_summary.csv",
        "covariance_artifact": "KiDS source-native 300x300 COVMAT via existing endpoint route",
        "nuisance_or_amplitude_rule": "source-frozen low-mode carrier; diagnostic endpoint amplitude preserved as existing artifact only",
    },
    "observer_path_basis_low_z": {
        "row_scope_artifact": "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv",
        "score_source_artifact": "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv",
        "covariance_artifact": "narrow 12-row permission replay covariance surrogate",
        "nuisance_or_amplitude_rule": "permission-only observer/path basis amplitude; no population validation",
    },
    "desi_shape_time_readout": {
        "row_scope_artifact": "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv",
        "score_source_artifact": "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv",
        "covariance_artifact": "small DESI shape-route covariance interface",
        "nuisance_or_amplitude_rule": "shape route replay amplitude frozen by source-side review; row-sensitive margin caveat",
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
    manifest = read_rows(MANIFEST)
    jls = read_one(JLS_SUMMARY)
    scaffold = read_one(SCAFFOLD_SUMMARY)
    active = [row for row in manifest if row["positive_support_allowed"] == "true"]
    active_ids = [row["channel_id"] for row in active]
    if active_ids != list(CHANNEL_BINDINGS):
        raise SystemExit(f"unexpected active channel order: {active_ids}")
    if jls["joint_statistic_defined"] != "false" or jls["endpoint_scoring_allowed"] != "false":
        raise SystemExit("joint likelihood gate must remain blocked before prerequisite binding")
    if scaffold["verdict"] != "JOINT_MATCHED_CONTROL_SUITE_IMPLEMENTATION_SCAFFOLD_FROZEN_NOT_RUN":
        raise SystemExit("matched-control scaffold must be frozen first")

    rows: list[dict[str, str]] = []
    for index, channel_id in enumerate(active_ids, start=1):
        binding = CHANNEL_BINDINGS[channel_id]
        manifest_row = next(row for row in active if row["channel_id"] == channel_id)
        row_scope_exists = (ROOT / binding["row_scope_artifact"]).exists()
        score_source_exists = (ROOT / binding["score_source_artifact"]).exists()
        rows.append(
            {
                "binding_id": f"JSS_BIND_{index:02d}",
                "channel_id": channel_id,
                "channel_order": str(index),
                "kernel_role": manifest_row["kernel_role"],
                "q_i": manifest_row["Q_i"],
                "row_scope_artifact": binding["row_scope_artifact"],
                "row_scope_artifact_exists": str(row_scope_exists).lower(),
                "score_source_artifact": binding["score_source_artifact"],
                "score_source_artifact_exists": str(score_source_exists).lower(),
                "covariance_artifact": binding["covariance_artifact"],
                "nuisance_or_amplitude_rule": binding["nuisance_or_amplitude_rule"],
                "candidate_control_same_statistic_required": "true",
                "candidate_control_same_covariance_required": "true",
                "ready_for_single_statistic_protocol": "false",
                "readiness_blocker": "covariance_or_independence_and_single_statistic_not_closed",
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
        "binding_gate_id": "JOINT_SINGLE_STATISTIC_BINDING_PREREQUISITES_V1",
        "active_channel_count": str(len(rows)),
        "active_channel_order": ";".join(active_ids),
        "row_scope_artifacts_present": str(sum(row["row_scope_artifact_exists"] == "true" for row in rows)),
        "score_source_artifacts_present": str(sum(row["score_source_artifact_exists"] == "true" for row in rows)),
        "candidate_control_same_statistic_required": "true",
        "candidate_control_same_covariance_required": "true",
        "single_joint_statistic_defined": "false",
        "covariance_or_independence_closed": "false",
        "ready_for_single_statistic_protocol": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "next_required_action": "complete_covariance_or_independence_review_before_instantiating_single_statistic_protocol",
        "verdict": "JOINT_SINGLE_STATISTIC_BINDING_PREREQUISITES_FROZEN_PROTOCOL_BLOCKED",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint single-statistic binding prerequisites v1",
                "",
                "**Doc class:** binding prerequisites ledger",
                "**Status:** not scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This ledger freezes the channel-level inputs that a future single",
                "joint statistic must bind: active-channel order, row-scope artifact,",
                "score-source artifact, covariance object, and nuisance/amplitude rule.",
                "It does not define the statistic and does not run a replay.",
                "",
                "Summary:",
                "",
                f"- active channels: `{summary['active_channel_order']}`",
                f"- row-scope artifacts present: `{summary['row_scope_artifacts_present']}/{summary['active_channel_count']}`",
                f"- score-source artifacts present: `{summary['score_source_artifacts_present']}/{summary['active_channel_count']}`",
                f"- single statistic defined: `{summary['single_joint_statistic_defined']}`",
                f"- covariance/independence closed: `{summary['covariance_or_independence_closed']}`",
                f"- scoring allowed: `{summary['endpoint_scoring_allowed']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
            ]
        )
    )
    print(
        "JOINT_SINGLE_STATISTIC_BINDING_PREREQUISITES_V1_BUILT "
        f"verdict={summary['verdict']} channels={summary['active_channel_count']}"
    )


if __name__ == "__main__":
    main()
