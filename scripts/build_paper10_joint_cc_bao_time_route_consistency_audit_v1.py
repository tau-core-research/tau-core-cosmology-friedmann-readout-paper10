#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_joint_cc_bao_time_route_consistency_audit_policy_v1.csv"
CC_HZ = ROOT / "data/raw/hz_compilation/cosmic_chronometers_hz/data_CC.dat"
BAO = ROOT / "data/derived/sdss_bao_time_readout_observable_route_audit_v1.csv"
OUT = ROOT / "data/derived/paper10_joint_cc_bao_time_route_consistency_audit_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_joint_cc_bao_time_route_consistency_audit_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_joint_cc_bao_time_route_consistency_audit_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
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
    if len(rows) < 3:
        raise SystemExit("need at least three CC rows")
    return sorted(rows, key=lambda row: float(row["z"]))


def nearest_cc_index(cc_rows: list[dict[str, float | str]], z: float) -> int:
    return min(range(len(cc_rows)), key=lambda idx: abs(float(cc_rows[idx]["z"]) - z))


def logh_slope(cc_rows: list[dict[str, float | str]], idx: int) -> float:
    if idx <= 0:
        left, right = 0, 1
    elif idx >= len(cc_rows) - 1:
        left, right = len(cc_rows) - 2, len(cc_rows) - 1
    else:
        left, right = idx - 1, idx + 1
    z_left = float(cc_rows[left]["z"])
    z_right = float(cc_rows[right]["z"])
    h_left = float(cc_rows[left]["Hz"])
    h_right = float(cc_rows[right]["Hz"])
    denom = math.log1p(z_right) - math.log1p(z_left)
    if denom == 0:
        raise SystemExit("degenerate CC slope support")
    return (math.log(h_right) - math.log(h_left)) / denom


def normalize(values: list[float]) -> tuple[list[float], float, float]:
    center = sum(values) / len(values)
    scale = math.sqrt(sum((value - center) ** 2 for value in values) / len(values))
    if scale <= 0:
        raise SystemExit("degenerate vector")
    return [(value - center) / scale for value in values], center, scale


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b)) / len(a)


def main() -> None:
    policy = read_one(POLICY)
    if policy["status"] != "SOURCE_SIDE_JOINT_ROUTE_AUDIT_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad policy status")
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"{field} must be false")

    cc_rows = load_cc_rows()
    bao_rows = sorted(read_rows(BAO), key=lambda row: float(row["z_eff"]))
    if len(bao_rows) != 2:
        raise SystemExit("joint audit currently expects exactly two radial BAO rows")

    raw_bao = [float(row["time_readout_raw_minus_log_DH_over_rd"]) for row in bao_rows]
    bao_basis, bao_center, bao_scale = normalize(raw_bao)
    cc_level_raw: list[float] = []
    cc_slope_raw: list[float] = []
    rows: list[dict[str, str]] = []
    for row, bao_value in zip(bao_rows, bao_basis):
        z = float(row["z_eff"])
        idx = nearest_cc_index(cc_rows, z)
        cc = cc_rows[idx]
        level = math.log(float(cc["Hz"]))
        slope = logh_slope(cc_rows, idx)
        cc_level_raw.append(level)
        cc_slope_raw.append(slope)
        rows.append(
            {
                "audit_id": policy["audit_id"],
                "z_eff": row["z_eff"],
                "bao_observable": row["observable"],
                "bao_raw_minus_log_DH_over_rd": row["time_readout_raw_minus_log_DH_over_rd"],
                "bao_two_point_basis": f"{bao_value:.12g}",
                "nearest_cc_index": str(idx),
                "nearest_cc_z": f"{float(cc['z']):.12g}",
                "nearest_cc_Hz": f"{float(cc['Hz']):.12g}",
                "nearest_cc_reference": str(cc["reference"]),
                "cc_logH_level_raw": f"{level:.12g}",
                "cc_dlogH_dlog1pz_slope_raw": f"{slope:.12g}",
                "rd_nuisance_status": row["rd_nuisance_status"],
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    cc_level_basis, level_center, level_scale = normalize(cc_level_raw)
    cc_slope_basis, slope_center, slope_scale = normalize(cc_slope_raw)
    for row, level, slope in zip(rows, cc_level_basis, cc_slope_basis):
        row["cc_logH_level_two_point_basis"] = f"{level:.12g}"
        row["cc_slope_two_point_basis"] = f"{slope:.12g}"

    level_alignment = dot(bao_basis, cc_level_basis)
    slope_alignment = dot(bao_basis, cc_slope_basis)
    if level_alignment > 0 and slope_alignment < 0:
        verdict = "radial_bao_aligns_with_cc_level_not_cc_slope_underresolved_not_replay"
        interpretation = "BAO radial route supports an expansion-level time observable, not the current CC clock-slope route."
    elif level_alignment > 0 and slope_alignment > 0:
        verdict = "radial_bao_aligns_with_cc_level_and_slope_underresolved_not_replay"
        interpretation = "BAO radial route is directionally consistent with both checked CC time observables, but remains underresolved."
    else:
        verdict = "radial_bao_cc_time_route_direction_tension_underresolved_not_replay"
        interpretation = "BAO radial route does not directionally support the checked CC time observables under the frozen two-point audit."

    summary = [
        {
            "audit_id": policy["audit_id"],
            "status": "SOURCE_SIDE_JOINT_ROUTE_AUDIT_COMPLETE_NOT_REPLAY_NOT_VALIDATION",
            "radial_bao_rows": str(len(rows)),
            "nearest_cc_rows_used": str(len({row["nearest_cc_index"] for row in rows})),
            "bao_basis_center": f"{bao_center:.12g}",
            "bao_basis_scale": f"{bao_scale:.12g}",
            "cc_level_center": f"{level_center:.12g}",
            "cc_level_scale": f"{level_scale:.12g}",
            "cc_slope_center": f"{slope_center:.12g}",
            "cc_slope_scale": f"{slope_scale:.12g}",
            "bao_cc_level_two_point_alignment": f"{level_alignment:.12g}",
            "bao_cc_slope_two_point_alignment": f"{slope_alignment:.12g}",
            "rd_nuisance_unresolved": "true",
            "two_point_underresolved": "true",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": verdict,
            "interpretation": interpretation,
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_JOINT_CC_BAO_TIME_ROUTE_CONSISTENCY_AUDIT_BUILT "
        f"level_alignment={level_alignment:.3f} slope_alignment={slope_alignment:.3f} "
        f"verdict={verdict}"
    )


if __name__ == "__main__":
    main()
