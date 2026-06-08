# SDSS Multi-Tracer BAO/RSD Design Matrix v1

This design matrix reads the official SDSS DR16 LRG+ELG Fourier-space
multi-tracer compressed measurement and covariance. It keeps the published
observable order and attaches a source-native SDSS DR17 MCPM web basis by
nearest redshift-bin lookup.

The design matrix contains no model predictions, no residuals, no fitted
parameters, and no endpoint statistics. It is endpoint disabled.

The pilot policy is deliberately narrow: the web channel may affect only the
`f sigma_8` entries. The two BAO distance entries at each redshift are retained
because the official covariance couples the BAO and growth summary parameters.
