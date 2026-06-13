#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "derived" / "act_dr6_lensing_low_z_sampling_pilot_v1.csv"
OUT = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_candidate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_candidate_v1_summary.csv"
DOC = ROOT / "docs" / "act_dr6_lensing_path_weight_candidate_v1.md"
CLAIM_BOUNDARY = "act_dr6_lensing_path_weight_candidate_source_side_not_endpoint_not_validation"

VALUE_FIELDS = {
    "baseline": "baseline_kappa_lr",
    "curl": "curl_kappa_lr",
    "diff_f150_f090": "diff_f150_f090_kappa_lr",
}


def read_rows(path: Path) -> list[dict[str, str]]:
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


def to_float(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        return math.nan


def fmt(value: float) -> str:
    if not math.isfinite(value):
        return ""
    return f"{value:.12g}"


def median_mad(values: list[float]) -> tuple[float, float]:
    finite = [v for v in values if math.isfinite(v)]
    if len(finite) < 3:
        raise SystemExit("not enough finite values for robust source-side normalization")
    med = statistics.median(finite)
    mad = statistics.median([abs(v - med) for v in finite])
    if mad <= 0:
        # Keep the rule deterministic without silently accepting a degenerate channel.
        stdev = statistics.pstdev(finite)
        if stdev <= 0:
            raise SystemExit("degenerate source-side channel: zero MAD and zero standard deviation")
        return med, stdev
    return med, 1.4826 * mad


def pearson(xs: list[float], ys: list[float]) -> float:
    pairs = [(x, y) for x, y in zip(xs, ys, strict=True) if math.isfinite(x) and math.isfinite(y)]
    if len(pairs) < 3:
        return math.nan
    xvals = [p[0] for p in pairs]
    yvals = [p[1] for p in pairs]
    xmean = statistics.mean(xvals)
    ymean = statistics.mean(yvals)
    xden = math.sqrt(sum((x - xmean) ** 2 for x in xvals))
    yden = math.sqrt(sum((y - ymean) ** 2 for y in yvals))
    if xden == 0 or yden == 0:
        return math.nan
    return sum((x - xmean) * (y - ymean) for x, y in pairs) / (xden * yden)


def main() -> None:
    rows_in = read_rows(INPUT)
    if not rows_in:
        raise SystemExit("ACT DR6 sampling pilot is empty")

    mask_positive = [row["mask_positive"] == "true" for row in rows_in]
    if not any(mask_positive):
        raise SystemExit("no mask-positive rows available for path-weight candidate")

    values = {
        variant: [to_float(row[field]) if keep else math.nan for row, keep in zip(rows_in, mask_positive, strict=True)]
        for variant, field in VALUE_FIELDS.items()
    }
    scales = {variant: median_mad(vs) for variant, vs in values.items()}

    weights: dict[str, list[float]] = {}
    for variant, vs in values.items():
        center, scale = scales[variant]
        weights[variant] = [((v - center) / scale) if math.isfinite(v) else 0.0 for v in vs]

    rows_out: list[dict[str, str]] = []
    for i, row in enumerate(rows_in):
        rows_out.append(
            {
                "artifact_id": "ACT_DR6_LENSING_PATH_WEIGHT_CANDIDATE_V1",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "ra_deg": row["ra_deg"],
                "dec_deg": row["dec_deg"],
                "mask_positive": row["mask_positive"],
                "baseline_mask_nside4096": row["baseline_mask_nside4096"],
                "baseline_kappa_lr": row["baseline_kappa_lr"],
                "curl_kappa_lr": row["curl_kappa_lr"],
                "diff_f150_f090_kappa_lr": row["diff_f150_f090_kappa_lr"],
                "w_act_baseline_candidate": fmt(weights["baseline"][i]),
                "w_act_curl_null": fmt(weights["curl"][i]),
                "w_act_diff_f150_f090_null": fmt(weights["diff_f150_f090"][i]),
                "normalization_rule": "mask_positive_only_median_center_mad_scale_else_zero",
                "candidate_role": "baseline_science_candidate" if row["mask_positive"] == "true" else "outside_act_mask_zero_weight",
                "null_control_roles": "curl;diff_f150_f090",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "contains_distance_residuals": "false",
                "contains_fit_statistics": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    write_csv(OUT, rows_out)

    baseline_active = [weights["baseline"][i] for i, keep in enumerate(mask_positive) if keep]
    curl_active = [weights["curl"][i] for i, keep in enumerate(mask_positive) if keep]
    diff_active = [weights["diff_f150_f090"][i] for i, keep in enumerate(mask_positive) if keep]
    summary = {
        "artifact_id": "ACT_DR6_LENSING_PATH_WEIGHT_CANDIDATE_V1",
        "status": "SOURCE_SIDE_PATH_WEIGHT_CANDIDATE_BUILT_NOT_ENDPOINT",
        "source_rows": str(len(rows_in)),
        "mask_positive_rows": str(sum(mask_positive)),
        "mask_zero_rows": str(len(rows_in) - sum(mask_positive)),
        "normalization_rule": "mask_positive_only_median_center_mad_scale_else_zero",
        "baseline_center_median": fmt(scales["baseline"][0]),
        "baseline_scale_mad14826": fmt(scales["baseline"][1]),
        "curl_center_median": fmt(scales["curl"][0]),
        "curl_scale_mad14826": fmt(scales["curl"][1]),
        "diff_f150_f090_center_median": fmt(scales["diff_f150_f090"][0]),
        "diff_f150_f090_scale_mad14826": fmt(scales["diff_f150_f090"][1]),
        "baseline_active_mean": fmt(statistics.mean(baseline_active)),
        "baseline_active_std": fmt(statistics.pstdev(baseline_active)),
        "curl_active_mean": fmt(statistics.mean(curl_active)),
        "diff_f150_f090_active_mean": fmt(statistics.mean(diff_active)),
        "corr_baseline_curl_active": fmt(pearson(baseline_active, curl_active)),
        "corr_baseline_diff_f150_f090_active": fmt(pearson(baseline_active, diff_active)),
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "act_dr6_source_side_path_weight_candidate_ready_for_review_not_endpoint",
    }
    write_csv(SUMMARY, [summary])

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# ACT DR6 lensing path-weight candidate v1",
                "",
                "This artifact freezes a source-side, unitless observer/path lensing",
                "candidate from ACT DR6 low-resolution kappa sampling. It uses only",
                "mask-positive ACT rows for robust median/MAD normalization and assigns",
                "zero weight outside the ACT baseline mask.",
                "",
                "The baseline channel is the science candidate. Curl and f150-f090",
                "difference channels are retained as null controls. The artifact is not",
                "endpoint replay, not validation, and not a physical metric/lensing",
                "path-weight derivation.",
                "",
                f"- source rows: {summary['source_rows']}",
                f"- mask-positive rows: {summary['mask_positive_rows']}",
                f"- corr baseline/curl: {summary['corr_baseline_curl_active']}",
                f"- corr baseline/diff_f150_f090: {summary['corr_baseline_diff_f150_f090_active']}",
                f"- claim boundary: {CLAIM_BOUNDARY}",
                "",
            ]
        )
    )
    print(
        "ACT_DR6_LENSING_PATH_WEIGHT_CANDIDATE_V1_BUILT "
        f"rows={summary['source_rows']} mask_positive={summary['mask_positive_rows']} endpoint=false"
    )


if __name__ == "__main__":
    main()
