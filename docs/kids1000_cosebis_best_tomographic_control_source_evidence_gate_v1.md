**Doc class:** endpoint caveat source-evidence gate
**Reader role:** reviewer checking whether the best holdout-beating tomographic control has source-side support
**Status:** control-only closure; not validation
**Canonical parent:** README.md

# KiDS-1000 COSEBIs Best Tomographic Control Source-Evidence Gate

The source-frozen tomographic holdout replay leaves one control ahead of the
candidate:

```text
seeded_auto_cross_shuffle_702759
```

This gate asks a narrow question: can that control be interpreted as a
source-side physical or calibration alternative, rather than as a control-only
tomographic relabel?

The answer is no in the current source state. The mapping is an
auto/cross-preserving pair shuffle, but it is not induced by any single global
source-bin relabel. For example, the auto-pair map implies \(1\to2\) and
\(2\to3\), so a global source-bin relabel would send \(1\text{--}2\) to
\(2\text{--}3\). The observed control sends \(1\text{--}2\) to
\(1\text{--}5\). This contradiction prevents source-systematic promotion.

Current result:

- target control: `seeded_auto_cross_shuffle_702759`,
- target family: `auto_cross_preserving_shuffle`,
- global source-bin relabel: false,
- independent source evidence attached: false,
- accepted physical alternative: false,
- endpoint validation claimed: false.

Thus the best holdout-beating control remains control-only. It does not refute
the endpoint signal, but the broader tomographic-control caveat still blocks
validation.
