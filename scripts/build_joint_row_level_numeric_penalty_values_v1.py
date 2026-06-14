#!/usr/bin/env python3
from __future__ import annotations

import csv
import gzip
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSFORM = ROOT / "data/derived/joint_candidate_control_symmetric_normalized_feature_transform_v1.csv.gz"
WEIGHTS = ROOT / "data/derived/joint_row_level_penalty_block_weight_binding_shell_v1.csv"
AUTH_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_authorization_review_response_v1_summary.csv"
OUT = ROOT / "data/derived/joint_row_level_numeric_penalty_values_v1.csv"
JOINT_OUT = ROOT / "data/derived/joint_row_level_numeric_penalty_values_joint_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_values_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_numeric_penalty_values_v1.md"
CLAIM_BOUNDARY = "joint_row_level_numeric_penalty_values_not_rescoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_gzip_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with gzip.open(path, "rt", newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def parse_float(value: str, context: str) -> float:
    try:
        if "/" in value:
            numerator, denominator = value.split("/", 1)
            result = float(numerator) / float(denominator)
        else:
            result = float(value)
    except ValueError as exc:
        raise SystemExit(f"non-numeric value for {context}: {value!r}") from exc
    if not math.isfinite(result):
        raise SystemExit(f"non-finite value for {context}: {value!r}")
    return result


def load_weights() -> dict[str, float]:
    rows = read_rows(WEIGHTS)
    weights: dict[str, float] = {}
    for row in rows:
        channel = row["channel_id"]
        value = row["future_row_penalty_block_weight_value"]
        weights[channel] = parse_float(value, f"omega_i[{channel}]")
    require(weights, "no block weights loaded")
    total = sum(weights.values())
    require(abs(total - 1.0) < 1e-9, f"block weights must sum to 1.0, got {total}")
    return weights


