#!/usr/bin/env python3
from __future__ import annotations

import csv
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "data/derived/joint_numeric_zi_distribution_build_authorization_response_v1_summary.csv"
PROTOCOL = ROOT / "data/derived/joint_signed_zi_standardization_protocol_v1.csv"
READINESS = ROOT / "data/derived/joint_matched_control_distribution_readiness_v1.csv"
OUT = ROOT / "data/derived/joint_numeric_zi_distribution_ledger_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_zi_distribution_ledger_v1.md"
CLAIM_BOUNDARY = "joint_numeric_zi_distribution_ledger_not_tjoint_not_scoring_not_validation"


CHANNEL_SOURCES = {
    "kids_lensing_cosebis_low_mode": {
        "candidate_source": "data/derived/kids1000_cosebis_endpoint_scoring_v1_summary.csv",
        "candidate_field": "candidate_delta_chi2_vs_baseline",
        "control_source": "data/derived/kids1000_cosebis_endpoint_scoring_v1_null_controls.csv",
        "control_field": "delta_chi2_vs_baseline",
        "control_selector": "kids_null_controls",
        "native_value_definition": "delta_chi2_vs_baseline",
        "caveat": "endpoint-score-not-validation",
    },
    "observer_path_basis_low_z": {
        "candidate_source": "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv",
        "candidate_field": "delta_chi2_candidate_minus_best_control",
        "control_source": "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_grid.csv",
        "control_field": "chi2_observer_basis_replay",
        "control_selector": "non_candidate_non_baseline_branches_relative_to_best_control",
        "native_value_definition": "chi2_control_minus_best_control_chi2",
        "caveat": "permission-only-not-validation",
    },
    "desi_shape_time_readout": {
        "candidate_source": "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv",
        "candidate_field": "delta_candidate_minus_best_control_score",
        "control_source": "data/derived/paper10_desi_shape_route_authorized_replay_v1_grid.csv",
        "control_field": "shape_quadratic_score",
        "control_selector": "non_candidate_controls_relative_to_best_control",
        "native_value_definition": "control_shape_score_minus_best_control_shape_score",
        "caveat": "small-N-permission-only-not-validation",
    },
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
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
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def f(value: str) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise SystemExit(f"non-numeric value: {value}") from exc


def fmt(value: float) -> str:
    return f"{value:.12e}"


def median(values: list[float]) -> float:
    if not values:
        raise SystemExit("cannot compute median of empty distribution")
    return float(statistics.median(values))


def mad1p4826(values: list[float], center: float) -> float:
    deviations = [abs(value - center) for value in values]
    return 1.4826 * float(statistics.median(deviations))


def signed(value: float, sign_text: str) -> float:
    if sign_text == "+1":
        return value
    if sign_text == "-1":
        return -value
    raise SystemExit(f"unsupported support_positive_sign: {sign_text}")


def control_values(channel_id: str, spec: dict[str, str]) -> list[tuple[str, float]]:
    rows = read_rows(ROOT / spec["control_source"])
    if channel_id == "kids_lensing_cosebis_low_mode":
        controls = [
            (f"control_{row['control_index_one_based']}", f(row[spec["control_field"]]))
            for row in rows
            if row.get("control_family") or row.get("operator")
        ]
    elif channel_id == "observer_path_basis_low_z":
        control_rows = [row for row in rows if row["branch"] not in {"candidate", "baseline_only"}]
        best = min(f(row[spec["control_field"]]) for row in control_rows)
        controls = [
            (f"control_{idx + 1}_{row['branch']}", f(row[spec["control_field"]]) - best)
            for idx, row in enumerate(control_rows)
        ]
    elif channel_id == "desi_shape_time_readout":
        control_rows = [row for row in rows if row["control_family"] != "candidate"]
        best = max(f(row[spec["control_field"]]) for row in control_rows)
        controls = [
            (f"control_{idx + 1}_{row['control_family']}", f(row[spec["control_field"]]) - best)
            for idx, row in enumerate(control_rows)
        ]
    else:
        raise SystemExit(f"unknown channel: {channel_id}")
    if len(controls) < 2:
        raise SystemExit(f"{channel_id}: at least two matched controls are required")
    return controls


def main() -> None:
    auth = read_one(AUTH)
    if auth["numeric_zi_build_allowed"] != "true":
        raise SystemExit("numeric z_i distribution build is not authorized")
    for field in [
        "numeric_t_joint_allowed",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        if auth[field] != "false":
            raise SystemExit(f"unsafe authorization field: {field}")

    protocol_rows = read_rows(PROTOCOL)
    readiness_rows = {row["channel_id"]: row for row in read_rows(READINESS)}
    ledger_rows: list[dict[str, str]] = []
    summary_rows: list[dict[str, str]] = []
    blocked_channels = 0

    for protocol in protocol_rows:
        channel_id = protocol["channel_id"]
        spec = CHANNEL_SOURCES[channel_id]
        candidate = read_one(ROOT / spec["candidate_source"])
        candidate_native = f(candidate[spec["candidate_field"]])
        sign_text = protocol["support_positive_sign"]
        controls_native = control_values(channel_id, spec)
        controls_signed = [signed(value, sign_text) for _, value in controls_native]
        center = median(controls_signed)
        scale = mad1p4826(controls_signed, center)
        scale_status = "ok" if scale > 0 else "blocked_zero_or_unavailable_scale"
        if scale <= 0:
            blocked_channels += 1
        candidate_e = signed(candidate_native, sign_text)
        candidate_z = (candidate_e - center) / scale if scale > 0 else float("nan")

        for idx, (control_id, native_value) in enumerate(controls_native, start=1):
            e_value = signed(native_value, sign_text)
            z_value = (e_value - center) / scale if scale > 0 else float("nan")
            ledger_rows.append(
                {
                    "ledger_id": "JOINT_NUMERIC_ZI_DISTRIBUTION_LEDGER_V1",
                    "channel_order": protocol["channel_order"],
                    "channel_id": channel_id,
                    "row_type": "matched_control",
                    "row_id": control_id,
                    "control_index": str(idx),
                    "native_value": fmt(native_value),
                    "support_positive_sign": sign_text,
                    "signed_evidence_value": fmt(e_value),
                    "center_i": fmt(center),
                    "scale_i_mad1p4826": fmt(scale),
                    "z_i": fmt(z_value) if scale > 0 else "nan",
                    "native_value_definition": spec["native_value_definition"],
                    "source_artifact": spec["control_source"],
                    "caveat": spec["caveat"],
                    "computes_t_joint_now": "false",
                    "endpoint_scoring_allowed": "false",
                    "endpoint_validation_claimed": "false",
                    "cosmological_validation_claimed": "false",
                    "physical_validation_claimed": "false",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        ledger_rows.append(
            {
                "ledger_id": "JOINT_NUMERIC_ZI_DISTRIBUTION_LEDGER_V1",
                "channel_order": protocol["channel_order"],
                "channel_id": channel_id,
                "row_type": "candidate",
                "row_id": "candidate",
                "control_index": "not_applicable",
                "native_value": fmt(candidate_native),
                "support_positive_sign": sign_text,
                "signed_evidence_value": fmt(candidate_e),
                "center_i": fmt(center),
                "scale_i_mad1p4826": fmt(scale),
                "z_i": fmt(candidate_z) if scale > 0 else "nan",
                "native_value_definition": spec["candidate_field"],
                "source_artifact": spec["candidate_source"],
                "caveat": spec["caveat"],
                "computes_t_joint_now": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        summary_rows.append(
            {
                "ledger_id": "JOINT_NUMERIC_ZI_DISTRIBUTION_LEDGER_V1",
                "channel_order": protocol["channel_order"],
                "channel_id": channel_id,
                "matched_control_count": str(len(controls_native)),
                "readiness_status": readiness_rows[channel_id]["readiness_status"],
                "center_rule": protocol["center_rule"],
                "scale_rule": protocol["scale_rule"],
                "center_i": fmt(center),
                "scale_i_mad1p4826": fmt(scale),
                "scale_status": scale_status,
                "candidate_native_value": fmt(candidate_native),
                "candidate_signed_evidence_value": fmt(candidate_e),
                "candidate_z_i": fmt(candidate_z) if scale > 0 else "nan",
                "numeric_z_i_defined": "true" if scale > 0 else "false",
                "control_source_artifact": spec["control_source"],
                "candidate_source_artifact": spec["candidate_source"],
                "caveat": spec["caveat"],
                "computes_t_joint_now": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    aggregate = {
        "ledger_id": "JOINT_NUMERIC_ZI_DISTRIBUTION_LEDGER_V1_SUMMARY",
        "channel_order": "all",
        "channel_id": "all_channels",
        "matched_control_count": str(sum(int(row["matched_control_count"]) for row in summary_rows)),
        "readiness_status": "mixed_ready_and_caveated_ready",
        "center_rule": "median_of_matched_controls_only",
        "scale_rule": "MAD1p4826_of_matched_controls_only_else_declared_blocker",
        "center_i": "per_channel",
        "scale_i_mad1p4826": "per_channel",
        "scale_status": "ok" if blocked_channels == 0 else "blocked_zero_or_unavailable_scale",
        "candidate_native_value": "per_channel",
        "candidate_signed_evidence_value": "per_channel",
        "candidate_z_i": "per_channel_not_summed",
        "numeric_z_i_defined": str(blocked_channels == 0).lower(),
        "control_source_artifact": "per_channel",
        "candidate_source_artifact": "per_channel",
        "caveat": "channel_level_distribution_ledger_only_not_joint_statistic",
        "computes_t_joint_now": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, ledger_rows)
    write_csv(SUMMARY, summary_rows + [aggregate])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric z_i distribution ledger v1",
                "",
                "**Doc class:** numeric channel-level distribution ledger",
                "**Status:** z_i distribution built; not T_joint; not scoring; not validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This artifact applies the frozen signed median/MAD rule to each active",
                "channel independently. Centers and scales are computed only from matched",
                "controls. Candidate values do not define center or scale.",
                "",
                "The output is a channel-level `z_i` ledger only. It does not compute",
                "`T_joint`, endpoint scores, cosmological validation, or physical",
                "validation.",
                "",
                "Channel-level candidate `z_i` values are recorded in:",
                "",
                "- `data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv`",
                "- `data/derived/joint_numeric_zi_distribution_ledger_v1.csv`",
                "",
            ]
        )
    )
    print(
        "JOINT_NUMERIC_ZI_DISTRIBUTION_LEDGER_V1_BUILT "
        f"channels={len(summary_rows)} blocked_channels={blocked_channels}"
    )


if __name__ == "__main__":
    main()
