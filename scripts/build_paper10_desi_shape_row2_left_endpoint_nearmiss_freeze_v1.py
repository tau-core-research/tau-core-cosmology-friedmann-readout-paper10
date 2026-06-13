#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_policy_v1.csv"
SCOUT = ROOT / "data/derived/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.csv"
SCOUT_SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
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


def write_doc(summary: dict[str, str]) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Paper10 DESI shape row2 left-endpoint near-miss freeze v1",
                "",
                "**Doc class:** source-side caveated near-miss freeze",
                "**Reader role:** source-acquisition auditor / reviewer",
                "**Status:** left endpoint still blocked, not replay, not validation",
                "**Canonical parent:** Paper10 DESI shape-route replay chain",
                "",
                "This artifact freezes the relaxed independent left-endpoint context found",
                "by the row-2 endpoint-pair independence scout. It does not change the",
                "strict endpoint-pair gate.",
                "",
                "Frozen result:",
                "",
                f"- relaxed independent left candidates: `{summary['relaxed_independent_left_candidate_count']}`",
                f"- closest relaxed independent candidate: `{summary['closest_relaxed_independent_candidate']}`",
                f"- closest relaxed independent delta-z: `{summary['closest_relaxed_independent_delta_z']}`",
                f"- strict independent left support count: `{summary['strict_independent_left_support_count']}`",
                f"- left endpoint release allowed: `{summary['left_endpoint_release_allowed']}`",
                "",
                "Interpretation:",
                "",
                "Stern et al. (2010) and Moresco et al. (2012) are useful left-endpoint",
                "near-miss context, but both are outside the frozen strict `|Delta z| <= 0.05`",
                "endpoint window. They can motivate a separate source-window review or",
                "source-native shape support search; they do not authorize replay.",
                "",
                "Claim boundary:",
                "",
                "```text",
                summary["claim_boundary"],
                "```",
                "",
                f"Machine verdict: `{summary['verdict']}`.",
                "",
            ]
        )
    )


def main() -> None:
    policy = read_one(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad row2 left near-miss policy claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    scout_summary = read_one(SCOUT_SUMMARY)
    if scout_summary["endpoint_pair_independence_satisfied"] != "false":
        raise SystemExit("near-miss freeze expects endpoint-pair independence to remain unsatisfied")
    if scout_summary["left_strict_independent_count"] != "0":
        raise SystemExit("near-miss freeze expects no strict independent left support")

    relaxed = [
        row for row in read_rows(SCOUT)
        if row["endpoint_label"] == "left"
        and row["support_class"] == "relaxed_independent_endpoint_context"
        and row["independent_of_current_endpoint_family"] == "true"
        and row["within_relaxed_endpoint_window"] == "true"
        and row["within_strict_endpoint_window"] == "false"
    ]
    relaxed = sorted(relaxed, key=lambda row: float(row["candidate_abs_delta_z"]))
    if not relaxed:
        raise SystemExit("expected at least one relaxed independent left near-miss")

    rows = []
    for rank, row in enumerate(relaxed, start=1):
        rows.append(
            {
                "freeze_id": policy["freeze_id"],
                "shape_row": "2",
                "endpoint_label": "left",
                "endpoint_z": row["endpoint_z"],
                "candidate_rank_by_abs_delta_z": str(rank),
                "candidate_z": row["candidate_z"],
                "candidate_abs_delta_z": row["candidate_abs_delta_z"],
                "candidate_Hz": row["candidate_Hz"],
                "candidate_errHz": row["candidate_errHz"],
                "candidate_reference": row["candidate_reference"],
                "candidate_reference_family": row["candidate_reference_family"],
                "independent_of_current_endpoint_family": row["independent_of_current_endpoint_family"],
                "within_strict_endpoint_window": row["within_strict_endpoint_window"],
                "within_relaxed_endpoint_window": row["within_relaxed_endpoint_window"],
                "nearmiss_role": "caveated_left_endpoint_context_not_strict_support",
                "left_endpoint_release_allowed": "false",
                "endpoint_pair_replacement_candidate": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, rows)

    summary = {
        "freeze_id": policy["freeze_id"],
        "status": "DESI_SHAPE_ROW2_LEFT_ENDPOINT_NEARMISS_CONTEXT_FROZEN_NOT_REPLAY_NOT_VALIDATION",
        "strict_endpoint_window_abs_dz": policy["strict_endpoint_window_abs_dz"],
        "relaxed_endpoint_window_abs_dz": policy["relaxed_endpoint_window_abs_dz"],
        "relaxed_independent_left_candidate_count": str(len(rows)),
        "strict_independent_left_support_count": "0",
        "closest_relaxed_independent_candidate": rows[0]["candidate_reference"],
        "closest_relaxed_independent_candidate_z": rows[0]["candidate_z"],
        "closest_relaxed_independent_delta_z": rows[0]["candidate_abs_delta_z"],
        "left_endpoint_release_allowed": "false",
        "endpoint_pair_independence_satisfied": "false",
        "row2_promotion_ready": "false",
        "shape_route_promotion_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "row2_left_endpoint_has_relaxed_independent_nearmisses_but_no_strict_support",
        "recommended_next_action": "prepare_left_endpoint_window_review_or_find_source_native_shape_support_before_promotion",
    }
    write_csv(SUMMARY, [summary])
    write_doc(summary)


if __name__ == "__main__":
    main()
