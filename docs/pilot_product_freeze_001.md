# Paper 10 Pilot Product Freeze 001

This note records the first deliberately narrow product-freeze exercise.

It does not authorize endpoint scoring.

## Frozen Pilot Products

| Pilot product | Parent product | Role | Endpoint blocker |
| --- | --- | --- | --- |
| `CC_HZ_DATA_CC_DAT` | `CC_HZ_TABLE` | public cosmic-chronometer `H(z)` table | covariance/systematics policy not frozen |
| `PANTHEON_PLUS_SH0ES_DAT` | `PANTHEON_PLUS_LIGHTCURVE_OR_MU` | Pantheon+ distance table | covariance matrix was frozen in the next row, but endpoint policy remains blocked |
| `PANTHEON_PLUS_SH0ES_STAT_SYS_COV` | `PANTHEON_PLUS_LIGHTCURVE_OR_MU` | Pantheon+ STAT+SYS covariance matrix | mask/calibration/pilot-scope policy not frozen |

## Why These Products

These products are small enough to commit and hash-lock in the private scaffold.
They demonstrate the acquisition and validation mechanism without pulling large
chains, maps, or catalogues into the repo. The Pantheon+ covariance file is
included because it is the first useful covariance-capable distance-block
sanity check.

## Current Status

The pilot products are:

```text
PILOT_PRODUCT_FETCHED_FROZEN
```

but every row still has:

```text
endpoint_allowed=false
```

The reason is simple: even a distance table plus covariance matrix is not an
endpoint dataset until the mask, calibration, nuisance-parameter, and pilot
scope policies are frozen before scoring.

## Next Gate

The next data gate is not fitting. It is freezing one endpoint-eligible pilot
scope, for example:

```text
Pantheon+ distance table + covariance matrix + mask/calibration policy
```

or:

```text
Cosmic chronometer table + Moresco-style covariance/systematics recipe
```
