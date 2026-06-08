#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULE_MANIFEST = ROOT / "data" / "source_manifest" / "cosmology_activation_rule_manifest_v1.csv"
CHANNEL_MANIFEST = ROOT / "data" / "source_manifest" / "cosmology_channel_manifest_v1.csv"

REQUIRED_RULES = {
    "ACT_VOID_MATURITY_V1",
    "ACT_WEB_ANISOTROPY_V1",
    "ACT_PATH_PROJECTION_V1",
    "ACT_TIME_READOUT_V1",
}

ALLOWED_RULE_STATUSES = {"RULE_SHELL_DECLARED_NOT_NUMERIC"}

COMMON_FORBIDDEN = {
    "distance_residuals",
    "growth_residuals",
    "lensing_residuals",
    "fit_improvement_flags",
}

REQUIRED_OUTPUTS = {
    "ACT_VOID_MATURITY_V1": "W_void",
    "ACT_WEB_ANISOTROPY_V1": "W_web",
    "ACT_PATH_PROJECTION_V1": "W_path",
    "ACT_TIME_READOUT_V1": "W_time",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def split_semicolon(value: str) -> set[str]:
    return {part.strip() for part in value.split(";") if part.strip()}


def main() -> None:
    rows = read_csv(RULE_MANIFEST)
    channel_rows = read_csv(CHANNEL_MANIFEST)
    if not rows:
        raise SystemExit("activation rule manifest is empty")

    rule_ids = {row["activation_rule_id"] for row in rows}
    missing = REQUIRED_RULES - rule_ids
    if missing:
        raise SystemExit(f"activation rule manifest missing rules: {sorted(missing)}")

    channel_by_rule = {row["activation_rule_id"]: row["channel_id"] for row in channel_rows}
    channel_ids = {row["channel_id"] for row in channel_rows}

    for row in rows:
        rule_id = row["activation_rule_id"]
        channel_id = row["channel_id"]
        if channel_id not in channel_ids:
            raise SystemExit(f"{rule_id}: unknown channel_id={channel_id}")
        if channel_by_rule.get(rule_id) != channel_id:
            raise SystemExit(
                f"{rule_id}: channel manifest maps to {channel_by_rule.get(rule_id)} "
                f"but rule manifest maps to {channel_id}"
            )
        if row["rule_status"] not in ALLOWED_RULE_STATUSES:
            raise SystemExit(f"{rule_id}: invalid rule_status={row['rule_status']}")
        if row["endpoint_scoring_allowed"].lower() != "false":
            raise SystemExit(f"{rule_id}: endpoint_scoring_allowed must be false")
        if row["output_symbol"] != REQUIRED_OUTPUTS[rule_id]:
            raise SystemExit(f"{rule_id}: unexpected output_symbol={row['output_symbol']}")
        if not row["formula_shell"] or "=" not in row["formula_shell"]:
            raise SystemExit(f"{rule_id}: formula_shell must contain an equation shell")
        if not row["normalization_policy"]:
            raise SystemExit(f"{rule_id}: normalization_policy is blank")
        if not row["parameter_freeze_policy"].startswith("freeze_from_"):
            raise SystemExit(f"{rule_id}: parameter_freeze_policy must be source-freeze explicit")
        if not row["null_control"]:
            raise SystemExit(f"{rule_id}: null_control is blank")
        forbidden = split_semicolon(row["forbidden_inputs"])
        missing_forbidden = COMMON_FORBIDDEN - forbidden
        if missing_forbidden:
            raise SystemExit(
                f"{rule_id}: missing forbidden endpoint markers={sorted(missing_forbidden)}"
            )
        inputs_blob = row["source_inputs"].lower()
        if "residual" in inputs_blob or "fit_improvement" in inputs_blob:
            raise SystemExit(f"{rule_id}: source_inputs contains endpoint language")
        if row["output_range"] not in {"[0_1]", "[-1_1]"}:
            raise SystemExit(f"{rule_id}: unsupported output_range={row['output_range']}")

    print(
        "PAPER10_COSMOLOGY_ACTIVATION_RULE_MANIFEST_V1_VALIDATED "
        f"rows={len(rows)} rules={len(rule_ids)} endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()
