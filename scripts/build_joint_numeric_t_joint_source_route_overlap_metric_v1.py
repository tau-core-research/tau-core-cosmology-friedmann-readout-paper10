#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PENALTY_REQ = ROOT / "data/derived/joint_numeric_t_joint_channel_distinguishability_penalty_requirements_v1_summary.csv"
OUT = ROOT / "data/derived/joint_numeric_t_joint_source_route_overlap_metric_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_source_route_overlap_metric_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_source_route_overlap_metric_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_source_route_overlap_metric_not_scoring_not_validation"


ROUTES = {
    "observer_path_basis_low_z": {
        "source_family": "observer_path_low_z",
        "route_tags": {
            "observer_path",
            "low_z",
            "sky_direction",
            "z_center",
            "metric_environment",
            "permission_replay",
        },
        "source_artifact": "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv",
        "control_artifact": "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_grid.csv",
        "claim_boundary_source": "v2_observer_basis_authorized_replay_permission_only_not_validation",
    },
    "desi_shape_time_readout": {
        "source_family": "desi_shape_time",
        "route_tags": {
            "desi_bao",
            "time_readout",
            "clock_slope_shape",
            "radial_bao",
            "adjacent_first_difference",
            "permission_replay",
        },
        "source_artifact": "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv",
        "control_artifact": "data/derived/paper10_desi_shape_route_authorized_replay_v1_grid.csv",
        "claim_boundary_source": "paper10_desi_shape_route_authorized_replay_permission_only_not_validation",
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
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: float) -> str:
    return f"{value:.12e}"


def main() -> None:
    req = read_one(PENALTY_REQ)
    if req["numeric_t_joint_rescoring_allowed"] != "false":
        raise SystemExit("overlap metric scaffold requires rescoring to remain forbidden")

    channel_a, channel_b = req["channel_pair"].split("|")
    tags_a = ROUTES[channel_a]["route_tags"]
    tags_b = ROUTES[channel_b]["route_tags"]
    intersection = tags_a & tags_b
    union = tags_a | tags_b
    jaccard_overlap = len(intersection) / len(union)
    jaccard_distance = 1.0 - jaccard_overlap

    rows = []
    for channel in [channel_a, channel_b]:
        route = ROUTES[channel]
        rows.append(
            {
                "metric_id": "JOINT_NUMERIC_T_JOINT_SOURCE_ROUTE_OVERLAP_METRIC_V1",
                "channel_id": channel,
                "source_family": route["source_family"],
                "route_tags": ";".join(sorted(route["route_tags"])),
                "tag_count": str(len(route["route_tags"])),
                "source_artifact": route["source_artifact"],
                "control_artifact": route["control_artifact"],
                "claim_boundary_source": route["claim_boundary_source"],
                "uses_endpoint_scores_or_residuals": "false",
                "numeric_t_joint_rescoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    summary = {
        "metric_id": "JOINT_NUMERIC_T_JOINT_SOURCE_ROUTE_OVERLAP_METRIC_V1",
        "channel_pair": req["channel_pair"],
        "shared_route_tags": ";".join(sorted(intersection)) if intersection else "none",
        "shared_route_tag_count": str(len(intersection)),
        "union_route_tag_count": str(len(union)),
        "jaccard_overlap": fmt(jaccard_overlap),
        "jaccard_distance": fmt(jaccard_distance),
        "metric_status": "CAVEATED_SOURCE_NATIVE_TAG_DISTANCE_AVAILABLE",
        "penalty_admissible_now": "false",
        "why_not_penalty": "tag_distance_is_route_level_only_small_N_and_candidate_control_symmetry_still_open",
        "uses_endpoint_scores_or_residuals": "false",
        "numeric_t_joint_rescoring_allowed": "false",
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
                "# Joint numeric T_joint source-route overlap metric v1",
                "",
                "**Doc class:** residual-blind source-route overlap scaffold.",
                "**Status:** caveated metric available; not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This artifact defines a route-tag Jaccard overlap between the",
                "observer-path low-z channel and the DESI shape/time channel. The tags",
                "are source-route descriptors only; endpoint residuals, endpoint scores,",
                "and the thin `T_joint` margin are not used.",
                "",
                f"Shared tags: `{summary['shared_route_tags']}`.",
                f"Jaccard overlap: `{summary['jaccard_overlap']}`.",
                f"Jaccard distance: `{summary['jaccard_distance']}`.",
                "",
                "The metric supports the statement that the source routes are largely",
                "distinct at the route-tag level. It still does not authorize a penalty",
                "or any numeric `T_joint` rescoring, because the small-N balance and",
                "candidate/control symmetry requirements remain open.",
                "",
            ]
        )
    )
    print(
        "JOINT_NUMERIC_T_JOINT_SOURCE_ROUTE_OVERLAP_METRIC_V1_BUILT "
        f"distance={summary['jaccard_distance']}"
    )


if __name__ == "__main__":
    main()
