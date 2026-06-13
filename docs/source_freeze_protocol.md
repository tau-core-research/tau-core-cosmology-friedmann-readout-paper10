# Paper 10 Source-Freeze Protocol

Paper 10 is not allowed to become a measurement-claim paper until the source
manifest is frozen before endpoint scoring.

The source manifest is:

```text
data/source_manifest/paper10_source_freeze_manifest.csv
```

The first channel-level companion manifest is:

```text
data/source_manifest/cosmology_channel_manifest_v1.csv
data/source_manifest/cosmology_activation_rule_manifest_v1.csv
data/source_manifest/cosmology_activation_parameter_freeze_plan_v1.csv
docs/cosmology_channel_manifest_v1.md
docs/cosmology_activation_rule_manifest_v1.md
docs/cosmology_activation_parameter_freeze_plan_v1.md
```

It freezes the allowed source families and forbidden endpoint fields for the
four cosmology readout channels:

```text
W_void, W_web, W_path, W_time.
```

The activation-rule companion declares non-numeric formula shells, source-only
normalization policies, and null controls for those channels.
The parameter-freeze companion declares how the future normalization scales and
optional rule parameters must be frozen without endpoint residuals.

Each row declares:

- the source block,
- the public provider,
- the official access URL, or `not yet assigned` for rows that are still
  protocol placeholders rather than source-frozen endpoint inputs,
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
selected-only rather than `FETCHED_FROZEN`.

The repository also includes a compact source-page provenance cache:

```text
data/source_manifest/source_page_cache_manifest.csv
data/source_manifest/source_page_cache/
```

This cache records official source landing pages with byte counts and SHA-256
hashes. It does not contain raw survey products and does not authorize endpoint
scoring.

The next layer is the product-freeze plan:

```text
data/source_manifest/paper10_product_freeze_plan.csv
docs/product_freeze_plan.md
```

This plan declares which product role must be acquired from each selected source
family, but every row remains below endpoint status.

Therefore the allowed claim remains:

```text
Paper 10 defines a source-frozen Friedmann-readout audit protocol.
```

The disallowed claim remains:

```text
Paper 10 has validated a Tau Core late-time cosmology signal.
```
