# Joint row-level relaxed cyclic penalized stress v1

**Doc class:** relaxed-control stress test.
**Status:** complete; not validation.
**Claim boundary:** `joint_row_level_relaxed_cyclic_penalized_stress_not_validation`.

This is a fast stress test, not a strict endpoint validation.
It keeps the same frozen source-side penalty values but relaxes
the all-channel alignment rule by cyclically reusing the six DESI
shape/time controls across the 25 observer/path controls.

Because no per-control relaxed `T_joint` statistic has been
authorized for this construction, the test isolates the row-level
penalty term using the same frozen base `T_joint` for candidate and
relaxed controls.

Relaxed controls: `25`.
Controls whose penalty exceeds/equal candidate: `17`.
Minimum penalized margin: `-3.326129356899e-01`.

The result can motivate a future reviewed relaxed-alignment route,
but it does not replace the strict six-control endpoint replay.
