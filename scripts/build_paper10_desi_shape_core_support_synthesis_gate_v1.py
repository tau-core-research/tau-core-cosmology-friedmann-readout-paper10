#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_core_support_synthesis_gate_policy_v1.csv"
ROBUSTNESS = ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1_summary.csv"
ROBUSTNESS_GRID = ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1.csv"
ROW_SENSITIVITY = ROOT / "data/derived/paper10_desi_shape_row_sensitivity_source_audit_v1_summary.csv"
CORE_SCAN = ROOT / "data/derived/paper10_desi_shape_core_source_support_scan_v1_summary.csv"
ROW1_ATTACHMENT = ROOT / "data/derived/paper10_desi_shape_row1_confirmatory_source_attachment_v1_summary.csv"
ROW1_REVIEW_RESPONSE = ROOT / "data/derived/paper10_desi_shape_row1_confirmatory_source_review_response_v1_summary.csv"
ROW2_MORESCO = ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_v1_summary.csv"
ROW2_NATIVE_REVIEW = (
    ROOT / "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_response_v1_summary.csv"
)
ROW2_LEDGER = ROOT / "data/derived/paper10_desi_shape_row2_gate_status_ledger_v1_summary.csv"
ROW2_REPLAY = ROOT / "data/derived/paper10_desi_shape_row2_authorized_replay_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_shape_core_support_synthesis_gate_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_core_support_synthesis_gate_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_core_support_synthesis_gate_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_core_support_synthesis_gate_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def boolish(value: str) -> bool:
    return value.strip().lower() == "true"


