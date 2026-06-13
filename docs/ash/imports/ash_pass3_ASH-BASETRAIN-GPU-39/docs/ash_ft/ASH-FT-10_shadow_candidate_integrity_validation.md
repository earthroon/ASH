# ASH-FT-10 Shadow Candidate Integrity Validation

ASH-FT-10 is a read-only integrity validation step for the FT-09 staged shadow candidate. It does not load the model and does not run inference. It confirms that the shadow candidate is structurally valid safetensors data and that the source candidate/runtime default remain untouched.

The FT-08/FT-09 line may be metadata-only when raw delta payload bytes are absent. In that case, ASH-FT-10 accepts unchanged patched ranges when `--metadata-only-dryrun-allowed true` is set, while still validating header, tensor map, source hash, and unpatched range parity.
