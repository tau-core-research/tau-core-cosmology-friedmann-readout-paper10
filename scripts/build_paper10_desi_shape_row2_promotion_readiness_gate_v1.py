#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_row2_promotion_readiness_gate_policy_v1.csv"
SENSITIVITY = ROOT / "data/derived/paper10_desi_shape_row_sensitivity_source_audit_v1.csv"
ACQUISITION = ROOT / "data/derived/paper10_desi_shape_core_source_acquisition_manifest_v1.csv"
ATTACHMENT_SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_v1_summary.csv"
REVIEW_SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1_summary.csv"
SOURCE_NATIVE_REVIEW_SUMMARY = (
    ROOT / "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_response_v1_summary.csv"
)
OUT = ROOT / "data/derived/paper10_desi_shape_row2_promotion_readiness_gate_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_promotion_readiness_gate_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_promotion_readiness_gate_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_promotion_readiness_gate_not_validation"


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


def write_doc(row: dict[str, str], summary: dict[str, str]) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Paper10 DESI shape row2 promotion-readiness gate v1",
                "",
                "**Doc class:** source-side promotion-readiness ledger",
                "**Reader role:** reviewer / reproducibility auditor",
                "**Status:** combined caveats reduced, promotion still blocked, not replay, not validation",
                "**Canonical parent:** Paper10 DESI shape-route replay chain",
                "",
                "This gate resolves the row-2 status after the completed Moresco2012",
                "source-attachment review and the completed source-native DESI BAO",
                "shape-support review.",
                "",
                "Result:",
                "",
                f"- row sensitivity: `{row['row_sensitivity_class']}`",
                f"- previous source caveat: `{row['prior_source_caveat']}`",
                f"- reviewed Moresco2012 attachment verdict: `{row['moresco_review_verdict']}`",
                f"- reviewed source-native shape verdict: `{row['source_native_shape_review_verdict']}`",
                f"- source-native shape caveat reduced: `{row['source_native_shape_caveat_reduced']}`",
                f"- row2 source caveat reduced: `{row['row2_source_caveat_reduced']}`",
                f"- endpoint-pair independence satisfied: `{row['endpoint_pair_independence_satisfied']}`",
                f"- row2 promotion ready: `{row['row2_promotion_ready']}`",
                "",
                "Interpretation:",
                "",
                "Row 2 is no longer merely a single-reference-family caveat: it now has",
                "reviewed independent in-interval support and reviewed source-native",
                "DESI BAO shape context. However, neither review authorizes endpoint",
                "readiness, route promotion, or replay. The strict endpoint-pair",
                "independence blocker remains, so Row 2 is strengthened but not",
                "promotion-ready.",
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
        raise SystemExit("bad row2 promotion-readiness policy claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    sensitivity_rows = [row for row in read_rows(SENSITIVITY) if row["shape_row"] == "2"]
    acquisition_rows = [row for row in read_rows(ACQUISITION) if row["target_id"] == "DESI_SHAPE_ROW_2_CORE_SUPPORT"]
    if len(sensitivity_rows) != 1:
        raise SystemExit("expected exactly one row2 sensitivity row")
    if len(acquisition_rows) != 1:
        raise SystemExit("expected exactly one row2 acquisition row")
    sensitivity = sensitivity_rows[0]
    acquisition = acquisition_rows[0]
    attachment = read_one(ATTACHMENT_SUMMARY)
    review = read_one(REVIEW_SUMMARY)
    source_native_review = read_one(SOURCE_NATIVE_REVIEW_SUMMARY)

    if sensitivity["sensitivity_class"] != "core_sensitive":
        raise SystemExit("row2 must remain core-sensitive")
    if sensitivity["independent_reference_pair"] != "false":
        raise SystemExit("row2 endpoint pair should still be non-independent before promotion gate")
    if acquisition["current_source_caveat"] != "single_reference_family_pair":
        raise SystemExit("row2 acquisition caveat mismatch")
    if attachment["endpoint_pair_replacement"] != "false":
        raise SystemExit("attachment must not be endpoint-pair replacement")
    if review["row2_source_caveat_reduced"] != "true":
        raise SystemExit("completed review must reduce row2 source caveat")
    if review["row2_endpoint_ready"] != "false":
        raise SystemExit("completed review must keep row2 non-endpoint-ready")
    if review["endpoint_replay_allowed"] != "false":
        raise SystemExit("completed review must not authorize replay")
    if source_native_review["row2_source_caveat_reduced"] != "true":
        raise SystemExit("source-native review must reduce row2 source caveat")
    if source_native_review["row2_endpoint_ready"] != "false":
        raise SystemExit("source-native review must keep row2 non-endpoint-ready")
    if source_native_review["row2_promotion_ready"] != "false":
        raise SystemExit("source-native review must keep row2 non-promotion-ready")
    if source_native_review["endpoint_replay_allowed"] != "false":
        raise SystemExit("source-native review must not authorize replay")

    endpoint_pair_independence = "false"
    row2_promotion_ready = "false"
    combined_caveat_reduced = (
        review["row2_source_caveat_reduced"] == "true"
        and source_native_review["row2_source_caveat_reduced"] == "true"
    )
    row = {
        "gate_id": policy["gate_id"],
        "shape_row": "2",
        "radial_interval": sensitivity["radial_interval"],
        "z_left": sensitivity["z_left"],
        "z_right": sensitivity["z_right"],
        "z_mid": sensitivity["z_mid"],
        "row_sensitivity_class": sensitivity["sensitivity_class"],
        "prior_source_caveat": acquisition["current_source_caveat"],
        "moresco_review_verdict": review["verdict"],
        "moresco_caveat_reduced": review["row2_source_caveat_reduced"],
        "source_native_shape_review_verdict": source_native_review["verdict"],
        "source_native_shape_caveat_reduced": source_native_review["row2_source_caveat_reduced"],
        "row2_source_caveat_reduced": "true" if combined_caveat_reduced else "false",
        "endpoint_pair_replacement": attachment["endpoint_pair_replacement"],
        "endpoint_pair_independence_satisfied": endpoint_pair_independence,
        "row2_endpoint_ready": review["row2_endpoint_ready"],
        "row2_promotion_ready": row2_promotion_ready,
        "shape_route_promotion_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "blocking_reason": "row2_has_reviewed_in_interval_and_source_native_shape_support_but_no_endpoint_pair_independence_or_promotion_authorization",
        "next_action": "seek_endpoint_pair_independence_or_build_separate_shape_route_promotion_review_gate",
    }
    write_csv(OUT, [row])
    summary = {
        "gate_id": policy["gate_id"],
        "status": "DESI_SHAPE_ROW2_CAVEAT_REDUCED_BUT_PROMOTION_BLOCKED_NOT_REPLAY_NOT_VALIDATION",
        "row2_source_caveat_reduced": row["row2_source_caveat_reduced"],
        "moresco_caveat_reduced": row["moresco_caveat_reduced"],
        "source_native_shape_caveat_reduced": row["source_native_shape_caveat_reduced"],
        "endpoint_pair_independence_satisfied": endpoint_pair_independence,
        "row2_promotion_ready": row2_promotion_ready,
        "shape_route_promotion_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "row2_combined_caveats_reduced_but_promotion_and_endpoint_pair_independence_blockers_remain",
        "recommended_next_action": "seek_endpoint_pair_independence_or_prepare_separate_promotion_review_without_validation_claim",
    }
    write_csv(SUMMARY, [summary])
    write_doc(row, summary)
    print("paper10_desi_shape_row2_promotion_readiness_gate_v1: built")


if __name__ == "__main__":
    main()
