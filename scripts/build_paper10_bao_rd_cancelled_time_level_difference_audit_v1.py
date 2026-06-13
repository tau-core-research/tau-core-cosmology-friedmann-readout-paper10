#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_bao_rd_cancelled_time_level_difference_audit_policy_v1.csv"
BAO = ROOT / "data/derived/sdss_bao_time_readout_observable_route_audit_v1.csv"
CC_HZ = ROOT / "data/raw/hz_compilation/cosmic_chronometers_hz/data_CC.dat"
OUT = ROOT / "data/derived/paper10_bao_rd_cancelled_time_level_difference_audit_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_bao_rd_cancelled_time_level_difference_audit_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_bao_rd_cancelled_time_level_difference_audit_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_cc_rows() -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    with CC_HZ.open() as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            z, hz, err, reference = line.strip().split(",", 3)
            rows.append({"z": float(z), "Hz": float(hz), "errHz": float(err), "reference": reference})
    return sorted(rows, key=lambda row: float(row["z"]))


def nearest_cc(cc_rows: list[dict[str, float | str]], z: float) -> dict[str, float | str]:
    return min(cc_rows, key=lambda row: abs(float(row["z"]) - z))


def sign(value: float) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def main() -> None:
    policy = read_one(POLICY)
    if policy["status"] != "SOURCE_SIDE_RD_CANCELLED_DIFFERENCE_AUDIT_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad policy status")
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"{field} must be false")

    bao_rows = sorted(read_rows(BAO), key=lambda row: float(row["z_eff"]))
    if len(bao_rows) != 2:
        raise SystemExit("rd-cancelled audit expects exactly two radial BAO rows")
    cc_rows = [nearest_cc(load_cc_rows(), float(row["z_eff"])) for row in bao_rows]

    bao_y = [float(row["time_readout_raw_minus_log_DH_over_rd"]) for row in bao_rows]
    bao_sigma_y = [
        float(row["published_sigma"]) / float(row["observed_DH_over_rd"])
        for row in bao_rows
    ]
    cc_logh = [math.log(float(row["Hz"])) for row in cc_rows]
    cc_sigma_logh = [float(row["errHz"]) / float(row["Hz"]) for row in cc_rows]

    delta_bao = bao_y[1] - bao_y[0]
    delta_bao_sigma = math.sqrt(bao_sigma_y[0] ** 2 + bao_sigma_y[1] ** 2)
    delta_cc = cc_logh[1] - cc_logh[0]
    delta_cc_sigma = math.sqrt(cc_sigma_logh[0] ** 2 + cc_sigma_logh[1] ** 2)
    sign_agreement = sign(delta_bao) == sign(delta_cc) and sign(delta_bao) != 0
    bao_delta_snr = abs(delta_bao) / delta_bao_sigma if delta_bao_sigma > 0 else 0.0
    cc_delta_snr = abs(delta_cc) / delta_cc_sigma if delta_cc_sigma > 0 else 0.0
    ratio_bao_to_cc = delta_bao / delta_cc if delta_cc != 0 else float("nan")

    if sign_agreement and bao_delta_snr < 1:
        verdict = "rd_cancels_direction_agrees_but_bao_delta_low_significance_not_endpoint"
    elif sign_agreement:
        verdict = "rd_cancels_direction_agrees_not_endpoint"
    else:
        verdict = "rd_cancels_direction_tension_not_endpoint"

    rows = []
    for idx, (bao, cc, y, sy, logh, slogh) in enumerate(
        zip(bao_rows, cc_rows, bao_y, bao_sigma_y, cc_logh, cc_sigma_logh)
    ):
        rows.append(
            {
                "audit_id": policy["audit_id"],
                "point_order": str(idx),
                "z_eff": bao["z_eff"],
                "minus_log_DH_over_rd": f"{y:.12g}",
                "sigma_minus_log_DH_over_rd": f"{sy:.12g}",
                "nearest_cc_z": f"{float(cc['z']):.12g}",
                "nearest_cc_Hz": f"{float(cc['Hz']):.12g}",
                "nearest_cc_sigma_logH": f"{slogh:.12g}",
                "nearest_cc_logH": f"{logh:.12g}",
                "nearest_cc_reference": str(cc["reference"]),
                "rd_cancels_in_difference": "true",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    summary = {
        "audit_id": policy["audit_id"],
        "status": "SOURCE_SIDE_RD_CANCELLED_DIFFERENCE_AUDIT_COMPLETE_NOT_REPLAY_NOT_VALIDATION",
        "radial_bao_rows": "2",
        "delta_bao_minus_log_DH_over_rd": f"{delta_bao:.12g}",
        "delta_bao_sigma": f"{delta_bao_sigma:.12g}",
        "delta_bao_snr": f"{bao_delta_snr:.12g}",
        "delta_cc_logH": f"{delta_cc:.12g}",
        "delta_cc_sigma": f"{delta_cc_sigma:.12g}",
        "delta_cc_snr": f"{cc_delta_snr:.12g}",
        "ratio_delta_bao_to_delta_cc": f"{ratio_bao_to_cc:.12g}",
        "rd_cancels_in_difference": "true",
        "differential_direction_sign_agreement": str(sign_agreement).lower(),
        "amplitude_interpretation_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": verdict,
    }
    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    print(
        "PAPER10_BAO_RD_CANCELLED_TIME_LEVEL_DIFFERENCE_AUDIT_BUILT "
        f"snr={bao_delta_snr:.3f} verdict={verdict}"
    )


if __name__ == "__main__":
    main()
