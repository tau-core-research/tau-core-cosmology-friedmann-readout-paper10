#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTE = ROOT / "data" / "source_manifest" / "kids1000_lensing_route_v1.csv"
HEAD = ROOT / "data" / "derived" / "kids1000_lensing_route_v1_head.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_lensing_route_v1_summary.csv"


def main() -> None:
    with ROUTE.open(newline="") as f:
        route = list(csv.DictReader(f))[0]
    with HEAD.open(newline="") as f:
        head = list(csv.DictReader(f))[0]
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if route["endpoint_scoring_allowed"] != "false":
        raise SystemExit("route endpoint flag must remain false")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("summary endpoint flag must remain false")
    if head["contains_lensing_data_vectors"] != "false":
        raise SystemExit("HEAD artifact must not contain lensing data vectors")
    if head["contains_covariance_matrices"] != "false":
        raise SystemExit("HEAD artifact must not contain covariance matrices")
    if summary["contains_lensing_likelihood"] != "false":
        raise SystemExit("route check must not contain a lensing likelihood")
    if int(head["status_code"]) != 200:
        raise SystemExit("KiDS route HEAD request did not return 200")
    if int(head["content_length"]) <= 0:
        raise SystemExit("KiDS route content length missing")
    if "gzip" not in head["content_type"]:
        raise SystemExit("KiDS route content type is not gzip")
    for marker in [
        "tomographic_bin_policy",
        "statistic_choice_COSEBIs_or_2PCF_or_bandpowers",
        "covariance_block_policy",
    ]:
        if marker not in summary["future_freeze_items"]:
            raise SystemExit(f"missing future freeze item: {marker}")
    print("PAPER10_KIDS1000_LENSING_ROUTE_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
