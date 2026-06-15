#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import shutil
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
CANONICAL_RESPONSE = DERIVED / "joint_row_level_penalized_t_joint_endpoint_authorization_review_response_v1.csv"
CANONICAL_SUMMARY = DERIVED / "joint_row_level_penalized_t_joint_endpoint_authorization_review_completed_summary_v1.csv"
CANONICAL_NOTES = DERIVED / "joint_row_level_penalized_t_joint_endpoint_authorization_review_notes_v1.md"
CANONICAL_LOG = DERIVED / "joint_row_level_penalized_t_joint_endpoint_authorization_review_validation_log_v1.txt"

EXPECTED_FILES = {
    "joint_row_level_penalized_t_joint_endpoint_authorization_review_response_v1.csv": CANONICAL_RESPONSE,
    "joint_row_level_penalized_t_joint_endpoint_authorization_review_completed_summary_v1.csv": CANONICAL_SUMMARY,
    "joint_row_level_penalized_t_joint_endpoint_authorization_review_notes_v1.md": CANONICAL_NOTES,
    "joint_row_level_penalized_t_joint_endpoint_authorization_review_validation_log_v1.txt": CANONICAL_LOG,
}


def read_one_csv(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise SystemExit(f"Expected exactly one row in {path}, got {len(rows)}")
    return rows[0]


def read_rows_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate_extracted(tmp: Path) -> None:
    summary = read_one_csv(tmp / "joint_row_level_penalized_t_joint_endpoint_authorization_review_completed_summary_v1.csv")
    response = read_rows_csv(tmp / "joint_row_level_penalized_t_joint_endpoint_authorization_review_response_v1.csv")
    log_text = (tmp / "joint_row_level_penalized_t_joint_endpoint_authorization_review_validation_log_v1.txt").read_text(
        encoding="utf-8"
    )

    require(len(response) == 4, "Completed response must contain four question rows.")
    require(summary.get("question_count") == "4", "Summary question count must be 4.")
    require(summary.get("completed_response_rows") == "4", "Summary completed response rows must be 4.")
    require(summary.get("accepted_rows") == "4", "All four rows must be accepted.")
    require(summary.get("penalized_t_joint_ledger_authorized") == "true", "Penalized ledger is not authorized.")
    require(
        summary.get("guarded_endpoint_scoring_replay_authorized") == "true",
        "Guarded endpoint replay is not authorized.",
    )
    require(summary.get("endpoint_scoring_run_by_this_review") == "false", "Review itself must not run scoring.")
    for key in [
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
        "forbidden_inputs_used",
    ]:
        require(summary.get(key) == "false", f"Unsafe summary flag {key}.")
    require(
        summary.get("decision")
        == "AUTHORIZE_PENALIZED_T_JOINT_LEDGER_AND_ONE_GUARDED_ENDPOINT_SCORING_REPLAY_NOT_VALIDATION",
        "Unexpected reviewer decision.",
    )
    require("completion_check=pass" in log_text, "Validation log does not show completion pass.")
    require("forbidden_inputs_used=false" in log_text or summary.get("forbidden_inputs_used") == "false", "Forbidden input check missing.")

    for row in response:
        require(row.get("review_id") == "joint_row_level_penalized_t_joint_endpoint_authorization_review_package_v1", "Bad review_id.")
        require(row.get("response", "").strip().lower() in {"accept", "yes"}, "Unexpected response value.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Import completed consolidated row-level endpoint authorization review.")
    parser.add_argument("zip_path")
    args = parser.parse_args()
    source = Path(args.zip_path).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"Missing zip: {source}")

    with tempfile.TemporaryDirectory(prefix="penalized_endpoint_auth_import_") as tmp_text:
        tmp = Path(tmp_text)
        with zipfile.ZipFile(source, "r") as archive:
            archive.extractall(tmp)
        for name in EXPECTED_FILES:
            require((tmp / name).exists(), f"Missing required response file in zip: {name}")
        validate_extracted(tmp)
        DERIVED.mkdir(parents=True, exist_ok=True)
        for name, target in EXPECTED_FILES.items():
            shutil.copy2(tmp / name, target)

    print(
        "JOINT_ROW_LEVEL_PENALIZED_T_JOINT_ENDPOINT_AUTHORIZATION_RESPONSE_IMPORTED "
        f"summary={CANONICAL_SUMMARY.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
