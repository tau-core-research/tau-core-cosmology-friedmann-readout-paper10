#!/usr/bin/env python3
from __future__ import annotations

import csv
import gzip
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/kids1000_cosebis_null_control_theory_replay_policy_v1.csv"
SEEDS = ROOT / "data/derived/kids1000_cosebis_null_control_seed_inventory_v1.csv"
THEORY = ROOT / "data/derived/kids1000_cosebis_source_frozen_theory_vector_v1.csv"
OUT = ROOT / "data/derived/kids1000_cosebis_null_control_row_vectors_v1.csv.gz"
SUMMARY = ROOT / "data/derived/kids1000_cosebis_null_control_row_vectors_v1_summary.csv"
DOC = ROOT / "docs/kids1000_cosebis_null_control_row_vectors_v1.md"


CLAIM_BOUNDARY = "kids1000_cosebis_null_control_row_vectors_not_scoring_not_validation"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "wt", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_pair_order(theory_rows: list[dict[str, str]]) -> list[str]:
    pair_order: list[str] = []
    for row in theory_rows:
        pair_id = row["pair_id"]
        if pair_id not in pair_order:
            pair_order.append(pair_id)
    if len(pair_order) != 15:
        raise SystemExit(f"expected 15 tomographic pairs, got {len(pair_order)}")
    return pair_order


def vector_stats(values: list[float]) -> dict[str, str]:
    mean = sum(values) / len(values)
    return {
        "min_control_value": f"{min(values):.12e}",
        "max_control_value": f"{max(values):.12e}",
        "mean_control_value": f"{mean:.12e}",
    }


