# KiDS-1000 COSEBIs F-overlap full-route cache inventory v1

This artifact records a local source-cache inventory for the KiDS-1000 path-mask route needed before any endpoint-grade F-overlap construction can be attempted.

It is not an overlap factor, not a path mapping, not a theory vector, and not endpoint scoring.

## Inputs

- Policy: `data/source_manifest/kids1000_cosebis_f_overlap_full_route_cache_inventory_policy_v1.csv`
- Parent route manifest: `data/derived/kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.csv`
- Committed package subset: `data/raw/weak_lensing/kids1000_path_masks/mask_subset_v1/`
- Ignored local full-route cache: `data/raw/weak_lensing/kids1000_path_masks/full_route_cache_v1/`

The ignored local cache is intentionally not part of the public package because it is about 1 GB of external FITS products. Public reproduction does not require those raw files; it validates the committed source-cache inventory snapshot and keeps the raw-cache fetch as an explicitly documented optional acquisition step.

## Current local snapshot

The local acquisition run accounted for all 196 expected mask products:

- 193 products in the ignored full-route cache.
- 3 products in the committed subset.
- 196 nonzero files with SHA-256 hashes in the committed inventory.

This resolves the previous source-cache absence at the acquisition level only. It does not resolve the F-overlap endpoint route gate by itself.

## Leakage boundary

The inventory contains no KiDS data-vector values, posterior chains, residuals, predictions, fit statistics, mapping vector, or theory vector. It only records source URLs, relative file locations, byte sizes, and SHA-256 hashes.

Endpoint scoring remains disabled.

## Next gate toward scoring

The next required step is an independently specified F-overlap construction rule that uses the source-cache products without reading endpoint residuals or posterior chains. Only after that route is accepted can the non-degenerate path-mapping gate be revisited.
