#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_validation_permission_replay_authorization_review_policy_v1.csv"
ROUTE_SUMMARY = ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv"
ROBUSTNESS_SUMMARY = ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1_summary.csv"
SOURCE_SYNTHESIS_SUMMARY = ROOT / "data/derived/paper10_desi_shape_route_source_synthesis_review_response_v1_summary.csv"
POST_SYNTHESIS_SUMMARY = ROOT / "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1_summary.csv"
VALIDATION_GATE_SUMMARY = ROOT / "data/derived/paper10_desi_shape_validation_oriented_gate_review_response_v1_summary.csv"
TEMPLATE = ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.zip"
SHA = ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1_summary.csv"
PACKAGE_ID = "PAPER10_DESI_SHAPE_VALIDATION_PERMISSION_REPLAY_AUTHORIZATION_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "paper10_desi_shape_validation_permission_replay_authorization_not_validation"

PACKAGE_FILES = [
    "docs/paper10_desi_shape_validation_permission_replay_authorization_review_v1.md",
    "data/source_manifest/paper10_desi_shape_validation_permission_replay_authorization_review_policy_v1.csv",
    "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_template_v1.csv",
    "docs/paper10_desi_shape_validation_oriented_gate_review_v1.md",
    "data/source_manifest/paper10_desi_shape_validation_oriented_gate_review_policy_v1.csv",
    "data/derived/paper10_desi_shape_validation_oriented_gate_review_response_v1.csv",
    "data/derived/paper10_desi_shape_validation_oriented_gate_review_response_v1_summary.csv",
    "data/derived/paper10_desi_shape_validation_oriented_gate_review_completed_summary_v1.csv",
    "docs/paper10_desi_shape_validation_oriented_gate_review_notes_v1.md",
    "docs/paper10_desi_shape_post_synthesis_gate_authorization_review_v1.md",
    "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1.csv",
    "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1_summary.csv",
    "docs/paper10_desi_shape_post_synthesis_gate_authorization_review_notes_v1.md",
    "docs/paper10_desi_shape_route_source_synthesis_review_v1.md",
    "data/derived/paper10_desi_shape_route_source_synthesis_review_response_v1.csv",
    "data/derived/paper10_desi_shape_route_source_synthesis_review_response_v1_summary.csv",
    "docs/paper10_desi_shape_route_source_synthesis_review_notes_v1.md",
    "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv",
    "data/derived/paper10_desi_shape_route_robustness_stress_v1_summary.csv",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_row(rel: str) -> dict[str, str]:
    path = ROOT / rel
    if not path.exists():
        raise SystemExit(f"missing review package member: {rel}")
    return {
        "package_id": PACKAGE_ID,
        "package_path": rel,
        "byte_count": str(path.stat().st_size),
        "sha256": sha256(path),
        "contains_endpoint_residuals": "false",
        "contains_new_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy_rows = read_rows(POLICY)
    require(len(policy_rows) == 4, "validation permission replay policy must contain four questions")
    require({row["claim_boundary"] for row in policy_rows} == {CLAIM_BOUNDARY}, "bad policy claim boundary")

    route = one_row(ROUTE_SUMMARY)
    robustness = one_row(ROBUSTNESS_SUMMARY)
    source_synthesis = one_row(SOURCE_SYNTHESIS_SUMMARY)
    post_synthesis = one_row(POST_SYNTHESIS_SUMMARY)
    validation_gate = one_row(VALIDATION_GATE_SUMMARY)

    require(route["status"] == "DESI_SHAPE_ROUTE_AUTHORIZED_REPLAY_PERMISSION_ONLY_NOT_VALIDATION", "route replay summary must remain permission-only")
    require(robustness["verdict"] == "positive_but_narrow_margin_and_row_sensitive_not_validation", "robustness caveat must remain active")
    require(source_synthesis["future_gate_preparation_allowed"] == "true", "source synthesis must allow only future gate preparation")
    require(source_synthesis["endpoint_replay_allowed"] == "false", "source synthesis must not authorize replay")
    require(post_synthesis["prepare_later_authorization_package_allowed"] == "true", "post-synthesis gate must allow later package preparation")
    require(post_synthesis["endpoint_replay_allowed"] == "false", "post-synthesis gate must not authorize replay")
    require(validation_gate["future_permission_only_replay_preparation_allowed"] == "true", "validation gate must allow only future replay preparation")
    require(validation_gate["endpoint_replay_allowed"] == "false", "validation gate must not authorize replay")
    require(validation_gate["endpoint_validation_claimed"] == "false", "validation gate must not claim validation")
    require(validation_gate["physical_validation_claimed"] == "false", "validation gate must not claim physical validation")
    require(validation_gate["narrow_margin_caveat_retained"] == "true", "narrow-margin caveat must be retained")
    require(validation_gate["row_sensitive_caveat_retained"] == "true", "row-sensitive caveat must be retained")
    require(validation_gate["row2_negative_diagnostic_retained"] == "true", "Row2 negative caveat must be retained")

    template_rows = []
    for row in policy_rows:
        template_rows.append(
            {
                "policy_id": row["policy_id"],
                "question_id": row["question_id"],
                "question_text": row["question_text"],
                "required_response": row["required_response"],
                "acceptance_condition": row["acceptance_condition"],
                "review_completed": "false",
                "reviewer_id_or_role": "",
                "reviewer_response": "",
                "reviewer_rationale": "",
                "forbidden_inputs_used": "false",
                "route_candidate_score": validation_gate["route_candidate_score"],
                "route_best_control_score": validation_gate["route_best_control_score"],
                "route_margin": validation_gate["route_margin"],
                "robustness_verdict": validation_gate["robustness_verdict"],
                "narrow_margin_caveat_retained": validation_gate["narrow_margin_caveat_retained"],
                "row_sensitive_caveat_retained": validation_gate["row_sensitive_caveat_retained"],
                "row2_negative_diagnostic_retained": validation_gate["row2_negative_diagnostic_retained"],
                "future_permission_only_replay_preparation_allowed": validation_gate["future_permission_only_replay_preparation_allowed"],
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "authorization_scope": "one_future_frozen_DESI_shape_route_permission_only_diagnostic_replay_not_validation",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(TEMPLATE, template_rows)

    rows = [manifest_row(rel) for rel in PACKAGE_FILES]
    write_csv(MANIFEST, rows)
    package_rows = rows + [manifest_row(str(MANIFEST.relative_to(ROOT)))]
    with zipfile.ZipFile(PACKAGE, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for row in package_rows:
            path = ROOT / row["package_path"]
            info = zipfile.ZipInfo(row["package_path"])
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    digest = sha256(PACKAGE)
    SHA.write_text(f"{digest}  {PACKAGE.name}\n")
    write_csv(
        SUMMARY,
        [
            {
                "package_id": PACKAGE_ID,
                "status": "DESI_SHAPE_VALIDATION_PERMISSION_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED",
                "zip_path": str(PACKAGE.relative_to(ROOT)),
                "zip_sha256_path": str(SHA.relative_to(ROOT)),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "route_candidate_score": validation_gate["route_candidate_score"],
                "route_best_control_score": validation_gate["route_best_control_score"],
                "route_margin": validation_gate["route_margin"],
                "robustness_verdict": validation_gate["robustness_verdict"],
                "narrow_margin_caveat_retained": validation_gate["narrow_margin_caveat_retained"],
                "row_sensitive_caveat_retained": validation_gate["row_sensitive_caveat_retained"],
                "row2_negative_diagnostic_retained": validation_gate["row2_negative_diagnostic_retained"],
                "future_permission_only_replay_preparation_allowed": validation_gate["future_permission_only_replay_preparation_allowed"],
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "verdict": "validation_permission_replay_authorization_package_ready_not_completed_not_replay",
                "recommended_next_action": "send_zip_to_reviewer_and_validate_completed_authorization_response_before_any_run",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"paper10_desi_shape_validation_permission_replay_authorization_review_package_v1: built sha256={digest}")


if __name__ == "__main__":
    main()
