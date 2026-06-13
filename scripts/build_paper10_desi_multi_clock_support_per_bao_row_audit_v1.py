#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_multi_clock_support_per_bao_row_audit_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_multi_clock_support_per_bao_row_audit_not_validation"


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


def load_cc_rows(path: Path) -> list[dict[str, str | float]]:
    if not path.exists():
        raise SystemExit(f"missing CC source table: {path.relative_to(ROOT)}")
    rows: list[dict[str, str | float]] = []
    with path.open() as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            z, hz, err, reference = line.split(",", 3)
            rows.append(
                {
                    "z": float(z),
                    "Hz": float(hz),
                    "errHz": float(err),
                    "reference": reference,
                }
            )
    return sorted(rows, key=lambda row: float(row["z"]))


def support_summary(
    cc_rows: list[dict[str, str | float]],
    target_z: float,
    window: float,
) -> tuple[list[dict[str, str | float]], int, int, str]:
    hits = [row for row in cc_rows if abs(float(row["z"]) - target_z) <= window]
    refs = sorted({str(row["reference"]) for row in hits})
    z_list = ";".join(f"{float(row['z']):.12g}" for row in hits) if hits else "none"
    return hits, len(hits), len(refs), z_list


def main() -> None:
    policy = one_row(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad multi-clock audit claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    cc_table = ROOT / policy["cc_source_table"]
    cc_match_ledger = ROOT / policy["cc_match_ledger"]
    cc_rows = load_cc_rows(cc_table)
    match_rows = read_rows(cc_match_ledger)
    authorized = [int(value) for value in policy["authorized_radial_indices"].split(";")]
    strict_window = float(policy["strict_delta_z_window"])
    relaxed_window = float(policy["relaxed_delta_z_window"])
    min_entries = int(policy["minimum_clock_entries"])
    min_refs = int(policy["minimum_independent_references"])

    match_by_index = {int(row["radial_index"]): row for row in match_rows}
    out_rows: list[dict[str, str]] = []
    for radial_index in authorized:
        if radial_index not in match_by_index:
            raise SystemExit(f"authorized radial index {radial_index} missing from CC match ledger")
        match = match_by_index[radial_index]
        if match["cc_support_status"] != "MATCHED_WITHIN_CC_RANGE":
            raise SystemExit(f"authorized radial index {radial_index} is not CC matched")
        z_eff = float(match["z_eff"])
        strict_hits, strict_count, strict_ref_count, strict_z_list = support_summary(cc_rows, z_eff, strict_window)
        relaxed_hits, relaxed_count, relaxed_ref_count, relaxed_z_list = support_summary(cc_rows, z_eff, relaxed_window)
        strict_pass = strict_count >= min_entries and strict_ref_count >= min_refs
        relaxed_pass = relaxed_count >= min_entries and relaxed_ref_count >= min_refs
        strict_refs = sorted({str(row["reference"]) for row in strict_hits})
        relaxed_refs = sorted({str(row["reference"]) for row in relaxed_hits})
        out_rows.append(
            {
                "audit_id": policy["audit_id"],
                "radial_index": str(radial_index),
                "z_eff": f"{z_eff:.12g}",
                "strict_delta_z_window": f"{strict_window:.12g}",
                "strict_clock_support_count": str(strict_count),
                "strict_independent_reference_count": str(strict_ref_count),
                "strict_clock_z_values": strict_z_list,
                "strict_references": ";".join(strict_refs) if strict_refs else "none",
                "strict_multi_clock_pass": "true" if strict_pass else "false",
                "relaxed_delta_z_window": f"{relaxed_window:.12g}",
                "relaxed_clock_support_count": str(relaxed_count),
                "relaxed_independent_reference_count": str(relaxed_ref_count),
                "relaxed_clock_z_values": relaxed_z_list,
                "relaxed_references": ";".join(relaxed_refs) if relaxed_refs else "none",
                "relaxed_multi_clock_pass": "true" if relaxed_pass else "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, out_rows)

    strict_pass_count = sum(row["strict_multi_clock_pass"] == "true" for row in out_rows)
    relaxed_pass_count = sum(row["relaxed_multi_clock_pass"] == "true" for row in out_rows)
    failed_relaxed = [
        row["radial_index"]
        for row in out_rows
        if row["relaxed_multi_clock_pass"] != "true"
    ]
    endpoint_ready = relaxed_pass_count == len(out_rows)
    summary = [
        {
            "audit_id": policy["audit_id"],
            "status": "DESI_MULTI_CLOCK_SUPPORT_PER_BAO_ROW_AUDIT_BUILT_NOT_REPLAY_NOT_VALIDATION",
            "authorized_row_count": str(len(out_rows)),
            "strict_delta_z_window": f"{strict_window:.12g}",
            "relaxed_delta_z_window": f"{relaxed_window:.12g}",
            "minimum_clock_entries": str(min_entries),
            "minimum_independent_references": str(min_refs),
            "strict_multi_clock_pass_count": str(strict_pass_count),
            "relaxed_multi_clock_pass_count": str(relaxed_pass_count),
            "relaxed_multi_clock_failed_radial_indices": ";".join(failed_relaxed) if failed_relaxed else "none",
            "multi_clock_support_endpoint_ready": "true" if endpoint_ready else "false",
            "blocks_endpoint_reason": "not_all_authorized_rows_have_two_independent_clock_references_under_relaxed_window"
            if not endpoint_ready
            else "none",
            "next_primary_gate": "independent_shape_review_or_new_clock_compilation",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "desi_multi_clock_support_incomplete_not_endpoint_ready"
            if not endpoint_ready
            else "desi_multi_clock_support_source_side_complete_but_replay_still_requires_authorization",
        }
    ]
    write_csv(SUMMARY, summary)


if __name__ == "__main__":
    main()
