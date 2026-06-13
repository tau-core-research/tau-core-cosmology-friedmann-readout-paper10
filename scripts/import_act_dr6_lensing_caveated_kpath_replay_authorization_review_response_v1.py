#!/usr/bin/env python3
"""Import a completed ACT caveated K_path replay-authorization response.

This importer accepts either a completed CSV or a ZIP containing the completed
CSV.  It does not authorize scoring by itself; the paired validator determines
whether the response allows a later guarded replay package.
"""

from __future__ import annotations

import csv
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DEFAULT_INPUT = (
    Path.home()
    / "Downloads"
    / "act_dr6_lensing_caveated_kpath_replay_authorization_completed_review_response_v1.zip"
)
RESPONSE_NAME = "act_dr6_lensing_caveated_kpath_replay_authorization_review_response_v1.csv"
OUT_RESPONSE = DERIVED / RESPONSE_NAME
OUT_SUMMARY = DERIVED / "act_dr6_lensing_caveated_kpath_replay_authorization_review_response_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def is_false(value: str) -> bool:
    return value.strip().lower() in {"false", "0", "no", "n"}


def find_response_file(input_path: Path) -> Path:
    if input_path.suffix.lower() == ".csv":
        return input_path
    if input_path.suffix.lower() != ".zip":
        raise SystemExit("input must be a completed response CSV or ZIP")
    tmpdir = tempfile.TemporaryDirectory()
    tmp = Path(tmpdir.name)
    with zipfile.ZipFile(input_path) as zf:
        zf.extractall(tmp)
    candidates = list(tmp.rglob(RESPONSE_NAME))
    if len(candidates) != 1:
        tmpdir.cleanup()
        raise SystemExit(f"expected exactly one {RESPONSE_NAME} in ZIP, found {len(candidates)}")
    # Keep the tempdir alive by attaching it to the path object via a module global.
    globals()["_TMPDIR_KEEPALIVE"] = tmpdir
    return candidates[0]


def main() -> None:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    if not input_path.exists():
        raise SystemExit(f"missing completed review response: {input_path}")
    response_path = find_response_file(input_path)
    rows = read_rows(response_path)
    if len(rows) != 5:
        raise SystemExit(f"expected five completed response rows, found {len(rows)}")

    DERIVED.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(response_path, OUT_RESPONSE)

    answers = {row["question_id"]: row.get("reviewer_answer", "") for row in rows}
    q5 = answers.get("Q5_permission_only_replay", "")
    replay_package_preparation_allowed = q5 == "authorize_permission_only_replay_package"
    forbidden_inputs_used = any(not is_false(row.get("forbidden_inputs_used", "")) for row in rows)
    completed = all(row.get("reviewer_answer", "") for row in rows)

    summary = {
        "artifact_id": "ACT_DR6_LENSING_CAVEATED_KPATH_REPLAY_AUTHORIZATION_REVIEW_RESPONSE_V1",
        "review_completed": str(completed).lower(),
        "review_rows": str(len(rows)),
        "q5_answer": q5,
        "forbidden_inputs_used": str(forbidden_inputs_used).lower(),
        "permission_only_guarded_replay_package_preparation_allowed": str(
            replay_package_preparation_allowed and not forbidden_inputs_used and completed
        ).lower(),
        "endpoint_replay_allowed_by_this_review": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "claim_boundary": "replay_authorization_response_import_not_scoring",
        "verdict": (
            "ACT_CAVEATED_KPATH_REPLAY_PACKAGE_PREPARATION_ALLOWED_NOT_SCORING"
            if replay_package_preparation_allowed and not forbidden_inputs_used and completed
            else "ACT_CAVEATED_KPATH_REPLAY_PACKAGE_PREPARATION_NOT_ALLOWED"
        ),
    }
    with OUT_SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(f"ACT_CAVEATED_KPATH_REPLAY_AUTHORIZATION_RESPONSE_IMPORTED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()
