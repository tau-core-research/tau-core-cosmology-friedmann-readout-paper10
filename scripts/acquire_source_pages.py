#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "data" / "source_manifest" / "paper10_source_freeze_manifest.csv"
CACHE_DIR = ROOT / "data" / "source_manifest" / "source_page_cache"
CACHE_MANIFEST = ROOT / "data" / "source_manifest" / "source_page_cache_manifest.csv"


def slug(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("_")


def fetch(url: str) -> tuple[int, bytes]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "tau-core-paper10-source-provenance-cache/0.1",
            "Accept": "text/html,application/xhtml+xml,application/xml,text/plain,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        status = getattr(response, "status", 200)
        payload = response.read(2_000_000)
    return int(status), payload


def main() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with SOURCE_MANIFEST.open(newline="") as f:
        rows = list(csv.DictReader(f))

    out_rows: list[dict[str, str]] = []
    acquired_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    for row in rows:
        source_id = row["source_id"]
        url = row["official_url"]
        cache_name = f"{slug(source_id)}.html"
        cache_path = CACHE_DIR / cache_name
        try:
            status_code, payload = fetch(url)
            sha256 = hashlib.sha256(payload).hexdigest()
            cache_path.write_bytes(payload)
            status = "CACHED"
            error = ""
        except Exception as exc:  # noqa: BLE001 - provenance script records failures.
            status_code = 0
            payload = b""
            sha256 = ""
            status = "FETCH_FAILED"
            error = f"{type(exc).__name__}: {exc}"
        out_rows.append(
            {
                "source_id": source_id,
                "official_url": url,
                "cache_path": str(cache_path.relative_to(ROOT)),
                "status": status,
                "status_code": str(status_code),
                "byte_count": str(len(payload)),
                "sha256": sha256,
                "acquired_at_utc": acquired_at,
                "error": error,
            }
        )

    with CACHE_MANIFEST.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "source_id",
                "official_url",
                "cache_path",
                "status",
                "status_code",
                "byte_count",
                "sha256",
                "acquired_at_utc",
                "error",
            ],
        )
        writer.writeheader()
        writer.writerows(out_rows)

    failed = [row["source_id"] for row in out_rows if row["status"] != "CACHED"]
    print(f"PAPER10_SOURCE_PAGES_ACQUIRED rows={len(out_rows)} failed={len(failed)}")
    if failed:
        print("failed_source_pages=" + ",".join(failed))


if __name__ == "__main__":
    main()
