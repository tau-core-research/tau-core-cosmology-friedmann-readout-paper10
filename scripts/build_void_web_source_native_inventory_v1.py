#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data" / "source_manifest" / "void_web_source_native_frozen_products_v1.csv"
OUT = ROOT / "data" / "derived" / "void_web_source_native_inventory_v1.csv"


def count_void_table(path: Path) -> tuple[int, list[str]]:
    with path.open() as f:
        lines = [line.strip() for line in f if line.strip()]
    header = lines[0].lstrip("# ").split()
    data_rows = [line for line in lines[1:] if not line.startswith("#")]
    return len(data_rows), header


def parse_fits_bintable_rows(path: Path) -> tuple[int, int, int]:
    with path.open("rb") as f:
        extension = 0
        while True:
            header = b""
            while True:
                block = f.read(2880)
                if not block:
                    raise SystemExit(f"no BINTABLE extension found in {path}")
                header += block
                if b"END" in block:
                    break
            cards = [header[i : i + 80].decode("ascii", "ignore") for i in range(0, len(header), 80)]
            values: dict[str, str] = {}
            for card in cards:
                key = card[:8].strip()
                if not key or key == "END":
                    continue
                if card[8:10] == "= ":
                    values[key] = card[10:30].split("/")[0].strip().strip("'")
            if values.get("XTENSION") == "BINTABLE":
                return (
                    int(values.get("NAXIS2", "0") or 0),
                    int(values.get("NAXIS1", "0") or 0),
                    int(values.get("TFIELDS", "0") or 0),
                )
            naxis = int(values.get("NAXIS", "0") or 0)
            bitpix = abs(int(values.get("BITPIX", "8") or 8))
            data_size = 0
            if naxis > 0:
                product = 1
                for idx in range(1, naxis + 1):
                    product *= int(values.get(f"NAXIS{idx}", "0") or 0)
                data_size = product * bitpix // 8
            padding = (2880 - (data_size % 2880)) % 2880
            f.seek(data_size + padding, 1)
            extension += 1


def main() -> None:
    with FROZEN.open(newline="") as f:
        rows = list(csv.DictReader(f))

    output_rows: list[dict[str, str]] = []
    for row in rows:
        path = ROOT / row["local_path"]
        product_id = row["frozen_product_id"]
        if product_id == "VOIDFINDER_PLANCK2018_MAXIMAL_VOID_TABLE":
            n_rows, columns = count_void_table(path)
            observable_summary = f"void_rows={n_rows};columns={'|'.join(columns)}"
        elif product_id == "SDSS_DR17_MCPM_SLIMEMOLD_GALAXY_CATALOG":
            n_rows, row_bytes, n_fields = parse_fits_bintable_rows(path)
            observable_summary = (
                f"fits_bintable_rows={n_rows};row_bytes={row_bytes};fields={n_fields}"
            )
        elif product_id == "VOIDFINDER_PLANCK2018_MASK":
            observable_summary = "mask_pickle_frozen_not_parsed"
        elif product_id == "SDSS_DR17_MCPM_SHA1SUM":
            observable_summary = "provider_sha1sum_frozen"
        else:
            observable_summary = "frozen_not_parsed"

        output_rows.append(
            {
                "frozen_product_id": product_id,
                "channel_id": row["channel_id"],
                "local_path": row["local_path"],
                "byte_count": row["byte_count"],
                "sha256": row["sha256"],
                "observable_summary": observable_summary,
                "endpoint_allowed": "false",
                "contains_endpoint_scores": "false",
                "contains_residuals": "false",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"PAPER10_VOID_WEB_SOURCE_NATIVE_INVENTORY_V1_BUILT rows={len(output_rows)}")


if __name__ == "__main__":
    main()
