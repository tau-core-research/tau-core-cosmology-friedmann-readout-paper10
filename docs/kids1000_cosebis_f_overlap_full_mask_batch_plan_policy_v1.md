# KiDS-1000 COSEBIs `F_overlap` Full-Mask Batch Plan v1

This gate turns the 193 missing preferred-route mask products into a
reproducible batch plan. It does not fetch any products.

The plan uses batches of at most 20 FITS files. With 193 missing masks, this
creates ten batches. Large future FITS products are assigned to:

```text
data/raw/weak_lensing/kids1000_path_masks/full_route_cache_v1/
```

The cache is intentionally excluded from Git. The repository should commit
manifests, checksums, and derived source-side summaries, not the full future
FITS cache. The current three-mask subset remains the only raw mask subset
included in the public package.

The batch plan keeps `F_overlap` unresolved: no products are fetched, no
overlap rule is computed, no path mapping is built, and no endpoint scoring is
allowed.
