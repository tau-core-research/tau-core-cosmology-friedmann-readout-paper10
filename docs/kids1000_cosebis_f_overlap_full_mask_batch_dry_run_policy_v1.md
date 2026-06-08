# KiDS-1000 COSEBIs `F_overlap` Full-Mask Batch Dry Run v1

This gate provides the reproducible batch-runner interface for future
full-route mask acquisition while keeping the public reproduction path dry.

The default reproducibility command inspects batch 0 only and does not fetch
any FITS products. It writes the selected URLs, expected cache paths, and
leakage flags to derived CSV files. Network output fields such as HTTP status,
byte count, and SHA-256 remain empty in dry-run mode.

Manual execution is intentionally separate:

```bash
python scripts/acquire_kids1000_cosebis_f_overlap_full_mask_batch_v1.py --batch-index 0 --execute
```

Large downloaded FITS files are written to the ignored full-route cache. Even
after a manual fetch, overlap derivation, path mapping, theory vectors, and
endpoint scoring remain separate later gates.
