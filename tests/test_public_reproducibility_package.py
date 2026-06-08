from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_files_exist() -> None:
    required = [
        "README.md",
        "DATA_NOTICE.md",
        "CITATION.cff",
        "LICENSE",
        "paper10_submission_source/main.tex",
        "paper10_submission_source/refs.bib",
        "paper10_submission_source/main.pdf",
        "arxiv_submission_source.zip",
        "data/derived/audit_gate_inventory.csv",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_manuscript_claim_markers() -> None:
    text = (ROOT / "paper10_submission_source/main.tex").read_text()
    assert "A source-frozen Friedmann-readout audit protocol" in text
    assert "does not claim that Tau Core" in text
    assert "explains dark energy" in text
    assert "Lambda-like distance behavior" in text
    assert "web/environment-dependent growth or lensing residual" in text
    forbidden = [
        "we detect Tau Core",
        "we prove Tau Core explains dark energy",
        "we replace Lambda-CDM",
        "validated physical model",
    ]
    lower = text.lower()
    for phrase in forbidden:
        assert phrase.lower() not in lower


def test_arxiv_zip_is_source_only() -> None:
    zip_path = ROOT / "arxiv_submission_source.zip"
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    assert "main.tex" in names
    assert "refs.bib" in names
    assert "main.pdf" not in names
    assert not any(name.endswith(".aux") for name in names)


def test_gate_inventory_is_protocol_only() -> None:
    with (ROOT / "data/derived/audit_gate_inventory.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 6
    assert {row["status"] for row in rows} == {"planned"}
    forbidden_blob = " ".join(row["forbidden_inputs"] for row in rows)
    assert "target_residuals" in forbidden_blob
    assert "endpoint_tuned_labels" in forbidden_blob
