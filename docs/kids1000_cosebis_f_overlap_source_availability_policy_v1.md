# KiDS-1000 COSEBIs `F_overlap` Source Availability v1

This gate audits the local source availability for the accepted future
`F_overlap` routes. It does not fetch new products and does not compute
overlap values.

Current source-side state:

- the 58,800-row COSEBIs target-row by route-tile domain shell is available;
- the preferred DR4.1 9-band mask route script lists 196 route tiles;
- only the three-mask subset is present locally as a partial path sanity layer;
- no official footprint geometry product is accepted in the repository;
- no full 196-mask source-native overlap route is accepted yet.

Therefore `F_overlap` remains unresolved. The first unresolved source gap is:
official footprint geometry or a full 196-mask source-native product set.

The gate preserves this negative/partial result explicitly so that later
mapping or scoring cannot proceed by silently treating the route script or the
three-mask subset as a full overlap rule.