def check_authorization() -> dict[str, str]:
    auth = read_one(AUTH_SUMMARY)
    require(
        auth["decision"] == "AUTHORIZE_SEPARATE_NUMERIC_PENALTY_VALUE_PACKAGE_NOT_RESCORING_NOT_VALIDATION",
        f"unexpected authorization decision: {auth['decision']}",
    )
    require(auth["numeric_penalty_computation_authorized"] == "true", "numeric penalty computation not authorized")
    require(auth["lambda_row_numeric_value_authorized"] == "false", "lambda_row numeric value must remain unauthorized")
    require(auth["t_joint_rescoring_authorized"] == "false", "T_joint rescoring must remain unauthorized")
    require(auth["endpoint_scoring_allowed"] == "false", "endpoint scoring must remain forbidden")
    require(auth["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
    return auth


def main() -> None:
    auth = check_authorization()
    weights = load_weights()
    rows = read_gzip_rows(TRANSFORM)
    require(rows, "normalized transform is empty")

    groups: dict[tuple[str, str, str, str], dict[str, object]] = {}
    for idx, row in enumerate(rows, start=1):
        require(row["uses_endpoint_scores_or_residuals"] == "false", f"endpoint leakage flag at transform row {idx}")
        require(row["numeric_t_joint_rescoring_allowed"] == "false", f"rescoring flag at transform row {idx}")
        require(row["endpoint_validation_claimed"] == "false", f"validation flag at transform row {idx}")
        channel = row["channel_id"]
        require(channel in weights, f"missing block weight for channel {channel}")
        key = (channel, row["row_type"], row["control_family"], row["control_id"])
        z = parse_float(row["normalized_feature_value"], f"normalized_feature_value row {idx}")
        if key not in groups:
            groups[key] = {
                "count": 0,
                "sum_z2": 0.0,
                "source_artifacts": set(),
            }
        groups[key]["count"] = int(groups[key]["count"]) + 1
        groups[key]["sum_z2"] = float(groups[key]["sum_z2"]) + z * z
        cast_set = groups[key]["source_artifacts"]
        assert isinstance(cast_set, set)
        cast_set.add(row["source_artifact"])

    value_rows: list[dict[str, str]] = []
    for ordinal, key in enumerate(sorted(groups), start=1):
        channel, row_type, control_family, control_id = key
        group = groups[key]
        count = int(group["count"])
        sum_z2 = float(group["sum_z2"])
        mean_z2 = sum_z2 / count
        omega = weights[channel]
        p_i = omega * mean_z2
        source_artifacts = sorted(group["source_artifacts"])
        value_rows.append(
            {
                "value_id": f"JRNPV1_{ordinal:05d}",
                "channel_id": channel,
                "row_type": row_type,
                "control_family": control_family,
                "control_id": control_id,
                "feature_row_count": str(count),
                "sum_z2": f"{sum_z2:.12g}",
                "mean_z2": f"{mean_z2:.12g}",
                "omega_i": f"{omega:.12g}",
                "P_i": f"{p_i:.12g}",
                "joint_scope": "complete_joint_candidate" if row_type == "candidate" else "channel_local_control_only",
                "joint_penalty_contribution_allowed": "true" if row_type == "candidate" else "false",
                "lambda_row_numeric_value_defined": "false",
                "t_joint_rescoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "source_artifact_count": str(len(source_artifacts)),
                "source_artifacts": "|".join(source_artifacts),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    write_csv(OUT, value_rows)

    active_channels = sorted(weights)
    candidate_rows = [row for row in value_rows if row["row_type"] == "candidate"]
    candidate_channels = sorted(row["channel_id"] for row in candidate_rows)
    complete_candidate = candidate_channels == active_channels
    require(complete_candidate, f"candidate is not complete across channels: {candidate_channels} vs {active_channels}")
    p_row_candidate = sum(parse_float(row["P_i"], f"P_i[{row['channel_id']}]") for row in candidate_rows)

    joint_rows = [
        {
            "joint_value_id": "JRNPV1_JOINT_CANDIDATE",
            "row_type": "candidate",
            "control_family": "candidate",
            "control_id": "candidate",
            "channels_present": "|".join(candidate_channels),
            "channels_present_count": str(len(candidate_channels)),
            "channels_required": "|".join(active_channels),
            "channels_required_count": str(len(active_channels)),
            "joint_penalty_computed": "true",
            "P_row": f"{p_row_candidate:.12g}",
            "control_joint_penalty_computed": "false",
            "control_joint_penalty_reason": "controls are channel-local null alternatives and are not cross-channel aligned in this package",
            "lambda_row_numeric_value_defined": "false",
            "t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(JOINT_OUT, joint_rows)

    control_rows = [row for row in value_rows if row["row_type"] != "candidate"]
    summary = {
        "package_id": "JOINT_ROW_LEVEL_NUMERIC_PENALTY_VALUES_V1",
        "authorization_response": str(AUTH_SUMMARY.relative_to(ROOT)),
        "authorization_decision": auth["decision"],
        "normalized_transform": str(TRANSFORM.relative_to(ROOT)),
        "block_weight_shell": str(WEIGHTS.relative_to(ROOT)),
        "feature_rows_read": str(len(rows)),
        "channel_penalty_rows": str(len(value_rows)),
        "candidate_channel_penalty_rows": str(len(candidate_rows)),
        "control_channel_penalty_rows": str(len(control_rows)),
        "complete_joint_penalty_rows": str(len(joint_rows)),
        "candidate_joint_penalty_computed": "true",
        "control_joint_penalty_computed": "false",
        "control_joint_penalty_reason": "control alternatives remain channel-local; no residual-blind cross-channel alignment artifact is authorized here",
        "P_row_candidate": f"{p_row_candidate:.12g}",
        "lambda_row_numeric_value_defined": "false",
        "t_joint_rescoring_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "penalty_values_computed": "true",
        "verdict": "NUMERIC_PENALTY_VALUES_COMPUTED_NOT_RESCORING",
        "next_required_action": "review_numeric_penalty_values_before_any_lambda_or_rescoring",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level numeric penalty values v1",
                "",
                "**Doc class:** numeric value package.",
                "**Status:** separate penalty values only; not `lambda_row`; not `T_joint` rescoring; not endpoint validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This package implements the reviewer-authorized numeric value step",
                "for the symbolic row-level penalty shell. It computes channel-local",
                "penalty values",
                "",
                "`P_i(a) = omega_i mean_{r,f}(z_{i,a,r,f}^2)`",
                "",
                "from the residual-blind normalized source-feature transform and the",
                "frozen equal block weights. It does not choose a numeric `lambda_row`,",
                "does not modify `T_joint`, and does not perform endpoint scoring.",
                "",
                "## Scope",
                "",
                f"- feature rows read: `{summary['feature_rows_read']}`",
                f"- channel penalty rows: `{summary['channel_penalty_rows']}`",
                f"- candidate channel penalty rows: `{summary['candidate_channel_penalty_rows']}`",
                f"- control channel penalty rows: `{summary['control_channel_penalty_rows']}`",
                f"- complete joint penalty rows: `{summary['complete_joint_penalty_rows']}`",
                f"- candidate `P_row`: `{summary['P_row_candidate']}`",
                "",
                "Controls are kept as channel-local penalty values because the current",
                "source package does not define a residual-blind cross-channel control",
                "alignment. Inventing that alignment here would create a new analysis",
                "choice outside the authorization.",
                "",
                "## Boundary",
                "",
                "- `lambda_row_numeric_value_defined=false`",
                "- `t_joint_rescoring_allowed=false`",
                "- `endpoint_scoring_allowed=false`",
                "- `endpoint_validation_claimed=false`",
                "",
            ]
        )
    )
    print(
        "JOINT_ROW_LEVEL_NUMERIC_PENALTY_VALUES_V1_BUILT "
        f"channel_rows={len(value_rows)} P_row_candidate={summary['P_row_candidate']}"
    )


if __name__ == "__main__":
    main()
