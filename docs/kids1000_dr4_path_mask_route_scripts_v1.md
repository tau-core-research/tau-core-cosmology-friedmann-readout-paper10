# KiDS DR4 Path-Mask Route Scripts v1

This freezes the official KiDS DR4 mask route scripts needed for a future
source-side `W_PATH_PROJECTION` mapping.

The frozen artifacts are the route scripts only:

```text
kids_dr4.1_9band_msk_wget.sh  -> preferred multi-band mask route
kids_dr4.0_9band_msk_wget.sh  -> legacy multi-band mask route
kids_dr4.0_msk_wget.sh        -> legacy single-band mask route
```

The preferred DR4.1 9-band script lists 196 mask FITS products. The present
package does not download those mask FITS products, does not parse a mask map,
does not compute a path mapping vector, and does not build a COSEBIs theory
vector.

This gate turns the previous path-mask/depth source gap into a source-frozen
route to the external products required for a future path-aware lensing
endpoint. It still does not authorize scoring.
