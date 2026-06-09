# KiDS-1000 COSEBIs `F_overlap` Execution Review Template v1

This gate materializes an empty review template for the default batch-0
full-mask acquisition route.

The template has the exact columns declared by the execution-review schema and
the 20 planned product rows from the dry run. It is not an execution log:
network fields, checksums, fetched timestamps, and reviewer fields are empty or
pending, and all forbidden-input and endpoint flags remain false.

The template can be handed to a future reviewer after a manual fetch, but the
filled artifact must be committed separately and validated before any
batch-promotion decision. The template itself does not fetch products, promote a
batch, compute overlap, construct a mapping vector, or enable endpoint scoring.
