#!/usr/bin/env python3
"""Build one consolidated row-level penalized T_joint endpoint authorization package.

This package intentionally replaces the previous micro-gate sequence with one
review artifact.  It does not compute penalized scores and does not authorize
validation by itself.  A completed response may authorize a later frozen
record-only penalized ledger and one guarded endpoint-scoring replay.
"""

from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
SOURCE_MANIFEST = ROOT / "data" / "source_manifest"
DOCS = ROOT / "docs"

PACKAGE_ID = "joint_row_level_penalized_t_joint_endpoint_authorization_review_package_v1"

REQUIRED_INPUTS = [
    DERIVED / "joint_numeric_t_joint_ledger_v1_summary.csv",
    DERIVED / "joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv",
    DERIVED / "joint_row_level_aligned_control_values_v1_summary.csv",
    DERIVED / "joint_row_level_numeric_lambda_blocker_status_v1_summary.csv",
    DERIVED / "joint_row_level_numeric_lambda_review_response_v1_summary.csv",
    DERIVED / "joint_row_level_scoring_readiness_v1_summary.csv",
]

OUTPUTS = {
    "policy": SOURCE_MANIFEST
    / "joint_row_level_penalized_t_joint_endpoint_authorization_policy_v1.csv",
    "template": DERIVED
    / "joint_row_level_penalized_t_joint_endpoint_authorization_response_template_v1.csv",
    "manifest": DERIVED / f"{PACKAGE_ID}_manifest.csv",
    "summary": DERIVED / f"{PACKAGE_ID}_summary.csv",
    "zip": DERIVED / f"{PACKAGE_ID}.zip",
    "sha": DERIVED / f"{PACKAGE_ID}.zip.sha256",
    "doc": DOCS / f"{PACKAGE_ID}.md",
}


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise SystemExit(f"Expected exactly one row in {path}, got {len(rows)}")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assert_inputs() -> dict[str, dict[str, str]]:
    missing = [str(path) for path in REQUIRED_INPUTS if not path.exists()]
    if missing:
        raise SystemExit("Missing required inputs:\n" + "\n".join(missing))
    data = {path.name: read_one(path) for path in REQUIRED_INPUTS}

    readiness = data["joint_row_level_scoring_readiness_v1_summary.csv"]
    if readiness.get("aligned_control_values_ready") != "true":
        raise SystemExit("Aligned control values are not marked ready.")
    if readiness.get("numeric_lambda_ready") != "true":
        raise SystemExit("Numeric lambda is not marked ready.")
    if readiness.get("t_joint_rescoring_authorized") != "false":
        raise SystemExit("This package expects T_joint rescoring to still be unauthorized.")

    blocker = data["joint_row_level_numeric_lambda_blocker_status_v1_summary.csv"]
    if blocker.get("lambda_row_numeric_value_authorized") != "true":
        raise SystemExit("Numeric lambda value is not authorized.")
    if blocker.get("t_joint_rescoring_authorized") != "false":
        raise SystemExit("Numeric-lambda blocker unexpectedly authorizes rescoring.")

    t_joint = data["joint_numeric_t_joint_ledger_v1_summary.csv"]
    if t_joint.get("numeric_t_joint_allowed") != "true":
        raise SystemExit("Base numeric T_joint ledger is not allowed.")
    if t_joint.get("endpoint_scoring_allowed") != "false":
        raise SystemExit("Base T_joint ledger unexpectedly allows endpoint scoring.")

    formula = data["joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv"]
    if formula.get("penalty_formula_defined") != "true":
        raise SystemExit("Symbolic row-level penalty formula is not frozen.")
    if formula.get("uses_endpoint_scores_or_residuals") != "false":
        raise SystemExit("Formula shell reports endpoint-score/residual use.")

    aligned = data["joint_row_level_aligned_control_values_v1_summary.csv"]
    if aligned.get("aligned_control_values_computed") != "true":
        raise SystemExit("Aligned control values are not computed.")
    if aligned.get("endpoint_scoring_allowed") != "false":
        raise SystemExit("Aligned control values unexpectedly allow endpoint scoring.")

    return data


