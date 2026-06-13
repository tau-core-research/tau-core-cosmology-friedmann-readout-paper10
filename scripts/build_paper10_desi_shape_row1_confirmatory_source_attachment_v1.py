#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_row1_confirmatory_source_attachment_policy_v1.csv"
SCAN = ROOT / "data/derived/paper10_desi_shape_core_source_support_scan_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_shape_row1_confirmatory_source_attachment_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row1_confirmatory_source_attachment_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row1_confirmatory_source_attachment_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row1_confirmatory_source_attachment_not_validation"


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


def write_doc(rows: list[dict[str, str]], summary: dict[str, str]) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    bullets = [
        f"- `{row['attached_source_reference']}` at `z={row['attached_z']}` with `H(z)={row['attached_Hz']} +/- {row['attached_errHz']}`"
        for row in rows
    ]
    DOC.write_text(
        "\n".join(
            [
                "# Paper10 DESI shape Row1 confirmatory source attachment v1",
                "",
                "**Doc class:** source-side attachment",
                "**Reader role:** reviewer / reproducibility auditor",
                "**Status:** confirmatory source support; not replay; not validation",
                "**Canonical parent:** Paper10 DESI shape-core support chain",
                "",
                "This attachment records independent in-interval cosmic-chronometer",
                "support for DESI shape Row1 from the already frozen CC table.",
                "It does not use endpoint residuals, scores, or fit statistics.",
                "",
                "Attached support rows:",
                "",
                *bullets,
                "",
                "Interpretation:",
                "",
                f"- row1 confirmatory source support count: `{summary['row1_confirmatory_source_count']}`",
                f"- row1 status: `{summary['row1_status']}`",
                f"- endpoint replay allowed: `{summary['endpoint_replay_allowed']}`",
                f"- validation claimed: `{summary['endpoint_validation_claimed']}`",
                "",
                "Claim boundary:",
                "",
                "```text",
                CLAIM_BOUNDARY,
                "```",
                "",
            ]
        )
    )


def main() -> None:
    policy = read_one(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad policy claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    candidates = [
        row for row in read_rows(SCAN)
        if row["target_id"] == policy["target_id"]
        and row["support_role"] == "independent_in_interval_support"
        and row["source_status"] == "already_frozen_in_CC_table"
    ]
    if len(candidates) < 2:
        raise SystemExit("expected at least two independent Row1 confirmatory support rows")
    out_rows: list[dict[str, str]] = []
    for row in candidates:
        out_rows.append(
            {
                "attachment_id": policy["attachment_id"],
                "target_id": policy["target_id"],
                "shape_row": row["shape_row"],
                "radial_interval": row["radial_interval"],
                "attached_source_reference": row["candidate_reference"],
                "attached_source_family": row["candidate_reference_family"],
                "attached_z": row["candidate_z"],
                "attached_delta_z_to_mid": row["candidate_delta_z_to_mid"],
                "attached_Hz": row["candidate_Hz"],
                "attached_errHz": row["candidate_errHz"],
                "support_role": "confirmatory_independent_in_interval_support",
                "source_status": "already_frozen_in_CC_table",
                "row1_endpoint_ready": "false",
                "row1_promotion_ready": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, out_rows)
    summary = {
        "attachment_id": policy["attachment_id"],
        "status": "DESI_SHAPE_ROW1_CONFIRMATORY_SOURCE_ATTACHED_NOT_REPLAY_NOT_VALIDATION",
        "target_id": policy["target_id"],
        "row1_confirmatory_source_count": str(len(out_rows)),
        "attached_source_references": ";".join(row["attached_source_reference"] for row in out_rows),
        "attached_z_values": ";".join(row["attached_z"] for row in out_rows),
        "row1_status": "confirmatory_independent_in_interval_support_attached_not_endpoint_ready",
        "row1_endpoint_ready": "false",
        "row1_promotion_ready": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "row1_confirmatory_independent_support_attached_not_endpoint_ready",
        "recommended_next_action": "retain_as_confirmatory_core_support_or_send_to_source_reviewer_before_stronger_route_claims",
    }
    write_csv(SUMMARY, [summary])
    write_doc(out_rows, summary)
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"wrote {SUMMARY.relative_to(ROOT)}")
    print(f"wrote {DOC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
