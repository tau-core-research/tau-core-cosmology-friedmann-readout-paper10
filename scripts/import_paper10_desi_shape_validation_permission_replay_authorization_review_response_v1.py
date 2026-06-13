#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_RESPONSE = (
    ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_v1.csv"
)
CANONICAL_SUMMARY = (
    ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_v1_summary.csv"
)
CANONICAL_COMPLETED_SUMMARY = (
    ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_completed_summary_v1.csv"
)
CANONICAL_LOG = (
    ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_validation_log_v1.txt"
)
CANONICAL_NOTES = (
    ROOT / "docs/paper10_desi_shape_validation_permission_replay_authorization_review_notes_v1.md"
)
VALIDATOR = ROOT / "scripts/validate_paper10_desi_shape_validation_permission_replay_authorization_review_response_v1.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import a completed external DESI shape validation-permission replay authorization response."
    )
    parser.add_argument("response", help="Path to completed reviewer response CSV or ZIP.")
    return parser.parse_args()


def find_response_csv(path: Path, tmp: Path) -> Path:
    if path.suffix.lower() == ".csv":
        return path
    if path.suffix.lower() != ".zip":
        raise SystemExit(f"response must be a CSV or ZIP file: {path}")
    with zipfile.ZipFile(path) as zf:
        names = [n for n in zf.namelist() if n.endswith("_response_v1.csv")]
        if len(names) != 1:
            raise SystemExit(f"expected exactly one response CSV in zip, found {len(names)}")
        zf.extract(names[0], tmp)
        for optional, target in [
            ("paper10_desi_shape_validation_permission_replay_authorization_review_completed_summary_v1.csv", CANONICAL_COMPLETED_SUMMARY),
            ("paper10_desi_shape_validation_permission_replay_authorization_review_validation_log_v1.txt", CANONICAL_LOG),
            ("paper10_desi_shape_validation_permission_replay_authorization_review_notes_v1.md", CANONICAL_NOTES),
        ]:
            if optional in zf.namelist():
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(optional) as src:
                    target.write_bytes(src.read())
        return tmp / names[0]


def run_validator(response: Path, summary: Path) -> None:
    result = subprocess.run(
        [
            "python",
            str(VALIDATOR.relative_to(ROOT)),
            str(response),
            "--summary-out",
            str(summary),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "validator rejected response").strip()
        raise SystemExit(f"response validation failed; canonical artifacts were not modified: {detail}")


def main() -> None:
    args = parse_args()
    response = Path(args.response).expanduser()
    if not response.is_absolute():
        response = (Path.cwd() / response).resolve()
    if not response.exists():
        raise SystemExit(f"response does not exist: {response}")

    with tempfile.TemporaryDirectory(prefix="desi_shape_validation_permission_import_") as tmpdir:
        tmp = Path(tmpdir)
        response_csv = find_response_csv(response, tmp)
        tmp_summary = tmp / "validated_summary.csv"
        run_validator(response_csv, tmp_summary)
        CANONICAL_RESPONSE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(response_csv, CANONICAL_RESPONSE)
        shutil.copy2(tmp_summary, CANONICAL_SUMMARY)
        shutil.copy2(tmp_summary, CANONICAL_COMPLETED_SUMMARY)

    print(
        "PAPER10_DESI_SHAPE_VALIDATION_PERMISSION_REPLAY_AUTHORIZATION_RESPONSE_IMPORTED "
        f"response={CANONICAL_RESPONSE.relative_to(ROOT)} "
        f"summary={CANONICAL_SUMMARY.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
