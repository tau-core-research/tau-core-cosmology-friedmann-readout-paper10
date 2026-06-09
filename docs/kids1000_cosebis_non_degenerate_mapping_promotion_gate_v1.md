# KiDS-1000 COSEBIs Non-Degenerate Mapping Promotion Gate V1

This gate records the minimum conditions required before the KiDS COSEBIs
partial-control diagnostic route may be promoted toward endpoint scoring.

It is not a score and not endpoint validation. It exists because the previous
partial-control degeneracy audit showed that the positive three-mask branch
family is effectively rank one. A rank-one partial-control branch can be useful
as a smoke test, but it cannot stand in for a non-degenerate endpoint
theory-vector family.

The frozen gates are:

1. accept an endpoint-grade `F_overlap` route from official geometry or full
   route masks;
2. make the source-preflight mapping state ready;
3. pass a non-degenerate branch-geometry audit;
4. compute a frozen 300-row theory vector from the source-frozen mapping;
5. execute predeclared null controls after the mapping vector exists;
6. keep leakage guards active.

Current status:

- only the leakage guard passes;
- `F_overlap` remains the first blocker;
- the partial-control rank-one geometry remains an explicit blocker;
- endpoint scoring remains disabled.

Claim boundary:

`non_degenerate_mapping_promotion_gate_not_scoring_not_validation`
