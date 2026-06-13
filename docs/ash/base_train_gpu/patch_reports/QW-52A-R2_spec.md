# QW-52A-R2
## Existing QWave Conditioning Projection Rebind / Cheonjiin Feature Input Bridge Seal

### SSOT
- Base patch: QW-52A-R1
- Rust-owned bridge and validation.
- Python is injector only.
- This patch rebinds `CheonjiinJasoStrokeFacade` to the existing `lora_train::qwave_conditioning_projection_dry_run` dry-run path.

### Scope
- Add `model_core::cheonjiin_projection_input_bridge`.
- Add `lora_train::qwave_conditioning_cheonjiin_projection_bridge`.
- Add Rust validator binary `qw52a_r2_projection_rebind_validate`.
- Attach additive `cheonjiin_projection_bridge` trace field to candidate awareness.

### No mutation policy
- No new projection matrix.
- No new adapter weight.
- No new projection math.
- No hidden state fusion.
- No logit mutation.
- No sampler mutation.
- No token selection mutation.
- Gate remains 0.0.
- `applied_to_hidden=false`.

### Outputs
- `workspace/trace/qw52a_r2_projection_bridge_schema.json`
- `workspace/trace/qw52a_r2_projection_bridge_fixture.json`
- `workspace/trace/qw52a_r2_receipt.json`
- `workspace/trace/qw52a_r2_static_validation_result.json`
