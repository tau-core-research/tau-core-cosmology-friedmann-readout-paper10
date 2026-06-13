#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METRIC_ENV = ROOT / "data/derived/observer_path_metric_environment_product_v1.csv"
OBSERVER = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2.csv"
DESIGN = ROOT / "data/derived/pantheon_void_web_source_native_design_matrix_v1.csv"
SCREEN_SUMMARY = ROOT / "data/derived/observer_path_metric_environment_fast_screen_v1_summary.csv"
SCREEN_FAMILY = ROOT / "data/derived/observer_path_metric_environment_fast_screen_v1_family_summary.csv"
OUT = ROOT / "data/derived/observer_path_metric_environment_ordering_diagnostic_v1.csv"
PAIRWISE = ROOT / "data/derived/observer_path_metric_environment_ordering_diagnostic_v1_pairwise.csv"
SUMMARY = ROOT / "data/derived/observer_path_metric_environment_ordering_diagnostic_v1_summary.csv"
DOC = ROOT / "docs/observer_path_metric_environment_ordering_diagnostic_v1.md"
CLAIM_BOUNDARY = "observer_path_metric_environment_ordering_diagnostic_source_side_not_endpoint"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
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


def rank(values: list[float], reverse: bool = False) -> list[int]:
    ordered = sorted(enumerate(values), key=lambda item: item[1], reverse=reverse)
    ranks = [0] * len(values)
    for i, (idx, _value) in enumerate(ordered, start=1):
        ranks[idx] = i
    return ranks


