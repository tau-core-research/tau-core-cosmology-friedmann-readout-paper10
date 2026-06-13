#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_row2_moresco2012_source_attachment_policy_v1.csv"
SUPPORT_SCAN = ROOT / "data/derived/paper10_desi_shape_core_source_support_scan_v1.csv"
SUPPORT_SUMMARY = ROOT / "data/derived/paper10_desi_shape_core_source_support_scan_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_moresco2012_source_attachment_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_moresco2012_source_attachment_not_validation"


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


def write_doc(summary: dict[str, str], row: dict[str, str]) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Paper10 DESI shape row2 Moresco2012 source attachment v1",
                "",
                "**Doc class:** source-side attachment ledger",
                "**Reader role:** reviewer / reproducibility auditor",
                "**Status:** partial source strengthening, not replay, not validation",
                "**Canonical parent:** Paper10 DESI shape-route replay chain",
                "",
                "This ledger promotes the existing support-scan finding into a reviewed",
                "source attachment for the DESI shape-route row-2 caveat. It attaches only",
                "an already frozen in-interval cosmic-chronometer support point:",
                "",
                f"- source: `{row['source_reference']}`",
                f"- source key: `{row['source_key']}`",
                f"- arXiv: `{row['arxiv_id']}`",
                f"- DOI: `{row['doi']}`",
                f"- redshift: `{row['z']}`",
                f"- H(z): `{row['H_z_km_s_Mpc']} +/- {row['sigma_H_km_s_Mpc']}` km/s/Mpc",
                f"- support role: `{row['support_type']}`",
                "",
                "Claim boundary:",
                "",
                "```text",
                summary["claim_boundary"],
                "```",
                "",
                "Interpretation:",
                "",
                "- row 2 is partially strengthened because it has non-Simon in-interval",
                "  clock support;",
                "- this is not a full endpoint-pair replacement;",
                "- this does not authorize replay;",
                "- this does not claim endpoint or physical validation.",
                "",
                f"Machine verdict: `{summary['verdict']}`.",
                "",
            ]
        )
    )


def main() -> None:
    policy = read_one(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad row2 Moresco2012 attachment policy claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    support_summary = read_one(SUPPORT_SUMMARY)
    if support_summary["row2_moresco2012_support_found"] != "true":
        raise SystemExit("Moresco2012 row2 support must be found before attachment")
    if support_summary["row2_support_status"] != "partial_strengthening_in_interval_not_endpoint_pair_replacement":
        raise SystemExit("row2 support status must remain partial")
    if support_summary["endpoint_replay_allowed"] != "false":
        raise SystemExit("support scan must not authorize replay")

    support_rows = read_rows(SUPPORT_SCAN)
    matches = [
        row
        for row in support_rows
        if row["target_id"] == "DESI_SHAPE_ROW_2_CORE_SUPPORT"
        and row["shape_row"] == "2"
        and row["candidate_reference"] == "Moresco et al. (2012)"
        and row["candidate_z"] == "1.037"
        and row["independent_of_current_endpoint_families"] == "true"
    ]
    if len(matches) != 1:
        raise SystemExit("expected exactly one independent row2 Moresco2012 support row")
    src = matches[0]

    row = {
        "attachment_id": policy["attachment_id"],
        "target_id": src["target_id"],
        "shape_row": src["shape_row"],
        "radial_interval": src["radial_interval"],
        "target_z_left": src["target_z_left"],
        "target_z_right": src["target_z_right"],
        "target_z_mid": src["target_z_mid"],
        "source_key": "Moresco2012ExpansionRate",
        "source_reference": src["candidate_reference"],
        "source_reference_family": src["candidate_reference_family"],
        "arxiv_id": "1201.3609",
        "doi": "10.1088/1475-7516/2012/08/006",
        "z": src["candidate_z"],
        "H_z_km_s_Mpc": src["candidate_Hz"],
        "sigma_H_km_s_Mpc": src["candidate_errHz"],
        "support_type": "independent_in_interval_clock_support",
        "source_status": src["source_status"],
        "independent_of_current_endpoint_families": src["independent_of_current_endpoint_families"],
        "endpoint_pair_replacement": "false",
        "row2_source_caveat_reduced": "true",
        "row2_endpoint_ready": "false",
        "source_attachment_review_required_for_promotion": "true",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, [row])

    summary = {
        "attachment_id": policy["attachment_id"],
        "status": "DESI_SHAPE_ROW2_MORESCO2012_SOURCE_ATTACHED_PARTIAL_NOT_REPLAY_NOT_VALIDATION",
        "attached_source_count": "1",
        "attached_source_key": row["source_key"],
        "attached_source_reference": row["source_reference"],
        "attached_z": row["z"],
        "row2_source_caveat_reduced": "true",
        "endpoint_pair_replacement": "false",
        "row2_endpoint_ready": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "row2_moresco2012_in_interval_support_attached_partial_not_endpoint_ready",
        "recommended_next_action": "seek_endpoint_pair_independence_or_external_review_before_any_shape_route_promotion",
    }
    write_csv(SUMMARY, [summary])
    write_doc(summary, row)
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"wrote {SUMMARY.relative_to(ROOT)}")
    print(f"wrote {DOC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
