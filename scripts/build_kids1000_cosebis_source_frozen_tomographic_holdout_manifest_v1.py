#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_source_frozen_tomographic_holdout_manifest_policy_v1.csv"
GATE = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_holdout_calibration_gate_v1_summary.csv"
ZINV = ROOT / "data" / "derived" / "kids1000_cosebis_redshift_kernel_inventory_v1.csv"

BIN_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_tomographic_holdout_bins_v1.csv"
PAIR_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_tomographic_holdout_pairs_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = read_one(POLICY)
    gate = read_one(GATE)
    zrows = read_rows(ZINV)

    if policy["status"] != "SOURCE_FROZEN_TOMOGRAPHIC_HOLDOUT_MANIFEST_POLICY_FROZEN":
        raise SystemExit("unexpected tomographic holdout manifest policy status")
    if gate["endpoint_replay_allowed"] != "false":
        raise SystemExit("parent holdout gate should not authorize replay")
    if policy["computes_new_scores"] != "false":
        raise SystemExit("holdout manifest must not compute scores")
    if policy["endpoint_replay_allowed"] != "false":
        raise SystemExit("holdout manifest must not authorize endpoint replay")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("holdout manifest must not claim validation")

    by_bin = {int(row["source_bin"]): row for row in zrows}
    if set(by_bin) != {1, 2, 3, 4, 5}:
        raise SystemExit("unexpected KiDS source-bin set")

    bin_rows: list[dict[str, str]] = []
    for source_bin in sorted(by_bin):
        row = by_bin[source_bin]
        bin_rows.append(
            {
                "policy_id": policy["policy_id"],
                "source_bin": str(source_bin),
                "nz_column": row["nz_column"],
                "mean_z": row["mean_z"],
                "support_z_min_nonzero": row["support_z_min_nonzero"],
                "support_z_max_nonzero": row["support_z_max_nonzero"],
                "holdout_fold_id": f"holdout_source_bin_{source_bin}",
                "calibration_evidence_class": policy["calibration_evidence_class"],
                "source_native_nz_available": "true",
                "independent_external_photoz_calibration_attached": "false",
                "uses_kids_data_vector_values_for_source_selection": "false",
                "uses_residuals": "false",
                "uses_fit_statistics": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    pair_rows: list[dict[str, str]] = []
    for fold_bin in sorted(by_bin):
        for i in sorted(by_bin):
            for j in range(i, 6):
                touches_holdout = fold_bin in {i, j}
                pair_rows.append(
                    {
                        "policy_id": policy["policy_id"],
                        "holdout_fold_id": f"holdout_source_bin_{fold_bin}",
                        "held_out_source_bin": str(fold_bin),
                        "tomographic_pair": f"{i}-{j}",
                        "bin_i": str(i),
                        "bin_j": str(j),
                        "pair_role": "holdout_pair" if touches_holdout else "calibration_pair",
                        "holdout_reason": (
                            "pair_touches_held_out_source_bin"
                            if touches_holdout
                            else "pair_does_not_touch_held_out_source_bin"
                        ),
                        "mean_z_i": by_bin[i]["mean_z"],
                        "mean_z_j": by_bin[j]["mean_z"],
                        "pair_mean_z": f"{0.5 * (float(by_bin[i]['mean_z']) + float(by_bin[j]['mean_z'])):.12e}",
                        "uses_kids_data_vector_values_for_source_selection": "false",
                        "uses_residuals": "false",
                        "uses_fit_statistics": "false",
                        "endpoint_replay_allowed": "false",
                        "endpoint_validation_claimed": "false",
                        "claim_boundary": policy["claim_boundary"],
                    }
                )

    holdout_counts = {
        str(fold): sum(
            1
            for row in pair_rows
            if row["held_out_source_bin"] == str(fold) and row["pair_role"] == "holdout_pair"
        )
        for fold in sorted(by_bin)
    }
    calibration_counts = {
        str(fold): sum(
            1
            for row in pair_rows
            if row["held_out_source_bin"] == str(fold) and row["pair_role"] == "calibration_pair"
        )
        for fold in sorted(by_bin)
    }
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "SOURCE_FROZEN_TOMOGRAPHIC_HOLDOUT_MANIFEST_BUILT",
            "selected_statistic": policy["selected_statistic"],
            "source_bin_count": str(len(by_bin)),
            "tomographic_pair_count": "15",
            "holdout_fold_count": str(len(by_bin)),
            "holdout_pair_counts_by_fold": ";".join(f"{k}:{v}" for k, v in holdout_counts.items()),
            "calibration_pair_counts_by_fold": ";".join(f"{k}:{v}" for k, v in calibration_counts.items()),
            "calibration_evidence_class": policy["calibration_evidence_class"],
            "source_native_nz_available": "true",
            "independent_external_photoz_calibration_attached": "false",
            "h1_independent_evidence_complete": "false",
            "h2_holdout_partition_frozen": "true",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values_for_scoring": "false",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "uses_residuals": "false",
            "uses_fit_statistics": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "holdout_partition_frozen_but_independent_photoz_calibration_still_open",
            "recommended_next_action": "attach_independent_photoz_or_tomographic_calibration_evidence_before_endpoint_replay",
            "claim_boundary": policy["claim_boundary"],
        }
    ]

    write_csv(BIN_OUT, bin_rows)
    write_csv(PAIR_OUT, pair_rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_SOURCE_FROZEN_TOMOGRAPHIC_HOLDOUT_MANIFEST_V1_BUILT "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
