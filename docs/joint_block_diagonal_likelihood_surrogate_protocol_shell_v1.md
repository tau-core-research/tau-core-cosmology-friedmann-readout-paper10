# Joint block-diagonal likelihood-surrogate protocol shell v1

**Doc class:** protocol shell draft
**Status:** not scoring; not endpoint validation; not cosmological validation
**Claim boundary:** `joint_block_diagonal_likelihood_surrogate_protocol_shell_not_scoring_not_validation`

This artifact freezes the algebraic shape of a possible future
block-diagonal likelihood-surrogate for the three active Paper10
channels. It is a shell only: it does not read endpoint residuals,
does not invert new covariance matrices, does not compute a score,
and does not authorize a replay.

The predeclared shell is:

\[
  Q_{\rm joint}^{\rm BD} = \sum_i r_i^T C_i^{-1} r_i,
\]

where each block must use the same row scope, score-source artifact,
covariance block, nuisance rule, and statistic for the candidate and
all matched controls.

Current machine state:

- active channels: `kids_lensing_cosebis_low_mode;observer_path_basis_low_z;desi_shape_time_readout`
- block-diagonal review status: `completed_caveated_protocol_shell_allowed`
- protocol shell allowed by review: `true`
- cross-probe covariance defined: `false`
- cross-probe independence closed: `false`
- executable now: `false`
- endpoint scoring allowed: `false`
- verdict: `JOINT_BLOCK_DIAGONAL_PROTOCOL_SHELL_FROZEN_COVARIANCE_STILL_OPEN_NOT_SCORING`
