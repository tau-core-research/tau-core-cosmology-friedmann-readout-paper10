# KiDS DR4 Path-Mask Observable Shell Policy v1

This gate converts the predeclared three-product KiDS DR4.1 path-mask subset
into a source-only observable shell.

The shell records only:

- filename-derived KiDS tile coordinates,
- finite/nonzero mask-pixel fractions already present in the subset inventory,
- a centered zero-fraction shell value across the three frozen masks.

The shell is deliberately not a physical path map. The KiDS mask-value semantics
are not interpreted as a lensing weight here, and no COSEBIs row mapping is
constructed. The centered shell is only a pre-mapping source observable that can
later be audited as a candidate path/projection input if a full source-frozen
survey geometry rule is added.

This gate does not use KiDS data-vector values, posterior chains, residuals, fit
statistics, or post-hoc projection labels. It does not compute a theory vector
and it does not score a Tau Core channel.
