#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METRIC_ENV = ROOT / "data/derived/observer_path_metric_environment_product_v1.csv"
OBSERVER = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2.csv"
DESIGN = ROOT / "data/derived/pantheon_void_web_source_native_design_matrix_v1.csv"
OUT = ROOT / "data/derived/observer_path_source_native_ordering_kernel_v1.csv"
SUMMARY = ROOT / "data/derived/observer_path_source_native_ordering_kernel_v1_summary.csv"
DOC = ROOT / "docs/observer_path_source_native_ordering_kernel_v1.md"
CLAIM_BOUNDARY = "observer_path_source_native_ordering_kernel_source_side_not_endpoint"


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


def fmt(value: float) -> str:
    return f"{value:.12g}"


def max_abs(values: list[float], fallback: float = 1.0) -> float:
    finite = [abs(value) for value in values if math.isfinite(value)]
    return max(max(finite), fallback) if finite else fallback


def bounded(value: float) -> float:
    return value / (1.0 + abs(value))


def normalized(values: list[float]) -> list[float]:
    scale = max_abs(values)
    return [value / scale if math.isfinite(value) else 0.0 for value in values]


def main() -> None:
    metric_rows = read_rows(METRIC_ENV)
    observer_by_source = {row["source_row_index"]: row for row in read_rows(OBSERVER)}
    design_by_source = {row["source_row_index"]: row for row in read_rows(DESIGN)}
    if len(metric_rows) != 12:
        raise SystemExit("source-native ordering kernel expects the frozen 12-row observer/path scope")

    z_values = [float(design_by_source[row["source_row_index"]]["zHD"]) for row in metric_rows]
    z_mean = sum(z_values) / len(z_values)
    z_center_raw = [value - z_mean for value in z_values]
    z_center = normalized(z_center_raw)
    rows: list[dict[str, str]] = []
    raw_columns: dict[str, list[float]] = {
        "K_order_metric_environment": [],
        "K_order_los_web_gate": [],
        "K_order_void_web_los_balanced": [],
        "K_order_metric_los_skyz": [],
        "K_order_metric_observer_x_z": [],
        "K_order_metric_environment_gradient": [],
    }

    prepared: list[dict[str, float | str]] = []
    for i, row in enumerate(metric_rows):
        source = row["source_row_index"]
        observer = observer_by_source[source]
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
                raise SystemExit(f"unsafe field {key} is not false for {source}")
        metric = float(row["metric_environment_path_weight"])
        void_component = float(row["void_component"])
        los_component = float(row["los_component"])
        web_component = float(row["web_component"])
        sky_x = float(observer["sky_x"])
        sky_z = float(observer["sky_z"])
        w_path = float(observer["W_path_source_value"])
        prepared.append(
            {
                "CID": row["CID"],
                "source_row_index": source,
                "zHD": z_values[i],
                "metric": metric,
                "void": void_component,
                "los": los_component,
                "web": web_component,
                "sky_x": sky_x,
                "sky_z": sky_z,
                "w_path": w_path,
                "z_center": z_center[i],
            }
        )

    for item in prepared:
        metric = float(item["metric"])
        void_component = float(item["void"])
        los_component = float(item["los"])
        web_component = float(item["web"])
        sky_x = float(item["sky_x"])
        sky_z = float(item["sky_z"])
        w_path = float(item["w_path"])
        zc = float(item["z_center"])

        raw_columns["K_order_metric_environment"].append(metric)
        raw_columns["K_order_los_web_gate"].append((0.55 * los_component + 0.45 * web_component) * (1.0 + abs(void_component)))
        raw_columns["K_order_void_web_los_balanced"].append(0.40 * void_component + 0.30 * los_component + 0.30 * web_component)
        raw_columns["K_order_metric_los_skyz"].append(metric * (1.0 + los_component) * sky_z)
        raw_columns["K_order_metric_observer_x_z"].append(metric * sky_x * zc)
        raw_columns["K_order_metric_environment_gradient"].append(metric * (web_component - los_component) * (1.0 + abs(w_path)))

    normalized_columns = {key: normalized(values) for key, values in raw_columns.items()}
    for i, item in enumerate(prepared):
        out_row = {
            "artifact_id": "OBSERVER_PATH_SOURCE_NATIVE_ORDERING_KERNEL_V1",
            "CID": str(item["CID"]),
            "source_row_index": str(item["source_row_index"]),
            "zHD": fmt(float(item["zHD"])),
            "metric_environment_path_weight": fmt(float(item["metric"])),
            "void_component": fmt(float(item["void"])),
            "los_component": fmt(float(item["los"])),
            "web_component": fmt(float(item["web"])),
            "sky_x": fmt(float(item["sky_x"])),
            "sky_z": fmt(float(item["sky_z"])),
            "W_path_source_value": fmt(float(item["w_path"])),
            "z_center_normalized": fmt(float(item["z_center"])),
        }
        for key, values in raw_columns.items():
            out_row[f"{key}_raw"] = fmt(values[i])
            out_row[key] = fmt(bounded(normalized_columns[key][i]))
        out_row.update(
            {
                "kernel_bank_rule": "predeclared_source_side_ordering_bank_void_los_web_observer_basis",
                "source_inputs": "metric_environment_product;observer_orientation_kernel;design_zHD",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        rows.append(out_row)

    write_csv(OUT, rows)
    summary = {
        "artifact_id": "OBSERVER_PATH_SOURCE_NATIVE_ORDERING_KERNEL_V1",
        "status": "SOURCE_NATIVE_ORDERING_KERNEL_BANK_BUILT_NOT_ENDPOINT",
        "n_rows": str(len(rows)),
        "kernel_family_count": str(len(raw_columns)),
        "kernel_families": ";".join(raw_columns),
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "contains_endpoint_scores": "false",
        "contains_distance_residuals": "false",
        "physical_lensing_path_weight_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "SOURCE_NATIVE_ORDERING_KERNEL_BANK_READY_FOR_PREAUTH_SCREEN_NOT_ENDPOINT",
    }
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Observer/path source-native ordering kernel v1",
                "",
                "**Doc class:** source-side kernel-bank construction",
                "**Status:** not endpoint replay; not validation; no residual fields",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "The previous metric-environment product improved the baseline but",
                "failed the rank-reversal control. This artifact freezes a small",
                "source-native ordering-bank before any new scoring claim. The bank",
                "uses only the already frozen metric-environment product, observer",
                "orientation basis, and source redshift coordinate.",
                "",
                "Kernel families:",
                "",
                "- `K_order_metric_environment`: direct metric-environment carrier.",
                "- `K_order_los_web_gate`: LOS/web gate modulated by path-void support.",
                "- `K_order_void_web_los_balanced`: balanced source-side environment rule.",
                "- `K_order_metric_los_skyz`: metric environment modulated by LOS and sky-z.",
                "- `K_order_metric_observer_x_z`: metric environment modulated by observer x and centered redshift.",
                "- `K_order_metric_environment_gradient`: web-minus-LOS environment gradient.",
                "",
                "This is a candidate bank for a preauthorization screen only. It does",
                "not authorize endpoint replay and does not claim physical lensing.",
                "",
            ]
        )
    )
    print(
        "OBSERVER_PATH_SOURCE_NATIVE_ORDERING_KERNEL_V1_BUILT "
        f"rows={summary['n_rows']} families={summary['kernel_family_count']}"
    )


if __name__ == "__main__":
    main()
