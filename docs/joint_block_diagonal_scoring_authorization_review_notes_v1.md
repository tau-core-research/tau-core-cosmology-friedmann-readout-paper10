# Joint block-diagonal scoring authorization review notes v1

Decision:

```text
AUTHORIZE_SEPARATE_GUARDED_JOINT_PERMISSION_REPLAY_PACKAGE_NOT_SCORING_NOT_VALIDATION
```

Scope: this review authorizes preparation of a separate guarded permission-only joint replay/scoring authorization package. It does not run scoring and does not claim endpoint or cosmological validation.

Required caveats carried forward:

- shared sky/mask overlap remains unmodeled by a full cross-probe covariance product;
- redshift-kernel overlap remains a caveat;
- shared cosmology, nuisance and calibration correlations remain caveats;
- population-level cross-probe covariance is still missing;
- candidate and controls must use the same predeclared block-diagonal statistic and the same reviewed covariance/independence blocks;
- a separate replay/scoring authorization package is still required before any computation.

Boundary flags:

```text
forbidden_inputs_used=false
endpoint_scoring_allowed=false
endpoint_validation_claimed=false
cosmological_validation_claimed=false
permission_only_replay_authorization_allowed=true
separate_replay_package_required=true
```

Interpretation: the caveated block-diagonal independence precondition can be carried into a future guarded package, but direct scoring remains forbidden in this review.
