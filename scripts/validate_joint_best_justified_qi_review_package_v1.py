#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "data/source_manifest/joint_best_justified_qi_review_requirements_v1.csv"
DOC = ROOT / "docs/joint_best_justified_qi_review_package_v1.md"

REQUIRED_IDS = {
    "QI_REVIEW_01_SOURCE_GATES",
    "QI_REVIEW_02_KIDS_COSEBIS",
    "QI_REVIEW_03_OBSERVER_PATH",
    "QI_REVIEW_04_DESI_SHAPE",
    "QI_REVIEW_05_ZERO_SUPPORT_BRANCHES",
    "QI_REVIEW_06_EXPONENT_POLICY",
    "QI_REVIEW_07_PROMOTION_RULE",
}

FORBIDDEN_FIELDS = {
    "endpoint_residuals",
    "fit_improvements",
    "posterior_chains",
    "post_score_control_ranks",
}


def main() -> None:
    if not REQUIREMENTS.exists():
        raise SystemExit(f"missing {REQUIREMENTS.relative_to(ROOT)}")
    if not DOC.exists():
        raise SystemExit(f"missing {DOC.relative_to(ROOT)}")

    with REQUIREMENTS.open(newline="") as f:
        rows = list(csv.DictReader(f))
    ids = {row["requirement_id"] for row in rows}
    if ids != REQUIRED_IDS:
        raise SystemExit(f"unexpected requirement ids: {sorted(ids)}")
    for row in rows:
        if row["endpoint_scoring_allowed"] != "false":
            raise SystemExit(f"{row['requirement_id']} allows endpoint scoring")
        if row["endpoint_validation_claimed"] != "false":
            raise SystemExit(f"{row['requirement_id']} claims endpoint validation")
        if row["cosmological_validation_claimed"] != "false":
            raise SystemExit(f"{row['requirement_id']} claims cosmological validation")
        forbidden = set(row["forbidden_inputs"].split(";"))
        if forbidden != FORBIDDEN_FIELDS:
            raise SystemExit(f"{row['requirement_id']} has unexpected forbidden fields: {forbidden}")
        if row["claim_boundary"] != "qi_review_source_side_only_not_scoring":
            raise SystemExit(f"{row['requirement_id']} has unexpected claim boundary")

    doc_text = DOC.read_text()
    for phrase in [
        "SOURCE_SIDE_REVIEW_PACKAGE_NOT_SCORING",
        "does not compute new endpoint scores",
        "covariance-aware joint likelihood prototype",
    ]:
        if phrase not in doc_text:
            raise SystemExit(f"missing phrase in doc: {phrase}")
    print("joint best-justified Q_i review package v1 valid")


if __name__ == "__main__":
    main()