def spearman(xs: list[float], ys: list[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 3:
        return math.nan
    rx = rank(xs)
    ry = rank(ys)
    mx = sum(rx) / len(rx)
    my = sum(ry) / len(ry)
    num = sum((x - mx) * (y - my) for x, y in zip(rx, ry, strict=True))
    denx = math.sqrt(sum((x - mx) ** 2 for x in rx))
    deny = math.sqrt(sum((y - my) ** 2 for y in ry))
    if denx == 0.0 or deny == 0.0:
        return math.nan
    return num / (denx * deny)


def normalized_rank_reverse(values: list[float]) -> list[float]:
    sorted_desc = sorted(values, reverse=True)
    return sorted_desc


def main() -> None:
    screen_summary = read_rows(SCREEN_SUMMARY)[0]
    if screen_summary["best_candidate_survives_controls"] != "false":
        raise SystemExit("ordering diagnostic is intended for the non-control-resistant screen state")
    if screen_summary["best_candidate_family"] != "metric_environment_path":
        raise SystemExit("unexpected best candidate family")

    families = read_rows(SCREEN_FAMILY)
    best_family = next(row for row in families if row["family_id"] == "metric_environment_path")
    if best_family["best_control_branch"] != "rank_reverse":
        raise SystemExit("ordering diagnostic expects rank_reverse as the best control")

    design_by_source = {row["source_row_index"]: row for row in read_rows(DESIGN)}
    observer_by_source = {row["source_row_index"]: row for row in read_rows(OBSERVER)}
    rows = read_rows(METRIC_ENV)
    source_rows: list[dict[str, str]] = []
    metric_values: list[float] = []
    z_values: list[float] = []
    sky_x_values: list[float] = []
    sky_z_values: list[float] = []
    w_path_values: list[float] = []
    void_values: list[float] = []
    los_values: list[float] = []
    web_values: list[float] = []
    cids: list[str] = []

    for row in rows:
        source = row["source_row_index"]
        if row["metric_environment_product_available_for_source"] != "true":
            raise SystemExit(f"metric environment product unavailable for {source}")
        for key in [
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "contains_endpoint_scores",
            "contains_distance_residuals",
            "contains_lensing_residuals",
            "contains_fit_statistics",
            "physical_lensing_path_weight_claimed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"forbidden source leakage flag {key} is not false for {source}")
        design = design_by_source[source]
        observer = observer_by_source[source]
        metric = float(row["metric_environment_path_weight"])
        z = float(design["zHD"])
        sky_x = float(observer["sky_x"])
        sky_z = float(observer["sky_z"])
        w_path = float(observer["W_path_source_value"])
        void_component = float(row["void_component"])
        los_component = float(row["los_component"])
        web_component = float(row["web_component"])
        cids.append(row["CID"])
        metric_values.append(metric)
        z_values.append(z)
        sky_x_values.append(sky_x)
        sky_z_values.append(sky_z)
        w_path_values.append(w_path)
        void_values.append(void_component)
        los_values.append(los_component)
        web_values.append(web_component)

    metric_rank_low_to_high = rank(metric_values)
    metric_rank_high_to_low = rank(metric_values, reverse=True)
    z_rank_low_to_high = rank(z_values)
    reversed_values = normalized_rank_reverse(metric_values)
    reversed_rank_low_to_high = rank(reversed_values)
    for i, row in enumerate(rows):
        source_rows.append(
            {
                "diagnostic_id": "OBSERVER_PATH_METRIC_ENVIRONMENT_ORDERING_DIAGNOSTIC_V1",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": f"{z_values[i]:.12g}",
                "metric_environment_path_weight": f"{metric_values[i]:.12g}",
                "metric_environment_rank_low_to_high": str(metric_rank_low_to_high[i]),
                "metric_environment_rank_high_to_low": str(metric_rank_high_to_low[i]),
                "rank_reverse_control_value_at_position": f"{reversed_values[i]:.12g}",
                "rank_reverse_rank_low_to_high": str(reversed_rank_low_to_high[i]),
                "z_rank_low_to_high": str(z_rank_low_to_high[i]),
                "void_component": f"{void_values[i]:.12g}",
                "los_component": f"{los_values[i]:.12g}",
                "web_component": f"{web_values[i]:.12g}",
                "sky_x": f"{sky_x_values[i]:.12g}",
                "sky_z": f"{sky_z_values[i]:.12g}",
                "W_path_source_value": f"{w_path_values[i]:.12g}",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    metrics = {
        "zHD": z_values,
        "sky_x": sky_x_values,
        "sky_z": sky_z_values,
        "W_path_source_value": w_path_values,
        "void_component": void_values,
        "los_component": los_values,
        "web_component": web_values,
    }
    pairwise_rows = []
    for name, values in metrics.items():
        pairwise_rows.append(
            {
                "diagnostic_id": "OBSERVER_PATH_METRIC_ENVIRONMENT_ORDERING_DIAGNOSTIC_V1",
                "quantity": name,
                "spearman_rho_with_metric_environment_path": f"{spearman(metric_values, values):.12g}",
                "spearman_rho_with_rank_reverse_position_value": f"{spearman(reversed_values, values):.12g}",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    rho_metric_z = spearman(metric_values, z_values)
    rho_reverse_z = spearman(reversed_values, z_values)
    rho_metric_w_path = spearman(metric_values, w_path_values)
    delta_candidate_control = float(best_family["delta_chi2_candidate_minus_best_control"])
    if delta_candidate_control <= 0:
        verdict = "ORDERING_DIAGNOSTIC_UNEXPECTED_CONTROL_SURVIVAL"
    elif abs(rho_metric_z) >= 0.75 or abs(rho_metric_w_path) >= 0.75:
        verdict = "SOURCE_ORDER_TOO_MONOTONIC_CONTROL_CAN_EXPLOIT_NOT_ENDPOINT"
    else:
        verdict = "SOURCE_ORDER_NOT_CONTROL_RESISTANT_REQUIRES_SOURCE_NATIVE_REORDERING_NOT_ENDPOINT"

    summary = {
        "diagnostic_id": "OBSERVER_PATH_METRIC_ENVIRONMENT_ORDERING_DIAGNOSTIC_V1",
        "n_rows": str(len(rows)),
        "cids": ";".join(cids),
        "best_candidate_family": screen_summary["best_candidate_family"],
        "best_control_branch": best_family["best_control_branch"],
        "delta_chi2_candidate_minus_best_control": best_family["delta_chi2_candidate_minus_best_control"],
        "spearman_metric_environment_with_zHD": f"{rho_metric_z:.12g}",
        "spearman_rank_reverse_position_value_with_zHD": f"{rho_reverse_z:.12g}",
        "spearman_metric_environment_with_W_path": f"{rho_metric_w_path:.12g}",
        "interpretation": "rank_reverse control beats the source-ordered metric-environment candidate; use this only to guide a future source-side ordering rule",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "contains_endpoint_scores": "false",
        "contains_distance_residuals": "false",
        "physical_lensing_path_weight_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": verdict,
    }
    write_csv(OUT, source_rows)
    write_csv(PAIRWISE, pairwise_rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Observer/path metric-environment ordering diagnostic v1",
                "",
                "**Doc class:** source-side ordering diagnostic",
                "**Status:** not endpoint replay; not validation; no distance residuals",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "The metric-environment fast screen improved relative to the baseline",
                "but failed the rank-reversal control. This diagnostic records the",
                "source-side ordering of the metric-environment product and compares",
                "it to frozen source observables. It is not a retuning step.",
                "",
                "Summary:",
                "",
                f"- rows: `{summary['n_rows']}`",
                f"- best candidate family: `{summary['best_candidate_family']}`",
                f"- best control branch: `{summary['best_control_branch']}`",
                f"- candidate minus best-control delta chi2: `{summary['delta_chi2_candidate_minus_best_control']}`",
                f"- Spearman(metric environment, zHD): `{summary['spearman_metric_environment_with_zHD']}`",
                f"- Spearman(metric environment, W_path): `{summary['spearman_metric_environment_with_W_path']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: the current source-side product is too weakly",
                "control-resistant for replay promotion. A next kernel must provide a",
                "source-native ordering rule that is frozen before endpoint scoring.",
                "",
            ]
        )
    )
    print(
        "OBSERVER_PATH_METRIC_ENVIRONMENT_ORDERING_DIAGNOSTIC_V1_BUILT "
        f"rho_z={summary['spearman_metric_environment_with_zHD']} "
        f"rho_w_path={summary['spearman_metric_environment_with_W_path']} "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
