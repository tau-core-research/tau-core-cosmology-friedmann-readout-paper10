#!/usr/bin/env python3
"""Build a guarded replay package for the caveated ACT K_path route.

This package is prepared only after replay-package authorization review.  It is
still not a replay execution and not validation.
"""

from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
PACKAGE_ID = "ACT_DR6_LENSING_CAVEATED_KPATH_GUARDED_REPLAY_PACKAGE_V1"
CLAIM_BOUNDARY = "act_dr6_lensing_caveated_kpath_guarded_replay_package_not_scoring"

AUTH_SUMMARY = DERIVED / "act_dr6_lensing_caveated_kpath_replay_authorization_review_response_v1_summary.csv"
OUT_ZIP = DERIVED / "act_dr6_lensing_caveated_kpath_guarded_replay_package_v1.zip"
OUT_ZIP_SHA256 = DERIVED / "act_dr6_lensing_caveated_kpath_guarded_replay_package_v1.zip.sha256"
MANIFEST = DERIVED / "act_dr6_lensing_caveated_kpath_guarded_replay_package_v1_manifest.csv"
SUMMARY = DERIVED / "act_dr6_lensing_caveated_kpath_guarded_replay_package_v1_summary.csv"
RUN_INSTRUCTIONS = DERIVED / "act_dr6_lensing_caveated_kpath_guarded_replay_run_instructions_v1.md"

PACKAGE_FILES = [
    "data/derived/act_dr6_lensing_caveated_kpath_replay_authorization_review_response_v1_summary.csv",
    "data/derived/act_dr6_lensing_caveated_kpath_replay_authorization_review_response_v1.csv",
    "data/source_manifest/act_dr6_lensing_caveated_kpath_source_design_v1.csv",
    "data/derived/act_dr6_lensing_caveated_kpath_source_design_v1_summary.csv",
    "data/derived/act_dr6_lensing_path_weight_candidate_v1.csv",
    "data/derived/act_dr6_lensing_path_weight_candidate_v1_summary.csv",
    "data/source_manifest/act_dr6_lensing_path_weight_replay_run_template_v1.csv",
    "data/derived/act_dr6_lensing_path_weight_replay_run_template_v1_summary.csv",
    "scripts/run_act_dr6_lensing_path_weight_authorized_replay_v1.py",
    "scripts/validate_act_dr6_lensing_path_weight_authorized_replay_v1.py",
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise RuntimeError(f"expected one row in {path.relative_to(ROOT)}")
    return rows[0]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def manifest_row(rel: str) -> dict[str, str]:
    path = ROOT / rel
    if not path.exists():
        raise SystemExit(f"missing guarded replay package file: {rel}")
    return {
        "package_id": PACKAGE_ID,
        "package_path": rel,
        "byte_count": str(path.stat().st_size),
        "sha256": sha256(path),
        "contains_endpoint_residuals": "false",
        "contains_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "endpoint_replay_executed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    auth = read_one(AUTH_SUMMARY)
    if auth["permission_only_guarded_replay_package_preparation_allowed"] != "true":
        raise SystemExit("guarded replay package preparation is not authorized")
    if auth["endpoint_replay_allowed_by_this_review"] != "false":
        raise SystemExit("authorization response must not directly allow endpoint replay")

    RUN_INSTRUCTIONS.write_text(
        "\n".join(
            [
                "# ACT DR6 caveated K_path guarded replay package v1",
                "",
                "This package is a prepared run bundle, not a replay execution.",
                "",
                "The allowed next action is to run the guarded replay only as a",
                "permission-only endpoint diagnostic with all controls retained.",
                "",
                "Required controls:",
                "",
                "- off",
                "- baseline_only",
                "- curl_null",
                "- diff_f150_f090_null",
                "- wrong_sign",
                "- deterministic_shuffle",
                "- rank_reverse",
                "- source_basis_recenter_stress, if implemented as a frozen stress",
                "",
                "Forbidden claims:",
                "",
                "- validation",
                "- physical K_path promotion",
                "- dark-sector inference",
                "- family verdict",
                "",
                f"Claim boundary: `{CLAIM_BOUNDARY}`.",
                "",
            ]
        )
    )

    rows = [manifest_row(rel) for rel in PACKAGE_FILES]
    rows.append(manifest_row(str(RUN_INSTRUCTIONS.relative_to(ROOT))))
    write_csv(MANIFEST, rows)
    zip_rows = rows + [manifest_row(str(MANIFEST.relative_to(ROOT)))]

    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for row in zip_rows:
            path = ROOT / row["package_path"]
            info = zipfile.ZipInfo(row["package_path"])
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())

    zip_hash = sha256(OUT_ZIP)
    OUT_ZIP_SHA256.write_text(f"{zip_hash}  {OUT_ZIP.name}\n")
    write_csv(
        SUMMARY,
        [
            {
                "package_id": PACKAGE_ID,
                "status": "GUARDED_REPLAY_PACKAGE_READY_NOT_EXECUTED",
                "authorization_verdict": auth["verdict"],
                "zip_path": str(OUT_ZIP.relative_to(ROOT)),
                "zip_sha256_path": str(OUT_ZIP_SHA256.relative_to(ROOT)),
                "zip_sha256": zip_hash,
                "package_file_count": str(len(zip_rows)),
                "endpoint_replay_executed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "dark_sector_inference_allowed": "false",
                "family_verdict_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": "ACT_CAVEATED_KPATH_GUARDED_REPLAY_PACKAGE_READY_NOT_EXECUTED",
            }
        ],
    )


if __name__ == "__main__":
    main()
