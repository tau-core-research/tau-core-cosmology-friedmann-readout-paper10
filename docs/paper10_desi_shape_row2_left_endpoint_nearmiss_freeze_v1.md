# Paper10 DESI shape row2 left-endpoint near-miss freeze v1

**Doc class:** source-side caveated near-miss freeze
**Reader role:** source-acquisition auditor / reviewer
**Status:** left endpoint still blocked, not replay, not validation
**Canonical parent:** Paper10 DESI shape-route replay chain

This artifact freezes the relaxed independent left-endpoint context found
by the row-2 endpoint-pair independence scout. It does not change the
strict endpoint-pair gate.

Frozen result:

- relaxed independent left candidates: `2`
- closest relaxed independent candidate: `Stern et al. (2010)`
- closest relaxed independent delta-z: `0.054`
- strict independent left support count: `0`
- left endpoint release allowed: `false`

Interpretation:

Stern et al. (2010) and Moresco et al. (2012) are useful left-endpoint
near-miss context, but both are outside the frozen strict `|Delta z| <= 0.05`
endpoint window. They can motivate a separate source-window review or
source-native shape support search; they do not authorize replay.

Claim boundary:

```text
paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_not_validation
```

Machine verdict: `row2_left_endpoint_has_relaxed_independent_nearmisses_but_no_strict_support`.
