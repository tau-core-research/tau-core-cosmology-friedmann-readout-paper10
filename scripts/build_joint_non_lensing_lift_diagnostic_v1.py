#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/derived/joint_multichannel_endpoint_candidate_v1.csv"
OUT = ROOT / "data/derived/joint_non_lensing_lift_diagnostic_v1.csv"
SUMMARY = ROOT / "data/derived/joint_non_lensing_lift_diagnostic_v1_summary.csv"
DOC = ROOT / "docs/joint_non_lensing_lift_diagnostic_v1.md"
CLAIM_BOUNDARY = "joint_non_lensing_lift_diagnostic_not_validation"
LENSING_CHANNEL = "kids_lensing_cosebis_low_mode"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = read_rows(INPUT)
    active = [row for row in rows if float(row["channel_weight"]) != 0.0]
    non_lensing = [row for row in active if row["channel_id"] != LENSING_CHANNEL]
    lensing = [row for row in active if row["channel_id"] == LENSING_CHANNEL]
    if len(lensing) != 1:
        raise SystemExit("expected exactly one KiDS/lensing channel")
    non_lensing_sum = sum(float(row["weighted_channel_score"]) for row in non_lensing)
    required_to_zero = max(0.0, -non_lensing_sum)
    required_to_margin_025 = max(0.0, 0.25 * sum(abs(float(row["channel_weight"])) for row in non_lensing) - non_lensing_sum)

    out_rows = []
    for row in non_lensing:
        weight = float(row["channel_weight"])
        score = float(row["bounded_channel_score"])
        weighted = float(row["weighted_channel_score"])
        max_weighted = weight * 1.0
        neutral_lift = -weighted if weighted < 0 else 0.0
        max_additional_lift = max(0.0, max_weighted - weighted)
        can_singlehandedly_zero = max_additional_lift >= required_to_zero and required_to_zero > 0
        can_singlehandedly_margin = max_additional_lift >= required_to_margin_025 and required_to_margin_025 > 0
        out_rows.append(
            {
                "diagnostic_id": "JOINT_NON_LENSING_LIFT_DIAGNOSTIC_V1",
                "channel_id": row["channel_id"],
                "current_bounded_score": f"{score:.9f}",
                "channel_weight": f"{weight:.3f}",
                "current_weighted_score": f"{weighted:.9f}",
                "neutral_lift_needed_for_this_channel": f"{neutral_lift:.9f}",
                "max_additional_lift_if_channel_reaches_score_1": f"{max_additional_lift:.9f}",
                "can_singlehandedly_make_non_lensing_sum_positive": str(can_singlehandedly_zero).lower(),
                "can_singlehandedly_reach_protocol_margin_0p25": str(can_singlehandedly_margin).lower(),
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    priority = sorted(out_rows, key=lambda r: float(r["max_additional_lift_if_channel_reaches_score_1"]), reverse=True)
    best_priority = priority[0]["channel_id"] if priority else "none"
    if required_to_zero == 0:
        verdict = "NON_LENSING_BLOCK_ALREADY_POSITIVE_NOT_VALIDATION"
    elif any(row["can_singlehandedly_make_non_lensing_sum_positive"] == "true" for row in out_rows):
        verdict = "NON_LENSING_FRAGILITY_REMEDIATION_HAS_SINGLE_CHANNEL_ROUTES_NOT_VALIDATION"
    else:
        verdict = "NON_LENSING_FRAGILITY_REQUIRES_MULTI_CHANNEL_REMEDIATION_NOT_VALIDATION"

    summary = {
        "diagnostic_id": "JOINT_NON_LENSING_LIFT_DIAGNOSTIC_V1",
        "active_non_lensing_channels": str(len(non_lensing)),
        "non_lensing_weighted_sum": f"{non_lensing_sum:.9f}",
        "required_lift_to_zero": f"{required_to_zero:.9f}",
        "required_lift_to_protocol_margin_0p25": f"{required_to_margin_025:.9f}",
        "highest_lift_priority_channel": best_priority,
        "single_channel_zero_routes": str(sum(1 for row in out_rows if row["can_singlehandedly_make_non_lensing_sum_positive"] == "true")),
        "single_channel_margin_routes": str(sum(1 for row in out_rows if row["can_singlehandedly_reach_protocol_margin_0p25"] == "true")),
        "verdict": verdict,
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(OUT, out_rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint non-lensing lift diagnostic v1",
                "",
                "**Doc class:** fragility-remediation diagnostic",
                "**Status:** not endpoint scoring; not validation",
                "",
                "This diagnostic asks how much non-lensing support is needed for the",
                "joint multichannel score to remain positive when the KiDS/COSEBIs",
                "lensing block is removed. It uses only the already frozen joint",
                "candidate channel ledger.",
                "",
                "Summary:",
                "",
                f"- non-lensing weighted sum: `{summary['non_lensing_weighted_sum']}`",
                f"- required lift to zero: `{summary['required_lift_to_zero']}`",
                f"- required lift to protocol margin 0.25: `{summary['required_lift_to_protocol_margin_0p25']}`",
                f"- highest lift-priority channel: `{summary['highest_lift_priority_channel']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: this identifies where additional source-frozen work",
                "would reduce KiDS/lensing dominance. It is not an invitation to tune",
                "a channel after looking at residuals.",
                "",
            ]
        )
    )
    print(
        "JOINT_NON_LENSING_LIFT_DIAGNOSTIC_V1_BUILT "
        f"non_lensing_sum={summary['non_lensing_weighted_sum']} "
        f"required_lift={summary['required_lift_to_zero']} "
        f"priority={best_priority}"
    )


if __name__ == "__main__":
    main()
