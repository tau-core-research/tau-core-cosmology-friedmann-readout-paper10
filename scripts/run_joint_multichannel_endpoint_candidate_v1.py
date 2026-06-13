#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/source_manifest/joint_multichannel_endpoint_manifest_v1.csv"
OUT = ROOT / "data/derived/joint_multichannel_endpoint_candidate_v1.csv"
SUMMARY = ROOT / "data/derived/joint_multichannel_endpoint_candidate_v1_summary.csv"
DOC = ROOT / "docs/joint_multichannel_endpoint_candidate_v1.md"
CLAIM_BOUNDARY = "joint_multichannel_endpoint_candidate_preflight_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def score_value(raw: float, transform: str) -> float:
    if transform == "delta_lower_is_better_tanh_scale_5":
        return -math.tanh(raw / 5.0)
    if transform == "delta_lower_is_better_tanh_scale_1":
        return -math.tanh(raw / 1.0)
    if transform == "delta_higher_is_better_tanh_scale_0p05":
        return math.tanh(raw / 0.05)
    if transform == "tail_fraction_lower_is_better_log10_scale_3":
        if raw <= 0:
            return 1.0
        return max(0.0, min(1.0, -math.log10(raw) / 3.0))
    if transform == "controls_better_penalty_scale_3":
        return -max(0.0, min(1.0, raw / 3.0))
    raise SystemExit(f"unknown score transform: {transform}")


def main() -> None:
    manifest_rows = read_rows(MANIFEST)
    if len(manifest_rows) < 5:
        raise SystemExit("joint manifest must contain at least five channels")

    result_rows: list[dict[str, str]] = []
    weighted_sum = 0.0
    absolute_weight = 0.0
    positive_components = 0
    negative_components = 0

    for manifest in manifest_rows:
        if manifest["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"bad claim boundary in manifest row: {manifest['channel_id']}")
        if manifest["endpoint_residual_fields_forbidden"].lower() != "true":
            raise SystemExit(f"endpoint residual fields must be forbidden for {manifest['channel_id']}")
        if manifest["label_selection_source"] != "pre_frozen_summary_artifact":
            raise SystemExit(f"label source is not frozen for {manifest['channel_id']}")

        source = ROOT / manifest["source_artifact"]
        source_row = read_one(source)
        metric_field = manifest["metric_field"]
        if metric_field not in source_row:
            raise SystemExit(f"{metric_field} not found in {source.relative_to(ROOT)}")
        raw = float(source_row[metric_field])
        bounded = score_value(raw, manifest["score_transform"])
        weight = float(manifest["channel_weight"])
        weighted = weight * bounded
        weighted_sum += weighted
        absolute_weight += abs(weight)
        if weighted > 0:
            positive_components += 1
        elif weighted < 0:
            negative_components += 1

        result_rows.append(
            {
                "joint_run_id": "JOINT_MULTICHANNEL_ENDPOINT_CANDIDATE_V1",
                "channel_id": manifest["channel_id"],
                "source_artifact": manifest["source_artifact"],
                "metric_field": metric_field,
                "raw_metric_value": f"{raw:.12g}",
                "score_transform": manifest["score_transform"],
                "bounded_channel_score": f"{bounded:.9f}",
                "channel_weight": f"{weight:.3f}",
                "weighted_channel_score": f"{weighted:.9f}",
                "channel_role": manifest["channel_role"],
                "endpoint_residual_fields_used": "false",
                "joint_endpoint_claimed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    normalized_joint_score = weighted_sum / absolute_weight if absolute_weight else 0.0
    if normalized_joint_score > 0.25 and positive_components >= 3 and negative_components >= 1:
        verdict = "JOINT_ENDPOINT_CANDIDATE_SIGNAL_PRESENT_PREVALIDATION"
    else:
        verdict = "JOINT_ENDPOINT_CANDIDATE_INCONCLUSIVE_PREVALIDATION"

    summary = {
        "joint_run_id": "JOINT_MULTICHANNEL_ENDPOINT_CANDIDATE_V1",
        "channels_in_manifest": str(len(manifest_rows)),
        "channels_scored": str(len(result_rows)),
        "positive_weighted_components": str(positive_components),
        "negative_weighted_components": str(negative_components),
        "absolute_protocol_weight": f"{absolute_weight:.3f}",
        "joint_weighted_sum": f"{weighted_sum:.9f}",
        "normalized_joint_score": f"{normalized_joint_score:.9f}",
        "verdict": verdict,
        "joint_endpoint_claimed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "requires_next_gate": "single_predeclared_joint_likelihood_with_covariance_shuffled_and_wrong_channel_controls",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(OUT, result_rows)
    write_csv(SUMMARY, [summary])

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint multichannel endpoint candidate v1",
                "",
                "**Doc class:** predeclared joint-channel preflight",
                "**Status:** candidate score only; not a joint endpoint; not cosmological validation",
                "",
                "This ledger is the first executable joint-channel layer above the existing",
                "artifact meta-score.  It reads the frozen channel manifest, applies only",
                "predeclared metric transforms, and records whether the combined pattern",
                "remains positive before a true joint likelihood is attempted.",
                "",
                "Forbidden interpretation: this is not an empirical validation of Tau Core",
                "cosmology and not a replacement for covariance-aware joint endpoint scoring.",
                "",
                "Summary:",
                "",
                f"- channels scored: `{summary['channels_scored']}`",
                f"- normalized joint score: `{summary['normalized_joint_score']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Next required gate:",
                "",
                "```text",
                summary["requires_next_gate"],
                "```",
                "",
            ]
        )
    )

    print(
        "JOINT_MULTICHANNEL_ENDPOINT_CANDIDATE_V1_RUN "
        f"channels={summary['channels_scored']} normalized_joint_score={summary['normalized_joint_score']} "
        f"verdict={verdict}"
    )


if __name__ == "__main__":
    main()
