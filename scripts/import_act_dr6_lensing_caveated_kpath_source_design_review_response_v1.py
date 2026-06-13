#!/usr/bin/env python3
"""Import the completed ACT caveated K_path source-design review response."""

from __future__ import annotations

import csv
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DEFAULT_ZIP = (
    Path.home()
    / "Downloads"
    / "act_dr6_lensing_caveated_kpath_source_design_completed_review_response_v1.zip"
)

EXPECTED = {
    "act_dr6_lensing_caveated_kpath_source_design_review_response_v1.csv": DERIVED
    / "act_dr6_lensing_caveated_kpath_source_design_review_response_v1.csv",
    "act_dr6_lensing_caveated_kpath_source_design_review_completed_summary_v1.csv": DERIVED
    / "act_dr6_lensing_caveated_kpath_source_design_review_completed_summary_v1.csv",
    "act_dr6_lensing_caveated_kpath_source_design_review_notes_v1.md": DERIVED
    / "act_dr6_lensing_caveated_kpath_source_design_review_notes_v1.md",
    "act_dr6_lensing_caveated_kpath_source_design_review_validation_log_v1.txt": DERIVED
    / "act_dr6_lensing_caveated_kpath_source_design_review_validation_log_v1.txt",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    zip_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ZIP
    if not zip_path.exists():
        raise SystemExit(f"missing review response zip: {zip_path}")

    DERIVED.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(tmp)
        for name, out_path in EXPECTED.items():
            src = tmp / name
            if not src.exists():
                raise SystemExit(f"response zip missing {name}")
            shutil.copyfile(src, out_path)

    summary = read_rows(EXPECTED["act_dr6_lensing_caveated_kpath_source_design_review_completed_summary_v1.csv"])
    if len(summary) != 1:
        raise SystemExit("completed summary must contain exactly one row")
    row = summary[0]
    if row["decision"] != "ACCEPT_CAVEATED_KPATH_SOURCE_DESIGN_FOR_REVIEW_ONLY":
        raise SystemExit(f"unexpected decision: {row['decision']}")
    if row["current_replay_authorized_by_this_review"] != "false":
        raise SystemExit("source-design review must not authorize current replay")
    if row["future_permission_only_replay_review_preparation_allowed"] != "true":
        raise SystemExit("source-design review should allow only future replay-review preparation")
    print(
        "ACT_CAVEATED_KPATH_SOURCE_DESIGN_REVIEW_RESPONSE_IMPORTED "
        "decision=ACCEPT_CAVEATED_KPATH_SOURCE_DESIGN_FOR_REVIEW_ONLY"
    )


if __name__ == "__main__":
    main()
