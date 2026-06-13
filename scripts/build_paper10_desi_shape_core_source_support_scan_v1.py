#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_core_source_support_scan_policy_v1.csv"
ACQUISITION = ROOT / "data/derived/paper10_desi_shape_core_source_acquisition_manifest_v1.csv"
ACQUISITION_SUMMARY = ROOT / "data/derived/paper10_desi_shape_core_source_acquisition_manifest_v1_summary.csv"
CC_TABLE = ROOT / "data/raw/hz_compilation/cosmic_chronometers_hz/data_CC.dat"
OUT = ROOT / "data/derived/paper10_desi_shape_core_source_support_scan_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_core_source_support_scan_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_core_source_support_scan_not_validation"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_csv(path)
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
    if not path.exists():
        raise SystemExit(f"missing CC table: {path.relative_to(ROOT)}")
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


def main() -> None:
    policy = one_row(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad shape-core support scan policy claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    acquisition_summary = one_row(ACQUISITION_SUMMARY)
    if acquisition_summary["source_fetch_completed"] != "false":
        raise SystemExit("support scan expects acquisition fetch to remain pending")
    if acquisition_summary["p0_targets"] != "DESI_SHAPE_ROW_2_CORE_SUPPORT":
        raise SystemExit("support scan expects row 2 as P0")

    cc_rows = read_cc_table(CC_TABLE)
    out_rows: list[dict[str, str]] = []
    for target in read_csv(ACQUISITION):
        z_left = float(target["z_left"])
        z_right = float(target["z_right"])
        z_mid = float(target["z_mid"])
        current_families = {family(target["current_left_reference"]), family(target["current_right_reference"])}
        candidates = [
            row
            for row in cc_rows
            if z_left <= float(row["z"]) <= z_right
        ]
        for row in candidates:
            ref_family = family(row["reference"])
            independent = ref_family not in current_families
            out_rows.append(
                {
                    "scan_id": policy["scan_id"],
                    "target_id": target["target_id"],
                    "priority": target["priority"],
                    "shape_row": target["shape_row"],
                    "radial_interval": target["radial_interval"],
                    "target_z_left": target["z_left"],
                    "target_z_right": target["z_right"],
                    "target_z_mid": target["z_mid"],
                    "candidate_z": row["z"],
                    "candidate_delta_z_to_mid": f"{abs(float(row['z']) - z_mid):.12g}",
                    "candidate_Hz": row["Hz"],
                    "candidate_errHz": row["errHz"],
                    "candidate_reference": row["reference"],
                    "candidate_reference_family": ref_family,
                    "independent_of_current_endpoint_families": "true" if independent else "false",
                    "support_role": "independent_in_interval_support" if independent else "same_family_context",
                    "source_status": "already_frozen_in_CC_table",
                    "endpoint_replay_allowed": "false",
                    "endpoint_validation_claimed": "false",
                    "physical_validation_claimed": "false",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if not out_rows:
        raise SystemExit("support scan found no in-interval rows")
    write_csv(OUT, out_rows)

    p0_support = [
        row
        for row in out_rows
        if row["priority"] == "P0" and row["independent_of_current_endpoint_families"] == "true"
    ]
    p1_support = [
        row
        for row in out_rows
        if row["priority"] == "P1" and row["independent_of_current_endpoint_families"] == "true"
    ]
    row2_moresco = [
        row
        for row in p0_support
        if row["shape_row"] == "2" and row["candidate_reference"] == "Moresco et al. (2012)"
    ]
    verdict = (
        "p0_row2_has_existing_independent_in_interval_CC_support_not_endpoint_ready"
        if row2_moresco
        else "p0_row2_no_existing_independent_in_interval_support_found"
    )
    summary = [
        {
            "scan_id": policy["scan_id"],
            "status": "DESI_SHAPE_CORE_SOURCE_SUPPORT_SCAN_BUILT_NOT_REPLAY_NOT_VALIDATION",
            "target_count": str(len(read_csv(ACQUISITION))),
            "candidate_count": str(len(out_rows)),
            "p0_independent_support_count": str(len(p0_support)),
            "p1_independent_support_count": str(len(p1_support)),
            "row2_moresco2012_support_found": "true" if row2_moresco else "false",
            "row2_support_status": "partial_strengthening_in_interval_not_endpoint_pair_replacement" if row2_moresco else "open",
            "source_fetch_completed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": verdict,
            "recommended_next_action": "promote_row2_support_to_reviewed_source_attachment_or_seek_endpoint_pair_independence_before_replay",
        }
    ]
    write_csv(SUMMARY, summary)
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"wrote {SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
