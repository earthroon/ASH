# ASH-FT-03 CPU Tensor Sanity Baseline

ASH-FT-03 converts ASH-FT-02 sampled slice probe statistics into a stable pre-training baseline.

It produces:

- tensor baseline table
- family baseline table
- atlas group baseline table
- sampled norm drift registry
- tensor outlier review queue
- no-train receipt

This patch does not reopen candidate safetensors data and does not replay slice reads. It only reads previously emitted JSON artifacts.

## Next step

After PASS, the next natural seal is:

```txt
ASH-FT-04
Single Atlas Group GPU Upload Dry-run /
No Forward No Train Seal
```
