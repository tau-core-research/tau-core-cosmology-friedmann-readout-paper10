# Cosmology Channel Manifest v1

Paper 10 now has an explicit channel-freeze layer:

```text
data/source_manifest/cosmology_channel_manifest_v1.csv
```

This manifest is the operational version of the multi-channel Tau Core
readout basis. It does not score data and it does not validate a cosmological
signal. It declares which source-side information may later define each
cosmological readout channel.

## Channels

| Channel | Role | Current status |
| --- | --- | --- |
| `W_VOID_MATURITY` | void maturity / late-time distance-growth activation | declared, not endpoint |
| `W_WEB_ANISOTROPY` | cosmic-web environment / growth-lensing anisotropy | declared, not endpoint |
| `W_PATH_PROJECTION` | observer/path projection through the null-geodesic-bundle environment | declared, not endpoint |
| `W_TIME_READOUT` | time/readout projection of observed `a(t)` and `H(t)` reconstructions | declared, not endpoint |

## Projection-Induction Interpretation

The channel manifest is below a physical derivation. Its job is to prepare the
source-freeze layer required by the projection-induction gate:

```text
Tau-side mode
    -> activation
    -> quotient survival
    -> closure stability
    -> 4D readout survival
    -> induced observable / closure source
```

At this stage each channel is only a declared proxy route. A future derivation
would need to show, for example, that `W_void` or `W_web` is the 4D readout of
a stable Tau-side mode rather than a phenomenological template.

## Leakage Prevention

The manifest forbids:

```text
distance residuals
growth residuals
lensing residuals
fit-improvement flags
post-hoc environment labels
post-hoc sky direction selection
late-time fit parameters
```

from selecting the channel labels, activation rules, thresholds, or masks.

## Endpoint Status

Every row currently has:

```text
endpoint_scoring_allowed=false
freeze_status=CHANNEL_DECLARED_NOT_ENDPOINT
```

This means the manifest can be reproduced and audited, but it cannot yet be
used as an endpoint validation dataset.

The next allowed step is to acquire exact public products and freeze numerical
activation rules without using target residuals.
