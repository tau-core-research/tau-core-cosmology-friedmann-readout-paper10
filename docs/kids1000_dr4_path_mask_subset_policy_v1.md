# KiDS DR4 Path-Mask Subset Policy v1

This freezes a small source-side mask-product subset from the preferred KiDS
DR4.1 9-band mask route.

Subset rule:

```text
promote_head_sample_first_middle_last_to_download_subset
indices: 0;98;195
```

The subset is deliberately tiny relative to the full 196-mask route. It is used
only to verify that the external mask route can be materialized and parsed as
FITS image data. The inventory records file hashes, image shapes, finite-pixel
counts, and basic mask-value summaries.

This is not a path mapping and not a lensing endpoint. It does not connect mask
pixels to COSEBIs rows, does not compute a theory vector, and does not score a
Tau Core channel.
