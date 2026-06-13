#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQ = ROOT / "data/source_manifest/full_observer_path_kernel_source_requirements_v1.csv"
GATE = ROOT / "data/derived/observer_path_strengthening_gate_v1.csv"
GATE_SUMMARY = ROOT / "data/derived/observer_path_strengthening_gate_v1_summary.csv"
ROUTE_AUDIT = ROOT / "data/derived/low_z_pantheon_metric_lensing_path_route_audit_v1.csv"
DOC = ROOT / "docs/observer_path_metric_product_requirements_package_v1.md"
INSTRUCTIONS = ROOT / "docs/observer_path_metric_product_requirements_reviewer_instructions_v1.md"
TEMPLATE = ROOT / "data/derived/observer_path_metric_product_requirements_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/observer_path_metric_product_requirements_package_v1.zip"
MANIFEST = ROOT / "data/derived/observer_path_metric_product_requirements_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/observer_path_metric_product_requirements_package_v1_summary.csv"
SHA = ROOT / "data/derived/observer_path_metric_product_requirements_package_v1.zip.sha256"
CLAIM_BOUNDARY = "observer_path_metric_product_requirements_not_endpoint_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    req_rows = read_rows(REQ)
    r5 = next(row for row in req_rows if row["requirement_id"] == "R5")
    gate_summary = read_one(GATE_SUMMARY)
    gate_rows = read_rows(GATE)
    metric_route = next(row for row in gate_rows if row["route_id"] == "metric_lensing_path_weight")
    route_rows = read_rows(ROUTE_AUDIT)

    if r5["endpoint_replay_allowed"] != "false":
        raise SystemExit("R5 must not authorize endpoint replay")
    if metric_route["route_status"] != "BLOCKED_FOR_ENDPOINT_UNTIL_SOURCE_ALIGNED_NUMERIC_PRODUCT":
        raise SystemExit("metric route must remain blocked before this package")
    if gate_summary["metric_path_source_aligned_numeric_count"] != "0":
        raise SystemExit("current gate must have zero source-aligned metric products")

    statuses = sorted({row["path_weight_value_status"] for row in route_rows})
    status_counts = {
        status: sum(row["path_weight_value_status"] == status for row in route_rows)
        for status in statuses
    }
    blocked_count = sum(
        row["path_weight_value_status"] == "BLOCKED_NO_SOURCE_ALIGNED_METRIC_LENSING_PRODUCT"
        for row in route_rows
    )
    numeric_count = sum(
        row["metric_lensing_numeric_product_available_for_source"] == "true"
        for row in route_rows
    )

    doc = f"""# Observer/path metric-product requirements package v1

**Doc class:** source-product requirements package
**Status:** not endpoint replay; not validation

The observer/path strengthening gate identifies the quickest non-lensing
fragility route, but it also blocks the physical metric/lensing path branch.
The block is narrow: the current 12-object scope has no source-aligned numeric
convergence, shear, mass-map integral, or metric/lensing path product.

This package asks an external reviewer to evaluate only the source-product
requirements for reopening that route. It does not authorize endpoint scoring.

Required product family:

- one row per source object in the active observer/path scope, with the same
  rule applicable to the wider low-z route-audit universe when promoted,
- a source-aligned numeric metric/path observable such as kappa, shear,
  projected mass-map integral, or documented null-geodesic/metric-environment
  path weight,
- provenance for the map/catalogue, coordinate match, mask/coverage status, and
  any normalization rule,
- no use of Pantheon residuals, endpoint scores, fitted distance residuals, or
  post-hoc selection by improvement.

Current blocker evidence:

- R5 requirement: `{r5['required_source_observable']}`
- metric route status: `{metric_route['route_status']}`
- source-aligned metric count: `{gate_summary['metric_path_source_aligned_numeric_count']}`
- route-audit numeric count: `{numeric_count}`
- route-audit rows: `{len(route_rows)}`
- active observer/path scope rows: `{gate_summary['metric_path_scope_rows']}`
- blocked rows: `{blocked_count}`
- route-audit statuses: `{status_counts}`

Allowed reviewer outcomes:

- `ACCEPT_REQUIREMENTS_ONLY`: requirements are sufficient for a future
  acquisition/freeze package, but no replay is authorized.
- `REQUEST_SOURCE_PRODUCT_DETAIL`: reviewer needs a more specific map/catalogue
  and coordinate/mask policy.
- `REJECT_AS_ENDPOINT_LEAKAGE_RISK`: requirements would allow residual or
  endpoint leakage.

Claim boundary: `{CLAIM_BOUNDARY}`.
"""
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(doc)

    instructions = f"""# External reviewer instructions: observer/path metric product requirements v1

You do not need repository access for this review. Use only the files included
in this zip package.

## What you are reviewing

This package does **not** ask whether Tau Core is correct and does **not**
authorize endpoint scoring. It asks only whether the stated source-product
requirements are sufficient to acquire or construct a future observer/path
metric-product without endpoint leakage.

The current blocker is:

- active observer/path scope rows: `{gate_summary['metric_path_scope_rows']}`
- wider low-z route-audit rows: `{len(route_rows)}`
- source-aligned numeric metric/path products currently available: `0`
- endpoint replay allowed: `false`
- validation claimed: `false`

## Files to inspect

1. `docs/observer_path_metric_product_requirements_package_v1.md`
   - Plain-language summary of the blocker and allowed outcomes.
2. `data/source_manifest/full_observer_path_kernel_source_requirements_v1.csv`
   - Full source requirements; focus especially on `R5`.
3. `data/derived/observer_path_strengthening_gate_v1.csv`
   - Route-level gate showing that the physical metric/lensing path branch is
     blocked until a source-aligned numeric product exists.
4. `data/derived/observer_path_strengthening_gate_v1_summary.csv`
   - One-row summary of the current blocker.
5. `data/derived/low_z_pantheon_metric_lensing_path_route_audit_v1.csv`
   - Wider low-z route audit; this documents that the current audit has no
     source-aligned numeric kappa/shear/mass-map/path-weight product.
6. `data/derived/observer_path_metric_product_requirements_review_response_template_v1.csv`
   - Fill this file and return it.

## Allowed reviewer responses

Use one of these outcomes in `reviewer_response` for each row:

- `ACCEPT_REQUIREMENTS_ONLY`
- `REQUEST_SOURCE_PRODUCT_DETAIL`
- `REJECT_AS_ENDPOINT_LEAKAGE_RISK`

## Required safety checks

Please leave or set these fields as:

- `forbidden_inputs_used=false`
- `endpoint_replay_allowed=false`
- `endpoint_validation_claimed=false`
- `physical_lensing_path_weight_claimed=false`

If any requirement would permit use of Pantheon residuals, fitted distance
residuals, endpoint scores, or post-hoc selection by improvement, mark the
relevant row as `REJECT_AS_ENDPOINT_LEAKAGE_RISK` and explain why.

## What would count as a useful future source product

A future acquisition/freeze package should provide, per source object, at least
one independently sourced numeric metric/path observable such as:

- convergence (`kappa`),
- shear,
- projected mass-map integral,
- documented null-geodesic or metric-environment path weight.

It should also document coordinate matching, coverage/mask status, provenance,
and normalization without using endpoint residuals or score improvement.

Claim boundary: `{CLAIM_BOUNDARY}`.
"""
    INSTRUCTIONS.write_text(instructions)

    questions = [
        (
            "Q1_product_specificity",
            "Are the required metric/path observables specific enough to acquire or construct without endpoint residuals?",
        ),
        (
            "Q2_source_alignment",
            "Does the requirement enforce one source-aligned numeric product per observer/path-scope object?",
        ),
        (
            "Q3_leakage_barrier",
            "Does the requirement forbid Pantheon residuals, endpoint scores, fitted residuals, and post-hoc improvement selection?",
        ),
        (
            "Q4_replay_boundary",
            "Should this package remain requirements-only, with endpoint replay disabled until a separate source-product freeze/replay authorization exists?",
        ),
    ]
    template_rows = [
        {
            "question_id": qid,
            "question": question,
            "reviewer_response": "",
            "reviewer_rationale": "",
            "review_completed": "false",
            "allowed_outcome": "ACCEPT_REQUIREMENTS_ONLY|REQUEST_SOURCE_PRODUCT_DETAIL|REJECT_AS_ENDPOINT_LEAKAGE_RISK",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for qid, question in questions
    ]
    write_csv(TEMPLATE, template_rows)

    package_files = [REQ, GATE, GATE_SUMMARY, ROUTE_AUDIT, DOC, INSTRUCTIONS, TEMPLATE]
    with zipfile.ZipFile(PACKAGE, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in package_files:
            arcname = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(arcname)
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    digest = sha256(PACKAGE)
    SHA.write_text(f"{digest}  {PACKAGE.name}\n")
    write_csv(
        MANIFEST,
        [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(path),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for path in package_files
        ],
    )
    write_csv(
        SUMMARY,
        [
            {
                "package_id": "OBSERVER_PATH_METRIC_PRODUCT_REQUIREMENTS_PACKAGE_V1",
                "status": "REQUIREMENTS_PACKAGE_BUILT_NOT_REVIEWED",
                "r5_required_source_observable": r5["required_source_observable"],
                "observer_path_scope_rows": gate_summary["metric_path_scope_rows"],
                "route_audit_rows": str(len(route_rows)),
                "metric_path_source_aligned_numeric_count": gate_summary[
                    "metric_path_source_aligned_numeric_count"
                ],
                "route_audit_numeric_product_count": str(numeric_count),
                "blocked_no_source_aligned_metric_product_count": str(blocked_count),
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "zip_path": PACKAGE.relative_to(ROOT).as_posix(),
                "zip_sha256": digest,
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": "METRIC_PATH_PRODUCT_REQUIREMENTS_READY_FOR_EXTERNAL_REVIEW_NOT_ENDPOINT",
            }
        ],
    )
    print(
        "OBSERVER_PATH_METRIC_PRODUCT_REQUIREMENTS_PACKAGE_V1_BUILT "
        f"observer_scope_rows={gate_summary['metric_path_scope_rows']} route_audit_rows={len(route_rows)} "
        f"metric_count={gate_summary['metric_path_source_aligned_numeric_count']} "
        f"sha256={digest}"
    )


if __name__ == "__main__":
    main()
