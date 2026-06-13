#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "data/derived/void_source_basis_refinement_v2_sky_z_source_audit_v1.csv"
VOID = ROOT / "data/derived/low_z_pantheon_path_aware_void_geometry_v1.csv"
LOS = ROOT / "data/derived/low_z_pantheon_los_radial_profile_v1.csv"
WEB = ROOT / "data/derived/low_z_pantheon_directional_web_anisotropy_v1.csv"
OUT = ROOT / "data/derived/observer_path_metric_environment_product_v1.csv"
SUMMARY = ROOT / "data/derived/observer_path_metric_environment_product_v1_summary.csv"
DOC = ROOT / "docs/observer_path_metric_environment_product_v1.md"
CLAIM_BOUNDARY = "observer_path_metric_environment_product_source_side_not_endpoint_not_physical_lensing"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def to_float(value: str) -> float:
    if value is None or value == "":
        return math.nan
    return float(value)


def fmt(value: float) -> str:
    if math.isnan(value):
        return ""
    return f"{value:.12g}"


def max_abs(values: list[float], fallback: float = 1.0) -> float:
    finite = [abs(v) for v in values if math.isfinite(v)]
    if not finite:
        return fallback
    return max(max(finite), fallback)


def safe_norm(value: float, scale: float) -> float:
    if not math.isfinite(value):
        return 0.0
    return value / scale


