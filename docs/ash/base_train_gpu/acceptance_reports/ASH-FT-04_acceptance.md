# ASH-FT-04 Acceptance

## PASS

- FT-00/01/02/03 JSON inputs are read.
- Candidate sha256 matches expected value.
- Selected group exists in FT-01 budget.
- Selected group tensor keys exist in FT-00 manifest.
- Only selected group data is read.
- Bounded upload bytes do not exceed `--max-upload-bytes`.
- GPU adapter/device/queue/buffer creation succeeds.
- Queue write upload succeeds.
- GPU capability snapshot, upload plan, upload receipt, and main receipt are written.
- Shader/pipeline/dispatch/forward/backward/loss/optimizer/train/candidate write/default apply/readback stay false.

## FAIL

- Missing input artifact.
- Candidate sha256 mismatch.
- Selected group missing.
- Selected group tensor key missing from manifest.
- Data read escapes selected group.
- Upload bytes exceed max_upload_bytes.
- GPU adapter/device/buffer/queue write fails.
- Any forbidden execution occurs.
