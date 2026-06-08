# CMB Safety Low-z Support Check v1

This is a known-limit safety check, not a CMB fit and not evidence for a Tau
Core cosmological signal.

The present Paper 10 pilots activate only low-redshift void and web channels.
The void basis is derived from a local VAST/SDSS DR7 void catalogue and the web
basis from an SDSS DR17 MCPM catalogue with usable redshift bins below
approximately `z=3`. The CMB safety check asks whether these channel bases are
zero at recombination-scale redshift and above a conservative high-redshift
safety floor.

Frozen policy:

```text
z_recombination_proxy = 1089.92
z_safety_floor = 10.0
```

Pass condition:

```text
W_void(z_recombination_proxy) = 0
W_web(z_recombination_proxy) = 0
W_void(z_safety_floor) = 0
W_web(z_safety_floor) = 0
```

Interpretation: the current late-time void/web pilots do not directly modify
the early-universe CMB safety regime. This does not test CMB lensing, CMB maps,
or a full early-universe likelihood.
