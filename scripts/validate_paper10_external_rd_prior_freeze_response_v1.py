#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_SUMMARY = ROOT / "data/derived/paper10_external_rd_prior_freeze_protocol_v1_summary.csv"
RESPONSE = ROOT / "data/derived/paper10_external_rd_prior_freeze_response_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_external_rd_prior_freeze_response_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_external_rd_prior_freeze_response_not_validation"


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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    protocol = read_one(PROTOCOL_SUMMARY)
    row = read_one(RESPONSE)
    require(protocol["verdict"] == "external_rd_prior_protocol_ready_but_no_numeric_prior_frozen", "protocol not ready")
    require(row["prior_source_id"] == "Planck2018_base_LCDM_TTTEEE_lowE_lensing_rdrag", "unexpected prior source")
    require(row["assumption_family"] == "Planck2018_base_LCDM_TTTEEE_lowE_lensing", "bad assumption family")
    rd = float(row["rd_mpc"])
    sigma = float(row["sigma_rd_mpc"])
    require(140.0 < rd < 155.0, "rd value out of broad physical range")
    require(0.0 < sigma < 2.0, "rd uncertainty out of expected source-prior range")
    require("Planck2018Cosmology" in row["source_reference"], "source reference must cite Planck2018Cosmology")
    require("10.1051/0004-6361/201833910" in row["source_url_or_doi"], "Planck DOI missing")
    require("Table 2" in row["extraction_note"], "extraction note must identify table")
    require("rdrag" in row["extraction_note"], "extraction note must identify rdrag")
    require(row["uses_pantheon_residuals"] == "false", "Pantheon residual leakage forbidden")
    require(row["uses_endpoint_scores"] == "false", "endpoint score leakage forbidden")
    require(row["uses_late_time_fit_parameters"] == "false", "late-time fit leakage forbidden")
    require(row["reviewer_verdict"] == "ACCEPT_AS_CAVEATED_EXTERNAL_RD_PRIOR_SOURCE_FREEZE", "bad reviewer verdict")

    summary = {
        "prior_source_id": row["prior_source_id"],
        "status": "SOURCE_SIDE_EXTERNAL_RD_PRIOR_FROZEN_NOT_REPLAY_NOT_VALIDATION",
        "rd_mpc": row["rd_mpc"],
        "sigma_rd_mpc": row["sigma_rd_mpc"],
        "assumption_family": row["assumption_family"],
        "source_reference": row["source_reference"],
        "uses_pantheon_residuals": "false",
        "uses_endpoint_scores": "false",
        "uses_late_time_fit_parameters": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "planck2018_rd_prior_frozen_as_caveated_external_source_not_endpoint",
    }
    write_csv(SUMMARY, [summary])
    print(
        "PAPER10_EXTERNAL_RD_PRIOR_FREEZE_RESPONSE_VALIDATED "
        f"rd={summary['rd_mpc']} sigma={summary['sigma_rd_mpc']} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
