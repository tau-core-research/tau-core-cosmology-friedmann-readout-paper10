#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data/source_manifest/paper10_external_rd_prior_freeze_protocol_v1.csv"
TEMPLATE = ROOT / "data/derived/paper10_external_rd_prior_freeze_response_template_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_external_rd_prior_freeze_protocol_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_external_rd_prior_freeze_protocol_not_validation"

REQUIRED_FIELDS = {
    "prior_source_id",
    "rd_mpc",
    "sigma_rd_mpc",
    "assumption_family",
    "source_reference",
    "source_url_or_doi",
    "extraction_note",
    "hash_or_page_cache",
}

FORBIDDEN_MARKERS = {
    "Pantheon_distance_residuals",
    "fit_statistics",
    "endpoint_scores",
    "late_time_fit_parameters",
    "posthoc_prior_selection",
    "rd_fit_from_same_endpoint",
}


def read_rows(path: Path) -> list[dict[str, str]]:
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
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def split_semicolon(value: str) -> set[str]:
    return {part.strip() for part in value.split(";") if part.strip()}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    row = read_one(PROTOCOL)
    template_rows = read_rows(TEMPLATE)
    require(row["status"] == "SOURCE_SIDE_EXTERNAL_RD_PRIOR_PROTOCOL_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(row["route_id"] == "time_level_route", "bad route id")
    require(REQUIRED_FIELDS <= split_semicolon(row["required_fields"]), "required fields missing from protocol")
    require(FORBIDDEN_MARKERS <= split_semicolon(row["forbidden_inputs"]), "forbidden markers missing")
    require("prior_off_control" in row["required_controls"], "prior_off_control missing")
    require("wrong_prior_control" in row["required_controls"], "wrong_prior_control missing")
    require(row["endpoint_replay_allowed"] == "false", "endpoint replay must remain false")
    require(row["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
    require(row["physical_validation_claimed"] == "false", "physical validation must remain false")
    require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")
    require(len(template_rows) == 1, "template must contain exactly one blank response row")
    template_fields = set(template_rows[0])
    require(REQUIRED_FIELDS <= template_fields, "template missing required response fields")
    for marker in ["uses_pantheon_residuals", "uses_endpoint_scores", "uses_late_time_fit_parameters"]:
        require(marker in template_fields, f"template missing leakage marker {marker}")
        require(template_rows[0][marker] == "false", f"template default {marker} must be false")

    summary = {
        "protocol_id": row["protocol_id"],
        "status": "SOURCE_SIDE_EXTERNAL_RD_PRIOR_PROTOCOL_VALIDATED_NOT_REPLAY_NOT_VALIDATION",
        "route_id": row["route_id"],
        "accepted_prior_source_families": row["accepted_prior_source_families"],
        "required_fields_count": str(len(REQUIRED_FIELDS)),
        "template_ready": "true",
        "completed_response_present": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "external_rd_prior_protocol_ready_but_no_numeric_prior_frozen",
    }
    write_csv(SUMMARY, [summary])
    print(
        "PAPER10_EXTERNAL_RD_PRIOR_FREEZE_PROTOCOL_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
