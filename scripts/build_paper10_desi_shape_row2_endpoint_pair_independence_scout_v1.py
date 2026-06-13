#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_row2_endpoint_pair_independence_scout_policy_v1.csv"
SENSITIVITY = ROOT / "data/derived/paper10_desi_shape_row_sensitivity_source_audit_v1.csv"
PROMOTION = ROOT / "data/derived/paper10_desi_shape_row2_promotion_readiness_gate_v1_summary.csv"
CC_TABLE = ROOT / "data/raw/hz_compilation/cosmic_chronometers_hz/data_CC.dat"
OUT = ROOT / "data/derived/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_endpoint_pair_independence_scout_not_validation"


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


def endpoint_candidates(
    cc_rows: list[dict[str, str]],
    endpoint_label: str,
    endpoint_z: float,
    current_reference: str,
    strict_window: float,
    relaxed_window: float,
) -> list[dict[str, str]]:
    current_family = family(current_reference)
    rows = []
    for cc in cc_rows:
        z = float(cc["z"])
        dz = abs(z - endpoint_z)
        if dz > relaxed_window:
            continue
        ref_family = family(cc["reference"])
        independent = ref_family != current_family
        support_class = (
            "strict_independent_endpoint_support"
            if independent and dz <= strict_window
            else "relaxed_independent_endpoint_context"
            if independent
            else "same_family_endpoint_context"
        )
        rows.append(
            {
                "scout_id": "PAPER10_DESI_SHAPE_ROW2_ENDPOINT_PAIR_INDEPENDENCE_SCOUT_V1",
                "shape_row": "2",
                "endpoint_label": endpoint_label,
                "endpoint_z": f"{endpoint_z:.12g}",
                "current_endpoint_reference": current_reference,
                "current_endpoint_reference_family": current_family,
                "candidate_z": cc["z"],
                "candidate_abs_delta_z": f"{dz:.12g}",
                "candidate_Hz": cc["Hz"],
                "candidate_errHz": cc["errHz"],
                "candidate_reference": cc["reference"],
                "candidate_reference_family": ref_family,
                "independent_of_current_endpoint_family": "true" if independent else "false",
                "within_strict_endpoint_window": "true" if dz <= strict_window else "false",
                "within_relaxed_endpoint_window": "true",
                "support_class": support_class,
                "endpoint_pair_replacement_candidate": "true" if support_class == "strict_independent_endpoint_support" else "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(rows, key=lambda row: (row["endpoint_label"], float(row["candidate_abs_delta_z"])))


def write_doc(summary: dict[str, str]) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Paper10 DESI shape row2 endpoint-pair independence scout v1",
                "",
                "**Doc class:** source-side endpoint-pair independence scout",
                "**Reader role:** reviewer / source-acquisition auditor",
                "**Status:** endpoint-pair independence still blocked, not replay, not validation",
                "**Canonical parent:** Paper10 DESI shape-route replay chain",
                "",
                "This scout checks the already frozen cosmic-chronometer table for",
                "independent endpoint-near support for both row-2 endpoints.",
                "",
                "Result:",
                "",
                f"- left strict independent support count: `{summary['left_strict_independent_count']}`",
                f"- right strict independent support count: `{summary['right_strict_independent_count']}`",
                f"- endpoint-pair independence satisfied: `{summary['endpoint_pair_independence_satisfied']}`",
                f"- row2 promotion ready: `{summary['row2_promotion_ready']}`",
                "",
                "Interpretation:",
                "",
                "The frozen table contains useful right-endpoint context near row 2, but",
                "does not supply independent strict-window support for both endpoints.",
                "Therefore the Moresco2012 attachment remains a caveat reducer, not an",
                "endpoint-pair replacement.",
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
        raise SystemExit("bad row2 endpoint-pair scout policy claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")
    strict_window = float(policy["strict_endpoint_window_abs_dz"])
    relaxed_window = float(policy["relaxed_endpoint_window_abs_dz"])

    promotion = read_one(PROMOTION)
    if promotion["row2_source_caveat_reduced"] != "true":
        raise SystemExit("row2 caveat must be reduced before endpoint-pair scout")
    if promotion["row2_promotion_ready"] != "false":
        raise SystemExit("row2 must not already be promotion-ready")

    row2_rows = [row for row in read_rows(SENSITIVITY) if row["shape_row"] == "2"]
    if len(row2_rows) != 1:
        raise SystemExit("expected exactly one row2 sensitivity row")
    row2 = row2_rows[0]
    z_left = float(row2["z_left"])
    z_right = float(row2["z_right"])
    cc_rows = read_cc_table(CC_TABLE)

    rows = []
    rows.extend(
        endpoint_candidates(
            cc_rows,
            "left",
            z_left,
            row2["left_cc_reference"],
            strict_window,
            relaxed_window,
        )
    )
    rows.extend(
        endpoint_candidates(
            cc_rows,
            "right",
            z_right,
            row2["right_cc_reference"],
            strict_window,
            relaxed_window,
        )
    )
    if not rows:
        rows.append(
            {
                "scout_id": policy["scout_id"],
                "shape_row": "2",
                "endpoint_label": "none",
                "endpoint_z": "",
                "current_endpoint_reference": "",
                "current_endpoint_reference_family": "",
                "candidate_z": "",
                "candidate_abs_delta_z": "",
                "candidate_Hz": "",
                "candidate_errHz": "",
                "candidate_reference": "",
                "candidate_reference_family": "",
                "independent_of_current_endpoint_family": "false",
                "within_strict_endpoint_window": "false",
                "within_relaxed_endpoint_window": "false",
                "support_class": "no_relaxed_window_endpoint_candidates_found",
                "endpoint_pair_replacement_candidate": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, rows)

    left_strict = [
        row for row in rows
        if row["endpoint_label"] == "left" and row["support_class"] == "strict_independent_endpoint_support"
    ]
    right_strict = [
        row for row in rows
        if row["endpoint_label"] == "right" and row["support_class"] == "strict_independent_endpoint_support"
    ]
    endpoint_pair_independence = bool(left_strict and right_strict)
    summary = {
        "scout_id": policy["scout_id"],
        "status": "DESI_SHAPE_ROW2_ENDPOINT_PAIR_INDEPENDENCE_SCOUT_BUILT_NOT_REPLAY_NOT_VALIDATION",
        "strict_endpoint_window_abs_dz": policy["strict_endpoint_window_abs_dz"],
        "relaxed_endpoint_window_abs_dz": policy["relaxed_endpoint_window_abs_dz"],
        "candidate_count": str(len(rows)),
        "left_strict_independent_count": str(len(left_strict)),
        "right_strict_independent_count": str(len(right_strict)),
        "left_best_independent_candidate": left_strict[0]["candidate_reference"] if left_strict else "none",
        "right_best_independent_candidate": right_strict[0]["candidate_reference"] if right_strict else "none",
        "endpoint_pair_independence_satisfied": "true" if endpoint_pair_independence else "false",
        "row2_promotion_ready": "true" if endpoint_pair_independence else "false",
        "shape_route_promotion_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": (
            "row2_endpoint_pair_independence_satisfied_but_separate_promotion_gate_required"
            if endpoint_pair_independence
            else "row2_endpoint_pair_independence_not_satisfied_in_frozen_CC_table"
        ),
        "recommended_next_action": (
            "prepare_separate_shape_route_promotion_review_without_validation_claim"
            if endpoint_pair_independence
            else "seek_left_endpoint_independent_clock_or_source_native_shape_support_before_promotion"
        ),
    }
    write_csv(SUMMARY, [summary])
    write_doc(summary)
    print("paper10_desi_shape_row2_endpoint_pair_independence_scout_v1: built")


if __name__ == "__main__":
    main()
