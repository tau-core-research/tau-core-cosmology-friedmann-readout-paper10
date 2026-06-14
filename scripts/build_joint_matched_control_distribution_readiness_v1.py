#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data/derived/joint_signed_zi_standardization_protocol_v1_summary.csv"
OUT = ROOT / "data/derived/joint_matched_control_distribution_readiness_v1.csv"
SUMMARY = ROOT / "data/derived/joint_matched_control_distribution_readiness_v1_summary.csv"
DOC = ROOT / "docs/joint_matched_control_distribution_readiness_v1.md"
CLAIM_BOUNDARY = "joint_matched_control_distribution_readiness_not_scoring_not_validation"


CHANNELS = [
    {
        "channel_id": "kids_lensing_cosebis_low_mode",
        "control_source_artifact": "data/derived/kids1000_cosebis_endpoint_scoring_diagnostics_v1_top_nulls.csv",
        "control_value_field": "delta_chi2_vs_baseline",
        "candidate_field": "candidate_delta_chi2_vs_baseline",
        "raw_control_distribution_status": "PARTIAL_TOP_NULLS_ONLY",
        "readiness_status": "BLOCKED_NEEDS_FULL_CONTROL_EXPORT",
        "caveat": "family summary reports 1008 controls, but the current repo artifact exposes only top-null rows plus family aggregates",
    },
    {
        "channel_id": "observer_path_basis_low_z",
        "control_source_artifact": "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_grid.csv",
        "control_value_field": "chi2_observer_basis_replay",
        "candidate_field": "chi2_observer_basis_replay",
        "raw_control_distribution_status": "GRID_WITH_CONTROL_BRANCHES_AVAILABLE",
        "readiness_status": "READY_FOR_FUTURE_ZI_DISTRIBUTION_BUILD",
        "caveat": "permission-only replay grid; not validation",
    },
    {
        "channel_id": "desi_shape_time_readout",
        "control_source_artifact": "data/derived/paper10_desi_shape_route_authorized_replay_v1_grid.csv",
        "control_value_field": "shape_quadratic_score",
        "candidate_field": "shape_quadratic_score",
        "raw_control_distribution_status": "SMALL_SHAPE_BOUND_CONTROL_SET_AVAILABLE",
        "readiness_status": "CAVEATED_READY_SMALL_N",
        "caveat": "only six non-candidate control rows; adequate for a caveated pilot scale check, not population validation",
    },
]


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


def count_controls(channel_id: str, rows: list[dict[str, str]]) -> int:
    if channel_id == "kids_lensing_cosebis_low_mode":
        return sum(1 for row in rows if row.get("control_family") or row.get("operator"))
    if channel_id == "observer_path_basis_low_z":
        return sum(1 for row in rows if row["branch"] not in {"candidate", "baseline_only"})
    if channel_id == "desi_shape_time_readout":
        return sum(1 for row in rows if row["control_family"] != "candidate")
    raise SystemExit(f"unknown channel: {channel_id}")


def main() -> None:
    protocol = read_one(PROTOCOL)
    if protocol["signed_standardization_rule_frozen"] != "true":
        raise SystemExit("signed z_i protocol must be frozen before control readiness audit")
    rows: list[dict[str, str]] = []
    for order, spec in enumerate(CHANNELS, start=1):
        source = ROOT / spec["control_source_artifact"]
        source_rows = read_rows(source)
        control_count = count_controls(spec["channel_id"], source_rows)
        rows.append(
            {
                "readiness_id": "JOINT_MATCHED_CONTROL_DISTRIBUTION_READINESS_V1",
                "channel_order": str(order),
                "channel_id": spec["channel_id"],
                "control_source_artifact": spec["control_source_artifact"],
                "control_value_field": spec["control_value_field"],
                "candidate_field": spec["candidate_field"],
                "raw_rows_available": str(len(source_rows)),
                "matched_control_rows_available": str(control_count),
                "raw_control_distribution_status": spec["raw_control_distribution_status"],
                "readiness_status": spec["readiness_status"],
                "caveat": spec["caveat"],
                "center_scale_computable_now": "false",
                "numeric_z_i_defined": "false",
                "computes_numeric_statistic_now": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    blocked = sum("BLOCKED" in row["readiness_status"] for row in rows)
    caveated = sum("CAVEATED" in row["readiness_status"] for row in rows)
    ready = sum(row["readiness_status"] == "READY_FOR_FUTURE_ZI_DISTRIBUTION_BUILD" for row in rows)
    summary = {
        "readiness_id": "JOINT_MATCHED_CONTROL_DISTRIBUTION_READINESS_V1",
        "active_channel_count": str(len(rows)),
        "ready_channels": str(ready),
        "caveated_ready_channels": str(caveated),
        "blocked_channels": str(blocked),
        "all_channels_ready_for_numeric_zi": "false",
        "center_scale_computable_now": "false",
        "numeric_z_i_defined_channels": "0",
        "computes_numeric_statistic_now": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "next_required_action": "export_or_rebuild_full_kids_matched_control_distribution_then_authorize_numeric_zi_distribution_build",
        "verdict": "MATCHED_CONTROL_DISTRIBUTIONS_PARTIAL_KIDS_BLOCKED",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint matched-control distribution readiness v1",
                "",
                "**Doc class:** matched-control distribution readiness audit",
                "**Status:** partial; not scoring; not validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "The frozen signed `z_i` protocol requires matched-control distributions",
                "to define each channel center and scale. This audit checks whether the",
                "current repository artifacts expose those raw control distributions.",
                "",
                "Current result:",
                "",
                f"- ready channels: `{summary['ready_channels']}`",
                f"- caveated-ready channels: `{summary['caveated_ready_channels']}`",
                f"- blocked channels: `{summary['blocked_channels']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "The KiDS channel remains blocked because the current repository exposes",
                "top-null and family-summary artifacts, not the full raw matched-control",
                "distribution needed by the frozen median/MAD rule.",
                "",
            ]
        )
    )
    print(
        "JOINT_MATCHED_CONTROL_DISTRIBUTION_READINESS_V1_BUILT "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
