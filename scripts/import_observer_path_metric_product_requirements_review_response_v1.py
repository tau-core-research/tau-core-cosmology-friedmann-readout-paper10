#!/usr/bin/env python3
from __future__ import annotations

import csv
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOWNLOAD_ZIP = (
    Path.home()
    / "Downloads/observer_path_metric_product_requirements_completed_review_response_v1.zip"
)
OUT_RESPONSE = ROOT / "data/derived/observer_path_metric_product_requirements_review_response_v1.csv"
OUT_COMPLETED_SUMMARY = (
    ROOT / "data/derived/observer_path_metric_product_requirements_review_completed_summary_v1.csv"
)
OUT_NOTES = ROOT / "docs/observer_path_metric_product_requirements_review_notes_v1.md"
OUT_LOG = ROOT / "data/derived/observer_path_metric_product_requirements_review_validation_log_v1.txt"
CLAIM_BOUNDARY = "observer_path_metric_product_requirements_not_endpoint_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def truthy_false(value: str) -> bool:
    return value.strip().lower() == "false"


def main() -> None:
    if not DOWNLOAD_ZIP.exists():
        raise SystemExit(f"missing completed reviewer zip: {DOWNLOAD_ZIP}")

    with zipfile.ZipFile(DOWNLOAD_ZIP) as zf:
        names = set(zf.namelist())
        expected = {
            "observer_path_metric_product_requirements_review_response_v1.csv",
            "observer_path_metric_product_requirements_review_completed_summary_v1.csv",
            "observer_path_metric_product_requirements_review_notes_v1.md",
            "observer_path_metric_product_requirements_review_validation_log_v1.txt",
        }
        if names != expected:
            raise SystemExit(f"unexpected zip contents: {sorted(names)}")
        tmp = ROOT / "data/derived/.observer_path_metric_product_requirements_review_tmp"
        if tmp.exists():
            shutil.rmtree(tmp)
        tmp.mkdir(parents=True)
        zf.extractall(tmp)

    response = tmp / "observer_path_metric_product_requirements_review_response_v1.csv"
    completed = tmp / "observer_path_metric_product_requirements_review_completed_summary_v1.csv"
    notes = tmp / "observer_path_metric_product_requirements_review_notes_v1.md"
    log = tmp / "observer_path_metric_product_requirements_review_validation_log_v1.txt"

    rows = read_rows(response)
    if len(rows) != 4:
        raise SystemExit("expected four reviewer response rows")
    for row in rows:
        if row["reviewer_response"] != "ACCEPT_REQUIREMENTS_ONLY":
            raise SystemExit(f"{row['question_id']} was not accepted requirements-only")
        if row["review_completed"].strip().lower() != "true":
            raise SystemExit(f"{row['question_id']} review not completed")
        for field in [
            "forbidden_inputs_used",
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "physical_lensing_path_weight_claimed",
        ]:
            if not truthy_false(row[field]):
                raise SystemExit(f"{row['question_id']} unsafe field {field}={row[field]}")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{row['question_id']} claim boundary mismatch")

    summary = read_one(completed)
    if summary["decision"] != "ACCEPT_REQUIREMENTS_ONLY":
        raise SystemExit("summary decision mismatch")
    if summary["accepted_requirements_only_rows"] != "4":
        raise SystemExit("summary accepted row count mismatch")
    if summary["source_aligned_metric_product_count"] != "0":
        raise SystemExit("summary should preserve zero metric product blocker")
    if summary["completion_check"] != "pass":
        raise SystemExit("summary completion check must pass")
    for field in [
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
        "physical_lensing_path_weight_claimed",
    ]:
        if not truthy_false(summary[field]):
            raise SystemExit(f"summary unsafe field {field}={summary[field]}")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")

    OUT_RESPONSE.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(response, OUT_RESPONSE)
    shutil.copyfile(completed, OUT_COMPLETED_SUMMARY)
    OUT_NOTES.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(notes, OUT_NOTES)
    shutil.copyfile(log, OUT_LOG)
    shutil.rmtree(tmp)
    print(
        "OBSERVER_PATH_METRIC_PRODUCT_REQUIREMENTS_REVIEW_RESPONSE_IMPORTED "
        "decision=ACCEPT_REQUIREMENTS_ONLY endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
