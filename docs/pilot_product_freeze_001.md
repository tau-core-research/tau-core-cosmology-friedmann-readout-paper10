# Paper 10 Pilot Product Freeze 001

This note records the first deliberately narrow product-freeze exercise.

It does not authorize endpoint scoring.

## Frozen Pilot Products

| Pilot product | Parent product | Role | Endpoint blocker |
| --- | --- | --- | --- |
| `CC_HZ_DATA_CC_DAT` | `CC_HZ_TABLE` | public cosmic-chronometer `H(z)` table | covariance/systematics policy not frozen |
| `PANTHEON_PLUS_SH0ES_DAT` | `PANTHEON_PLUS_LIGHTCURVE_OR_MU` | Pantheon+ distance table | covariance matrix not frozen |

## Why These Products

These two products are small enough to commit and hash-lock in the private
scaffold. They demonstrate the acquisition and validation mechanism without
pulling large chains, maps, catalogues, or covariance matrices into the repo.

## Current Status

The pilot products are:

```text
PILOT_PRODUCT_FETCHED_FROZEN
```

but every row still has:

```text
endpoint_allowed=false
```

The reason is simple: distance-table central values without the corresponding
covariance/systematics policy are not an endpoint dataset.

## Next Gate

The next data gate is not fitting. It is freezing one covariance-capable pilot
scope, for example:

```text
Pantheon+ distance table + covariance matrix + mask policy
```

or:

```text
Cosmic chronometer table + Moresco-style covariance/systematics recipe
```
