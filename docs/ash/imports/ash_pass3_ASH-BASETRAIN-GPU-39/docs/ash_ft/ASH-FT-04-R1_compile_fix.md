# ASH-FT-04-R1 Compile Fix

This patch fixes a compile-time variable name mismatch in the ASH-FT-04 GPU upload receipt summary.

The computed local is `total_upload_bytes`; the receipt field is `total_uploaded_bytes`. The fix maps the local into the field explicitly.

No GPU execution policy is changed. FT-04 remains upload-only and no-forward/no-train.
