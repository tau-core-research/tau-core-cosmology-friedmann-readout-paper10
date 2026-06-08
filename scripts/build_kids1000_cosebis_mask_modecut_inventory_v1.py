#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mask_modecut_policy_v1.csv"
TOMO = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_mode_inventory_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_mask_modecut_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mask_modecut_inventory_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("COSEBIs mask/mode-cut policy must remain endpoint disabled")
    with TOMO.open(newline="") as f:
        tomo_rows = list(csv.DictReader(f))
    rows: list[dict[str, str]] = []
    retained_total = 0
    for row in tomo_rows:
        retained = int(row["rows_for_pair"])
        retained_total += retained
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "parent_policy": policy["parent_policy"],
                "selected_hdu_data_vector": policy["selected_hdu_data_vector"],
                "pair_id": row["pair_id"],
                "bin1": row["bin1"],
                "bin2": row["bin2"],
                "input_rows_for_pair": row["rows_for_pair"],
                "retained_rows_for_pair": str(retained),
                "dropped_rows_for_pair": "0",
                "retained_modes": row["modes"],
                "dropped_modes": "",
                "mask_reason": "retain_all_source_rows_pre_score",
                "mode_cut_reason": "retain_modes_1_through_20_pre_score",
                "uses_residuals": "false",
                "uses_fit_statistics": "false",
                "endpoint_scoring_allowed": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "claim_boundary": "kids1000_cosebis_mask_modecut_inventory_not_validation",
            }
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_MASK_MODECUT_INVENTORY_BUILT_NOT_SCORED",
        "selected_hdu_data_vector": policy["selected_hdu_data_vector"],
        "mask_policy": policy["mask_policy"],
        "mode_cut_policy": policy["mode_cut_policy"],
        "input_rows": str(sum(int(row["input_rows_for_pair"]) for row in rows)),
        "retained_rows": str(retained_total),
        "dropped_rows": "0",
        "n_retained_tomographic_pairs": str(len(rows)),
        "retained_mode_range": policy["retained_mode_range"],
        "uses_residuals": "false",
        "uses_fit_statistics": "false",
        "endpoint_scoring_allowed": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "claim_boundary": "kids1000_cosebis_mask_modecut_inventory_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_MASK_MODECUT_INVENTORY_V1_BUILT "
        f"retained={retained_total} dropped=0 endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
