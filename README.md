# Tau Core Cosmology Friedmann-Readout Paper 10

This repository is the initial private reproducibility scaffold for Paper 10:

**A source-frozen Friedmann-readout audit protocol for late-time cosmology**

The paper is a protocol and pilot-analysis design. It connects the
Koushiappas uncertainty-Friedmann external comparison to a Tau Core
Friedmann-readout residual audit, then asks a two-level question:

1. source-by-source, do independently frozen readout/projection channels carry
   any control-surviving or diagnostically informative signal?
2. jointly, do the already recorded channel outcomes form a nonempty
   multi-channel pattern?

The current answer is intentionally cautious. Some source channels are
suggestive, some are weak, and some are preserved negatives. The joint layer is
positive in sign but fragile and not a validation result.

## Main Claim

The repository defines a reproducible audit protocol:

```text
source-frozen projection/readout channels
    -> separate source-by-source audits with controls
    -> joint preflight synthesis of recorded channel summaries
    -> future multi-probe endpoint only after covariance-aware controls.
```

The current evidence is best described as
`multi-channel viability evidence, not cosmological validation`.

## Does Not Claim

- It does not claim that Tau Core explains dark energy.
- It does not claim a detection of a Friedmann-readout residual.
- It does not replace Lambda-CDM.
- It does not validate the Koushiappas uncertainty-Friedmann model.
- It does not use CMB maps as direct evidence for a Tau Core effect.
- It does not contain a completed perturbation-level or covariant Tau Core
  cosmology derivation.

## Included Data

This first scaffold contains only compact protocol artifacts in `data/derived/`.
No raw survey products are included.

The source-freeze manifest is:

```text
data/source_manifest/paper10_source_freeze_manifest.csv
```

It records candidate public source families, their current freeze status,
planned local artifact paths, and endpoint fields that are forbidden during
source selection.

The first explicit multi-channel readout manifest is:

```text
data/source_manifest/cosmology_channel_manifest_v1.csv
data/source_manifest/cosmology_activation_rule_manifest_v1.csv
data/source_manifest/cosmology_activation_parameter_freeze_plan_v1.csv
data/source_manifest/cosmology_source_grounding_gate_v1.csv
data/source_manifest/cosmology_flrw_consistency_channel_audit_v1.csv
docs/cosmology_channel_manifest_v1.md
docs/cosmology_activation_rule_manifest_v1.md
docs/cosmology_activation_parameter_freeze_plan_v1.md
docs/cosmology_source_grounding_gate_v1.md
docs/cosmology_flrw_consistency_channel_audit_v1.md
scripts/validate_cosmology_channel_manifest_v1.py
scripts/validate_cosmology_activation_rule_manifest_v1.py
scripts/validate_cosmology_activation_parameter_freeze_plan_v1.py
scripts/validate_cosmology_source_grounding_gate_v1.py
scripts/validate_cosmology_flrw_consistency_channel_audit_v1.py
```

It declares the four source-frozen channel families `W_void`, `W_web`,
`W_path`, and `W_time`, plus their allowed source families, forbidden endpoint
fields, activation-rule IDs, null controls, and projection-induction roles.
The activation-rule manifest adds non-numeric formula shells and source-only
parameter-freeze policies. The parameter-freeze plan declares how scales such
as `S_void_star`, `Q_env_star`, `P_lens_star`, and `Delta_clock_star` may later
be frozen from source-native data. The source-grounding manifest then freezes
the four missing projection-induction checks for each channel: activation,
quotient survival, closure stability, and 4D readout survival. Every row
remains `endpoint_scoring_allowed=false`.
The FLRW-consistency channel audit then declares whether each channel primarily
touches optical/path readout, expansion/time readout, density reconstruction, or
the single-FLRW-geometry assumption. This is a discipline artifact, not a new
score: it prevents `C_tau,cosmo` from becoming an unfrozen absorber for
curvature, backreaction, dark-energy, calibration, or reconstruction effects.

The current best-justified joint-kernel preflight is recorded in:

```text
data/source_manifest/joint_best_justified_kernel_manifest_v1.csv
data/derived/joint_best_justified_kernel_score_v1.csv
data/derived/joint_best_justified_kernel_score_v1_controls.csv
data/derived/joint_best_justified_kernel_score_v1_leave_one_channel.csv
data/derived/joint_best_justified_kernel_score_v1_summary.csv
docs/joint_best_justified_kernel_score_v1.md
scripts/run_joint_best_justified_kernel_score_v1.py
scripts/validate_joint_best_justified_kernel_score_v1.py
```

It implements the residual-blind rule
`Q_i = product_a (g_i^a)^(1/7)` and `w_i = Q_i / sum_j Q_j`.
The first run keeps only KiDS/COSEBIs low-mode, observer/path low-z, and DESI
shape/readout as positive-support channels. It gives normalized score
`0.713515777`, exact sign-flip `p = 0.125000000`, and verdict
`BEST_JUSTIFIED_JOINT_KERNEL_POSITIVE_PREFLIGHT_NOT_VALIDATION`. This is not a
joint cosmological likelihood and not validation.

The source-side weighting robustness stress for that same frozen channel
ledger is recorded in:

```text
data/derived/joint_best_justified_kernel_robustness_v1.csv
data/derived/joint_best_justified_kernel_robustness_v1_controls.csv
data/derived/joint_best_justified_kernel_robustness_v1_summary.csv
docs/joint_best_justified_kernel_robustness_v1.md
paper10_submission_source/figures/fig_joint_best_justified_kernel_v1.pdf
scripts/run_joint_best_justified_kernel_robustness_v1.py
scripts/validate_joint_best_justified_kernel_robustness_v1.py
scripts/build_joint_best_justified_kernel_figure_v1.py
```

It tests equal-geometric, source-heavy, control-heavy, projection-heavy, and
conservative min-gate support rules. All five remain positive, with minimum
normalized score `0.703534932`, exact sign-flip `p = 0.125000000`, and verdict
`BEST_JUSTIFIED_KERNEL_ROBUST_POSITIVE_PREFLIGHT_NOT_VALIDATION`. The
conservative min-gate combined weight-shuffle control is intentionally reported
as weak (`p = 0.993055556`) because equal active weights make that shuffle
nearly degenerate. This robustness stress supports sign stability against
source-side exponent choice; it is not validation and not a joint likelihood.
The figure is generated directly from the frozen manifest and robustness CSVs.

A compact referee-readiness audit of the current manuscript claim boundary is
recorded in:

```text
docs/paper10_referee_readiness_audit_v1.md
```

Its verdict is `SUBMIT_AFTER_MAJOR_STRUCTURE_REDUCTION_OR_AS_LONG_PROTOCOL_PREFLIGHT`.
It records the current strongest points, reviewer-risk points, and the next
required gate before stronger claims: source-native `Q_i` review plus a
covariance-aware joint likelihood prototype.

The first source-side `Q_i` review package for the best-justified joint kernel
is prepared in:

```text
data/source_manifest/joint_best_justified_qi_review_requirements_v1.csv
data/derived/joint_best_justified_qi_review_response_template_v1.csv
data/derived/joint_best_justified_qi_review_response_v1.csv
data/derived/joint_best_justified_qi_review_response_v1_summary.csv
data/derived/joint_best_justified_qi_review_validation_log_v1.txt
docs/joint_best_justified_qi_review_package_v1.md
docs/joint_best_justified_qi_review_response_gate_v1.md
docs/joint_best_justified_qi_review_notes_v1.md
scripts/validate_joint_best_justified_qi_review_package_v1.py
scripts/validate_joint_best_justified_qi_review_response_v1.py
```

This package does not compute new endpoint scores. It freezes the review
questions needed before the protocol support scores `Q_i` can be promoted
beyond preflight bookkeeping. The response gate validates either the blank
template state or a fully completed source-side reviewer response. It rejects
partial responses, forbidden endpoint inputs, endpoint-score permissions, and
validation claims. A completed positive response can only support future gate
preparation; it still cannot authorize a joint likelihood or cosmological
validation. The current completed response is
`QI_REVIEW_ACCEPTED_OR_CAVEATED_SOURCE_SIDE_NOT_VALIDATION`: the active
support factors are accepted only with caveats, zero-support branches remain
excluded, and validation-facing promotion remains blocked until a separate
covariance-aware joint likelihood or likelihood surrogate exists.

The corresponding likelihood-surrogate requirements gate is now frozen in:

```text
data/source_manifest/joint_likelihood_surrogate_requirements_policy_v1.csv
data/derived/joint_likelihood_surrogate_requirements_gate_v1.csv
data/derived/joint_likelihood_surrogate_requirements_gate_v1_summary.csv
docs/joint_likelihood_surrogate_requirements_gate_v1.md
scripts/build_joint_likelihood_surrogate_requirements_gate_v1.py
scripts/validate_joint_likelihood_surrogate_requirements_gate_v1.py
```

Its current verdict is
`JOINT_LIKELIHOOD_SURROGATE_REQUIREMENTS_FROZEN_SCORING_BLOCKED`. It records
that the Q_i source-side review, active-channel freeze, preflight signal, and
forbidden-field discipline pass, but endpoint scoring remains blocked by three
hard requirements: a joint covariance model, a single likelihood-surrogate
statistic, and a matched control suite under the same statistic.

The first hard blocker is narrowed by the covariance-model requirements gate:

```text
data/source_manifest/joint_covariance_model_policy_v1.csv
data/derived/joint_covariance_model_requirements_gate_v1.csv
data/derived/joint_covariance_model_requirements_gate_v1_summary.csv
docs/joint_covariance_model_requirements_gate_v1.md
scripts/build_joint_covariance_model_requirements_gate_v1.py
scripts/validate_joint_covariance_model_requirements_gate_v1.py
```

Its verdict is
`JOINT_COVARIANCE_MODEL_REQUIREMENTS_PARTIAL_BLOCKS_READY_CROSS_PROBE_BLOCKED`.
KiDS/COSEBIs has source-native full-covariance support; the observer/path and
DESI shape/readout blocks have only narrow, caveated surrogate covariance
support. Cross-probe covariance or a reviewed block-diagonal independence
attestation remains missing, so endpoint scoring is still disabled.

A block-diagonal independence reviewer handoff package is frozen in:

```text
data/source_manifest/joint_block_diagonal_independence_review_policy_v1.csv
data/derived/joint_block_diagonal_independence_review_response_template_v1.csv
data/derived/joint_block_diagonal_independence_review_package_v1.zip
data/derived/joint_block_diagonal_independence_review_package_v1.zip.sha256
data/derived/joint_block_diagonal_independence_review_package_v1_manifest.csv
data/derived/joint_block_diagonal_independence_review_package_v1_summary.csv
data/derived/joint_block_diagonal_independence_review_response_v1_summary.csv
docs/joint_block_diagonal_independence_review_package_v1.md
scripts/build_joint_block_diagonal_independence_review_package_v1.py
scripts/validate_joint_block_diagonal_independence_review_package_v1.py
scripts/validate_joint_block_diagonal_independence_review_response_v1.py
scripts/import_joint_block_diagonal_independence_review_response_v1.py
```

Its completed response is
`JOINT_BLOCK_DIAGONAL_PROTOCOL_SHELL_ALLOWED_CROSS_PROBE_OPEN_NOT_SCORING`.
The external reviewer accepts the active block scope and allows a
block-diagonal surrogate only as a future protocol shell. Cross-probe
independence remains open, and endpoint scoring, endpoint validation, and
cosmological validation remain disabled. A separate source-side
covariance/independence rationale is still required before any executable
single-statistic replay.

When a reviewer returns the completed CSV or a zip containing it, import it with:

```bash
python scripts/import_joint_block_diagonal_independence_review_response_v1.py /path/to/completed_response.csv
```

The importer refuses blank templates, partial responses, forbidden endpoint
inputs, endpoint-score permissions, and validation claims before replacing the
canonical response artifact.

The next source-side blocker package is now frozen in:

```text
data/source_manifest/joint_cross_probe_covariance_closure_review_policy_v1.csv
data/derived/joint_cross_probe_covariance_closure_review_response_template_v1.csv
data/derived/joint_cross_probe_covariance_closure_review_package_v1.zip
data/derived/joint_cross_probe_covariance_closure_review_package_v1.zip.sha256
data/derived/joint_cross_probe_covariance_closure_review_package_v1_manifest.csv
data/derived/joint_cross_probe_covariance_closure_review_package_v1_summary.csv
data/derived/joint_cross_probe_covariance_closure_review_response_v1_summary.csv
data/derived/joint_cross_probe_covariance_closure_review_completed_summary_v1.csv
data/derived/joint_cross_probe_covariance_closure_review_validation_log_v1.txt
docs/joint_cross_probe_covariance_closure_review_package_v1.md
docs/joint_cross_probe_covariance_closure_review_notes_v1.md
scripts/build_joint_cross_probe_covariance_closure_review_package_v1.py
scripts/validate_joint_cross_probe_covariance_closure_review_package_v1.py
scripts/validate_joint_cross_probe_covariance_closure_review_response_v1.py
scripts/import_joint_cross_probe_covariance_closure_review_response_v1.py
```

This package asks the reviewer to close, caveat, or keep open the
cross-probe covariance/independence condition. It allows two source-side
routes only: a named source-native/source-frozen cross-probe covariance product,
or a source-side block-diagonal independence rationale. It contains no endpoint
residuals, no new endpoint scores, and no fit statistics.

The completed response now records
`JOINT_BLOCK_DIAGONAL_INDEPENDENCE_PRECONDITION_CAVEATED_CLOSED_NOT_SCORING`.
No source-native cross-probe covariance product is available. The reviewer
accepts a caveated block-diagonal independence precondition only for a later
separately authorized scoring package. Shared sky/mask, redshift-kernel,
cosmology/nuisance, calibration, and non-population covariance caveats must be
carried forward.

When a reviewer returns the completed CSV or a zip containing it, import it
with:

```bash
python scripts/import_joint_cross_probe_covariance_closure_review_response_v1.py /path/to/completed_response.csv
```

The importer refuses incomplete responses, forbidden endpoint inputs,
endpoint-score permissions, endpoint-validation claims, and cosmological
validation claims before replacing the canonical response artifact.

For a reviewer without repository access, use the standalone handoff package:

```text
data/derived/joint_cross_probe_covariance_closure_reviewer_handoff_package_v1.zip
data/derived/joint_cross_probe_covariance_closure_reviewer_handoff_package_v1.zip.sha256
data/derived/joint_cross_probe_covariance_closure_reviewer_handoff_package_v1_manifest.csv
data/derived/joint_cross_probe_covariance_closure_reviewer_handoff_package_v1_summary.csv
data/derived/REVIEWER_README_JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_V1.md
scripts/build_joint_cross_probe_covariance_closure_reviewer_handoff_package_v1.py
scripts/validate_joint_cross_probe_covariance_closure_reviewer_handoff_package_v1.py
```

The same zip is copied for convenience to:

```text
/Users/jolcsak/Downloads/joint_cross_probe_covariance_closure_reviewer_handoff_package_v1.zip
```

The source-side requirements behind this blocker are frozen in:

```text
data/source_manifest/joint_cross_probe_covariance_source_requirements_policy_v1.csv
data/derived/joint_cross_probe_covariance_source_requirements_v1.csv
data/derived/joint_cross_probe_covariance_source_requirements_v1_summary.csv
docs/joint_cross_probe_covariance_source_requirements_v1.md
scripts/build_joint_cross_probe_covariance_source_requirements_v1.py
scripts/validate_joint_cross_probe_covariance_source_requirements_v1.py
```

The current verdict is
`JOINT_CROSS_PROBE_CAVEATED_INDEPENDENCE_PRECONDITION_CLOSED_SCORING_AUTH_REQUIRED`.
It records eight source-side requirements: active block scope, cross-probe
covariance product, shared sky/mask overlap, redshift-kernel overlap,
shared cosmology/nuisance terms, block-diagonal caveats, same-statistic
candidate/control binding, and forbidden-field discipline. The forbidden-field
discipline and caveated independence route now pass. The cross-probe covariance
product route remains unavailable, and executable scoring remains blocked until
a separate scoring authorization package binds the same statistic, covariance
blocks, caveats, and matched controls.

That separate scoring-authorization review package has now been completed:

```text
data/source_manifest/joint_block_diagonal_scoring_authorization_review_policy_v1.csv
data/derived/joint_block_diagonal_scoring_authorization_review_response_template_v1.csv
data/derived/joint_block_diagonal_scoring_authorization_review_response_v1.csv
data/derived/joint_block_diagonal_scoring_authorization_review_response_v1_summary.csv
data/derived/joint_block_diagonal_scoring_authorization_review_completed_summary_v1.csv
data/derived/joint_block_diagonal_scoring_authorization_review_validation_log_v1.txt
data/derived/joint_block_diagonal_scoring_authorization_review_package_v1.zip
data/derived/joint_block_diagonal_scoring_authorization_review_package_v1.zip.sha256
data/derived/joint_block_diagonal_scoring_authorization_review_package_v1_manifest.csv
data/derived/joint_block_diagonal_scoring_authorization_review_package_v1_summary.csv
docs/joint_block_diagonal_scoring_authorization_review_package_v1.md
docs/joint_block_diagonal_scoring_authorization_review_notes_v1.md
scripts/build_joint_block_diagonal_scoring_authorization_review_package_v1.py
scripts/validate_joint_block_diagonal_scoring_authorization_review_package_v1.py
scripts/validate_joint_block_diagonal_scoring_authorization_review_response_v1.py
scripts/import_joint_block_diagonal_scoring_authorization_review_response_v1.py
```

The completed response authorizes preparation of a separate guarded
permission-only joint replay package under the caveated block-diagonal
precondition. It does not authorize direct scoring and does not claim endpoint
or cosmological validation.

That next guarded permission-replay authorization package is prepared and now
has a completed external response:

```text
data/source_manifest/joint_guarded_permission_replay_authorization_policy_v1.csv
data/derived/joint_guarded_permission_replay_authorization_response_template_v1.csv
data/derived/joint_guarded_permission_replay_authorization_package_v1.zip
data/derived/joint_guarded_permission_replay_authorization_package_v1.zip.sha256
data/derived/joint_guarded_permission_replay_authorization_package_v1_manifest.csv
data/derived/joint_guarded_permission_replay_authorization_package_v1_summary.csv
data/derived/joint_guarded_permission_replay_authorization_response_v1.csv
data/derived/joint_guarded_permission_replay_authorization_response_v1_summary.csv
data/derived/joint_guarded_permission_replay_authorization_review_completed_summary_v1.csv
data/derived/joint_guarded_permission_replay_authorization_review_validation_log_v1.txt
docs/joint_guarded_permission_replay_authorization_package_v1.md
docs/joint_guarded_permission_replay_authorization_review_notes_v1.md
scripts/build_joint_guarded_permission_replay_authorization_package_v1.py
scripts/validate_joint_guarded_permission_replay_authorization_package_v1.py
scripts/validate_joint_guarded_permission_replay_authorization_response_v1.py
scripts/import_joint_guarded_permission_replay_authorization_response_v1.py
```

The package asks whether a run-template package may be prepared with candidate
and controls bound to the same block-diagonal statistic, the same covariance
blocks, and the same caveats. It still does not execute replay/scoring. A copy
is available at:

```text
/Users/jolcsak/Downloads/joint_guarded_permission_replay_authorization_package_v1.zip
```

When a completed reviewer response returns, it must be imported through:

```bash
python scripts/import_joint_guarded_permission_replay_authorization_response_v1.py \
  /path/to/completed_response.zip
```

The importer refuses incomplete rows, forbidden endpoint inputs, direct
execution permission, endpoint-validation claims, and cosmological-validation
claims.

The completed response decision is:

```text
AUTHORIZE_GUARDED_PERMISSION_REPLAY_PACKAGE_PREPARATION_ONLY_NOT_EXECUTION_NOT_SCORING_NOT_VALIDATION
```

This authorizes only a separate guarded run-template gate.  That template is
now frozen at:

```text
data/source_manifest/joint_guarded_replay_run_template_v1.csv
data/derived/joint_guarded_replay_run_template_v1_summary.csv
docs/joint_guarded_replay_run_template_v1.md
scripts/build_joint_guarded_replay_run_template_v1.py
scripts/validate_joint_guarded_replay_run_template_v1.py
```

It fixes the active block order, shared block-diagonal statistic, same
block-weight rule, same covariance/caveat discipline, and eight matched-control
families.  Its status is
`JOINT_GUARDED_REPLAY_RUN_TEMPLATE_READY_NOT_EXECUTED`; direct execution,
endpoint scoring, endpoint validation, and cosmological validation all remain
false.

A further external reviewer package has been prepared for this run-template
itself:

```text
data/source_manifest/joint_guarded_replay_run_template_authorization_policy_v1.csv
data/derived/joint_guarded_replay_run_template_authorization_response_template_v1.csv
data/derived/joint_guarded_replay_run_template_authorization_package_v1.zip
data/derived/joint_guarded_replay_run_template_authorization_package_v1.zip.sha256
data/derived/joint_guarded_replay_run_template_authorization_package_v1_manifest.csv
data/derived/joint_guarded_replay_run_template_authorization_package_v1_summary.csv
docs/joint_guarded_replay_run_template_authorization_package_v1.md
scripts/build_joint_guarded_replay_run_template_authorization_package_v1.py
scripts/validate_joint_guarded_replay_run_template_authorization_package_v1.py
scripts/validate_joint_guarded_replay_run_template_authorization_response_v1.py
scripts/import_joint_guarded_replay_run_template_authorization_response_v1.py
```

This package is blank and reviewer-not-completed.  It asks only whether the
frozen template may be used as the basis for a later executable
permission-only replay.  It still does not execute replay, does not produce
endpoint scores, and does not claim endpoint or cosmological validation.
The reviewer-facing instructions are also copied to:

```text
/Users/jolcsak/Downloads/joint_guarded_replay_run_template_authorization_reviewer_instructions_v1.md
```

When a completed response returns, it must be imported through:

```bash
python scripts/import_joint_guarded_replay_run_template_authorization_response_v1.py \
  /path/to/completed_response.csv-or-zip
```

The importer refuses incomplete rows, forbidden endpoint inputs, direct
execution permission, endpoint scoring, endpoint-validation claims, and
cosmological-validation claims.

The current execution blocker is recorded in:

```text
data/derived/joint_guarded_replay_execution_blocker_status_v1.csv
data/derived/joint_guarded_replay_execution_blocker_status_v1_summary.csv
docs/joint_guarded_replay_execution_blocker_status_v1.md
scripts/build_joint_guarded_replay_execution_blocker_status_v1.py
scripts/validate_joint_guarded_replay_execution_blocker_status_v1.py
```

At this stage the blocker is
`guarded_runner_and_execution_authorization_not_yet_prepared`.  The completed
run-template authorization response has been imported and authorizes only
preparation of a separate execution plan:

```text
data/derived/joint_guarded_replay_run_template_authorization_response_v1.csv
data/derived/joint_guarded_replay_run_template_authorization_response_v1_summary.csv
data/derived/joint_guarded_replay_run_template_authorization_review_completed_summary_v1.csv
data/derived/joint_guarded_replay_run_template_authorization_review_validation_log_v1.txt
docs/joint_guarded_replay_run_template_authorization_review_notes_v1.md
```

The execution plan is now frozen at:

```text
data/source_manifest/joint_guarded_replay_execution_plan_v1.csv
data/derived/joint_guarded_replay_execution_plan_v1_summary.csv
docs/joint_guarded_replay_execution_plan_v1.md
scripts/build_joint_guarded_replay_execution_plan_v1.py
scripts/validate_joint_guarded_replay_execution_plan_v1.py
```

It is still plan-only.  The runner does not exist yet, and a separate execution
authorization gate is still required before any permission-only replay can run.
The runner and output validator are now prepared, but the replay is still
blocked until the separate execution authorization response is completed:

```text
scripts/run_joint_guarded_replay_permission_only_v1.py
scripts/validate_joint_guarded_replay_permission_only_v1.py
data/source_manifest/joint_guarded_replay_execution_authorization_policy_v1.csv
data/derived/joint_guarded_replay_execution_authorization_response_template_v1.csv
data/derived/joint_guarded_replay_execution_authorization_package_v1.zip
data/derived/joint_guarded_replay_execution_authorization_package_v1.zip.sha256
data/derived/joint_guarded_replay_execution_authorization_package_v1_manifest.csv
data/derived/joint_guarded_replay_execution_authorization_package_v1_summary.csv
docs/joint_guarded_replay_execution_authorization_package_v1.md
scripts/build_joint_guarded_replay_execution_authorization_package_v1.py
scripts/validate_joint_guarded_replay_execution_authorization_package_v1.py
scripts/import_joint_guarded_replay_execution_authorization_response_v1.py
scripts/validate_joint_guarded_replay_execution_authorization_response_v1.py
```

The current blocker is now `execution_authorization_response_missing`.

The matched-control requirements are now specified in:

```text
data/source_manifest/joint_matched_control_suite_requirements_policy_v1.csv
data/derived/joint_matched_control_suite_requirements_gate_v1.csv
data/derived/joint_matched_control_suite_requirements_gate_v1_summary.csv
docs/joint_matched_control_suite_requirements_gate_v1.md
scripts/build_joint_matched_control_suite_requirements_gate_v1.py
scripts/validate_joint_matched_control_suite_requirements_gate_v1.py
```

Its verdict is
`JOINT_MATCHED_CONTROL_SUITE_REQUIREMENTS_FROZEN_IMPLEMENTATION_BLOCKED`.
The gate names the required shuffled-channel, wrong-channel, sign-flip,
block-drop, null/readout, leakage, shared-statistic, and covariance-binding
controls. It does not run them. All controls remain blocked until the
covariance/independence review and single joint statistic are closed.

The matched-control implementation scaffold is now specified in:

```text
data/derived/joint_matched_control_suite_implementation_scaffold_v1.csv
data/derived/joint_matched_control_suite_implementation_scaffold_v1_summary.csv
docs/joint_matched_control_suite_implementation_scaffold_v1.md
scripts/build_joint_matched_control_suite_implementation_scaffold_v1.py
scripts/validate_joint_matched_control_suite_implementation_scaffold_v1.py
```

Its verdict is
`JOINT_MATCHED_CONTROL_SUITE_IMPLEMENTATION_SCAFFOLD_FROZEN_NOT_RUN`.
The scaffold declares future builder names, validators, output artifacts,
freeze inputs, and minimum control-count rules for the eight families. It still
does not create control vectors, residuals, likelihoods, fit statistics, or
endpoint scores.

The single-statistic binding prerequisites are recorded in:

```text
data/derived/joint_single_statistic_binding_prerequisites_v1.csv
data/derived/joint_single_statistic_binding_prerequisites_v1_summary.csv
docs/joint_single_statistic_binding_prerequisites_v1.md
scripts/build_joint_single_statistic_binding_prerequisites_v1.py
scripts/validate_joint_single_statistic_binding_prerequisites_v1.py
```

This ledger freezes the active-channel order, row-scope artifact,
score-source artifact, covariance object, and nuisance/amplitude rule that a
future single joint statistic must bind. It does not define that statistic and
does not run any replay. Its verdict is
`JOINT_SINGLE_STATISTIC_BINDING_PREREQUISITES_FROZEN_PROTOCOL_BLOCKED`.
All three active channels now have explicit row-scope and score-source
artifacts present in the repository; the remaining blockers are no longer
missing channel artifacts, but covariance/independence closure and the single
joint-statistic protocol itself.

The current residual-blind common source-feature export is recorded in:

```text
data/derived/joint_common_source_feature_export_v5.csv
data/derived/joint_common_source_feature_export_v5_summary.csv
docs/joint_common_source_feature_export_v5.md
scripts/build_joint_common_source_feature_export_v5.py
scripts/validate_joint_common_source_feature_export_v5.py
data/derived/kids1000_cosebis_null_control_row_vectors_v1.csv.gz
data/derived/kids1000_cosebis_null_control_row_vectors_v1_summary.csv
scripts/build_kids1000_cosebis_null_control_row_vectors_v1.py
scripts/validate_kids1000_cosebis_null_control_row_vectors_v1.py
```

This export contains 6635 feature rows across DESI, observer/path, and
KiDS/COSEBIs, plus a compressed 302400-row KiDS null-control row-vector
artifact. It replaces the earlier KiDS summary-only caveat with source-frozen
KiDS candidate row features and row-level null-control input availability.
This closes the source-feature input blocker for a future row-level penalty,
but it still does not define or run that penalty, authorize endpoint replay,
claim validation, or permit `T_joint` rescoring.

The corresponding non-scoring row-level penalty protocol shell is recorded in:

```text
data/derived/joint_row_level_penalty_protocol_shell_v2.csv
data/derived/joint_row_level_penalty_protocol_shell_v2_summary.csv
docs/joint_row_level_penalty_protocol_shell_v2.md
scripts/build_joint_row_level_penalty_protocol_shell_v2.py
scripts/validate_joint_row_level_penalty_protocol_shell_v2.py
data/derived/joint_row_level_penalty_block_weight_binding_shell_v1.csv
data/derived/joint_row_level_penalty_block_weight_binding_shell_v1_summary.csv
docs/joint_row_level_penalty_block_weight_binding_shell_v1.md
scripts/build_joint_row_level_penalty_block_weight_binding_shell_v1.py
scripts/validate_joint_row_level_penalty_block_weight_binding_shell_v1.py
data/derived/joint_row_level_penalty_protocol_shell_v3.csv
data/derived/joint_row_level_penalty_protocol_shell_v3_summary.csv
docs/joint_row_level_penalty_protocol_shell_v3.md
scripts/build_joint_row_level_penalty_protocol_shell_v3.py
scripts/validate_joint_row_level_penalty_protocol_shell_v3.py
data/derived/joint_symbolic_row_level_penalty_formula_shell_v1.csv
data/derived/joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv
docs/joint_symbolic_row_level_penalty_formula_shell_v1.md
scripts/build_joint_symbolic_row_level_penalty_formula_shell_v1.py
scripts/validate_joint_symbolic_row_level_penalty_formula_shell_v1.py
data/derived/joint_row_level_penalty_protocol_shell_v4.csv
data/derived/joint_row_level_penalty_protocol_shell_v4_summary.csv
docs/joint_row_level_penalty_protocol_shell_v4.md
scripts/build_joint_row_level_penalty_protocol_shell_v4.py
scripts/validate_joint_row_level_penalty_protocol_shell_v4.py
data/derived/joint_channel_local_source_normalization_rule_v1.csv
data/derived/joint_channel_local_source_normalization_rule_v1_summary.csv
data/derived/joint_candidate_control_symmetric_normalized_feature_transform_v1.csv.gz
data/derived/joint_candidate_control_symmetric_normalized_feature_transform_v1_summary.csv
scripts/build_joint_channel_local_source_normalization_rule_v1.py
scripts/validate_joint_channel_local_source_normalization_rule_v1.py
scripts/build_joint_candidate_control_symmetric_normalized_feature_transform_v1.py
scripts/validate_joint_candidate_control_symmetric_normalized_feature_transform_v1.py
```

It records `source_feature_inputs_complete=true`,
`channel_local_normalization_frozen=true`, and
`candidate_control_symmetric_transform_built=true`. The v3 shell additionally
records `covariance_or_block_weight_binding_frozen=true` by binding the
normalized transform to the caveated block-diagonal route with an equal-channel
preweight shell. It still keeps
`penalty_formula_defined=false`, `penalty_computed=false`, and
`numeric_t_joint_rescoring_allowed=false`. The remaining protocol blocker is
now the symbolic row-level penalty formula itself, which must be defined in a
separate non-scoring gate before any numeric penalty or score change can be
proposed.

The v4 shell freezes that symbolic formula without computing it:

```text
P_i(a) = omega_i * mean_{r,f}(z_{i,a,r,f}^2)
P_row(a) = sum_i P_i(a)
T_joint_penalized(a) = T_joint(a) + lambda_row * P_row(a)
```

Here `z_{i,a,r,f}` is the already frozen normalized source feature for channel
`i`, candidate/control alternative `a`, row `r`, and feature `f`. The coefficient
`lambda_row` remains symbolic only: no numeric value is chosen, fitted, inferred,
or applied. The v4 shell records `penalty_formula_defined=true`, but still keeps
`penalty_computed=false`, `numeric_penalty_values_written=false`, and
`numeric_t_joint_rescoring_allowed=false`. The next blocker is now a separate
numeric-penalty computation authorization review package.

That authorization package is prepared, but not completed:

```text
data/source_manifest/joint_row_level_numeric_penalty_authorization_review_policy_v1.csv
data/derived/joint_row_level_numeric_penalty_authorization_review_response_template_v1.csv
data/derived/joint_row_level_numeric_penalty_authorization_review_package_v1.zip
data/derived/joint_row_level_numeric_penalty_authorization_review_package_v1.zip.sha256
data/derived/joint_row_level_numeric_penalty_authorization_review_package_v1_manifest.csv
data/derived/joint_row_level_numeric_penalty_authorization_review_package_v1_summary.csv
docs/joint_row_level_numeric_penalty_authorization_review_package_v1.md
scripts/build_joint_row_level_numeric_penalty_authorization_review_package_v1.py
scripts/validate_joint_row_level_numeric_penalty_authorization_review_package_v1.py
scripts/validate_joint_row_level_numeric_penalty_authorization_review_response_v1.py
scripts/import_joint_row_level_numeric_penalty_authorization_review_response_v1.py
data/derived/joint_row_level_numeric_penalty_blocker_status_v1.csv
data/derived/joint_row_level_numeric_penalty_blocker_status_v1_summary.csv
docs/joint_row_level_numeric_penalty_blocker_status_v1.md
scripts/build_joint_row_level_numeric_penalty_blocker_status_v1.py
scripts/validate_joint_row_level_numeric_penalty_blocker_status_v1.py
scripts/run_joint_row_level_numeric_penalty_values_guarded_v1.py
data/derived/joint_row_level_numeric_penalty_preflight_v1.csv
data/derived/joint_row_level_numeric_penalty_preflight_v1_summary.csv
docs/joint_row_level_numeric_penalty_preflight_v1.md
scripts/check_joint_row_level_numeric_penalty_preflight_v1.py
```

The package was completed and imported. It contains no endpoint residuals, no
new endpoint scores, no fit statistics, no numeric penalty values, and no
numeric `lambda_row`. The completed reviewer response authorizes only a
separate numeric penalty-value package for `P_i(a)` and `P_row(a)`. It does not
authorize numeric `lambda_row`, endpoint replay, endpoint validation, or
`T_joint` rescoring.

When the completed reviewer response is returned, validate/import it with:

```bash
python scripts/validate_joint_row_level_numeric_penalty_authorization_review_response_v1.py /path/to/completed_response.csv --summary-out /tmp/joint_rnp_response_summary.csv
python scripts/import_joint_row_level_numeric_penalty_authorization_review_response_v1.py /path/to/completed_response.csv
```

The importer refuses incomplete templates, any `forbidden_inputs_used=true`,
numeric `lambda_row` authorization, or direct `T_joint` rescoring authorization.
The current machine-readable blocker status is
`NUMERIC_PENALTY_VALUES_READY_FOR_SEPARATE_PACKAGE_NOT_RESCORING`: the reviewer
response has been imported, and the next allowed action is a separate numeric
penalty-value package without `lambda_row` and without `T_joint` rescoring.

The guarded runner enforces this boundary:

```bash
python scripts/run_joint_row_level_numeric_penalty_values_guarded_v1.py
```

In the current repository state this command must exit ready-for-separate-package.
It is only a guard: it does not compute values itself, and it still requires a
separate numeric penalty value package.

A one-command preflight verifies the whole boundary:

```bash
python scripts/check_joint_row_level_numeric_penalty_preflight_v1.py
```

The current expected verdict is
`PREFLIGHT_PASS_READY_FOR_SEPARATE_NUMERIC_PENALTY_PACKAGE_NOT_RESCORING`.

A block-diagonal likelihood-surrogate protocol shell is now recorded in:

```text
data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1.csv
data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1_summary.csv
docs/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1.md
scripts/build_joint_block_diagonal_likelihood_surrogate_protocol_shell_v1.py
scripts/validate_joint_block_diagonal_likelihood_surrogate_protocol_shell_v1.py
```

Its verdict is
`JOINT_BLOCK_DIAGONAL_PROTOCOL_SHELL_FROZEN_COVARIANCE_STILL_OPEN_NOT_SCORING`.
The shell declares only the future algebraic form
`Q_joint^BD = sum_i r_i^T C_i^{-1} r_i` and the rule that candidate and
matched controls must use the same row scopes, covariance blocks, nuisance
rules, and statistic. It does not read endpoint residuals, invert new
covariances, compute scores, or authorize replay. It remains non-executable
until cross-probe covariance or independence is separately closed and a
separate single-statistic scoring authorization is supplied.

A standalone reviewer handoff package is also available for reviewers who do
not have repository access:

```text
data/derived/joint_best_justified_qi_review_package_v1.zip
data/derived/joint_best_justified_qi_review_package_v1.zip.sha256
```

The zip contains reviewer instructions, the `Q_i` requirements CSV, a fillable
response template, and the source-side manifest/summary files needed for the
review. It is a source-side review package only; it is not an endpoint replay
authorization and not a validation package.

The detailed route-by-route ledgers that were too log-like for the main
manuscript are preserved in the supplementary source file:

```text
paper10_submission_source/supplement_route_ledgers.tex
```

The main manuscript keeps the narrative, status ledgers, best-justified joint
kernel, and validation boundary; the supplement preserves the full audit trail.

## Reproduce

```bash
python scripts/reproduce.py
```

The reproduction script compiles the manuscript with `tectonic`, validates the
source-freeze and channel manifests, builds the arXiv source package, and runs
smoke tests.

For release verification, prefer the command above or the focused public
reproducibility tests. The full `python -m pytest -q` suite is a developer
regeneration path as well as a validator: it may rebuild reviewer packages,
figures, and checksum ledgers before validation. Those regenerated artifacts are
kept claim-bounded, but they should be reviewed before being committed.

To reproduce the current headline preflight artifacts directly:

```bash
python scripts/run_joint_best_justified_kernel_score_v1.py
python scripts/run_joint_best_justified_kernel_robustness_v1.py
python scripts/build_joint_best_justified_kernel_figure_v1.py
python scripts/validate_joint_best_justified_qi_review_package_v1.py
python scripts/validate_joint_best_justified_qi_review_response_v1.py
```

Then check:

```text
data/derived/joint_best_justified_kernel_score_v1_summary.csv
data/derived/joint_best_justified_kernel_robustness_v1_summary.csv
paper10_submission_source/figures/fig_joint_best_justified_kernel_v1.pdf
```

## arXiv Source Package

`arxiv_submission_source.zip` is generated from `paper10_submission_source/`
and excludes `main.pdf` plus TeX build byproducts.

## Online Data Dependencies

The one-command reproduction path does not perform live online data acquisition.
Future source-acquisition scripts should document exact URLs, versions, hashes
where possible, and redistribution boundaries.

For provenance, the repository includes a compact cache of the official source
landing pages listed in the manifest:

```bash
python scripts/acquire_source_pages.py
python scripts/validate_cached_source_pages.py
```

The acquisition script is intentionally separate from `scripts/reproduce.py`;
reproduction validates the committed cache hashes instead of depending on live
network access.

Current source manifest status:

- all required source families now have a candidate public source route,
- official source landing pages are cached with SHA-256 hashes,
- no source row is `FETCHED_FROZEN`,
- no endpoint scoring is allowed from this scaffold.

The first source-selection audit is recorded in:

```text
docs/source_selection_audit_001.md
```

The product-freeze preflight plan is recorded in:

```text
data/source_manifest/paper10_product_freeze_plan.csv
docs/product_freeze_plan.md
```

It declares the product roles, transformation-rule IDs, covariance/mask policy
requirements, and `endpoint_allowed=false` status for every planned product.

The next source-native void/web upgrade gate is recorded in:

```text
data/source_manifest/void_web_source_native_freeze_plan_v1.csv
docs/void_web_source_native_freeze_plan_v1.md
scripts/validate_void_web_source_native_freeze_plan_v1.py
```

It declares one preferred VAST/SDSS DR7 void-catalogue route and one SDSS DR17
MCPM cosmic-web route for replacing the proxy `W_void` and `W_web` bases. Both
rows are `SOURCE_NATIVE_CANDIDATE_SELECTED_NOT_FETCHED`, and both keep
`endpoint_scoring_allowed=false`.

The first fetched source-native void/web products are recorded in:

```text
data/source_manifest/void_web_source_native_frozen_products_v1.csv
data/derived/void_web_source_native_inventory_v1.csv
docs/void_web_source_native_products_v1.md
scripts/acquire_void_web_source_native_products_v1.py
scripts/validate_void_web_source_native_products_v1.py
scripts/build_void_web_source_native_inventory_v1.py
scripts/validate_void_web_source_native_inventory_v1.py
```

This freezes a VAST/SDSS DR7 Planck2018 maximal void table, the associated NSA
mask, the SDSS DR17 MCPM SlimeMold galaxy catalogue, and the provider sha1sum
file. The inventory records `void_rows=1163` and
`fits_bintable_rows=638820`. These products remain endpoint-disabled because
the catalogue-to-scoring transform is not yet frozen.

The first source-native transform and distance-only pilot are recorded in:

```text
data/source_manifest/void_web_source_native_transform_rule_v1.csv
data/derived/pantheon_void_web_source_native_design_matrix_v1.csv
data/source_manifest/pantheon_void_web_source_native_full_cov_pilot_v1.csv
data/derived/pantheon_void_web_source_native_full_cov_pilot_v1_summary.csv
docs/void_web_source_native_transform_rule_v1.md
docs/pantheon_void_web_source_native_design_matrix_v1.md
docs/pantheon_void_web_source_native_full_cov_pilot_v1.md
```

The design matrix is not scored and contains no residuals. The separate
full-covariance pilot remains
`VOID_WEB_SOURCE_NATIVE_FULL_COV_PILOT_NOT_VALIDATION`. It improves
Pantheon-only full-covariance chi-square by `0.508` relative to the
flat-Lambda-CDM branch, but loses under AIC by `3.492`, and the deterministic
shuffled control can still do better in chi-square. This is therefore a useful
source-native pipeline step, not a detection or endpoint validation.

The first growth-side multi-probe step is recorded in:

```text
data/source_manifest/sdss_final_bao_rsd_growth_summary_v1.csv
data/source_manifest/growth_web_source_native_transform_rule_v1.csv
data/derived/growth_web_source_native_design_matrix_v1.csv
data/source_manifest/growth_web_source_native_pilot_v1.csv
data/derived/growth_web_source_native_pilot_v1_summary.csv
docs/sdss_final_bao_rsd_growth_summary_v1.md
docs/growth_web_source_native_design_matrix_v1.md
docs/growth_web_source_native_pilot_v1.md
```

This freezes six SDSS final BAO/RSD `f sigma8(z)` summary points and attaches
the source-native `W_web` basis to them. The pilot is diagonal-summary only. It
improves chi-square by `0.306`, but loses under AIC by `1.694`, and the
wrong-sign control is equally good on the symmetric pilot grid. This is a first
growth-side stress test, not a growth endpoint validation.

The first official-covariance BAO/RSD growth block is recorded in:

```text
data/source_manifest/sdss_multitracer_bao_rsd_products_v1.csv
data/source_manifest/sdss_multitracer_bao_rsd_transform_rule_v1.csv
data/derived/sdss_multitracer_bao_rsd_design_matrix_v1.csv
data/source_manifest/sdss_multitracer_bao_rsd_full_cov_pilot_v1.csv
data/derived/sdss_multitracer_bao_rsd_full_cov_pilot_v1_summary.csv
docs/sdss_multitracer_bao_rsd_products_v1.md
docs/sdss_multitracer_bao_rsd_transform_rule_v1.md
docs/sdss_multitracer_bao_rsd_design_matrix_v1.md
docs/sdss_multitracer_bao_rsd_full_cov_pilot_v1.md
```

This freezes the official SDSS DR16 LRG+ELG multi-tracer BAO/RSD compressed
products and uses the Fourier-space six-component vector with its official
6x6 covariance. In this pilot the web channel modifies only the `f sigma8`
entries while the BAO distance entries remain in the shared covariance block.
The result is effectively neutral: chi-square improves by only `0.010`, AIC
loses by `1.990`, and the wrong-sign control is equally good. This is a useful
multi-probe covariance gate and a seminegative control, not evidence for a
preferred web-growth direction.

The first CMB-safety support check is recorded in:

```text
data/source_manifest/cmb_safety_lowz_support_v1.csv
data/derived/cmb_safety_lowz_support_v1.csv
data/derived/cmb_safety_lowz_support_v1_summary.csv
docs/cmb_safety_lowz_support_v1.md
scripts/build_cmb_safety_lowz_support_v1.py
scripts/validate_cmb_safety_lowz_support_v1.py
```

This is not a CMB likelihood and contains no CMB map data. It checks only that
the currently active late-time source-native void/web bases vanish above a
conservative safety floor (`z=10`) and at a recombination proxy (`z=1089.92`).
The check passes, so the current late-time pilots do not directly modify the
early-universe safety regime.

The FLRW-audited void/web endpoint-readiness ledger is recorded in:

```text
data/source_manifest/void_web_endpoint_readiness_after_flrw_audit_policy_v1.csv
data/derived/void_web_endpoint_readiness_after_flrw_audit_v1.csv
data/derived/void_web_endpoint_readiness_after_flrw_audit_v1_summary.csv
docs/void_web_endpoint_readiness_after_flrw_audit_v1.md
scripts/build_void_web_endpoint_readiness_after_flrw_audit_v1.py
scripts/validate_void_web_endpoint_readiness_after_flrw_audit_v1.py
```

This ledger combines the source-native Pantheon distance pilot, the SDSS growth
pilot, the official-covariance SDSS multi-tracer pilot, the CMB-safety support
check, and the FLRW-consistency channel audit. It records
`endpoint_ready_count=0` and `support_ready_count=1`: the CMB-safety support
passes, but the scoring-facing void/web pilots remain blocked by AIC loss,
shuffled or wrong-sign controls, and near-zero full-covariance signal. The next
required gate is a predeclared combined multiblock endpoint protocol with joint
nulls and a unified information criterion.

That next protocol shell is frozen in:

```text
data/source_manifest/void_web_combined_multiblock_endpoint_protocol_v1.csv
docs/void_web_combined_multiblock_endpoint_protocol_v1.md
scripts/validate_void_web_combined_multiblock_endpoint_protocol_v1.py
```

It declares the future combined observable blocks, active void/web channels,
disabled path/time channels, shared AIC shell, joint null controls, block-drop
controls, and forbidden endpoint-leakage fields. It remains
`scoring_allowed=false` and computes no likelihood, residual, information
criterion, endpoint score, or validation result.

The authorization-review template for that future combined run is recorded in:

```text
data/source_manifest/void_web_combined_multiblock_endpoint_authorization_review_policy_v1.csv
data/derived/void_web_combined_multiblock_endpoint_authorization_review_response_template_v1.csv
data/derived/void_web_combined_multiblock_endpoint_authorization_review_template_v1_summary.csv
docs/void_web_combined_multiblock_endpoint_authorization_review_v1.md
scripts/build_void_web_combined_multiblock_endpoint_authorization_review_template_v1.py
scripts/validate_void_web_combined_multiblock_endpoint_authorization_review_template_v1.py
```

The template is intentionally uncompleted and keeps `endpoint_run_allowed=false`.
A future combined endpoint run requires a separate accepted response that uses
only protocol/readiness/source-side artifacts, not residuals, fit statistics,
or post-hoc block/channel choices.

For reviewers without repository access, the authorization package is:

```text
REVIEWER_README_VOID_WEB_COMBINED_ENDPOINT_AUTHORIZATION.md
data/derived/void_web_combined_multiblock_endpoint_authorization_review_package_v1.zip
data/derived/void_web_combined_multiblock_endpoint_authorization_review_package_v1.zip.sha256
data/derived/void_web_combined_multiblock_endpoint_authorization_review_package_v1_manifest.csv
data/derived/void_web_combined_multiblock_endpoint_authorization_review_package_v1_summary.csv
scripts/build_void_web_combined_multiblock_endpoint_authorization_review_package_v1.py
scripts/validate_void_web_combined_multiblock_endpoint_authorization_review_package_v1.py
```

The package contains only protocol, readiness, source-grounding, FLRW-audit,
and blank authorization-template materials. It explicitly excludes endpoint
residuals, endpoint scores, and fit statistics.

The completed independent authorization response is recorded in:

```text
data/derived/void_web_combined_multiblock_endpoint_authorization_review_response_v1.csv
data/derived/void_web_combined_multiblock_endpoint_authorization_review_response_v1_summary.csv
data/derived/void_web_combined_multiblock_endpoint_authorization_review_response_v1_validation_report.txt
docs/void_web_combined_multiblock_endpoint_authorization_review_response_v1.md
scripts/validate_void_web_combined_multiblock_endpoint_authorization_review_response_v1.py
```

Its decision is `GO_COMBINED_VOID_WEB_ENDPOINT_PERMISSION_ONLY`. This permits
one separate, predeclared combined void/web endpoint run under the frozen
protocol. It does not promote the existing isolated pilots, does not score this
package, and keeps `physical_validation_claimed=false`.

The authorized combined endpoint run is recorded in:

```text
data/source_manifest/void_web_combined_multiblock_authorized_endpoint_run_v1.csv
data/derived/void_web_combined_multiblock_authorized_endpoint_v1_summary.csv
data/derived/void_web_combined_multiblock_authorized_endpoint_v1_grid.csv
data/derived/void_web_combined_multiblock_authorized_endpoint_v1_block_drop.csv
docs/void_web_combined_multiblock_authorized_endpoint_v1.md
scripts/run_void_web_combined_multiblock_authorized_endpoint_v1.py
scripts/validate_void_web_combined_multiblock_authorized_endpoint_v1.py
```

This endpoint result is preserved as a weak/negative combined result, not a
validation. The source-native void/web candidate improves chi-square slightly
relative to the baseline (`delta_chi2=-0.32825117`), but is worse by AIC/BIC
(`delta_aic=3.67174883`, `delta_bic=14.13576949`) and does not beat the best
deterministic shuffled void/web control. The next step is diagnostic rather than
claim promotion.

The first diagnostic ledger for this weak/negative result is:

```text
data/derived/void_web_combined_endpoint_diagnostics_v1_summary.csv
data/derived/void_web_combined_endpoint_diagnostics_v1_branch_summary.csv
data/derived/void_web_combined_endpoint_diagnostics_v1_block_drop_summary.csv
docs/void_web_combined_endpoint_diagnostics_v1.md
scripts/build_void_web_combined_endpoint_diagnostics_v1.py
scripts/validate_void_web_combined_endpoint_diagnostics_v1.py
```

Its current failure-mode verdict is
`void_channel_inactive_and_shuffled_control_marginally_better`: the best
combined candidate has `omega_void=0`, so it collapses to the web-only branch,
while the deterministic shuffled void/web control remains marginally better.
This points to a void-source-basis or shared-amplitude-grammar diagnostic, not
to endpoint claim promotion.

The first void-channel inactivity diagnostic is:

```text
data/derived/void_channel_inactivity_diagnostic_v1_summary.csv
data/derived/void_channel_inactivity_diagnostic_v1_profile.csv
docs/void_channel_inactivity_diagnostic_v1.md
scripts/build_void_channel_inactivity_diagnostic_v1.py
scripts/validate_void_channel_inactivity_diagnostic_v1.py
```

It finds that the source-native void basis is active on only
`0.310722100656` of the Pantheon rows, versus `0.972283005106` for the web
basis, and that every non-zero frozen `omega_void` profile worsens relative to
`omega_void=0`. This preserves the next action as a void mapping/source-basis
audit before any endpoint scoring is reopened.

The follow-up void source-basis audit is:

```text
data/derived/void_source_basis_audit_v1_summary.csv
data/derived/void_source_basis_audit_v1_redshift_bins.csv
docs/void_source_basis_audit_v1.md
scripts/build_void_source_basis_audit_v1.py
scripts/validate_void_source_basis_audit_v1.py
```

It identifies the immediate blocker as
`low_z_volume_limited_void_catalog_mapped_to_full_pantheon_distance_block`.
The current void catalogue support is only approximately
`z=0.0103747416544` to `z=0.108950468807`, while the Pantheon distance block
runs to `z=2.26137`; all rows above `z=0.2` have zero void support. Therefore
the combined endpoint should not be reopened until the void mapping is rebuilt
for the declared observable scope or the endpoint scope is explicitly narrowed.

The corresponding void-channel remediation decision gate is:

```text
data/source_manifest/void_channel_remediation_policy_v1.csv
data/derived/void_channel_remediation_gate_v1.csv
docs/void_channel_remediation_gate_v1.md
scripts/build_void_channel_remediation_gate_v1.py
scripts/validate_void_channel_remediation_gate_v1.py
```

It freezes the allowed future routes without running any new endpoint:
predeclare a low-redshift Pantheon scope, rebuild the void source basis for the
full distance scope, or quarantine the void channel from the full-distance
endpoint. The current gate status is `ENDPOINT_REOPEN_BLOCKED`; no route is
selected and `endpoint_scoring_allowed=false`.

The first low-redshift void-scope candidate for the allowed low-z route is:

```text
data/source_manifest/low_z_pantheon_void_scope_candidate_policy_v1.csv
data/derived/low_z_pantheon_void_scope_candidate_v1_row_mask.csv
data/derived/low_z_pantheon_void_scope_candidate_v1_summary.csv
docs/low_z_pantheon_void_scope_candidate_v1.md
scripts/build_low_z_pantheon_void_scope_candidate_v1.py
scripts/validate_low_z_pantheon_void_scope_candidate_v1.py
```

It freezes only an eligible row mask: `424 / 1371` Pantheon rows satisfy the
current low-z void-support rule. It does not authorize or run endpoint scoring;
`candidate_endpoint_run_allowed_now=false` and a separate authorization would
still be required before any replay.

The corresponding low-z replay authorization handoff package is:

```text
REVIEWER_README_LOW_Z_VOID_SCOPE_REPLAY_AUTHORIZATION.md
data/source_manifest/low_z_pantheon_void_scope_replay_authorization_review_policy_v1.csv
data/derived/low_z_pantheon_void_scope_replay_authorization_review_response_template_v1.csv
data/derived/low_z_pantheon_void_scope_replay_authorization_review_template_v1_summary.csv
data/derived/low_z_pantheon_void_scope_replay_authorization_review_package_v1.zip
data/derived/low_z_pantheon_void_scope_replay_authorization_review_package_v1.zip.sha256
data/derived/low_z_pantheon_void_scope_replay_authorization_review_package_v1_manifest.csv
data/derived/low_z_pantheon_void_scope_replay_authorization_review_package_v1_summary.csv
docs/low_z_pantheon_void_scope_replay_authorization_review_v1.md
scripts/build_low_z_pantheon_void_scope_replay_authorization_review_template_v1.py
scripts/validate_low_z_pantheon_void_scope_replay_authorization_review_template_v1.py
scripts/build_low_z_pantheon_void_scope_replay_authorization_review_package_v1.py
scripts/validate_low_z_pantheon_void_scope_replay_authorization_review_package_v1.py
```

This package is a reviewer handoff only. It is not completed, does not authorize
a replay by itself, and records no endpoint residuals, scores, or fit
statistics.

The frozen low-z replay protocol shell is:

```text
data/source_manifest/low_z_pantheon_void_replay_protocol_v1.csv
docs/low_z_pantheon_void_replay_protocol_v1.md
scripts/validate_low_z_pantheon_void_replay_protocol_v1.py
```

It declares only the future replay grammar: the low-z Pantheon distance subset,
the active `W_VOID_MATURITY` channel, disabled web/path/time channels, low-z
AIC shell, wrong/shuffled controls, and forbidden leakage fields. It remains
`LOW_Z_VOID_REPLAY_PROTOCOL_FROZEN_NOT_RUN` with `scoring_allowed=false`.

If a completed independent review grants
`low_z_void_replay_authorized_permission_only_not_validation`, the only
allowed next run is:

```text
data/source_manifest/low_z_pantheon_void_replay_run_v1.csv
scripts/run_low_z_pantheon_void_replay_v1.py
scripts/validate_low_z_pantheon_void_replay_v1.py
```

This run remains a permission-only low-z replay. It does not reopen the
full-Pantheon void endpoint and does not claim physical validation.

The first authorized low-z replay is recorded in:

```text
docs/low_z_pantheon_void_replay_v1.md
data/derived/low_z_pantheon_void_replay_v1_summary.csv
data/derived/low_z_pantheon_void_replay_v1_grid.csv
```

It is a weak/mixed result: `delta_chi2_void_minus_baseline=-0.37847238`, but
`delta_aic_void_minus_baseline=+1.62152762`, and one shuffled control is better
than the candidate. This is retained as a caveated negative/control result, not
as validation.

The follow-up diagnostic is:

```text
docs/low_z_void_replay_diagnostics_v1.md
data/derived/low_z_void_replay_diagnostics_v1_summary.csv
data/derived/low_z_void_replay_diagnostics_v1_branch_summary.csv
```

It records `grid_edge_pressure_and_shuffled_control_beats_candidate`, so the
next void-side step is source-basis refinement rather than post-hoc amplitude or
grid tuning.

The source-side refinement gate is:

```text
docs/void_source_basis_refinement_gate_v1.md
data/source_manifest/void_source_basis_refinement_gate_policy_v1.csv
data/derived/void_source_basis_refinement_gate_v1.csv
```

It freezes the blocker as
`current_W_void_not_endpoint_ready_redshift_degenerate_not_control_unique` and
allows only a future source-side acquisition manifest before any new void replay.

That acquisition manifest is:

```text
docs/void_source_basis_refinement_acquisition_manifest_v1.md
data/source_manifest/void_source_basis_refinement_acquisition_manifest_policy_v1.csv
data/derived/void_source_basis_refinement_acquisition_manifest_v1.csv
```

It freezes six required source-side routes: object-level void catalogue
properties, supernova host-to-void geometry, line-of-sight environment,
redshift-independence preflight, control-resistance preflight, and independent
leakage review. It attaches no sources yet and opens no replay.

The first R1-R3 source attachment layer is:

```text
docs/void_source_basis_refinement_r1_r3_source_attachment_v1.md
data/derived/void_source_basis_refinement_r1_r3_source_attachment_v1.csv
data/derived/void_source_basis_refinement_r1_r3_source_attachment_v1_summary.csv
data/derived/low_z_pantheon_void_geometry_join_v1.csv
data/derived/low_z_pantheon_los_environment_v1.csv
```

It attaches the source-native object-level void catalogue, builds a residual-blind
low-z Pantheon host/SN-to-void geometry join, and builds a fixed-window
line-of-sight environment proxy. The layer remains non-scoring and keeps R4-R6
open: redshift-independence preflight, control-resistance preflight, and
independent leakage review are still required before any new void replay request.

The R4 redshift/source-row independence preflight is:

```text
docs/void_source_basis_refinement_r4_independence_preflight_v1.md
data/derived/void_source_basis_refinement_r4_independence_preflight_v1.csv
data/derived/void_source_basis_refinement_r4_independence_preflight_v1_summary.csv
```

It tests seven R1-R3 source-side features against `zHD` and
`source_row_index`. Five pass the frozen low-correlation threshold, while the
distance-like void-center and wall-distance features remain moderately
redshift-correlated. This is a preflight result only: R5 control-resistance
preflight and R6 independent leakage review remain required before any new void
replay request.

The R5 control-resistance preflight is:

```text
docs/void_source_basis_refinement_r5_control_resistance_preflight_v1.md
data/derived/void_source_basis_refinement_r5_control_resistance_preflight_v1.csv
data/derived/void_source_basis_refinement_r5_control_vectors_v1.csv
data/derived/void_source_basis_refinement_r5_control_resistance_preflight_v1_summary.csv
```

It freezes five source-side control families for the five R4-passing features:
zero, wrong-sign, deterministic row-shuffle, lower-quartile threshold, and
upper-quartile threshold controls. This remains non-scoring and does not reopen
void replay: R6 independent leakage review is still required before any endpoint
request.

The R6 independent leakage-review handoff is:

```text
docs/void_source_basis_refinement_r6_external_reviewer_instructions_v1.md
docs/void_source_basis_refinement_r6_reviewer_template_v1.md
docs/void_source_basis_refinement_r6_reviewer_handoff_package_v1.md
data/derived/void_source_basis_refinement_r6_reviewer_template_v1.csv
data/derived/void_source_basis_refinement_r6_reviewer_handoff_package_v1.zip
data/derived/void_source_basis_refinement_r6_reviewer_handoff_package_v1.zip.sha256
data/derived/void_source_basis_refinement_r6_reviewer_handoff_package_v1_manifest.csv
data/derived/void_source_basis_refinement_r6_reviewer_handoff_package_v1_summary.csv
```

It packages the source-side R1-R5 artifacts for an external reviewer who does
not have repository access. The package is still incomplete until a reviewer
returns a completed response; it does not authorize replay or claim validation.

The completed R6 reviewer response is:

```text
data/derived/void_source_basis_refinement_r6_completed_reviewer_response_v1.csv
data/derived/void_source_basis_refinement_r6_completed_reviewer_response_v1_summary.csv
```

The current response accepts the R6 review as
`ACCEPT_AS_CAVEATED_SOURCE_SIDE_REVIEW`: R6 source-side leakage review is closed
as caveated source-side evidence, while endpoint replay and endpoint validation
remain false and require a separate authorization gate.

The separate refined-void endpoint replay authorization handoff is:

```text
docs/void_source_basis_refinement_endpoint_replay_authorization_review_v1.md
data/source_manifest/void_source_basis_refinement_endpoint_replay_authorization_review_policy_v1.csv
data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_response_template_v1.csv
data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_template_v1_summary.csv
data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_package_v1.zip
data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_package_v1.zip.sha256
data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_package_v1_manifest.csv
data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_package_v1_summary.csv
scripts/validate_void_source_basis_refinement_endpoint_replay_authorization_review_response_v1.py
```

This package is ready but not completed. It asks whether one predeclared refined
low-z void source-basis replay may be authorized as permission-only, without
turning the R6 source-side review into endpoint validation.

A completed reviewer response must be validated with:

```bash
python scripts/validate_void_source_basis_refinement_endpoint_replay_authorization_review_response_v1.py \
  path/to/completed_response.csv
```

The validator accepts only a permission-only decision:
`GO_REFINED_VOID_REPLAY_PERMISSION_ONLY`, with `forbidden_inputs_used=false`,
`endpoint_replay_allowed=true`, and `endpoint_validation_claimed=false`.

The completed authorization response currently validates as permission-only:

```text
data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_response_v1.csv
data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_response_v1_summary.csv
```

This opens only the next predeclared refined-void replay gate. It is not an
endpoint validation result and does not by itself run scoring.

The permission-only refined void replay is recorded in:

```text
data/source_manifest/void_source_basis_refinement_authorized_replay_run_v1.csv
data/derived/void_source_basis_refinement_authorized_replay_v1_grid.csv
data/derived/void_source_basis_refinement_authorized_replay_v1_summary.csv
scripts/run_void_source_basis_refinement_authorized_replay_v1.py
scripts/validate_void_source_basis_refinement_authorized_replay_v1.py
```

Current replay status: the best refined source-basis candidate improves the
low-z baseline chi2 modestly, but not AIC, and several frozen controls still
beat it. This is a permission-only diagnostic replay, not validation.

The targeted control-dominance audit is recorded in:

```text
data/derived/void_source_basis_refinement_control_dominance_audit_v1_branches.csv
data/derived/void_source_basis_refinement_control_dominance_audit_v1_summary.csv
scripts/build_void_source_basis_refinement_control_dominance_audit_v1.py
scripts/validate_void_source_basis_refinement_control_dominance_audit_v1.py
```

Its current verdict is
`candidate_signal_not_source_specific_shuffled_control_dominates_without_redshift_leak`.
In plain terms: the candidate has a weak chi2 signal, but a frozen row-shuffled
control beats it without obvious redshift/row-index leakage, so the current
source-basis refinement is not source-specific enough for a positive endpoint
reading.

The V2 projection/morphology source-basis gate is recorded in:

```text
docs/void_source_basis_refinement_v2_projection_morphology_gate_v1.md
data/source_manifest/void_source_basis_refinement_v2_projection_morphology_policy.csv
data/derived/void_source_basis_refinement_v2_void_morphology_values.csv
data/derived/void_source_basis_refinement_v2_void_morphology_values_summary.csv
data/derived/void_source_basis_refinement_v2_web_morphology_values.csv
data/derived/void_source_basis_refinement_v2_web_morphology_values_summary.csv
data/derived/void_source_basis_refinement_v2_cmb_safety_values.csv
data/derived/void_source_basis_refinement_v2_cmb_safety_values_summary.csv
data/derived/void_source_basis_refinement_v2_path_projection_crossmap_audit.csv
data/derived/void_source_basis_refinement_v2_path_projection_crossmap_audit_summary.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_policy.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_policy_summary.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_values.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_values_summary.csv
docs/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.md
data/source_manifest/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_policy_v1.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_response_template_v1.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.zip
data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.zip.sha256
data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1_manifest.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1_summary.csv
docs/void_source_basis_refinement_v2_path_partial_scope_completed_review_notes_v1.md
data/derived/void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1_summary.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_completed_review_summary_v1.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_completed_review_validation_log_v1.txt
docs/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_v1.md
data/source_manifest/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_policy_v1.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_template_v1.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_template_v1_summary.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.zip
data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.zip.sha256
data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1_manifest.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1_summary.csv
docs/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1.md
data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1_summary.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1_validation_log.txt
docs/void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1.md
data/source_manifest/void_source_basis_refinement_v2_path_partial_scope_authorized_replay_run_v1.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1_grid.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1_summary.csv
data/derived/void_source_basis_refinement_v2_path_projection_route_ledger.csv
data/derived/void_source_basis_refinement_v2_path_projection_route_ledger_summary.csv
data/derived/void_source_basis_refinement_v2_time_readout_route_ledger.csv
data/derived/void_source_basis_refinement_v2_time_readout_route_ledger_summary.csv
data/derived/void_source_basis_refinement_v2_multichannel_coupling_ledger.csv
data/derived/void_source_basis_refinement_v2_multichannel_coupling_ledger_summary.csv
data/derived/void_source_basis_refinement_v2_projection_morphology_gate_v1.csv
data/derived/void_source_basis_refinement_v2_projection_morphology_gate_v1_summary.csv
scripts/build_void_source_basis_refinement_v2_web_morphology_values_v1.py
scripts/validate_void_source_basis_refinement_v2_web_morphology_values_v1.py
scripts/build_void_source_basis_refinement_v2_void_morphology_values_v1.py
scripts/validate_void_source_basis_refinement_v2_void_morphology_values_v1.py
scripts/build_void_source_basis_refinement_v2_cmb_safety_values_v1.py
scripts/validate_void_source_basis_refinement_v2_cmb_safety_values_v1.py
scripts/build_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py
scripts/validate_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py
scripts/build_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py
scripts/validate_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py
scripts/build_void_source_basis_refinement_v2_path_partial_scope_values_v1.py
scripts/validate_void_source_basis_refinement_v2_path_partial_scope_values_v1.py
scripts/build_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.py
scripts/validate_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.py
scripts/validate_void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1.py
scripts/build_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_template_v1.py
scripts/validate_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_template_v1.py
scripts/build_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.py
scripts/validate_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.py
scripts/validate_void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1.py
scripts/run_void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1.py
scripts/validate_void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1.py
docs/void_source_basis_refinement_v2_path_coupled_projection_screen_v1.md
data/source_manifest/void_source_basis_refinement_v2_path_coupled_projection_screen_v1.csv
data/derived/void_source_basis_refinement_v2_path_coupled_projection_screen_v1_grid.csv
data/derived/void_source_basis_refinement_v2_path_coupled_projection_screen_v1_summary.csv
scripts/run_void_source_basis_refinement_v2_path_coupled_projection_screen_v1.py
scripts/validate_void_source_basis_refinement_v2_path_coupled_projection_screen_v1.py
docs/void_source_basis_refinement_v2_path_transform_bank_screen_v1.md
data/source_manifest/void_source_basis_refinement_v2_path_transform_bank_screen_v1.csv
data/derived/void_source_basis_refinement_v2_path_transform_bank_screen_v1_grid.csv
data/derived/void_source_basis_refinement_v2_path_transform_bank_screen_v1_family_summary.csv
data/derived/void_source_basis_refinement_v2_path_transform_bank_screen_v1_summary.csv
scripts/run_void_source_basis_refinement_v2_path_transform_bank_screen_v1.py
scripts/validate_void_source_basis_refinement_v2_path_transform_bank_screen_v1.py
docs/void_source_basis_refinement_v2_path_sky_environment_screen_v1.md
data/source_manifest/void_source_basis_refinement_v2_path_sky_environment_screen_v1.csv
data/derived/void_source_basis_refinement_v2_path_sky_environment_screen_v1_grid.csv
data/derived/void_source_basis_refinement_v2_path_sky_environment_screen_v1_family_summary.csv
data/derived/void_source_basis_refinement_v2_path_sky_environment_screen_v1_summary.csv
scripts/run_void_source_basis_refinement_v2_path_sky_environment_screen_v1.py
scripts/validate_void_source_basis_refinement_v2_path_sky_environment_screen_v1.py
docs/void_source_basis_refinement_v2_observer_dependence_followup_v1.md
data/source_manifest/void_source_basis_refinement_v2_observer_dependence_followup_policy_v1.csv
data/derived/void_source_basis_refinement_v2_observer_dependence_followup_response_template_v1.csv
data/derived/void_source_basis_refinement_v2_observer_dependence_followup_template_v1_summary.csv
data/derived/void_source_basis_refinement_v2_observer_dependence_followup_package_v1.zip
data/derived/void_source_basis_refinement_v2_observer_dependence_followup_package_v1.zip.sha256
data/derived/void_source_basis_refinement_v2_observer_dependence_followup_package_v1_manifest.csv
data/derived/void_source_basis_refinement_v2_observer_dependence_followup_package_v1_summary.csv
scripts/build_void_source_basis_refinement_v2_observer_dependence_followup_template_v1.py
scripts/validate_void_source_basis_refinement_v2_observer_dependence_followup_template_v1.py
scripts/build_void_source_basis_refinement_v2_observer_dependence_followup_package_v1.py
scripts/validate_void_source_basis_refinement_v2_observer_dependence_followup_package_v1.py
docs/void_source_basis_refinement_v2_sky_z_replay_authorization_review_v1.md
data/source_manifest/void_source_basis_refinement_v2_sky_z_replay_authorization_review_policy_v1.csv
data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_template_v1.csv
data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_template_v1_summary.csv
data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1.zip
data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1.zip.sha256
data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1_manifest.csv
data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1_summary.csv
scripts/build_void_source_basis_refinement_v2_sky_z_replay_authorization_review_template_v1.py
scripts/validate_void_source_basis_refinement_v2_sky_z_replay_authorization_review_template_v1.py
scripts/build_void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1.py
scripts/validate_void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1.py
scripts/validate_void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1.py
docs/void_source_basis_refinement_v2_sky_z_authorized_replay_v1.md
data/source_manifest/void_source_basis_refinement_v2_sky_z_authorized_replay_run_v1.csv
data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1.csv
data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1_summary.csv
data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_completed_summary_v1.csv
data/derived/void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1_validation_log.txt
docs/void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1.md
data/derived/void_source_basis_refinement_v2_sky_z_authorized_replay_v1_grid.csv
data/derived/void_source_basis_refinement_v2_sky_z_authorized_replay_v1_summary.csv
scripts/run_void_source_basis_refinement_v2_sky_z_authorized_replay_v1.py
scripts/validate_void_source_basis_refinement_v2_sky_z_authorized_replay_v1.py
docs/void_source_basis_refinement_v2_sky_z_source_audit_v1.md
data/derived/void_source_basis_refinement_v2_sky_z_source_audit_v1.csv
data/derived/void_source_basis_refinement_v2_sky_z_source_audit_v1_summary.csv
scripts/build_void_source_basis_refinement_v2_sky_z_source_audit_v1.py
scripts/validate_void_source_basis_refinement_v2_sky_z_source_audit_v1.py
docs/void_source_basis_refinement_v2_observer_orientation_kernel_v2.md
data/source_manifest/void_source_basis_refinement_v2_observer_orientation_kernel_v2_manifest.csv
data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2.csv
data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_summary.csv
scripts/build_void_source_basis_refinement_v2_observer_orientation_kernel_v2.py
scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2.py
docs/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization.md
data/source_manifest/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_policy.csv
data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_template.csv
data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template_summary.csv
data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package.zip
data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package.zip.sha256
data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package_manifest.csv
data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package_summary.csv
scripts/build_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template.py
scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template.py
scripts/build_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package.py
scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package.py
docs/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_review_notes_v1.md
data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_v1.csv
data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_v1_summary.csv
data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_review_completed_summary_v1.csv
data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_v1_validation_log.txt
scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response.py
docs/void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay.md
data/source_manifest/void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_run.csv
data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_grid.csv
data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_summary.csv
scripts/run_void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay.py
scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay.py
docs/void_source_basis_refinement_v2_observer_basis_fast_screen_v1.md
data/source_manifest/void_source_basis_refinement_v2_observer_basis_fast_screen_v1.csv
data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_grid.csv
data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_family_summary.csv
data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_summary.csv
scripts/run_void_source_basis_refinement_v2_observer_basis_fast_screen_v1.py
scripts/validate_void_source_basis_refinement_v2_observer_basis_fast_screen_v1.py
docs/void_source_basis_refinement_v2_observer_basis_candidate_review_v1.md
data/source_manifest/void_source_basis_refinement_v2_observer_basis_candidate_review_policy_v1.csv
data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_response_template_v1.csv
data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1.zip
data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1.zip.sha256
data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1_manifest.csv
data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1_summary.csv
scripts/build_void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1.py
scripts/validate_void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1.py
docs/void_source_basis_refinement_v2_observer_basis_candidate_review_notes_v1.md
data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_response_v1.csv
data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_response_v1_summary.csv
data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_completed_summary_v1.csv
data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_response_v1_validation_log.txt
scripts/validate_void_source_basis_refinement_v2_observer_basis_candidate_review_response_v1.py
docs/void_source_basis_refinement_v2_observer_basis_replay_authorization_v1.md
data/source_manifest/void_source_basis_refinement_v2_observer_basis_replay_authorization_policy_v1.csv
data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_response_template_v1.csv
data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1.zip
data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1.zip.sha256
data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1_manifest.csv
data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1_summary.csv
scripts/build_void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1.py
scripts/validate_void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1.py
docs/void_source_basis_refinement_v2_observer_basis_replay_authorization_review_notes_v1.md
data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_response_v1.csv
data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_response_v1_summary.csv
data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_review_completed_summary_v1.csv
data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_response_v1_validation_log.txt
scripts/validate_void_source_basis_refinement_v2_observer_basis_replay_authorization_response_v1.py
docs/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1.md
data/source_manifest/void_source_basis_refinement_v2_observer_basis_authorized_replay_run_v1.csv
data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_grid.csv
data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv
scripts/run_void_source_basis_refinement_v2_observer_basis_authorized_replay_v1.py
scripts/validate_void_source_basis_refinement_v2_observer_basis_authorized_replay_v1.py
scripts/build_void_source_basis_refinement_v2_path_projection_route_ledger_v1.py
scripts/validate_void_source_basis_refinement_v2_path_projection_route_ledger_v1.py
scripts/build_void_source_basis_refinement_v2_time_readout_route_ledger_v1.py
scripts/validate_void_source_basis_refinement_v2_time_readout_route_ledger_v1.py
scripts/build_void_source_basis_refinement_v2_multichannel_coupling_ledger_v1.py
scripts/validate_void_source_basis_refinement_v2_multichannel_coupling_ledger_v1.py
scripts/build_void_source_basis_refinement_v2_projection_morphology_gate_v1.py
scripts/validate_void_source_basis_refinement_v2_projection_morphology_gate_v1.py
```

This is the first source-side accounting layer that includes the missing Tau
Core projection/morphology channels: void morphology, web morphology,
observer/path projection, time/readout projection, CMB safety, and multi-channel
coupling. It currently tracks all six components but keeps endpoint replay
blocked until the missing V2 source values are frozen. The void-morphology
component is source-frozen for the low-z scope, but its weak-negative
control-dominance status is explicitly preserved. The web-morphology
component is now source-frozen for the low-z Pantheon scope from the existing
source-native W_web design matrix, with deterministic null controls and all
endpoint/leakage flags set to false. This is not a replay authorization and
does not score the endpoint. The CMB-safety component is also frozen as a
low-z support/safety ledger; it uses no CMB map data, no CMB likelihood, and no
endpoint residuals. The observer/path component now has a route ledger: KiDS
path products are source-supported. A crossmap audit now confirms that low-z
Pantheon RA/DEC are available and that a small number of rows have nearby KiDS
tile candidates, but the crossmap is not complete for the low-z scope and no
Pantheon-row path-weight rule is frozen. Therefore no `W_path` values are
computed. The partial-scope policy freezes the consequence: `W_path` is at most
a 12-row source-side candidate subset in this low-z replay scope, with 5 strict
and 7 caveated candidates, not a full low-z channel. A source-only
tile-proximity control value is now frozen for those 12 rows, using only the
nearest KiDS tile separation. This is explicitly not promoted as a physical
lensing-path weight and does not authorize a partial-scope replay. The
corresponding reviewer package is now built for a repository-independent
source-side audit of this 12-row control. It asks only whether the partial
control may be retained as caveated source-side material for a future separate
authorization package; it does not authorize endpoint scoring and contains no
endpoint residuals, fit statistics, posterior chains, or KiDS data-vector
values. The completed reviewer response accepts this as
`ACCEPT_PARTIAL_PATH_CONTROL_AS_CAVEATED_SOURCE_SIDE`: the 12-row control can be
kept only as caveated source-side material for a later, separate partial-scope
authorization package. Endpoint replay, endpoint validation, a full low-z
`W_path` channel, and physical lensing-path weight claims remain false. That
separate partial-scope replay authorization package is now built but not
completed. It asks whether one permission-only replay may be run on the 12
predeclared rows; it still contains no endpoint residuals, scores, fit
statistics, KiDS data-vector values, or posterior chains. The
completed authorization response grants
`GO_PARTIAL_PATH_REPLAY_PERMISSION_ONLY`: exactly one separate, explicitly
predeclared 12-row partial `W_path` replay is permitted. This permission still
does not claim endpoint validation, does not enable a full low-z `W_path`
channel, and does not promote the tile-proximity control to a calibrated
physical lensing-path weight. The permission-only replay has now been run on
the 12-row subset. It gives a small chi2 improvement over the baseline
(`delta_chi2_candidate_minus_baseline=-0.20237914656`) but worsens AIC and
ranks third among the candidate/control set because two frozen controls beat
the candidate. This is therefore a weak caveated diagnostic replay, not a
positive endpoint validation. A faster path-coupled projection screen has also
been run on the same 12 predeclared rows, combining already frozen source-side
`W_path`, `W_void_centered`, and `W_web_centered` values into bounded candidate
families (`W_path`, `W_path x W_void`, `W_path x W_web`, and
`W_path x W_void x W_web`). This screen is explicitly preauthorization-only:
it is not an endpoint replay, does not claim validation, and does not promote a
physical lensing-path weight. Its best candidate is the simple normalized
`W_path` family, with `delta_chi2_candidate_minus_baseline=-0.29032427181`,
but the candidate ranks eighth among candidate/control branches and seven
controls beat it. The verdict is therefore
`coupled_candidate_not_control_resistant_in_fast_screen`. In practical terms,
the current simple path-coupled products do not justify a new authorization
package without a stronger source-side projection basis. A second fast
transform-bank screen searched simple source-side transforms of the same
12-row nearest-tile path control (`existing_W_path`, raw proximity, margin,
inverse distance, Gaussian kernels, binary near/core cuts, and rank quantile),
with optional void/web couplings. Its best candidate is
`tile_gaussian_sigma_2p0__web`, with
`delta_chi2_candidate_minus_baseline=-0.33433018032`, but it is still not
control resistant: the candidate ranks 53rd among candidate/control branches
and 52 controls beat it. The verdict is
`path_transform_candidate_not_control_resistant_in_fast_screen`. This is a
useful negative search result: the bottleneck is unlikely to be fixed by a
simple monotone transform of the 12-row tile-separation proxy. A stronger
source-side path/projection basis is required before a new authorization
package is scientifically justified. A third fast screen now tests the more
Tau-Core-relevant observer/path idea that measurement readouts are
observer-dependent: it combines the 12-row path control with frozen RA/DEC,
sky-vector, tile-offset, line-of-sight environment, and void-geometry source
fields. The global best candidate is `W_path_x_los_density_excess`, with
`delta_chi2_candidate_minus_baseline=-0.51673114829`, but it still fails global
control resistance: the candidate ranks seventh and six controls beat it. A
narrower follow-up signal appears for `W_path_x_sky_z`, which survives its own
family controls in the same 12-row screen. This is not endpoint validation, but
it is the first screen-level hint that observer/sky-orientation terms may be a
better source-side path basis than tile proximity alone. A dedicated
observer-dependence follow-up package is now built for `W_path_x_sky_z`. The
package asks only whether this can be retained as a source-side
observer-dependence follow-up candidate and whether the next action may be
limited to a separate replay authorization package. It does not authorize
replay, does not claim endpoint validation, and contains no endpoint residuals,
endpoint scores, or fit statistics. The completed external review authorizes
exactly one permission-only replay of the centered observer-orientation kernel
`K_v2 = W_path * (sky_z - mean_sky_z_scope)`. That replay improves the baseline
chi2 (`delta_chi2_candidate_minus_baseline=-0.47326976306`), but it is not
control-resistant: one deterministic-shuffle control is slightly better
(`delta_chi2_candidate_minus_best_control=0.01875086453`). The verdict is
`observer_orientation_v2_permission_replay_not_control_resistant_not_validation`.
This is a useful diagnostic negative: centering the sky-orientation coordinate
does not by itself preserve the raw `W_path_x_sky_z` control-surviving signal.
An accelerated preauthorization observer-basis bank was therefore run without
reviewer-gated endpoint promotion. It tests only predeclared source-side
sky-vector and redshift-modulated observer-basis functions on the same 12-row
scope. The best candidate is
`W_path_x_sky_x_x_zcenter`, with
`delta_chi2_candidate_minus_baseline=-0.58072431813`; it survives its local
controls with `delta_chi2_candidate_minus_best_control=-0.08783266799` and is
slightly better than the best global control in the bank
(`best_candidate_delta_chi2_minus_best_global_control=-0.02302956281`). This is
still a preauthorization diagnostic, not validation. Because it improves on the
previous raw `W_path_x_sky_z` candidate, it is the next family that should go to
external reviewer authorization before any replay claim. The subsequent
permission-only replay authorization review accepted exactly one frozen 12-row
replay for `W_path_x_sky_x_x_zcenter`. The replay preserves the signal:
`delta_chi2_candidate_minus_baseline=-0.58072431813`,
`delta_chi2_candidate_minus_best_control=-0.08783266799`, rank 1 among the
candidate and frozen controls, with zero controls better than the candidate.
This is the strongest current narrow observer/projection replay, but still not
population validation or a physical path-weight derivation. It is also still a
simplified observer/path proxy: `W_path_x_sky_x_x_zcenter` keeps only a
source-side path proxy, one sky-vector component, and a centered redshift
coordinate. A future full Tau Core observer/path kernel would need to include
the full sky direction, redshift, line-of-sight environment, void/web geometry,
observer/survey-frame orientation, metric or lensing-path information, and any
independently source-grounded time/readout phase. The current result motivates
that full-kernel construction; it does not provide or validate it.
A first preauthorization full-kernel-proxy fast screen has now been run on the
same 12-row scope. It multiplies the observer-basis carrier by frozen source-side
void, web, line-of-sight environment, and void-geometry proxies. The best family
is still the simpler `W_path_x_sky_x_x_zcenter`
(`delta_chi2_candidate_minus_baseline=-0.58072431813`). The only enriched family
that survives its local controls is
`W_path_x_sky_x_x_zcenter_x_web_centered_x_los_density_mean`, and it is weaker
(`delta_chi2_candidate_minus_baseline=-0.451413`,
`delta_chi2_candidate_minus_best_control=-0.048323`). The best global control in
the enlarged bank is slightly better than the best candidate
(`best_candidate_delta_chi2_minus_best_global_control=0.115454`). This is a
useful diagnostic constraint, not a failure of the observer/path idea: simply
stacking available source-side proxies is not enough. A genuine full kernel
needs better source-native path/environment/readout observables.
A component audit makes this sharper: zero enriched families are stronger than
the base observer-basis carrier. The mixed void-web proxy is close but fails
controls; the mixed web-LOS-density proxy survives local controls but remains
weaker than the base. This keeps the interpretation narrow and useful: the
current evidence points to an observer-basis channel, not to arbitrary
environment-proxy accumulation.
The next gate is therefore a source-requirements gate, not another score search:
the full observer/path kernel needs a full observer-frame basis, radial
line-of-sight environment integral, path-aware void geometry, directional web
anisotropy, independent metric/lensing-path information, and independent
time/readout phase evidence before replay or validation language is allowed.
The first concrete R2 upgrade is now present: a source-side LOS radial profile
with five frozen redshift shells inside the same 2 degree cone. It is available
for 424 low-z rows, with 153 complete five-shell profiles; on the 12-row partial
path scope, 7 rows have complete profiles and 10 have at least one non-empty
shell. This is a better source observable than the earlier scalar count/density
proxy, but it is still not a full metric/lensing-weighted path integral.
A first R3 upgrade is also present: a path-aware void-geometry observable that
uses the observer-to-source segment instead of only the nearest void to the
source position. It finds 180 effective-void path crossings among 424 low-z
rows, and 10 crossings in the 12-row partial path scope. This is a better void
geometry source observable, but still a low-z Euclidean proxy rather than a
metric/lensing-weighted null-geodesic bundle term.
A first R4 upgrade is now present as well: a source-side directional web
anisotropy observable computed from the same SDSS DR17 MCPM catalogue. It uses
a fixed 2 degree cone and a frozen redshift window around each low-z Pantheon+
source, then records tangent-plane density-weighted dipole and quadrupole
moments. It is quadrupole-ready for 238 of 424 low-z rows and for 9 of the 12
partial path-scope rows. This improves the earlier scalar web proxy, but it is
still not a full cosmic-web tensor contracted with a metric/lensing-weighted
observer-source path.
The R5 metric/lensing-path route audit is also now explicit. Public KiDS and
CMB lensing routes are cached, and the low-z Pantheon+ rows are cross-checked
against the KiDS DR4.1 tile-coordinate inventory. Only 5 of 424 low-z rows are
within 1 degree of a KiDS tile proxy, and no source-aligned kappa, shear,
mass-map integral, or metric/lensing path weight is computed. This narrows the
blocker: R5 is route-grounded but not yet observable-grounded.
The first CMB-lensing source-product acquisition route is now frozen for ACT
DR6 through the public NASA LAMBDA release. The manifest records the LAMBDA
info/download pages, provider download script, expected byte count, local byte
count, checksum when complete, and the explicit endpoint-disabled claim
boundary. This is still source-side acquisition only: it does not yet synthesize
a physical metric/lensing path weight and does not authorize endpoint replay.
The route therefore strengthens R5 data availability without authorizing
observer/path endpoint replay.
The source inventory contains 13 ACT DR6 lensing variants with kappa alm,
HEALPix mask, filter, and noise products for each variant. The baseline variant
is available as the recommended science route, and `diff_f150_f090`,
`diff_f150_f090_tonly`, and `curl` are available as null-control variants.
A first low-resolution source-side sampling pilot now synthesizes ACT DR6
kappa maps from the baseline, curl, and `diff_f150_f090` alm products at
`nside=512`, `lmax=1024`, samples them at the 424 low-z Pantheon+ sky
positions, and samples the baseline `nside=4096` ACT mask. The pilot finds 168
mask-positive rows and records all sampled values with `endpoint_replay_allowed
= false`, `contains_distance_residuals = false`, and `contains_fit_statistics
= false`. This is an observer/path lensing input artifact, not a physical
metric-path kernel and not a validation result.
A follow-up candidate freezes a unitless ACT lensing path-weight shape by
normalizing the baseline kappa samples over mask-positive rows with a
source-side median/MAD rule and assigning zero weight outside the ACT mask. The
curl and `diff_f150_f090` channels are frozen with the same rule as null
controls. The active-row baseline/control correlations are
`corr(baseline,curl)=-0.0415435390521` and
`corr(baseline,diff_f150_f090)=-0.230185832443`, so the candidate is
nondegenerate enough for external review. It remains not endpoint replay, not
validation, and not a physical path-weight claim.
After the guarded replay and control-dominance diagnostic, the Paper11-style
control-veto gate records:

```text
data/derived/act_dr6_lensing_path_weight_paper11_control_veto_gate_v1_summary.csv
```

The gate maps the ACT result into the Paper11 decision language:
`M0_no_dark_tau_readout`, `M1_tau_base_substrate`, and
`M2_standard_dark_sector`. Because four controls beat the present candidate and
the best control is `curl_null`, the current ACT path-weight source basis is
not family-verdict eligible. This blocks an M0/M1 source-structure claim for
this ACT basis, but it also explicitly blocks any inference that the result
favors a standard dark-sector benchmark. The required next gate is therefore
`source_basis_freeze_or_demote_act_path_weight`, not combination search.
That gate is now materialized as:

```text
data/derived/act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1_summary.csv
data/derived/act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1_checklist.csv
```

It demotes the current unitless ACT path-weight basis to a preserved
negative/control-dominated candidate. Reopening remains allowed only through a
new source-side basis freeze that supplies the source object, E-mode route,
curl-null policy, mask/coverage policy, units/normalization, channel handoff,
and predeclared control suite before any replay.
The first item in that reopen checklist is now defined source-side:

```text
data/source_manifest/act_dr6_lensing_observer_path_source_object_v1.csv
data/derived/act_dr6_lensing_observer_path_source_object_v1_summary.csv
```

The source object is the ACT DR6 observer/path lensing-environment bundle:
baseline convergence reconstruction samples, curl and frequency-difference
null-control samples, and ACT mask coverage sampled at predeclared low-z
Pantheon sky positions. It is explicitly not a metric/lensing path integral,
not a physical `K_path` kernel, not an endpoint score, and not a dark-sector
decision object. Therefore `ACT_REOPEN_01_SOURCE_OBJECT` is now
`DEFINED_SOURCE_SIDE`, while replay remains disabled by the remaining reopen
requirements.
The second item is also defined only at source-route level:

```text
data/source_manifest/act_dr6_lensing_e_mode_route_v1.csv
data/derived/act_dr6_lensing_e_mode_route_v1_summary.csv
```

This freezes why the baseline channel is the candidate route: the ACT inventory
labels `baseline` as the recommended science variant and provides baseline
kappa alm modes plus mask support. This is not yet a physical E/B theorem,
gauge-descent proof, metric/lensing path integral, or replay authorization.
Thus `ACT_REOPEN_02_E_MODE_ROUTE` is `DEFINED_SOURCE_SIDE`, while
`ACT_REOPEN_03_CURL_NULL_POLICY`, normalization, channel handoff, and controls
remain active blockers.
The curl-null policy is now frozen as a protocol veto:

```text
data/source_manifest/act_dr6_lensing_curl_null_policy_v1.csv
data/derived/act_dr6_lensing_curl_null_policy_v1_summary.csv
```

The policy treats `curl` as a source-native null/control branch for the ACT
path-weight candidate, not as a positive Tau path channel in this paper. Since
the guarded replay already found `curl_null` as the best control, the current
branch is explicitly vetoed: the ACT basis remains control-dominated and cannot
support a family verdict. This freezes `ACT_REOPEN_03_CURL_NULL_POLICY` as
`FROZEN_SOURCE_SIDE_VETO_ACTIVE`; it does not prove operator-level curl quotient
triviality or physical E/B gauge descent.
The mask and coverage policy is now frozen source-side:

```text
data/source_manifest/act_dr6_lensing_mask_coverage_policy_v1.csv
data/derived/act_dr6_lensing_mask_coverage_policy_v1_summary.csv
```

It records the predeclared low-z Pantheon scope of 424 rows, 168 ACT
mask-positive rows, and 256 outside-mask rows. Mask-positive rows are used only
for source-side center/scale normalization; outside-mask rows are assigned zero
weight but kept in the scope. The policy explicitly forbids endpoint-driven row
dropping or post-hoc selection. Thus `ACT_REOPEN_04_MASK_AND_COVERAGE_POLICY`
is now `FROZEN_SOURCE_SIDE`.
The units/normalization policy is now frozen only as a proxy-level diagnostic:

```text
data/source_manifest/act_dr6_lensing_units_normalization_policy_v1.csv
data/derived/act_dr6_lensing_units_normalization_policy_v1_summary.csv
```

It records the current mask-positive median/MAD rule as a deterministic
source-side, dimensionless proxy normalization. This does not define physical
path-weight units, response amplitude, or endpoint amplitude tuning. A physical
ACT path-weight reopen would still require source-native convergence-to-path
response units, or a theorem-bounded mapping from ACT kappa samples to
`K_path` amplitude. Thus `ACT_REOPEN_05_UNITS_AND_NORMALIZATION` is now
`PROXY_FROZEN_PHYSICAL_BLOCKER_OPEN`, while channel handoff and the full
control suite remain open.
The channel handoff is now frozen as a source-diagnostic demotion:

```text
data/source_manifest/act_dr6_lensing_channel_handoff_policy_v1.csv
data/derived/act_dr6_lensing_channel_handoff_policy_v1_summary.csv
```

The baseline ACT kappa route remains a `K_path` observer/path candidate, but
only as `K_path_candidate_source_diagnostic_only`. Positive `K_path` promotion
is blocked because physical units are still missing and the Paper11-style veto
found `curl_null` as the best control. No `K_closure` handoff is allowed because
no closure equation or theorem-bounded mapping is frozen. The curl branch is
retained as `K_null` control. Thus `ACT_REOPEN_06_CHANNEL_HANDOFF` is now
`SOURCE_DIAGNOSTIC_ONLY_NOT_PHYSICAL_K_PATH`, while the full control suite
remains open.
The current ACT control suite is now frozen:

```text
data/source_manifest/act_dr6_lensing_control_suite_policy_v1.csv
data/derived/act_dr6_lensing_control_suite_policy_v1_summary.csv
```

It records seven scored controls from the guarded replay: `off`,
`baseline_only`, `curl_null`, `diff_f150_f090_null`, `wrong_sign`,
`deterministic_shuffle`, and `rank_reverse`. It also records
`source_basis_recenter_stress` as a future reopen stress, not as a scored
current-branch rescue. All controls are bound as `K_null`. Because `curl_null`
is already the best control, the suite freezes the veto rather than reopening
the branch. Thus `ACT_REOPEN_07_CONTROL_SUITE` is
`FROZEN_CURRENT_BRANCH_REPLAY_STILL_DISABLED`.
The resulting ACT reopen closure ledger is:

```text
data/derived/act_dr6_lensing_reopen_closure_ledger_v1.csv
data/derived/act_dr6_lensing_reopen_closure_ledger_v1_summary.csv
```

It records that all seven ACT reopen gates are now accounted for and closed or
frozen for the current branch. This is not replay authorization. It is a
quarantine result: the current ACT branch is preserved as a
control-dominated diagnostic, and any future ACT path-weight attempt must start
from a new source-side basis design without reusing endpoint scores.
The corresponding next-basis design scaffold is now frozen at:

```text
data/source_manifest/act_dr6_lensing_next_source_basis_design_scaffold_v1.csv
data/derived/act_dr6_lensing_next_source_basis_design_scaffold_v1_summary.csv
```

It predeclares seven requirements for any future ACT attempt: a physical
`K_path` mapping, operator/quotient descent, mask and coverage policy,
source-only recenter stress, a complete control suite, channel-handoff decision,
and a forbidden-endpoint-field ledger. This artifact is not replay
authorization and does not improve the current ACT score. Its role is to make
the next ACT source-basis route auditable before any future endpoint scoring.
The first caveated source-design instance for that route is:

```text
data/source_manifest/act_dr6_lensing_caveated_kpath_source_design_v1.csv
data/derived/act_dr6_lensing_caveated_kpath_source_design_v1_summary.csv
data/derived/act_dr6_lensing_caveated_kpath_source_design_review_package_v1.zip
```

This design carries ACT baseline kappa only as a dimensionless
`K_path`-shape proxy, keeps curl and frequency-difference products as
`K_null` controls, preserves the partial ACT mask coverage, and requires
external review before any future permission-only replay. It does not reopen
the quarantined ACT endpoint branch and does not claim a physical path-weight
amplitude.
The completed external source-design response is now imported and validated:

```text
data/derived/act_dr6_lensing_caveated_kpath_source_design_review_response_v1.csv
data/derived/act_dr6_lensing_caveated_kpath_source_design_review_completed_summary_v1.csv
```

The decision is `ACCEPT_CAVEATED_KPATH_SOURCE_DESIGN_FOR_REVIEW_ONLY`.
This permits preparation of a later permission-only replay-review package, but
it still sets `current_replay_authorized_by_this_review=false`,
`endpoint_replay_allowed=false`, `endpoint_validation_claimed=false`, and
`physical_lensing_path_weight_claimed=false`.
That next replay-authorization review package is now prepared at:

```text
data/derived/act_dr6_lensing_caveated_kpath_replay_authorization_review_package_v1.zip
data/derived/act_dr6_lensing_caveated_kpath_replay_authorization_review_package_v1_summary.csv
```

It is still pending reviewer completion. The package asks only whether a
separate permission-only guarded replay package may be prepared from the
accepted caveated source design. It does not itself authorize replay,
validation, physical `K_path` promotion, or a dark-sector/family verdict.
When a completed response is returned, it is imported and checked with:

```text
scripts/import_act_dr6_lensing_caveated_kpath_replay_authorization_review_response_v1.py
scripts/validate_act_dr6_lensing_caveated_kpath_replay_authorization_review_response_v1.py
```

The validator can only permit preparation of a later guarded replay package.
It keeps `endpoint_replay_allowed_by_this_review=false`; scoring remains a
separate downstream gate.
The completed response now authorizes that preparation step only:

```text
data/derived/act_dr6_lensing_caveated_kpath_replay_authorization_review_response_v1_summary.csv
data/derived/act_dr6_lensing_caveated_kpath_guarded_replay_package_v1.zip
data/derived/act_dr6_lensing_caveated_kpath_guarded_replay_package_v1_summary.csv
```

The guarded replay package is ready but not executed. It keeps
`endpoint_replay_executed=false`, `endpoint_validation_claimed=false`, and
`physical_lensing_path_weight_claimed=false`. The next step, if chosen, is a
separate guarded replay execution with all mandatory controls retained.
That guarded replay has now been executed as a permission-only diagnostic:

```text
data/derived/act_dr6_lensing_caveated_kpath_guarded_replay_v1_grid.csv
data/derived/act_dr6_lensing_caveated_kpath_guarded_replay_v1_summary.csv
```

The result remains control-dominated. The candidate improves over the baseline
(`Delta chi2 candidate - baseline = -1.218200515`), but the best control is
still `curl_null`, with
`Delta chi2 candidate - best control = 1.241099132`, and four controls beat
the candidate. The verdict is
`ACT_CAVEATED_KPATH_GUARDED_REPLAY_CONTROL_DOMINATED_PERMISSION_ONLY_NOT_VALIDATION`.
This preserves ACT as a negative/control-dominated branch under the current
caveated source basis.
The time/readout component now has a sharper R6 source audit. The cosmic
chronometer `H(z)` table is fetched and frozen, the SDSS DR16 multi-tracer
BAO/RSD products are fetched and frozen, and the Planck/LAMBDA CMB route page
is cached. The 424 low-z Pantheon+ rows all have a nearby CC `H(z)` redshift
support point under the current source-side coverage rule. However, no
`Delta_clock`, `Delta_clock_star`, redshift-bin phase rule, or numeric `W_time`
activation has been derived or frozen. R6 is therefore route-grounded but still
activation-blocked.
The next R6 subgate freezes only a source-side normalization candidate:
`Delta_clock_star_candidate = median(errHz/Hz) = 0.16581626506` from the
fetched/frozen cosmic-chronometer table. This removes one normalization
ambiguity, but it still does not compute `Delta_clock` or activate `W_time`.
The following R6 subgate freezes a source-side redshift-bin policy candidate:
low-z Pantheon+ rows are assigned to source-native cosmic-chronometer support
cells, with SDSS BAO/RSD nodes recorded only as route markers. This fixes the
domain on which a later clock/readout observable could be evaluated, but it
still does not compute `Delta_clock`, does not smooth `H(z)`, and does not
activate `W_time`.
The next R6 subgate freezes a narrow uncertainty-channel `Delta_clock`
candidate:
`Delta_clock_uncertainty_candidate = log((errHz/Hz)_assigned_CC_bin /
median(errHz/Hz)_CC)`. This is a residual-blind CC measurement-uncertainty
contrast, not a physical clock-drift measurement and not a `W_time` activation.
The resulting low-z candidate has range `[0.0476000829881, 0.834341816646]`
under the current CC-support assignment.
The next source-only transform freezes a `W_time` basis candidate by centering
and scaling that `Delta_clock` candidate over the source rows:
`W_time_uncertainty_basis = (Delta_clock_uncertainty_candidate - source_mean) /
source_std`. The resulting basis has range `[-4.23048519997, 2.81443932804]`
and zero source mean, but it remains a candidate basis only: it does not
authorize replay, does not claim validation, and must pass a separate control
or replay-authorization gate before scoring.
A replay-authorization review package for this basis is now prepared and
validated at
`data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1.zip`
with checksum
`2067b221b0309bb8fcc3a294fcebf5c8fddd6123d7d7d7a151615c992a2fd69f`.
The package is intentionally not completed: `endpoint_replay_allowed=false`
until an external response is filled and validated.
A replay run template and guarded runner are also present.  After the completed
external reviewer response was imported, one permission-only replay was run.
The result is diagnostic rather than validating: the candidate improves over
the baseline slightly (`Delta chi2 = -0.652452012`) but is not control
resistant because three controls beat the candidate and the best control is
`rank_reverse`.
This is structurally useful: in Tau Core language a full `W_time` projection is
not expected to be a homogeneous function of redshift or scale factor alone.
It should be treated as potentially observer/path dependent and morphology
aware, with source environment, void/web structure, null-geodesic bundle,
observer frame, and readout phase all eligible only when frozen from
independent source-side observables. The tested `W_time_uncertainty_basis` is
therefore only a narrow CC-uncertainty stress test. Its control failure
motivates a richer source-frozen `W_time(z, n_hat, env, path, phi_readout)`
basis rather than a validation claim.
A first preauthorization overlap screen combines the current observer-basis
carrier with this narrow time/readout basis on the same 12-row observer scope.
It tests `observer_only`, `time_on_observer_scope`, `observer_times_time`, and
`observer_plus_time`. The best family remains the pure observer carrier
`W_path_x_sky_x_x_zcenter` with
`delta_chi2_candidate_minus_baseline=-0.58072431813`; the multiplicative
observer/time coupling is weaker (`-0.477935`), the additive proxy is weaker
(`-0.423746`), and the time basis alone is nearly inactive (`-0.030493`). This
is not replay authorization and not validation. It says the present
CC-uncertainty `W_time` proxy does not improve the successful narrow
observer/path proxy; a combined observer/time kernel needs a better
source-native clock/readout observable.
The next source-side attempt replaces uncertainty with a clock-rate/phase
candidate from the fetched cosmic-chronometer `H(z)` values: assigned `log H`,
finite-difference `d log H / d log(1+z)`, and their normalized product. The
preauthorization fast screen finds the product `clock_phase` family as the best
candidate, with `delta_chi2_candidate_minus_baseline=-0.523771964`, but it is
not control-resistant: the best global control is `rank_reverse` on
`clock_level` with `chi2=377.625521`, better than the candidate
`chi2=381.270425`. This is a stronger negative diagnostic than the
uncertainty-only branch: direct CC rate information is more relevant, but the
current low-z CC support has only three bins and remains vulnerable to
redshift-ordering controls.
A follow-up rank-control audit makes the blocker explicit without promoting the
branch to replay. The low-z rows occupy only three CC support bins
(`0:397;1:20;2:7`), each clock family has at most three unique basis values,
and `rank_reverse` is the best local control for all three clock families. The
verdict is
`low_cc_bin_count_rank_control_dominance_confirmed_not_validation`. This means
the present clock-rate/phase proxy is a useful source-side failure analysis,
not an endpoint-ready Tau Core time/readout kernel.

The next focused stress test widens the CC support from low-z only to the
Pantheon rows covered by the fetched CC table. It includes `1370 / 1371`
Pantheon design rows, uses 31 nearest-neighbor CC support bins, and excludes
one row above the CC support. This improves the time/readout signal:
`clock_slope` gives `delta_chi2_candidate_minus_baseline=-1.142872` and
survives its local family controls. But the global control gate still fails:
`rank_reverse/clock_level` remains better than the best candidate. The verdict
is `clock_rate_phase_cc_support_fast_screen_not_control_resistant`. This is a
promising diagnostic for a clock-slope route, not replay authorization.
The follow-up route gate freezes this status explicitly:
`CLOCK_SLOPE_REVIEW_CANDIDATE_ENDPOINT_BLOCKED_BY_GLOBAL_CONTROL`. The allowed
next route is a reviewer-gated `clock_slope`-only candidate, because the slope
tracks a rate of expansion readout, `d log H / d log(1+z)`, rather than the
background clock level. The forbidden route is endpoint replay or validation
language before the global control blocker is resolved.
The reviewer authorization package for this next route is now prepared but not
completed:
`data/derived/pantheon_clock_slope_route_replay_authorization_review_package_v1.zip`.
It contains no endpoint residuals, no endpoint scores, and no fit statistics;
its checksum is recorded in the adjacent `.sha256` file. A completed reviewer
response is required before any `clock_slope`-only replay candidate can be
prepared.

An independent SDSS radial-BAO route audit now checks whether the frozen
multi-tracer BAO/RSD products contain a non-CC time/readout observable. The
radial BAO entries satisfy `D_H/r_d = c/(H(z) r_d)`, so `-log(DH_over_rd)` is a
source-side proxy for `log H(z)` up to the unresolved sound-horizon nuisance
`r_d`. The audit finds exactly two usable `DH_over_rd` rows at `z_eff=0.700`
and `z_eff=0.845`, independent of Pantheon distance residuals and independent
of the CC `clock_level` route. The verdict is
`independent_radial_bao_time_observable_present_but_underresolved_not_replay`:
this is a useful source-side route discovery, not replay authorization and not
validation.

The joint CC+BAO consistency audit then compares the two BAO radial points with
the nearest CC support values. In this two-point source-side check, radial BAO
aligns with the CC `logH` level route (`bao_cc_level_two_point_alignment=1`) and
anti-aligns with the current CC `clock_slope` route
(`bao_cc_slope_two_point_alignment=-1`). This prevents overpromoting BAO as
clock-slope support. The result is instead an independent, underresolved
expansion-level time/readout route:
`radial_bao_aligns_with_cc_level_not_cc_slope_underresolved_not_replay`.

The resulting time/readout synthesis gate records the current route state as:
`clock_slope_review_candidate_plus_independent_bao_level_route_underresolved_not_endpoint`.
The allowed next route is either a completed external authorization for the
`clock_slope` route or separate source-side level/slope time routes built
without endpoint scores. Endpoint replay, validation language, and any claim
that radial BAO already supports the clock-slope route remain forbidden until a
joint nuisance/interface policy is frozen and the current blockers are closed.

The route split is now explicit in:

```text
data/source_manifest/paper10_time_readout_level_slope_route_split_ledger_policy_v1.csv
data/derived/paper10_time_readout_level_slope_route_split_ledger_v1.csv
data/derived/paper10_time_readout_level_slope_route_split_ledger_v1_summary.csv
docs/paper10_time_readout_level_slope_route_split_ledger_v1.md
scripts/build_paper10_time_readout_level_slope_route_split_ledger_v1.py
scripts/validate_paper10_time_readout_level_slope_route_split_ledger_v1.py
```

It records two non-endpoint routes. The `time_level_route` has independent BAO
support and CC-level alignment, but remains two-point underresolved and
`r_d`-blocked. The `time_slope_route` has the CC clock-slope candidate signal,
but remains blocked by global controls and cannot cite radial BAO as supporting
evidence. The ledger verdict is
`level_and_slope_time_routes_split_source_side_not_endpoint`.

The level route also has an explicit nuisance/interface freeze plan:

```text
data/source_manifest/paper10_time_level_route_nuisance_interface_freeze_plan_v1.csv
data/derived/paper10_time_level_route_nuisance_interface_freeze_plan_v1_summary.csv
docs/paper10_time_level_route_nuisance_interface_freeze_plan_v1.md
scripts/validate_paper10_time_level_route_nuisance_interface_freeze_plan_v1.py
```

This plan permits only two-point directional level alignment from `D_H/r_d`.
It forbids fitting `r_d` from Pantheon residuals, claiming an absolute `H(z)`
scale without an `r_d` policy, or using radial BAO as clock-slope support. The
next source gate must freeze an external `r_d` prior or an `r_d`
marginalization policy and expand radial-BAO support before endpoint scoring.

A first `r_d`-cancelled differential check is recorded in:

```text
data/source_manifest/paper10_bao_rd_cancelled_time_level_difference_audit_policy_v1.csv
data/derived/paper10_bao_rd_cancelled_time_level_difference_audit_v1.csv
data/derived/paper10_bao_rd_cancelled_time_level_difference_audit_v1_summary.csv
docs/paper10_bao_rd_cancelled_time_level_difference_audit_v1.md
scripts/build_paper10_bao_rd_cancelled_time_level_difference_audit_v1.py
scripts/validate_paper10_bao_rd_cancelled_time_level_difference_audit_v1.py
```

Because `Delta[-log(D_H/r_d)] = Delta[log H]`, the constant `r_d` term cancels
in the two-point difference. The audit finds directional agreement with the
nearest CC `logH` difference, but the BAO differential signal is low
significance (`delta_bao_snr=0.0997626410319`). The verdict is
`rd_cancels_direction_agrees_but_bao_delta_low_significance_not_endpoint`.
This is useful route discipline, not endpoint evidence.

The current `r_d` policy-selection gate is recorded in:

```text
data/source_manifest/paper10_time_level_rd_policy_selection_gate_v1.csv
data/derived/paper10_time_level_rd_policy_selection_gate_v1_summary.csv
docs/paper10_time_level_rd_policy_selection_gate_v1.md
scripts/validate_paper10_time_level_rd_policy_selection_gate_v1.py
```

It accepts only `rd_cancelled_differential_direction` as the current
source-side policy. `external_rd_prior` and `analytic_rd_marginalization` remain
future routes pending source/protocol freeze. `fit_rd_from_pantheon_residuals`
is explicitly forbidden. The current verdict is
`rd_cancelled_direction_only_currently_allowed_external_or_marginalized_rd_pending`.

The external `r_d` prior route now has a source-side freeze protocol and blank
response template:

```text
data/source_manifest/paper10_external_rd_prior_freeze_protocol_v1.csv
data/derived/paper10_external_rd_prior_freeze_response_template_v1.csv
data/derived/paper10_external_rd_prior_freeze_protocol_v1_summary.csv
docs/paper10_external_rd_prior_freeze_protocol_v1.md
scripts/validate_paper10_external_rd_prior_freeze_protocol_v1.py
```

The protocol accepts only source-side prior families such as
`Planck2018_base_LCDM_rdrag`, `DESI_or_BAO_external_rd_prior`, or
`BBN_BAO_external_rd_prior`, with explicit fields for `rd_mpc`,
`sigma_rd_mpc`, assumption family, source reference, URL/DOI, extraction note,
and source hash/page cache. The template defaults all leakage flags to false.
The current verdict is
`external_rd_prior_protocol_ready_but_no_numeric_prior_frozen`: the protocol is
ready, but no numerical prior is frozen and no endpoint replay is opened.

A first completed caveated external prior response is now recorded in:

```text
data/derived/paper10_external_rd_prior_freeze_response_v1.csv
data/derived/paper10_external_rd_prior_freeze_response_v1_summary.csv
docs/paper10_external_rd_prior_freeze_response_v1.md
scripts/validate_paper10_external_rd_prior_freeze_response_v1.py
```

It freezes the Planck2018 base-\(\Lambda\)CDM TT,TE,EE+lowE+lensing
`rdrag` source value:
`r_d = 147.09 +/- 0.26 Mpc`, cited to Planck 2018 cosmological parameters,
Table 2. This is a caveated external early-universe prior for the time-level
route only. It uses no Pantheon residuals, endpoint scores, or late-time fit
parameters, and it does not authorize endpoint replay. The response verdict is
`planck2018_rd_prior_frozen_as_caveated_external_source_not_endpoint`.

The BAO `r_d` marginalization protocol is recorded in:

```text
data/source_manifest/paper10_bao_rd_marginalization_protocol_v1.csv
data/derived/paper10_bao_rd_marginalization_protocol_v1_summary.csv
docs/paper10_bao_rd_marginalization_protocol_v1.md
scripts/validate_paper10_bao_rd_marginalization_protocol_v1.py
```

It freezes the source-side interface
`-log(D_H/r_d)=logH+beta_rd`, with
`beta_rd=log(r_d)-log(c)` in consistent units. The protocol allows only
analytic linear nuisance projection or predeclared `r_d` prior marginalization.
It forbids Pantheon residuals, endpoint scores, late-time fit parameters,
posthoc `r_d` choices, and using radial BAO as clock-slope support. Its verdict
is `rd_marginalization_protocol_frozen_but_endpoint_still_blocked`.

The time-level endpoint control-suite protocol is recorded in:

```text
data/source_manifest/paper10_time_level_endpoint_control_suite_protocol_v1.csv
data/derived/paper10_time_level_endpoint_control_suite_protocol_v1_summary.csv
docs/paper10_time_level_endpoint_control_suite_protocol_v1.md
scripts/validate_paper10_time_level_endpoint_control_suite_protocol_v1.py
```

It declares seven future control families: `rd_off_control`,
`external_prior_width_stress`, `wrong_prior_control`, `BAO_pair_drop_control`,
`CC_match_window_stress`, `level_slope_swap_control`, and
`redshift_order_shuffle_control`. This is only a protocol declaration. The
controls are not replayed here, no endpoint score is computed, and a future
seed manifest is still required before any replay.

The BAO-support expansion manifest is recorded in:

```text
data/source_manifest/paper10_time_level_bao_support_expansion_manifest_v1.csv
data/derived/paper10_time_level_bao_support_expansion_manifest_v1_summary.csv
docs/paper10_time_level_bao_support_expansion_manifest_v1.md
scripts/validate_paper10_time_level_bao_support_expansion_manifest_v1.py
```

It declares the current SDSS DR16 radial route plus three candidate future
source routes: public DESI radial BAO products, eBOSS/SDSS LyA-QSO radial BAO,
and an independent low-z BAO compilation cross-check. It imports no new BAO
values and opens no endpoint replay. The protocol target is at least four
independent radial BAO support bins before a future endpoint can be considered.

The first source-frozen expansion inventory, for public DESI DR2 BAO products,
is recorded in:

```text
data/source_manifest/paper10_desi_dr2_bao_source_inventory_policy_v1.csv
data/raw/desi_dr2_bao/desi_gaussian_bao_ALL_GCcomb_mean.txt
data/raw/desi_dr2_bao/desi_gaussian_bao_ALL_GCcomb_cov.txt
data/derived/paper10_desi_dr2_bao_source_inventory_v1.csv
data/derived/paper10_desi_dr2_bao_source_inventory_v1_summary.csv
docs/paper10_desi_dr2_bao_source_inventory_v1.md
scripts/build_paper10_desi_dr2_bao_source_inventory_v1.py
scripts/validate_paper10_desi_dr2_bao_source_inventory_v1.py
```

The inventory freezes the public DESI DR2 combined Gaussian BAO mean/covariance
files from the DESI/Cobaya public BAO likelihood route. The cached mean file
contains 13 BAO rows, including 6 radial `DH_over_rs` rows, with a 13 by 13
covariance block. This is source-freeze evidence only: the DESI rows are not
yet integrated into the time-level replay matrix, `r_d` marginalization, or
endpoint controls.

The DESI radial BAO time-level interface is recorded in:

```text
data/source_manifest/paper10_desi_dr2_radial_bao_time_interface_policy_v1.csv
data/derived/paper10_desi_dr2_radial_bao_time_interface_v1.csv
data/derived/paper10_desi_dr2_radial_bao_time_interface_covariance_v1.csv
data/derived/paper10_desi_dr2_radial_bao_time_interface_v1_summary.csv
docs/paper10_desi_dr2_radial_bao_time_interface_v1.md
scripts/build_paper10_desi_dr2_radial_bao_time_interface_v1.py
scripts/validate_paper10_desi_dr2_radial_bao_time_interface_v1.py
```

It converts the six DESI `DH_over_rs` rows into the source-side time-level
observable `-log(DH_over_rs)=logH+beta_rd`, with `beta_rd` retained as an
`r_d` nuisance parameter. The radial covariance subblock is propagated by the
Jacobian rule `C_y,ij=C_x,ij/(x_i*x_j)`. This freezes the interface only; it
still does not match to CC support, open a replay, or claim validation.

The DESI radial BAO to cosmic-chronometer match ledger is recorded in:

```text
data/source_manifest/paper10_desi_dr2_radial_bao_cc_match_policy_v1.csv
data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv
data/derived/paper10_desi_dr2_radial_bao_cc_match_v1_summary.csv
docs/paper10_desi_dr2_radial_bao_cc_match_v1.md
scripts/build_paper10_desi_dr2_radial_bao_cc_match_v1.py
scripts/validate_paper10_desi_dr2_radial_bao_cc_match_v1.py
```

It matches DESI radial BAO rows to the nearest frozen cosmic-chronometer
`H(z)` support point without smoothing or extrapolation. Five DESI rows are
matched within the CC redshift range; the `z=2.33` row is explicitly blocked as
outside CC coverage. This is a source-side support ledger only.

The external-prior readiness gate is recorded in:

```text
data/source_manifest/paper10_time_level_route_external_rd_readiness_gate_v1.csv
data/derived/paper10_time_level_route_external_rd_readiness_gate_v1.csv
data/derived/paper10_time_level_route_external_rd_readiness_gate_v1_summary.csv
docs/paper10_time_level_route_external_rd_readiness_gate_v1.md
scripts/build_paper10_time_level_route_external_rd_readiness_gate_v1.py
scripts/validate_paper10_time_level_route_external_rd_readiness_gate_v1.py
```

This closes only source-side blockers:
`external_rd_prior_source_freeze` and
`joint_rd_marginalization_protocol_definition`, and
`endpoint_control_suite_definition`, and
`bao_support_expansion_manifest_declared`, and
`desi_dr2_public_bao_source_inventory_frozen`, and
`desi_dr2_radial_bao_time_interface_frozen`, and
`desi_dr2_radial_bao_cc_match_ledger_frozen`, and
`desi_dr2_high_z_row_policy_frozen`, and
`desi_time_level_control_seed_manifest_frozen`. The seed manifest freezes seven
control families over the first five-row DESI/CC-matched scope with deterministic
seeds `41001`--`41007`. It deliberately keeps the time-level route outside
endpoint replay. The remaining endpoint blocker is
`time_level_endpoint_authorization_review_missing`. The older
`low_significance_current_sdss_bao_difference` is retained as a diagnostic of the
earlier SDSS-only two-point route, not as an active DESI blocker. The gate verdict
is
`desi_time_cc_matched_scope_and_controls_frozen_but_endpoint_authorization_missing`.

The reviewer handoff for that final blocker is recorded in:

```text
docs/paper10_desi_time_level_endpoint_authorization_review_v1.md
data/source_manifest/paper10_desi_time_level_endpoint_authorization_review_policy_v1.csv
data/derived/paper10_desi_time_level_endpoint_authorization_review_response_template_v1.csv
data/derived/paper10_desi_time_level_endpoint_authorization_review_template_v1_summary.csv
data/derived/paper10_desi_time_level_endpoint_authorization_review_package_v1.zip
data/derived/paper10_desi_time_level_endpoint_authorization_review_package_v1.zip.sha256
data/derived/paper10_desi_time_level_endpoint_authorization_review_package_v1_manifest.csv
data/derived/paper10_desi_time_level_endpoint_authorization_review_package_v1_summary.csv
scripts/build_paper10_desi_time_level_endpoint_authorization_review_template_v1.py
scripts/validate_paper10_desi_time_level_endpoint_authorization_review_template_v1.py
scripts/build_paper10_desi_time_level_endpoint_authorization_review_package_v1.py
scripts/validate_paper10_desi_time_level_endpoint_authorization_review_package_v1.py
```

The package is intentionally blank/not completed:
`endpoint_replay_allowed=false`, `endpoint_validation_claimed=false`, and
`physical_validation_claimed=false`. It contains no endpoint residuals, scores,
or fit statistics. It only asks a reviewer whether a later permission-only
five-row DESI/CC replay may be prepared under the frozen controls.

If a completed external reviewer CSV is returned for this DESI handoff, validate
and import it with:

```bash
python scripts/import_paper10_desi_time_level_endpoint_authorization_review_response_v1.py \
  /path/to/completed_desi_time_level_endpoint_authorization_response.csv
```

The importer first runs
`scripts/validate_paper10_desi_time_level_endpoint_authorization_review_response_v1.py`.
Canonical response artifacts are written only if the completed CSV accepts all
five authorization questions, keeps `forbidden_inputs_used=false`, and keeps
`endpoint_validation_claimed=false` and `physical_validation_claimed=false`.

The replay grammar that would be used after such an authorization is frozen in:

```text
docs/paper10_desi_time_level_endpoint_replay_run_template_v1.md
data/source_manifest/paper10_desi_time_level_endpoint_replay_run_template_v1.csv
scripts/validate_paper10_desi_time_level_endpoint_replay_run_template_v1.py
```

This template remains `endpoint_replay_allowed=false`. It only records the
future replay scope, excluded high-z row, seven control families, and forbidden
inputs.

The completed DESI authorization response has now been imported and validated:

```text
docs/paper10_desi_time_level_endpoint_authorization_review_response_v1.md
data/derived/paper10_desi_time_level_endpoint_authorization_review_response_v1.csv
data/derived/paper10_desi_time_level_endpoint_authorization_review_response_v1_summary.csv
```

Its decision is
`GO_DESI_CC_5ROW_TIME_LEVEL_REPLAY_PERMISSION_ONLY`. This authorizes preparation
of one guarded replay under the frozen five-row scope and seven controls, while
keeping `endpoint_validation_claimed=false` and
`physical_validation_claimed=false`. No endpoint score is produced by the
authorization response.

The permission-only replay has now been run and preserved as a negative
control-result artifact:

```text
docs/paper10_desi_time_level_endpoint_authorized_replay_v1.md
data/derived/paper10_desi_time_level_endpoint_authorized_replay_v1_grid.csv
data/derived/paper10_desi_time_level_endpoint_authorized_replay_v1_summary.csv
scripts/run_paper10_desi_time_level_endpoint_authorized_replay_v1.py
scripts/validate_paper10_desi_time_level_endpoint_authorized_replay_v1.py
```

It fits the constant `beta_rd` nuisance over the five DESI/CC rows and reports
`candidate_chi2=5.52425578108`. The result is not control-resistant:
`best_control_branch=redshift_order_shuffle_control`,
`best_control_chi2=2.14549721198`, and
`verdict=desi_time_level_permission_replay_not_control_resistant_not_validation`.
This is a useful endpoint diagnostic, not a validation result.

A focused negative-control diagnostic explains the failure mode without changing
the replay:

```text
docs/paper10_desi_time_level_negative_control_diagnostic_v1.md
data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_rows.csv
data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_branches.csv
data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_summary.csv
paper10_submission_source/figures/fig_desi_time_level_negative_control_diagnostic.pdf
scripts/build_paper10_desi_time_level_negative_control_diagnostic_v1.py
scripts/validate_paper10_desi_time_level_negative_control_diagnostic_v1.py
```

The diagnostic verdict is
`desi_time_level_negative_control_diagnostic_explains_non_control_resistance_not_validation`.
Its failure mode is
`five_row_time_level_constant_beta_endpoint_is_ordering_fragile`: the candidate
constant-level fit is not catastrophic, but the five-row time-level endpoint is
too small and ordering-fragile to distinguish the candidate from frozen
controls. The recommended next action is to retain this negative control and
require richer independent clock or time-readout support before any endpoint
claim.

The negative-control response gate is recorded in:

```text
docs/paper10_desi_time_level_negative_control_response_gate_v1.md
data/source_manifest/paper10_desi_time_level_negative_control_response_gate_v1.csv
data/derived/paper10_desi_time_level_negative_control_response_gate_v1.csv
data/derived/paper10_desi_time_level_negative_control_response_gate_v1_summary.csv
scripts/build_paper10_desi_time_level_negative_control_response_gate_v1.py
scripts/validate_paper10_desi_time_level_negative_control_response_gate_v1.py
```

It closes the first DESI/CC constant-beta route as
`DESI_TIME_LEVEL_ROUTE_BLOCKED_PENDING_RICHER_CLOCK_READOUT_SUPPORT`; replay
remains disabled. The next allowed action is only
`build_source_side_time_readout_expansion_manifest_only`.

That expansion manifest is recorded in:

```text
docs/paper10_desi_time_readout_expansion_manifest_v1.md
data/source_manifest/paper10_desi_time_readout_expansion_manifest_v1.csv
data/derived/paper10_desi_time_readout_expansion_manifest_v1_summary.csv
scripts/validate_paper10_desi_time_readout_expansion_manifest_v1.py
```

It freezes five required source-side gates before the DESI time-level route can
be considered again: high-z independent clock support, multiple clock support
per BAO row, a time/readout shape observable beyond a constant level, preserved
ordering controls, and a joint covariance/nuisance policy. It currently has
`endpoint_ready_route_count=0`; the next primary source gate is
`HIGH_Z_INDEPENDENT_CLOCK_SUPPORT`, with `TIME_READOUT_SHAPE_OBSERVABLE` as the
parallel route.

The first high-z support audit is recorded in:

```text
docs/paper10_desi_high_z_independent_clock_support_audit_v1.md
data/source_manifest/paper10_desi_high_z_independent_clock_support_audit_policy_v1.csv
data/derived/paper10_desi_high_z_independent_clock_support_audit_v1.csv
data/derived/paper10_desi_high_z_independent_clock_support_audit_v1_summary.csv
scripts/build_paper10_desi_high_z_independent_clock_support_audit_v1.py
scripts/validate_paper10_desi_high_z_independent_clock_support_audit_v1.py
```

It confirms that the frozen CC table has 32 rows and ends at `z=1.965`.
The excluded DESI Ly-alpha row is at `z=2.33`, with
`delta_z_to_nearest_frozen_clock=0.365`, so it is neither inside nor bracketed
by the frozen clock support. The verdict is
`desi_high_z_clock_support_missing_row_remains_holdout_not_validation`, and the
row cannot enter replay without a new source-frozen high-z clock/readout route.

The parallel time/readout shape-observable gate is recorded in:

```text
docs/paper10_desi_time_readout_shape_observable_gate_v1.md
data/source_manifest/paper10_desi_time_readout_shape_observable_gate_policy_v1.csv
data/derived/paper10_desi_time_readout_shape_observable_gate_v1.csv
data/derived/paper10_desi_time_readout_shape_observable_gate_v1_summary.csv
scripts/build_paper10_desi_time_readout_shape_observable_gate_v1.py
scripts/validate_paper10_desi_time_readout_shape_observable_gate_v1.py
```

It removes the constant `beta_rd` nuisance by freezing adjacent first
differences of `-log(D_H/r_d)-log H_CC` over the five CC-matched DESI rows, and
also records an uneven-grid second-difference curvature proxy. The gate produces
four first-difference rows and three second-difference rows, with maximum
diagonal signal-to-noise values `1.90323313675` and `1.72319652004`,
respectively. This is a useful source-side candidate shape, but it is not an
endpoint route: the excluded high-z row still lacks independent clock support,
and the shape observable uses only the five nearest-neighbor CC-matched rows.
The verdict is
`desi_time_readout_shape_candidate_frozen_but_not_endpoint_ready`.

The same frozen shape observable is also mapped onto the current Tau Core
general readout-basis and projection-induction discipline:

```text
docs/paper10_desi_time_readout_shape_projection_induction_v1.md
data/source_manifest/paper10_desi_time_readout_shape_projection_induction_policy_v1.csv
data/derived/paper10_desi_time_readout_shape_projection_induction_v1.csv
data/derived/paper10_desi_time_readout_shape_projection_induction_v1_summary.csv
scripts/build_paper10_desi_time_readout_shape_projection_induction_v1.py
scripts/validate_paper10_desi_time_readout_shape_projection_induction_v1.py
```

This ledger classifies the clock-slope and curvature shapes as `K_time`
candidates, keeps radial BAO level information as `K_closure` context, and
keeps redshift-order controls in `K_null`. Its verdict is
`time_shape_maps_to_K_time_candidate_but_projection_induction_incomplete`: the
shape has source-candidate activation, but quotient survival, closure
stability, and 4D readout survival are not yet proven, and replay remains
disabled.

The corresponding `K_null` ordering-control suite is recorded in:

```text
docs/paper10_desi_ordering_control_suite_v1.md
data/source_manifest/paper10_desi_ordering_control_suite_policy_v1.csv
data/derived/paper10_desi_ordering_control_suite_v1.csv
data/derived/paper10_desi_ordering_control_suite_v1_summary.csv
scripts/build_paper10_desi_ordering_control_suite_v1.py
scripts/validate_paper10_desi_ordering_control_suite_v1.py
```

It declares five required control families:
`redshift_order_shuffle`, `leave_row_or_pair`, `cc_window_stress`,
`wrong_time_basis`, and `rd_prior_stress`. Only the redshift-order shuffle is
currently available from the negative-control diagnostic; none are yet bound to
the shape route. The verdict is
`k_null_ordering_controls_declared_but_not_shape_bound`.

The first shape-bound control-vector ledger is recorded in:

```text
docs/paper10_desi_shape_bound_control_vectors_v1.md
data/source_manifest/paper10_desi_shape_bound_control_vectors_policy_v1.csv
data/derived/paper10_desi_shape_bound_control_vectors_v1.csv
data/derived/paper10_desi_shape_bound_control_vectors_v1_summary.csv
scripts/build_paper10_desi_shape_bound_control_vectors_v1.py
scripts/validate_paper10_desi_shape_bound_control_vectors_v1.py
```

It now binds all five controls to the frozen shape route without endpoint
scores or endpoint residuals. The CC-window stress is supplied by the Row4
source-side review chain and is bound only as caveated source context:

```text
docs/paper10_desi_cc_window_stress_binding_v1.md
data/source_manifest/paper10_desi_cc_window_stress_binding_policy_v1.csv
data/derived/paper10_desi_cc_window_stress_binding_v1.csv
data/derived/paper10_desi_cc_window_stress_binding_v1_summary.csv
scripts/build_paper10_desi_cc_window_stress_binding_v1.py
scripts/validate_paper10_desi_cc_window_stress_binding_v1.py
```

The control suite is therefore shape-bound, but it still cannot enter replay.
The verdict is `shape_route_controls_bound_but_replay_not_authorized`.

The corresponding multi-clock support audit is recorded in:

```text
docs/paper10_desi_multi_clock_support_per_bao_row_audit_v1.md
data/source_manifest/paper10_desi_multi_clock_support_per_bao_row_audit_policy_v1.csv
data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1.csv
data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1_summary.csv
scripts/build_paper10_desi_multi_clock_support_per_bao_row_audit_v1.py
scripts/validate_paper10_desi_multi_clock_support_per_bao_row_audit_v1.py
```

It checks whether each of the five authorized DESI radial rows has at least two
clock entries and at least two independent reference sources in fixed redshift
windows. In the strict `delta_z <= 0.05` window, three of five rows pass. In the
relaxed `delta_z <= 0.10` window, four of five pass; radial row `4` remains
blocked because its two relaxed-window clock entries come from only one
independent reference source. The verdict is
`desi_multi_clock_support_incomplete_not_endpoint_ready`.

Because the shape observable exists but the clock support remains incomplete, a
separate independent shape-review handoff package is prepared:

```text
docs/paper10_desi_time_readout_shape_independent_review_v1.md
data/source_manifest/paper10_desi_time_readout_shape_independent_review_policy_v1.csv
data/derived/paper10_desi_time_readout_shape_independent_review_response_template_v1.csv
data/derived/paper10_desi_time_readout_shape_independent_review_package_v1.zip
data/derived/paper10_desi_time_readout_shape_independent_review_package_v1.zip.sha256
data/derived/paper10_desi_time_readout_shape_independent_review_package_v1_manifest.csv
data/derived/paper10_desi_time_readout_shape_independent_review_package_v1_summary.csv
scripts/build_paper10_desi_time_readout_shape_independent_review_package_v1.py
scripts/validate_paper10_desi_time_readout_shape_independent_review_package_v1.py
```

This package asks only whether the adjacent-difference / curvature shape
observable may be retained as a caveated source-side diagnostic candidate. It is
blank and uncompleted, contains no endpoint residuals, scores, or fit
statistics, and keeps `endpoint_replay_allowed=false`.

After the five shape-route controls are bound, a separate replay-authorization
handoff is prepared:

```text
docs/paper10_desi_shape_route_replay_authorization_review_v1.md
data/source_manifest/paper10_desi_shape_route_replay_authorization_review_policy_v1.csv
data/derived/paper10_desi_shape_route_replay_authorization_review_response_template_v1.csv
data/derived/paper10_desi_shape_route_replay_authorization_review_package_v1.zip
data/derived/paper10_desi_shape_route_replay_authorization_review_package_v1.zip.sha256
data/derived/paper10_desi_shape_route_replay_authorization_review_package_v1_manifest.csv
data/derived/paper10_desi_shape_route_replay_authorization_review_package_v1_summary.csv
scripts/build_paper10_desi_shape_route_replay_authorization_review_package_v1.py
scripts/validate_paper10_desi_shape_route_replay_authorization_review_package_v1.py
scripts/validate_paper10_desi_shape_route_replay_authorization_review_response_v1.py
scripts/import_paper10_desi_shape_route_replay_authorization_review_response_v1.py
```

This package asks a reviewer whether the already frozen DESI shape route may be
advanced to replay. It is still blank and uncompleted, contains no endpoint
residuals, scores, or fit statistics, keeps `endpoint_replay_allowed=false`, and
records `shape_bound_control_count=5` with `unbound_control_families=none`.
The verdict is
`desi_shape_route_replay_authorization_package_ready_not_completed`.
The completed-response validator can only promote a reviewer `GO` to
permission-only replay status; it still requires
`endpoint_validation_claimed=false` and `physical_validation_claimed=false`, and
rejects any response with forbidden endpoint fields.

The completed external response has been imported and validated:

```text
docs/paper10_desi_shape_route_replay_authorization_review_notes_v1.md
data/derived/paper10_desi_shape_route_replay_authorization_review_response_v1.csv
data/derived/paper10_desi_shape_route_replay_authorization_review_response_v1_summary.csv
data/derived/paper10_desi_shape_route_replay_authorization_review_completed_summary_v1.csv
data/derived/paper10_desi_shape_route_replay_authorization_validation_log_v1.txt
```

The decision is `GO_DESI_SHAPE_ROUTE_REPLAY_PERMISSION_ONLY`. This authorizes
one separate predeclared DESI shape-route replay. It does not claim endpoint
validation or physical validation.

The corresponding shape-route replay-run template is recorded in:

```text
docs/paper10_desi_shape_route_replay_run_template_v1.md
data/source_manifest/paper10_desi_shape_route_replay_run_template_v1.csv
scripts/validate_paper10_desi_shape_route_replay_run_template_v1.py
```

This template freezes the five-row radial scope, four adjacent shape rows, three
curvature rows, and the five shape-bound control families. It remains
authorization-required and keeps `endpoint_replay_allowed=false`; it is a run
grammar, not a replay result.

The authorized DESI shape-route replay is recorded in:

```text
data/derived/paper10_desi_shape_route_authorized_replay_v1_grid.csv
data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv
scripts/run_paper10_desi_shape_route_authorized_replay_v1.py
scripts/validate_paper10_desi_shape_route_authorized_replay_v1.py
```

The replay uses a source-native quadratic shape score. The candidate
`CLOCK_SLOPE_SHAPE` score is `5.52425578108`; the best control is
`control_leave_shape_row_max` with score `5.50939872844`. The candidate exceeds
all frozen controls, but the margin to the strongest leave-row control is small
(`0.01485705264`). This is therefore a permission-only positive replay signal,
not endpoint validation and not physical validation.

The internal robustness stress for this replay is recorded in:

```text
docs/paper10_desi_shape_route_robustness_stress_v1.md
data/source_manifest/paper10_desi_shape_route_robustness_stress_policy_v1.csv
data/derived/paper10_desi_shape_route_robustness_stress_v1.csv
data/derived/paper10_desi_shape_route_robustness_stress_v1_summary.csv
paper10_submission_source/figures/fig_desi_shape_route_robustness_stress.pdf
scripts/build_paper10_desi_shape_route_robustness_stress_v1.py
scripts/validate_paper10_desi_shape_route_robustness_stress_v1.py
scripts/build_paper10_desi_shape_route_robustness_figure_v1.py
scripts/validate_paper10_desi_shape_route_robustness_figure_v1.py
docs/paper10_desi_shape_row_sensitivity_source_audit_v1.md
data/source_manifest/paper10_desi_shape_row_sensitivity_source_audit_policy_v1.csv
data/derived/paper10_desi_shape_row_sensitivity_source_audit_v1.csv
data/derived/paper10_desi_shape_row_sensitivity_source_audit_v1_summary.csv
scripts/build_paper10_desi_shape_row_sensitivity_source_audit_v1.py
scripts/validate_paper10_desi_shape_row_sensitivity_source_audit_v1.py
docs/paper10_desi_shape_core_source_acquisition_manifest_v1.md
data/source_manifest/paper10_desi_shape_core_source_acquisition_manifest_policy_v1.csv
data/derived/paper10_desi_shape_core_source_acquisition_manifest_v1.csv
data/derived/paper10_desi_shape_core_source_acquisition_manifest_v1_summary.csv
scripts/build_paper10_desi_shape_core_source_acquisition_manifest_v1.py
scripts/validate_paper10_desi_shape_core_source_acquisition_manifest_v1.py
docs/paper10_desi_shape_core_source_support_scan_v1.md
data/source_manifest/paper10_desi_shape_core_source_support_scan_policy_v1.csv
data/derived/paper10_desi_shape_core_source_support_scan_v1.csv
data/derived/paper10_desi_shape_core_source_support_scan_v1_summary.csv
scripts/build_paper10_desi_shape_core_source_support_scan_v1.py
scripts/validate_paper10_desi_shape_core_source_support_scan_v1.py
docs/paper10_desi_shape_row2_moresco2012_source_attachment_v1.md
data/source_manifest/paper10_desi_shape_row2_moresco2012_source_attachment_policy_v1.csv
data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_v1.csv
data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_v1_summary.csv
scripts/build_paper10_desi_shape_row2_moresco2012_source_attachment_v1.py
scripts/validate_paper10_desi_shape_row2_moresco2012_source_attachment_v1.py
docs/paper10_desi_shape_row2_moresco2012_source_attachment_review_v1.md
data/source_manifest/paper10_desi_shape_row2_moresco2012_source_attachment_review_policy_v1.csv
data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_response_template_v1.csv
data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.zip
data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.zip.sha256
data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1_manifest.csv
data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1_summary.csv
scripts/build_paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.py
scripts/validate_paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.py
scripts/validate_paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1.py
scripts/import_paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1.py
data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1.csv
data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_response_v1_summary.csv
docs/paper10_desi_shape_row2_moresco2012_source_attachment_review_notes_v1.md
data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_validation_log_v1.txt
docs/paper10_desi_shape_row2_promotion_readiness_gate_v1.md
data/source_manifest/paper10_desi_shape_row2_promotion_readiness_gate_policy_v1.csv
data/derived/paper10_desi_shape_row2_promotion_readiness_gate_v1.csv
data/derived/paper10_desi_shape_row2_promotion_readiness_gate_v1_summary.csv
scripts/build_paper10_desi_shape_row2_promotion_readiness_gate_v1.py
scripts/validate_paper10_desi_shape_row2_promotion_readiness_gate_v1.py
docs/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.md
data/source_manifest/paper10_desi_shape_row2_endpoint_pair_independence_scout_policy_v1.csv
data/derived/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.csv
data/derived/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1_summary.csv
scripts/build_paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.py
scripts/validate_paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.py
docs/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.md
data/source_manifest/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_policy_v1.csv
data/derived/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.csv
data/derived/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1_summary.csv
scripts/build_paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.py
scripts/validate_paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.py
docs/paper10_desi_shape_row2_left_endpoint_window_review_v1.md
data/source_manifest/paper10_desi_shape_row2_left_endpoint_window_review_policy_v1.csv
data/derived/paper10_desi_shape_row2_left_endpoint_window_review_response_template_v1.csv
data/derived/paper10_desi_shape_row2_left_endpoint_window_review_package_v1.zip
data/derived/paper10_desi_shape_row2_left_endpoint_window_review_package_v1.zip.sha256
data/derived/paper10_desi_shape_row2_left_endpoint_window_review_package_v1_manifest.csv
data/derived/paper10_desi_shape_row2_left_endpoint_window_review_package_v1_summary.csv
scripts/build_paper10_desi_shape_row2_left_endpoint_window_review_package_v1.py
scripts/validate_paper10_desi_shape_row2_left_endpoint_window_review_package_v1.py
scripts/validate_paper10_desi_shape_row2_left_endpoint_window_review_response_v1.py
scripts/import_paper10_desi_shape_row2_left_endpoint_window_review_response_v1.py
data/derived/paper10_desi_shape_row2_left_endpoint_window_review_response_v1.csv
data/derived/paper10_desi_shape_row2_left_endpoint_window_review_response_v1_summary.csv
docs/paper10_desi_shape_row2_left_endpoint_window_review_notes_v1.md
data/derived/paper10_desi_shape_row2_left_endpoint_window_review_validation_log_v1.txt
docs/paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1.md
data/source_manifest/paper10_desi_shape_row2_left_endpoint_window_decision_gate_policy_v1.csv
data/derived/paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1.csv
data/derived/paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1_summary.csv
scripts/build_paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1.py
scripts/validate_paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1.py
docs/paper10_desi_shape_row2_post_window_review_source_plan_v1.md
data/source_manifest/paper10_desi_shape_row2_post_window_review_source_plan_policy_v1.csv
data/derived/paper10_desi_shape_row2_post_window_review_source_plan_v1.csv
data/derived/paper10_desi_shape_row2_post_window_review_source_plan_v1_summary.csv
scripts/build_paper10_desi_shape_row2_post_window_review_source_plan_v1.py
scripts/validate_paper10_desi_shape_row2_post_window_review_source_plan_v1.py
docs/paper10_desi_shape_row2_left_strict_support_scout_v1.md
data/source_manifest/paper10_desi_shape_row2_left_strict_support_scout_policy_v1.csv
data/derived/paper10_desi_shape_row2_left_strict_support_scout_v1.csv
data/derived/paper10_desi_shape_row2_left_strict_support_scout_v1_summary.csv
scripts/build_paper10_desi_shape_row2_left_strict_support_scout_v1.py
scripts/validate_paper10_desi_shape_row2_left_strict_support_scout_v1.py
docs/paper10_desi_shape_row2_source_native_shape_support_scout_v1.md
data/source_manifest/paper10_desi_shape_row2_source_native_shape_support_scout_policy_v1.csv
data/derived/paper10_desi_shape_row2_source_native_shape_support_scout_v1.csv
data/derived/paper10_desi_shape_row2_source_native_shape_support_scout_v1_summary.csv
scripts/build_paper10_desi_shape_row2_source_native_shape_support_scout_v1.py
scripts/validate_paper10_desi_shape_row2_source_native_shape_support_scout_v1.py
docs/paper10_desi_shape_row2_source_native_shape_support_review_v1.md
data/source_manifest/paper10_desi_shape_row2_source_native_shape_support_review_policy_v1.csv
data/derived/paper10_desi_shape_row2_source_native_shape_support_review_response_template_v1.csv
data/derived/paper10_desi_shape_row2_source_native_shape_support_review_package_v1.zip
data/derived/paper10_desi_shape_row2_source_native_shape_support_review_package_v1.zip.sha256
data/derived/paper10_desi_shape_row2_source_native_shape_support_review_package_v1_manifest.csv
data/derived/paper10_desi_shape_row2_source_native_shape_support_review_package_v1_summary.csv
scripts/build_paper10_desi_shape_row2_source_native_shape_support_review_package_v1.py
scripts/validate_paper10_desi_shape_row2_source_native_shape_support_review_package_v1.py
scripts/validate_paper10_desi_shape_row2_source_native_shape_support_review_response_v1.py
scripts/import_paper10_desi_shape_row2_source_native_shape_support_review_response_v1.py
data/derived/paper10_desi_shape_row2_source_native_shape_support_review_response_v1.csv
data/derived/paper10_desi_shape_row2_source_native_shape_support_review_response_v1_summary.csv
docs/paper10_desi_shape_row2_source_native_shape_support_review_notes_v1.md
data/derived/paper10_desi_shape_row2_source_native_shape_support_review_validation_log_v1.txt
docs/paper10_desi_shape_row2_gate_status_ledger_v1.md
data/source_manifest/paper10_desi_shape_row2_gate_status_ledger_policy_v1.csv
data/derived/paper10_desi_shape_row2_gate_status_ledger_v1.csv
data/derived/paper10_desi_shape_row2_gate_status_ledger_v1_summary.csv
scripts/build_paper10_desi_shape_row2_gate_status_ledger_v1.py
scripts/validate_paper10_desi_shape_row2_gate_status_ledger_v1.py
docs/paper10_desi_shape_row2_promotion_review_v1.md
data/source_manifest/paper10_desi_shape_row2_promotion_review_policy_v1.csv
data/derived/paper10_desi_shape_row2_promotion_review_response_template_v1.csv
data/derived/paper10_desi_shape_row2_promotion_review_package_v1.zip
data/derived/paper10_desi_shape_row2_promotion_review_package_v1.zip.sha256
data/derived/paper10_desi_shape_row2_promotion_review_package_v1_manifest.csv
data/derived/paper10_desi_shape_row2_promotion_review_package_v1_summary.csv
scripts/build_paper10_desi_shape_row2_promotion_review_package_v1.py
scripts/validate_paper10_desi_shape_row2_promotion_review_package_v1.py
```

The stress keeps the candidate ranked first by the frozen shape score, but it
also shows that the margin is very narrow (`0.00268942156713` fractionally
relative to the candidate score) and that the strongest leave-one-row stress
retains `0.997310578432` of the full candidate score. The verdict is therefore
`positive_but_narrow_margin_and_row_sensitive_not_validation`.

Compact stress ledger:

| Quantity | Value | Claim-safe reading |
| --- | ---: | --- |
| Candidate score | `5.52425578108` | Rank `1` by frozen quadratic shape score |
| Best control score | `5.50939872844` | Strongest control is leave-shape-row |
| Fractional margin | `0.00268942156713` | Positive but narrow |
| Strongest leave-one stress | `0.997310578432` | Row-sensitive |
| Drop Row2 stress | `0.749151602906` | Row2 is important but not the sole carrier |
| Most required row | Row1; `0.669168123641` retained when dropped | Core signal is concentrated in middle rows |
| Strongest leave-two stress | `0.83195519127` | Not purely single-row, but not validation |

The follow-up row-sensitivity source audit identifies shape rows `1;2` as the
core-sensitive middle rows. Row `0` is the most dispensable row, row `1` is the
most required row, and row `2` remains source-caveated because its current CC
support endpoints come from the same reference family. The recommended next
action is independent clock or shape support for rows `1` and `2`, especially
row `2`, before any DESI shape-route promotion.

The shape-core source acquisition manifest freezes this as a concrete work
order: `DESI_SHAPE_ROW_2_CORE_SUPPORT` is `P0`, because it is core-sensitive and
single-reference caveated; `DESI_SHAPE_ROW_1_CORE_SUPPORT` is `P1`, because it
is the most required row and needs confirmatory independent support. The
manifest does not fetch sources and keeps replay disabled.

Scanning the already frozen cosmic-chronometer table finds existing
independent in-interval support for the P0 row-2 target: `Moresco et al. (2012)`
at `z=1.037`, with `H(z)=153.7 +/- 19.6736`. This partially strengthens the
row-2 source status, but it is not a full endpoint-pair replacement and does
not authorize replay.
For the P1 Row1 target, the same frozen CC scan also supplies two independent
in-interval confirmatory support rows: `Borghi et al. (2022)` at `z=0.75` and
`Stern et al. (2010)` at `z=0.88`. These are attached only as source-side
confirmation for the most required row; they do not make Row1 endpoint-ready and
do not authorize replay.
The corresponding repository-independent Row1 source-review package has now
also been completed. The reviewer response accepts those two rows as
confirmatory independent in-interval Row1 support, while keeping endpoint
replay, endpoint validation, physical validation, and route promotion false.

The follow-up source-attachment ledger promotes that support-scan finding into
a reviewable row-2 attachment:
`row2_moresco2012_in_interval_support_attached_partial_not_endpoint_ready`.
It records source key `Moresco2012ExpansionRate`, arXiv `1201.3609`, DOI
`10.1088/1475-7516/2012/08/006`, and keeps
`endpoint_replay_allowed=false`, `endpoint_validation_claimed=false`, and
`physical_validation_claimed=false`. The attachment reduces the row-2 source
caveat but still does not supply an endpoint-pair replacement.

A repository-independent reviewer package is also prepared at
`data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_review_package_v1.zip`.
It asks only whether the attachment may be accepted as caveat-reducing
source-side support. The package is blank/uncompleted and cannot authorize
replay or validation.
The completed-response validator accepts only three source-side outcomes:
caveat-reducing acceptance, rejection, or needs-more-context. Even an accepted
response keeps `endpoint_pair_replacement=false`, `row2_endpoint_ready=false`,
`endpoint_replay_allowed=false`, and all validation claims false. The importer
copies completed reviewer artifacts into canonical paths only after this
validator succeeds.

The completed reviewer response accepts the attachment only as caveat-reducing
row-2 source support:
`row2_moresco2012_attachment_accepted_as_caveat_reducing_not_endpoint_ready`.
The canonical response keeps `forbidden_inputs_used=false`,
`endpoint_pair_replacement=false`, `row2_endpoint_ready=false`,
`endpoint_replay_allowed=false`, `endpoint_validation_claimed=false`, and
`physical_validation_claimed=false`. The next allowed action remains endpoint
pair independence or a separate replay/promotion gate; this review alone does
not move the DESI shape route to endpoint-ready status.
The row-2 promotion-readiness gate freezes this implication:
`row2_combined_caveats_reduced_but_promotion_and_endpoint_pair_independence_blockers_remain`.
Thus row 2 is stronger than before because both the Moresco2012 in-interval
support and the DESI source-native shape context are accepted as caveat-reducing
source-side evidence, but `row2_promotion_ready=false` and
`shape_route_promotion_allowed=false` until endpoint-pair independence or a
separate promotion review is obtained.

A focused endpoint-pair independence scout then checks the already frozen
cosmic-chronometer table around row 2. It finds one strict independent
right-endpoint candidate, `Moresco (2015)`, but no strict independent
left-endpoint support. The resulting verdict is
`row2_endpoint_pair_independence_not_satisfied_in_frozen_CC_table`; the row
therefore remains caveat-reduced but not promotion-ready. The next allowed
source-side action is a left-endpoint independent clock source or a
source-native shape support route before any replay or promotion can be
considered.

The left-endpoint near-miss freeze records the useful but still insufficient
context explicitly. It finds two relaxed independent left-endpoint candidates:
`Stern et al. (2010)` at `z=0.88` and `Moresco et al. (2012)` at `z=0.8754`.
The closest one misses the frozen strict endpoint window by a small amount
(`|0.88-0.934|=0.054` while the strict window is `0.05`). The machine verdict is
`row2_left_endpoint_has_relaxed_independent_nearmisses_but_no_strict_support`.
This motivates a separate source-window review or a source-native
shape-support search, but it keeps `left_endpoint_release_allowed=false`,
`row2_promotion_ready=false`, and all replay/validation flags false.

A repository-independent source-window review package is prepared for that
narrow question at
`data/derived/paper10_desi_shape_row2_left_endpoint_window_review_package_v1.zip`
with checksum
`bea5e03193895643398a20d2603eebe0b41fa57e54a0efbe63f1f87178fdb574`.
The package is intentionally blank and asks only whether the relaxed near-miss
sources may be treated as caveated source-window context. It contains no
endpoint residuals, no endpoint scores, and no fit statistics. Until a completed
response is validated, `left_endpoint_release_allowed=false`,
`row2_promotion_ready=false`, and replay remains disabled.
The completed-response validator accepts only internally consistent
source-window outcomes. In the strongest allowed positive case it records
`source_reopen_caveated=true`, but still keeps
`left_endpoint_release_allowed=false`, `row2_promotion_ready=false`, and
`endpoint_replay_allowed=false`. Any response that sets replay or validation
flags is rejected before canonical artifacts are modified.
The companion decision gate resolves the current machine state. With no
completed response imported it would record pending status. The completed
reviewer response is now imported and validates the strongest allowed
source-side outcome:
`ROW2_LEFT_SOURCE_REOPEN_CAVEATED_NO_REPLAY`, with verdict
`row2_left_source_reopen_caveated_no_replay`. This means the left endpoint
source-window route is reopened only as caveated source context. It still keeps
`left_endpoint_release_allowed=false`, `row2_promotion_ready=false`,
`shape_route_promotion_allowed=false`, and all replay/validation flags false.
The post-window-review source plan then freezes the only allowed next source
targets. The current status is
`ROW2_SOURCE_REOPENED_CAVEATED_LEFT_ENDPOINT_STILL_NOT_RELEASED`: the source
route is reopened only in a caveated source-side sense, with strict left-endpoint
support still at zero. The two P0 targets are (i) independent strict left-endpoint
support inside the frozen window, or (ii) source-native shape support for the
row-2 interval. Both routes forbid endpoint residuals, endpoint scores, and
kernel-performance feedback.
The left strict-support scout preserves the current negative source-side
result. In the frozen CC table the nearest point to the row-2 left endpoint is
the existing same-family Simon et al. (2005) point at `z=0.9`; the nearest
independent candidate is Stern et al. (2010) at `z=0.88`, with
`|Delta z|=0.054`, just outside the strict `0.05` window. The verdict is
`row2_left_strict_support_absent_in_frozen_cc_table`. Thus the strict-left P0
route remains genuinely open and no replay or promotion is authorized.
The complementary source-native shape-support scout finds that the row-2
interval does have DESI DR2 BAO shape information at both endpoints: `DM/rs`
and `DH/rs` at `z=0.934` and `z=1.321`, with a positive-definite covariance
subblock. It freezes the source-native vector
`delta_log_DM_over_rs=0.246281910984`,
`delta_log_DH_over_rs=-0.218701863111`, and
`delta_log_anisotropy_DM_over_DH=0.464983774095`. This is positive source-side
support for the shape route, but it still uses no endpoint residuals or scores
and keeps `row2_promotion_ready=false`.
The corresponding external review package is now built as a blank
source-side-only package. It asks whether this DESI DR2 source-native BAO vector
may be accepted as caveat-reducing Row2 support. It contains the frozen source
rows, covariance source files, inventory, scout artifacts, and response
template, but no endpoint residuals, scores, or fit statistics. The package
verdict is `row2_source_native_shape_support_review_package_ready_not_completed`.
The completed external response accepts the vector as caveat-reducing
source-native shape context:
`row2_source_native_shape_support_accepted_as_caveat_reducing_not_endpoint_ready`.
This reduces the Row2 source caveat, but it does not make Row2 endpoint-ready,
does not promote the route, and does not authorize replay.
The Row2 gate-status ledger now freezes the combined state as
`ROW2_ENDPOINT_REPLAY_BLOCKED_PROMOTION_NOT_READY`: the source-native shape
context has passed review and both source-side caveats are reduced, but Row2
remains non-promotion-ready and endpoint replay remains forbidden.
The follow-up Row2 promotion-review package is therefore only a handoff asking
whether a separate future replay-authorization package may be prepared. It is
not replay authorization, not endpoint validation, and not a route-success
claim.
The completed promotion-review response accepts only that narrow handoff:
`row2_promotion_review_accepts_preparing_separate_replay_authorization_not_direct_replay`.
The Row2 gate-status ledger therefore moves to
`ROW2_SEPARATE_REPLAY_AUTH_REVIEW_ALLOWED_NOT_REPLAY`. This still keeps
`endpoint_replay_allowed=false`; it only permits preparing the next reviewer
package.
The Row2 replay-authorization reviewer package is now built as a permission-only
handoff. It asks whether one frozen Row2 replay may later be run without
endpoint-validation, physical-validation, or route-success claims. It contains
no endpoint residuals, scores, or fit statistics:

```text
docs/paper10_desi_shape_row2_replay_authorization_review_v1.md
data/source_manifest/paper10_desi_shape_row2_replay_authorization_review_policy_v1.csv
data/derived/paper10_desi_shape_row2_replay_authorization_review_response_template_v1.csv
data/derived/paper10_desi_shape_row2_replay_authorization_review_package_v1.zip
data/derived/paper10_desi_shape_row2_replay_authorization_review_package_v1.zip.sha256
data/derived/paper10_desi_shape_row2_replay_authorization_review_package_v1_manifest.csv
data/derived/paper10_desi_shape_row2_replay_authorization_review_package_v1_summary.csv
scripts/build_paper10_desi_shape_row2_replay_authorization_review_package_v1.py
scripts/validate_paper10_desi_shape_row2_replay_authorization_review_package_v1.py
```

The completed replay-authorization review accepts the narrow permission-only
scope:
`GO_DESI_SHAPE_ROW2_REPLAY_PERMISSION_ONLY`. The ledger now records
`ROW2_PERMISSION_ONLY_REPLAY_AUTHORIZED_NOT_VALIDATION`. This turns on
`endpoint_replay_allowed=true` only for one frozen Row2 diagnostic replay; it
does not turn on endpoint validation, physical validation, route promotion, or
route-success claims. The imported response artifacts are:

```text
data/derived/paper10_desi_shape_row2_replay_authorization_review_response_v1.csv
data/derived/paper10_desi_shape_row2_replay_authorization_review_response_v1_summary.csv
data/derived/paper10_desi_shape_row2_replay_authorization_review_completed_summary_v1.csv
data/derived/paper10_desi_shape_row2_replay_authorization_review_validation_log_v1.txt
docs/paper10_desi_shape_row2_replay_authorization_review_notes_v1.md
scripts/import_paper10_desi_shape_row2_replay_authorization_review_response_v1.py
scripts/validate_paper10_desi_shape_row2_replay_authorization_review_response_v1.py
```

The authorized Row2-only diagnostic replay has now been run under the same
permission-only boundary. It isolates `shape_row=2` (`z=0.934--1.321`) rather
than replaying the full DESI shape route. The result is preserved as a weak
local diagnostic:
`row2_permission_replay_candidate_not_control_resistant_not_validation`.
The frozen candidate score is `0.415519707291`, while the strongest local
control is `control_redshift_order_shuffle_ROW2` with score `1.62654904473`.
Thus Row2 alone does not carry the full route signal. This is not a validation
or falsification claim; it narrows the interpretation of the earlier route-wide
shape replay by showing that the evidence is not concentrated in Row2 alone.
Combined with the route-wide ablation ledger, the current interpretation is a
multi-row, narrow-margin pattern: Row2 by itself is not control-resistant, but
the route-wide candidate retains about `75%` of its score when Row2 is removed.

The shape-core support synthesis gate now freezes this in one non-scoring
ledger:
`DESI_SHAPE_CORE_SUPPORT_SYNTHESIS_BUILT_SOURCE_STRENGTHENED_NOT_VALIDATION`.
It combines the route-wide stress, row-sensitivity audit, source-support scan,
Row2 source-side reviews, and isolated Row2 permission replay. The reading is
source-side strengthening of a multi-row, narrow-margin route signal: rows `1;2`
are the core, Row1 is the most required row with confirmatory independent
source support externally accepted, Row2 is caveat-reduced but not
promotion-ready, and the Row2-only replay is retained as a negative local
control. The gate does not authorize new replay and does not claim endpoint or
physical validation.

The current reproducibility rerun preserves the same boundary. Re-running the
frozen full DESI shape-route permission replay gives candidate score
`5.52425578108`, strongest control score `5.50939872844`, and narrow margin
`0.01485705264`. The full route replay is therefore positive only in the
permission-only sense. The synthesis gate itself keeps
`endpoint_replay_allowed_by_this_gate=false`; the next allowed scientific step
is a route-level source-synthesis review before any stronger validation-oriented
claim.

That next reviewer handoff is now prepared and validated as:

```text
docs/paper10_desi_shape_route_source_synthesis_review_v1.md
data/source_manifest/paper10_desi_shape_route_source_synthesis_review_policy_v1.csv
data/derived/paper10_desi_shape_route_source_synthesis_review_response_template_v1.csv
data/derived/paper10_desi_shape_route_source_synthesis_review_package_v1.zip
data/derived/paper10_desi_shape_route_source_synthesis_review_package_v1.zip.sha256
data/derived/paper10_desi_shape_route_source_synthesis_review_package_v1_manifest.csv
data/derived/paper10_desi_shape_route_source_synthesis_review_package_v1_summary.csv
scripts/build_paper10_desi_shape_route_source_synthesis_review_package_v1.py
scripts/validate_paper10_desi_shape_route_source_synthesis_review_package_v1.py
```

The package checksum is
`a7c71dc3d5e9d5adeb3ce3313177dba0f757d80465b3e3834ff4c48ddd4f56f9`.
It asks only whether the Row1 and Row2 source-side support can be synthesized
as future-gate preparation. It keeps `endpoint_replay_allowed=false`,
`endpoint_validation_claimed=false`, `physical_validation_claimed=false`, and
`shape_route_promotion_allowed=false`.

The completed source-synthesis review response is now imported as:

```text
data/derived/paper10_desi_shape_route_source_synthesis_review_response_v1.csv
data/derived/paper10_desi_shape_route_source_synthesis_review_response_v1_summary.csv
data/derived/paper10_desi_shape_route_source_synthesis_review_completed_summary_v1.csv
data/derived/paper10_desi_shape_route_source_synthesis_review_validation_log_v1.txt
docs/paper10_desi_shape_route_source_synthesis_review_notes_v1.md
scripts/import_paper10_desi_shape_route_source_synthesis_review_response_v1.py
scripts/validate_paper10_desi_shape_route_source_synthesis_review_response_v1.py
```

Decision:
`ACCEPT_AS_SOURCE_SYNTHESIS_SUPPORT_FOR_FUTURE_GATE_PREPARATION_NOT_REPLAY_NOT_VALIDATION`.
The response accepts all four questions and sets
`future_gate_preparation_allowed=true`, while keeping
`shape_route_promotion_allowed=false`, `endpoint_replay_allowed=false`,
`endpoint_validation_claimed=false`, `physical_validation_claimed=false`, and
`forbidden_inputs_used=false`.

The next staged handoff is now prepared as a post-synthesis gate-authorization
package:

```text
docs/paper10_desi_shape_post_synthesis_gate_authorization_review_v1.md
data/source_manifest/paper10_desi_shape_post_synthesis_gate_authorization_review_policy_v1.csv
data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_template_v1.csv
data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1.zip
data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1.zip.sha256
data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1_manifest.csv
data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1_summary.csv
scripts/build_paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1.py
scripts/validate_paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1.py
```

Checksum:
`4a125b1cc20e54d93de131e68c6798ae6ec2de74030abf5855d590ad190aecfd`.
This package only asks whether a later replay-authorization package may be
prepared. It keeps `prepare_later_authorization_package_allowed=false`,
`endpoint_replay_allowed=false`, `endpoint_validation_claimed=false`, and
`physical_validation_claimed=false` until a completed reviewer response is
validated.

The completed post-synthesis gate authorization response is imported as:

```text
data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1.csv
data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1_summary.csv
data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_completed_summary_v1.csv
data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_validation_log_v1.txt
docs/paper10_desi_shape_post_synthesis_gate_authorization_review_notes_v1.md
scripts/import_paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1.py
scripts/validate_paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1.py
```

Decision:
`ACCEPT_PREPARE_SEPARATE_VALIDATION_ORIENTED_GATE_PACKAGE_NOT_REPLAY_NOT_VALIDATION`.
It sets `prepare_later_authorization_package_allowed=true`, while keeping
`endpoint_replay_allowed=false`, `endpoint_validation_claimed=false`, and
`physical_validation_claimed=false`.

The separate validation-oriented gate reviewer package is now prepared as:

```text
docs/paper10_desi_shape_validation_oriented_gate_review_v1.md
data/source_manifest/paper10_desi_shape_validation_oriented_gate_review_policy_v1.csv
data/derived/paper10_desi_shape_validation_oriented_gate_review_response_template_v1.csv
data/derived/paper10_desi_shape_validation_oriented_gate_review_package_v1.zip
data/derived/paper10_desi_shape_validation_oriented_gate_review_package_v1.zip.sha256
data/derived/paper10_desi_shape_validation_oriented_gate_review_package_v1_manifest.csv
data/derived/paper10_desi_shape_validation_oriented_gate_review_package_v1_summary.csv
scripts/build_paper10_desi_shape_validation_oriented_gate_review_package_v1.py
scripts/validate_paper10_desi_shape_validation_oriented_gate_review_package_v1.py
```

Checksum:
`26fddf67c46cd82585ecc185abee13e0c309ba8c9c3c6b657b4d8d4bcbf8ec52`.
It is still blank and uncompleted. It asks whether a future completed response
may authorize one frozen permission-only replay diagnostic; it does not itself
authorize replay or validation.

The completed validation-oriented gate response is now imported as:

```text
data/derived/paper10_desi_shape_validation_oriented_gate_review_response_v1.csv
data/derived/paper10_desi_shape_validation_oriented_gate_review_response_v1_summary.csv
data/derived/paper10_desi_shape_validation_oriented_gate_review_completed_summary_v1.csv
data/derived/paper10_desi_shape_validation_oriented_gate_review_validation_log_v1.txt
docs/paper10_desi_shape_validation_oriented_gate_review_notes_v1.md
scripts/import_paper10_desi_shape_validation_oriented_gate_review_response_v1.py
scripts/validate_paper10_desi_shape_validation_oriented_gate_review_response_v1.py
```

Decision:
`GO_DESI_SHAPE_VALIDATION_ORIENTED_PERMISSION_REPLAY_ONLY`.
The response accepts preparation for a future permission-only diagnostic replay,
but it does not itself authorize replay. It keeps
`endpoint_replay_allowed=false`, `endpoint_validation_claimed=false`,
`physical_validation_claimed=false`, and `forbidden_inputs_used=false`, while
retaining the narrow-margin, row-sensitive, and Row2-negative caveats. The next
required handoff is therefore a separate completed permission-only replay
authorization response before any run.

That final permission-only replay authorization package is now prepared as:

```text
docs/paper10_desi_shape_validation_permission_replay_authorization_review_v1.md
data/source_manifest/paper10_desi_shape_validation_permission_replay_authorization_review_policy_v1.csv
data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_template_v1.csv
data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.zip
data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.zip.sha256
data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1_manifest.csv
data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1_summary.csv
scripts/build_paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.py
scripts/validate_paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.py
```

Checksum:
`03dd33a4968f710adf0490fe9d8e9e1e2c4298455202aab4af795905dbb3579d`.
It asks only whether one future frozen DESI shape-route permission-only
diagnostic replay may be authorized. It remains blank and keeps
`endpoint_replay_allowed=false`, `endpoint_validation_claimed=false`, and
`physical_validation_claimed=false` until a completed reviewer response is
validated.

The completed validation-permission authorization response is now imported as:

```text
data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_v1.csv
data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_v1_summary.csv
data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_completed_summary_v1.csv
data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_validation_log_v1.txt
docs/paper10_desi_shape_validation_permission_replay_authorization_review_notes_v1.md
scripts/import_paper10_desi_shape_validation_permission_replay_authorization_review_response_v1.py
scripts/validate_paper10_desi_shape_validation_permission_replay_authorization_review_response_v1.py
```

Decision:
`GO_DESI_SHAPE_VALIDATION_PERMISSION_REPLAY_ONLY`.
It authorizes exactly one frozen permission-only diagnostic replay while keeping
`endpoint_validation_claimed=false`, `physical_validation_claimed=false`, and
all retained caveats active.

That replay has now been run as a separate artifact:

```text
data/derived/paper10_desi_shape_validation_permission_authorized_replay_v1_grid.csv
data/derived/paper10_desi_shape_validation_permission_authorized_replay_v1_summary.csv
scripts/run_paper10_desi_shape_validation_permission_authorized_replay_v1.py
scripts/validate_paper10_desi_shape_validation_permission_authorized_replay_v1.py
```

Result:
`candidate_shape_quadratic_score=5.52425578108`,
`best_control_branch=control_leave_shape_row_max`,
`best_control_shape_quadratic_score=5.50939872844`,
`delta_candidate_minus_best_control_score=0.01485705264`.
The candidate remains ahead of all frozen controls, but the margin is narrow and
row-sensitive. Verdict:
`desi_shape_validation_permission_replay_candidate_exceeds_all_controls_not_validation`.

```text
data/source_manifest/paper10_desi_shape_row2_authorized_replay_run_v1.csv
data/derived/paper10_desi_shape_row2_authorized_replay_v1_grid.csv
data/derived/paper10_desi_shape_row2_authorized_replay_v1_summary.csv
docs/paper10_desi_shape_row2_authorized_replay_v1.md
scripts/run_paper10_desi_shape_row2_authorized_replay_v1.py
scripts/validate_paper10_desi_shape_row2_authorized_replay_v1.py
docs/paper10_desi_shape_row1_confirmatory_source_attachment_v1.md
data/source_manifest/paper10_desi_shape_row1_confirmatory_source_attachment_policy_v1.csv
data/derived/paper10_desi_shape_row1_confirmatory_source_attachment_v1.csv
data/derived/paper10_desi_shape_row1_confirmatory_source_attachment_v1_summary.csv
scripts/build_paper10_desi_shape_row1_confirmatory_source_attachment_v1.py
scripts/validate_paper10_desi_shape_row1_confirmatory_source_attachment_v1.py
docs/paper10_desi_shape_row1_confirmatory_source_review_v1.md
data/source_manifest/paper10_desi_shape_row1_confirmatory_source_review_policy_v1.csv
data/derived/paper10_desi_shape_row1_confirmatory_source_review_response_template_v1.csv
data/derived/paper10_desi_shape_row1_confirmatory_source_review_package_v1.zip
data/derived/paper10_desi_shape_row1_confirmatory_source_review_package_v1.zip.sha256
data/derived/paper10_desi_shape_row1_confirmatory_source_review_package_v1_manifest.csv
data/derived/paper10_desi_shape_row1_confirmatory_source_review_package_v1_summary.csv
scripts/build_paper10_desi_shape_row1_confirmatory_source_review_package_v1.py
scripts/validate_paper10_desi_shape_row1_confirmatory_source_review_package_v1.py
docs/paper10_desi_shape_core_support_synthesis_gate_v1.md
data/source_manifest/paper10_desi_shape_core_support_synthesis_gate_policy_v1.csv
data/derived/paper10_desi_shape_core_support_synthesis_gate_v1.csv
data/derived/paper10_desi_shape_core_support_synthesis_gate_v1_summary.csv
scripts/build_paper10_desi_shape_core_support_synthesis_gate_v1.py
scripts/validate_paper10_desi_shape_core_support_synthesis_gate_v1.py
```

The final source-side DESI clock-support action in this chain freezes the
missing acquisition targets before any source fetch:

```text
docs/paper10_desi_clock_support_acquisition_manifest_v1.md
data/source_manifest/paper10_desi_clock_support_acquisition_manifest_policy_v1.csv
data/derived/paper10_desi_clock_support_acquisition_manifest_v1.csv
data/derived/paper10_desi_clock_support_acquisition_manifest_v1_summary.csv
scripts/build_paper10_desi_clock_support_acquisition_manifest_v1.py
scripts/validate_paper10_desi_clock_support_acquisition_manifest_v1.py
```

It freezes exactly two targets: radial row `4` at `z_eff=1.484`, where relaxed
clock support exists but only from one independent reference family, and the
excluded high-redshift row `5` at `z_eff=2.33`, where support must cover or
bracket the row without extrapolation. This manifest is not a source fetch, not
a replay authorization, and not validation.

A first source-side candidate scan for these two targets is recorded in:

```text
docs/paper10_desi_clock_support_source_candidate_scan_v1.md
data/source_manifest/paper10_desi_clock_support_source_candidate_scan_policy_v1.csv
data/derived/paper10_desi_clock_support_source_candidate_scan_v1.csv
data/derived/paper10_desi_clock_support_source_candidate_scan_v1_summary.csv
scripts/build_paper10_desi_clock_support_source_candidate_scan_v1.py
scripts/validate_paper10_desi_clock_support_source_candidate_scan_v1.py
```

It identifies useful context sources but no gate-closing clock support. The
eBOSS DR16 QSO BAO/RSD route is near row 4 at `z_eff=1.48`, but it is a
clustering route rather than an independent clock measurement. The VANDELS
`z=1.26` and LEGA-C `z=0.8` CC measurements are source-relevant but outside the
frozen row-4 `z=1.484` window; the eBOSS/SDSS Ly-alpha BAO route covers
`z=2.33`, but is a BAO/r_d cross-probe route rather than an independent clock
measurement. The scan verdict is
`desi_clock_support_candidate_scan_found_cross_probe_context_but_no_gate_closing_clock_support`.

The resulting blocker verdict is recorded in:

```text
docs/paper10_desi_clock_support_blocker_verdict_v1.md
data/source_manifest/paper10_desi_clock_support_blocker_verdict_policy_v1.csv
data/derived/paper10_desi_clock_support_blocker_verdict_v1.csv
data/derived/paper10_desi_clock_support_blocker_verdict_v1_summary.csv
scripts/build_paper10_desi_clock_support_blocker_verdict_v1.py
scripts/validate_paper10_desi_clock_support_blocker_verdict_v1.py
```

It closes the current search loop as
`DESI_CLOCK_SUPPORT_ROUTE_BLOCKED_AFTER_SOURCE_SCAN_NOT_REPLAY_NOT_VALIDATION`.
The DESI time-readout route can only be reopened if an independent row-4 clock
reference near `z=1.484` or an independent high-z clock/source-native
time-readout route for `z=2.33` is frozen before replay.

A completed external source-side review is recorded in:

```text
docs/paper10_desi_clock_support_blocker_external_review_notes_v1.md
data/derived/paper10_desi_clock_support_blocker_external_review_response_v1.csv
data/derived/paper10_desi_clock_support_blocker_external_review_completed_summary_v1.csv
data/derived/paper10_desi_clock_support_blocker_external_review_response_v1_summary.csv
data/derived/paper10_desi_clock_support_blocker_external_review_validation_log_v1.txt
scripts/import_paper10_desi_clock_support_blocker_external_review_response_v1.py
scripts/validate_paper10_desi_clock_support_blocker_external_review_response_v1.py
```

The completed review partially reopens source acquisition for row 4 only:
independent cosmic-chronometer entries bracketing `z=1.484` at `z=1.43` and
`z=1.53` were reported. Row 5 at `z=2.33` remains blocked, and BAO/RSD plus
Ly-alpha BAO remain cross-probe/context controls unless independent
clock/time-readout evidence is attached. The response explicitly keeps
`endpoint_replay_allowed=false` and makes no validation claim.

The row-4-only reopen manifest is recorded in:

```text
docs/paper10_desi_row4_clock_reopen_manifest_v1.md
data/source_manifest/paper10_desi_row4_clock_reopen_manifest_policy_v1.csv
data/derived/paper10_desi_row4_clock_reopen_manifest_v1.csv
data/derived/paper10_desi_row4_clock_reopen_manifest_v1_summary.csv
scripts/build_paper10_desi_row4_clock_reopen_manifest_v1.py
scripts/validate_paper10_desi_row4_clock_reopen_manifest_v1.py
```

It keeps `row4_can_enter_replay=false` until the source-native CC values,
uncertainties, reference provenance, and covariance status for `z=1.43` and
`z=1.53` are cached and frozen.

That source-native freeze is recorded in:

```text
docs/paper10_desi_row4_cc_bracket_source_freeze_v1.md
data/source_manifest/paper10_desi_row4_cc_bracket_source_freeze_policy_v1.csv
data/derived/paper10_desi_row4_cc_bracket_source_freeze_v1.csv
data/derived/paper10_desi_row4_cc_bracket_source_freeze_v1_summary.csv
scripts/build_paper10_desi_row4_cc_bracket_source_freeze_v1.py
scripts/validate_paper10_desi_row4_cc_bracket_source_freeze_v1.py
```

It freezes `H(z=1.43)=177+/-18` and `H(z=1.53)=140+/-14` km/s/Mpc from the
compiled cosmic-chronometer table. Both entries are attributed to the
Simon et al. (2005) reference family. Therefore this improves the explicit row-4
source record, but it does **not** satisfy the independent-reference-family
redundancy blocker. Row 4 remains `row4_can_enter_replay=false`.

The strict non-Simon row-4 follow-up search is recorded in:

```text
docs/paper10_desi_row4_non_simon_clock_search_v1.md
data/source_manifest/paper10_desi_row4_non_simon_clock_search_policy_v1.csv
data/derived/paper10_desi_row4_non_simon_clock_search_v1.csv
data/derived/paper10_desi_row4_non_simon_clock_search_v1_summary.csv
scripts/build_paper10_desi_row4_non_simon_clock_search_v1.py
scripts/validate_paper10_desi_row4_non_simon_clock_search_v1.py
```

It checks the frozen row-4 release condition under the strict
`|Delta z| <= 0.10` source window. The nearest non-Simon cosmic-chronometer
candidate currently attached to the source chain is Moresco (2015) at
`z=1.363`, with `H(z)=160+/-33.6` km/s/Mpc. This is independent of the Simon
reference family, but `|1.363-1.484|=0.121`, just outside the frozen row-4
window. The verdict is therefore
`row4_non_simon_strict_window_search_negative_blocker_remains`: useful
near-miss source context, no endpoint replay, no validation claim.

The resulting row-4 source-window external review handoff is:

```text
docs/paper10_desi_row4_window_review_v1.md
data/source_manifest/paper10_desi_row4_window_review_policy_v1.csv
data/derived/paper10_desi_row4_window_review_response_template_v1.csv
data/derived/paper10_desi_row4_window_review_package_v1.zip
data/derived/paper10_desi_row4_window_review_package_v1.zip.sha256
data/derived/paper10_desi_row4_window_review_package_v1_manifest.csv
data/derived/paper10_desi_row4_window_review_package_v1_summary.csv
scripts/build_paper10_desi_row4_window_review_package_v1.py
scripts/validate_paper10_desi_row4_window_review_package_v1.py
scripts/validate_paper10_desi_row4_window_review_response_v1.py
scripts/import_paper10_desi_row4_window_review_response_v1.py
```

This package asks only whether the strict row-4 window should remain fixed or
whether the Moresco (2015) `z=1.363` near miss may be accepted as caveated
source-side context. It contains no endpoint residuals, scores, or fit
statistics, and does not authorize replay.

If a completed reviewer ZIP is returned, import it with:

```bash
python scripts/import_paper10_desi_row4_window_review_response_v1.py \
  /path/to/completed_row4_window_review.zip
```

The importer first runs
`scripts/validate_paper10_desi_row4_window_review_response_v1.py`. Even a
positive response can only set `source_reopen_caveated=true`; it keeps
`row4_can_enter_replay=false` and requires a separate replay-authorization
handoff before any endpoint scoring.

The row-4 source-window decision gate is recorded in:

```text
docs/paper10_desi_row4_window_decision_gate_v1.md
data/source_manifest/paper10_desi_row4_window_decision_gate_policy_v1.csv
data/derived/paper10_desi_row4_window_decision_gate_v1.csv
data/derived/paper10_desi_row4_window_decision_gate_v1_summary.csv
scripts/build_paper10_desi_row4_window_decision_gate_v1.py
scripts/validate_paper10_desi_row4_window_decision_gate_v1.py
```

The completed source-blocker review accepts the Moresco (2015) near miss only
as caveated source-side context. The imported row-4 decision gate now reports
`ROW4_SOURCE_REOPEN_CAVEATED_NO_REPLAY`; endpoint replay remains disabled.

The route-level DESI time-readout closure status is recorded in:

```text
docs/paper10_desi_time_route_closure_status_v1.md
data/source_manifest/paper10_desi_time_route_closure_status_policy_v1.csv
data/derived/paper10_desi_time_route_closure_status_v1.csv
data/derived/paper10_desi_time_route_closure_status_v1_summary.csv
scripts/build_paper10_desi_time_route_closure_status_v1.py
scripts/validate_paper10_desi_time_route_closure_status_v1.py
```

It synthesizes the current DESI time-route state from the row-4 and row-5
decision gates as
`DESI_TIME_ROUTE_CLOSED_PENDING_SOURCE_BLOCKERS_NOT_REPLAY`: row 4 is caveated
source-reopened but not replay-ready, row 5 lacks high-z independent clock
support, and the negative-control response gate still blocks replay until
richer clock/readout support exists.

The row-5 high-z source-side review handoff is:

```text
docs/paper10_desi_row5_high_z_review_v1.md
data/source_manifest/paper10_desi_row5_high_z_review_policy_v1.csv
data/derived/paper10_desi_row5_high_z_review_response_template_v1.csv
data/derived/paper10_desi_row5_high_z_review_package_v1.zip
data/derived/paper10_desi_row5_high_z_review_package_v1.zip.sha256
data/derived/paper10_desi_row5_high_z_review_package_v1_manifest.csv
data/derived/paper10_desi_row5_high_z_review_package_v1_summary.csv
scripts/build_paper10_desi_row5_high_z_review_package_v1.py
scripts/validate_paper10_desi_row5_high_z_review_package_v1.py
scripts/validate_paper10_desi_row5_high_z_review_response_v1.py
scripts/import_paper10_desi_row5_high_z_review_response_v1.py
```

This package asks whether a public/citable high-z clock or source-native
time/readout route can support `z=2.33` without extrapolating the frozen
cosmic-chronometer table. It keeps Ly-alpha BAO as cross-probe context unless
an independent clock/time-readout observable is explicitly attached. It contains
no endpoint residuals, scores, or fit statistics, and does not authorize replay.

If a completed reviewer ZIP is returned, import it with:

```bash
python scripts/import_paper10_desi_row5_high_z_review_response_v1.py \
  /path/to/completed_row5_high_z_review.zip
```

The importer first runs
`scripts/validate_paper10_desi_row5_high_z_review_response_v1.py`. Even a
positive response can only set a source-side reopen flag or request a separate
replay-authorization handoff; it keeps `row5_can_enter_replay=false`.

The row-5 high-z decision gate is recorded in:

```text
docs/paper10_desi_row5_high_z_decision_gate_v1.md
data/source_manifest/paper10_desi_row5_high_z_decision_gate_policy_v1.csv
data/derived/paper10_desi_row5_high_z_decision_gate_v1.csv
data/derived/paper10_desi_row5_high_z_decision_gate_v1_summary.csv
scripts/build_paper10_desi_row5_high_z_decision_gate_v1.py
scripts/validate_paper10_desi_row5_high_z_decision_gate_v1.py
```

The completed row-5 review identifies no independent high-z clock source and no
source-native high-z time/readout observable covering `z=2.33`; Ly-alpha BAO
remains cross-probe context only. The imported decision gate now reports
`ROW5_HIGH_Z_BLOCKER_REMAINS_NOT_REPLAY`, so endpoint replay remains disabled.

The focused row-5 high-z route scout is recorded in:

```text
docs/paper10_desi_row5_high_z_source_route_scout_v1.md
data/source_manifest/paper10_desi_row5_high_z_source_route_scout_policy_v1.csv
data/derived/paper10_desi_row5_high_z_source_route_scout_v1.csv
data/derived/paper10_desi_row5_high_z_source_route_scout_v1_summary.csv
scripts/build_paper10_desi_row5_high_z_source_route_scout_v1.py
scripts/validate_paper10_desi_row5_high_z_source_route_scout_v1.py
```

It records four context routes: DESI DR1 cosmic chronometers, the current
cosmic-chronometer review/forecast route, DESI/Ly-alpha BAO at `z=2.33`, and a
future standard-timer style prompt. The verdict is
`row5_high_z_scout_found_context_but_no_gate_closing_source`; all rows remain
context/control only and endpoint replay remains disabled.

The post-review Row5 holdout confirmation gate is recorded in:

```text
docs/paper10_desi_row5_holdout_confirmation_v1.md
data/source_manifest/paper10_desi_row5_holdout_confirmation_policy_v1.csv
data/derived/paper10_desi_row5_holdout_confirmation_v1.csv
data/derived/paper10_desi_row5_holdout_confirmation_v1_summary.csv
scripts/build_paper10_desi_row5_holdout_confirmation_v1.py
scripts/validate_paper10_desi_row5_holdout_confirmation_v1.py
```

It freezes the consequence of the review and scout: row 5 remains holdout, rows
`0;1;2;3;4` remain the only first CC-matched DESI endpoint rows, and this is not
a post-score row selection.

The post-review DESI time-route priority ledger is recorded in:

```text
docs/paper10_desi_post_review_time_route_priority_v1.md
data/source_manifest/paper10_desi_post_review_time_route_priority_policy_v1.csv
data/derived/paper10_desi_post_review_time_route_priority_v1.csv
data/derived/paper10_desi_post_review_time_route_priority_v1_summary.csv
scripts/build_paper10_desi_post_review_time_route_priority_v1.py
scripts/validate_paper10_desi_post_review_time_route_priority_v1.py
```

It freezes the next source-side priority after the Row5 holdout decision:
`TIME_READOUT_SHAPE_OBSERVABLE` is now the primary next gate, while high-z
support becomes a future holdout-reopen route rather than the current replay
target.

For the separate low-z Pantheon \(W_{\rm time}\) uncertainty-basis replay
authorization route, import a completed external reviewer CSV with:

```bash
python scripts/import_paper10_desi_time_readout_shape_independent_review_response_v1.py \
  /path/to/completed_shape_review_response.csv
```

The importer first runs
`scripts/validate_paper10_desi_time_readout_shape_independent_review_response_v1.py`.
The only accepted positive outcome retains the shape as a caveated source-side
candidate; it still keeps endpoint replay, endpoint validation, and physical
validation false.

When a completed external reviewer CSV is returned, import it with:

```bash
python scripts/import_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_v1.py \
  /path/to/completed_response.csv
```

The importer validates the external CSV before copying it into
`data/derived/`; an incomplete or non-GO response is rejected without modifying
the canonical response artifacts.
A gate-status ledger records this state explicitly: the source-side basis,
review package, completed GO response, and replay template all pass for a
permission-only replay, while endpoint validation remains false.

The multi-channel coupling component is also accounted by a frozen source-side
ledger. It combines the current V2 component statuses and deliberately keeps
all coupling rules endpoint-blocked: the void branch retains its weak-negative
control-dominance result, while path and time values are still unavailable.
This ledger prevents the V2 gate from silently treating coupling as either
solved or missing; it is present, reproducible, and not a replay authorization.

The first lensing route-freeze check is recorded in:

```text
data/source_manifest/kids1000_lensing_route_v1.csv
data/derived/kids1000_lensing_route_v1_head.csv
data/derived/kids1000_lensing_route_v1_summary.csv
docs/kids1000_lensing_route_v1.md
scripts/check_kids1000_lensing_route_v1.py
scripts/validate_kids1000_lensing_route_v1.py
```

This checks the public KiDS-1000 cosmic-shear tarball route by HEAD metadata
only. It does not fetch or redistribute the lensing tarball and contains no
data vector, covariance matrix, posterior chain, lensing residual, or fit
statistic. Lensing scoring remains forbidden until tomographic-bin policy,
statistic choice, covariance block, mask policy, and readout policy are frozen.

The first fetched KiDS lensing source product and COSEBIs route inventory are
recorded in:

```text
data/source_manifest/kids1000_lensing_products_v1.csv
data/source_manifest/kids1000_cosebis_lensing_route_v1.csv
data/raw/weak_lensing/kids1000/KiDS1000_cosmic_shear_data_release.tgz
data/derived/kids1000_lensing_inventory_v1.csv
data/derived/kids1000_lensing_inventory_v1_summary.csv
docs/kids1000_lensing_products_v1.md
docs/kids1000_cosebis_lensing_route_v1.md
scripts/acquire_kids1000_lensing_products_v1.py
scripts/validate_kids1000_lensing_products_v1.py
scripts/build_kids1000_lensing_inventory_v1.py
scripts/validate_kids1000_lensing_inventory_v1.py
```

The inventory finds `28` non-directory tarball members, `3` FITS products, and
exactly one selected COSEBIs FITS product for the future narrow lensing route.
This remains endpoint disabled and contains no lensing score.

The first COSEBIs FITS HDU policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_hdu_policy_v1.csv
data/derived/kids1000_cosebis_hdu_inventory_v1.csv
data/derived/kids1000_cosebis_hdu_inventory_v1_summary.csv
docs/kids1000_cosebis_hdu_policy_v1.md
scripts/build_kids1000_cosebis_hdu_inventory_v1.py
scripts/validate_kids1000_cosebis_hdu_inventory_v1.py
```

It freezes `COVMAT` as a `300x300` covariance matrix, `En` as a 300-row
COSEBIs data-vector table, and `NZ_SOURCE` as a 119-row redshift-distribution
table. The covariance is positive definite. This is still not a lensing
likelihood and contains no model residuals or fit statistics.

The COSEBIs tomographic/mode policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_tomographic_mode_policy_v1.csv
data/derived/kids1000_cosebis_tomographic_mode_inventory_v1.csv
data/derived/kids1000_cosebis_tomographic_mode_inventory_v1_summary.csv
docs/kids1000_cosebis_tomographic_mode_policy_v1.md
scripts/build_kids1000_cosebis_tomographic_mode_inventory_v1.py
scripts/validate_kids1000_cosebis_tomographic_mode_inventory_v1.py
```

It freezes the selected `En` data-vector structure as `5` source bins, `15`
upper-triangular tomographic pairs, and `20` COSEBIs modes per pair, for `300`
rows. This is a source-side structure freeze only: it does not set a mode cut,
does not invert the covariance, and does not compute lensing predictions,
residuals, likelihood values, or Tau Core amplitudes.

The COSEBIs covariance-readiness policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_covariance_readiness_policy_v1.csv
data/derived/kids1000_cosebis_covariance_readiness_v1.csv
data/derived/kids1000_cosebis_covariance_readiness_v1_summary.csv
docs/kids1000_cosebis_covariance_readiness_policy_v1.md
scripts/build_kids1000_cosebis_covariance_readiness_v1.py
scripts/validate_kids1000_cosebis_covariance_readiness_v1.py
```

It records only source-side covariance diagnostics for the selected `COVMAT`
block: shape, symmetry error, diagonal positivity, eigenvalue range, condition
number, and Cholesky readiness. It does not save an inverse covariance, select a
data-vector mask, choose a theory vector, or compute lensing scores.

The first COSEBIs mask/mode-cut policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_mask_modecut_policy_v1.csv
data/derived/kids1000_cosebis_mask_modecut_inventory_v1.csv
data/derived/kids1000_cosebis_mask_modecut_inventory_v1_summary.csv
docs/kids1000_cosebis_mask_modecut_policy_v1.md
scripts/build_kids1000_cosebis_mask_modecut_inventory_v1.py
scripts/validate_kids1000_cosebis_mask_modecut_inventory_v1.py
```

It retains all `300` source rows: all `15` tomographic pairs and modes `1..20`.
This deliberately avoids residual-based row or mode removal. It is not an
endpoint and does not define a theory vector, inverse covariance, likelihood, or
Tau Core lensing amplitude.

The first COSEBIs tomographic-pair retention-weight policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_tomographic_weight_policy_v1.csv
data/derived/kids1000_cosebis_tomographic_weight_inventory_v1.csv
data/derived/kids1000_cosebis_tomographic_weight_inventory_v1_summary.csv
docs/kids1000_cosebis_tomographic_weight_policy_v1.md
scripts/build_kids1000_cosebis_tomographic_weight_inventory_v1.py
scripts/validate_kids1000_cosebis_tomographic_weight_inventory_v1.py
```

It assigns unit source-retention weights to all `15` tomographic pairs. These
are not likelihood weights, fitted amplitudes, or covariance weights; they only
state that no pair is upweighted or downweighted using residuals, fit
statistics, posterior chains, or endpoint behavior.

The first COSEBIs covariance-subselection policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_covariance_subselection_policy_v1.csv
data/derived/kids1000_cosebis_covariance_subselection_inventory_v1.csv
data/derived/kids1000_cosebis_covariance_subselection_inventory_v1_summary.csv
docs/kids1000_cosebis_covariance_subselection_policy_v1.md
scripts/build_kids1000_cosebis_covariance_subselection_inventory_v1.py
scripts/validate_kids1000_cosebis_covariance_subselection_inventory_v1.py
```

It retains the full `300x300` covariance block because all `300` data-vector
rows are retained. It records the contiguous 20-row covariance intervals for
each of the `15` tomographic pairs, but it does not save an inverse covariance,
select a likelihood, or compute a lensing score.

The first COSEBIs covariance-inversion readiness policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_covariance_inversion_policy_v1.csv
data/derived/kids1000_cosebis_covariance_inversion_readiness_v1.csv
data/derived/kids1000_cosebis_covariance_inversion_readiness_v1_summary.csv
docs/kids1000_cosebis_covariance_inversion_policy_v1.md
scripts/build_kids1000_cosebis_covariance_inversion_readiness_v1.py
scripts/validate_kids1000_cosebis_covariance_inversion_readiness_v1.py
```

It freezes the future numerical solve policy as Cholesky solve on the full
`300x300` covariance, but explicitly does not execute the solve and does not
store an inverse covariance. A frozen theory vector and scoring protocol are
still required before any lensing likelihood can be evaluated.

The first COSEBIs theory-vector readiness policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_theory_vector_policy_v1.csv
data/derived/kids1000_cosebis_theory_vector_readiness_v1.csv
data/derived/kids1000_cosebis_theory_vector_readiness_v1_summary.csv
docs/kids1000_cosebis_theory_vector_policy_v1.md
scripts/build_kids1000_cosebis_theory_vector_readiness_v1.py
scripts/validate_kids1000_cosebis_theory_vector_readiness_v1.py
data/source_manifest/kids1000_cosebis_theory_vector_template_policy_v1.csv
data/derived/kids1000_cosebis_theory_vector_template_v1.csv
data/derived/kids1000_cosebis_theory_vector_template_v1_summary.csv
docs/kids1000_cosebis_theory_vector_template_v1.md
scripts/build_kids1000_cosebis_theory_vector_template_v1.py
scripts/validate_kids1000_cosebis_theory_vector_template_v1.py
data/source_manifest/kids1000_cosebis_source_frozen_theory_vector_policy_v1.csv
data/derived/kids1000_cosebis_source_frozen_theory_vector_v1.csv
data/derived/kids1000_cosebis_source_frozen_theory_vector_v1_summary.csv
docs/kids1000_cosebis_source_frozen_theory_vector_v1.md
scripts/build_kids1000_cosebis_source_frozen_theory_vector_v1.py
scripts/validate_kids1000_cosebis_source_frozen_theory_vector_v1.py
data/source_manifest/kids1000_cosebis_mapping_template_join_contract_policy_v1.csv
data/derived/kids1000_cosebis_mapping_template_join_contract_v1.csv
data/derived/kids1000_cosebis_mapping_template_join_contract_v1_summary.csv
docs/kids1000_cosebis_mapping_template_join_contract_v1.md
scripts/build_kids1000_cosebis_mapping_template_join_contract_v1.py
scripts/validate_kids1000_cosebis_mapping_template_join_contract_v1.py
```

It declares the `300`-row COSEBIs theory-vector gate for the active
`W_WEB_ANISOTROPY` and `W_PATH_PROJECTION` lensing route. The parent policy
remains endpoint-disabled and declarative. A separate source-frozen,
unit-amplitude theory-vector shell is now computed from the frozen mapping basis
and a predeclared unit-mean `mode^{-1/2}` mode-shape rule. This shell forbids
KiDS data-vector values, posterior chains, residuals, fit-improvement flags,
post-hoc mode cuts, and post-hoc amplitude calibration. It is not endpoint
scoring and not empirical validation.
The accompanying template freezes the 300-row tomographic-pair/mode interface
with empty theory-value and channel-contribution fields. It is a row-index
template only, not a prediction.
The mapping-to-template join contract then freezes the future source-frozen
join key and required mapping columns for that same 300-row interface. It does
not fill any mapping value, theory value, channel contribution, prediction, or
score.

The first COSEBIs web/path mapping readiness policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_web_path_mapping_policy_v1.csv
data/derived/kids1000_cosebis_web_path_mapping_readiness_v1.csv
data/derived/kids1000_cosebis_web_path_mapping_readiness_v1_summary.csv
docs/kids1000_cosebis_web_path_mapping_policy_v1.md
scripts/build_kids1000_cosebis_web_path_mapping_readiness_v1.py
scripts/validate_kids1000_cosebis_web_path_mapping_readiness_v1.py
data/source_manifest/kids1000_cosebis_source_frozen_mapping_vector_policy_v1.csv
data/derived/kids1000_cosebis_source_frozen_mapping_domain_weights_v1.csv
data/derived/kids1000_cosebis_source_frozen_mapping_vector_v1.csv
data/derived/kids1000_cosebis_source_frozen_mapping_vector_v1_summary.csv
docs/kids1000_cosebis_source_frozen_mapping_vector_v1.md
scripts/build_kids1000_cosebis_source_frozen_mapping_vector_v1.py
scripts/validate_kids1000_cosebis_source_frozen_mapping_vector_v1.py
```

It declares the source-side inputs required before a future `W_WEB_ANISOTROPY`
and `W_PATH_PROJECTION` COSEBIs theory vector can be built. The current release
now includes a source-frozen 300-row mapping basis with 15 tomographic-pair
values. This basis has pair/redshift/path variation, but no COSEBIs mode-shape
and no theory value; `W_web` remains a zero null-control channel. It therefore
does not compute a theory vector, prediction, residual, fit statistic, or score,
and forbids KiDS data-vector values, posterior chains, residuals,
fit-improvement flags, and post-hoc sky-direction selection.

The first COSEBIs redshift-kernel inventory is recorded in:

```text
data/source_manifest/kids1000_cosebis_redshift_kernel_policy_v1.csv
data/derived/kids1000_cosebis_redshift_kernel_inventory_v1.csv
data/derived/kids1000_cosebis_redshift_kernel_inventory_v1_summary.csv
docs/kids1000_cosebis_redshift_kernel_policy_v1.md
scripts/build_kids1000_cosebis_redshift_kernel_inventory_v1.py
scripts/validate_kids1000_cosebis_redshift_kernel_inventory_v1.py
```

It reads only the selected `NZ_SOURCE` table and records source-bin redshift
areas, mean redshifts, and support intervals for the five KiDS source bins. This
is a source-side kernel inventory, not a COSEBIs theory vector, lensing
prediction, residual, or likelihood score.

The first COSEBIs path mask/depth gap audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_mask_depth_gap_policy_v1.csv
data/derived/kids1000_cosebis_path_mask_depth_gap_inventory_v1.csv
data/derived/kids1000_cosebis_path_mask_depth_gap_inventory_v1_summary.csv
docs/kids1000_cosebis_path_mask_depth_gap_policy_v1.md
scripts/build_kids1000_cosebis_path_mask_depth_gap_inventory_v1.py
scripts/validate_kids1000_cosebis_path_mask_depth_gap_inventory_v1.py
```

It scans the selected KiDS-1000 cosmic-shear release tarball and records that no
standalone source-frozen footprint, path mask, depth map, random catalogue, or
equivalent path-load product is accepted from that tarball. Filename `mask`
tokens in the statistic FITS products are classified as statistic-product
metadata, not as survey path maps. The future `W_PATH_PROJECTION` route
therefore remains blocked on an external source-frozen path/mask/depth product.

The first official KiDS DR4 path-mask route-script freeze is recorded in:

```text
data/source_manifest/kids1000_dr4_path_mask_route_scripts_v1.csv
data/raw/weak_lensing/kids1000_path_masks/kids_dr4.1_9band_msk_wget.sh
data/raw/weak_lensing/kids1000_path_masks/kids_dr4.0_9band_msk_wget.sh
data/raw/weak_lensing/kids1000_path_masks/kids_dr4.0_msk_wget.sh
data/derived/kids1000_dr4_path_mask_route_scripts_inventory_v1.csv
data/derived/kids1000_dr4_path_mask_route_scripts_inventory_v1_summary.csv
docs/kids1000_dr4_path_mask_route_scripts_v1.md
scripts/acquire_kids1000_dr4_path_mask_route_scripts_v1.py
scripts/validate_kids1000_dr4_path_mask_route_scripts_v1.py
```

This freezes the small official KiDS DR4 wget scripts that point to external
mask FITS products. The preferred DR4.1 9-band route script lists `196` mask
products. Those mask FITS files are not downloaded in this package, and no
path-mapping vector or COSEBIs theory vector is computed.

The preferred-route tile inventory is recorded in:

```text
data/source_manifest/kids1000_dr4_path_mask_route_tile_inventory_policy_v1.csv
data/derived/kids1000_dr4_path_mask_route_tile_inventory_v1.csv
data/derived/kids1000_dr4_path_mask_route_tile_inventory_v1_summary.csv
docs/kids1000_dr4_path_mask_route_tile_inventory_policy_v1.md
scripts/build_kids1000_dr4_path_mask_route_tile_inventory_v1.py
scripts/validate_kids1000_dr4_path_mask_route_tile_inventory_v1.py
```

It parses all `196` preferred DR4.1 9-band mask-product URLs into
filename-derived tile coordinates. This gives a source-frozen route geometry
index, but still does not download the 196 mask products, compute a footprint
polygon, build a path map, or connect anything to COSEBIs rows.

The first preferred-route HEAD sample is recorded in:

```text
data/source_manifest/kids1000_dr4_path_mask_head_sample_policy_v1.csv
data/derived/kids1000_dr4_path_mask_head_sample_v1.csv
data/derived/kids1000_dr4_path_mask_head_sample_v1_summary.csv
docs/kids1000_dr4_path_mask_head_sample_policy_v1.md
scripts/check_kids1000_dr4_path_mask_head_sample_v1.py
scripts/validate_kids1000_dr4_path_mask_head_sample_v1.py
```

It checks only the first, middle, and last mask-product URLs from the preferred
DR4.1 9-band route. All three return HTTP `200` with FITS content and positive
content length. This is an availability sanity check only: the mask FITS files
are not downloaded and no path mapping is computed.

The first source-frozen KiDS DR4 path-mask subset inventory is recorded in:

```text
data/source_manifest/kids1000_dr4_path_mask_subset_policy_v1.csv
data/raw/weak_lensing/kids1000_path_masks/mask_subset_v1/
data/derived/kids1000_dr4_path_mask_subset_inventory_v1.csv
data/derived/kids1000_dr4_path_mask_subset_inventory_v1_summary.csv
docs/kids1000_dr4_path_mask_subset_policy_v1.md
scripts/acquire_kids1000_dr4_path_mask_subset_v1.py
scripts/validate_kids1000_dr4_path_mask_subset_v1.py
```

It downloads and hash-freezes the first/middle/last DR4.1 9-band mask FITS
products from the predeclared HEAD sample, then records FITS image shape and
basic finite/nonzero pixel summaries. The three masks total `15,091,583` bytes
and `1,323,000,000` image pixels. This still does not compute a path map, does
not connect masks to COSEBIs rows, and does not score a lensing model.

The first source-only mask observable shell is recorded in:

```text
data/source_manifest/kids1000_dr4_path_mask_observable_shell_policy_v1.csv
data/derived/kids1000_dr4_path_mask_observable_shell_v1.csv
data/derived/kids1000_dr4_path_mask_observable_shell_v1_summary.csv
docs/kids1000_dr4_path_mask_observable_shell_policy_v1.md
scripts/build_kids1000_dr4_path_mask_observable_shell_v1.py
scripts/validate_kids1000_dr4_path_mask_observable_shell_v1.py
```

It parses only filename tile coordinates and the subset inventory's nonzero
mask-pixel fractions, then builds a centered zero-fraction shell across the
three frozen masks. This is a pre-mapping source observable only: mask-value
semantics are not interpreted as a physical lensing path weight, no COSEBIs-row
mapping is constructed, and no theory vector or endpoint score is computed.

The first COSEBIs path-mapping design skeleton is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_mapping_design_skeleton_policy_v1.csv
data/derived/kids1000_cosebis_path_mapping_design_skeleton_v1.csv
data/derived/kids1000_cosebis_path_mapping_design_skeleton_v1_summary.csv
docs/kids1000_cosebis_path_mapping_design_skeleton_policy_v1.md
scripts/build_kids1000_cosebis_path_mapping_design_skeleton_v1.py
scripts/validate_kids1000_cosebis_path_mapping_design_skeleton_v1.py
```

It builds the 300-row future mapping layout from COSEBIs row structure,
tomographic-pair redshift summaries, and the preferred 196-tile route span. It
does not compute tile/path weights, a path mapping vector, a theory vector,
predictions, residuals, or endpoint scores.

The full target-row by route-tile domain skeleton is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_mapping_domain_skeleton_policy_v1.csv
data/derived/kids1000_cosebis_path_mapping_domain_skeleton_v1.csv
data/derived/kids1000_cosebis_path_mapping_domain_skeleton_v1_summary.csv
docs/kids1000_cosebis_path_mapping_domain_skeleton_policy_v1.md
scripts/build_kids1000_cosebis_path_mapping_domain_skeleton_v1.py
scripts/validate_kids1000_cosebis_path_mapping_domain_skeleton_v1.py
```

It forms the complete `300 x 196 = 58,800` source-side mapping domain from
COSEBIs target rows and preferred-route tiles. It still does not compute
footprint overlap, tile weights, path weights, web-environment labels, a mapping
vector, a theory vector, predictions, residuals, or scores.

The path-weight construction-rule ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_weight_construction_rule_v1.csv
data/derived/kids1000_cosebis_path_weight_construction_rule_v1.csv
data/derived/kids1000_cosebis_path_weight_construction_rule_v1_summary.csv
docs/kids1000_cosebis_path_weight_construction_rule_v1.md
scripts/build_kids1000_cosebis_path_weight_construction_rule_v1.py
scripts/validate_kids1000_cosebis_path_weight_construction_rule_v1.py
```

The source-side normalization rule is recorded in:

```text
data/source_manifest/kids1000_cosebis_c_norm_source_side_rule_policy_v1.csv
data/derived/kids1000_cosebis_c_norm_source_side_domain_rule_v1.csv
data/derived/kids1000_cosebis_c_norm_source_side_rule_v1_summary.csv
docs/kids1000_cosebis_c_norm_source_side_rule_v1.md
scripts/build_kids1000_cosebis_c_norm_source_side_rule_v1.py
scripts/validate_kids1000_cosebis_c_norm_source_side_rule_v1.py
```

It declares the future factorization
`N_pair * T_tile * F_overlap * D_path * E_web * C_norm` and records which
factors are source-supported. The source-weight rule is now source-side computable: `F_overlap` has
non-degenerate source support from the full-route pixel-fraction rule,
`D_path` has caveated non-degenerate source support from the full-route
mask-load proxy, `E_web` is source-supported only as a uniform null-web
control, and `C_norm = 2.110707798749` normalizes the frozen raw source-factor
product to unit mean over the 58,800-row domain. This does not make a positive
web/environment claim. No mapping vector, theory vector, residual, or endpoint
score is produced.

The source-factor acquisition plan is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_factor_acquisition_plan_v1.csv
data/derived/kids1000_cosebis_path_factor_acquisition_plan_v1.csv
data/derived/kids1000_cosebis_path_factor_acquisition_plan_v1_summary.csv
docs/kids1000_cosebis_path_factor_acquisition_plan_v1.md
scripts/build_kids1000_cosebis_path_factor_acquisition_plan_v1.py
scripts/validate_kids1000_cosebis_path_factor_acquisition_plan_v1.py
```

It converts the source-factor status into seven source-side acquisition
requirements. At the current stage none of the seven requirements blocks the
source-weight algebra: source-side normalization is resolved after the nonzero
source factors and the null-web control exist. It fetches no products and
computes no endpoint weights. The next blocker is the mapping vector.

The source-product route candidate manifest is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_source_product_route_policy_v1.csv
data/derived/kids1000_cosebis_path_source_product_route_manifest_v1.csv
data/derived/kids1000_cosebis_path_source_product_route_manifest_v1_summary.csv
docs/kids1000_cosebis_path_source_product_route_policy_v1.md
scripts/build_kids1000_cosebis_path_source_product_route_manifest_v1.py
scripts/validate_kids1000_cosebis_path_source_product_route_manifest_v1.py
```

It declares ten source-product routes for the next source-gathering step:
six already-supported locks/routes, no remaining blocker-resolving candidate
before the mapping vector, two alternative-not-needed routes, one unfetched
external web route kept as a future positive-web option, and one deferred null-control route. The supported
`E_web` route is a null-web control only; the external web/environment catalogue
route remains unfetched and does not support a positive web claim. The manifest
still fetches no external products, creates no path mapping, and computes no
score.

The blocker-resolution order policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_blocker_resolution_order_policy_v1.csv
data/derived/kids1000_cosebis_path_blocker_resolution_order_v1.csv
data/derived/kids1000_cosebis_path_blocker_resolution_order_v1_summary.csv
docs/kids1000_cosebis_path_blocker_resolution_order_policy_v1.md
scripts/build_kids1000_cosebis_path_blocker_resolution_order_v1.py
scripts/validate_kids1000_cosebis_path_blocker_resolution_order_v1.py
```

It freezes the future source-side order: `F_overlap` first, then `D_path`,
then `E_web`, then `C_norm`, then a mapping vector, then null controls. It
records that `F_overlap`, a caveated `D_path` mask-load proxy, a uniform
null-web `E_web` control, and source-side `C_norm` are now supported. The first
remaining blocker is the mapping vector. It fetches no products and keeps
mapping and endpoint scoring disabled.

The first-blocker `F_overlap` rule shell is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_rule_shell_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_rule_shell_v1.csv
data/derived/kids1000_cosebis_f_overlap_rule_shell_v1_summary.csv
docs/kids1000_cosebis_f_overlap_rule_shell_policy_v1.md
scripts/build_kids1000_cosebis_f_overlap_rule_shell_v1.py
scripts/validate_kids1000_cosebis_f_overlap_rule_shell_v1.py
```

It declares the accepted future output schema for the row-tile overlap factor
over the full `300 x 196 = 58,800` target-row by route-tile domain. It accepts
only source-frozen official footprint geometry or source-native full-mask
overlap derivations. It computes no overlap values and still forbids mapping
and scoring.

The `F_overlap` source-availability audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_source_availability_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_source_availability_v1.csv
data/derived/kids1000_cosebis_f_overlap_source_availability_v1_summary.csv
docs/kids1000_cosebis_f_overlap_source_availability_policy_v1.md
scripts/build_kids1000_cosebis_f_overlap_source_availability_v1.py
scripts/validate_kids1000_cosebis_f_overlap_source_availability_v1.py
```

It records that the route script and three-mask subset are not sufficient for a
full overlap rule. No official footprint geometry product or full 196-mask
source-native product set is currently accepted, so `F_overlap` remains
unresolved and mapping remains disabled.

The `F_overlap` full-mask acquisition manifest is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_full_mask_acquisition_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1_summary.csv
docs/kids1000_cosebis_f_overlap_full_mask_acquisition_policy_v1.md
scripts/build_kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.py
scripts/validate_kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.py
```

It expands the preferred route into a 196-row acquisition manifest. In the
public reproduce path this manifest remains conservative: the package contains
the three committed sample masks and records the remaining 193 products as
fetch-required. A separate author-local full-route cache inventory, described
below, records a completed source-cache snapshot without making the large raw
FITS cache part of the public package.

The `F_overlap` full-mask batch plan is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_full_mask_batch_plan_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_mask_batch_plan_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_mask_batch_plan_v1_summary.csv
docs/kids1000_cosebis_f_overlap_full_mask_batch_plan_policy_v1.md
scripts/build_kids1000_cosebis_f_overlap_full_mask_batch_plan_v1.py
scripts/validate_kids1000_cosebis_f_overlap_full_mask_batch_plan_v1.py
```

It splits the 193 missing mask products into ten future acquisition batches of
at most 20 files each. Future large FITS products are assigned to an ignored
cache directory; only manifests and derived summaries should be committed.

The first `F_overlap` batch dry run is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_full_mask_batch_dry_run_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1_summary.csv
docs/kids1000_cosebis_f_overlap_full_mask_batch_dry_run_policy_v1.md
scripts/acquire_kids1000_cosebis_f_overlap_full_mask_batch_v1.py
scripts/validate_kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1.py
```

The public reproduction path runs this script only in dry-run mode on batch 0.
It inspects the 20 planned product URLs and cache paths without fetching any
large FITS product, without computing overlap fractions, without constructing a
path-mapping vector, and without enabling endpoint scoring. Manual acquisition
is available only through the explicit `--execute` option; outputs from that
mode are written under ignored `data/local/` execution logs plus the ignored
full-route FITS cache. They remain outside the public reproduce path until
separately reviewed, checksum-frozen, and promoted through a source-freeze
artifact.

The author-local full-route cache inventory is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_full_route_cache_inventory_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_route_cache_inventory_v1_summary.csv
docs/kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.md
scripts/build_kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.py
scripts/validate_kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.py
```

This local snapshot accounts for all 196 expected mask products: 193 products
in the ignored `data/raw/weak_lensing/kids1000_path_masks/full_route_cache_v1/`
cache plus the three committed subset masks. Each product is recorded with a
relative path, byte size, and SHA-256 hash. Public reproduction does not require
the ignored raw cache; it uses the committed inventory snapshot only. The
inventory does not compute overlap fractions, path mapping, a theory vector,
predictions, residuals, or scores. It moves the first `F_overlap` blocker from
"source products missing" to "derive a source-frozen full-mask overlap rule
without endpoint inputs."

The first source-frozen full-route overlap rule candidate is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_header_footprint_rule_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_header_footprint_tile_rule_v1.csv
data/derived/kids1000_cosebis_f_overlap_header_footprint_rule_v1.csv
data/derived/kids1000_cosebis_f_overlap_header_footprint_rule_v1_summary.csv
docs/kids1000_cosebis_f_overlap_header_footprint_rule_v1.md
scripts/build_kids1000_cosebis_f_overlap_header_footprint_rule_v1.py
scripts/validate_kids1000_cosebis_f_overlap_header_footprint_rule_v1.py
```

It derives a header-WCS area proxy from the 196 mask products and attaches it
to the full `300 x 196 = 58,800` target-row by route-tile domain. This is a
source-only `F_overlap` rule candidate, but it does not read pixel-mask values
and does not construct a path mapping or score.

The corresponding degeneracy audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1.csv
data/derived/kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1_summary.csv
docs/kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1.md
scripts/build_kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1.py
scripts/validate_kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1.py
```

The audit preserves an important negative result: all route tiles have the
same header-footprint area at this precision, so `F_overlap=1` for every tile.
This rule is source-frozen and leakage-safe, but it is too uniform to support a
non-degenerate endpoint mapping. The next scoring-facing `F_overlap` step is a
pixel-mask or sub-tile overlap rule derived without endpoint inputs.

The first pixel-content `F_overlap` pilot is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_pixel_fraction_pilot_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_pixel_fraction_pilot_tile_v1.csv
data/derived/kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1_summary.csv
docs/kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1.md
scripts/build_kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1.py
scripts/validate_kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1.py
```

It uses only the three committed, source-frozen mask products and their
upstream parsed finite/nonzero pixel fractions. Unlike the header footprint
proxy, this pixel-content pilot is non-uniform (`F_overlap` ranges from about
`0.866` to `1.000` on the subset). This is a proof-of-method result, not a
population endpoint: it resolves the header-uniformity concern only for the
subset and motivates a full-route streaming/cache pixel or sub-tile extractor.

The source-frozen full-route pixel-fraction `F_overlap` rule is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_route_pixel_fraction_tile_rule_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1_summary.csv
docs/kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.md
scripts/build_kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.py
scripts/validate_kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.py
```

It reads the 196 source mask products from the local full-route cache plus the
committed subset masks, computes a finite/nonzero pixel-content fraction for
each route tile, and attaches the resulting source-only factor to the full
`300 x 196 = 58,800` target-row by route-tile domain. The rule is
non-degenerate (`F_overlap` ranges from about `0.453` to `1.000`, with 196
rounded unique tile values). This resolves the `F_overlap` source blocker, but
it still computes no path mapping, theory vector, prediction, residual, or
score. Public reproduction validates the committed outputs; rebuilding them
requires the ignored local raw mask cache documented in the full-route cache
inventory.

The source-frozen full-route `D_path` mask-load proxy is recorded in:

```text
data/source_manifest/kids1000_cosebis_d_path_full_route_mask_load_rule_policy_v1.csv
data/derived/kids1000_cosebis_d_path_full_route_mask_load_tile_rule_v1.csv
data/derived/kids1000_cosebis_d_path_full_route_mask_load_rule_v1.csv
data/derived/kids1000_cosebis_d_path_full_route_mask_load_rule_v1_summary.csv
docs/kids1000_cosebis_d_path_full_route_mask_load_rule_v1.md
scripts/build_kids1000_cosebis_d_path_full_route_mask_load_rule_v1.py
scripts/validate_kids1000_cosebis_d_path_full_route_mask_load_rule_v1.py
```

It uses the same 196 source mask products, but extracts a different observable:
the mean nonzero mask value per tile, normalized by the maximum tile mean. This
is not a calibrated survey-depth map; it is a caveated source-side mask-load
proxy. It is non-degenerate (`D_path` ranges from about `0.508` to `1.000`) and
is not identical to the `F_overlap` coverage channel. This resolves the
`D_path` source blocker only as a mask-load proxy; it still computes no mapping
vector, theory vector, prediction, residual, or endpoint score.

The source-frozen `E_web` null-control rule is recorded in:

```text
data/source_manifest/kids1000_cosebis_e_web_null_control_rule_policy_v1.csv
data/derived/kids1000_cosebis_e_web_null_control_tile_rule_v1.csv
data/derived/kids1000_cosebis_e_web_null_control_rule_v1.csv
data/derived/kids1000_cosebis_e_web_null_control_rule_v1_summary.csv
docs/kids1000_cosebis_e_web_null_control_rule_v1.md
scripts/build_kids1000_cosebis_e_web_null_control_rule_v1.py
scripts/validate_kids1000_cosebis_e_web_null_control_rule_v1.py
```

It freezes `E_web(tile)=1` for all 196 route tiles and all 58,800 domain rows.
This is intentionally uniform and therefore is not a non-degenerate
web/environment measurement. It resolves the web gate only as a path-only
null-control route with no positive web claim, and computes no mapping vector,
theory vector, prediction, residual, or endpoint score.

The `F_overlap` batch-promotion review checklist is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_batch_promotion_review_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_batch_promotion_review_v1.csv
data/derived/kids1000_cosebis_f_overlap_batch_promotion_review_v1_summary.csv
docs/kids1000_cosebis_f_overlap_batch_promotion_review_policy_v1.md
scripts/build_kids1000_cosebis_f_overlap_batch_promotion_review_v1.py
scripts/validate_kids1000_cosebis_f_overlap_batch_promotion_review_v1.py
```

It is currently expected to remain `promotion_ready=false`: there is no
committed fetched-batch review artifact, no checksum manifest for fetched
products, and no forbidden-input audit for a fetched batch. This checklist
does not read ignored `data/local/` execution logs and computes no overlap
rule, mapping vector, theory vector, prediction, residual, or score.
The checklist also records the availability of the filled-review validator as a
satisfied-but-not-promoting item; this makes the future review path more
auditable without changing the current negative promotion status.

The future fetched-batch execution-review schema is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_execution_review_schema_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_execution_review_schema_v1.csv
data/derived/kids1000_cosebis_f_overlap_execution_review_schema_v1_summary.csv
docs/kids1000_cosebis_f_overlap_execution_review_schema_policy_v1.md
scripts/build_kids1000_cosebis_f_overlap_execution_review_schema_v1.py
scripts/validate_kids1000_cosebis_f_overlap_execution_review_schema_v1.py
```

It freezes the required columns for a later committed fetched-batch review
artifact: product identity, URL, cache path, HTTP status, byte count, SHA-256,
review status, reviewer role, forbidden-input flags, and claim-boundary flags.
It does not fetch products or promote a batch.

The default batch-0 execution-review template is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_execution_review_template_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_execution_review_template_v1.csv
data/derived/kids1000_cosebis_f_overlap_execution_review_template_v1_summary.csv
docs/kids1000_cosebis_f_overlap_execution_review_template_policy_v1.md
scripts/build_kids1000_cosebis_f_overlap_execution_review_template_v1.py
scripts/validate_kids1000_cosebis_f_overlap_execution_review_template_v1.py
docs/kids1000_cosebis_f_overlap_filled_execution_review_validator_v1.md
scripts/validate_kids1000_cosebis_f_overlap_filled_execution_review_artifact_v1.py
data/source_manifest/kids1000_cosebis_f_overlap_resolution_decision_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_resolution_decision_v1.csv
data/derived/kids1000_cosebis_f_overlap_resolution_decision_v1_summary.csv
docs/kids1000_cosebis_f_overlap_resolution_decision_v1.md
scripts/build_kids1000_cosebis_f_overlap_resolution_decision_v1.py
scripts/validate_kids1000_cosebis_f_overlap_resolution_decision_v1.py
data/source_manifest/kids1000_cosebis_partial_control_scoring_protocol_v1.csv
docs/kids1000_cosebis_partial_control_scoring_protocol_v1.md
scripts/validate_kids1000_cosebis_partial_control_scoring_protocol_v1.py
data/source_manifest/kids1000_cosebis_partial_control_mapping_shell_policy_v1.csv
data/derived/kids1000_cosebis_partial_control_mapping_shell_v1.csv
data/derived/kids1000_cosebis_partial_control_mapping_shell_v1_summary.csv
docs/kids1000_cosebis_partial_control_mapping_shell_v1.md
scripts/build_kids1000_cosebis_partial_control_mapping_shell_v1.py
scripts/validate_kids1000_cosebis_partial_control_mapping_shell_v1.py
```

It materializes the 20 planned batch-0 product rows using the frozen
execution-review schema, but keeps all network, checksum, timestamp, and
reviewer fields empty or pending. It is a reviewer template, not an execution
log or source-freeze artifact.

The filled execution-review validator is a utility for checking either this
committed empty template (`--mode template`) or a future manually filled
execution-review artifact (`--mode filled`) against the frozen schema and
batch-0 dry-run identities. It does not fetch products, promote a batch,
derive an overlap rule, construct a path-mapping vector, or enable endpoint
scoring.
The F-overlap resolution decision gate records the current formal blocker
decision: no endpoint-grade overlap route is accepted; the three source-frozen
mask products are accepted only as a caveated partial path-mask control; the
official-geometry and batch-0 dry-run routes remain unresolved. The
full-196-mask route is now source-cache complete in the committed local
inventory snapshot. A source-frozen header-footprint rule has also been
derived, but the degeneracy audit shows it is uniform and not promotable as a
non-degenerate endpoint mapping support. The route remains endpoint-disabled
until a pixel-mask or sub-tile overlap rule is derived without endpoint inputs.
The partial-control scoring protocol freezes only a future diagnostic grammar
for that caveated three-mask control. It keeps both partial-control scoring and
endpoint scoring disabled and emits no score artifacts.
The partial-control mapping shell materializes the `300 x 3 = 900` source-side
support table linking the COSEBIs template rows to the three caveated mask
controls. It carries mask-shell observables and row identities only; no mapping
value, theory vector, residual, or score is computed.
The subsequent partial-control mapping-values artifact applies a frozen
source-only diagnostic rule to that same `900`-row support table:
`source_mask_shell_value * normalized_pair_mean_z_weight * mode^{-1/2}`.
The mean-redshift weight comes from the source-frozen KiDS `NZ_SOURCE`
inventory and the mode weight comes from COSEBIs row structure. This is a
caveated partial-control mapping-value vector only; it is not an endpoint
mapping vector, not a COSEBIs theory vector, and still emits no residual,
likelihood, score, AIC value, or validation result.

```text
data/source_manifest/kids1000_cosebis_partial_control_mapping_values_policy_v1.csv
data/derived/kids1000_cosebis_partial_control_mapping_values_v1.csv
data/derived/kids1000_cosebis_partial_control_mapping_values_v1_summary.csv
docs/kids1000_cosebis_partial_control_mapping_values_v1.md
scripts/build_kids1000_cosebis_partial_control_mapping_values_v1.py
scripts/validate_kids1000_cosebis_partial_control_mapping_values_v1.py
```
The partial-control design matrix then reduces those `900` mapping values to
six deterministic `300`-row diagnostic branches: `baseline_zero`,
`mask_sample_0`, `mask_sample_98`, `mask_sample_195`, `positive_mask_mean`, and
`sign_flip_positive_mean`. This is scoring-facing support only; it is not an
endpoint theory vector and still does not use the KiDS data vector, covariance
solve, residuals, fit statistics, or post-hoc branch selection.

```text
data/source_manifest/kids1000_cosebis_partial_control_design_matrix_policy_v1.csv
data/derived/kids1000_cosebis_partial_control_design_matrix_v1.csv
data/derived/kids1000_cosebis_partial_control_design_matrix_v1_summary.csv
docs/kids1000_cosebis_partial_control_design_matrix_v1.md
scripts/build_kids1000_cosebis_partial_control_design_matrix_v1.py
scripts/validate_kids1000_cosebis_partial_control_design_matrix_v1.py
```
The first caveated partial-control diagnostic score is recorded in:

```text
data/source_manifest/kids1000_cosebis_partial_control_diagnostic_scoring_v1.csv
data/derived/kids1000_cosebis_partial_control_diagnostic_scoring_v1_grid.csv
data/derived/kids1000_cosebis_partial_control_diagnostic_scoring_v1_summary.csv
docs/kids1000_cosebis_partial_control_diagnostic_scoring_v1.md
scripts/run_kids1000_cosebis_partial_control_diagnostic_scoring_v1.py
scripts/validate_kids1000_cosebis_partial_control_diagnostic_scoring_v1.py
```

This run compares the frozen 300x6 branch matrix to the retained KiDS COSEBIs
`En` data vector using the full 300x300 covariance and a nonnegative
one-amplitude-per-branch rule. It improves the zero-branch diagnostic
chi-square by about `183.6`, but it is explicitly not endpoint validation. In
this simplified control, the positive mask branches are effectively
amplitude-degenerate, so the result should be read only as a successful
diagnostic scoring smoke test for the partial-control route.

The corresponding null replay is recorded in:

```text
data/source_manifest/kids1000_cosebis_partial_control_null_replay_v1.csv
data/derived/kids1000_cosebis_partial_control_null_replay_v1_grid.csv
data/derived/kids1000_cosebis_partial_control_null_replay_v1_summary.csv
docs/kids1000_cosebis_partial_control_null_replay_v1.md
scripts/run_kids1000_cosebis_partial_control_null_replay_v1.py
scripts/validate_kids1000_cosebis_partial_control_null_replay_v1.py
```

This replay compares the observed positive-mask diagnostic branch against
`1008` deterministic controls: sky rotations, tomographic-pair shuffles,
wrong-channel activations, and sign-flip controls. One pair-shuffle null
slightly outperforms the observed branch, so the observed branch is not an
absolute winner. The conservative plus-one tail fraction is `0.001982160555`.
This is a diagnostic rarity check only, not endpoint validation and not a
KiDS lensing population claim.

The partial-control degeneracy audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_partial_control_degeneracy_audit_policy_v1.csv
data/derived/kids1000_cosebis_partial_control_degeneracy_audit_v1_pair_grid.csv
data/derived/kids1000_cosebis_partial_control_degeneracy_audit_v1_summary.csv
docs/kids1000_cosebis_partial_control_degeneracy_audit_v1.md
scripts/build_kids1000_cosebis_partial_control_degeneracy_audit_v1.py
scripts/validate_kids1000_cosebis_partial_control_degeneracy_audit_v1.py
```

It shows that the positive partial-control branches are effectively rank one:
their covariance-metric absolute cosine is numerically unity and the maximum
positive-branch relative shape residual is about `2.2e-12`. This remains a
preserved negative result for the caveated three-mask partial-control route. It
is not erased by later gates: the partial-control branch is still unsuitable as
an endpoint family on its own.

The endpoint-family geometry audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_family_geometry_audit_policy_v1.csv
data/derived/kids1000_cosebis_endpoint_family_geometry_audit_v1.csv
data/derived/kids1000_cosebis_endpoint_family_geometry_audit_v1_summary.csv
docs/kids1000_cosebis_endpoint_family_geometry_audit_v1.md
scripts/build_kids1000_cosebis_endpoint_family_geometry_audit_v1.py
scripts/validate_kids1000_cosebis_endpoint_family_geometry_audit_v1.py
```

This audit replaces the three-mask partial-control geometry as the
endpoint-readiness geometry test. It uses the source-frozen candidate theory
shell plus the predeclared source-frozen null-control theory replay, with the
KiDS covariance used only as a geometry metric. It does not read the KiDS `En`
data-vector values, residuals, posterior chains, fit statistics, or endpoint
scores. The resulting endpoint comparison family has `1009` vectors over the
`300` retained COSEBIs rows and effective rank `15` in both the raw Euclidean
and covariance-metric geometry audits. This resolves the geometry readiness
blocker without converting the earlier partial-control diagnostic into
endpoint evidence.

The non-degenerate mapping promotion gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_non_degenerate_mapping_promotion_gate_policy_v1.csv
data/derived/kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.csv
data/derived/kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1_summary.csv
docs/kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.md
scripts/build_kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.py
scripts/validate_kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.py
```

It freezes six required promotion gates before any endpoint scoring: endpoint
grade `F_overlap`, source-preflight readiness, endpoint-family geometry,
a frozen 300-row theory vector, null controls after mapping, and leakage
guards. In the current repository the `F_overlap` endpoint-route gate,
source-preflight mapping state, source-frozen theory-vector gate, null-control
theory replay, endpoint-family geometry audit, and leakage guard pass. The
promotion gate now records `6` passed gates and `0` blockers. Endpoint scoring
remained disabled at this gate until a separate explicitly approved scoring run
was opened under the frozen protocol below.

The endpoint scoring-readiness ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_scoring_readiness_policy_v1.csv
data/derived/kids1000_cosebis_endpoint_scoring_readiness_v1.csv
data/derived/kids1000_cosebis_endpoint_scoring_readiness_v1_summary.csv
docs/kids1000_cosebis_endpoint_scoring_readiness_v1.md
scripts/build_kids1000_cosebis_endpoint_scoring_readiness_v1.py
scripts/validate_kids1000_cosebis_endpoint_scoring_readiness_v1.py
```

It collects the current pre-scoring state in one place. The data-vector
structure, covariance matrix, covariance solve policy, theory-vector
row-interface template, mapping-to-template join contract, F-overlap
resolution/control decision, web/path mapping ledger, and source preflight are
source-side ready. `F_overlap`, caveated `D_path`, null-control `E_web`,
source-side `C_norm`, the source-frozen mapping basis, and a source-frozen
unit-amplitude theory-vector shell are supported. The predeclared null controls
have also been replayed against the source-frozen theory shell as deterministic
control-vector digests, but no null score has been computed. The
endpoint-family geometry audit now passes, so the readiness ledger records `12`
ready components and `0` blockers. This readiness ledger does not itself score;
the separate approved run below is the first endpoint scoring artifact.

The frozen endpoint scoring protocol shell is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_scoring_protocol_v1.csv
docs/kids1000_cosebis_endpoint_scoring_protocol_v1.md
scripts/validate_kids1000_cosebis_endpoint_scoring_protocol_v1.py
```

It declares the future COSEBIs scoring grammar
`chi2 = (d - t)^T C^{-1} (d - t)`, the Cholesky solve policy, required
baseline/candidate/null-control comparisons, AIC/control-rank reporting, and
pass-condition shell. The protocol shell itself is not a score. The separate
approved run below is the first artifact that computes endpoint residuals,
chi-square values, AIC values, and null-control scores under that frozen
grammar.

The first approved endpoint scoring run is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_scoring_run_v1.csv
data/derived/kids1000_cosebis_endpoint_scoring_v1_results.csv
data/derived/kids1000_cosebis_endpoint_scoring_v1_residuals.csv
data/derived/kids1000_cosebis_endpoint_scoring_v1_grid.csv
data/derived/kids1000_cosebis_endpoint_scoring_v1_null_controls.csv
data/derived/kids1000_cosebis_endpoint_scoring_v1_summary.csv
docs/kids1000_cosebis_endpoint_scoring_v1.md
scripts/run_kids1000_cosebis_endpoint_scoring_v1.py
scripts/validate_kids1000_cosebis_endpoint_scoring_v1.py
```

This run is opened only after the readiness ledger records `12` ready
components and `0` blockers. It uses the retained 300-row KiDS COSEBIs `En`
vector only for scoring, not for source selection or post-hoc channel choices.
The source-frozen candidate improves over the zero baseline by
`Delta chi2 = -183.6152665217` and `Delta AIC = -181.6152665217` under the
full covariance Cholesky policy and a nonnegative single-amplitude branch rule.
Against the `1008` predeclared null-control vectors, the candidate ranks
`3/1009` by both chi-square and AIC, with a plus-one null tail fraction of
`0.002973240832507`. This is an endpoint score, not a KiDS validation claim:
two predeclared null controls score better than the candidate, so the
claim-safe reading is a low-tail endpoint signal that requires follow-up
robustness.

The endpoint scoring diagnostics are recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_scoring_diagnostics_policy_v1.csv
data/derived/kids1000_cosebis_endpoint_scoring_diagnostics_v1_family_summary.csv
data/derived/kids1000_cosebis_endpoint_scoring_diagnostics_v1_top_nulls.csv
data/derived/kids1000_cosebis_endpoint_scoring_diagnostics_v1_summary.csv
scripts/build_kids1000_cosebis_endpoint_scoring_diagnostics_v1.py
scripts/validate_kids1000_cosebis_endpoint_scoring_diagnostics_v1.py
```

The diagnostic result is
`candidate_low_tail_but_not_absolute_winner_tomographic_shuffle_controls_dominate`.
The two controls that beat the candidate both come from the
`tomographic_pair_shuffle` family. No `sky_rotation`, `wrong_channel_activation`,
or `web_path_sign_flip` control beats the candidate. This narrows the next
robustness question to tomographic-pair structure rather than to a generic
wrong-channel or sign-flip failure.

The tomographic-structure robustness run is recorded in:

```text
data/source_manifest/kids1000_cosebis_tomographic_structure_robustness_policy_v1.csv
data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_controls.csv
data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_family_summary.csv
data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_top_controls.csv
data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_summary.csv
docs/kids1000_cosebis_tomographic_structure_robustness_v1.md
scripts/run_kids1000_cosebis_tomographic_structure_robustness_v1.py
scripts/validate_kids1000_cosebis_tomographic_structure_robustness_v1.py
```

This run compares the same endpoint candidate against stricter tomographic
controls: all `119` non-identity five-bin label permutations and `1000`
auto/cross-preserving pair shuffles. The candidate remains low-tail with rank
`4/1120` and plus-one tail fraction `0.003571428571429`. Three structured
controls beat it, so this is robustness evidence rather than validation. The
remaining caveat is specifically tomographic-structure robustness.

The tomographic-control plausibility audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_tomographic_control_plausibility_audit_policy_v1.csv
data/derived/kids1000_cosebis_tomographic_control_plausibility_audit_v1.csv
data/derived/kids1000_cosebis_tomographic_control_plausibility_audit_v1_summary.csv
docs/kids1000_cosebis_tomographic_control_plausibility_audit_v1.md
scripts/build_kids1000_cosebis_tomographic_control_plausibility_audit_v1.py
scripts/validate_kids1000_cosebis_tomographic_control_plausibility_audit_v1.py
```

This audit checks whether the better tomographic controls should be interpreted
as physical alternatives. It reads the top `25` tomographic controls and the
source-side redshift kernel inventory, computes mapping-geometry diagnostics,
and computes no new scores. Among the three audited controls that beat the
candidate, two are control-only non-global pair shuffles and one is only a
conditional source-systematic candidate requiring independent photo-z or
tomographic calibration support. No better control is accepted as a physical
alternative in the current source state. Therefore the controls do not refute
the endpoint signal, but they still block validation.

The tomographic holdout/calibration gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_tomographic_holdout_calibration_gate_policy_v1.csv
data/derived/kids1000_cosebis_tomographic_holdout_calibration_gate_v1.csv
data/derived/kids1000_cosebis_tomographic_holdout_calibration_gate_v1_summary.csv
docs/kids1000_cosebis_tomographic_holdout_calibration_gate_v1.md
scripts/build_kids1000_cosebis_tomographic_holdout_calibration_gate_v1.py
scripts/validate_kids1000_cosebis_tomographic_holdout_calibration_gate_v1.py
```

This gate is the next validation-facing work order, not a new score. It freezes
the conditions required before any tomographic endpoint replay can be treated as
validation-facing: independent photo-z or tomographic-calibration evidence, a
source-bin or tomographic-pair holdout partition, a rule for promoting a
tomographic control to a source-systematic candidate, a frozen replay protocol,
and a leakage validator. It explicitly forbids observed COSEBIs values,
endpoint residuals, `Delta chi2`, null-control ranks, best-control identity, and
post-score residual shape from source-side selection. Its verdict is
`tomographic_holdout_required_before_endpoint_replay_or_validation`.

The following H1/R4 artifacts are chronological prerequisite states. Statements
such as "H1 remains open" or "R4 remains incomplete" describe the local state of
that artifact when it was created. The current post-reviewer source-side closure
state is recorded later in
`data/derived/kids1000_cosebis_external_photoz_calibration_closure_ledger_v1_summary.csv`:
R4/H1 are source-side closed for the external photo-z calibration route, while
endpoint replay remains forbidden and endpoint validation is not claimed.

The first source-frozen tomographic holdout manifest is recorded in:

```text
data/source_manifest/kids1000_cosebis_source_frozen_tomographic_holdout_manifest_policy_v1.csv
data/derived/kids1000_cosebis_source_frozen_tomographic_holdout_bins_v1.csv
data/derived/kids1000_cosebis_source_frozen_tomographic_holdout_pairs_v1.csv
data/derived/kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1_summary.csv
docs/kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1.md
scripts/build_kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1.py
scripts/validate_kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1.py
```

This manifest freezes the H2 holdout partition as a deterministic
leave-one-source-bin schedule. In fold `k`, all tomographic pairs touching
source bin `k` are held out, and all other pairs are calibration pairs. The
manifest uses the committed source-native redshift-kernel inventory only; it
does not use observed COSEBIs values, residuals, fit statistics, or null ranks.
It does not complete H1: independent external photo-z/tomographic calibration is
still open, so endpoint replay remains forbidden. Its verdict is
`holdout_partition_frozen_but_independent_photoz_calibration_still_open`.

The source-side photo-z/tomographic calibration evidence ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_photoz_tomographic_calibration_evidence_policy_v1.csv
data/derived/kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.csv
data/derived/kids1000_cosebis_photoz_tomographic_calibration_evidence_v1_summary.csv
docs/kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.md
scripts/build_kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.py
scripts/validate_kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.py
```

This ledger records the H1 state without reopening endpoint scoring. It accepts
the checksum-frozen KiDS lensing product, cached public KiDS DR4 lensing-page
photo-z/SOM-gold documentation markers, and the committed source-native
`NZ_SOURCE` five-bin inventory. It also records the remaining blocker:
independent external photo-z or tomographic calibration is not yet attached.
Endpoint replay and validation claims remain forbidden. Its verdict is
`partial_photoz_tomographic_evidence_available_but_h1_external_calibration_open`.

The external photo-z/tomographic calibration acquisition plan is recorded in:

```text
data/source_manifest/kids1000_cosebis_external_photoz_calibration_acquisition_plan_policy_v1.csv
data/derived/kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.csv
data/derived/kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1_summary.csv
docs/kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.md
scripts/build_kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.py
scripts/validate_kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.py
```

This plan freezes the missing H1 acquisition routes: a source-frozen photo-z
calibration reference or product manifest, a SOM-gold or redshift-distribution
validation manifest, tomographic-bin quality or \(\Delta z\) prior evidence, and
a leakage review for any attached calibration artifacts. At this planning
stage, no route is attached, so H1 remains open and endpoint replay remains
forbidden. Its verdict is
`external_photoz_calibration_acquisition_plan_frozen_h1_still_open`.

The external photo-z/tomographic calibration source manifest is recorded in:

```text
data/source_manifest/kids1000_cosebis_external_photoz_calibration_source_manifest_policy_v1.csv
data/derived/kids1000_cosebis_external_photoz_calibration_source_manifest_v1.csv
data/derived/kids1000_cosebis_external_photoz_calibration_source_manifest_v1_summary.csv
docs/kids1000_cosebis_external_photoz_calibration_source_manifest_v1.md
scripts/build_kids1000_cosebis_external_photoz_calibration_source_manifest_v1.py
scripts/validate_kids1000_cosebis_external_photoz_calibration_source_manifest_v1.py
```

This manifest attaches cached public sources for the H1 routes R1--R3: the
A&A KiDS-1000 redshift-calibration article, its arXiv metadata page, and the
official KiDS DR4 SOM-gold catalogue page. The marker checks are source-side
only: SOM calibration, five tomographic redshift bins, gold selection,
mean-redshift bias/uncertainty statements, clustering-redshift cross-checks,
and the official KiDS \(n(z)\) product route. The R4 leakage review is still
open, so H1 is not complete and endpoint replay remains forbidden. Its verdict
is `external_photoz_calibration_sources_attached_pending_leakage_review`.

The automated leakage-review preflight for those attached sources is recorded
in:

```text
data/source_manifest/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_policy_v1.csv
data/derived/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.csv
data/derived/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1_summary.csv
docs/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.md
scripts/build_kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.py
scripts/validate_kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.py
```

This preflight passes the automated no-endpoint-leakage checks for the cached
R1--R3 source artifacts and the source-manifest builder. It is not an
independent reviewer attestation. The full R4 leakage review remains open, H1
remains incomplete, and endpoint replay remains forbidden. Its verdict is
`automated_leakage_preflight_passed_independent_reviewer_still_open`.

The independent reviewer attestation template is recorded in:

```text
data/source_manifest/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_policy_v1.csv
data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.csv
data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1_summary.csv
docs/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.md
scripts/build_kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.py
scripts/validate_kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.py
```

This template is a blank handoff artifact for the remaining independent review
step. It records the questions and forbidden inputs a reviewer must respect,
but it is not a completed review response. R4 remains incomplete, H1 remains
incomplete, and endpoint replay remains forbidden. Its verdict is
`reviewer_attestation_template_ready_not_completed`.

The portable reviewer handoff package is recorded in:

```text
data/source_manifest/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_policy_v1.csv
REVIEWER_README_KIDS1000_PHOTOZ_HANDOFF.md
data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.zip
data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.zip.sha256
data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1_manifest.csv
data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1_summary.csv
docs/kids1000_cosebis_external_photoz_calibration_external_reviewer_instructions_v1.md
docs/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.md
scripts/build_kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.py
scripts/validate_kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.py
```

This ZIP packages a root reviewer README, the blank reviewer template, external
reviewer instructions, source manifest, automated leakage preflight,
completed-response validation rule, short docs, and cached public source pages.
It contains no endpoint residuals, endpoint scores, ranks, fit statistics, or
post-score residual shapes. It is a handoff package only: R4 remains incomplete,
H1 remains incomplete, and endpoint replay remains forbidden. Its verdict is
`reviewer_handoff_package_ready_not_completed`.
The adjacent `.zip.sha256` sidecar is provided only for transfer integrity.

The completed reviewer response validator is recorded in:

```text
data/source_manifest/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_policy_v1.csv
docs/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.md
scripts/validate_kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.py
```

This validator checks a returned reviewer CSV as source-side evidence only:
even an accepted response does not compute new scores, does not claim endpoint
validation, and does not authorize endpoint replay. Its accepted verdict is
`completed_reviewer_response_accepted_source_side_only_endpoint_replay_still_forbidden`.

The completed source-side reviewer response is recorded in:

```text
data/derived/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.csv
data/derived/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1_summary.csv
docs/kids1000_cosebis_external_photoz_calibration_completed_review_notes_v1.md
```

This response accepts R4 as caveated source-side evidence and marks the H1
external photo-z calibration evidence gate as source-side complete. It remains
strictly non-endpoint: it computes no new scores, contains no endpoint data,
does not authorize endpoint replay, and does not claim endpoint validation.

The external photo-z calibration closure ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_external_photoz_calibration_closure_ledger_policy_v1.csv
data/derived/kids1000_cosebis_external_photoz_calibration_closure_ledger_v1.csv
data/derived/kids1000_cosebis_external_photoz_calibration_closure_ledger_v1_summary.csv
docs/kids1000_cosebis_external_photoz_calibration_closure_ledger_v1.md
scripts/build_kids1000_cosebis_external_photoz_calibration_closure_ledger_v1.py
scripts/validate_kids1000_cosebis_external_photoz_calibration_closure_ledger_v1.py
```

This ledger is the current post-reviewer source-side closure state: R4/H1 are
closed for the external photo-z calibration route, while endpoint replay remains
forbidden and endpoint validation is not claimed. Earlier acquisition, manifest,
preflight, and handoff artifacts remain historical prerequisite states.

The endpoint replay authorization review package is recorded in:

```text
REVIEWER_MESSAGE_KIDS1000_ENDPOINT_REPLAY_AUTHORIZATION.md
REVIEWER_README_KIDS1000_ENDPOINT_REPLAY_AUTHORIZATION.md
data/source_manifest/kids1000_cosebis_endpoint_replay_authorization_review_policy_v1.csv
data/derived/kids1000_cosebis_endpoint_replay_authorization_review_response_template_v1.csv
data/derived/kids1000_cosebis_endpoint_replay_authorization_review_response_v1.csv
data/derived/kids1000_cosebis_endpoint_replay_authorization_review_response_v1_summary.csv
data/derived/kids1000_cosebis_endpoint_replay_authorization_review_package_v1.zip
data/derived/kids1000_cosebis_endpoint_replay_authorization_review_package_v1.zip.sha256
data/derived/kids1000_cosebis_endpoint_replay_authorization_review_package_v1_manifest.csv
docs/kids1000_cosebis_endpoint_replay_authorization_review_v1.md
scripts/validate_kids1000_cosebis_endpoint_replay_authorization_review_response_v1.py
```

This package is for an external reviewer without repository access. It asks only
for a go/no-go decision on whether a separate, single, predeclared endpoint
replay may be authorized under the frozen source-side state. It contains no
observed COSEBIs values, endpoint residuals, endpoint scores, fit statistics,
null-control ranks, or post-score residual shapes. A go decision would be replay
permission only: `endpoint_validation_claimed=false` must remain fixed.
The completed reviewer response accepts this permission-only gate:
`endpoint_replay_allowed=true` and `endpoint_validation_claimed=false`. Its
verdict is `endpoint_replay_authorized_permission_only_not_validation`.

The authorized endpoint replay is recorded in:

```text
data/source_manifest/kids1000_cosebis_authorized_endpoint_replay_run_v1.csv
data/derived/kids1000_cosebis_authorized_endpoint_replay_v1_summary.csv
scripts/run_kids1000_cosebis_authorized_endpoint_replay_v1.py
scripts/validate_kids1000_cosebis_authorized_endpoint_replay_v1.py
```

This wrapper replays the already frozen KiDS/COSEBIs endpoint scoring grammar
after the permission-only authorization gate. It records the same low-tail
endpoint signal (`Delta chi2 = -183.6152665217`, plus-one null tail fraction
`0.002973240832507`) while preserving
`endpoint_validation_claimed=false`. The claim-safe verdict is
`authorized_endpoint_replay_low_tail_signal_not_validation`.

The post-replay tomographic-control disambiguation ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_tomographic_control_disambiguation_policy_v1.csv
data/derived/kids1000_cosebis_tomographic_control_disambiguation_v1.csv
data/derived/kids1000_cosebis_tomographic_control_disambiguation_v1_summary.csv
docs/kids1000_cosebis_tomographic_control_disambiguation_v1.md
scripts/build_kids1000_cosebis_tomographic_control_disambiguation_v1.py
scripts/validate_kids1000_cosebis_tomographic_control_disambiguation_v1.py
```

This ledger computes no new endpoint score. It only classifies the three
tomographic controls that beat the candidate in the stricter tomographic
robustness ensemble: two are control-only relabel/pair-shuffle controls, one
is a conditional source-systematic candidate requiring independent photo-z or
tomographic support, and zero are accepted as physical alternatives. The
result blocks endpoint validation but does not refute the low-tail endpoint
signal.

The source-frozen tomographic holdout replay is recorded in:

```text
data/source_manifest/kids1000_cosebis_tomographic_holdout_replay_policy_v1.csv
data/derived/kids1000_cosebis_tomographic_holdout_replay_v1_grid.csv
data/derived/kids1000_cosebis_tomographic_holdout_replay_v1_summary.csv
docs/kids1000_cosebis_tomographic_holdout_replay_v1.md
scripts/run_kids1000_cosebis_tomographic_holdout_replay_v1.py
scripts/validate_kids1000_cosebis_tomographic_holdout_replay_v1.py
```

This replay uses the pre-frozen five source-bin holdout manifest. For each
fold, it fits the nonnegative amplitude on calibration tomographic pairs that
do not touch the held-out source bin, then scores only the held-out pairs. The
candidate improves over the zero baseline in `4/5` held-out folds and has
aggregate holdout `Delta chi2 = -521.8035067179`. One candidate-beating
tomographic control remains slightly better in the same replay, so the
holdout replay preserves the endpoint signal diagnostically but keeps the
tomographic-control caveat active. It is not validation.

The best holdout-beating tomographic-control source-evidence gate is recorded
in:

```text
data/source_manifest/kids1000_cosebis_best_tomographic_control_source_evidence_gate_policy_v1.csv
data/derived/kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1.csv
data/derived/kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1_summary.csv
docs/kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1.md
scripts/build_kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1.py
scripts/validate_kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1.py
```

This gate audits the one holdout-beating control,
`seeded_auto_cross_shuffle_702759`. It is not induced by a single global
source-bin relabel: the auto-pair map would imply `1->2` and `2->3`, so a
global relabel would map `1-2` to `2-3`, whereas the control maps `1-2` to
`1-5`. With no independent photo-z/tomographic source evidence attached, the
control remains control-only. It does not refute the endpoint signal, but the
broader tomographic-control caveat still blocks validation.

The KiDS/COSEBIs validation-readiness ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_validation_readiness_ledger_policy_v1.csv
data/derived/kids1000_cosebis_validation_readiness_ledger_v1.csv
data/derived/kids1000_cosebis_validation_readiness_ledger_v1_summary.csv
docs/kids1000_cosebis_validation_readiness_ledger_v1.md
scripts/build_kids1000_cosebis_validation_readiness_ledger_v1.py
scripts/validate_kids1000_cosebis_validation_readiness_ledger_v1.py
```

This ledger computes no new score. It summarizes the current KiDS endpoint
state after the authorized replay, tomographic-control disambiguation,
source-bin holdout replay, best-control source-evidence gate, and physical
promotion blocker ledger. Its allowed current claim is
`diagnostic_low_tail_signal_with_reduced_tomographic_control_concern_not_validation`.
The signal has survived the narrow follow-up checks performed so far, and the
most dangerous tomographic control is not accepted as a physical alternative.
However, `validation_ready=false`: the tomographic caveat remains active and
physical promotion remains blocked by open operator/amplitude/normalization
requirements.

The KiDS/COSEBIs tomographic/photo-z closure status ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_tomographic_photoz_closure_status_policy_v1.csv
data/derived/kids1000_cosebis_tomographic_photoz_closure_status_v1.csv
data/derived/kids1000_cosebis_tomographic_photoz_closure_status_v1_summary.csv
docs/kids1000_cosebis_tomographic_photoz_closure_status_v1.md
scripts/build_kids1000_cosebis_tomographic_photoz_closure_status_v1.py
scripts/validate_kids1000_cosebis_tomographic_photoz_closure_status_v1.py
```

This ledger computes no new score. It records the narrower post-reviewer
status: the external photo-z/tomographic route is source-side closed
(`h1_independent_evidence_complete=true`,
`r4_leakage_review_complete=true`), the source-bin holdout signal survives
diagnostically, and the best holdout-beating tomographic control remains
control-only rather than a physical alternative. The allowed current claim is
`source_side_photoz_closed_and_holdout_signal_survives_but_validation_blocked`.
It reduces the tomographic/photo-z source-side concern, but it does not make the
KiDS branch validation-ready: `validation_ready=false` and
`physical_promotion_ready=false`.

The physical-promotion dependency order ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_physical_promotion_dependency_order_policy_v1.csv
data/derived/kids1000_cosebis_physical_promotion_dependency_order_v1.csv
data/derived/kids1000_cosebis_physical_promotion_dependency_order_v1_summary.csv
docs/kids1000_cosebis_physical_promotion_dependency_order_v1.md
scripts/build_kids1000_cosebis_physical_promotion_dependency_order_v1.py
scripts/validate_kids1000_cosebis_physical_promotion_dependency_order_v1.py
```

This ledger computes no new score and proves no new theorem. It orders the five
remaining physical-promotion blockers by logical dependency. The next primary
proof gate is `B2_operator_leakage_theorem_open`; the next parallel proof gate
is `B3_gauge_quotient_descent_open`. Response-unit normalization, the
standard-lensing/no-Tau-source null-amplitude theorem, and the full
survey-native operator theorem remain downstream. Its verdict is
`physical_promotion_ordered_leakage_and_gauge_are_next_not_validation`.

The B2 operator-leakage proof-plan ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_operator_leakage_proof_plan_policy_v1.csv
data/derived/kids1000_cosebis_operator_leakage_proof_plan_v1.csv
data/derived/kids1000_cosebis_operator_leakage_proof_plan_v1_summary.csv
docs/kids1000_cosebis_operator_leakage_proof_plan_v1.md
scripts/build_kids1000_cosebis_operator_leakage_proof_plan_v1.py
scripts/validate_kids1000_cosebis_operator_leakage_proof_plan_v1.py
```

This ledger computes no new score and does not prove the leakage theorem. It
freezes the exit conditions for the next primary proof gate. The uniform
tile-average null limit is available, and the no-endpoint-feedback guard is
satisfied. Three proof steps remain open: non-uniform leakage projection,
pure-mask quotient/control, and single-operator coupling. Its verdict is
`B2_operator_leakage_exit_conditions_frozen_but_theorem_open`.

The non-uniform leakage projection criterion is recorded in:

```text
data/source_manifest/kids1000_cosebis_operator_leakage_projection_criterion_policy_v1.csv
data/source_manifest/kids1000_cosebis_operator_leakage_domain_decomposition_policy_v1.csv
data/derived/kids1000_cosebis_operator_leakage_domain_decomposition_v1.csv
data/derived/kids1000_cosebis_operator_leakage_domain_decomposition_v1_summary.csv
docs/kids1000_cosebis_operator_leakage_domain_decomposition_v1.md
scripts/build_kids1000_cosebis_operator_leakage_domain_decomposition_v1.py
scripts/validate_kids1000_cosebis_operator_leakage_domain_decomposition_v1.py
data/derived/kids1000_cosebis_operator_leakage_projection_criterion_v1.csv
data/derived/kids1000_cosebis_operator_leakage_projection_criterion_v1_summary.csv
docs/kids1000_cosebis_operator_leakage_projection_criterion_v1.md
scripts/build_kids1000_cosebis_operator_leakage_projection_criterion_v1.py
scripts/validate_kids1000_cosebis_operator_leakage_projection_criterion_v1.py
```

This criterion computes no new score and proves no new theorem. It states the
sufficient condition needed to close the `P2_nonuniform_leakage_projection`
step: mask-only source directions must either project to zero in the physical
low-mode response class, modulo quotient-null directions, or be routed into a
predeclared null-control family by the same source-native operator that
generates the mode response. The verdict is
`nonuniform_leakage_projection_criterion_frozen_but_not_proven`.

The supporting domain-decomposition ledger now declares the bookkeeping split
`V_source = V_phys_candidate + V_mask + V_control_or_null`. Here
`V_phys_candidate` is only the source-frozen low-mode candidate response shell,
`V_mask` is the pure-mask/depth/path basis, and `V_control_or_null` is the
predeclared null-control family. This closes only the naming/bookkeeping part of
the criterion: pairwise orthogonality, null projection, control routing, and the
operator-leakage theorem all remain open. Its verdict is
`domain_decomposition_declared_but_projection_and_leakage_theorem_remain_open`.

The endpoint jackknife/localization robustness audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_jackknife_robustness_policy_v1.csv
data/derived/kids1000_cosebis_endpoint_jackknife_robustness_v1_grid.csv
data/derived/kids1000_cosebis_endpoint_jackknife_robustness_v1_summary.csv
docs/kids1000_cosebis_endpoint_jackknife_robustness_v1.md
scripts/run_kids1000_cosebis_endpoint_jackknife_robustness_v1.py
scripts/validate_kids1000_cosebis_endpoint_jackknife_robustness_v1.py
```

This post-score audit keeps the source-frozen theory vector fixed and reruns
the same full-covariance, nonnegative single-amplitude scoring rule on
predeclared localization masks. All `20/20` leave-one source-bin and
leave-one tomographic-pair subsets retain negative `Delta chi2` and negative
`Delta AIC`, so the endpoint signal is not carried by a single source bin or
single tomographic pair under this first jackknife. The mode-band result is
more caveated: only `2/3` mode-band subsets improve, and the low-mode-removed
subset has `Delta chi2 = 0`. This is localization robustness, not validation.

The endpoint mode-localization audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_mode_localization_policy_v1.csv
data/derived/kids1000_cosebis_endpoint_mode_localization_v1_grid.csv
data/derived/kids1000_cosebis_endpoint_mode_localization_v1_summary.csv
docs/kids1000_cosebis_endpoint_mode_localization_v1.md
scripts/run_kids1000_cosebis_endpoint_mode_localization_v1.py
scripts/validate_kids1000_cosebis_endpoint_mode_localization_v1.py
```

This follow-up audit localizes the mode-band caveat. It scores predeclared
single-mode, cumulative-low-mode, and low-mode-removal subsets under the same
full-covariance submatrix and nonnegative single-amplitude policy. The best
single mode is `single_mode_1` with `Delta chi2 = -101.5735188246`; the best
cumulative low-mode subset is `cumulative_low_modes_1_to_3` with
`Delta chi2 = -237.1074068478`; and removing modes `1-5` gives
`Delta chi2 = 0`. The claim-safe verdict is that the endpoint signal is
strongly low-mode localized: this is a useful diagnostic and a sharpened
follow-up target, not validation.

The endpoint mode-shape stress audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_mode_shape_stress_policy_v1.csv
data/derived/kids1000_cosebis_endpoint_mode_shape_stress_v1_grid.csv
data/derived/kids1000_cosebis_endpoint_mode_shape_stress_v1_summary.csv
docs/kids1000_cosebis_endpoint_mode_shape_stress_v1.md
scripts/run_kids1000_cosebis_endpoint_mode_shape_stress_v1.py
scripts/validate_kids1000_cosebis_endpoint_mode_shape_stress_v1.py
```

This stress test keeps the same source-frozen `W_path` mapping and endpoint
scoring rule, but replaces the source-independent mode carrier. The predeclared
candidate `n^-0.5` carrier remains best in this small stress family with
`Delta chi2 = -183.6152665217`; a flat carrier still improves with
`Delta chi2 = -136.5504934506`; and high-`n` weighting removes the signal
with `Delta chi2 = 0`. Thus the low-mode result is carrier-sensitive, but the
signal is not produced solely by the exact `n^-0.5` carrier choice. This is a
mode-shape sensitivity diagnostic, not validation.

The endpoint scoring synthesis ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_scoring_synthesis_ledger_policy_v1.csv
data/derived/kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.csv
data/derived/kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1_summary.csv
docs/kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.md
scripts/build_kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.py
scripts/validate_kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.py
```

This ledger does not compute a new score. It aggregates the approved endpoint
score, null-control diagnostics, tomographic-structure robustness, jackknife,
mode-localization, mode-shape stress, and physical-promotion blocker ledger into
one claim-safe synthesis. The current verdict is
`endpoint_signal_low_tail_caveated_by_tomographic_controls_and_physical_promotion_blockers`.
In plain terms, the KiDS COSEBIs branch has a low-tail diagnostic endpoint
signal, but it is not an absolute control winner, the tomographic-structure
caveat remains active. The better tomographic controls are not accepted as
physical alternatives without independent photo-z/tomographic calibration
support, and physical promotion is still blocked by the five requirements listed
below.

The low-mode carrier source-grounding ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_low_mode_carrier_source_grounding_policy_v1.csv
data/derived/kids1000_cosebis_low_mode_carrier_source_grounding_v1.csv
data/derived/kids1000_cosebis_low_mode_carrier_source_grounding_v1_summary.csv
docs/kids1000_cosebis_low_mode_carrier_source_grounding_v1.md
scripts/build_kids1000_cosebis_low_mode_carrier_source_grounding_v1.py
scripts/validate_kids1000_cosebis_low_mode_carrier_source_grounding_v1.py
```

This ledger answers the immediate reviewer question raised by the low-mode
diagnostics. It records that the `n^-0.5` carrier is source independent,
predeclared, unit-mean normalized, and not selected from KiDS data-vector values.
It is consistent with a broad coherent path/readout prior and with the post-score
diagnostics, but it is not a first-principles Tau Core lensing kernel derivation.
The verdict is
`partial_protocol_grounding_with_open_first_principles_derivation_blocker`.

The low-mode kernel-envelope derivation artifact is recorded in:

```text
data/source_manifest/kids1000_cosebis_low_mode_kernel_envelope_derivation_policy_v1.csv
data/derived/kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.csv
data/derived/kids1000_cosebis_low_mode_kernel_envelope_derivation_v1_mode_weights.csv
data/derived/kids1000_cosebis_low_mode_kernel_envelope_derivation_v1_summary.csv
docs/kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.md
scripts/build_kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.py
scripts/validate_kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.py
```

This artifact narrows the open blocker. Under the explicit source-side prior
that a smooth path/readout residual has approximately constant power per
logarithmic COSEBIs mode band, the discrete mode power scales as `P_n ~ 1/n`
and the coherent amplitude envelope scales as `sqrt(P_n) ~ n^-0.5`. The
finite retained mode domain then fixes the unit-mean normalization over
`n=1..20`. This is a conditional envelope derivation, not a covariant KiDS
lensing/path kernel theorem; the remaining blocker is the survey-native or
covariant derivation of when the log-band-neutral prior applies.

The log-band prior eligibility gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_log_band_prior_eligibility_gate_policy_v1.csv
data/derived/kids1000_cosebis_log_band_prior_eligibility_gate_v1.csv
data/derived/kids1000_cosebis_log_band_prior_eligibility_gate_v1_summary.csv
docs/kids1000_cosebis_log_band_prior_eligibility_gate_v1.md
scripts/build_kids1000_cosebis_log_band_prior_eligibility_gate_v1.py
scripts/validate_kids1000_cosebis_log_band_prior_eligibility_gate_v1.py
```

This gate states when the conditional log-band prior is allowed as a protocol
object. The current COSEBIs route passes ordered-mode, no-posthoc-mode-cut,
source-side path-mapping, and no-high-frequency-only guardrails. It still leaves
one unproven smoothness assumption and one open full-kernel blocker. The verdict
is `protocol_eligible_for_conditional_envelope_but_not_full_kernel_validated`.

The log-band prior deterministic mock-sanity suite is recorded in:

```text
data/source_manifest/kids1000_cosebis_log_band_prior_mock_sanity_policy_v1.csv
data/derived/kids1000_cosebis_log_band_prior_mock_sanity_v1_grid.csv
data/derived/kids1000_cosebis_log_band_prior_mock_sanity_v1_summary.csv
docs/kids1000_cosebis_log_band_prior_mock_sanity_v1.md
scripts/run_kids1000_cosebis_log_band_prior_mock_sanity_v1.py
scripts/validate_kids1000_cosebis_log_band_prior_mock_sanity_v1.py
```

This is a deterministic template-recovery sanity check, not physical mock
validation. It tests four synthetic truth families over the retained `15 x 20`
COSEBIs row structure: low log-band `n^-0.5`, flat coherent, high-mode `n`,
and oscillatory alternating. Each truth recovers its matching template. The
purpose is only to show that the protocol does not automatically classify every
deterministic pattern as low-mode. The suite uses no KiDS data-vector values, no
fit statistics, no random noise, and makes no endpoint-validation claim. Its
verdict is
`deterministic_template_recovery_pass_not_physical_mock_validation`.

The survey-native path-kernel derivation gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_survey_native_path_kernel_derivation_gate_policy_v1.csv
data/derived/kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.csv
data/derived/kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1_summary.csv
docs/kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.md
scripts/build_kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.py
scripts/validate_kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.py
```

This gate separates route support from full kernel derivation. The current
source route has a source-frozen mapping basis, a caveated full-route mask-load
path proxy, a source-side path-weight factorization rule, a source-frozen
theory-vector shell, and the deterministic template-recovery guardrail. These
are enough to make the route support concrete, but not enough to claim a
survey-native Tau Core lensing kernel. Three blockers remain explicit: a
survey-native operator from path observables to COSEBIs mode response, a
derivation of the log-band prior from that response spectrum, and a covariant or
survey-native lensing/path limit. The verdict is
`survey_native_path_route_available_but_mode_response_and_covariant_kernel_derivation_blocked`.

The COSEBIs mode-response operator specification is recorded in:

```text
data/source_manifest/kids1000_cosebis_mode_response_operator_spec_policy_v1.csv
data/derived/kids1000_cosebis_mode_response_operator_spec_v1.csv
data/derived/kids1000_cosebis_mode_response_operator_spec_v1_summary.csv
docs/kids1000_cosebis_mode_response_operator_spec_v1.md
scripts/build_kids1000_cosebis_mode_response_operator_spec_v1.py
scripts/validate_kids1000_cosebis_mode_response_operator_spec_v1.py
```

This artifact freezes what a future survey-native mode-response operator must
satisfy before the low-mode envelope can be promoted beyond a conditional
protocol carrier. It defines the path-observable domain, retained COSEBIs-row
codomain, linearity-before-amplitude rule, pair/redshift/path separation,
no-feedback constraint, gauge/mask null-safety requirement, and standard-lensing
null limit. It does not derive the operator. The verdict is
`operator_requirements_frozen_but_survey_native_mode_response_not_derived`.

The COSEBIs mode-response spectrum attempt is recorded in:

```text
data/source_manifest/kids1000_cosebis_mode_response_spectrum_attempt_policy_v1.csv
data/derived/kids1000_cosebis_mode_response_spectrum_attempt_v1.csv
data/derived/kids1000_cosebis_mode_response_spectrum_attempt_v1_spectra.csv
data/derived/kids1000_cosebis_mode_response_spectrum_attempt_v1_summary.csv
docs/kids1000_cosebis_mode_response_spectrum_attempt_v1.md
scripts/build_kids1000_cosebis_mode_response_spectrum_attempt_v1.py
scripts/validate_kids1000_cosebis_mode_response_spectrum_attempt_v1.py
```

This artifact keeps the spectrum-level argument conditional. Under the explicit
smooth coherent path/readout prior, constant power per logarithmic COSEBIs mode
band gives `P_n ~ 1/n` and coherent amplitude `M_n ~ n^-0.5`. The flat spectrum
is preserved as a boundary control, while high-mode and oscillatory spectra are
rejected only under that smooth-path prior. The mode-response operator and
operator-level gauge/null safety remain open blockers. The verdict is
`conditional_source_spectrum_attempt_preserves_operator_and_null_safety_blockers`.

The COSEBIs operator null-safety gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_operator_null_safety_gate_policy_v1.csv
data/derived/kids1000_cosebis_operator_null_safety_gate_v1.csv
data/derived/kids1000_cosebis_operator_null_safety_gate_v1_summary.csv
docs/kids1000_cosebis_operator_null_safety_gate_v1.md
scripts/build_kids1000_cosebis_operator_null_safety_gate_v1.py
scripts/validate_kids1000_cosebis_operator_null_safety_gate_v1.py
```

This artifact audits the remaining null-safety blocker at operator level. It
records that source-frozen null controls exist and have been replayed without
endpoint scores, that the domain/codomain route exists with a caveated
path/mask-load proxy, and that a uniform web route is accepted only as a null
control. It does not prove operator-level null safety. Three blockers remain:
pure-mask response, gauge/quotient descent, and coupling the conditional mode
spectrum to null transforms through one source-native operator. The verdict is
`null_controls_exist_but_operator_level_null_safety_remains_blocked`.

The COSEBIs pure-mask response gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_pure_mask_response_gate_policy_v1.csv
data/derived/kids1000_cosebis_pure_mask_response_gate_v1.csv
data/derived/kids1000_cosebis_pure_mask_response_gate_v1_summary.csv
data/derived/kids1000_cosebis_pure_mask_response_tile_basis_v1.csv
data/derived/kids1000_cosebis_pure_mask_response_domain_basis_v1.csv
docs/kids1000_cosebis_pure_mask_response_gate_v1.md
scripts/build_kids1000_cosebis_pure_mask_response_gate_v1.py
scripts/validate_kids1000_cosebis_pure_mask_response_gate_v1.py
```

This artifact narrows the pure-mask branch of the null-safety blocker. It
constructs a centered, unit-RMS, source-only pure-mask perturbation basis from
the full-route `F_overlap` and `D_path` mask observables, and lifts that basis
to the `58,800` target-by-route-tile domain. The centered basis has rank `2`.
It still does not construct a mapping vector, theory vector, prediction,
residual, fit statistic, or endpoint score. Quotient triviality and coupling to
the COSEBIs mode response remain open blockers. The verdict is
`pure_mask_basis_exists_but_quotient_triviality_and_mode_coupling_remain_blocked`.

The COSEBIs mask-mode leakage audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_mask_mode_leakage_audit_policy_v1.csv
data/derived/kids1000_cosebis_mask_mode_leakage_audit_v1.csv
data/derived/kids1000_cosebis_mask_mode_leakage_audit_v1_grid.csv
data/derived/kids1000_cosebis_mask_mode_leakage_audit_v1_summary.csv
docs/kids1000_cosebis_mask_mode_leakage_audit_v1.md
scripts/build_kids1000_cosebis_mask_mode_leakage_audit_v1.py
scripts/validate_kids1000_cosebis_mask_mode_leakage_audit_v1.py
```

This artifact audits a source-side leakage risk. The centered pure-mask basis
collapses to zero under uniform tile averaging, with
`max_uniform_collapse_norm` at numerical roundoff level. However, if a future
survey-native operator couples non-uniform mask amplitudes into a mode
envelope, mask-only leakage into the low-mode carrier is not yet ruled out.
The verdict is
`uniform_mask_collapse_is_null_but_nonuniform_operator_leakage_remains_open`.

The COSEBIs operator-leakage theorem requirements gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_operator_leakage_theorem_requirements_policy_v1.csv
data/derived/kids1000_cosebis_operator_leakage_theorem_requirements_v1.csv
data/derived/kids1000_cosebis_operator_leakage_theorem_requirements_v1_summary.csv
docs/kids1000_cosebis_operator_leakage_theorem_requirements_v1.md
scripts/build_kids1000_cosebis_operator_leakage_theorem_requirements_v1.py
scripts/validate_kids1000_cosebis_operator_leakage_theorem_requirements_v1.py
```

This artifact converts the mask-mode leakage audit into a frozen requirement
list for a future survey-native operator theorem. It records the uniform
tile-average null limit as a source-side limit, keeps the non-uniform leakage
risk open, freezes the pure-mask rejection/control-subspace requirement and the
mode-spectrum/null-coupling requirement, and leaves two explicit blockers:
operator leakage theorem and gauge/quotient descent. The verdict is
`requirements_frozen_for_operator_leakage_theorem_but_proof_remains_open`.

The COSEBIs gauge/quotient descent gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_gauge_quotient_descent_gate_policy_v1.csv
data/derived/kids1000_cosebis_gauge_quotient_descent_gate_v1.csv
data/derived/kids1000_cosebis_gauge_quotient_descent_gate_v1_summary.csv
docs/kids1000_cosebis_gauge_quotient_descent_gate_v1.md
scripts/build_kids1000_cosebis_gauge_quotient_descent_gate_v1.py
scripts/validate_kids1000_cosebis_gauge_quotient_descent_gate_v1.py
```

This artifact freezes the representation-invariance requirements for a future
survey-native path/readout operator. It records allowed representative changes,
the uniform mask-offset null limit, normalization and tile-relabeling
invariance requirements, and pure-mask control compatibility. It does not prove
gauge/quotient descent and does not construct the missing survey-native
operator. The verdict is
`gauge_quotient_descent_requirements_frozen_but_theorem_remains_open`.

The COSEBIs survey-native operator construction attempt is recorded in:

```text
data/source_manifest/kids1000_cosebis_survey_native_operator_construction_attempt_policy_v1.csv
data/derived/kids1000_cosebis_survey_native_operator_construction_attempt_v1.csv
data/derived/kids1000_cosebis_survey_native_operator_construction_attempt_v1_ledger.csv
data/derived/kids1000_cosebis_survey_native_operator_construction_attempt_v1_summary.csv
docs/kids1000_cosebis_survey_native_operator_construction_attempt_v1.md
scripts/build_kids1000_cosebis_survey_native_operator_construction_attempt_v1.py
scripts/validate_kids1000_cosebis_survey_native_operator_construction_attempt_v1.py
```

This artifact writes the first explicit source-side factorized operator
skeleton for the KiDS COSEBIs branch, \(K_i=M_iS_n\), using the frozen mapping
component and the conditional log-band mode-response weight. It is a
unit-amplitude source-side kernel, not a survey-native operator theorem and not
an endpoint prediction. Mask-leakage theorem, gauge/quotient descent, and
physical operator-unit derivation remain open. The verdict is
`factorized_source_side_operator_skeleton_exists_but_operator_theorem_remains_open`.

The COSEBIs physical operator-units gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_physical_operator_units_gate_policy_v1.csv
data/derived/kids1000_cosebis_physical_operator_units_gate_v1.csv
data/derived/kids1000_cosebis_physical_operator_units_gate_v1_summary.csv
docs/kids1000_cosebis_physical_operator_units_gate_v1.md
scripts/build_kids1000_cosebis_physical_operator_units_gate_v1.py
scripts/validate_kids1000_cosebis_physical_operator_units_gate_v1.py
```

This artifact records the unit and normalization blockers left by the
operator-skeleton attempt. The current \(K_i=M_iS_n\) kernel is identified as a
dimensionless unit-amplitude source-side object. The gate freezes the need for
physical response units, a source-side amplitude map, and a standard-lensing
null normalization before any physical COSEBIs prediction can be claimed. The
verdict is
`dimensionless_operator_kernel_identified_but_physical_units_and_amplitude_remain_open`.

The COSEBIs source-side amplitude-map attempt is recorded in:

```text
data/source_manifest/kids1000_cosebis_source_side_amplitude_map_attempt_policy_v1.csv
data/derived/kids1000_cosebis_source_side_amplitude_map_attempt_v1.csv
data/derived/kids1000_cosebis_source_side_amplitude_map_attempt_v1_ledger.csv
data/derived/kids1000_cosebis_source_side_amplitude_map_attempt_v1_summary.csv
docs/kids1000_cosebis_source_side_amplitude_map_attempt_v1.md
scripts/build_kids1000_cosebis_source_side_amplitude_map_attempt_v1.py
scripts/validate_kids1000_cosebis_source_side_amplitude_map_attempt_v1.py
```

This artifact freezes only the internal dimensionless source-normalized
amplitude map \(A_{\rm src}=1\) induced by the unit-mean `C_norm` rule and the
unit-mean operator skeleton. It removes an arbitrary source-side scale from the
current skeleton, but it does not derive physical COSEBIs response units, does
not calibrate an endpoint amplitude, and does not prove the standard-lensing
null amplitude. The verdict is
`dimensionless_source_amplitude_map_exists_but_physical_amplitude_remains_open`.

The COSEBIs physical-amplitude requirements gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_physical_amplitude_requirements_gate_policy_v1.csv
data/derived/kids1000_cosebis_physical_amplitude_requirements_gate_v1.csv
data/derived/kids1000_cosebis_physical_amplitude_requirements_gate_v1_summary.csv
docs/kids1000_cosebis_physical_amplitude_requirements_gate_v1.md
scripts/build_kids1000_cosebis_physical_amplitude_requirements_gate_v1.py
scripts/validate_kids1000_cosebis_physical_amplitude_requirements_gate_v1.py
```

This gate states what remains after \(A_{\rm src}=1\): a physical response
amplitude \(A_{\rm phys}\) would still need the missing COSEBIs response-unit
normalization and the standard-lensing/no-Tau-source null amplitude theorem.
The covariance metric is preserved as a future scoring metric but is explicitly
not used as an amplitude derivation. The verdict is
`dimensionless_source_amplitude_available_but_physical_response_amplitude_remains_open`.

The COSEBIs response-unit normalization requirements gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_response_unit_normalization_requirements_gate_policy_v1.csv
data/derived/kids1000_cosebis_response_unit_normalization_requirements_gate_v1.csv
data/derived/kids1000_cosebis_response_unit_normalization_requirements_gate_v1_summary.csv
docs/kids1000_cosebis_response_unit_normalization_requirements_gate_v1.md
scripts/build_kids1000_cosebis_response_unit_normalization_requirements_gate_v1.py
scripts/validate_kids1000_cosebis_response_unit_normalization_requirements_gate_v1.py
```

This gate freezes the requirements for mapping the dimensionless source kernel
and \(A_{\rm src}=1\) into COSEBIs response units. The 300-row COSEBIs domain,
dimensionless kernel/source amplitude, and covariance metric are available, but
the response-unit map itself remains open and must be compatible with the
standard-lensing/no-\(\tau\)-source null limit. The verdict is
`cosebis_response_unit_requirements_frozen_but_normalization_remains_open`.

The COSEBIs standard-lensing null-amplitude theorem-requirements gate is
recorded in:

```text
data/source_manifest/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_policy_v1.csv
data/derived/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.csv
data/derived/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1_summary.csv
docs/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.md
scripts/build_kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.py
scripts/validate_kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.py
```

This gate freezes the theorem requirements for the no-\(\tau\)-source limit:
source-replayed null controls are available only as controls, the zero-Tau
amplitude statement is specified but not derived, and operator null safety,
gauge/quotient descent, and non-uniform leakage control remain open blockers.
The verdict is
`standard_lensing_null_amplitude_requirements_frozen_but_theorem_remains_open`.

The COSEBIs physical-promotion blocker ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_physical_promotion_blocker_ledger_policy_v1.csv
data/derived/kids1000_cosebis_physical_promotion_blocker_ledger_v1.csv
data/derived/kids1000_cosebis_physical_promotion_blocker_ledger_v1_summary.csv
docs/kids1000_cosebis_physical_promotion_blocker_ledger_v1.md
scripts/build_kids1000_cosebis_physical_promotion_blocker_ledger_v1.py
scripts/validate_kids1000_cosebis_physical_promotion_blocker_ledger_v1.py
```

This ledger separates diagnostic endpoint readiness from physical promotion.
The diagnostic endpoint pipeline is ready, but physical promotion remains
blocked by five open requirements: survey-native operator theorem, operator
leakage theorem, gauge/quotient descent, response-unit normalization, and
standard-lensing/no-\(\tau\)-source null-amplitude theorem. The verdict is
`diagnostic_endpoint_ready_but_physical_promotion_blocked_by_five_open_requirements`.

The COSEBIs path-mapping source-preflight ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_mapping_source_preflight_policy_v1.csv
data/derived/kids1000_cosebis_path_mapping_source_preflight_v1.csv
data/derived/kids1000_cosebis_path_mapping_source_preflight_v1_summary.csv
docs/kids1000_cosebis_path_mapping_source_preflight_policy_v1.md
scripts/build_kids1000_cosebis_path_mapping_source_preflight_v1.py
scripts/validate_kids1000_cosebis_path_mapping_source_preflight_v1.py
```

It summarizes the current source-side state for a future path-aware COSEBIs
endpoint: target row structure, redshift kernels, the 196-tile route coordinate
index, the 300-row design skeleton, and the 58,800-row target-tile domain
skeleton are available; the path-weight construction rule is source-side
computable; the three-mask observable shell is preserved as a control; the
full-route `D_path` mask-load proxy is available but caveated; the positive
web-environment catalogue remains absent and is represented only by a null-web
control; and source-frozen null-control theory replay is available. It contains
no endpoint predictions, residuals, fit statistics, or scores.

The first COSEBIs null-control readiness policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_null_control_policy_v1.csv
data/derived/kids1000_cosebis_null_control_readiness_v1.csv
data/derived/kids1000_cosebis_null_control_readiness_v1_summary.csv
docs/kids1000_cosebis_null_control_policy_v1.md
scripts/build_kids1000_cosebis_null_control_readiness_v1.py
scripts/validate_kids1000_cosebis_null_control_readiness_v1.py
```

It declares four null-control families: sky rotation, tomographic-pair shuffle,
wrong-channel activation, and web/path sign flip. In this release these controls
are replayed only as source-frozen theory-vector digests, not as null scores.

The first COSEBIs null-control seed and multiplicity policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_null_control_seed_policy_v1.csv
data/derived/kids1000_cosebis_null_control_seed_inventory_v1.csv
data/derived/kids1000_cosebis_null_control_seed_inventory_v1_summary.csv
docs/kids1000_cosebis_null_control_seed_policy_v1.md
scripts/build_kids1000_cosebis_null_control_seed_inventory_v1.py
scripts/validate_kids1000_cosebis_null_control_seed_inventory_v1.py
```

It freezes deterministic family seeds and planned multiplicities for the four
future null-control families, totaling `1008` declared future control draws. It
does not execute controls and contains no control scores, predictions,
residuals, or fit statistics.

The first COSEBIs null-control theory replay is recorded in:

```text
data/source_manifest/kids1000_cosebis_null_control_theory_replay_policy_v1.csv
data/derived/kids1000_cosebis_null_control_theory_replay_v1.csv
data/derived/kids1000_cosebis_null_control_theory_replay_v1_summary.csv
docs/kids1000_cosebis_null_control_theory_replay_v1.md
scripts/build_kids1000_cosebis_null_control_theory_replay_v1.py
scripts/validate_kids1000_cosebis_null_control_theory_replay_v1.py
```

It applies the predeclared control transformations to the source-frozen
unit-amplitude theory-vector shell and stores compact vector digests and source
statistics for `1008` controls. It does not compare those controls to the KiDS
data vector and does not compute scores.

The first tiny pilot product freeze is recorded in:

```text
data/source_manifest/pilot_frozen_product_manifest.csv
docs/pilot_product_freeze_001.md
```

It freezes three public distance-side files for provenance and covariance-shape
testing only: one Cosmic Chronometers table, one Pantheon+ distance table, and
one Pantheon+ STAT+SYS covariance matrix. All rows remain
`endpoint_allowed=false`.

The first Pantheon+ endpoint-eligible scope declaration is recorded in:

```text
data/source_manifest/pantheon_endpoint_scope_v1.csv
data/derived/pantheon_scope_v1_summary.csv
docs/pantheon_endpoint_scope_v1.md
```

It freezes a residual-blind row rule and covariance-submatrix policy, but it is
still `SCOPE_FROZEN_NOT_SCORED`.

The first scoring grammar is frozen here:

```text
data/source_manifest/pantheon_scoring_protocol_v1.csv
docs/pantheon_scoring_protocol_v1.md
```

It declares the baseline family, nuisance policy, Tau activation family, and
required future controls. It also keeps endpoint `scoring_allowed=false`.

The dry-run design matrix is frozen here:

```text
data/source_manifest/pantheon_design_matrix_protocol_v1.csv
data/derived/pantheon_design_matrix_v1.csv
data/derived/pantheon_design_matrix_v1_summary.csv
docs/pantheon_design_matrix_v1.md
```

It contains source and activation-basis columns only. It contains no model
predictions, residuals, likelihoods, or fit statistics.

The first Pantheon+ numerical smoke test is recorded here:

```text
data/source_manifest/pantheon_pilot_scoring_v1.csv
data/derived/pantheon_pilot_scoring_v1_summary.csv
data/derived/pantheon_pilot_scoring_v1_grid.csv
docs/pantheon_pilot_scoring_v1.md
```

This is a diagonal-covariance pilot score, not endpoint validation. On the
current frozen grid, the Tau late-activation shell improves diagonal-covariance
\(\chi^2\) by only `0.084` relative to the flat-Lambda-CDM branch, while its
AIC is worse by `5.916` because the Tau shell carries more effective
parameters. This is therefore a reproducible scoring-pipeline smoke test, not
evidence for dark energy or for Tau Core cosmology.

The pilot diagnostic figure is generated reproducibly from the frozen grid:

```text
scripts/build_figures.py
figures/fig_pantheon_full_cov_pilot_branch_diagnostics.pdf
paper10_submission_source/figures/fig_pantheon_full_cov_pilot_branch_diagnostics.pdf
figures/fig_kids1000_cosebis_mode_localization.pdf
paper10_submission_source/figures/fig_kids1000_cosebis_mode_localization.pdf
```

The first full-covariance pilot repeats the same frozen branch grammar using
the retained Pantheon+ STAT+SYS covariance submatrix with Cholesky solves:

```text
data/source_manifest/pantheon_full_cov_pilot_scoring_v1.csv
data/derived/pantheon_full_cov_pilot_scoring_v1_summary.csv
data/derived/pantheon_full_cov_pilot_scoring_v1_grid.csv
docs/pantheon_full_cov_pilot_scoring_v1.md
```

It gives `Delta chi2 = -0.192` for the Tau shell relative to flat-Lambda-CDM,
but `Delta AIC = +5.808`. This preserves the same conclusion as the diagonal
smoke test: the scoring ladder works, but this is not evidence for a new
cosmological model.

The first two-channel full-covariance proxy pilot is:

```text
data/source_manifest/pantheon_void_web_proxy_full_cov_pilot_v1.csv
data/derived/pantheon_void_web_proxy_full_cov_pilot_v1_summary.csv
data/derived/pantheon_void_web_proxy_full_cov_pilot_v1_grid.csv
docs/pantheon_void_web_proxy_full_cov_pilot_v1.md
```

It activates only `W_VOID_MATURITY` and `W_WEB_ANISOTROPY`; `W_PATH_PROJECTION`
and `W_TIME_READOUT` remain disabled. Because no source-native void/web product
values are frozen yet, the current bases are leakage-safe redshift/scale-factor
proxies. This is a two-channel scoring-grammar stress test, not a void/web
detection. The current full-covariance distance-only proxy result is
`Delta chi2 = -0.05994162` and `Delta AIC = +3.94005838`, so it is
model-selection negative despite a tiny chi-square improvement.

The multi-probe full-covariance endpoint plan is recorded in:

```text
docs/multi_probe_full_cov_scoring_plan_v1.md
```

That future gate must combine distance, growth, lensing, and CMB-safety blocks.
It is not implemented in this scaffold.

## General Tau Core Readout Continuation

The weak full-covariance Pantheon+ pilot should be read primarily as a
limitation of the homogeneous late-activation shell, not as a true negative
against the broader Tau Core morphology/projection-readout framework. The
current pilot tests only one smooth proxy:

```text
W_tau(a)
```

The next step is not to import the galaxy TPG bridge itself. Rather, it is to
use the general Tau Core readout principle made explicit by the galactic bridge
discipline:
four-dimensional residuals may be readouts of deeper morphology/projection
channels. In cosmology this requires source-frozen channel families:

```text
W_void(a)          void maturity / distance activation
W_web(a,k,env)     cosmic-web anisotropy for growth and lensing
W_path(z,n_hat)    observer/path projection along the null-geodesic bundle
W_time(z,n_hat,env,path,phi_readout)
                   morphology-aware time/readout projection for observed a(t), H(t)
```

These channels must be frozen from independent source-side observables before
distance, growth, lensing, or CMB-safety residuals are scored.

The latest Tau Core theory-side readout packets sharpen the claim boundary for
this branch. A non-injective readout constrains a source class rather than a
unique source, so a positive `W_time` or `W_path` proxy would not by itself
identify a unique Tau-side time or path mechanism. Observer-dependent readouts
must also declare an embedded interface profile: position, scale, coupling,
protocol, resolution, channel access, and null model. Paper 10 therefore keeps
the CC and radial-BAO time/readout routes below endpoint status until a joint
interface/nuisance policy is source-frozen.

The current DESI shape/readout replay should be interpreted in the same
restricted way. It is positive but narrow: the frozen candidate score
`5.52425578108` exceeds the best frozen control score `5.50939872844` by
`0.01485705264`, while endpoint validation and physical validation remain
false. This is a source-strengthened, row-sensitive diagnostic, not a
validated cosmological result.

The main Paper 10 takeaway is therefore not a single-channel discovery claim.
It is a convergent multi-channel viability pattern: distance, lensing,
observer/path, and shape/time-readout routes each remain caveated, but together
they form a coherent source-frozen evidence pattern with low-tail,
control-surviving, or diagnostically constraining behavior. This may be
reported as pre-validation evidence, not empirical validation. The next
required test is a declared joint endpoint with shuffled-channel,
wrong-channel, and covariance-aware controls.

The existing-artifact cross-channel meta-score is recorded in:

```text
data/derived/joint_existing_artifact_meta_score_v1.csv
data/derived/joint_existing_artifact_meta_score_v1_summary.csv
docs/joint_existing_artifact_meta_score_v1.md
scripts/build_joint_existing_artifact_meta_score_v1.py
scripts/validate_joint_existing_artifact_meta_score_v1.py
```

It audits seven already frozen summary artifacts and returns
`MULTI_CHANNEL_VIABILITY_PATTERN_PRESENT_NOT_VALIDATION`, with three positive
caveated channels, two neutral/control-negative diagnostic channels, two
negative current-proxy channels, and net protocol weight `2.500`. These are
protocol weights, not physical likelihood weights.

The first executable joint-channel endpoint-candidate preflight is recorded in:

```text
data/source_manifest/joint_multichannel_endpoint_manifest_v1.csv
data/derived/joint_multichannel_endpoint_candidate_v1.csv
data/derived/joint_multichannel_endpoint_candidate_v1_summary.csv
docs/joint_multichannel_endpoint_candidate_v1.md
scripts/run_joint_multichannel_endpoint_candidate_v1.py
scripts/validate_joint_multichannel_endpoint_candidate_v1.py
```

It uses the same seven frozen channel summaries, predeclared metric transforms,
and no endpoint residual fields for label selection. With negative current-proxy
branches pulling the score downward, the normalized joint score is `0.200059110`
and the verdict is
`JOINT_ENDPOINT_CANDIDATE_INCONCLUSIVE_PREVALIDATION`. This is a positive-sign
combined preflight, not a joint endpoint pass and not cosmological validation.

The block-aware preflight adds sign-flip controls, seeded channel-weight
shuffles, and leave-one-channel stress:

```text
data/derived/joint_multichannel_block_score_v1.csv
data/derived/joint_multichannel_block_score_v1_controls.csv
data/derived/joint_multichannel_block_score_v1_leave_one_channel.csv
data/derived/joint_multichannel_block_score_v1_summary.csv
docs/joint_multichannel_block_score_v1.md
scripts/run_joint_multichannel_block_score_v1.py
scripts/validate_joint_multichannel_block_score_v1.py
```

It returns block-normalized score `0.413070369`, exact sign-flip
`p(score >= observed) = 0.375000000`, and leave-one positive `4/5`.
The missing leave-one pass occurs when the KiDS/COSEBIs lensing block is removed,
so the present joint pattern is positive but materially carried by that block.
The verdict is
`JOINT_BLOCK_SCORE_FRAGILE_OR_INCONCLUSIVE_PREVALIDATION`.

The direct non-lensing lift diagnostic is recorded in:

```text
data/derived/joint_non_lensing_lift_diagnostic_v1.csv
data/derived/joint_non_lensing_lift_diagnostic_v1_summary.csv
docs/joint_non_lensing_lift_diagnostic_v1.md
scripts/build_joint_non_lensing_lift_diagnostic_v1.py
scripts/validate_joint_non_lensing_lift_diagnostic_v1.py
```

It shows that the active non-lensing weighted sum is `-0.363118958`.
The non-lensing block therefore needs lift `0.363118958` to become positive, and
lift `1.113118958` to reach the illustrative protocol margin `0.25`. The
highest lift-priority channel is `observer_path_basis_low_z`. This diagnostic
does not authorize post-hoc retuning; it only identifies where independent
source-side work would most efficiently reduce KiDS/lensing dominance.

The observer/path strengthening gate is recorded in:

```text
data/derived/observer_path_strengthening_gate_v1.csv
data/derived/observer_path_strengthening_gate_v1_summary.csv
docs/observer_path_strengthening_gate_v1.md
scripts/build_observer_path_strengthening_gate_v1.py
scripts/validate_observer_path_strengthening_gate_v1.py
```

It keeps the current narrow `W_path_x_sky_x_x_zcenter` route as the accepted
source-frozen observer/path diagnostic, keeps centered sky-z as a control or
secondary route only, and blocks full metric/lensing path weighting until a
source-aligned numeric kappa/shear/mass-map product exists. In the current
12-object scope, `0/12` rows have such a source-aligned metric path product.

The next source-product blocker is packaged explicitly in:

```text
data/derived/observer_path_metric_product_requirements_package_v1_summary.csv
data/derived/observer_path_metric_product_requirements_package_v1_manifest.csv
data/derived/observer_path_metric_product_requirements_review_response_template_v1.csv
data/derived/observer_path_metric_product_requirements_package_v1.zip
docs/observer_path_metric_product_requirements_package_v1.md
docs/observer_path_metric_product_requirements_reviewer_instructions_v1.md
scripts/build_observer_path_metric_product_requirements_package_v1.py
scripts/validate_observer_path_metric_product_requirements_package_v1.py
```

This is a requirements-only external-review package. It asks what independent
source-aligned metric/path observable would be needed to reopen the physical
observer/path route: convergence, shear, mass-map integral, or a documented
metric-environment path weight. It preserves `endpoint_replay_allowed=false`
and `endpoint_validation_claimed=false`. The summary separates the active
observer/path scope (`12` rows) from the broader low-z route-audit universe
(`424` rows), and both currently have zero source-aligned numeric metric/path
products.

The completed external response is recorded in:

```text
data/derived/observer_path_metric_product_requirements_review_response_v1.csv
data/derived/observer_path_metric_product_requirements_review_completed_summary_v1.csv
data/derived/observer_path_metric_product_requirements_review_validation_log_v1.txt
docs/observer_path_metric_product_requirements_review_notes_v1.md
scripts/import_observer_path_metric_product_requirements_review_response_v1.py
scripts/validate_observer_path_metric_product_requirements_review_response_v1.py
```

The reviewer decision is `ACCEPT_REQUIREMENTS_ONLY` for all four review rows.
This strengthens the data-acquisition gate but does not provide the missing
metric/path product: `source_aligned_metric_product_count=0`,
`endpoint_replay_allowed=false`, and `physical_lensing_path_weight_claimed=false`
remain frozen.

After that requirements review, a first source-aligned caveated
metric-environment path product is built for the active observer/path scope:

```text
data/derived/observer_path_metric_environment_product_v1.csv
data/derived/observer_path_metric_environment_product_v1_summary.csv
docs/observer_path_metric_environment_product_v1.md
data/derived/observer_path_metric_product_acquisition_status_v1.csv
data/derived/observer_path_metric_product_acquisition_status_v1_summary.csv
docs/observer_path_metric_product_acquisition_status_v1.md
scripts/build_observer_path_metric_environment_product_v1.py
scripts/validate_observer_path_metric_environment_product_v1.py
scripts/build_observer_path_metric_product_acquisition_status_v1.py
scripts/validate_observer_path_metric_product_acquisition_status_v1.py
```

This uses existing source-side path-aware void geometry, line-of-sight radial
profile, and directional-web anisotropy artifacts to provide a numeric
`caveated_metric_environment_path_proxy` for `12/12` active observer/path rows.
It changes the data status from no source-aligned metric/path observable to a
caveated metric-environment observable. It still does not provide kappa, shear,
or a mass-map integral, so the physical lensing-path branch remains blocked and
any endpoint use requires a separate replay-authorization gate.

A focused preauthorization diagnostic screen is then run in:

```text
data/derived/observer_path_metric_environment_fast_screen_v1_grid.csv
data/derived/observer_path_metric_environment_fast_screen_v1_family_summary.csv
data/derived/observer_path_metric_environment_fast_screen_v1_summary.csv
docs/observer_path_metric_environment_fast_screen_v1.md
scripts/run_observer_path_metric_environment_fast_screen_v1.py
scripts/validate_observer_path_metric_environment_fast_screen_v1.py
```

The best candidate is `metric_environment_path`. It improves the 12-row
baseline by `Delta chi2 = -0.55793885392`, but it does not survive local
family controls: `Delta chi2(candidate - best control) = 0.12520399356`. The
verdict is
`METRIC_ENVIRONMENT_PREAUTH_SIGNAL_NOT_CONTROL_RESISTANT_NOT_ENDPOINT`. This is
preserved as a useful negative/control result: the new source-aligned product is
informative, but the current formula is not ready for replay promotion.

The follow-up source-side ordering diagnostic is:

```text
data/derived/observer_path_metric_environment_ordering_diagnostic_v1.csv
data/derived/observer_path_metric_environment_ordering_diagnostic_v1_pairwise.csv
data/derived/observer_path_metric_environment_ordering_diagnostic_v1_summary.csv
docs/observer_path_metric_environment_ordering_diagnostic_v1.md
scripts/build_observer_path_metric_environment_ordering_diagnostic_v1.py
scripts/validate_observer_path_metric_environment_ordering_diagnostic_v1.py
```

It preserves the failure mode rather than hiding it: the best local control is
still `rank_reverse`, and the candidate-minus-best-control gap remains
`0.12520399356`. The source-side product is not simply a redshift proxy
(`Spearman(metric environment, zHD) = -0.195804195804`) and is not simply the
older `W_path` proxy (`Spearman(metric environment, W_path) = -0.048951048951`),
but its ordering is still not control-resistant. The next honest step is
therefore a source-native ordering rule for the metric-environment path kernel,
frozen before any replay scoring, not endpoint promotion of the current proxy.

That source-native ordering bank is now built and screened:

```text
data/derived/observer_path_source_native_ordering_kernel_v1.csv
data/derived/observer_path_source_native_ordering_kernel_v1_summary.csv
docs/observer_path_source_native_ordering_kernel_v1.md
data/derived/observer_path_source_native_ordering_fast_screen_v1_grid.csv
data/derived/observer_path_source_native_ordering_fast_screen_v1_family_summary.csv
data/derived/observer_path_source_native_ordering_fast_screen_v1_summary.csv
docs/observer_path_source_native_ordering_fast_screen_v1.md
scripts/build_observer_path_source_native_ordering_kernel_v1.py
scripts/validate_observer_path_source_native_ordering_kernel_v1.py
scripts/run_observer_path_source_native_ordering_fast_screen_v1.py
scripts/validate_observer_path_source_native_ordering_fast_screen_v1.py
```

The result is preserved as another useful negative/control result. The best
source-native ordering candidate is `K_order_void_web_los_balanced`; it improves
the baseline by `Delta chi2 = -0.16922377119`, but it does not survive controls:
`Delta chi2(candidate - best control) = 0.07467294067`. This means that simply
combining the available void, web, LOS, and observer-basis source proxies is not
yet enough. A stronger next route needs either a genuinely source-native path
metric/lensing observable or a more physically justified ordering rule, frozen
before any endpoint replay.

The route is therefore closed by an explicit next-action gate:

```text
data/derived/observer_path_metric_lensing_next_gate_v1.csv
data/derived/observer_path_metric_lensing_next_gate_v1_summary.csv
docs/observer_path_metric_lensing_next_gate_v1.md
scripts/build_observer_path_metric_lensing_next_gate_v1.py
scripts/validate_observer_path_metric_lensing_next_gate_v1.py
```

The gate verdict is
`ACT_DR6_PATH_WEIGHT_CANDIDATE_READY_BUT_REVIEW_BLOCKS_REPLAY`. It records:
`caveated_metric_environment_proxy_available=true`,
`act_dr6_source_side_kappa_sampling_available=true`,
`act_dr6_source_frozen_path_weight_candidate_available=true`,
`act_dr6_mask_positive_rows=168`,
`physical_metric_lensing_path_product_available=false`,
`metric_environment_screen_survives_controls=false`,
`source_native_ordering_screen_survives_controls=false`, and
`endpoint_replay_allowed=false`. The next required action is not another
combination search; it is external review and replay authorization for the ACT
path-weight candidate, including explicit null-control handling, before any
endpoint scoring.
The external-review handoff package is now built at
`data/derived/act_dr6_lensing_path_weight_replay_authorization_review_package_v1.zip`
with checksum
`8594b1cd9e967836b9c7238834619e558f176ad888c70de15fc067e8d6ec676d`.
It contains the response template, candidate summaries, gate ledger, docs, and
relevant scripts, but it remains `review_completed=false` and
`endpoint_replay_allowed=false`.
A completed reviewer response can be checked with
`scripts/validate_act_dr6_lensing_path_weight_replay_authorization_review_response_v1.py`
or imported with
`scripts/import_act_dr6_lensing_path_weight_replay_authorization_review_response_v1.py`.
Even an accepted response only authorizes a separate caveated replay; it does
not turn the package into validation and does not claim a physical lensing
path-weight derivation.
A guarded replay run template is also frozen at
`data/source_manifest/act_dr6_lensing_path_weight_replay_run_template_v1.csv`.
It fixes the candidate basis, authorization-summary dependency, grid, six
mandatory controls (`off`, `wrong_sign`, `curl_null`, `diff_f150_f090_null`,
`deterministic_shuffle`, `rank_reverse`), and forbidden-input markers. The
template remains `ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_PREPARED_AUTH_REQUIRED_NOT_VALIDATION`.
The guarded runner/validator pair is prepared in
`scripts/run_act_dr6_lensing_path_weight_authorized_replay_v1.py` and
`scripts/validate_act_dr6_lensing_path_weight_authorized_replay_v1.py`. A
completed external response now authorizes only a caveated permission-only
replay, not validation or a physical path-weight claim. The guarded replay
reports `candidate_best_chi2_act_path=380.575996101` versus
`baseline_best_chi2_act_path=381.794196616`, but the best null control is
`curl_null` with `best_control_chi2_act_path=379.334896969`. The recorded verdict
is therefore
`act_dr6_lensing_path_weight_candidate_not_control_resistant_permission_only_not_validation`.
This is a preserved negative/control-dominance result for the present ACT
unitless path-weight candidate. A follow-up diagnostic is recorded in
`data/derived/act_dr6_lensing_path_weight_control_dominance_diagnostic_v1_summary.csv`:
the candidate improves over baseline but loses to null/order controls, so the
present ACT vector is a weak, non-specific source-side signal rather than a
promotable observer/path metric-lensing readout.

Paper 10 also does not test a Tau base-substrate or dark-sector response layer.
Narrow or weak signals in this repository may indicate an incomplete channel
basis, but they do not identify the missing channel as dark-sector response.
That question belongs to a separate source-frozen `M0/M1/M2` decision protocol:
no-dark Tau readout versus Tau base-substrate response versus a standard
dark-sector benchmark.

## Joint guarded replay status

The joint guarded replay execution authorization response has been imported and
validated:

`data/derived/joint_guarded_replay_execution_authorization_response_v1_summary.csv`

It authorizes exactly one permission-only guarded replay while keeping endpoint
validation, cosmological validation, and physical validation false. The replay
has now been run and validated:

`data/derived/joint_guarded_replay_permission_only_summary_v1.csv`

The active-block ledger is:

`data/derived/joint_guarded_replay_permission_only_grid_v1.csv`

Summary:

- active blocks: `3`
- positive or caveated support blocks: `3`
- KiDS/COSEBIs low-mode: caveated low-tail support
- observer/path low-z: candidate beats the best control in the permission-only
  statistic
- DESI shape/readout: candidate exceeds controls in the source-native shape
  score

This is a permission-only joint replay, not endpoint validation, not
cosmological validation, and not physical proof. The claim boundary is:

`joint_guarded_replay_permission_only_not_validation`

The post-replay promotion-readiness gate is recorded in:

`data/derived/joint_permission_replay_promotion_readiness_gate_v1_summary.csv`

It preserves the positive permission-only signal while blocking promotion:

- clean control-resistant blocks: `2`
- caveated support blocks: `1`
- negative blocks: `0`
- hard blockers open: `3`
- promotion ready for validation protocol: `false`

The blockers are: the caveated KiDS/COSEBIs support block, incomplete
cross-probe covariance or surrogate closure, and the missing same-statistic
matched-control implementation. Verdict:

`JOINT_PERMISSION_REPLAY_POSITIVE_BUT_PROMOTION_BLOCKED_NOT_VALIDATION`

The first blocker is now expanded into a concrete KiDS caveat-resolution plan:

`data/derived/joint_kids_caveated_block_resolution_plan_v1_summary.csv`

It preserves the KiDS low-tail signal but keeps the block caveated until the
physical-promotion proof chain is closed. Frozen order:

1. operator leakage theorem,
2. gauge quotient descent,
3. response unit normalization,
4. standard-lensing null-amplitude theorem,
5. survey-native operator theorem.

This plan computes no new scores and makes no validation claim. Verdict:

`KIDS_JOINT_BLOCK_HAS_SIGNAL_BUT_CAVEAT_RESOLUTION_REQUIRES_PHYSICAL_PROMOTION_PROOFS`

The plan is now post-synthesis aware: each resolution row cites the latest
closure-attempt summary for its blocker, and the B1 row cites the survey-native
operator theorem synthesis artifact rather than only the earlier source-side
skeleton. The B1 state is therefore explicit: `operator_skeleton_constructed=true`
but `operator_theorem_proven=false`.

The rank-1 KiDS proof blocker is narrowed further here:

```text
data/derived/kids1000_cosebis_operator_leakage_closure_attempt_v1.csv
data/derived/kids1000_cosebis_operator_leakage_closure_attempt_v1_summary.csv
docs/kids1000_cosebis_operator_leakage_closure_attempt_v1.md
scripts/build_kids1000_cosebis_operator_leakage_closure_attempt_v1.py
scripts/validate_kids1000_cosebis_operator_leakage_closure_attempt_v1.py
```

This artifact states the minimal operator-level closure target: every
admissible mask-only direction must either vanish in the physical quotient or
be routed to the frozen null-control family under the same statistic and
covariance discipline, while the same operator also recovers the uniform
pure-mask null limit and descends through gauge/quotient representations. The
current verdict is
`OPERATOR_LEAKAGE_CLOSURE_ATTEMPT_NARROWS_PROOF_BUT_THEOREM_REMAINS_OPEN`.
It computes no new score, uses no KiDS data-vector values, and leaves the KiDS
block caveated.

The parallel gauge/quotient descent blocker is narrowed here:

```text
data/derived/kids1000_cosebis_gauge_quotient_descent_closure_attempt_v1.csv
data/derived/kids1000_cosebis_gauge_quotient_descent_closure_attempt_v1_summary.csv
docs/kids1000_cosebis_gauge_quotient_descent_closure_attempt_v1.md
scripts/build_kids1000_cosebis_gauge_quotient_descent_closure_attempt_v1.py
scripts/validate_kids1000_cosebis_gauge_quotient_descent_closure_attempt_v1.py
```

This artifact states the minimal descent target: source representatives related
by tile relabeling, source-basis recentering, admissible normalization changes,
or gauge/null transformations must produce the same physical quotient class
under the future survey-native operator. It preserves the uniform mask-offset
limit but leaves normalization invariance, tile-relabeling invariance,
pure-mask control compatibility, and the single-operator dependency open. The
verdict is
`GAUGE_QUOTIENT_DESCENT_CLOSURE_ATTEMPT_NARROWS_PROOF_BUT_THEOREM_REMAINS_OPEN`.

The response-unit normalization blocker is narrowed here:

```text
data/derived/kids1000_cosebis_response_unit_normalization_closure_attempt_v1.csv
data/derived/kids1000_cosebis_response_unit_normalization_closure_attempt_v1_summary.csv
docs/kids1000_cosebis_response_unit_normalization_closure_attempt_v1.md
scripts/build_kids1000_cosebis_response_unit_normalization_closure_attempt_v1.py
scripts/validate_kids1000_cosebis_response_unit_normalization_closure_attempt_v1.py
```

This artifact separates three facts that must not be conflated: the retained
300-row COSEBIs codomain is available, the current source-side kernel is
dimensionless, and the covariance metric is available for later scoring but is
not a response-unit derivation. The missing theorem is a source-side or
theory-side map from the dimensionless `A_src K_i` object into COSEBIs response
units, compatible with the standard-lensing/no-Tau-source null limit and with
the still-open leakage and gauge/quotient gates. The verdict is
`RESPONSE_UNIT_NORMALIZATION_CLOSURE_ATTEMPT_NARROWS_PROOF_BUT_UNITS_REMAIN_OPEN`.

The standard-lensing null-amplitude blocker is narrowed here:

```text
data/derived/kids1000_cosebis_standard_lensing_null_amplitude_closure_attempt_v1.csv
data/derived/kids1000_cosebis_standard_lensing_null_amplitude_closure_attempt_v1_summary.csv
docs/kids1000_cosebis_standard_lensing_null_amplitude_closure_attempt_v1.md
scripts/build_kids1000_cosebis_standard_lensing_null_amplitude_closure_attempt_v1.py
scripts/validate_kids1000_cosebis_standard_lensing_null_amplitude_closure_attempt_v1.py
```

This artifact preserves the distinction between having source-replayed null
controls and proving a physical no-Tau-source theorem. Null controls are
available only as control limits; the zero-Tau-source amplitude statement is
specified but not derived. The physical theorem remains blocked by operator
null safety, response-unit normalization, leakage control, and gauge/quotient
descent. The verdict is
`STANDARD_LENSING_NULL_AMPLITUDE_CLOSURE_ATTEMPT_NARROWS_PROOF_BUT_THEOREM_REMAINS_OPEN`.

The survey-native operator theorem blocker is then synthesized here:

```text
data/derived/kids1000_cosebis_survey_native_operator_theorem_closure_attempt_v1.csv
data/derived/kids1000_cosebis_survey_native_operator_theorem_closure_attempt_v1_summary.csv
docs/kids1000_cosebis_survey_native_operator_theorem_closure_attempt_v1.md
scripts/build_kids1000_cosebis_survey_native_operator_theorem_closure_attempt_v1.py
scripts/validate_kids1000_cosebis_survey_native_operator_theorem_closure_attempt_v1.py
```

This artifact is the B1 synthesis gate. It records that a factorized
source-side operator skeleton exists, but that a physical survey-native
operator theorem requires one and the same operator to pass leakage,
gauge/quotient descent, response-unit normalization, and standard-lensing
null-amplitude conditions. Since those B2--B5 conditions remain open, the KiDS
block cannot yet be promoted to clean joint support. The verdict is
`SURVEY_NATIVE_OPERATOR_THEOREM_SYNTHESIS_HAS_SOURCE_SKELETON_BUT_PROOF_CHAIN_REMAINS_OPEN`.

The covariance blocker is also expanded into a concrete route plan:

`data/derived/joint_covariance_resolution_plan_v1_summary.csv`

Allowed routes:

1. source-native/source-frozen cross-probe covariance product,
2. caveated block-diagonal surrogate,
3. same-statistic matched-control binding under the chosen covariance route.

The fastest currently documented route is the caveated block-diagonal surrogate
plus same-statistic controls, but this remains non-validation and non-scoring.
Verdict:

`COVARIANCE_RESOLUTION_ROUTES_FROZEN_CROSS_PROBE_STILL_OPEN_NOT_SCORING`

The matched-control blocker is expanded here:

`data/derived/joint_matched_control_resolution_plan_v1_summary.csv`

It freezes eight required control families under the same future statistic and
same covariance route as the candidate:

1. `shuffled_channel_labels`
2. `wrong_channel_or_wrong_family_controls`
3. `sign_flip_controls`
4. `leave_one_probe_or_block_drop`
5. `null_readout_controls`
6. `scope_and_forbidden_input_controls`
7. `single_statistic_binding`
8. `covariance_binding`

Six are planned but not implemented; two remain blocked by upstream
statistic/covariance gates. Verdict:

`MATCHED_CONTROL_RESOLUTION_PLAN_FROZEN_IMPLEMENTATION_BLOCKED_NOT_SCORING`

The matched-control implementation-readiness ledger is recorded in:

```text
data/derived/joint_matched_control_implementation_readiness_v1.csv
data/derived/joint_matched_control_implementation_readiness_v1_summary.csv
docs/joint_matched_control_implementation_readiness_v1.md
scripts/build_joint_matched_control_implementation_readiness_v1.py
scripts/validate_joint_matched_control_implementation_readiness_v1.py
```

It separates design readiness from executable validation. Six control families
have source-side implementation scaffolds but remain blocked by the missing
single-statistic/covariance binding; two families remain upstream-blocked. The
verdict is
`MATCHED_CONTROL_IMPLEMENTATION_READINESS_HAS_DESIGNS_BUT_PROTOCOL_BINDING_BLOCKED`.

The symbolic single-statistic protocol shell is recorded in:

```text
data/derived/joint_single_statistic_protocol_shell_v1.csv
data/derived/joint_single_statistic_protocol_shell_v1_summary.csv
docs/joint_single_statistic_protocol_shell_v1.md
scripts/build_joint_single_statistic_protocol_shell_v1.py
scripts/validate_joint_single_statistic_protocol_shell_v1.py
```

It freezes the future shared statistic form as `T_joint = sum_i q_i z_i`, where
each channel contributes a signed standardized response. This is only a
symbolic shell: `single_joint_statistic_defined=false`, `protocol_executable=false`,
and no endpoint scoring is allowed until the covariance route and matched
controls are frozen together.

The same-statistic replay authorization package is recorded in:

```text
data/derived/joint_same_statistic_replay_authorization_package_v1.zip
data/derived/joint_same_statistic_replay_authorization_package_v1_summary.csv
data/derived/joint_same_statistic_replay_authorization_response_template_v1.csv
docs/joint_same_statistic_replay_authorization_package_v1.md
scripts/build_joint_same_statistic_replay_authorization_package_v1.py
scripts/validate_joint_same_statistic_replay_authorization_package_v1.py
```

This is a reviewer handoff package, not a replay. It asks whether a later
guarded permission-only replay package may use the symbolic `T_joint` shell
under the caveated block-diagonal covariance route and matched-control
readiness boundary. Direct scoring remains forbidden:
`permission_only_replay_package_allowed=false` and `direct_scoring_allowed=false`.

Completed reviewer responses for this package must be imported through:

```text
scripts/import_joint_same_statistic_replay_authorization_response_v1.py
scripts/validate_joint_same_statistic_replay_authorization_response_v1.py
```

The importer rejects incomplete templates and responses that allow direct
scoring, endpoint validation, cosmological validation, forbidden inputs, or
post-score control feedback. The completed canonical response is now recorded
in:

```text
data/derived/joint_same_statistic_replay_authorization_response_v1.csv
data/derived/joint_same_statistic_replay_authorization_response_v1_summary.csv
```

Its decision is:

`AUTHORIZE_SAME_STATISTIC_GUARDED_PERMISSION_REPLAY_PACKAGE_NOT_SCORING_NOT_VALIDATION`

The resulting same-statistic guarded permission package is recorded in:

```text
data/source_manifest/joint_same_statistic_guarded_permission_replay_policy_v1.csv
data/derived/joint_same_statistic_guarded_permission_replay_package_v1.zip
data/derived/joint_same_statistic_guarded_permission_replay_package_v1_summary.csv
data/derived/joint_same_statistic_guarded_permission_replay_package_v1_manifest.csv
docs/joint_same_statistic_guarded_permission_replay_package_v1.md
scripts/build_joint_same_statistic_guarded_permission_replay_package_v1.py
scripts/validate_joint_same_statistic_guarded_permission_replay_package_v1.py
```

This package freezes the same symbolic statistic and matched-control boundary
for a later replay gate. It is still not execution, not scoring, not endpoint
validation, and not cosmological validation:
`direct_execution_allowed=false` and `endpoint_scoring_allowed=false`.

The next same-statistic execution authorization handoff is recorded in:

```text
data/source_manifest/joint_same_statistic_execution_authorization_policy_v1.csv
data/derived/joint_same_statistic_execution_authorization_response_template_v1.csv
data/derived/joint_same_statistic_execution_authorization_package_v1.zip
data/derived/joint_same_statistic_execution_authorization_package_v1_summary.csv
data/derived/joint_same_statistic_execution_authorization_package_v1_manifest.csv
docs/joint_same_statistic_execution_authorization_package_v1.md
scripts/build_joint_same_statistic_execution_authorization_package_v1.py
scripts/validate_joint_same_statistic_execution_authorization_package_v1.py
```

This is an external reviewer handoff for one possible permission-only
execution. It is not pre-authorized and does not execute anything:
`review_completed=false` and `permission_only_execution_allowed=false`.

Completed reviewer responses for this execution package must be imported
through:

```text
scripts/import_joint_same_statistic_execution_authorization_response_v1.py
scripts/validate_joint_same_statistic_execution_authorization_response_v1.py
```

The importer rejects incomplete templates and responses that use forbidden
inputs or claim endpoint, cosmological, or physical validation. A positive
response may only authorize one permission-only execution.

The completed same-statistic execution response has now been imported and
authorizes one permission-only execution:

```text
data/derived/joint_same_statistic_execution_authorization_response_v1.csv
data/derived/joint_same_statistic_execution_authorization_response_v1_summary.csv
```

Decision:

`AUTHORIZE_SAME_STATISTIC_PERMISSION_ONLY_EXECUTION_NOT_VALIDATION`

The permission-only replay has been run and validated under the same-statistic
boundary:

```text
data/derived/joint_guarded_replay_permission_only_grid_v1.csv
data/derived/joint_guarded_replay_permission_only_summary_v1.csv
docs/joint_guarded_replay_permission_only_v1.md
```

The replay records three active blocks, with all three positive or caveated
positive under their local permission-only diagnostics:

- KiDS/COSEBIs low mode: caveated support.
- observer/path low-z: candidate beats the best control.
- DESI shape/time readout: candidate exceeds the best control.

This is still not endpoint validation, not cosmological validation, and not
physical validation.

The same-statistic binding status is now split into symbolic and executable
levels:

```text
data/derived/joint_symbolic_statistic_binding_status_v1.csv
data/derived/joint_symbolic_statistic_binding_status_v1_summary.csv
docs/joint_symbolic_statistic_binding_status_v1.md
scripts/build_joint_symbolic_statistic_binding_status_v1.py
scripts/validate_joint_symbolic_statistic_binding_status_v1.py
```

Verdict:

`SYMBOLIC_SAME_STATISTIC_BINDING_PASSED_NUMERIC_VALIDATION_BINDING_BLOCKED`

This records that the symbolic shared-statistic condition has passed, while a
numeric executable validation statistic and cross-probe covariance closure
remain blocked.

The first same-statistic matched-control artifact is now available as a
symbolic, non-scoring sign-flip enumeration:

```text
data/derived/joint_control_sign_flip_symbolic_v1.csv
data/derived/joint_control_sign_flip_symbolic_v1_summary.csv
docs/joint_control_sign_flip_symbolic_v1.md
scripts/build_joint_control_sign_flip_symbolic_v1.py
scripts/validate_joint_control_sign_flip_symbolic_v1.py
```

It enumerates all seven nontrivial sign-flip controls for the three active
channels under the shared symbolic statistic. It does not compute a numeric
statistic and does not authorize scoring or validation.

The second same-statistic matched-control artifact is now available as a
symbolic, non-scoring block-drop / leave-one-probe enumeration:

```text
data/derived/joint_control_block_drop_symbolic_v1.csv
data/derived/joint_control_block_drop_symbolic_v1_summary.csv
docs/joint_control_block_drop_symbolic_v1.md
scripts/build_joint_control_block_drop_symbolic_v1.py
scripts/validate_joint_control_block_drop_symbolic_v1.py
```

It enumerates all seven nontrivial block-drop controls for the three active
channels under the shared symbolic statistic, including leave-one,
all-but-one, and all-drop/null controls. It does not compute a numeric
statistic and does not authorize scoring or validation.

The current same-statistic matched-control coverage status is recorded in:

```text
data/derived/joint_same_statistic_control_coverage_status_v1.csv
data/derived/joint_same_statistic_control_coverage_status_v1_summary.csv
docs/joint_same_statistic_control_coverage_status_v1.md
scripts/build_joint_same_statistic_control_coverage_status_v1.py
scripts/validate_joint_same_statistic_control_coverage_status_v1.py
```

This ledger records two symbolically complete control families, one
symbolically partial null-control family, and three design-ready but
numeric-blocked control families. It preserves the current boundary:
same-statistic control coverage has progressed, but numeric `T_joint`,
cross-probe covariance closure, endpoint scoring, and validation remain
blocked.

The numeric `T_joint` promotion gate is recorded in:

```text
data/derived/joint_numeric_t_joint_promotion_gate_v1.csv
data/derived/joint_numeric_t_joint_promotion_gate_v1_summary.csv
docs/joint_numeric_t_joint_promotion_gate_v1.md
scripts/build_joint_numeric_t_joint_promotion_gate_v1.py
scripts/validate_joint_numeric_t_joint_promotion_gate_v1.py
```

This gate records four passed symbolic prerequisites and four remaining
numeric blockers: numeric channel `z_i` binding, numeric matched-control
execution under the same `T_joint`, cross-probe covariance closure, and a
separate validation authorization package. It does not compute the statistic
and does not authorize endpoint scoring.

The channel-level numeric `z_i` binding audit is recorded in:

```text
data/derived/joint_numeric_channel_zi_binding_audit_v1.csv
data/derived/joint_numeric_channel_zi_binding_audit_v1_summary.csv
docs/joint_numeric_channel_zi_binding_audit_v1.md
scripts/build_joint_numeric_channel_zi_binding_audit_v1.py
scripts/validate_joint_numeric_channel_zi_binding_audit_v1.py
```

This audit identifies candidate numeric source fields for all three active
channels, but it deliberately leaves `z_i` undefined. The remaining blocker is
a shared signed-standardization rule that must apply to candidate and controls
before numeric `T_joint` scoring can be considered.

The shared signed `z_i` standardization protocol is recorded in:

```text
data/derived/joint_signed_zi_standardization_protocol_v1.csv
data/derived/joint_signed_zi_standardization_protocol_v1_summary.csv
docs/joint_signed_zi_standardization_protocol_v1.md
scripts/build_joint_signed_zi_standardization_protocol_v1.py
scripts/validate_joint_signed_zi_standardization_protocol_v1.py
```

The protocol freezes the support-positive sign convention and the future
standardization rule:

```text
e_i = sign_i * native_value
center_i = median(e_i over matched controls only)
scale_i = MAD1.4826(e_i over matched controls only)
z_i = (e_i - center_i) / scale_i
```

Candidate values are not allowed to define the center or scale. If the matched
control scale is unavailable or zero, the channel remains blocked rather than
being rescued by a fitted normalization. This artifact still does not compute
`z_i`, `T_joint`, endpoint scoring, or validation.

The matched-control distribution readiness audit is recorded in:

```text
data/derived/joint_matched_control_distribution_readiness_v1.csv
data/derived/joint_matched_control_distribution_readiness_v1_summary.csv
docs/joint_matched_control_distribution_readiness_v1.md
scripts/build_joint_matched_control_distribution_readiness_v1.py
scripts/validate_joint_matched_control_distribution_readiness_v1.py
```

This audit checks whether the repository currently exposes the raw
matched-control distributions needed by the frozen median/MAD rule. The
current status is available but caveated: the observer/path channel is ready
for a future distribution build, the KiDS channel exposes the full 1008-row
null-control distribution but only as endpoint-score-not-validation material,
and the DESI shape/time channel is caveated-ready with a small control set. No
center, scale, `z_i`, or `T_joint` is computed.

The numeric `z_i` distribution-build authorization package is recorded in:

```text
data/source_manifest/joint_numeric_zi_distribution_build_authorization_policy_v1.csv
data/derived/joint_numeric_zi_distribution_build_authorization_response_template_v1.csv
data/derived/joint_numeric_zi_distribution_build_authorization_package_v1.zip
data/derived/joint_numeric_zi_distribution_build_authorization_package_v1.zip.sha256
data/derived/joint_numeric_zi_distribution_build_authorization_package_v1_manifest.csv
data/derived/joint_numeric_zi_distribution_build_authorization_package_v1_summary.csv
docs/joint_numeric_zi_distribution_build_authorization_package_v1.md
scripts/build_joint_numeric_zi_distribution_build_authorization_package_v1.py
scripts/validate_joint_numeric_zi_distribution_build_authorization_package_v1.py
```

This package asks an external reviewer whether a numeric channel-level `z_i`
distribution build may be prepared from the frozen signed standardization
protocol and currently exposed matched-control distributions. It is prepared
but not completed; it does not authorize `T_joint`, endpoint scoring, or
validation.

The current numeric `z_i` distribution-build blocker status is recorded in:

```text
data/derived/joint_numeric_zi_distribution_build_blocker_status_v1.csv
data/derived/joint_numeric_zi_distribution_build_blocker_status_v1_summary.csv
docs/joint_numeric_zi_distribution_build_blocker_status_v1.md
scripts/build_joint_numeric_zi_distribution_build_blocker_status_v1.py
scripts/validate_joint_numeric_zi_distribution_build_blocker_status_v1.py
```

Current blocker:

`numeric_zi_distribution_build_authorization_response_missing`

The next required action is to obtain and validate a completed reviewer
response. Until then, no `z_i`, `T_joint`, endpoint scoring, or validation is
authorized.

A completed reviewer response can be imported and validated with:

```bash
python scripts/import_joint_numeric_zi_distribution_build_authorization_response_v1.py \
  /path/to/completed_reviewer_response.csv
python scripts/build_joint_numeric_zi_distribution_build_blocker_status_v1.py
python scripts/validate_joint_numeric_zi_distribution_build_blocker_status_v1.py
```

The importer also accepts a zip containing exactly one matching response CSV.
Accepted responses only authorize a numeric channel-level `z_i` distribution
ledger. They do not authorize `T_joint`, endpoint scoring, cosmological
validation, or physical validation.

The accepting reviewer responses are exact-string gated. The short internal
tokens are:
`authorize_distribution_build`,
`accept_caveated_distribution_boundary`,
`accept_frozen_center_scale_rule`, and
`accept_no_t_joint_promotion`.
The accepted external-reviewer aliases are:
`AUTHORIZE_NUMERIC_ZI_DISTRIBUTION_BUILD_ONLY_NOT_TJOINT`,
`ACCEPT_CAVEATED_DISTRIBUTION_BOUNDARY`,
`ACCEPT_FROZEN_MEDIAN_MAD_CONTROL_ONLY_RULE`, and
`ACCEPT_NO_TJOINT_PROMOTION_DISTRIBUTION_LEDGER_ONLY`.

Once authorized, the channel-level numeric `z_i` distribution ledger is built
with:

```bash
python scripts/build_joint_numeric_zi_distribution_ledger_v1.py
python scripts/validate_joint_numeric_zi_distribution_ledger_v1.py
python scripts/build_joint_numeric_zi_distribution_build_blocker_status_v1.py
python scripts/validate_joint_numeric_zi_distribution_build_blocker_status_v1.py
```

This produces:

```text
data/derived/joint_numeric_zi_distribution_ledger_v1.csv
data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv
docs/joint_numeric_zi_distribution_ledger_v1.md
```

The ledger computes per-channel `z_i` values only. It does not sum them into
`T_joint` and does not authorize endpoint scoring or validation.

Current channel-level ledger result:

```text
kids_lensing_cosebis_low_mode : z_i = 3.348919353870e+00
observer_path_basis_low_z     : z_i = 1.218797645009e+00
desi_shape_time_readout       : z_i = 1.106851383042e+00
```

These are distribution-standardized channel values under the frozen
median/MAD rule. They are not a joint statistic and should not be quoted as
endpoint, cosmological, or physical validation.

The next separate authorization package for numeric `T_joint` is recorded in:

```text
data/source_manifest/joint_numeric_t_joint_authorization_policy_v1.csv
data/derived/joint_numeric_t_joint_authorization_response_template_v1.csv
data/derived/joint_numeric_t_joint_authorization_package_v1.zip
data/derived/joint_numeric_t_joint_authorization_package_v1.zip.sha256
data/derived/joint_numeric_t_joint_authorization_package_v1_manifest.csv
data/derived/joint_numeric_t_joint_authorization_package_v1_summary.csv
docs/joint_numeric_t_joint_authorization_package_v1.md
docs/joint_numeric_t_joint_authorization_reviewer_instructions_v1.md
scripts/build_joint_numeric_t_joint_authorization_package_v1.py
scripts/validate_joint_numeric_t_joint_authorization_package_v1.py
```

This package asks only whether the existing `z_i` ledger may be combined once
under the frozen shell `T_joint = sum_i q_i z_i`. It still does not authorize
new endpoint scores, endpoint validation, cosmological validation, or physical
validation.

A completed numeric `T_joint` reviewer response can be imported and validated
with:

```bash
python scripts/import_joint_numeric_t_joint_authorization_response_v1.py \
  /path/to/completed_reviewer_response.csv
python scripts/build_joint_numeric_t_joint_blocker_status_v1.py
python scripts/validate_joint_numeric_t_joint_blocker_status_v1.py
```

The accepting reviewer responses are exact-string gated. The short internal
tokens are:
`authorize_numeric_t_joint_once`,
`accept_frozen_numeric_inputs`,
`accept_caveated_covariance_boundary`, and
`accept_numeric_t_joint_no_validation`.
The accepted external-reviewer aliases are:
`AUTHORIZE_NUMERIC_T_JOINT_LEDGER_ONLY_NOT_ENDPOINT_SCORING`,
`ACCEPT_FROZEN_QI_ZI_INPUTS_NO_RETUNING`,
`ACCEPT_CAVEATED_COVARIANCE_BOUNDARY`, and
`ACCEPT_NUMERIC_TJOINT_NO_VALIDATION`.

The current numeric `T_joint` blocker status is recorded in:

```text
data/derived/joint_numeric_t_joint_blocker_status_v1.csv
data/derived/joint_numeric_t_joint_blocker_status_v1_summary.csv
docs/joint_numeric_t_joint_blocker_status_v1.md
scripts/build_joint_numeric_t_joint_blocker_status_v1.py
scripts/validate_joint_numeric_t_joint_blocker_status_v1.py
```

Current blocker:

`numeric_t_joint_authorization_response_missing`

If a completed reviewer response later authorizes the numeric joint ledger,
the guarded build path is:

```bash
python scripts/import_joint_numeric_t_joint_authorization_response_v1.py \
  /path/to/completed_reviewer_response.csv
python scripts/build_joint_numeric_t_joint_ledger_v1.py
python scripts/validate_joint_numeric_t_joint_ledger_v1.py
python scripts/build_joint_numeric_t_joint_blocker_status_v1.py
python scripts/validate_joint_numeric_t_joint_blocker_status_v1.py
```

The guarded builder refuses to run without the imported authorization summary.
The resulting `T_joint`, if authorized, remains a numeric joint ledger only,
not endpoint scoring or validation.

The authorized numeric `T_joint` ledger is now recorded in:

```text
data/derived/joint_numeric_t_joint_ledger_v1.csv
data/derived/joint_numeric_t_joint_ledger_v1_summary.csv
docs/joint_numeric_t_joint_ledger_v1.md
scripts/build_joint_numeric_t_joint_ledger_v1.py
scripts/validate_joint_numeric_t_joint_ledger_v1.py
```

Current numeric joint ledger:

```text
T_joint = 4.142466300799e+00
```

Channel contributions:

```text
kids_lensing_cosebis_low_mode : 2.492514715023e+00
observer_path_basis_low_z     : 8.800470982924e-01
desi_shape_time_readout       : 7.699044874836e-01
```

This remains a caveated numeric joint ledger only. It is not an endpoint score,
not a cosmological validation claim, and not a physical validation claim. The
current blocker after this ledger is:

`numeric_t_joint_ledger_built_endpoint_scoring_authorization_missing`

The numeric same-statistic control suite around this frozen `T_joint` is now
recorded in:

```text
data/derived/joint_numeric_t_joint_control_suite_v1.csv
data/derived/joint_numeric_t_joint_control_suite_v1_summary.csv
docs/joint_numeric_t_joint_control_suite_v1.md
scripts/build_joint_numeric_t_joint_control_suite_v1.py
scripts/validate_joint_numeric_t_joint_control_suite_v1.py
```

It uses the same frozen statistic, signs, row scope, and standardization logic
for candidate and controls. The current prevalidation result is:

```text
candidate T_joint = 4.142466300799e+00
numeric controls  = 26
controls beating or equaling candidate = 0
```

This is a control-suite precondition only. It is not endpoint scoring, not a
p-value, not a likelihood ratio, and not cosmological or physical validation.

The current external handoff package asks only whether this `0/26`
prevalidation control-suite result is sufficient to prepare a separate
permission-only endpoint-scoring authorization package:

```text
data/derived/joint_numeric_t_joint_control_suite_review_package_v1.zip
data/derived/joint_numeric_t_joint_control_suite_review_package_v1.zip.sha256
data/derived/joint_numeric_t_joint_control_suite_review_package_v1_summary.csv
data/derived/joint_numeric_t_joint_control_suite_review_response_template_v1.csv
docs/joint_numeric_t_joint_control_suite_review_external_message_v1.md
docs/joint_numeric_t_joint_control_suite_review_instructions_v1.md
scripts/validate_joint_numeric_t_joint_control_suite_review_package_v1.py
scripts/import_joint_numeric_t_joint_control_suite_review_response_v1.py
```

Current package checksum:

```text
70de8881d432a1ec7ae69825462821fee45afe13b539afb88cb6a659e025abba
```

The reviewer does not need repository access. If accepted, all four response
rows must set:

```text
endpoint_scoring_authorization_package_preparation_allowed=true
endpoint_scoring_allowed=false
endpoint_validation_claimed=false
cosmological_validation_claimed=false
physical_validation_claimed=false
```

The completed response can be imported with:

```bash
python scripts/import_joint_numeric_t_joint_control_suite_review_response_v1.py \
  /path/to/completed_reviewer_response.csv
python scripts/build_joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1.py
python scripts/validate_joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1.py
```

The current endpoint-authorization blocker ledger is recorded in:

```text
data/derived/joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1.csv
data/derived/joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1_summary.csv
docs/joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1.md
scripts/build_joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1.py
scripts/validate_joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1.py
```

Current blocker:

`control_suite_review_response_missing`

Until that response is imported and validated, no endpoint-scoring
authorization package can be built, and no endpoint scoring or validation is
authorized.

The current same-statistic execution blocker ledger is recorded in:

```text
data/derived/joint_same_statistic_execution_blocker_status_v1.csv
data/derived/joint_same_statistic_execution_blocker_status_v1_summary.csv
docs/joint_same_statistic_execution_blocker_status_v1.md
scripts/build_joint_same_statistic_execution_blocker_status_v1.py
scripts/validate_joint_same_statistic_execution_blocker_status_v1.py
```

Current blocker/status:

`permission_only_replay_completed_not_validation`

The consolidated post-replay validation roadmap is recorded in:

`data/derived/joint_post_replay_validation_roadmap_v1_summary.csv`

It freezes the only allowed promotion order:

1. close the KiDS/COSEBIs physical-promotion proof chain,
2. close covariance through a source-native product or reviewed caveated
   block-diagonal surrogate,
3. implement all same-statistic matched controls,
4. only then prepare a separate validation-protocol authorization package.

Current verdict:

`JOINT_POST_REPLAY_ROADMAP_FROZEN_VALIDATION_NOT_READY`

## Row-level numeric penalty value package

The reviewer-authorized row-level penalty route has advanced only to a
separate numeric value package:

```bash
python scripts/build_joint_row_level_numeric_penalty_values_v1.py
python scripts/validate_joint_row_level_numeric_penalty_values_v1.py
```

Outputs:

```text
data/derived/joint_row_level_numeric_penalty_values_v1.csv
data/derived/joint_row_level_numeric_penalty_values_joint_v1.csv
data/derived/joint_row_level_numeric_penalty_values_v1_summary.csv
docs/joint_row_level_numeric_penalty_values_v1.md
```

Reviewer handoff package:

```bash
python scripts/build_joint_row_level_numeric_penalty_value_review_package_v1.py
python scripts/validate_joint_row_level_numeric_penalty_value_review_package_v1.py
```

```text
data/derived/joint_row_level_numeric_penalty_value_review_package_v1.zip
data/derived/joint_row_level_numeric_penalty_value_review_package_v1.zip.sha256
data/derived/joint_row_level_numeric_penalty_value_review_response_template_v1.csv
```

Current package SHA-256:

```text
7878efb9e08cd4721b8fef04b0f9998cbdf82f447b1eb7aad1ca565f8750ed3c
```

Current result:

```text
channel_rows=1042
complete_joint_penalty_rows=1
P_row_candidate=0.0702783215662
```

This is not `lambda_row`, not `T_joint` rescoring, not endpoint scoring, and
not validation. Control alternatives remain channel-local because no
residual-blind cross-channel control alignment artifact is authorized yet.

Completed value review:

```bash
python scripts/import_joint_row_level_numeric_penalty_value_review_response_v1.py \
  /path/to/joint_row_level_numeric_penalty_value_review_completed_response_v1.zip
python scripts/validate_joint_row_level_numeric_penalty_value_review_response_v1.py
python scripts/build_joint_row_level_numeric_penalty_value_review_blocker_status_v1.py
python scripts/validate_joint_row_level_numeric_penalty_value_review_blocker_status_v1.py
```

Current value-review verdict:

```text
NUMERIC_PENALTY_VALUES_ACCEPTED_FOR_RECORD_ONLY_NEXT_USE_BLOCKED
```

The numeric values are accepted for the record only. Cross-channel control
alignment, `lambda_row`, `T_joint` rescoring, endpoint scoring, and validation
remain blocked pending a separate authorization route.

Next-use authorization review package:

```bash
python scripts/build_joint_row_level_penalty_use_authorization_review_package_v1.py
python scripts/validate_joint_row_level_penalty_use_authorization_review_package_v1.py
```

```text
data/derived/joint_row_level_penalty_use_authorization_review_package_v1.zip
data/derived/joint_row_level_penalty_use_authorization_review_package_v1.zip.sha256
data/derived/joint_row_level_penalty_use_authorization_review_response_template_v1.csv
```

Current package SHA-256:

```text
b77bae01b2d09b5be254164bcfcc04f5bb0ba36aa05003defa4efdc2a975ad85
```

This package still does not authorize `lambda_row`, cross-channel control
alignment, `T_joint` rescoring, endpoint replay, or validation. It only asks
whether a later residual-blind use-policy route may be planned.

Completed use-authorization review:

```bash
python scripts/import_joint_row_level_penalty_use_authorization_review_response_v1.py \
  /path/to/joint_row_level_penalty_use_authorization_completed_review_response_v1.zip
python scripts/validate_joint_row_level_penalty_use_authorization_review_response_v1.py
python scripts/build_joint_row_level_penalty_use_authorization_blocker_status_v1.py
python scripts/validate_joint_row_level_penalty_use_authorization_blocker_status_v1.py
```

Current use-authorization verdict:

```text
PENALTY_USE_ROUTE_PLANNING_ALLOWED_RESCORING_STILL_BLOCKED
```

The allowed next work is route planning only:

1. build a residual-blind cross-channel control alignment package;
2. build a separate residual-blind `lambda_row` policy package;
3. only after both pass, consider a separate rescoring authorization package.

Cross-channel control alignment design package:

```bash
python scripts/build_joint_row_level_cross_channel_control_alignment_review_package_v1.py
python scripts/validate_joint_row_level_cross_channel_control_alignment_review_package_v1.py
```

```text
data/derived/joint_row_level_cross_channel_control_alignment_review_package_v1.zip
data/derived/joint_row_level_cross_channel_control_alignment_review_package_v1.zip.sha256
data/derived/joint_row_level_cross_channel_control_alignment_review_response_template_v1.csv
```

Current package SHA-256:

```text
077268b34bbac09b1a11ee3a5121eaec62f3afbe657a81fb6133e60b54e398e4
```

This is only an alignment-design review package. It records the current
control-count imbalance and proposes a deterministic min-count index alignment
for review. It does not compute aligned joint control values, choose
`lambda_row`, rescore `T_joint`, or authorize validation.

Completed alignment-design review responses are imported and checked with:

```bash
python scripts/import_joint_row_level_cross_channel_control_alignment_review_response_v1.py \
  /path/to/joint_row_level_cross_channel_control_alignment_completed_review_response_v1.zip
python scripts/validate_joint_row_level_cross_channel_control_alignment_review_response_v1.py
python scripts/build_joint_row_level_cross_channel_control_alignment_blocker_status_v1.py
python scripts/validate_joint_row_level_cross_channel_control_alignment_blocker_status_v1.py
```

The current blocker status is intentionally waiting for a completed reviewer
response unless a completed response has been imported. After importing
`joint_row_level_open_blocker_completed_review_response_v1.zip`, the current
status is:

```text
CROSS_CHANNEL_ALIGNMENT_DESIGN_ACCEPTED_VALUES_STILL_BLOCKED
```

The accepted design allows only the next separate aligned-control value package
to be prepared. It still does not authorize aligned values inside the design
review itself, numeric `lambda_row`, `T_joint` rescoring, endpoint scoring, or
validation.

Separate aligned-control value authorization package:

```bash
python scripts/build_joint_row_level_aligned_control_value_authorization_review_package_v1.py
python scripts/validate_joint_row_level_aligned_control_value_authorization_review_package_v1.py
```

The prepared package is a value-computation authorization handoff only:

```text
data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1.zip
data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1.zip.sha256
data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1_manifest.csv
data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1_summary.csv
data/derived/joint_row_level_aligned_control_value_authorization_response_template_v1.csv
docs/joint_row_level_aligned_control_value_authorization_review_package_v1.md
```

The package has also been copied for reviewer handoff to:

```text
/Users/jolcsak/Downloads/joint_row_level_aligned_control_value_authorization_review_package_v1.zip
```

It contains no aligned joint-control values, no numeric `lambda_row`, no
`T_joint` rescoring, no endpoint scoring, and no validation claim.

Completed aligned-control value authorization responses are imported and checked with:

```bash
python scripts/import_joint_row_level_aligned_control_value_authorization_response_v1.py \
  /path/to/joint_row_level_aligned_control_value_authorization_completed_response_v1.zip
python scripts/validate_joint_row_level_aligned_control_value_authorization_response_v1.py
python scripts/build_joint_row_level_aligned_control_value_authorization_blocker_status_v1.py
python scripts/validate_joint_row_level_aligned_control_value_authorization_blocker_status_v1.py
```

The current status after importing the completed positive response and running
the guarded value computation is:

```text
ALIGNED_CONTROL_VALUES_COMPUTED_RESCORING_STILL_BLOCKED
```

The imported response authorizes only the aligned-control value computation. It
does not authorize numeric `lambda_row`, `T_joint` rescoring, endpoint scoring,
or validation. The guarded non-scoring value artifact is built and checked with:

```bash
python scripts/build_joint_row_level_aligned_control_values_guarded_v1.py
python scripts/validate_joint_row_level_aligned_control_values_v1.py
```

Before that response exists, the builder must stop with a missing authorization
summary. The guarded artifact still does not choose `lambda_row`, rescore
`T_joint`, run endpoint scoring, or claim validation.

```text
data/derived/joint_row_level_aligned_control_value_authorization_blocker_status_v1.csv
data/derived/joint_row_level_aligned_control_value_authorization_blocker_status_v1_summary.csv
docs/joint_row_level_aligned_control_value_authorization_blocker_status_v1.md
data/derived/joint_row_level_aligned_control_values_v1.csv
data/derived/joint_row_level_aligned_control_values_v1_summary.csv
docs/joint_row_level_aligned_control_values_v1.md
```

```text
data/derived/joint_row_level_cross_channel_control_alignment_blocker_status_v1.csv
data/derived/joint_row_level_cross_channel_control_alignment_blocker_status_v1_summary.csv
docs/joint_row_level_cross_channel_control_alignment_blocker_status_v1.md
```

Residual-blind `lambda_row` policy review package:

```bash
python scripts/build_joint_row_level_lambda_policy_review_package_v1.py
python scripts/validate_joint_row_level_lambda_policy_review_package_v1.py
```

```text
data/derived/joint_row_level_lambda_policy_review_package_v1.zip
data/derived/joint_row_level_lambda_policy_review_package_v1.zip.sha256
data/derived/joint_row_level_lambda_policy_review_response_template_v1.csv
```

Current package SHA-256:

```text
0908e1a41ce7ac76e31b7974e04554007ca7bbf36a1709ff2ed9dc574e839395
```

This package is policy-only. It records that any future `lambda_row` must be
dimensionless and residual-blind. It does not choose a numeric `lambda_row`,
rescore `T_joint`, or authorize validation.

Completed lambda-policy review responses are imported and checked with:

```bash
python scripts/import_joint_row_level_lambda_policy_review_response_v1.py \
  /path/to/joint_row_level_lambda_policy_completed_review_response_v1.zip
python scripts/validate_joint_row_level_lambda_policy_review_response_v1.py
python scripts/build_joint_row_level_lambda_policy_blocker_status_v1.py
python scripts/validate_joint_row_level_lambda_policy_blocker_status_v1.py
```

The current blocker status is intentionally waiting for a completed reviewer
response unless a completed response has been imported. After importing
`joint_row_level_open_blocker_completed_review_response_v1.zip`, the current
status is:

```text
LAMBDA_POLICY_ACCEPTED_NUMERIC_VALUE_STILL_BLOCKED
```

The accepted policy allows only a later residual-blind numeric-lambda package
to be prepared. It still does not authorize a numeric `lambda_row`, `T_joint`
rescoring, endpoint scoring, or validation.

Separate numeric `lambda_row` review package:

```bash
python scripts/build_joint_row_level_numeric_lambda_review_package_v1.py
python scripts/validate_joint_row_level_numeric_lambda_review_package_v1.py
```

The prepared package proposes only a record-only dimensionless unit-weight
candidate:

```text
lambda_row = 1
```

It is not fitted from endpoint residuals or scores, is not applied to
`T_joint`, and does not authorize endpoint scoring or validation.

```text
data/derived/joint_row_level_numeric_lambda_review_package_v1.zip
data/derived/joint_row_level_numeric_lambda_review_package_v1.zip.sha256
data/derived/joint_row_level_numeric_lambda_review_package_v1_manifest.csv
data/derived/joint_row_level_numeric_lambda_review_package_v1_summary.csv
data/derived/joint_row_level_numeric_lambda_review_response_template_v1.csv
docs/joint_row_level_numeric_lambda_review_package_v1.md
```

Row-level scoring readiness is tracked separately with:

```bash
python scripts/build_joint_row_level_scoring_readiness_v1.py
python scripts/validate_joint_row_level_scoring_readiness_v1.py
```

The current readiness ledger records that aligned-control values are available
(`6` aligned rows, mean `P_row_control=0.109794891058`) and that the numeric
`lambda_row` review package is ready, but no completed numeric-lambda response
has been imported. Therefore row-level scoring is still not ready:

```text
ROW_LEVEL_SCORING_NOT_READY_NUMERIC_LAMBDA_RESPONSE_MISSING
```

The ledger is non-scoring and non-validation:

```text
data/derived/joint_row_level_scoring_readiness_v1.csv
data/derived/joint_row_level_scoring_readiness_v1_summary.csv
docs/joint_row_level_scoring_readiness_v1.md
scripts/build_joint_row_level_scoring_readiness_v1.py
scripts/validate_joint_row_level_scoring_readiness_v1.py
```

After importing the completed numeric-lambda response, the readiness blocker
moves to the next gate:

```text
ROW_LEVEL_SCORING_NOT_READY_T_JOINT_RESCORING_AUTHORIZATION_MISSING
```

The corresponding reviewer package is:

```bash
python scripts/build_joint_row_level_t_joint_rescoring_authorization_review_package_v1.py
python scripts/validate_joint_row_level_t_joint_rescoring_authorization_review_package_v1.py
```

This package asks only whether a later guarded, record-only
`T_joint_penalized = T_joint + lambda_row * P_row` ledger may be computed. It
does not contain penalized values, endpoint scores, fit statistics, or
validation claims.

```text
data/derived/joint_row_level_t_joint_rescoring_authorization_review_package_v1.zip
data/derived/joint_row_level_t_joint_rescoring_authorization_review_package_v1.zip.sha256
data/derived/joint_row_level_t_joint_rescoring_authorization_review_package_v1_manifest.csv
data/derived/joint_row_level_t_joint_rescoring_authorization_review_package_v1_summary.csv
data/derived/joint_row_level_t_joint_rescoring_authorization_response_template_v1.csv
docs/joint_row_level_t_joint_rescoring_authorization_review_package_v1.md
```

The package has also been copied for reviewer handoff to:

```text
/Users/jolcsak/Downloads/joint_row_level_numeric_lambda_review_package_v1.zip
```

Completed numeric `lambda_row` review responses are imported and checked with:

```bash
python scripts/import_joint_row_level_numeric_lambda_review_response_v1.py \
  /path/to/joint_row_level_numeric_lambda_completed_response_v1.zip
python scripts/validate_joint_row_level_numeric_lambda_review_response_v1.py
python scripts/build_joint_row_level_numeric_lambda_blocker_status_v1.py
python scripts/validate_joint_row_level_numeric_lambda_blocker_status_v1.py
```

The current status before importing a completed response is:

```text
NUMERIC_LAMBDA_WAITING_FOR_REVIEW_RESPONSE
```

```text
data/derived/joint_row_level_numeric_lambda_blocker_status_v1.csv
data/derived/joint_row_level_numeric_lambda_blocker_status_v1_summary.csv
docs/joint_row_level_numeric_lambda_blocker_status_v1.md
```

Both post-open-blocker value-gate packages can also be sent together to a
reviewer without repository access:

```bash
python scripts/build_joint_row_level_value_gate_reviewer_handoff_v1.py
python scripts/validate_joint_row_level_value_gate_reviewer_handoff_v1.py
```

Reviewer handoff:

```text
data/derived/joint_row_level_value_gate_reviewer_handoff_v1.zip
data/derived/joint_row_level_value_gate_reviewer_handoff_v1.zip.sha256
data/derived/joint_row_level_value_gate_reviewer_handoff_v1_summary.csv
docs/joint_row_level_value_gate_reviewer_handoff_v1.md
/Users/jolcsak/Downloads/joint_row_level_value_gate_reviewer_handoff_v1.zip
```

This handoff remains non-scoring and non-validation. It asks only for review of
the aligned-control value computation gate and the numeric `lambda_row=1`
record-only candidate.

```text
data/derived/joint_row_level_lambda_policy_blocker_status_v1.csv
data/derived/joint_row_level_lambda_policy_blocker_status_v1_summary.csv
docs/joint_row_level_lambda_policy_blocker_status_v1.md
```

Both open blockers can also be sent together to a reviewer without repository
access:

```bash
python scripts/build_joint_row_level_open_blocker_reviewer_handoff_v1.py
python scripts/validate_joint_row_level_open_blocker_reviewer_handoff_v1.py
```

```text
data/derived/joint_row_level_open_blocker_reviewer_handoff_v1.zip
data/derived/joint_row_level_open_blocker_reviewer_handoff_v1.zip.sha256
data/derived/joint_row_level_open_blocker_reviewer_handoff_v1_summary.csv
docs/joint_row_level_open_blocker_reviewer_handoff_v1.md
```

Current handoff SHA-256:

```text
c7734f99b77ebe35fedb2752cc723390e07f2d0b0fafe152fe4d86fec16ebb5e
```

## Scope

This is a protocol scaffold and branch-opening paper package. The next
scientific milestone is a real-data pilot using public distance, void,
cosmic-web, observer/path, time/readout, growth, lensing, and CMB products
under the frozen audit ladder. A dark-sector decision should only be attempted
after both the no-dark channel basis and the candidate base-substrate response
basis are frozen without endpoint leakage.
