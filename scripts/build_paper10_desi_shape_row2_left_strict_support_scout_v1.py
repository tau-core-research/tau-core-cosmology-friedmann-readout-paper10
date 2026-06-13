#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_row2_left_strict_support_scout_policy_v1.csv"
SOURCE_PLAN = ROOT / "data/derived/paper10_desi_shape_row2_post_window_review_source_plan_v1_summary.csv"
CC_TABLE = ROOT / "data/raw/hz_compilation/cosmic_chronometers_hz/data_CC.dat"
OUT = ROOT / "data/derived/paper10_desi_shape_row2_left_strict_support_scout_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_left_strict_support_scout_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_left_strict_support_scout_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_left_strict_support_scout_not_validation"
ROW2_LEFT_Z = 0.934
CURRENT_LEFT_FAMILY = "Simon et al."


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
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


def read_cc_table(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        z, hz, err_hz, reference = [part.strip() for part in line.split(",", 3)]
        rows.append({"z": z, "Hz": hz, "errHz": err_hz, "reference": reference})
    if not rows:
        raise SystemExit("CC table is empty")
    return rows


def family(reference: str) -> str:
    return reference.split("(")[0].strip()


def write_doc(summary: dict[str, str], rows: list[dict[str, str]]) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    nearby = [
        "| Reference | z | abs delta-z | class |",
        "| --- | ---: | ---: | --- |",
    ]
    for row in rows:
        nearby.append(
            "| "
            + " | ".join(
                [
                    row["candidate_reference"],
                    row["candidate_z"],
                    row["candidate_abs_delta_z"],
                    row["support_class"],
                ]
            )
            + " |"
        )
    DOC.write_text(
        "\n".join(
            [
                "# Paper10 DESI shape row2 left strict-support scout v1",
                "",
                "**Doc class:** source-side strict endpoint-support scout",
                "**Reader role:** reviewer / source-acquisition auditor",
                "**Status:** negative source-side scout, not replay, not validation",
                "**Canonical parent:** Paper10 DESI shape-route replay chain",
                "",
                "This scout checks the frozen cosmic-chronometer table after the",
                "row-2 source-window review reopened the left endpoint only as caveated",
                "source context. It asks a narrow question: is there an independent",
                "source in the strict row-2 left endpoint window?",
                "",
                "Frozen result:",
                "",
                f"- row-2 left endpoint: `{summary['row2_left_endpoint_z']}`",
                f"- strict window: `{summary['strict_endpoint_window_abs_dz']}`",
                f"- strict independent support count: `{summary['strict_independent_support_count']}`",
                f"- nearest candidate: `{summary['nearest_candidate_reference']}` at `z={summary['nearest_candidate_z']}`",
                f"- nearest independent candidate: `{summary['nearest_independent_candidate_reference']}` at `z={summary['nearest_independent_candidate_z']}`",
                f"- endpoint replay allowed: `{summary['endpoint_replay_allowed']}`",
                "",
                "Nearest frozen CC candidates:",
                "",
                *nearby,
                "",
                "Interpretation:",
                "",
                "The frozen CC table contains near-window context, but no strict",
                "independent left-endpoint support. This preserves a negative",
                "source-side result: the P0 strict-support route remains open.",
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
    policy = one_row(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad row2 left strict-support scout claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    source_plan = one_row(SOURCE_PLAN)
    if source_plan["source_plan_status"] != "ROW2_SOURCE_REOPENED_CAVEATED_LEFT_ENDPOINT_STILL_NOT_RELEASED":
        raise SystemExit("strict-support scout expects caveated source reopen without left endpoint release")
    if source_plan["strict_left_endpoint_support_count"] != "0":
        raise SystemExit("strict-support scout expects no prior strict support")
    for field in ["row2_promotion_ready", "endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if source_plan[field] != "false":
            raise SystemExit(f"source plan {field} must remain false")

    strict_window = float(policy["strict_endpoint_window_abs_dz"])
    cc_rows = read_cc_table(CC_TABLE)
    candidate_rows: list[dict[str, str]] = []
    for row in cc_rows:
        z = float(row["z"])
        delta = abs(z - ROW2_LEFT_Z)
        independent = family(row["reference"]) != CURRENT_LEFT_FAMILY
        within_strict = delta <= strict_window
        if delta <= 0.10:
            if within_strict and independent:
                support_class = "strict_independent_left_endpoint_support"
            elif within_strict:
                support_class = "strict_same_family_context"
            elif independent:
                support_class = "relaxed_independent_near_window_context"
            else:
                support_class = "relaxed_same_family_context"
            candidate_rows.append(
                {
                    "scout_id": policy["scout_id"],
                    "shape_row": "2",
                    "endpoint_label": "left",
                    "endpoint_z": f"{ROW2_LEFT_Z:.3f}",
                    "strict_endpoint_window_abs_dz": policy["strict_endpoint_window_abs_dz"],
                    "candidate_z": row["z"],
                    "candidate_abs_delta_z": f"{delta:.12g}",
                    "candidate_Hz": row["Hz"],
                    "candidate_errHz": row["errHz"],
                    "candidate_reference": row["reference"],
                    "candidate_reference_family": family(row["reference"]),
                    "independent_of_current_left_family": "true" if independent else "false",
                    "within_strict_endpoint_window": "true" if within_strict else "false",
                    "support_class": support_class,
                    "source_status": "already_frozen_in_CC_table",
                    "left_endpoint_release_allowed": "false",
                    "row2_promotion_ready": "false",
                    "shape_route_promotion_allowed": "false",
                    "endpoint_replay_allowed": "false",
                    "endpoint_validation_claimed": "false",
                    "physical_validation_claimed": "false",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    candidate_rows.sort(key=lambda row: float(row["candidate_abs_delta_z"]))
    write_csv(OUT, candidate_rows)

    strict_independent = [
        row
        for row in candidate_rows
        if row["within_strict_endpoint_window"] == "true"
        and row["independent_of_current_left_family"] == "true"
    ]
    strict_any = [row for row in candidate_rows if row["within_strict_endpoint_window"] == "true"]
    nearest = candidate_rows[0]
    independent_candidates = [
        row for row in candidate_rows
        if row["independent_of_current_left_family"] == "true"
    ]
    if not independent_candidates:
        raise SystemExit("expected at least one independent relaxed candidate for context")
    nearest_independent = independent_candidates[0]
    summary = {
        "scout_id": policy["scout_id"],
        "status": "DESI_SHAPE_ROW2_LEFT_STRICT_SUPPORT_SCOUT_BUILT_NOT_REPLAY_NOT_VALIDATION",
        "row2_left_endpoint_z": f"{ROW2_LEFT_Z:.3f}",
        "strict_endpoint_window_abs_dz": policy["strict_endpoint_window_abs_dz"],
        "strict_any_support_count": str(len(strict_any)),
        "strict_independent_support_count": str(len(strict_independent)),
        "relaxed_candidate_count": str(len(candidate_rows)),
        "nearest_candidate_reference": nearest["candidate_reference"],
        "nearest_candidate_z": nearest["candidate_z"],
        "nearest_candidate_abs_delta_z": nearest["candidate_abs_delta_z"],
        "nearest_independent_candidate_reference": nearest_independent["candidate_reference"],
        "nearest_independent_candidate_z": nearest_independent["candidate_z"],
        "nearest_independent_candidate_abs_delta_z": nearest_independent["candidate_abs_delta_z"],
        "left_endpoint_release_allowed": "false",
        "row2_promotion_ready": "false",
        "shape_route_promotion_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "row2_left_strict_support_absent_in_frozen_cc_table",
        "recommended_next_action": "seek_new_source_native_or_independent_strict_left_endpoint_support_before_any_replay",
    }
    write_csv(SUMMARY, [summary])
    write_doc(summary, candidate_rows)
    print("PAPER10_DESI_SHAPE_ROW2_LEFT_STRICT_SUPPORT_SCOUT_BUILT")


if __name__ == "__main__":
    main()
