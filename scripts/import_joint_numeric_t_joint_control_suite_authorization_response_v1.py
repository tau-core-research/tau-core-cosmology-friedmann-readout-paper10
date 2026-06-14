#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_RESPONSE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_response_v1.csv"
CANONICAL_SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_response_v1_summary.csv"
VALIDATOR = ROOT / "scripts/validate_joint_numeric_t_joint_control_suite_authorization_response_v1.py"
NAMES = {
    "joint_numeric_t_joint_control_suite_authorization_response_v1.csv",
    "joint_numeric_t_joint_control_suite_authorization_review_response_v1.csv",
    "joint_numeric_t_joint_control_suite_authorization_response_template_v1.csv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import completed numeric T_joint control-suite authorization response.")
    parser.add_argument("response", help="Completed reviewer response CSV or zip.")
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    return path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def find_response(zip_path: Path, tmp: Path) -> Path:
    with zipfile.ZipFile(zip_path) as zf:
        names = [name for name in zf.namelist() if name.lower().endswith(".csv")]
        candidates = [name for name in names if Path(name).name in NAMES]
        if not candidates and len(names) == 1:
            candidates = names
        if len(candidates) != 1:
            raise SystemExit(f"zip must contain exactly one response CSV; found {names}")
        zf.extract(candidates[0], tmp)
        return tmp / candidates[0]


def run_validator(response: Path, summary: Path) -> None:
    result = subprocess.run(
        ["python", str(VALIDATOR.relative_to(ROOT)), str(response), "--summary-out", str(summary)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "validator rejected response").strip()
        raise SystemExit(f"response validation failed; canonical artifacts were not modified: {detail}")


def main() -> None:
    args = parse_args()
    source = resolve(args.response)
    if not source.exists():
        raise SystemExit(f"response path does not exist: {source}")
    with tempfile.TemporaryDirectory(prefix="joint_numeric_tjoint_control_suite_import_") as tmp_text:
        tmp = Path(tmp_text)
        if source.suffix.lower() == ".zip":
            response = find_response(source, tmp)
        elif source.suffix.lower() == ".csv":
            response = source
        else:
            raise SystemExit("response must be CSV or zip")
        rows = read_rows(response)
        if len(rows) != 4 or {row.get("review_completed", "").strip().lower() for row in rows} != {"true"}:
            raise SystemExit("refusing to import incomplete response")
        tmp_summary = tmp / "summary.csv"
        run_validator(response, tmp_summary)
        CANONICAL_RESPONSE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(response, CANONICAL_RESPONSE)
        run_validator(CANONICAL_RESPONSE, CANONICAL_SUMMARY)
        decision = read_rows(CANONICAL_SUMMARY)[0]["decision"]
    print(
        "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_AUTHORIZATION_RESPONSE_IMPORTED "
        f"decision={decision} response={CANONICAL_RESPONSE.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
