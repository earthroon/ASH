# ASH-BASETRAIN-BT-WGSL-ATLAS-RUNTIME-COMMITTED-GENERATION-CHECKPOINT-EXPORT-06C-R27-R1J-R3

## 0. Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-ATLAS-RUNTIME-COMMITTED-GENERATION-CHECKPOINT-EXPORT-06C-R27-R1J-R3`
- Build revision: `bt-wgsl-atlas-runtime-committed-generation-checkpoint-export-06c-r27-r1j-r3`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-ATLAS-RUNTIME-GRADIENT-OPTIMIZER-COMMIT-ADMISSION-06C-R27-R1J-R2E`
- Input authority: committed training generation `1`, optimizer step `1`, R2E transaction state `COMMITTED`
- Output authority: canonical checkpoint bundle plus live R1J E0-E5 writer provenance
- Training mutation during R3: CLOSED
- Reload/step2 continuation: CLOSED

## 1. R2E physical parent SSOT

R3 is admitted only after the same invocation physically completes R2E.

Current physical parent facts:

- optimizer: `adamw`
- learning rate: `0.00005`
- weight decay: `0.01`
- optimizer profile: `ASH-FT-38:ash_ft38_adamw_group_local_v1`
- configured gradient accumulation: `8`
- physical microbatch accumulation count: `1`
- production accumulation adoption: `0`
- logical gradients: `201/201`
- optimizer parameters: `201/201`
- candidate parameters: `201/201`
- training generation: `0 -> 1`
- optimizer step: `0 -> 1`
- canonical weight mutation: `1`
- optimizer-state mutation: `1`
- checkpoint write/export at R2E: `0`
- R1J real export event at R2E: `0`

The former specification assumption `configured_gradient_accumulation=32` is retired. The observed runtime SSOT is `8`.

## 2. Explicit admission

New CLI flag:

`--admit-committed-generation-checkpoint-export`

Required chain:

1. `--admit-atlas-runtime-route`
2. `--admit-atlas-forward-wave-execution`
3. `--admit-atlas-final-output-real-loss`
4. `--admit-atlas-real-loss-backward`
5. `--admit-atlas-gradient-optimizer-commit`
6. `--admit-committed-generation-checkpoint-export`

No parent admission is inferred from a child flag. R2E standalone PASS/HOLD behavior remains unchanged when the R3 flag is absent.

## 3. Source authority

R3 MUST consume the R2E committed runtime training store:

- `training_state/active_training_generation.json`
- `training_state/candidate_step_000001/transaction.json`
- `training_state/candidate_step_000001/candidate_parameter_manifest.json`
- the exact candidate weight/m/v files referenced by that manifest

Required source state:

- active-generation schema: `ash.basetrain.training_generation.v1`
- generation: `1`
- optimizer step: `1`
- parent generation: `0`
- transaction state: `COMMITTED`
- active-pointer candidate set digest equals the R2E physical receipt
- active-pointer training-step digest equals the R2E physical receipt
- candidate manifest physical SHA256 equals the active pointer digest

R3 MUST NOT recreate generation 1 from the genesis checkpoint, gradients, or optimizer math.

## 4. Generation-1 combined-state parity

R2E seals each logical parameter with three digests:

- candidate weight digest
- first-moment digest
- second-moment digest

R3 recomputes the exact ordered combined state digest from all 201 records using the same identity tuple:

`parameter_id : weight_digest : m_digest : v_digest`

The recomputed combined digest MUST equal the R2E `candidate_parameter_set_digest` before any checkpoint export is published.

R3 additionally emits separate model-logical and optimizer-logical digests for bundle identity. These separate digests do not replace the R2E combined-state authority.

## 5. Logical checkpoint layout

R3 publishes one checkpoint bundle directory:

```text
checkpoint_step_000001/
  model.safetensors
  optimizer.safetensors
  checkpoint_bundle_manifest.json
  model.safetensors.ASH_CHECKPOINT_EXPORT_PROVENANCE_R1J_CAPTURE_V1.json
