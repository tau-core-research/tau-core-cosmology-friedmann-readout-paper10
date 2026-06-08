# Paper 10 Source Selection Audit 001

This note records the first source-selection pass for the blocks that were
previously `BLOCKED_SOURCE_SELECTION`.

The audit does not download data and does not authorize endpoint scoring. It
only upgrades a block from:

```text
BLOCKED_SOURCE_SELECTION
```

to:

```text
SOURCE_SELECTED_NOT_FETCHED
```

when a plausible public source family exists.

## Resolved Source-Selection Blocks

| Block | Selected source family | URL | Remaining blocker |
| --- | --- | --- | --- |
| `HZ_CC_BAO` | University of Bologna / Moresco-related Cosmic Chronometers data page | `https://cluster.difa.unibo.it/astro/CC_data/` | exact covariance, SPS/systematics, and BAO-combination policy |
| `COSMIC_WEB_CLASSIFIER` | SDSS cosmic-web value-added catalogue | `https://www.sdss.org/dr18/data_access/value-added-catalogs/?vac_id=99` | mapping from web class/density output to `Q_env` |
| `RSD_GROWTH_COMPILATION` | SDSS/eBOSS DR16 large-scale-structure products | `https://www.sdss4.org/dr17/spectro/lss/` | exact `f sigma8` summary vector and covariance extraction |
| `WEAK_LENSING_PRODUCTS` | KiDS-1000 lensing catalogues and cosmology data products | `https://kids.strw.leidenuniv.nl/DR4/lensing.php` | tomographic bin, mask, covariance, and summary-statistic policy |

## Current Status

All required source families now have a candidate public source route.

However, no row is `FETCHED_FROZEN`. Therefore Paper 10 still remains below
real-data pilot status. The next gate is source acquisition with:

- exact product path,
- access date,
- checksum or immutable archive identifier where possible,
- transformation rule,
- covariance/mask policy,
- and explicit forbidden endpoint fields.

## Claim Boundary

The source-selection pass means:

```text
The Paper 10 real-data pilot is no longer blocked at the source-family
identification layer.
```

It does not mean:

```text
The Paper 10 endpoint can be scored.
```

Endpoint scoring remains forbidden until selected sources become
`FETCHED_FROZEN` or a narrower pilot scope is predeclared.