def main() -> None:
    scope_rows = read_rows(SCOPE)
    void_by_idx = {row["source_row_index"]: row for row in read_rows(VOID)}
    los_by_idx = {row["source_row_index"]: row for row in read_rows(LOS)}
    web_by_idx = {row["source_row_index"]: row for row in read_rows(WEB)}
    indices = [row["source_row_index"] for row in scope_rows]
    if len(indices) != 12:
        raise SystemExit("observer/path product expects the frozen 12-row scope")
    missing = [idx for idx in indices if idx not in void_by_idx or idx not in los_by_idx or idx not in web_by_idx]
    if missing:
        raise SystemExit(f"missing source-side rows for indices: {missing}")

    void_depth_values = [to_float(void_by_idx[idx]["path_void_depth_fraction"]) for idx in indices]
    void_margin_values = [to_float(void_by_idx[idx]["path_void_crossing_margin_mpc_over_h"]) for idx in indices]
    los_near_far_values = [to_float(los_by_idx[idx]["near_minus_far_density"]) for idx in indices]
    los_fg_bg_values = [to_float(los_by_idx[idx]["foreground_minus_background_density"]) for idx in indices]
    web_aniso_values = []
    for idx in indices:
        dipole = to_float(web_by_idx[idx]["web_dipole_amplitude_rad"])
        quad = to_float(web_by_idx[idx]["web_quadrupole_q"])
        if math.isfinite(dipole) or math.isfinite(quad):
            web_aniso_values.append(math.hypot(0.0 if math.isnan(dipole) else dipole, 0.0 if math.isnan(quad) else quad))
        else:
            web_aniso_values.append(math.nan)

    void_depth_scale = max_abs(void_depth_values)
    void_margin_scale = max_abs(void_margin_values)
    los_near_far_scale = max_abs(los_near_far_values)
    los_fg_bg_scale = max_abs(los_fg_bg_values)
    web_aniso_scale = max_abs(web_aniso_values)

    rows: list[dict[str, str]] = []
    for scope in scope_rows:
        idx = scope["source_row_index"]
        void = void_by_idx[idx]
        los = los_by_idx[idx]
        web = web_by_idx[idx]
        void_depth = to_float(void["path_void_depth_fraction"])
        void_margin = to_float(void["path_void_crossing_margin_mpc_over_h"])
        los_near_far = to_float(los["near_minus_far_density"])
        los_fg_bg = to_float(los["foreground_minus_background_density"])
        web_aniso = web_aniso_values[indices.index(idx)]
        los_nonempty = int(los["profile_nonempty_shell_count"])
        web_count = int(web["web_cone_count"])

        void_component = 0.70 * safe_norm(void_depth, void_depth_scale) + 0.30 * safe_norm(
            void_margin, void_margin_scale
        )
        los_component = 0.60 * safe_norm(los_near_far, los_near_far_scale) + 0.40 * safe_norm(
            los_fg_bg, los_fg_bg_scale
        )
        web_component = safe_norm(web_aniso, web_aniso_scale)
        los_weight = 1.0 if los_nonempty >= 3 else (0.5 if los_nonempty > 0 else 0.0)
        web_weight = 1.0 if web_count >= 3 else (0.5 if web_count > 0 else 0.0)
        raw = (
            0.50 * void_component
            + 0.25 * los_weight * los_component
            + 0.25 * web_weight * web_component
        )
        product = raw / (1.0 + abs(raw))
        rows.append(
            {
                "artifact_id": "OBSERVER_PATH_METRIC_ENVIRONMENT_PRODUCT_V1",
                "CID": scope["CID"],
                "source_row_index": idx,
                "zHD": scope["zHD"],
                "ra_deg": scope["ra_deg"],
                "dec_deg": scope["dec_deg"],
                "metric_environment_product_available_for_source": "true",
                "product_class": "caveated_metric_environment_path_proxy",
                "void_depth_fraction": fmt(void_depth),
                "void_crossing_margin_mpc_over_h": fmt(void_margin),
                "void_component": fmt(void_component),
                "los_near_minus_far_density": fmt(los_near_far),
                "los_foreground_minus_background_density": fmt(los_fg_bg),
                "los_profile_nonempty_shell_count": los["profile_nonempty_shell_count"],
                "los_component": fmt(los_component),
                "los_component_weight": fmt(los_weight),
                "web_cone_count": web["web_cone_count"],
                "web_anisotropy_component_raw": fmt(web_aniso),
                "web_component": fmt(web_component),
                "web_component_weight": fmt(web_weight),
                "metric_environment_path_weight_raw": fmt(raw),
                "metric_environment_path_weight": fmt(product),
                "normalization_rule": "bounded_raw_over_1_plus_abs_raw_with_scope_internal_source_side_scales",
                "source_inputs": "void_path_geometry;los_radial_profile;directional_web_anisotropy",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "contains_lensing_residuals": "false",
                "contains_fit_statistics": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, rows)
    available = sum(row["metric_environment_product_available_for_source"] == "true" for row in rows)
    nonzero = sum(abs(float(row["metric_environment_path_weight"])) > 0 for row in rows)
    summary = [
        {
            "artifact_id": "OBSERVER_PATH_METRIC_ENVIRONMENT_PRODUCT_V1",
            "status": "SOURCE_ALIGNED_CAVEATED_METRIC_ENVIRONMENT_PRODUCT_BUILT_NOT_ENDPOINT",
            "observer_path_scope_rows": str(len(rows)),
            "metric_environment_product_available_count": str(available),
            "nonzero_metric_environment_path_weight_count": str(nonzero),
            "void_depth_scale": fmt(void_depth_scale),
            "void_margin_scale": fmt(void_margin_scale),
            "los_near_far_scale": fmt(los_near_far_scale),
            "los_fg_bg_scale": fmt(los_fg_bg_scale),
            "web_aniso_scale": fmt(web_aniso_scale),
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "CAVEATED_SOURCE_ALIGNED_METRIC_ENVIRONMENT_PRODUCT_AVAILABLE_NOT_PHYSICAL_LENSING",
        }
    ]
    write_csv(SUMMARY, summary)
    DOC.write_text(
        "# Observer/path metric-environment product v1\n\n"
        "**Doc class:** source-aligned metric-environment product\n"
        "**Status:** not endpoint replay; not validation; not physical lensing\n\n"
        "This artifact fills the active 12-row observer/path scope with a numeric, "
        "source-aligned metric-environment path proxy built only from existing "
        "source-side path-aware void geometry, line-of-sight radial-profile, and "
        "directional-web anisotropy artifacts. It does not use endpoint residuals, "
        "distance residuals, fitted scores, or post-hoc improvement selection.\n\n"
        "The product is intentionally weaker than a physical lensing product: it is "
        "not kappa, shear, or a mass-map integral. It may support a caveated "
        "metric-environment observer/path route, but it does not support a physical "
        "lensing-path claim.\n\n"
        f"Rows: `{len(rows)}`. Available products: `{available}`. Nonzero weights: `{nonzero}`.\n\n"
        f"Claim boundary: `{CLAIM_BOUNDARY}`.\n"
    )
    print(
        "OBSERVER_PATH_METRIC_ENVIRONMENT_PRODUCT_V1_BUILT "
        f"rows={len(rows)} available={available} nonzero={nonzero}"
    )


if __name__ == "__main__":
    main()
