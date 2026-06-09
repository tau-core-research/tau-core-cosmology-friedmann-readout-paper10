# KiDS-1000 COSEBIs Log-Band Prior Mock Sanity v1

This deterministic sanity suite checks the template-recovery logic behind the
log-band prior. It is not a physical mock suite and it does not use KiDS data
vector values.

The suite creates four deterministic truth families over the retained
`15 x 20` COSEBIs row structure:

- low log-band truth, proportional to `n^-0.5`;
- flat coherent truth;
- high-mode truth, proportional to `n`;
- oscillatory alternating truth.

It compares each truth family against the same four template families using
cosine similarity. The expected outcome is that each truth recovers its matching
template. This confirms that the protocol does not automatically classify every
deterministic mock as low-mode.

Current verdict:

```text
deterministic_template_recovery_pass_not_physical_mock_validation
```

Claim boundary:

```text
kids1000_cosebis_log_band_prior_mock_sanity_not_validation
```
