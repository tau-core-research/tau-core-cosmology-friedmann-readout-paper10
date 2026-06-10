#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_v2_projection_morphology_policy.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_projection_morphology_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_projection_morphology_gate_v1_summary.csv"

REQUIRED_COMPONENTS = {
    "V2_VOID_MORPHOLOGY",
    "V2_WEB_MORPHOLOGY",
    "V2_OBSERVER_PATH_PROJECTION",
    "V2_TIME_READOUT_PROJECTION",
    "V2_CMB_SAFETY",
    "V2_MULTI_CHANNEL_COUPLING",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def artifact_exists_list(value: str) -> tuple[int, int]:
    paths = [item.strip() for item in value.split(";") if item.strip()]
    existing = sum(1 for item in paths if (ROOT / item).exists())
    return existing, len(paths)


def main() -> None:
    policy_rows = read_rows(POLICY)
    component_ids = {row["component_id"] for row in policy_rows}
    if component_ids != REQUIRED_COMPONENTS:
        raise SystemExit(f"unexpected V2 component set: {sorted(component_ids)}")

    gate_rows: list[dict[str, str]] = []
    ready_count = 0
    blocking_components: list[str] = []
    existing_artifacts_total = 0
    artifact_refs_total = 0
    for row in policy_rows:
        existing, total = artifact_exists_list(row["current_source_artifacts"])
        existing_artifacts_total += existing
        artifact_refs_total += total
        source_available = existing == total and total > 0
        replay_ready = row["current_status"] == "SOURCE_READY_FOR_REFINED_ENDPOINT"
        if source_available and replay_ready:
            gate_status = "READY"
            ready_count += 1
        elif source_available:
            gate_status = "SOURCE_PRESENT_BUT_NOT_ENDPOINT_READY"
            blocking_components.append(row["component_id"])
        else:
            gate_status = "SOURCE_MISSING_OR_PARTIAL"
            blocking_components.append(row["component_id"])
        gate_rows.append(
            {
                "gate_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_PROJECTION_MORPHOLOGY_GATE_V1",
                "component_id": row["component_id"],
                "channel_id": row["channel_id"],
                "component_family": row["component_family"],
                "source_role": row["source_role"],
                "current_status": row["current_status"],
                "source_artifacts_existing": str(existing),
                "source_artifacts_declared": str(total),
                "source_available": str(source_available).lower(),
                "gate_status": gate_status,
                "minimum_next_artifact": row["minimum_next_artifact"],
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "forbidden_inputs": row["forbidden_inputs"],
                "null_control": row["null_control"],
                "claim_boundary": row["claim_boundary"],
            }
        )

    all_components_tracked = set(row["component_id"] for row in gate_rows) == REQUIRED_COMPONENTS
    endpoint_ready = ready_count == len(REQUIRED_COMPONENTS)
    summary = [
        {
            "gate_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_PROJECTION_MORPHOLOGY_GATE_V1",
            "status": "V2_PROJECTION_MORPHOLOGY_SOURCE_BASIS_DECLARED_ENDPOINT_BLOCKED",
            "components_required": str(len(REQUIRED_COMPONENTS)),
            "components_tracked": str(len(gate_rows)),
            "all_components_tracked": str(all_components_tracked).lower(),
            "components_ready": str(ready_count),
            "components_blocking": str(len(blocking_components)),
            "blocking_component_ids": ";".join(blocking_components),
            "source_artifacts_existing": str(existing_artifacts_total),
            "source_artifacts_declared": str(artifact_refs_total),
            "endpoint_replay_allowed": str(endpoint_ready).lower(),
            "endpoint_validation_claimed": "false",
            "verdict": (
                "all_projection_morphology_components_ready_for_separate_authorization"
                if endpoint_ready
                else "missing_projection_morphology_components_accounted_endpoint_still_blocked"
            ),
            "recommended_next_action": (
                "request_separate_endpoint_authorization"
                if endpoint_ready
                else "freeze_missing_v2_source_values_before_any_new_endpoint"
            ),
            "claim_boundary": "void_source_basis_refinement_v2_projection_morphology_gate_not_scoring_not_validation",
        }
    ]
    write_csv(OUT, gate_rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_V2_PROJECTION_MORPHOLOGY_GATE_V1_BUILT "
        f"components_ready={ready_count}/{len(REQUIRED_COMPONENTS)} endpoint_replay_allowed={summary[0]['endpoint_replay_allowed']}"
    )


if __name__ == "__main__":
    main()
