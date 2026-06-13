#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COV_SUMMARY = ROOT / "data/derived/joint_covariance_model_requirements_gate_v1_summary.csv"
CLOSURE_SUMMARY = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_response_v1_summary.csv"
OUT = ROOT / "data/derived/joint_cross_probe_covariance_source_requirements_v1.csv"
SUMMARY = ROOT / "data/derived/joint_cross_probe_covariance_source_requirements_v1_summary.csv"
DOC = ROOT / "docs/joint_cross_probe_covariance_source_requirements_v1.md"
POLICY = ROOT / "data/source_manifest/joint_cross_probe_covariance_source_requirements_policy_v1.csv"
CLAIM_BOUNDARY = "joint_cross_probe_covariance_source_requirements_not_scoring_not_validation"


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
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    cov = read_one(COV_SUMMARY)
    closure = read_one(CLOSURE_SUMMARY)
    if cov["cross_probe_covariance_defined"] != "false":
        raise SystemExit("cross-probe covariance already defined; requirements gate should be revised")
    if closure["decision"] != "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_RESPONSE_TEMPLATE_READY_NOT_COMPLETED":
        raise SystemExit("closure review response is no longer blank; import/close path should run first")

    rows = [
        {
            "requirement_id": "CPC_SRC_01_ACTIVE_BLOCK_SCOPE",
            "route": "both",
            "requirement": "Freeze the exact active block vector order and row scopes for KiDS/COSEBIs, observer/path low-z, and DESI shape/readout.",
            "acceptable_source_evidence": "source manifests or completed review ledgers defining rows, masks, redshift windows, and channel identities without endpoint scores",
            "current_status": "partial",
            "current_evidence": cov["active_channel_order"],
            "blocks_scoring": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "CPC_SRC_02_CROSS_COV_PRODUCT",
            "route": "covariance_product",
            "requirement": "Provide a source-native or source-frozen covariance/correlation product covering cross-block terms between active probes.",
            "acceptable_source_evidence": "published joint covariance, official mock covariance, simulation ensemble, or frozen analytic covariance construction with dimensional scope",
            "current_status": "missing",
            "current_evidence": "no source-frozen KiDS-observer-DESI cross-probe covariance product",
            "blocks_scoring": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "CPC_SRC_03_SHARED_SKY_AND_MASK_OVERLAP",
            "route": "both",
            "requirement": "Quantify or bound shared-sky, mask, and line-of-sight overlap between the active blocks.",
            "acceptable_source_evidence": "survey footprints, sky masks, object/field overlap ledgers, or published overlap/independence statements",
            "current_status": "open",
            "current_evidence": "active blocks have heterogeneous sky support; no unified overlap bound frozen",
            "blocks_scoring": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "CPC_SRC_04_REDSHIFT_KERNEL_OVERLAP",
            "route": "both",
            "requirement": "Quantify or bound redshift/kernel overlap between lensing, low-z observer/path, and DESI shape/readout sensitivities.",
            "acceptable_source_evidence": "source redshift distributions, BAO/CC redshift rows, low-z masks, kernel support summaries, or source-side non-overlap rationale",
            "current_status": "open",
            "current_evidence": "component redshift scopes exist, but no cross-probe overlap covariance statement is frozen",
            "blocks_scoring": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "CPC_SRC_05_SHARED_COSMOLOGY_AND_NUISANCE",
            "route": "both",
            "requirement": "Identify shared cosmological, calibration, photo-z, distance-ladder, BAO, lensing, and nuisance parameters that could correlate blocks.",
            "acceptable_source_evidence": "published nuisance covariance, explicit nuisance marginalization policy, or source-side argument that shared parameters are not used in the limited statistic",
            "current_status": "open",
            "current_evidence": "no single nuisance binding across all active blocks is frozen",
            "blocks_scoring": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "CPC_SRC_06_BLOCK_DIAGONAL_LIMITS",
            "route": "independence_rationale",
            "requirement": "If using block diagonal covariance, explicitly freeze caveats and the approximation domain.",
            "acceptable_source_evidence": "reviewer-accepted rationale naming shared-sky, redshift, nuisance, calibration, and population covariance limitations",
            "current_status": "not_closed",
            "current_evidence": closure["decision"],
            "blocks_scoring": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "CPC_SRC_07_SAME_STATISTIC_AND_CONTROLS",
            "route": "both",
            "requirement": "Bind candidate and matched controls to the same covariance/statistic before any replay.",
            "acceptable_source_evidence": "frozen scoring authorization package after covariance closure; no endpoint residual leakage",
            "current_status": "blocked_until_covariance_closure",
            "current_evidence": "matched control suite exists as requirements only",
            "blocks_scoring": "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "CPC_SRC_08_FORBIDDEN_FIELDS",
            "route": "both",
            "requirement": "Forbid endpoint residuals, new endpoint scores, fit improvements, posterior chains, and post-score control ranks in covariance closure.",
            "acceptable_source_evidence": "validator-enforced response/import fields and reviewer package attestations",
            "current_status": "pass",
            "current_evidence": "closure review package and response validator enforce forbidden inputs",
            "blocks_scoring": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(POLICY, rows)
    write_csv(OUT, rows)
    open_blockers = sum(1 for row in rows if row["blocks_scoring"] == "true")
    pass_count = sum(1 for row in rows if row["current_status"] == "pass")
    write_csv(
        SUMMARY,
        [
            {
                "gate_id": "JOINT_CROSS_PROBE_COVARIANCE_SOURCE_REQUIREMENTS_V1",
                "requirement_count": str(len(rows)),
                "pass_count": str(pass_count),
                "open_or_partial_blockers": str(open_blockers),
                "covariance_product_route_ready": "false",
                "independence_rationale_route_ready": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "verdict": "JOINT_CROSS_PROBE_COVARIANCE_SOURCE_REQUIREMENTS_FROZEN_BLOCKED_NOT_SCORING",
                "next_required_action": "obtain_completed_closure_review_or_source_cross_probe_covariance_product",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    DOC.write_text(
        "\n".join(
            [
                "# Joint cross-probe covariance source requirements v1",
                "",
                "**Doc class:** source-side requirements gate",
                "**Status:** not scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This gate freezes the source-side requirements needed before Paper10",
                "can promote the best-justified joint kernel into a single covariance-aware",
                "joint replay. It does not compute a likelihood, score, or validation result.",
                "",
                "Two closure routes remain possible:",
                "",
                "1. a source-native/source-frozen cross-probe covariance product;",
                "2. a reviewer-accepted caveated block-diagonal independence rationale.",
                "",
                "Current verdict:",
                "",
                "`JOINT_CROSS_PROBE_COVARIANCE_SOURCE_REQUIREMENTS_FROZEN_BLOCKED_NOT_SCORING`",
                "",
                "The blocker remains open because no source-frozen cross-probe covariance",
                "product and no completed independence rationale is currently available.",
                "",
            ]
        )
    )
    print(
        "JOINT_CROSS_PROBE_COVARIANCE_SOURCE_REQUIREMENTS_V1_BUILT "
        "verdict=JOINT_CROSS_PROBE_COVARIANCE_SOURCE_REQUIREMENTS_FROZEN_BLOCKED_NOT_SCORING"
    )


if __name__ == "__main__":
    main()
