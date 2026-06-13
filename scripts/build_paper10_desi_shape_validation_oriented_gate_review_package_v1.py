#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_validation_oriented_gate_review_policy_v1.csv"
REVIEW_DOC = ROOT / "docs/paper10_desi_shape_validation_oriented_gate_review_v1.md"
TEMPLATE = ROOT / "data/derived/paper10_desi_shape_validation_oriented_gate_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/paper10_desi_shape_validation_oriented_gate_review_package_v1.zip"
SHA = ROOT / "data/derived/paper10_desi_shape_validation_oriented_gate_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/paper10_desi_shape_validation_oriented_gate_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_validation_oriented_gate_review_package_v1_summary.csv"
PACKAGE_ID = "PAPER10_DESI_SHAPE_VALIDATION_ORIENTED_GATE_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "paper10_desi_shape_validation_oriented_gate_review_not_replay_not_validation"

PACKAGE_FILES = [
    POLICY,
    REVIEW_DOC,
    TEMPLATE,
    ROOT / "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1_summary.csv",
    ROOT / "docs/paper10_desi_shape_post_synthesis_gate_authorization_review_notes_v1.md",
    ROOT / "data/derived/paper10_desi_shape_route_source_synthesis_review_response_v1_summary.csv",
    ROOT / "data/derived/paper10_desi_shape_core_support_synthesis_gate_v1_summary.csv",
    ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv",
    ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1_summary.csv",
    ROOT / "data/derived/paper10_desi_shape_row2_authorized_replay_v1_summary.csv",
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


def manifest_row(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing review package member: {path.relative_to(ROOT)}")
    contains_scores = path.name.endswith("_summary.csv") and (
        "authorized_replay" in path.name or "robustness_stress" in path.name
    )
    return {
        "package_id": PACKAGE_ID,
        "package_path": path.relative_to(ROOT).as_posix(),
        "byte_count": str(path.stat().st_size),
        "sha256": sha256(path),
        "contains_endpoint_residuals": "false",
        "contains_endpoint_scores": "true" if contains_scores else "false",
        "contains_fit_statistics": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    policy_rows = read_rows(POLICY)
    if len(policy_rows) != 4:
        raise SystemExit("validation-oriented gate review policy must contain four questions")
    if {row["claim_boundary"] for row in policy_rows} != {CLAIM_BOUNDARY}:
        raise SystemExit("bad validation-oriented gate claim boundary")
    for row in policy_rows:
        for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
            if row[field] != "false":
                raise SystemExit(f"policy {field} must remain false")

    post = one_row(ROOT / "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1_summary.csv")
    replay = one_row(ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv")
    robust = one_row(ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1_summary.csv")
    core = one_row(ROOT / "data/derived/paper10_desi_shape_core_support_synthesis_gate_v1_summary.csv")

    if post["prepare_later_authorization_package_allowed"] != "true":
        raise SystemExit("post-synthesis response must allow later authorization package preparation")
    if post["endpoint_replay_allowed"] != "false":
        raise SystemExit("post-synthesis response must not authorize immediate replay")
    if replay["verdict"] != "desi_shape_route_permission_replay_candidate_exceeds_all_controls_not_validation":
        raise SystemExit("route replay verdict mismatch")
    if robust["verdict"] != "positive_but_narrow_margin_and_row_sensitive_not_validation":
        raise SystemExit("robustness verdict mismatch")
    if core["route_interpretation"] != "multi_row_narrow_margin_source_sensitive_signal_not_row2_only":
        raise SystemExit("route interpretation mismatch")

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
                "source_reference_or_url": "",
                "forbidden_inputs_used": "false",
                "post_synthesis_prepare_later_authorization_package_allowed": post["prepare_later_authorization_package_allowed"],
                "route_candidate_score": replay["candidate_shape_quadratic_score"],
                "route_best_control_score": replay["best_control_shape_quadratic_score"],
                "route_margin": replay["delta_candidate_minus_best_control_score"],
                "robustness_verdict": robust["verdict"],
                "route_interpretation": core["route_interpretation"],
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "authorization_scope": "future_one_frozen_DESI_shape_route_permission_replay_only_not_validation",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(TEMPLATE, template_rows)

    rows = [manifest_row(path) for path in PACKAGE_FILES]
    write_csv(MANIFEST, rows)
    package_rows = rows + [manifest_row(MANIFEST)]
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
                "status": "DESI_SHAPE_VALIDATION_ORIENTED_GATE_REVIEW_PACKAGE_BUILT_NOT_COMPLETED",
                "zip_path": PACKAGE.relative_to(ROOT).as_posix(),
                "zip_sha256_path": SHA.relative_to(ROOT).as_posix(),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "post_synthesis_prepare_later_authorization_package_allowed": post["prepare_later_authorization_package_allowed"],
                "route_candidate_score": replay["candidate_shape_quadratic_score"],
                "route_best_control_score": replay["best_control_shape_quadratic_score"],
                "route_margin": replay["delta_candidate_minus_best_control_score"],
                "robustness_verdict": robust["verdict"],
                "route_interpretation": core["route_interpretation"],
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_fit_statistics": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": "validation_oriented_gate_review_package_ready_not_completed_not_replay",
                "recommended_next_action": "send_zip_to_reviewer_for_permission_only_replay_authorization_decision",
            }
        ],
    )
    print(f"PAPER10_DESI_SHAPE_VALIDATION_ORIENTED_GATE_REVIEW_PACKAGE_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
