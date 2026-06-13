# Paper 10 BAO r_d-cancelled time-level difference audit v1

**Doc class:** source-side differential route audit
**Status:** not endpoint replay, not validation
**Canonical parent:** Paper 10 time-level route nuisance/interface freeze plan

This audit tests the narrowest safe use of the radial BAO level route. Since

```text
-log(D_H/r_d) = log H + log(r_d/c),
```

the constant sound-horizon term cancels in the two-point difference:

```text
Delta[-log(D_H/r_d)] = Delta[log H].
```

This removes the \(r_d\) nuisance for a differential direction check, but it
does not provide an absolute \(H(z)\) scale and it does not authorize endpoint
scoring. With only two radial BAO points, the audit is underresolved by design.

Allowed interpretation:

```text
source-side differential direction check only
```

Forbidden interpretation:

```text
endpoint replay, validation, absolute H(z), or clock-slope support
```
