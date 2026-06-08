# KiDS-1000 COSEBIs `F_overlap` Full-Mask Acquisition Manifest v1

This gate builds a 196-row source-side acquisition manifest for the preferred
KiDS DR4.1 9-band route mask products. It does not fetch products.

For each preferred route tile, the manifest records:

- source URL from the frozen route inventory;
- expected local path;
- filename-coordinate proxies;
- whether the file is already present locally;
- whether the file would still need fetching before a full source-native
  overlap derivation.

Current result: only the three-mask subset is locally present. The remaining
193 mask products are missing, so the full-mask route is not accepted for
`F_overlap`, the overlap rule is not ready, and mapping/scoring remain disabled.

This gate is intentionally negative-preserving: a route script plus three mask
files must not be silently promoted into a full overlap rule.