def main() -> None:
    policy = read_one(POLICY)
    seed_rows = read_rows(SEEDS)
    theory_rows = read_rows(THEORY)
    theory_rows.sort(key=lambda row: int(row["row_index_zero_based"]))

    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("row-vector policy parent must remain endpoint disabled")
    if policy["current_control_scores_computed"] != "false":
        raise SystemExit("row-vector build must not derive from scored controls")
    if len(theory_rows) != 300:
        raise SystemExit("KiDS COSEBIs source-frozen theory vector must have 300 rows")
    for row in theory_rows:
        if row["contains_prediction"] != "false" or row["contains_residual"] != "false":
            raise SystemExit("theory rows must not contain predictions or residuals")
        if row["endpoint_scoring_allowed"] != "false":
            raise SystemExit("theory rows must remain endpoint disabled")

    seeds = {row["control_family"]: row for row in seed_rows}
    expected = {
        "sky_rotation": 4,
        "tomographic_pair_shuffle": 1000,
        "wrong_channel_activation": 2,
        "web_path_sign_flip": 2,
    }
    if set(seeds) != set(expected):
        raise SystemExit(f"unexpected seed families: {sorted(seeds)}")
    for family, multiplicity in expected.items():
        if int(seeds[family]["multiplicity"]) != multiplicity:
            raise SystemExit(f"unexpected multiplicity for {family}")
        if seeds[family]["endpoint_scoring_allowed"] != "false":
            raise SystemExit(f"seed family {family} must remain endpoint disabled")
        if seeds[family]["uses_kids_data_vector_values"] != "false":
            raise SystemExit(f"seed family {family} must not use KiDS data-vector values")

    pair_order = build_pair_order(theory_rows)
    by_pair_mode = {
        (row["pair_id"], int(row["mode"])): row for row in theory_rows
    }
    base_values = [float(row["theory_value"]) for row in theory_rows]
    out_rows: list[dict[str, str]] = []
    control_index = 0

    def emit_control(family: str, draw_index: int, operator: str, values: list[float]) -> None:
        nonlocal control_index
        control_index += 1
        if len(values) != len(theory_rows):
            raise SystemExit(f"control {operator} produced {len(values)} rows")
        for theory, value in zip(theory_rows, values, strict=True):
            out_rows.append(
                {
                    "policy_id": "KIDS1000_COSEBIS_NULL_CONTROL_ROW_VECTOR_POLICY_V1",
                    "parent_policy": policy["policy_id"],
                    "parent_theory_vector": "KIDS1000_COSEBIS_SOURCE_FROZEN_THEORY_VECTOR_POLICY_V1",
                    "selected_statistic": "COSEBIs",
                    "control_index_one_based": str(control_index),
                    "control_family": family,
                    "control_draw_index_zero_based": str(draw_index),
                    "operator": operator,
                    "row_index_zero_based": theory["row_index_zero_based"],
                    "row_index_one_based": theory["row_index_one_based"],
                    "bin1": theory["bin1"],
                    "bin2": theory["bin2"],
                    "pair_id": theory["pair_id"],
                    "mode": theory["mode"],
                    "control_theory_value": f"{value:.12e}",
                    "control_row_vector_computed": "true",
                    "contains_control_scores": "false",
                    "contains_prediction": "false",
                    "contains_residual": "false",
                    "contains_fit_statistic": "false",
                    "uses_kids_data_vector_values": "false",
                    "uses_posterior_chains": "false",
                    "uses_posthoc_control_selection": "false",
                    "uses_posthoc_control_multiplicity": "false",
                    "endpoint_scoring_allowed": "false",
                    "endpoint_validation_claimed": "false",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    sky_seed = int(seeds["sky_rotation"]["seed"])
    for draw_index in range(expected["sky_rotation"]):
        shift = (draw_index + 1) % len(pair_order)
        rotated = pair_order[shift:] + pair_order[:shift]
        pair_map = dict(zip(pair_order, rotated, strict=True))
        values = [
            float(by_pair_mode[(pair_map[row["pair_id"]], int(row["mode"]))]["theory_value"])
            for row in theory_rows
        ]
        emit_control("sky_rotation", draw_index, f"cyclic_pair_shift_{shift}_seed_{sky_seed}", values)

    shuffle_seed = int(seeds["tomographic_pair_shuffle"]["seed"])
    for draw_index in range(expected["tomographic_pair_shuffle"]):
        rng = random.Random(shuffle_seed + draw_index)
        shuffled = pair_order[:]
        rng.shuffle(shuffled)
        pair_map = dict(zip(pair_order, shuffled, strict=True))
        values = [
            float(by_pair_mode[(pair_map[row["pair_id"]], int(row["mode"]))]["theory_value"])
            for row in theory_rows
        ]
        emit_control(
            "tomographic_pair_shuffle",
            draw_index,
            f"seeded_pair_shuffle_{shuffle_seed + draw_index}",
            values,
        )

    wrong_seed = int(seeds["wrong_channel_activation"]["seed"])
    emit_control("wrong_channel_activation", 0, f"wrong_channel_web_null_zero_seed_{wrong_seed}", [0.0] * 300)
    emit_control("wrong_channel_activation", 1, f"wrong_channel_disabled_time_zero_seed_{wrong_seed}", [0.0] * 300)

    sign_seed = int(seeds["web_path_sign_flip"]["seed"])
    emit_control("web_path_sign_flip", 0, f"path_sign_flip_negative_seed_{sign_seed}", [-v for v in base_values])
    emit_control("web_path_sign_flip", 1, f"path_removed_zero_control_seed_{sign_seed}", [0.0] * 300)

    expected_rows = sum(expected.values()) * len(theory_rows)
    if len(out_rows) != expected_rows:
        raise SystemExit(f"expected {expected_rows} row-vector rows, got {len(out_rows)}")

    write_csv(OUT, out_rows)

    values = [float(row["control_theory_value"]) for row in out_rows]
    summary = {
        "policy_id": "KIDS1000_COSEBIS_NULL_CONTROL_ROW_VECTOR_POLICY_V1",
        "status": "KIDS1000_COSEBIS_NULL_CONTROL_ROW_VECTORS_BUILT_NOT_SCORED",
        "parent_policy": policy["policy_id"],
        "selected_statistic": "COSEBIs",
        "control_family_count": str(len(expected)),
        "control_draw_count": str(sum(expected.values())),
        "rows_per_control": str(len(theory_rows)),
        "total_row_vector_rows": str(len(out_rows)),
        "control_row_vectors_computed": "true",
        "contains_control_scores": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_control_selection": "false",
        "uses_posthoc_control_multiplicity": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    summary.update(vector_stats(values))
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# KiDS-1000 COSEBIs null-control row vectors v1",
                "",
                "**Doc class:** source-frozen row-level control-vector expansion.",
                "**Status:** not scoring; not endpoint validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This artifact expands the already frozen KiDS null-control theory",
                "replay into the same 300-row COSEBIs basis used by the candidate",
                "source-frozen theory vector. It uses only the source-frozen theory",
                "vector and the predeclared null-control seed inventory.",
                "",
                "It does not use KiDS data-vector values, posterior chains, residuals,",
                "fit statistics, post-hoc control selection, or endpoint scores.",
                "",
                "The row-vector table is stored as a gzip-compressed CSV because the",
                "uncompressed 302400-row table exceeds normal repository artifact",
                "comfort limits. The build script deterministically regenerates it.",
                "",
                f"Rows: `{summary['total_row_vector_rows']}`.",
                f"Verdict: `{summary['status']}`.",
                "",
            ]
        )
    )
    print(
        "PAPER10_KIDS1000_COSEBIS_NULL_CONTROL_ROW_VECTORS_V1_BUILT "
        f"rows={summary['total_row_vector_rows']} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
