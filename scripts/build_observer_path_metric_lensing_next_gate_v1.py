#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACQUISITION = ROOT / "data/derived/observer_path_metric_product_acquisition_status_v1_summary.csv"
METRIC_SCREEN = ROOT / "data/derived/observer_path_metric_environment_fast_screen_v1_summary.csv"
ORDERING_SCREEN = ROOT / "data/derived/observer_path_source_native_ordering_fast_screen_v1_summary.csv"
ACT_SAMPLING = ROOT / "data" / "derived" / "act_dr6_lensing_low_z_sampling_pilot_v1_summary.csv"
ACT_CANDIDATE = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_candidate_v1_summary.csv"
OUT = ROOT / "data/derived/observer_path_metric_lensing_next_gate_v1.csv"
SUMMARY = ROOT / "data/derived/observer_path_metric_lensing_next_gate_v1_summary.csv"
DOC = ROOT / "docs/observer_path_metric_lensing_next_gate_v1.md"
CLAIM_BOUNDARY = "observer_path_metric_lensing_next_gate_not_endpoint_not_validation"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {path.relative_to(ROOT)}")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_str(value: bool) -> str:
    return str(value).lower()


def main() -> None:
    acquisition = read_one(ACQUISITION)
    metric = read_one(METRIC_SCREEN)
    ordering = read_one(ORDERING_SCREEN)
    act_sampling = read_one(ACT_SAMPLING)
    act_candidate = read_one(ACT_CANDIDATE)

    caveated_count = int(acquisition["caveated_metric_environment_product_count"])
    physical_count = int(acquisition["physical_kappa_shear_mass_map_product_count"])
    metric_survives = metric["best_candidate_survives_controls"] == "true"
    ordering_survives = ordering["best_candidate_survives_controls"] == "true"
    has_caveated_proxy = caveated_count == 12
    has_physical_path = physical_count == 12
    has_act_sampling = act_sampling["status"] == "SOURCE_SIDE_SAMPLING_PILOT_BUILT_NOT_ENDPOINT"
    has_act_candidate = act_candidate["status"] == "SOURCE_SIDE_PATH_WEIGHT_CANDIDATE_BUILT_NOT_ENDPOINT"
    act_mask_positive = int(act_sampling["mask_positive_count"])
    act_rows = int(act_sampling["source_rows"])

    rows = [
        {
            "gate_id": "OBSERVER_PATH_METRIC_LENSING_NEXT_GATE_V1",
            "gate_item": "caveated_metric_environment_proxy_available",
            "status": "pass" if has_caveated_proxy else "fail",
            "evidence": f"{caveated_count}/12 active rows have caveated metric-environment proxy",
            "required_for_endpoint": "necessary_but_not_sufficient",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "OBSERVER_PATH_METRIC_LENSING_NEXT_GATE_V1",
            "gate_item": "act_dr6_source_side_kappa_sampling_available",
            "status": "pass" if has_act_sampling and act_mask_positive > 0 else "blocked",
            "evidence": (
                f"{act_mask_positive}/{act_rows} low-z rows are ACT baseline mask-positive; "
                f"variants={act_sampling['variants_sampled']}"
            ),
            "required_for_endpoint": "necessary_but_not_sufficient",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "OBSERVER_PATH_METRIC_LENSING_NEXT_GATE_V1",
            "gate_item": "physical_metric_lensing_path_product_available",
            "status": "pass" if has_physical_path else "blocked",
            "evidence": f"{physical_count}/12 active rows have kappa/shear/mass-map/path-metric product",
            "required_for_endpoint": "required_for_physical_path_claim",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "OBSERVER_PATH_METRIC_LENSING_NEXT_GATE_V1",
            "gate_item": "act_dr6_source_frozen_path_weight_candidate_available",
            "status": "pass" if has_act_candidate else "blocked",
            "evidence": (
                "candidate=true; "
                f"mask_positive_rows={act_candidate['mask_positive_rows']}; "
                f"corr_baseline_curl={act_candidate['corr_baseline_curl_active']}; "
                f"corr_baseline_diff={act_candidate['corr_baseline_diff_f150_f090_active']}"
            ),
            "required_for_endpoint": "necessary_but_not_sufficient",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "OBSERVER_PATH_METRIC_LENSING_NEXT_GATE_V1",
            "gate_item": "metric_environment_screen_control_resistant",
            "status": "pass" if metric_survives else "fail",
            "evidence": (
                "delta_chi2_candidate_minus_best_control="
                f"{metric['best_candidate_delta_chi2_minus_best_control']}"
            ),
            "required_for_endpoint": "required_for_replay_promotion",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "OBSERVER_PATH_METRIC_LENSING_NEXT_GATE_V1",
            "gate_item": "source_native_ordering_screen_control_resistant",
            "status": "pass" if ordering_survives else "fail",
            "evidence": (
                "delta_chi2_candidate_minus_best_control="
                f"{ordering['best_candidate_delta_chi2_minus_best_control']}"
            ),
            "required_for_endpoint": "required_for_replay_promotion",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, rows)

    replay_allowed = has_physical_path and (metric_survives or ordering_survives)
    if replay_allowed:
        verdict = "OBSERVER_PATH_METRIC_LENSING_ROUTE_READY_FOR_REVIEWED_REPLAY"
    elif has_act_candidate and not has_physical_path:
        verdict = "ACT_DR6_PATH_WEIGHT_CANDIDATE_READY_BUT_REVIEW_BLOCKS_REPLAY"
    elif has_act_sampling and not has_physical_path:
        verdict = "ACT_DR6_SAMPLING_READY_BUT_PATH_WEIGHT_DERIVATION_BLOCKS_REPLAY"
    elif not has_physical_path:
        verdict = "PHYSICAL_METRIC_LENSING_PRODUCT_BLOCKS_OBSERVER_PATH_REPLAY"
    else:
        verdict = "CONTROL_RESISTANCE_BLOCKS_OBSERVER_PATH_REPLAY"

    summary = {
        "gate_id": "OBSERVER_PATH_METRIC_LENSING_NEXT_GATE_V1",
        "caveated_metric_environment_proxy_available": bool_str(has_caveated_proxy),
        "act_dr6_source_side_kappa_sampling_available": bool_str(has_act_sampling),
        "act_dr6_source_frozen_path_weight_candidate_available": bool_str(has_act_candidate),
        "act_dr6_low_z_source_rows": str(act_rows),
        "act_dr6_mask_positive_rows": str(act_mask_positive),
        "act_dr6_corr_baseline_curl_active": act_candidate["corr_baseline_curl_active"],
        "act_dr6_corr_baseline_diff_f150_f090_active": act_candidate["corr_baseline_diff_f150_f090_active"],
        "physical_metric_lensing_path_product_available": bool_str(has_physical_path),
        "metric_environment_screen_survives_controls": bool_str(metric_survives),
        "source_native_ordering_screen_survives_controls": bool_str(ordering_survives),
        "endpoint_replay_allowed": bool_str(replay_allowed),
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": bool_str(has_physical_path and replay_allowed),
        "next_required_action": (
            "external_review_and_replay_authorization_for_act_path_weight_candidate"
            if has_act_candidate and not has_physical_path
            else "derive_source_frozen_metric_lensing_path_weight_from_act_sampling"
            if has_act_sampling and not has_physical_path
            else (
                "acquire_source_aligned_kappa_shear_mass_map_or_metric_path_product"
                if not has_physical_path
                else "derive_control_resistant_source_native_ordering_rule"
            )
        ),
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": verdict,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# Observer/path metric-lensing next gate v1",
                "",
                "**Doc class:** next-action gate",
                "**Status:** not endpoint replay; not validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This gate prevents the observer/path route from turning a weak",
                "metric-environment proxy into an endpoint claim. It combines the",
                "acquisition status, the metric-environment fast screen, and the",
                "source-native ordering-bank screen.",
                "",
                "Summary:",
                "",
                f"- caveated proxy available: `{summary['caveated_metric_environment_proxy_available']}`",
                f"- ACT DR6 source-side kappa sampling available: `{summary['act_dr6_source_side_kappa_sampling_available']}`",
                f"- ACT DR6 source-frozen path-weight candidate available: `{summary['act_dr6_source_frozen_path_weight_candidate_available']}`",
                f"- ACT DR6 mask-positive rows: `{summary['act_dr6_mask_positive_rows']}/{summary['act_dr6_low_z_source_rows']}`",
                f"- physical metric/lensing path product available: `{summary['physical_metric_lensing_path_product_available']}`",
                f"- metric-environment screen survives controls: `{summary['metric_environment_screen_survives_controls']}`",
                f"- source-native ordering screen survives controls: `{summary['source_native_ordering_screen_survives_controls']}`",
                f"- endpoint replay allowed: `{summary['endpoint_replay_allowed']}`",
                f"- next required action: `{summary['next_required_action']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: the current quick products are useful diagnostics",
                "but do not authorize replay. The focused next step is external",
                "review and replay authorization for the ACT path-weight candidate,",
                "including explicit null-control handling, before any endpoint scoring.",
                "",
            ]
        )
    )
    print(
        "OBSERVER_PATH_METRIC_LENSING_NEXT_GATE_V1_BUILT "
        f"verdict={verdict} next={summary['next_required_action']}"
    )


if __name__ == "__main__":
    main()
