# Joint numeric T_joint source-route overlap metric v1

**Doc class:** residual-blind source-route overlap scaffold.
**Status:** caveated metric available; not scoring; not validation.
**Claim boundary:** `joint_numeric_t_joint_source_route_overlap_metric_not_scoring_not_validation`.

This artifact defines a route-tag Jaccard overlap between the
observer-path low-z channel and the DESI shape/time channel. The tags
are source-route descriptors only; endpoint residuals, endpoint scores,
and the thin `T_joint` margin are not used.

Shared tags: `permission_replay`.
Jaccard overlap: `9.090909090909e-02`.
Jaccard distance: `9.090909090909e-01`.

The metric supports the statement that the source routes are largely
distinct at the route-tag level. It still does not authorize a penalty
or any numeric `T_joint` rescoring, because the small-N balance and
candidate/control symmetry requirements remain open.
