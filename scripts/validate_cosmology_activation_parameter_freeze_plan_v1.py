#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARAMETER_PLAN = (
    ROOT / "data" / "source_manifest" / "cosmology_activation_parameter_freeze_plan_v1.csv"
)
RULE_MANIFEST = ROOT / "data" / "source_manifest" / "cosmology_activation_rule_manifest_v1.csv"
SOURCE_MANIFEST = ROOT / "data" / "source_manifest" / "paper10_source_freeze_manifest.csv"

REQUIRED_PARAMETERS = {
    "P_VOID_S_STAR",
    "P_VOID_Q_OPTIONAL",
    "P_WEB_Q_STAR",
    "P_WEB_CLASS_WEIGHTS",
    "P_PATH_LENS_STAR",
    "P_PATH_MASK_POLICY",
    "P_TIME_CLOCK_STAR",
    "P_TIME_ZBIN_POLICY",
}

ALLOWED_STATUSES = {"PARAMETER_FREEZE_ROUTE_DECLARED_NOT_NUMERIC"}

COMMON_FORBIDDEN = {
    "distance_residuals",
    "fit_improvement_flags",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def split_semicolon(value: str) -> set[str]:
    return {part.strip() for part in value.split(";") if part.strip()}


def main() -> None:
    rows = read_csv(PARAMETER_PLAN)
    rule_rows = read_csv(RULE_MANIFEST)
    source_rows = read_csv(SOURCE_MANIFEST)
    if not rows:
        raise SystemExit("activation parameter freeze plan is empty")

    parameter_ids = {row["parameter_id"] for row in rows}
    missing = REQUIRED_PARAMETERS - parameter_ids
    if missing:
        raise SystemExit(f"parameter freeze plan missing parameters: {sorted(missing)}")

    rule_to_channel = {row["activation_rule_id"]: row["channel_id"] for row in rule_rows}
    source_ids = {row["source_id"] for row in source_rows}

    for row in rows:
        parameter_id = row["parameter_id"]
        rule_id = row["activation_rule_id"]
        if rule_id not in rule_to_channel:
            raise SystemExit(f"{parameter_id}: unknown activation_rule_id={rule_id}")
        if rule_to_channel[rule_id] != row["channel_id"]:
            raise SystemExit(
                f"{parameter_id}: channel mismatch for {rule_id}: "
                f"{row['channel_id']} != {rule_to_channel[rule_id]}"
            )
        if row["freeze_status"] not in ALLOWED_STATUSES:
            raise SystemExit(f"{parameter_id}: invalid freeze_status={row['freeze_status']}")
        if row["endpoint_scoring_allowed"].lower() != "false":
            raise SystemExit(f"{parameter_id}: endpoint_scoring_allowed must be false")
        if not row["parameter_symbol"]:
            raise SystemExit(f"{parameter_id}: parameter_symbol is blank")
        if not row["freeze_rule_shell"]:
            raise SystemExit(f"{parameter_id}: freeze_rule_shell is blank")
        if not row["required_future_artifact"].endswith(".csv"):
            raise SystemExit(f"{parameter_id}: required_future_artifact must be a csv path")
        if not row["null_control"]:
            raise SystemExit(f"{parameter_id}: null_control is blank")

        allowed_sources = split_semicolon(row["allowed_source_ids"])
        unknown_sources = allowed_sources - source_ids
        if unknown_sources:
            raise SystemExit(f"{parameter_id}: unknown allowed_source_ids={sorted(unknown_sources)}")

        forbidden = split_semicolon(row["forbidden_inputs"])
        missing_forbidden = COMMON_FORBIDDEN - forbidden
        if missing_forbidden:
            raise SystemExit(
                f"{parameter_id}: missing forbidden endpoint markers={sorted(missing_forbidden)}"
            )

        fields_blob = row["allowed_source_fields"].lower()
        shell_blob = row["freeze_rule_shell"].lower()
        if "residual" in fields_blob or "fit_improvement" in fields_blob:
            raise SystemExit(f"{parameter_id}: allowed_source_fields contains endpoint language")
        if "residual" in shell_blob or "fit" in shell_blob:
            raise SystemExit(f"{parameter_id}: freeze_rule_shell contains endpoint language")

    future_artifacts = {row["required_future_artifact"] for row in rows}
    print(
        "PAPER10_COSMOLOGY_ACTIVATION_PARAMETER_FREEZE_PLAN_V1_VALIDATED "
        f"rows={len(rows)} parameters={len(parameter_ids)} "
        f"future_artifacts={len(future_artifacts)} endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()
