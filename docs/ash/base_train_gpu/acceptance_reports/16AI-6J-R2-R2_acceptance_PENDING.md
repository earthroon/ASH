# 16AI-6J-R2-R2 Acceptance

Status: PENDING_RUNTIME

Patch: GPU Gate Status Reader Alignment Patch

Scope:
- generation path changed: false
- GPU replay8 parity logic changed: false
- source gate reader changed: true
- gpu_default=false maintained
- cpu_fallback=true maintained
- global_default_commit=false maintained
- token_ids_mutated=false maintained
- vocab_augmented=false maintained
- new_token_ids_created=false maintained

Expected runtime outcome:
- `--gpu-gate-json` status is read from supported JSON paths, or inferred from complete summary invariants.
- Gate check logs include `gpu_gate_status` and `status_source`.
- If the input is a PENDING bake manifest, the binary must fail with explicit found status/summary diagnostics, not silently PASS.
- If the input is a runtime 16AI-6J PASS JSON, the binary must enter GPU replay8 body.

Acceptance target:
- PASS_READER_ALIGNMENT after local compile/runtime check.
