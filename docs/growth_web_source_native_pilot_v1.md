# Growth Web Source-Native Pilot V1

This pilot asks whether the already frozen SDSS DR17 MCPM `W_web` source-native
basis has more natural support in a growth observable than in the Pantheon-only
distance observable.

It uses the six SDSS final BAO/RSD `f sigma8(z)` summary points and diagonal
published errors only.

## Claim Boundary

Status:

```text
GROWTH_WEB_SOURCE_NATIVE_PILOT_NOT_VALIDATION
```

This is not a full eBOSS/BOSS likelihood and not endpoint validation. The
official compressed-parameter covariance is not frozen here. The pilot is a
diagonal-summary stress test of the multi-probe direction.

## Model Grammar

Baseline:

```text
f sigma8_LCDM(z; Omega_m, sigma8_0)
```

using the growth-index approximation `gamma = 0.55`.

Web branch:

```text
f sigma8_web(z) = f sigma8_LCDM(z) * (1 + mu_web W_web(z))
```

Controls include a wrong-sign web branch and a deterministic shuffled `W_web`
branch.

## Current Result

The current frozen run gives:

```text
Delta chi2(web - baseline) = -0.3061020233
Delta AIC(web - baseline)  = +1.69389797667
```

The wrong-sign control reaches the same best chi-square on the symmetric pilot
grid, while the shuffled control is only slightly worse. This means the
diagonal-summary pilot does not establish a preferred web direction. It is a
useful multi-probe pipeline step, not evidence for a growth-side Tau Core
signal.
