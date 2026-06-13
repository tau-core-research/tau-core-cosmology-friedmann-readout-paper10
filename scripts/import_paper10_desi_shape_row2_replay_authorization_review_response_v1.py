#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ZIP = Path("/Users/jolcsak/Downloads/paper10_desi_shape_row2_replay_authorization_completed_review_response_v1.zip")
DESTINATIONS = {
    "paper10_desi_shape_row2_replay_authorization_review_response_v1.csv": ROOT
    / "data/derived/paper10_desi_shape_row2_replay_authorization_review_response_v1.csv",
    "paper10_desi_shape_row2_replay_authorization_review_completed_summary_v1.csv": ROOT
    / "data/derived/paper10_desi_shape_row2_replay_authorization_review_completed_summary_v1.csv",
    "paper10_desi_shape_row2_replay_authorization_review_notes_v1.md": ROOT
    / "docs/paper10_desi_shape_row2_replay_authorization_review_notes_v1.md",
    "paper10_desi_shape_row2_replay_authorization_review_validation_log_v1.txt": ROOT
    / "data/derived/paper10_desi_shape_row2_replay_authorization_review_validation_log_v1.txt",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import completed Row2 replay authorization review ZIP.")
    parser.add_argument("zip_path", nargs="?", default=str(DEFAULT_ZIP))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    zip_path = Path(args.zip_path).expanduser()
    if not zip_path.exists():
        raise SystemExit(f"missing completed response ZIP: {zip_path}")
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
        missing = set(DESTINATIONS) - names
        if missing:
            raise SystemExit(f"completed response ZIP is missing: {sorted(missing)}")
        tmp = ROOT / "data/derived/.tmp_row2_replay_authorization_response_import"
        if tmp.exists():
            shutil.rmtree(tmp)
        tmp.mkdir(parents=True)
        zf.extractall(tmp)
    try:
        for name, dest in DESTINATIONS.items():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(tmp / name, dest)
        subprocess.run(
            [
                "python",
                "scripts/validate_paper10_desi_shape_row2_replay_authorization_review_response_v1.py",
            ],
            cwd=ROOT,
            check=True,
        )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("PAPER10_DESI_SHAPE_ROW2_REPLAY_AUTHORIZATION_RESPONSE_IMPORTED")


if __name__ == "__main__":
    main()
