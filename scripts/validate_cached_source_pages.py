#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CACHE_MANIFEST = ROOT / "data" / "source_manifest" / "source_page_cache_manifest.csv"


def main() -> None:
    if not CACHE_MANIFEST.exists():
        raise SystemExit("source page cache manifest is missing")

    with CACHE_MANIFEST.open(newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise SystemExit("source page cache manifest is empty")

    failures: list[str] = []
    for row in rows:
        source_id = row["source_id"]
        if row["status"] != "CACHED":
            failures.append(f"{source_id}: status={row['status']}")
            continue
        path = ROOT / row["cache_path"]
        if not path.exists():
            failures.append(f"{source_id}: cache_path missing")
            continue
        payload = path.read_bytes()
        sha256 = hashlib.sha256(payload).hexdigest()
        if sha256 != row["sha256"]:
            failures.append(f"{source_id}: sha256 mismatch")
        if str(len(payload)) != row["byte_count"]:
            failures.append(f"{source_id}: byte_count mismatch")
        try:
            status_code = int(row["status_code"])
        except ValueError:
            failures.append(f"{source_id}: invalid status_code")
            continue
        if status_code < 200 or status_code >= 400:
            failures.append(f"{source_id}: non-success status_code={status_code}")

    if failures:
        raise SystemExit("source page cache validation failed: " + "; ".join(failures))

    print(f"PAPER10_SOURCE_PAGE_CACHE_VALIDATED rows={len(rows)}")


if __name__ == "__main__":
    main()
