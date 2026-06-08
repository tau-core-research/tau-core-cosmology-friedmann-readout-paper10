# KiDS DR4 Path-Mask HEAD Sample Policy v1

This freezes a small availability-only HEAD audit for the preferred KiDS DR4.1
9-band mask route script.

Sampling rule:

```text
first_middle_last_from_preferred_route
indices: 0;98;195
```

The policy checks only HTTP metadata for three mask FITS products listed by the
preferred route script. It does not download those FITS files, does not parse
mask pixels, does not compute a path mapping, and does not build a COSEBIs
theory vector.

The sample is a route-health sanity check, not a mask subset for scoring.
