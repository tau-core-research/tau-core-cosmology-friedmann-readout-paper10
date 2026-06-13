#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_route_replay_authorization_review_policy_v1.csv"
SHAPE_SUMMARY = ROOT / "data/derived/paper10_desi_time_readout_shape_observable_gate_v1_summary.csv"
PROJECTION_SUMMARY = ROOT / "data/derived/paper10_desi_time_readout_shape_projection_induction_v1_summary.csv"
CONTROL_SUMMARY = ROOT / "data/derived/paper10_desi_shape_bound_control_vectors_v1_summary.csv"
CC_WINDOW_SUMMARY = ROOT / "data/derived/paper10_desi_cc_window_stress_binding_v1_summary.csv"
MULTI_CLOCK_SUMMARY = ROOT / "data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1_summary.csv"
HIGH_Z_SUMMARY = ROOT / "data/derived/paper10_desi_high_z_independent_clock_support_audit_v1_summary.csv"
TEMPLATE = ROOT / "data/derived/paper10_desi_shape_route_replay_authorization_review_response_template_v1.csv"
PACKAGE = ROOT / "data/derived/paper10_desi_shape_route_replay_authorization_review_package_v1.zip"
SHA = ROOT / "data/derived/paper10_desi_shape_route_replay_authorization_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/paper10_desi_shape_route_replay_authorization_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_route_replay_authorization_review_package_v1_summary.csv"
PACKAGE_ID = "PAPER10_DESI_SHAPE_ROUTE_REPLAY_AUTHORIZATION_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "paper10_desi_shape_route_replay_authorization_review_not_validation"

PACKAGE_FILES = [
    "docs/paper10_desi_shape_route_replay_authorization_review_v1.md",
    "data/source_manifest/paper10_desi_shape_route_replay_authorization_review_policy_v1.csv",
    "data/derived/paper10_desi_shape_route_replay_authorization_review_response_template_v1.csv",
    "docs/paper10_desi_time_readout_shape_observable_gate_v1.md",
    "data/derived/paper10_desi_time_readout_shape_observable_gate_v1.csv",
    "data/derived/paper10_desi_time_readout_shape_observable_gate_v1_summary.csv",
    "docs/paper10_desi_time_readout_shape_projection_induction_v1.md",
    "data/derived/paper10_desi_time_readout_shape_projection_induction_v1.csv",
    "data/derived/paper10_desi_time_readout_shape_projection_induction_v1_summary.csv",
    "docs/paper10_desi_ordering_control_suite_v1.md",
    "data/derived/paper10_desi_ordering_control_suite_v1.csv",
    "data/derived/paper10_desi_ordering_control_suite_v1_summary.csv",
    "docs/paper10_desi_cc_window_stress_binding_v1.md",
    "data/derived/paper10_desi_cc_window_stress_binding_v1.csv",
    "data/derived/paper10_desi_cc_window_stress_binding_v1_summary.csv",
    "docs/paper10_desi_shape_bound_control_vectors_v1.md",
    "data/derived/paper10_desi_shape_bound_control_vectors_v1.csv",
    "data/derived/paper10_desi_shape_bound_control_vectors_v1_summary.csv",
    "docs/paper10_desi_multi_clock_support_per_bao_row_audit_v1.md",
    "data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1.csv",
    "data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1_summary.csv",
    "docs/paper10_desi_high_z_independent_clock_support_audit_v1.md",
    "data/derived/paper10_desi_high_z_independent_clock_support_audit_v1_summary.csv",
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
        "contains_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    policy_rows = read_rows(POLICY)
    if len(policy_rows) != 4:
        raise SystemExit("shape-route replay authorization policy must contain four questions")
    if {row["claim_boundary"] for row in policy_rows} != {CLAIM_BOUNDARY}:
        raise SystemExit("bad policy claim boundary")
    shape = one_row(SHAPE_SUMMARY)
    projection = one_row(PROJECTION_SUMMARY)
    controls = one_row(CONTROL_SUMMARY)
    cc_window = one_row(CC_WINDOW_SUMMARY)
    multi_clock = one_row(MULTI_CLOCK_SUMMARY)
    high_z = one_row(HIGH_Z_SUMMARY)
    if shape["shape_observable_candidate_available"] != "true":
        raise SystemExit("shape candidate must exist before replay authorization review")
    if projection["primary_candidate"] != "CLOCK_SLOPE_SHAPE":
        raise SystemExit("projection ledger must identify CLOCK_SLOPE_SHAPE as primary")
    if controls["shape_bound_control_count"] != "5" or controls["unbound_control_families"] != "none":
        raise SystemExit("shape-route controls must be fully bound before replay authorization review")
    if cc_window["cc_window_stress_release_policy"] != "SOURCE_REOPEN_ONLY_NO_REPLAY":
        raise SystemExit("CC-window stress must remain caveated no-replay")
    if high_z["high_z_row_can_enter_replay"] != "false":
        raise SystemExit("high-z row must remain excluded")

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
                "shape_observable_candidate_available": shape["shape_observable_candidate_available"],
                "primary_candidate": projection["primary_candidate"],
                "shape_bound_control_count": controls["shape_bound_control_count"],
                "unbound_control_families": controls["unbound_control_families"],
                "cc_window_stress_release_policy": cc_window["cc_window_stress_release_policy"],
                "multi_clock_support_endpoint_ready": multi_clock["multi_clock_support_endpoint_ready"],
                "high_z_row_can_enter_replay": high_z["high_z_row_can_enter_replay"],
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "authorization_scope": "one_permission_only_DESI_shape_route_replay_later_not_validation",
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
                "status": "DESI_SHAPE_ROUTE_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED",
                "zip_path": str(PACKAGE.relative_to(ROOT)),
                "zip_sha256_path": str(SHA.relative_to(ROOT)),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "shape_observable_candidate_available": shape["shape_observable_candidate_available"],
                "primary_candidate": projection["primary_candidate"],
                "shape_bound_control_count": controls["shape_bound_control_count"],
                "unbound_control_families": controls["unbound_control_families"],
                "cc_window_stress_release_policy": cc_window["cc_window_stress_release_policy"],
                "multi_clock_support_endpoint_ready": multi_clock["multi_clock_support_endpoint_ready"],
                "high_z_row_can_enter_replay": high_z["high_z_row_can_enter_replay"],
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "verdict": "desi_shape_route_replay_authorization_package_ready_not_completed",
                "recommended_next_action": "send_zip_to_reviewer_and_validate_completed_authorization_response",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"paper10_desi_shape_route_replay_authorization_review_package_v1: built sha256={digest}")


if __name__ == "__main__":
    main()
