# ASH-FT-02 Acceptance

## PASS

```txt
PASS_ASH_FT02_FULL_COVERAGE_SLICE_READ_NO_GPU_UPLOAD
```

Required checks:

1. FT-00 manifest is read.
2. FT-00 atlas plan is read.
3. FT-01 memory budget is read.
4. FT-01 optimizer shard estimate is read.
5. Candidate sha256 matches expected.
6. All FT-00 manifest tensor keys are probed.
7. Each tensor has at least one bounded sample.
8. Each family has at least one probe sample.
9. Sample ranges are inside tensor file ranges.
10. Sample lengths respect dtype alignment where applicable.
11. F32 samples decode as little-endian f32.
12. F32 samples contain no NaN/Inf.
13. Sample checksums are generated.
14. Total read bytes remain under `--max-total-read-mb`.
15. No GPU upload, forward, backward, optimizer step, candidate write, or runtime default apply occurs.

## FAIL

Any of the following fails the patch:

- Missing FT-00/FT-01 runtime artifacts.
- Candidate sha256 mismatch.
- Tensor key missing from probe output.
- Unknown tensor silently excluded.
- Sample range outside tensor byte range.
- F32 NaN/Inf found.
- Full tensor load or mmap materialization.
- GPU device/buffer/upload.
- Forward/backward/optimizer step.
- Candidate weight write.
- Runtime default apply or checkpoint alias rebind.
