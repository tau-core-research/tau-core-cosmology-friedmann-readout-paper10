#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data" / "source_manifest" / "pantheon_scoring_protocol_v1.csv"
SCOPE_SUMMARY = ROOT / "data" / "derived" / "pantheon_scope_v1_summary.csv"

FORBIDDEN_SCORE_ARTIFACTS = [
    ROOT / "data" / "derived" / "pantheon_scoring_v1_results.csv",
    ROOT / "data" / "derived" / "pantheon_scoring_v1_residuals.csv",
    ROOT / "data" / "derived" / "pantheon_tau_fit_results.csv",
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def main() -> None:
    protocol = read_one(PROTOCOL)
    scope = read_one(SCOPE_SUMMARY)

    if protocol["status"] != "SCORING_PROTOCOL_FROZEN_NOT_RUN":
        raise SystemExit("scoring protocol must remain frozen-not-run")
    if protocol["scoring_allowed"].lower() != "false":
        raise SystemExit("scoring_allowed must remain false")
    if scope["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("parent Pantheon scope must remain unscored")
    if protocol["parent_scope_id"] != scope["scope_id"]:
        raise SystemExit("scoring protocol parent_scope_id mismatch")
    if "flat_LCDM" not in protocol["baseline_family"]:
        raise SystemExit("baseline family must be declared")
    if "W_tau" not in protocol["tau_activation_family"]:
        raise SystemExit("Tau activation family must be declared")
    forbidden = protocol["forbidden_inputs"]
    for marker in [
        "distance_residuals",
        "fit_improvement_flags",
        "Tau_residual_parameters",
        "late_time_activation_fit",
        "posthoc_row_masks",
    ]:
        if marker not in forbidden:
            raise SystemExit(f"scoring protocol missing forbidden marker: {marker}")
    existing_forbidden = [str(path.relative_to(ROOT)) for path in FORBIDDEN_SCORE_ARTIFACTS if path.exists()]
    if existing_forbidden:
        raise SystemExit(
            "scoring protocol freeze cannot coexist with score artifacts: "
            + ",".join(existing_forbidden)
        )

    print("PAPER10_PANTHEON_SCORING_PROTOCOL_V1_VALIDATED scoring_allowed=false")


if __name__ == "__main__":
    main()
