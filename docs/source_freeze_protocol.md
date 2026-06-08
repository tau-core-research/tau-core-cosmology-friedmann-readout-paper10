# Paper 10 Source-Freeze Protocol

Paper 10 is not allowed to become a measurement-claim paper until the source
manifest is frozen before endpoint scoring.

The source manifest is:

```text
data/source_manifest/paper10_source_freeze_manifest.csv
```

Each row declares:

- the source block,
- the public provider,
- the official access URL or `TBD`,
- the current freeze status,
- the planned local artifact path,
- forbidden endpoint fields,
- and why the source is used.

## Freeze Statuses

`SOURCE_SELECTED_NOT_FETCHED`

The source family is acceptable as a candidate public input, but the raw product
has not yet been downloaded, checksummed, and frozen.

`BLOCKED_SOURCE_SELECTION`

The block is scientifically needed, but no exact public source product has been
accepted yet. Endpoint scoring using that block is forbidden.

`FETCHED_FROZEN`

Future status only. This means the source was acquired, local paths and hashes
were recorded, and the transformation rule was frozen before endpoint scoring.

## Leakage Rule

The following endpoint information must not be used to choose source products,
activation functions, void thresholds, web labels, or environment masks:

```text
distance residuals
growth residuals
lensing residuals
fit-improvement flags
posthoc environment labels
late-time fit parameters without prior source freeze
```

## Current Scientific Status

The current repository is still below real-data pilot status. It has a source
manifest and validation script, but several required blocks remain
`BLOCKED_SOURCE_SELECTION`.

Therefore the allowed claim remains:

```text
Paper 10 defines a source-frozen Friedmann-readout audit protocol.
```

The disallowed claim remains:

```text
Paper 10 has validated a Tau Core late-time cosmology signal.
```
