# Paper 10 KernelRecord Status Audit v1

**Doc class:** paper-level cosmology-kernel status audit
**Reader role:** reproducibility / claim-boundary reviewer
**Status:** audit map only; not endpoint scoring; not validation
**Canonical theory schema:** `KernelRecord_tau^S`

Paper 10 applies the same kernel-status discipline to cosmological
Friedmann-readout residual channels.  The current evidence is a
source-frozen prevalidation audit, not a joint likelihood and not a
cosmological validation.

## Channel Manifest Status

| channel | intended readout role | current status | source quotient | validation boundary |
| --- | --- | --- | --- | --- |
| `W_VOID_MATURITY` | void maturity / late-time distance-growth activation | declared channel; some refined source-side routes tested | `Q_src^P` proxy/source manifest | not endpoint by declaration |
| `W_WEB_ANISOTROPY` | cosmic-web anisotropy / growth-lensing environment | declared channel; used in joint preflight | `Q_src^P` proxy/source manifest | not endpoint by declaration |
| `W_PATH_PROJECTION` | observer/path projection through null-geodesic-bundle environment | declared channel; observer-basis/path screens tested | `Q_src^P` path/environment proxies | source-native full path kernel not closed |
| `W_TIME_READOUT` | time/readout projection of observed `a(t)` and `H(t)` reconstructions | declared channel; DESI/time/shape routes partially tested | `Q_src^P` time/shape support | route-specific blockers remain |

The manifest forbids distance/growth/lensing residuals, fit-improvement flags,
post-hoc sky labels, and late-time fit parameters from selecting channel
labels or activation rules.

## Main Kernel Families

| kernel / artifact | status | source support and composition | control status | validation boundary |
| --- | --- | --- | --- | --- |
| best-justified three-channel preflight kernel | source-frozen preflight positive | positive-support channel set; source-side exponents varied without changing labels or endpoint scores | robust under five source-side weighting schemes | not a joint likelihood; not validation |
| same-statistic numeric `T_joint` ledger | numeric diagnostic / preflight statistic | `T_joint = sum_i q_i z_i` under frozen channel definitions | same-statistic controls required | not a p-value, likelihood ratio, or validation-grade evidence |
| strict six-control row-level penalized replay | guarded endpoint-scoring ledger | candidate penalized statistic compared only to deterministically aligned row-level controls | `0/6` aligned controls beat/equal candidate | preflight evidence only; not endpoint/cosmological/physical validation |
| relaxed 25-control stress | caveated negative / stress control | relaxed control expansion without per-control relaxed `T_joint` | `17/25` relaxed controls match or exceed candidate row penalty in paper text | retained as cautionary negative result |
| full-kernel proxy component screen | diagnostic constraint | stacks void/web/LOS/geometry proxy factors around observer basis | enriched proxies fail to outperform base observer-basis carrier | not failure of observer/path projection; proxy factors are not source-native full kernel |

## KernelRecord Fields That Remain Open

| field | current Paper 10 state |
| --- | --- |
| `source_quotient` | proxy-level `Q_src^P` exists for declared channels; full Tau-side `Q_src^tau` not derived |
| `SourceSupp(Delta K_a)` | partially filled for channel/proxy families; source-native path/time support incomplete |
| `overlap_decision` | guarded for row-level/common source exports; cross-probe overlap still not validation-grade |
| `Compose_S` | best-justified joint kernel composition declared for preflight; not a physical parent action |
| `controls` | same-statistic, strict aligned, relaxed stress, and diagnostic controls exist |
| `robustness_checks` | source-side weighting robustness positive; relaxed stress negative/caveated |
| `validation_status` | no cosmological validation, no physical validation, no dark-energy explanation claim |
| `failure_or_demotion_rule` | relaxed-control and full-kernel-proxy negatives preserved as constraints |

## KernelRecord Verdict

Paper 10 currently supports this status:

```text
PAPER10_FRIEDMANN_READOUT =
    source-frozen cosmology prevalidation audit
    with positive strict preflight ledgers,
    preserved caveated-negative relaxed controls,
    and no validation-grade joint covariance closure.
```

The largest blocker remains:

```text
validation-grade cross-probe covariance and source-native multi-probe product
```

Therefore Paper 10 strengthens the Tau Core architecture as a reproducible
multi-channel audit protocol, not as a completed cosmological model.
