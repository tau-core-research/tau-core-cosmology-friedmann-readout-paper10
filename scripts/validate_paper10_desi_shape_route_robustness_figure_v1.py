#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIGURE = ROOT / "paper10_submission_source/figures/fig_desi_shape_route_robustness_stress.pdf"


def main() -> None:
    if not FIGURE.exists() or FIGURE.stat().st_size == 0:
        raise SystemExit("missing DESI shape-route robustness stress figure")
    print("paper10_desi_shape_route_robustness_figure_v1: OK")


if __name__ == "__main__":
    main()
