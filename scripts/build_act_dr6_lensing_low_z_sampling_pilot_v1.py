#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import healpy as hp
import numpy as np
from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "derived" / "low_z_pantheon_void_geometry_join_v1.csv"
RAW = ROOT / "data" / "raw" / "weak_lensing" / "act_dr6_lensing" / "extracted_sampling_v1" / "maps"
OUT = ROOT / "data" / "derived" / "act_dr6_lensing_low_z_sampling_pilot_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_low_z_sampling_pilot_v1_summary.csv"
DOC = ROOT / "docs" / "act_dr6_lensing_low_z_sampling_pilot_v1.md"

CLAIM_BOUNDARY = "act_dr6_lensing_low_z_sampling_pilot_source_side_not_endpoint_not_validation"
NSIDE_MAP = 512
NSIDE_MASK = 4096
L_MAX_OUT = 1024

VARIANTS = {
    "baseline": RAW / "baseline" / "kappa_alm_data_act_dr6_lensing_v1_baseline.fits",
    "curl": RAW / "curl" / "kappa_alm_data_act_dr6_lensing_v1_curl.fits",
    "diff_f150_f090": RAW
    / "diff_f150_f090"
    / "kappa_alm_data_act_dr6_lensing_v1_diff_f150_f090.fits",
}
MASK = RAW / "baseline" / "mask_act_dr6_lensing_v1_healpix_nside_4096_baseline.fits"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sample_variant(path: Path, ra: np.ndarray, dec: np.ndarray) -> tuple[np.ndarray, dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing ACT kappa alm file: {path.relative_to(ROOT)}")
    alm = hp.read_alm(path, hdu=1)
    nonfinite = int(np.count_nonzero(~np.isfinite(alm)))
    alm = np.nan_to_num(alm, nan=0.0, posinf=0.0, neginf=0.0)
    lmax_in = hp.Alm.getlmax(len(alm))
    alm_lr = hp.resize_alm(alm, lmax_in, lmax_in, L_MAX_OUT, L_MAX_OUT)
    kappa_map = hp.alm2map(alm_lr, nside=NSIDE_MAP, lmax=L_MAX_OUT)
    pix = hp.ang2pix(NSIDE_MAP, ra, dec, lonlat=True)
    values = np.asarray(kappa_map[pix], dtype=float)
    finite = np.isfinite(values)
    meta = {
        "lmax_in": str(lmax_in),
        "nonfinite_alm_entries_replaced_with_zero": str(nonfinite),
        "sample_finite_count": str(int(np.count_nonzero(finite))),
        "sample_nonfinite_count": str(int(np.count_nonzero(~finite))),
    }
    return values, meta


def sample_mask(path: Path, ra: np.ndarray, dec: np.ndarray) -> np.ndarray:
    if not path.exists():
        raise SystemExit(f"missing ACT mask file: {path.relative_to(ROOT)}")
    pix = hp.ang2pix(NSIDE_MASK, ra, dec, lonlat=True)
    rows = pix // 1024
    offsets = pix % 1024
    values = np.empty(len(pix), dtype=float)
    with fits.open(path, memmap=True) as hdul:
        field = hdul[1].data.field(0)
        for i, (row, offset) in enumerate(zip(rows, offsets, strict=True)):
            values[i] = float(field[int(row)][int(offset)])
    return values


def fmt(value: float) -> str:
    if not np.isfinite(value):
        return "nan"
    return f"{value:.12g}"


def main() -> None:
    source_rows = read_csv(INPUT)
    ra = np.array([float(row["ra_deg"]) for row in source_rows], dtype=float)
    dec = np.array([float(row["dec_deg"]) for row in source_rows], dtype=float)

    sampled: dict[str, np.ndarray] = {}
    variant_meta: dict[str, dict[str, str]] = {}
    for variant, path in VARIANTS.items():
        values, meta = sample_variant(path, ra, dec)
        sampled[variant] = values
        variant_meta[variant] = meta

    mask_values = sample_mask(MASK, ra, dec)
    mask_positive = mask_values > 0

    rows: list[dict[str, str]] = []
    for i, row in enumerate(source_rows):
        rows.append(
            {
                "artifact_id": "ACT_DR6_LENSING_LOW_Z_SAMPLING_PILOT_V1",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "coordinate_source": row["coordinate_source"],
                "ra_deg": row["ra_deg"],
                "dec_deg": row["dec_deg"],
                "nside_map": str(NSIDE_MAP),
                "lmax_out": str(L_MAX_OUT),
                "baseline_kappa_lr": fmt(sampled["baseline"][i]),
                "curl_kappa_lr": fmt(sampled["curl"][i]),
                "diff_f150_f090_kappa_lr": fmt(sampled["diff_f150_f090"][i]),
                "baseline_mask_nside4096": fmt(mask_values[i]),
                "mask_positive": str(bool(mask_positive[i])).lower(),
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "contains_distance_residuals": "false",
                "contains_fit_statistics": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, rows)

    summary = {
        "artifact_id": "ACT_DR6_LENSING_LOW_Z_SAMPLING_PILOT_V1",
        "status": "SOURCE_SIDE_SAMPLING_PILOT_BUILT_NOT_ENDPOINT",
        "source_rows": str(len(source_rows)),
        "nside_map": str(NSIDE_MAP),
        "nside_mask": str(NSIDE_MASK),
        "lmax_out": str(L_MAX_OUT),
        "variants_sampled": ";".join(VARIANTS.keys()),
        "baseline_lmax_in": variant_meta["baseline"]["lmax_in"],
        "baseline_nonfinite_alm_entries_replaced_with_zero": variant_meta["baseline"][
            "nonfinite_alm_entries_replaced_with_zero"
        ],
        "curl_nonfinite_alm_entries_replaced_with_zero": variant_meta["curl"][
            "nonfinite_alm_entries_replaced_with_zero"
        ],
        "diff_f150_f090_nonfinite_alm_entries_replaced_with_zero": variant_meta["diff_f150_f090"][
            "nonfinite_alm_entries_replaced_with_zero"
        ],
        "baseline_sample_finite_count": variant_meta["baseline"]["sample_finite_count"],
        "curl_sample_finite_count": variant_meta["curl"]["sample_finite_count"],
        "diff_f150_f090_sample_finite_count": variant_meta["diff_f150_f090"]["sample_finite_count"],
        "mask_positive_count": str(int(np.count_nonzero(mask_positive))),
        "mask_zero_count": str(int(len(mask_positive) - np.count_nonzero(mask_positive))),
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "act_dr6_low_z_sampling_pilot_built_source_side_not_endpoint",
    }
    write_csv(SUMMARY, [summary])

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# ACT DR6 lensing low-z sampling pilot v1",
                "",
                "This source-side pilot samples the ACT DR6 lensing convergence alm products",
                "at the low-z Pantheon sky positions. The baseline map is treated as the",
                "recommended science route, while curl and diff_f150_f090 are retained as",
                "null-control products.",
                "",
                "The artifact is not an endpoint replay, not a validation result, and not a",
                "physical lensing path-weight derivation. It contains no distance residuals",
                "and no fit statistics.",
                "",
                f"- rows: {summary['source_rows']}",
                f"- nside map: {NSIDE_MAP}",
                f"- output lmax: {L_MAX_OUT}",
                f"- mask-positive rows: {summary['mask_positive_count']}",
                f"- claim boundary: {CLAIM_BOUNDARY}",
                "",
            ]
        )
    )
    print(
        "ACT_DR6_LENSING_LOW_Z_SAMPLING_PILOT_V1_BUILT "
        f"rows={summary['source_rows']} mask_positive={summary['mask_positive_count']} endpoint=false"
    )


if __name__ == "__main__":
    main()
