#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mode_response_spectrum_attempt_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_spectrum_attempt_v1.csv"
SPECTRA = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_spectrum_attempt_v1_spectra.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_spectrum_attempt_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    ledger = read_rows(LEDGER)
    spectra = read_rows(SPECTRA)
    summary = read_one(SUMMARY)
    if policy["status"] != "MODE_RESPONSE_SPECTRUM_ATTEMPT_POLICY_FROZEN":
        raise SystemExit("unexpected spectrum attempt policy status")
    if summary["status"] != "MODE_RESPONSE_SPECTRUM_ATTEMPT_CONDITIONAL_COMPLETE":
        raise SystemExit("unexpected spectrum attempt summary status")
    if summary["spectrum_attempt_verdict"] != "conditional_source_spectrum_attempt_preserves_operator_and_null_safety_blockers":
        raise SystemExit("unexpected spectrum attempt verdict")
    if summary["mode_response_operator_derived"] != "false":
        raise SystemExit("spectrum attempt must not derive the mode-response operator")
    if summary["open_blocker_count"] != "2":
        raise SystemExit("expected two open blockers")
    if summary["conditional_primary_spectrum"] != "log_band_neutral_candidate":
        raise SystemExit("unexpected conditional primary spectrum")
    if len(ledger) != 7 or summary["ledger_rows"] != "7":
        raise SystemExit("ledger row count mismatch")
    if len(spectra) != 80:
        raise SystemExit("expected 4 spectra over 20 modes")
    by_step = {row["step_id"]: row for row in ledger}
    if by_step["S2_log_band_power_prior"]["status"] != "ASSUMPTION_NOT_SOURCE_PROVEN":
        raise SystemExit("log-band power prior must remain an unproven assumption")
    if by_step["B1_operator_spectrum_blocker"]["status"] != "OPEN_BLOCKER":
        raise SystemExit("operator spectrum blocker must remain open")
    if by_step["B2_gauge_null_safety_blocker"]["status"] != "OPEN_BLOCKER":
        raise SystemExit("gauge/null safety blocker must remain open")
    statuses = {row["spectrum_family"]: row["source_status"] for row in spectra if row["mode"] == "1"}
    if statuses["log_band_neutral_candidate"] != "CONDITIONAL_PRIMARY":
        raise SystemExit("log-band spectrum must be the conditional primary")
    if statuses["flat_boundary_control"] != "BOUNDARY_CONTROL":
        raise SystemExit("flat spectrum must remain a boundary control")
    if statuses["high_mode_rejected_under_smooth_path_prior"] != "REJECTED_BY_SMOOTH_PATH_PRIOR":
        raise SystemExit("high-mode spectrum should be rejected under smooth path prior")
    if statuses["oscillatory_rejected_under_smooth_path_prior"] != "REJECTED_BY_SMOOTH_PATH_PRIOR":
        raise SystemExit("oscillatory spectrum should be rejected under smooth path prior")
    by_family: dict[str, list[float]] = {}
    for row in spectra:
        by_family.setdefault(row["spectrum_family"], []).append(float(row["unit_mean_weight"]))
        for key in [
            "uses_kids_data_vector_values",
            "uses_fit_statistics",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"spectrum row {key} must be false")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("spectrum claim boundary mismatch")
    for family, values in by_family.items():
        mean = math.fsum(values) / len(values)
        if family != "oscillatory_rejected_under_smooth_path_prior" and not math.isclose(mean, 1.0, rel_tol=0.0, abs_tol=1e-12):
            raise SystemExit(f"{family} is not unit-mean normalized")
    for row in ledger:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("ledger claim boundary mismatch")
        if not row["dimension_check"] or not row["limit_check"]:
            raise SystemExit("ledger rows must include dimension and limit checks")
    for key in [
        "uses_kids_data_vector_values",
        "uses_fit_statistics",
        "uses_random_noise",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary {key} must be false")
    print(
        "PAPER10_KIDS1000_COSEBIS_MODE_RESPONSE_SPECTRUM_ATTEMPT_V1_VALIDATED "
        f"verdict={summary['spectrum_attempt_verdict']}"
    )


if __name__ == "__main__":
    main()