def synthesis_row(component_id: str, status: str, artifact: Path, interpretation: str) -> dict[str, str]:
    return {
        "gate_id": "PAPER10_DESI_SHAPE_CORE_SUPPORT_SYNTHESIS_GATE_V1",
        "component_id": component_id,
        "status": status,
        "artifact": artifact.relative_to(ROOT).as_posix(),
        "claim_safe_interpretation": interpretation,
        "endpoint_replay_allowed_by_this_gate": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_doc(rows: list[dict[str, str]], summary: dict[str, str]) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    component_lines = [
        f"- `{row['component_id']}`: `{row['status']}` -- {row['claim_safe_interpretation']}"
        for row in rows
    ]
    DOC.write_text(
        "\n".join(
            [
                "# Paper10 DESI shape-core support synthesis gate v1",
                "",
                "**Doc class:** source-side synthesis gate",
                "**Reader role:** reviewer / reproducibility auditor",
                "**Status:** synthesis only; not replay authorization; not validation",
                "**Canonical parent:** Paper10 DESI shape-route replay chain",
                "",
                "This gate combines the already frozen DESI shape-route robustness",
                "stress, row-sensitivity audit, core source-support scan, Row2",
                "source-side reviews, and the isolated Row2 permission replay.",
                "It does not run new endpoint scoring and does not authorize new replay.",
                "",
                "Component status:",
                "",
                *component_lines,
                "",
                "Synthesis:",
                "",
                f"- status: `{summary['status']}`",
                f"- core rows: `{summary['core_rows']}`",
                f"- route interpretation: `{summary['route_interpretation']}`",
                f"- row 1 status: `{summary['row1_status']}`",
                f"- row 2 status: `{summary['row2_status']}`",
                f"- validation status: `{summary['validation_status']}`",
                f"- recommended next action: `{summary['recommended_next_action']}`",
                "",
                "Claim boundary:",
                "",
                "```text",
                CLAIM_BOUNDARY,
                "```",
                "",
            ]
        )
    )


def main() -> None:
    policy = read_one(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad policy claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    robustness = read_one(ROBUSTNESS)
    robustness_grid = read_rows(ROBUSTNESS_GRID)
    row_sensitivity = read_one(ROW_SENSITIVITY)
    core_scan = read_one(CORE_SCAN)
    row1_attachment = read_one(ROW1_ATTACHMENT)
    row1_review_response = read_one(ROW1_REVIEW_RESPONSE) if ROW1_REVIEW_RESPONSE.exists() else None
    row2_moresco = read_one(ROW2_MORESCO)
    row2_native = read_one(ROW2_NATIVE_REVIEW)
    row2_ledger = read_one(ROW2_LEDGER)
    row2_replay = read_one(ROW2_REPLAY)

    route_positive_narrow = (
        robustness["verdict"] == "positive_but_narrow_margin_and_row_sensitive_not_validation"
        and robustness["candidate_score_rank_among_replay_branches"] == "1"
    )
    core_rows = row_sensitivity["core_sensitive_rows"]
    row1_is_required = row_sensitivity["most_required_row"] == "1"
    row1_confirmatory_attached = (
        row1_attachment["status"] == "DESI_SHAPE_ROW1_CONFIRMATORY_SOURCE_ATTACHED_NOT_REPLAY_NOT_VALIDATION"
        and row1_attachment["row1_confirmatory_source_count"] == "2"
    )
    row1_review_accepted = (
        row1_review_response is not None
        and row1_review_response["status"]
        == "DESI_SHAPE_ROW1_CONFIRMATORY_SOURCE_REVIEW_ACCEPTED_NOT_REPLAY_NOT_VALIDATION"
        and row1_review_response["row1_confirmatory_source_accepted"] == "true"
    )
    row2_caveat_reduced = (
        boolish(row2_moresco["row2_source_caveat_reduced"])
        and boolish(row2_native["row2_source_caveat_reduced"])
        and row2_ledger["source_native_shape_caveat_reduced"] == "true"
    )
    row2_only_negative = (
        row2_replay["verdict"] == "row2_permission_replay_candidate_not_control_resistant_not_validation"
        and row2_replay["family_survives_row2_controls"] == "false"
    )
    row2_drop_rows = [row for row in robustness_grid if row["test_id"] == "drop_shape_row_2"]
    if len(row2_drop_rows) != 1:
        raise SystemExit("expected exactly one drop_shape_row_2 robustness row")
    row2_removed_retained_fraction = row2_drop_rows[0]["score_fraction_of_full_candidate"]

    rows = [
        synthesis_row(
            "ROUTE_WIDE_REPLAY",
            robustness["verdict"],
            ROBUSTNESS,
            "candidate ranks first under the frozen shape score, but the margin is narrow",
        ),
        synthesis_row(
            "ROW_SENSITIVITY",
            row_sensitivity["verdict"],
            ROW_SENSITIVITY,
            "middle shape rows 1 and 2 are the core-sensitive rows; row 1 is most required",
        ),
        synthesis_row(
            "CORE_SOURCE_SUPPORT_SCAN",
            core_scan["verdict"],
            CORE_SCAN,
            "frozen CC table supplies independent in-interval support for the row-2 core target",
        ),
        synthesis_row(
            "ROW1_CONFIRMATORY_SOURCE_ATTACHMENT",
            row1_review_response["verdict"] if row1_review_response else row1_attachment["verdict"],
            ROW1_REVIEW_RESPONSE if row1_review_response else ROW1_ATTACHMENT,
            "external review accepts Borghi2022 and Stern2010 as Row1 confirmatory support"
            if row1_review_accepted
            else "Borghi2022 and Stern2010 provide frozen independent in-interval confirmatory support for Row1",
        ),
        synthesis_row(
            "ROW2_CAVEAT_REDUCTION",
            row2_ledger["status"],
            ROW2_LEDGER,
            "Moresco2012 and source-native DESI shape context reduce the row-2 caveat without promotion",
        ),
        synthesis_row(
            "ROW2_ONLY_PERMISSION_REPLAY",
            row2_replay["verdict"],
            ROW2_REPLAY,
            "isolated Row2 replay is not control-resistant, so the route signal is not Row2-only",
        ),
    ]
    write_csv(OUT, rows)

    if (
        route_positive_narrow
        and row1_is_required
        and row1_confirmatory_attached
        and row1_review_accepted
        and row2_caveat_reduced
        and row2_only_negative
    ):
        status = "DESI_SHAPE_CORE_SUPPORT_SYNTHESIS_BUILT_SOURCE_STRENGTHENED_NOT_VALIDATION"
        route_interpretation = "multi_row_narrow_margin_source_sensitive_signal_not_row2_only"
        recommended_next_action = "seek_route_level_source_synthesis_review_before_any_validation_claim"
    else:
        status = "DESI_SHAPE_CORE_SUPPORT_SYNTHESIS_INCOMPLETE_NOT_VALIDATION"
        route_interpretation = "core_support_chain_incomplete"
        recommended_next_action = "resolve_missing_core_support_inputs_before_interpretation"

    summary = {
        "gate_id": "PAPER10_DESI_SHAPE_CORE_SUPPORT_SYNTHESIS_GATE_V1",
        "status": status,
        "component_count": str(len(rows)),
        "route_candidate_score": robustness["candidate_score"],
        "route_fractional_margin": robustness["candidate_minus_best_control_score_fraction"],
        "core_rows": core_rows,
        "most_required_row": row_sensitivity["most_required_row"],
        "row1_status": "most_required_confirmatory_independent_support_review_accepted_not_endpoint_ready"
        if row1_is_required and row1_confirmatory_attached and row1_review_accepted
        else "most_required_confirmatory_independent_support_attached_review_pending"
        if row1_is_required and row1_confirmatory_attached
        else "row1_not_current_most_required",
        "row2_status": "caveat_reduced_but_permission_replay_not_control_resistant_not_promotion_ready"
        if row2_caveat_reduced and row2_only_negative
        else "row2_status_incomplete",
        "row2_removed_retained_fraction": row2_removed_retained_fraction,
        "row2_only_candidate_score": row2_replay["candidate_shape_quadratic_score"],
        "row2_only_best_control_score": row2_replay["best_control_shape_quadratic_score"],
        "route_interpretation": route_interpretation,
        "validation_status": "not_endpoint_validation_not_physical_validation_not_falsification",
        "endpoint_replay_allowed_by_this_gate": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "shape_core_support_strengthened_but_route_remains_narrow_margin_source_sensitive_not_validation"
        if status.endswith("SOURCE_STRENGTHENED_NOT_VALIDATION")
        else "shape_core_support_synthesis_incomplete_not_validation",
        "recommended_next_action": recommended_next_action,
    }
    write_csv(SUMMARY, [summary])
    write_doc(rows, summary)
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"wrote {SUMMARY.relative_to(ROOT)}")
    print(f"wrote {DOC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
