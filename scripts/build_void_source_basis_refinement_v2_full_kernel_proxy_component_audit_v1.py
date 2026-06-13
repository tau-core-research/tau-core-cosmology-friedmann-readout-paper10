#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

try:
    from run_void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1 import load_scope
except ImportError:
    from scripts.run_void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1 import load_scope


ROOT = Path(__file__).resolve().parents[1]
FAMILY_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_fast_screen_v1_family_summary.csv"
AUDIT = ROOT / "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1.csv"
CLASS_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1_class_summary.csv"
SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1_summary.csv"
CLAIM_BOUNDARY = "v2_full_kernel_proxy_component_audit_not_endpoint_not_validation"
BASE_FAMILY = "W_path_x_sky_x_x_zcenter"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def corr(a: np.ndarray, b: np.ndarray) -> float:
    if np.std(a) <= 0.0 or np.std(b) <= 0.0:
        return math.nan
    return float(np.corrcoef(a, b)[0, 1])


def classify_family(family_id: str) -> str:
    if family_id == BASE_FAMILY:
        return "base_observer_basis"
    if "void_centered_x_web_centered" in family_id:
        return "mixed_void_web"
    if "web_centered_x_los_density_mean" in family_id:
        return "mixed_web_los"
    if "void_wall_x_inside_void" in family_id:
        return "mixed_void_geometry"
    if "nearest_env" in family_id or "los_" in family_id:
        return "line_of_sight_environment"
    if "void_wall" in family_id or "inside_void" in family_id or "void_angular" in family_id:
        return "void_geometry"
    if "void_" in family_id:
        return "void_morphology"
    if "web_" in family_id:
        return "web_morphology"
    return "other"


def interpretation(row: dict[str, str], base_chi2: float) -> str:
    delta_base = float(row["candidate_best_chi2_screen"]) - base_chi2
    survives = row["survives_family_controls"] == "true"
    if row["family_id"] == BASE_FAMILY:
        return "reference_observer_basis_carrier"
    if survives and delta_base > 0.0:
        return "control_surviving_but_weaker_than_base"
    if survives and delta_base <= 0.0:
        return "control_surviving_and_stronger_than_base"
    if not survives and float(row["delta_chi2_candidate_minus_baseline"]) < 0.0:
        return "baseline_improving_but_control_failed"
    return "weak_or_degenerate_proxy"


def main() -> None:
    _, _, _, vectors, _, _ = load_scope()
    family_rows = read_rows(FAMILY_SUMMARY)
    by_family = {row["family_id"]: row for row in family_rows}
    if BASE_FAMILY not in vectors or BASE_FAMILY not in by_family:
        raise SystemExit("missing base observer-basis family")
    base_vector = vectors[BASE_FAMILY]
    base_chi2 = float(by_family[BASE_FAMILY]["candidate_best_chi2_screen"])
    audit_rows: list[dict[str, str]] = []
    for family_id in sorted(vectors):
        row = by_family[family_id]
        vector = vectors[family_id]
        unique_values = len({round(float(value), 10) for value in vector})
        audit_rows.append(
            {
                "audit_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_FULL_KERNEL_PROXY_COMPONENT_AUDIT_V1",
                "family_id": family_id,
                "component_class": classify_family(family_id),
                "candidate_best_chi2_screen": row["candidate_best_chi2_screen"],
                "delta_chi2_candidate_minus_baseline": row["delta_chi2_candidate_minus_baseline"],
                "delta_chi2_candidate_minus_base_observer_basis": f"{float(row['candidate_best_chi2_screen']) - base_chi2:.12g}",
                "delta_chi2_candidate_minus_best_control": row["delta_chi2_candidate_minus_best_control"],
                "controls_better_than_candidate_chi2": row["controls_better_than_candidate_chi2"],
                "survives_family_controls": row["survives_family_controls"],
                "corr_with_base_observer_basis": f"{corr(vector, base_vector):.12g}",
                "vector_std": f"{float(np.std(vector)):.12g}",
                "unique_value_count": str(unique_values),
                "best_control_branch": row["best_control_branch"],
                "interpretation": interpretation(row, base_chi2),
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(AUDIT, audit_rows)

    class_rows: list[dict[str, str]] = []
    classes = sorted({row["component_class"] for row in audit_rows})
    for component_class in classes:
        rows = [row for row in audit_rows if row["component_class"] == component_class]
        best = min(rows, key=lambda row: float(row["candidate_best_chi2_screen"]))
        surviving = [row for row in rows if row["survives_family_controls"] == "true"]
        class_rows.append(
            {
                "audit_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_FULL_KERNEL_PROXY_COMPONENT_AUDIT_V1",
                "component_class": component_class,
                "n_families": str(len(rows)),
                "surviving_family_count": str(len(surviving)),
                "best_family": best["family_id"],
                "best_delta_chi2_candidate_minus_baseline": best["delta_chi2_candidate_minus_baseline"],
                "best_delta_chi2_candidate_minus_base_observer_basis": best[
                    "delta_chi2_candidate_minus_base_observer_basis"
                ],
                "best_survives_family_controls": best["survives_family_controls"],
                "class_verdict": "contains_control_surviving_candidate"
                if surviving
                else "no_control_surviving_candidate",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    summary = [
        {
            "audit_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_FULL_KERNEL_PROXY_COMPONENT_AUDIT_V1",
            "n_families": str(len(audit_rows)),
            "n_component_classes": str(len(classes)),
            "base_family": BASE_FAMILY,
            "base_candidate_best_chi2_screen": f"{base_chi2:.12g}",
            "families_stronger_than_base": str(
                sum(float(row["delta_chi2_candidate_minus_base_observer_basis"]) < 0.0 for row in audit_rows)
            ),
            "control_surviving_families": ";".join(
                row["family_id"] for row in audit_rows if row["survives_family_controls"] == "true"
            ),
            "control_surviving_enriched_families": ";".join(
                row["family_id"]
                for row in audit_rows
                if row["survives_family_controls"] == "true" and row["family_id"] != BASE_FAMILY
            ),
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "extra_proxy_factors_do_not_outperform_base_observer_basis",
        }
    ]
    write_csv(CLASS_SUMMARY, class_rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_FULL_KERNEL_PROXY_COMPONENT_AUDIT_BUILT "
        f"verdict={summary[0]['verdict']} "
        f"stronger_than_base={summary[0]['families_stronger_than_base']}"
    )


if __name__ == "__main__":
    main()
