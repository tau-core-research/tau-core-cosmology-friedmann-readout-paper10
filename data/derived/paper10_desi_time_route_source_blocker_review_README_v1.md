# Paper10 DESI Time-route Source-blocker Review Package v1

This combined handoff is for an external reviewer who does not have repository
access.

It contains two independent source-side review packages:

1. `paper10_desi_row4_window_review_package_v1.zip`
   - Question: should the frozen DESI row-4 clock-support window remain strict,
     or may the Moresco (2015) `z=1.363` near-window chronometer point be carried
     as caveated source-side context for the DESI row at `z_eff=1.484`?
   - SHA256:
     `78efe0a4ed5bf439f3cc028a9c1f93040dc738ff795bb1f12d1fdb4c3325d925`

2. `paper10_desi_row5_high_z_review_package_v1.zip`
   - Question: is there an independent high-redshift clock/chronometer source,
     or a source-native high-z time/readout observable, that can support the
     DESI row at `z=2.33` without treating Ly-alpha BAO alone as clock support?
   - SHA256:
     `04b8e5e123276d99215be82e90d39f7e567252a806d67e4bd2ffcef00883c4cd`

Claim boundary:

- These are source-side review packages only.
- They contain no endpoint residuals, endpoint scores, or fit statistics.
- They do not authorize endpoint replay.
- They do not claim endpoint validation or physical validation.
- Even a positive response can only reopen source-side work or request a
  separate replay-authorization handoff.

Reviewer instructions:

1. Unzip each included package separately.
2. Fill the response CSV inside each package.
3. Keep all `endpoint_replay_allowed`, `endpoint_validation_claimed`, and
   `physical_validation_claimed` fields set to `false`.
4. Attach source references/URLs only for source-side evidence.
5. Return the completed response CSVs or zip each completed package back to the
   author.

Preferred conservative outcome:

- Row4 remains blocked unless the near-window Moresco (2015) source is accepted
  with explicit caveats.
- Row5 remains blocked unless a genuine high-z clock/source-native time-readout
  route is identified.
