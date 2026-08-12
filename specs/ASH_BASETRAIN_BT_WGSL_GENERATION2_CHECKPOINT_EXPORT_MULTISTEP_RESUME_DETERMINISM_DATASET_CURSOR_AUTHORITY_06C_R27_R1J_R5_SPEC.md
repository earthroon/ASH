# ASH-BASETRAIN-BT-WGSL-GENERATION2-CHECKPOINT-EXPORT-MULTISTEP-RESUME-DETERMINISM-DATASET-CURSOR-AUTHORITY-06C-R27-R1J-R5

## 0. Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-GENERATION2-CHECKPOINT-EXPORT-MULTISTEP-RESUME-DETERMINISM-DATASET-CURSOR-AUTHORITY-06C-R27-R1J-R5`
- Build revision: `bt-wgsl-generation2-checkpoint-export-multistep-resume-determinism-dataset-cursor-authority-06c-r27-r1j-r5`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-CHECKPOINT-RELOAD-PARITY-AND-STEP2-CONTINUATION-06C-R27-R1J-R4`
- Input authority: R4 committed training generation `2`, optimizer step `2`
- Export authority: generation-2 model/optimizer checkpoint bundle, dataset cursor V1, new live R1J E0-E5 event
- Determinism authority: two independent fresh-process step-3 probes from the exact same generation-2 bundle
- Promotion authority: exact compare barrier followed by primary-only generation `2 -> 3`, optimizer step `2 -> 3`, cursor revision `1 -> 2`
- Generation-3 checkpoint export: CLOSED
- Production accumulation/scheduler/multistep loop: CLOSED

## 1. R4 physical parent SSOT

R5 starts only from the physically passed R4 state:

- fresh process reload `1`
- R3 model/optimizer physical and logical parity `1`
- genesis fallback `0`
- zero-moment fallback `0`
- optimizer state origin `RELOADED_R3_STEP1_STATE`
- configured gradient accumulation `8`
- physical microbatch accumulation `1`
- production accumulation adoption `0`
- step1 batch ordinal `0`
- step2 batch ordinal `1`
- step2 logical gradient tensors `201`
- generation transition `1 -> 2`
- optimizer step transition `1 -> 2`
- generation-2 checkpoint write/export at R4 `0`

R5 exports the already committed generation-2 runtime state. It never rebuilds generation2 from R3, gradients, or deltas.

## 2. Four physical roles

R5 is deliberately split into four separate `base_train` invocations:

1. generation2 export plus cursor genesis adoption
2. fresh-process probe `primary`
3. fresh-process probe `shadow`
4. exact compare plus primary-only canonical promotion

Primary and shadow use different process IDs and output directories. R5 does not claim cross-GPU, cross-driver, or distributed bit determinism.

## 3. CLI contracts

### Export

- `--r5-parent-r4-run-dir <R4 output>`
- `--admit-generation2-checkpoint-export`

Export forbids genesis init, resume bundle, R2E/R3/R4 runtime admissions, and Atlas forward/loss/backward execution.

### Probe

- `--resume-checkpoint-bundle <R5 checkpoint_step_000002>`
- `--admit-r5-resume-determinism-probe`
- `--r5-determinism-run-role primary|shadow`
- `--admit-atlas-runtime-route`
- `--admit-atlas-forward-wave-execution`
- `--admit-atlas-final-output-real-loss`
- `--admit-atlas-real-loss-backward`

Probe forbids genesis init, inherited external Atlas plan files, R4 reload/step2 admission, R2E optimizer admission, and R3 export admission.

### Compare

- `--resume-checkpoint-bundle <same R5 checkpoint_step_000002>`
- `--admit-r5-resume-determinism-compare`
- `--r5-determinism-primary-dir <primary output>`
- `--r5-determinism-shadow-dir <shadow output>`

Compare performs no forward/loss/backward and forbids training-runtime admissions. Exactly one R5 role is admitted per invocation.

## 4. Generation2 source authority

Export reads the R4 physical runtime receipt and requires:

- R4 step2 PASS token
- generation after R4 `2`
- optimizer step after R4 `2`
- candidate parameter count `201`
- candidate gap/duplicate `0`
- checkpoint write/export in R4 `0`
- step1/step2 batch ordinal evidence `0` and `1`

It then reads R4 `training_state/active_training_generation.json`, resolves the committed candidate directory, verifies the candidate manifest physical SHA256, and recomputes the exact generation2 weight/m2/v2 combined state digest. Source transaction state MUST be `COMMITTED`.

## 5. Generation2 checkpoint layout

R5 export publishes:

```text
checkpoint_step_000002/
  model.safetensors
  optimizer.safetensors
  dataset_cursor.json
  checkpoint_bundle_manifest.json
  model.safetensors.ASH_CHECKPOINT_EXPORT_PROVENANCE_R1J_CAPTURE_V1.json