```

`model.safetensors` contains exactly `201` logical model tensors.

`optimizer.safetensors` contains exactly `402` logical optimizer-state tensors:

- `optimizer.m.<parameter_id>` for 201 first moments
- `optimizer.v.<parameter_id>` for 201 second moments

Physical R2E Atlas chunks are transport/storage implementation details and MUST NOT become checkpoint tensor identities.

## 6. Dtype and numerical identity

Current R3 export authority is F32 identity serialization.

Forbidden during export:

- quantization
- F16/BF16 conversion
- renormalization
- weight folding
- weight tying
- tail-zero repair
- epsilon repair
- optimizer-state compression
- gradient payload export

Generation-1 bytes are serialized exactly as committed by R2E.

## 7. Bounded Atlas checkpoint streaming

R3 MUST NOT materialize the full model or full optimizer state in host memory.

Current stream chunk budget:

`16 MiB`

Each logical source file is read and copied in bounded chunks. Large tensors remain one logical safetensors tensor while being physically streamed through multiple bounded chunks.

Required receipt fields:

- `checkpoint_stream_chunk_bytes=16777216`
- `model_stream_chunk_count=<observed>`
- `optimizer_stream_chunk_count=<observed>`
- `full_model_materialization=0`
- `full_optimizer_materialization=0`

## 8. Safetensors header authority

Before payload write, R3 computes the complete logical header from:

- tensor identity
- exact F32 dtype
- exact logical shape
- exact byte span
- deterministic data offset

The header is padded to safetensors 8-byte alignment. Payload offsets are data-section-relative.

Post-write validation requires:

- tensor count exact
- every expected tensor present
- F32 exact
- shape exact
- no offset gap
- no offset overlap
- final payload end exactly equals physical file size
- no trailing bytes

## 9. Partial-to-final publication

R3 writes through create-new partial files:

- `model.safetensors.partial`
- `optimizer.safetensors.partial`

For each file:

1. create-new partial destination
2. write header
3. bounded sequential payload stream
4. flush
5. filesystem sync
6. post-write reopen validation on partial
7. physical SHA256
8. rename partial to final
9. post-rename reopen validation
10. physical SHA256 parity after rename

Existing partial or final files are fail-closed. There is no silent overwrite or automatic partial resume.

## 10. Physical file identities

R3 records actual byte SHA256 for:

- `model.safetensors`
- `optimizer.safetensors`

Path-derived or metadata-derived surrogate hashes are forbidden.

The physical file SHA256 is distinct from the logical generation/state digest. Both authorities are retained.

## 11. R1J live export capture

R3 requires:

`ASH_R1J_CAPTURE_CHECKPOINT_EXPORT=1`

The existing R1J schema is retained. R3 adds a streamed-generation capture path rather than inventing a parallel provenance schema.

The streamed R1J path consumes exact generation-1 candidate weight files and the physically written `model.safetensors`.

For the canonical 27 forensic decoder records it verifies:

- source tensor identity
- source layer/semantic role
- source shape
- source F32 byte count
- source payload SHA256
- pre-serialize zero/nonzero observations
- destination header identity
- destination offset/span
- actual bytes written
- post-write zero/nonzero observations
- post-write payload SHA256
- source-to-output digest parity

Current forensic target cardinality remains:

- 27 records
- 21 projection records
- 6 RMS-control records

## 12. R1J E0-E5 interpretation

R3 physical PASS requires the live export lifecycle to be closed:

- E0: committed training generation 1 is bound as source authority
- E1: streamed canonical model writer binding is established
- E2: complete 201-tensor pre-serialize coverage/digest plan exists
- E3: exact create-new model destination is bound
- E4: model byte stream completes and is synchronized
- E5: final model file is reopened, physically SHA256-digested, and tensor/header/payload parity is verified

Historical reconstruction is forbidden. Only the live R3 export event may satisfy this gate.

The R3 streamed R1J capture records the actual physical model-file SHA256 as `outputFileSha256Authority` and becomes authoritative only after the post-write validations pass.

## 13. Bundle manifest authority

`checkpoint_bundle_manifest.json` is published only after:

- model final exists and validates
- optimizer final exists and validates
- physical SHA256 for both files is complete
- generation-1 combined-state parity passes
- R1J capture is complete
- R1J physical model SHA256 equals R3 physical model SHA256

The manifest records:

- patch ID
- training generation `1`
- optimizer step `1`
- model spec ID
- tokenizer lineage ID
- dataset manifest ID
- parent checkpoint lineage
- parent checkpoint physical SHA256
- R2E candidate combined-state digest
- R2E training-step state digest
- configured gradient accumulation `8` as observed for the current physical run
- physical microbatch count `1`
- production accumulation adoption `0`
- raw gradient L2/max-abs evidence
- optimizer configuration
- model logical digest and physical SHA256
- optimizer-state logical digest and physical SHA256
- R1J provenance file identity and E0-E5 closure
- publication state `COMMITTED`

The bundle manifest is the canonical checkpoint publication boundary. Orphan model/optimizer files without the committed manifest are not a canonical checkpoint bundle.

## 14. Training mutation firewall

R3 is serialization/provenance only.

Required:

- training generation before export: `1`
- training generation after export: `1`
- optimizer step before export: `1`
- optimizer step after export: `1`
- weight mutation: `0`
- optimizer-state mutation: `0`
- forward count: `0`
- backward count: `0`
- optimizer step count inside R3: `0`
- scheduler commit count: `0`
- generation 2 creation: `0`

## 15. Structural gate

Structural contract flags:

`--require-bt-wgsl-r27r1j-r3-contract-001` through `048`.

Required:

- gate count `48`
- exact cardinality
- no gaps
- no duplicates

Structural R3 does not perform physical export. It proves only that the bridge contract is closed while physical export remains not requested:

- `committed_generation_checkpoint_export_bridge_ready=1`
- `physical_checkpoint_export_pass=0`
- `checkpoint_export_count=0`
- `r1j_live_export_event_count=0`

## 16. Receipt Atlas

R3 physical receipt uses exactly `33` deterministic waves.

Receipt rules:

- each wave contains at most 8 fields
- parallel JSON chunk build
- deterministic ordinal sort
- sequential wave write
- duplicate-key fail closed
- final summary is not used as a monolithic payload carrier

The structural gate uses the same 33-wave authority shape.

## 17. Semantic canaries

R3 carries at least 90 semantic negative canaries. Current implementation cardinality: `90`.

Key failures include:

- missing R2E physical parent
- non-COMMITTED source
- generation not 1
- optimizer step not 1
- candidate manifest digest mismatch
- combined generation-state digest mismatch
- model tensor count not 201
- optimizer tensor count not 402
- source file digest mismatch
- source byte-count mismatch
- hidden dtype conversion
- offset gap/overlap/reorder
- full model/optimizer materialization
- destination overwrite
- partial auto-resume
- truncated/trailing physical file
- skipped post-write reopen
- physical SHA drift
- R1J capture disabled
- any missing E0-E5 stage
- R1J physical digest mismatch
- manifest publication before R1J E5
- generation/optimizer-step mutation during export
- forward/backward/optimizer/scheduler execution
- gradient payload export
- accumulation rewritten to 32
- generation2 creation

## 18. Physical runtime receipt minimum

Successful R3 must report:

- `r27r1jr2e_physical_parent=1`
- `explicit_checkpoint_export_requested=1`
- `source_training_generation=1`
- `source_optimizer_step=1`
- `source_transaction_state=COMMITTED`
- `logical_model_tensor_count=201`
- `logical_optimizer_state_tensor_count=402`
- missing/duplicate counts `0`
- bounded stream chunk size and observed chunk counts
- full materialization counts `0`
- model checkpoint write count `1`
- optimizer checkpoint write count `1`
- actual physical SHA256 for both files
- generation-1 combined-state digest parity `1`
- R1J E0-E5 all `1`
- R1J real export event `1`
- bundle manifest valid `1`
- bundle publication count `1`
- generation remains `1`
- optimizer step remains `1`
- configured gradient accumulation inherited from R2E, current physical SSOT `8`
- physical microbatch accumulation count `1`
- production accumulation adoption `0`
- all R3 training mutation counters `0`
- receipt Atlas waves `33`

## 19. PASS / HOLD

Physical PASS token:

`PASS_ASH_BASETRAIN_BT_WGSL_ATLAS_RUNTIME_COMMITTED_GENERATION_CHECKPOINT_EXPORT_06C_R27_R1J_R3`

Successful authority-boundary HOLD:

`HOLD_ASH_BASETRAIN_R1J_R3_GENERATION1_CHECKPOINT_BUNDLE_EXPORTED_R1J_E0_TO_E5_PROVENANCE_COMPLETE_RELOAD_CONTINUATION_NOT_YET_ADMITTED`

An exit code 1 caused only by this exact HOLD after the PASS token is an intended terminal boundary.

## 20. PASS meaning

R3 PASS means the physically committed R2E generation-1 runtime state, not a reconstructed substitute, was serialized into an exact 201-tensor model checkpoint and 402-tensor AdamW optimizer-state checkpoint through bounded streaming. Both files were reopened and physically SHA256-verified, the combined generation-1 state remained bound to the R2E digest, the live R1J E0-E5 writer provenance completed against the actual model bytes, and only then was the checkpoint bundle manifest atomically published.

R3 PASS does not mean reload parity, optimizer step 2, multi-step training, production 8-microbatch accumulation, or scheduler/warmup progression has been admitted.

## 21. Next frontier

Next patch:

`ASH-BASETRAIN-BT-WGSL-CHECKPOINT-RELOAD-PARITY-AND-STEP2-CONTINUATION-06C-R27-R1J-R4`

R4 must start from a fresh process and prove:

- model checkpoint reload: 201/201
- optimizer-state reload: 402/402
- training generation: 1
- optimizer step: 1
- exact logical parity with the R3 bundle manifest
- no genesis fallback
- no zero-moment fallback
- no silent checkpoint repair

Only after reload parity is proven may step-2 continuation be admitted.

## 22. SSOT seal

R2E creates generation 1.
R3 does not recreate it.

The committed runtime store is the source.
Atlas chunks are transport, not checkpoint tensor identity.

Model checkpoint: 201 logical tensors.
Optimizer checkpoint: 402 logical m/v tensors.

No full model materialization.
No full optimizer materialization.
No numerical transformation.
No tail repair.

A partial file is not a checkpoint.
A model file alone is not a checkpoint bundle.
R1J E5 must complete before bundle publication.

Generation stays 1.
Optimizer step stays 1.
No new training math executes inside R3.

The R3 boundary is:

`REAL GENERATION 1 -> REAL SAFETENSORS BYTES -> REAL PHYSICAL SHA256 -> REAL R1J E0-E5 -> CANONICAL CHECKPOINT BUNDLE`