def main() -> None:
    data = assert_inputs()
    SOURCE_MANIFEST.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    readiness = data["joint_row_level_scoring_readiness_v1_summary.csv"]
    blocker = data["joint_row_level_numeric_lambda_blocker_status_v1_summary.csv"]
    t_joint = data["joint_numeric_t_joint_ledger_v1_summary.csv"]
    aligned = data["joint_row_level_aligned_control_values_v1_summary.csv"]
    formula = data["joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv"]

    policy_rows = [
        {
            "policy_id": "ROW_LEVEL_CONSOLIDATED_ENDPOINT_AUTHORIZATION_V1",
            "scope": "one_completed_review_may_authorize_penalized_t_joint_ledger_and_one_guarded_endpoint_scoring_replay",
            "allowed_if_accepted": "compute_T_joint_penalized_record_only;run_one_frozen_endpoint_scoring_replay",
            "not_allowed": "formula_changes;label_changes;source_proxy_changes;post_score_retuning;validation_claims",
            "forbidden_endpoint_fields": "endpoint_residuals;endpoint_scores;fit_improvements;posterior_chains;post_score_control_ranks",
            "claim_boundary": "authorization_package_only_not_scoring_not_validation",
        }
    ]
    write_csv(OUTPUTS["policy"], policy_rows, list(policy_rows[0].keys()))

    template_rows = [
        {
            "review_id": PACKAGE_ID,
            "question_id": "Q1",
            "question": "Do the upstream frozen artifacts support a consolidated authorization gate?",
            "required_response": "accept_or_reject",
            "default_response": "REVIEW_REQUIRED",
            "acceptance_condition": "Base T_joint ledger, row-level formula shell, aligned controls, and lambda_row=1.0 are accepted as frozen source-side inputs.",
            "response": "",
            "reviewer_notes": "",
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "Q2",
            "question": "Authorize computing a record-only penalized ledger T_joint_penalized = T_joint + lambda_row * P_row?",
            "required_response": "yes_or_no",
            "default_response": "false",
            "acceptance_condition": "No endpoint residuals, endpoint scores, or post-score ranks are used.",
            "response": "",
            "reviewer_notes": "",
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "Q3",
            "question": "Authorize one guarded endpoint-scoring replay using the frozen penalized statistic?",
            "required_response": "yes_or_no",
            "default_response": "false",
            "acceptance_condition": "The replay changes no labels, kernels, source proxies, amplitudes, or covariance policy after this review.",
            "response": "",
            "reviewer_notes": "",
        },
        {
            "review_id": PACKAGE_ID,
            "question_id": "Q4",
            "question": "Confirm that validation, cosmological validation, and physical-validation claims remain forbidden?",
            "required_response": "yes_or_no",
            "default_response": "true",
            "acceptance_condition": "The result, if run, is reported as guarded endpoint scoring / preflight evidence only.",
            "response": "",
            "reviewer_notes": "",
        },
    ]
    write_csv(OUTPUTS["template"], template_rows, list(template_rows[0].keys()))

    summary_rows = [
        {
            "package_id": PACKAGE_ID,
            "base_t_joint": t_joint.get("numeric_t_joint", ""),
            "lambda_row_numeric_value": blocker.get("lambda_row_numeric_value", ""),
            "aligned_control_rows": aligned.get("aligned_control_rows", ""),
            "P_row_control_mean": aligned.get("P_row_control_mean", ""),
            "future_score_shell": formula.get("future_score_shell", ""),
            "review_completed": "false",
            "penalized_t_joint_ledger_authorized": "false",
            "endpoint_scoring_authorized": "false",
            "endpoint_scoring_run": "false",
            "endpoint_validation_claimed": "false",
            "cosmological_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "contains_endpoint_residuals": "false",
            "contains_new_endpoint_scores": "false",
            "contains_fit_statistics": "false",
            "readiness_verdict_before_package": readiness.get("verdict", ""),
            "verdict": "CONSOLIDATED_ENDPOINT_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED_NOT_SCORING",
            "next_required_action": "external_reviewer_completes_single_consolidated_authorization_response_before_any_penalized_scoring",
            "claim_boundary": "consolidated_authorization_package_not_scoring_not_validation",
        }
    ]
    write_csv(OUTPUTS["summary"], summary_rows, list(summary_rows[0].keys()))

    manifest_rows = []
    package_files = [
        OUTPUTS["policy"],
        OUTPUTS["template"],
        OUTPUTS["summary"],
        *REQUIRED_INPUTS,
    ]
    for path in package_files:
        rel = path.relative_to(ROOT)
        manifest_rows.append(
            {
                "package_id": PACKAGE_ID,
                "path": str(rel),
                "sha256": sha256(path),
                "role": "included_authorization_material",
                "contains_endpoint_scores": "false",
                "contains_endpoint_residuals": "false",
                "contains_fit_statistics": "false",
            }
        )
    write_csv(OUTPUTS["manifest"], manifest_rows, list(manifest_rows[0].keys()))

    doc = f"""# Consolidated row-level penalized T_joint endpoint authorization package

This reviewer package collapses the previous row-level micro-gates into one
authorization artifact.  It is intended to reduce review overhead while keeping
the leakage boundary explicit.

It does **not** compute `T_joint_penalized`, does **not** run endpoint scoring,
and does **not** claim validation.  If completed and accepted by an external
reviewer, it may authorize exactly two downstream actions:

1. compute a record-only `T_joint_penalized = T_joint + lambda_row * P_row`
   ledger under the already frozen row-level formula;
2. run one guarded endpoint-scoring replay using that frozen statistic.

The package freezes:

- base `T_joint = {t_joint.get('numeric_t_joint', '')}`;
- `lambda_row = {blocker.get('lambda_row_numeric_value', '')}`;
- aligned control rows = {aligned.get('aligned_control_rows', '')};
- mean aligned control penalty = {aligned.get('P_row_control_mean', '')}.

Forbidden inputs remain endpoint residuals, endpoint scores, fit improvements,
posterior chains, and post-score control ranks.  No labels, kernels, source
proxies, amplitudes, or covariance policy may be changed after this package is
accepted.

The claim boundary is:

```text
consolidated_authorization_package_not_scoring_not_validation
```
"""
    OUTPUTS["doc"].write_text(doc, encoding="utf-8")

    zip_path = OUTPUTS["zip"]
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in [OUTPUTS["doc"], OUTPUTS["manifest"], *package_files]:
            archive.write(path, path.relative_to(ROOT))

    digest = sha256(zip_path)
    OUTPUTS["sha"].write_text(f"{digest}  {zip_path.name}\n", encoding="utf-8")
    print(zip_path)
    print(digest)


if __name__ == "__main__":
    main()