```

Logical tensor authority:

- model `201`
- optimizer m2 `201`
- optimizer v2 `201`
- total optimizer state `402`

Atlas chunks are transport only and are never exposed as checkpoint tensor identities.

## 6. Writer reuse and bounded export

R5 reuses the R3 canonical streaming safetensors writer through crate-local helpers. It does not introduce a second serialization authority.

Required:

- stream chunk budget `16 MiB`
- full model materialization `0`
- full optimizer materialization `0`
- no quantization or dtype conversion
- no tail-zero repair
- no weight tying
- no optimizer-state compression
- create-new destination semantics
- bounded sequential payload writes
- flush and filesystem sync
- final physical SHA256

## 7. Generation2 R1J event

Export requires `ASH_R1J_CAPTURE_CHECKPOINT_EXPORT=1`.

Generation2 receives a new live R1J event. R3 generation1 provenance cannot satisfy R5.

Required stages:

- E0 committed generation2 source
- E1 canonical writer binding
- E2 201-tensor pre-serialize coverage
- E3 exact generation2 destination
- E4 physical write completion
- E5 final physical file digest and payload parity

R1J model SHA256 authority must equal the actual R5 `model.safetensors` SHA256.

## 8. Dataset Cursor V1

R5 introduces persisted cursor schema:

`ash.basetrain.dataset_cursor.v1`

It binds:

- dataset manifest ID and physical SHA256
- train split and dataset builder identity
- tokenizer lineage
- consumed batch count
- last committed batch ordinal
- next batch ordinal
- training generation
- optimizer step
- last batch digest
- cursor revision
- parent cursor digest
- cursor digest

## 9. One-time cursor genesis adoption

R3 did not persist a dataset cursor, and R4 explicitly used deterministic batch ordinals rather than fabricating one. R5 therefore permits exactly one named adoption:

`CURSOR_GENESIS_ADOPTION_FROM_R4_PHYSICAL_CHAIN`

Generation2 cursor state:

- consumed batch count `2`
- last committed ordinal `1`
- next ordinal `2`
- training generation `2`
- optimizer step `2`
- cursor revision `1`

The ordinal1 batch digest is independently rebuilt from the same deterministic train batch builder. It is not represented as previously persisted R4 state.

## 10. Dataset authority

The cursor binds physical dataset-manifest SHA256 and a dataset-builder identity, preventing the same ordinal from silently resolving under a changed builder contract.

R5 keeps random sampling, shuffle, automatic wraparound and implicit epoch transition CLOSED.

Reading the cursor never advances it. Cursor movement occurs only through a successful canonical training commit.

## 11. Generation2 bundle authority

`checkpoint_bundle_manifest.json` uses schema `ash.basetrain.checkpoint_bundle.r5.v1` and publication state `COMMITTED`.

It binds:

- generation `2`
- optimizer step `2`
- model/tokenizer/dataset lineage
- R4 generation2 candidate digest and training-step digest
- optimizer configuration and configured accumulation
- model logical digest and physical SHA256
- optimizer logical digest and physical SHA256
- cursor digest and physical SHA256
- cursor last ordinal `1`, next ordinal `2`
- generation2 R1J provenance

A bundle without a valid cursor is not a canonical R5 resume bundle.

## 12. Fresh-process probe preflight

Primary and shadow consume the exact same R5 bundle path. Each independently validates:

- bundle schema and committed publication state
- generation `2`, optimizer step `2`
- model, optimizer and cursor physical SHA256
- cursor internal digest
- dataset manifest physical SHA256
- model logical digest
- optimizer logical digest
- combined generation2 weight/m2/v2 digest
- R1J sidecar complete, authoritative and model-SHA-bound

## 13. Runtime fingerprint scope

R5 records a fingerprint from the current build revision, R5 step3 shader digest, WGPU device feature/limit material, backend identity and subgroup-size contract.

Primary and shadow require exact fingerprint parity. This is a same-runtime-fingerprint claim only. Cross-device or cross-driver determinism is not inferred.

## 14. Generation-aware Atlas plan

Each probe materializes a new production Atlas plan from generation2 `model.safetensors`. Genesis physical byte ranges are never reused. Primary and shadow must produce identical plan-set digests.

## 15. Step3 batch authority

Both probes deterministically build the first three train microbatches and consume ordinal `2` exactly.

Required:

- source cursor next ordinal `2`
- step3 ordinal `2`
- primary/shadow batch digest exact parity
- random fallback `0`

If ordinal2 does not exist, execution fails closed rather than rewinding or choosing another batch.

## 16. Real step3 forward/loss/backward

The existing R2B/R2C/R2D production math path is reused.

Each probe independently performs:

- real generation2 forward
- real final output/loss
- real backward
- logical gradients `201`
- missing gradients `0`
- nonfinite gradients `0`
- nonfinite adjoints `0`

Loss improvement is not a correctness condition.

## 17. Gradient replay and observability

The first step3 R2D pass provides compact gradient observability. Full production gradient readback remains `0`.

Each probe performs exactly one deterministic backward replay to feed live GPU gradient waves into the optimizer candidate sink. Replay parity includes exact tensor counts, global nonzero count, raw L2 bits, max-abs bits and tail classification.

R5 does not read the complete raw gradient payload to establish determinism. The exact final generation3 candidate state digest provides the whole-state barrier.

## 18. Step3 optimizer source

Optimizer state origin is exactly:

`RELOADED_R5_GENERATION2_STEP2_STATE`

For every parameter, step3 consumes generation2 weight, m2, v2 and the live step3 gradient. Zero-moment fallback is forbidden.

## 19. AdamW step3

The R5 WGSL kernel uses:

- `m3 = beta1*m2 + (1-beta1)*g3`
- `v3 = beta2*v2 + (1-beta2)*g3^2`
- denominator `1-beta1^3`
- denominator `1-beta2^3`
- decoupled AdamW weight decay

Step1 or step2 bias-correction denominators are forbidden.

## 20. Micro-Atlas continuation

R5 retains:

- macro stream chunk `16 MiB`
- micro tile target `65,536` elements
- workgroup size `64`
- target X workgroups `1024`
- dispatch axes each `<= 65,535`
- dispatch-axis violation `0`

Dense gradients use bounded sub-leases. Sparse embedding continuation remains row-aligned so untouched rows can still receive decoupled weight decay with logical zero gradient.

## 21. Probe candidate staging

Each probe writes to its own `candidate_step_000003/` and produces exactly 201 generation3 candidate weights plus m3/v3 states, exact coverage ranges, update observability and physical digests.

Candidate transaction ends at `VALIDATED`.

Before compare:

- primary canonical generation promotion `0`
- primary cursor promotion `0`
- shadow canonical generation promotion `0`
- shadow cursor promotion `0`

## 22. Cursor candidate

Each probe creates cursor candidate:

- revision `2`
- consumed batch count `3`
- last committed ordinal `2`
- next ordinal `3`
- training generation `3`
- optimizer step `3`
- actual step3 batch digest
- parent generation2 cursor digest

The cursor candidate digest must be exact between probes.

## 23. Exact determinism barrier

Compare requires exact parity for:

- source bundle path and physical identities
- runtime fingerprint, device material, shader digest and subgroup contract
- Atlas plan-set digest
- step3 batch digest
- step3 loss raw bits
- compact gradient observability digest
- raw gradient L2 and max-abs bits
- generation3 candidate state digest
- candidate manifest digest
- cursor candidate digest/ordinals
- update nonzero count
- update L2 bits
- update max-abs bits

There is no epsilon or close-enough acceptance.

## 24. Source bundle immutability

Compare does not trust probe receipts alone. Before promotion it re-hashes the actual source bundle manifest, generation2 model file, optimizer file and cursor file and binds them to the primary receipt. After promotion it hashes all four again and requires zero source mutation.

## 25. Primary-only promotion

Only after the exact compare barrier closes does compare copy the primary `VALIDATED` candidate to its canonical output state. Candidate manifest and cursor-candidate digests are revalidated after copying.

The shadow candidate is never promoted or copied into canonical training state.

## 26. Atomic generation3 / step3 / cursor3 commit

Compare publishes `training_state/active_training_state.json` with schema `ash.basetrain.training_state.v2`.

Required committed authority:

- generation `3`
- optimizer step `3`
- candidate directory `candidate_step_000003`
- exact primary parameter-set and manifest digests
- optimizer state origin `RELOADED_R5_GENERATION2_STEP2_STATE`
- cursor revision `2`
- cursor last ordinal `2`
- cursor next ordinal `3`
- cursor consumed count `3`
- primary/shadow determinism evidence references

The active-state temporary file is create-new, flushed, filesystem-synced and atomically renamed.

## 27. Exactly-once cursor semantics

Before successful compare, canonical resume authority remains generation2/step2/cursor-next2. A failed probe or compare therefore retries ordinal2.

After atomic promotion, generation3/step3/cursor-next3 are one authority and ordinal2 must not be replayed as canonical work.

Orphan candidates are never auto-adopted.

## 28. Closed authorities

R5 keeps closed:

- generation3 checkpoint write/export
- R1J writer event during probes and compare
- production gradient accumulation
- scheduler/warmup commit
- shuffled/epoch traversal
- full model/optimizer materialization
- full gradient payload readback
- unrestricted continuous training loop

## 29. Receipt and structural contracts

Full comparison receipt Atlas: exactly `48` waves.

Structural R5 bridge: exactly `48` waves.

Structural gates:

`--require-bt-wgsl-r27r1j-r5-contract-001=true`
through
`--require-bt-wgsl-r27r1j-r5-contract-064=true`

Gate count `64`, no gaps or duplicates.

Current semantic observations:

- policy assertions `11`
- negative semantic canaries `166`
- total semantic observations `177`

No recursion-limit workaround is introduced.

## 30. Export PASS/HOLD

PASS:

`PASS_ASH_BASETRAIN_BT_WGSL_GENERATION2_CHECKPOINT_EXPORT_AND_DATASET_CURSOR_AUTHORITY_06C_R27_R1J_R5`

HOLD:

`HOLD_ASH_BASETRAIN_R1J_R5_GENERATION2_CHECKPOINT_AND_CURSOR_AUTHORITY_READY_MULTISTEP_RESUME_DETERMINISM_NOT_YET_PROVEN`

Exit code 1 caused by this exact HOLD after PASS is intended.

## 31. Probe PASS/HOLD

PASS:

`PASS_ASH_BASETRAIN_BT_WGSL_R5_FRESH_PROCESS_STEP3_DETERMINISM_PROBE_06C_R27_R1J_R5`

HOLD:

`HOLD_ASH_BASETRAIN_R1J_R5_FRESH_PROCESS_STEP3_PROBE_COMPLETE_COMPARE_NOT_YET_ADMITTED`

Each probe is intentionally non-canonical before compare.

## 32. Full PASS/HOLD

PASS:

`PASS_ASH_BASETRAIN_BT_WGSL_GENERATION2_CHECKPOINT_EXPORT_MULTI_STEP_RESUME_DETERMINISM_DATASET_CURSOR_AUTHORITY_06C_R27_R1J_R5`

HOLD:

`HOLD_ASH_BASETRAIN_R1J_R5_GENERATION3_STEP3_AND_DATASET_CURSOR3_COMMITTED_PRODUCTION_MULTI_STEP_LOOP_NOT_YET_ADMITTED`

Exit code 1 after the exact PASS/HOLD pair is the intended terminal boundary.

## 33. PASS meaning

R5 full PASS means the physically committed R4 generation2/optimizer-step2 state was exported without reconstruction, a persisted cursor authority was explicitly adopted from the proven ordinal0/ordinal1 chain, and two independent fresh processes consumed the same generation2 bundle and exact ordinal2 batch under the same runtime fingerprint. They produced exactly matching step3 loss bits, compact gradient observability, generation3 weight/m3/v3 candidate state, cursor candidate and update observability. Only after this exact barrier did a separate compare invocation atomically publish the primary generation3/optimizer-step3/cursor-next3 state.

## 34. What R5 does not prove

R5 does not prove cross-GPU, cross-driver or distributed determinism; production accumulation of 8 microbatches; scheduler or warmup progression; shuffled/epoch traversal; generation3 checkpoint persistence; convergence; or unrestricted continuous BaseTrain.

## 35. Next frontier

Recommended next patch:

`ASH-BASETRAIN-BT-WGSL-PRODUCTION-MULTISTEP-LOOP-ACCUMULATION8-WARMUP-SCHEDULER-06C-R27-R1J-R6`

R6 may admit real 8-microbatch accumulation, warmup/scheduler authority, cursor-driven N-step continuous training, periodic checkpoint policy and crash-safe resume.

## 36. SSOT seal

R4 created generation2. R5 does not recreate it.

R5 persists generation2, m2/v2 and cursor2. Cursor history before R5 is not fabricated: the one-time adoption is explicitly derived from R4 ordinal0/ordinal1 evidence.

After adoption, cursor state is authoritative. Reading never advances it. Only canonical training commit advances it.

Primary and shadow are separate processes and separate mutable stores. Neither can promote generation3 before comparison.

Determinism is exact under the same admitted runtime fingerprint. There is no epsilon gate.

Generation3, optimizer step3 and cursor-next3 are one canonical transaction. Generation3 checkpoint export remains closed.

The R5 boundary is:

`REAL GENERATION2 -> CHECKPOINT2 + CURSOR2 -> FRESH STEP3 PRIMARY + FRESH STEP3 SHADOW -> EXACT COMPARE -> ATOMIC GENERATION3 + STEP3 + CURSOR3`
