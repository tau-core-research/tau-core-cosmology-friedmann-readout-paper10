# Pantheon time/readout clock-rate phase CC-support candidate v1

**Doc class:** source-side candidate construction
**Status:** not endpoint replay, not validation
**Canonical parent:** Paper 10 time/readout source audit

This artifact broadens the previous low-z clock-rate/phase construction from
three low-z CC support bins to the Pantheon rows covered by the fetched cosmic
chronometer table.

Construction:

- input distance rows: `pantheon_void_web_source_native_design_matrix_v1`;
- input clock support: `data_CC.dat`;
- include only rows with `zHD <= max(CC_z)`;
- assign each included row to the nearest CC redshift support point;
- freeze three source-side bases:
  - assigned `log H(z)` level;
  - finite-difference `d log H / d log(1+z)` slope;
  - normalized level/slope phase product.

Coverage:

- input Pantheon design rows: 1371;
- included rows: 1370;
- excluded above CC support: 1;
- used nearest-neighbor CC support bins: 31;
- below-minimum CC support rows are explicitly edge-clamped and flagged.

This is not a physical clock-drift measurement. It is a residual-blind,
source-side time/readout candidate built to test whether wider CC support
reduces the low-z rank-control blocker.
