# Pantheon clock-rate phase CC-support fast screen v1

**Doc class:** preauthorization diagnostic fast screen
**Status:** not endpoint replay, not validation
**Canonical parent:** Paper 10 time/readout source audit

This screen tests whether the wider CC-support clock-rate/phase basis improves
over the low-z three-bin blocker.

Result:

- best candidate family: `clock_slope`;
- candidate improvement over baseline:
  `delta_chi2_candidate_minus_baseline = -1.142872`;
- best candidate rank among candidates and controls: `2`;
- best global control: `rank_reverse/clock_level`;
- best global control chi-square: `1207.578076`;
- best candidate chi-square: `1208.99638`;
- verdict:
  `clock_rate_phase_cc_support_fast_screen_not_control_resistant`.

Interpretation:

The wider CC support improves the time/readout signal relative to the low-z
three-bin branch, and the `clock_slope` family survives its local family
controls. However, the run still fails the global control condition because a
rank-reversed `clock_level` control is better. Therefore this is a promising
diagnostic, not replay authorization and not validation.

The next focused source-side question is whether a predeclared, physically
motivated clock-slope-only route can be justified before scoring, or whether an
independent time/readout observable is needed.
