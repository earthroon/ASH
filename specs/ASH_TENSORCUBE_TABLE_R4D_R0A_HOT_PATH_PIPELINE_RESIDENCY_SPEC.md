# TENSORCUBE-TABLE-R4D-R0A

## HOT-PATH PIPELINE RESIDENCY

```text
TENSORCUBE-TABLE-R4D-R0A

HOT-PATH PIPELINE RESIDENCY

+ HEADWISE DISPATCHER PERSISTENT RUNTIME
+ R14 RMSNORM BACKWARD PIPELINE RESIDENCY
+ R15 ROPE BACKWARD PIPELINE RESIDENCY
+ G204D ATTENTION BACKWARD PIPELINE RESIDENCY
+ GRADIENT OBSERVER PIPELINE RESIDENCY
+ GRADIENT SUM-SQUARE PIPELINE RESIDENCY
+ R6 ACCUMULATOR PIPELINE RESIDENCY
+ DEVICE / QUEUE / RUNTIME-GENERATION BINDING
+ LEGACY COMPATIBILITY WRAPPERS
+ BOUNDED PIPELINE CREATION RECEIPT
+ NO READBACK POLICY CHANGE
+ NO WGSL / NUMERICAL MATH CHANGE
+ NO NEW GPU SYNCHRONIZATION
```

## 1. Purpose

R0A removes repeated CPU-side shader-module / compute-pipeline / dispatcher construction from the production hot path before changing any readback or observability semantics.

Parent:

```text
TENSORCUBE-TABLE-R4C-CF6
DIRECT / BOUNDED WEIGHT UPLOAD
```

This revision is the first implementation step of the CPU/host-intervention-collapse roadmap. R0B gradient-observability aggregation, CF7 VRAM hot-weight reuse, CF8 validation receipt caching, AdamW status aggregation, durable projection copy collapse, and durability I/O compaction are explicitly out of scope here.

## 2. Evidence Separation

R0A changes only pipeline lifetime / construction authority.

It does not change:

```text
map/readback timing
Poll(Wait) cardinality
gradient observability semantics
finite guard semantics
AdamW status semantics
weight H2D policy
durability policy
```

This keeps R0A performance attribution separable from R0B and later revisions.

## 3. Runtime Mode

Environment:

```text
ASH_TENSORCUBE_TABLE_R4D_R0A_MODE
```

Accepted:

```text
OFF
OBSERVE
ACTIVE
```

Aliases accepted by the parser include `DISABLED`, `OBSERVE_ONLY`, and `ACTIVE_VERIFIED`.

Default when absent:

```text
OFF
```

The route-owned persistent runtime is materialized only when the mode is enabled.

The R6 gradient accumulator separately owns its pipelines for its accumulator lifetime as a structural local-lifetime repair; it does not introduce process-global state.

## 4. Canonical Runtime Authority

New module:

```text
crates/base_train/src/tensorcube_table_r4d_r0a_hot_path_pipeline_residency.rs
```

Canonical runtime:

```text
R4dR0aHotPathPipelineResidency
```

It owns:

```text
HeadwiseAtlasDispatcher
R14RmsNormBackwardPipelineRuntime
R15NeoXRopeBackwardPipelineRuntime
BaseTrainG204DAttentionBackwardPipeline
R27R1GradientObserverPipelineRuntime
R2DGradientSumSquaresPipelineRuntime
```

The runtime is bound to the existing physical runtime identity:

```text
runtime_generation
device_authority_id
queue_authority_id
```

and validates `physical_runtime_binding_r1` before admission.

## 5. Headwise Dispatcher Residency

Production forward, final-output, and backward routes no longer instantiate a new `HeadwiseAtlasDispatcher` at each callsite when R0A is enabled.

They consume:

```text
r4d_r0a_headwise_dispatcher(...)
```

which returns either:

```text
Persistent(&HeadwiseAtlasDispatcher)
```

or the compatibility legacy dispatcher when R0A is off.

This allows the dispatcher's existing internal plan / pipeline / group-map / finite-guard caches to survive across hot calls within the route runtime lifetime.

No direct `HeadwiseAtlasDispatcher::from_runtime_handles(...)` call remains in the targeted production forward/final/backward files.

## 6. R14 RMSNorm Backward Residency

`base_train_r14_post_rmsnorm_backward.rs` now exposes:

```text
R14RmsNormBackwardPipelineRuntime
```

which owns exactly the existing three compute-pipeline families:

```text
row-dot
DX
DGamma
```

New runtime-aware calls reuse those pipelines. Legacy public wrappers remain and construct a temporary runtime for compatibility / non-R0A callers.

No RMSNorm formula, dispatch geometry, binding contract, readback, or diagnostic policy is changed.

## 7. R15 NeoX RoPE Backward Residency

`base_train_r15_neox_rope_backward.rs` now exposes:

```text
R15NeoXRopeBackwardPipelineRuntime
```

and a runtime-aware backward entrypoint.

The production real-loss backward path uses the resident runtime for both Q and K RoPE backward calls when R0A is enabled.

No RoPE numerical semantics change.

## 8. G204D Attention Backward Residency

The already-existing:

```text
BaseTrainG204DAttentionBackwardPipeline
```

is moved under the R0A route-owned runtime instead of being recreated by each production live call.

R0A routes production calls through the persistent instance's `run_live(...)` authority.

No G204D readback or status semantics change.

## 9. Gradient Observer Residency

`base_train_r27r1_gradient_observability.rs` now exposes:

```text
R27R1GradientObserverPipelineRuntime
```

and a runtime-aware observation entrypoint.

This revision only reuses the shader/pipeline. The existing compact observation readback and its synchronization remain unchanged and are intentionally reserved for R0B.

## 10. Gradient Sum-Square Residency

`base_train_r2d_gradient_stream.rs` now exposes:

```text
R2DGradientSumSquaresPipelineRuntime
```

holding the partial and reduce pipelines.

The real-loss backward and post-wave scheduler observation paths route through the same R0A runtime when available.

The sum-square readback policy is unchanged.

## 11. Wave Lifetime Propagation

`R6AR1WaveResidentStepExecution` carries:

```text
Option<Arc<R4dR0aHotPathPipelineResidency>>
```

from the route context into the scheduler observation stage.

This prevents the post-wave accumulated-gradient observer from falling back to newly-created observer/sum-square pipelines after the main route already established R0A residency.

The Arc carries pipeline/runtime identity only. It does not retain source checkpoint weight ranges or generation payloads.

## 12. R6 Gradient Accumulator Residency

`R6DeviceGradientAccumulator` now creates and owns its three existing pipeline families in its constructor:

```text
dense accumulation
sparse accumulation
finalize
```

The accumulator hot methods reuse those fields rather than repeatedly calling `make_pipeline(...)`.

Creation accounting is fixed to:

```text
shader_module_creation_count = 3
pipeline_creation_count = 3
```

per accumulator construction.

This is bounded by accumulator lifetime and does not create a global pipeline registry.

## 13. Compatibility Law

Existing public backend entrypoints remain available.

For R14, R15, R27 observer, and R2D sum-square:

```text
legacy entrypoint
    -> temporary runtime
    -> same existing dispatch semantics
```

Production R0A-enabled routes instead inject the persistent runtime.

No test/oracle caller is forced to adopt the new runtime immediately.

## 14. Pipeline Creation Accounting

Route-owned R0A fixed backend pipeline construction per runtime is recorded as:

```text
R14       3
R15       1
G204D     2
R27       1
R2D sumsq 2
----------------
fixed     9
```

Headwise dispatcher internal pipelines remain lazily created by its pre-existing cache and are not falsely counted as nine fixed pipelines.

R0A receipt separately records:

```text
runtime_create_count
headwise_dispatcher_create_count
headwise_dispatch_count
r14_pipeline_create_count
r14_dispatch_group_count
r15_pipeline_create_count
r15_dispatch_count
g204d_pipeline_create_count
g204d_dispatch_count
gradient_observer_pipeline_create_count
gradient_observer_dispatch_count
gradient_sumsq_pipeline_create_count
gradient_sumsq_dispatch_count
r6_accumulator_shader_module_create_count
r6_accumulator_pipeline_create_count
```

## 15. ACTIVE Fail-Closed Law

In ACTIVE mode, the receipt fails if:

```text
persistent runtime was not exercised
fixed route-owned pipeline counts drift
R6 accumulator pipeline construction is unbounded / absent
```

Failure classes include:

```text
FAIL_R4D_R0A_PIPELINE_RESIDENCY_NOT_EXERCISED
FAIL_R4D_R0A_PIPELINE_CREATION_DRIFT
FAIL_R4D_R0A_R6_PIPELINE_CREATION_UNBOUNDED
```

## 16. Terminal Receipt

Receipt:

```text
tensorcube_table_r4d_r0a_hot_path_pipeline_residency_receipt.json
```

Compact log:

```text
[ASH-TENSORCUBE-TABLE-R4D-R0A][hot-path-pipeline-residency]
```

Pass token:

```text
PASS_TENSORCUBE_TABLE_R4D_R0A_HOT_PATH_PIPELINE_RESIDENCY
```

Physical/performance hold token:

```text
HOLD_TENSORCUBE_TABLE_R4D_R0A_PHYSICAL_PERFORMANCE_UNVERIFIED
```

The hold token explicitly prevents SOURCE/STATIC evidence from being interpreted as a measured speedup.

## 17. No New Synchronization

The new R0A orchestration module contains no new:

```text
map_async
get_mapped_range
device.poll
PollType::Wait
queue.submit
copy_buffer_to_buffer
```

Existing backend synchronization remains in the existing backend implementation and is unchanged by R0A.

R0B owns readback/synchronization aggregation.

## 18. No Numerical / WGSL Change

R0A changes lifetime and reuse only.

Unchanged:

```text
optimizer math
Muon math
AdamW math
RMSNorm math
RoPE math
attention backward math
gradient reduction math
WGSL sources
TensorCube kernels
checkpoint format
generation identity
CF5 / CF6 weight loading
B06 commit evidence
CF11 source retirement
```

## 19. Actual Code Delta

```text
MOD 12
ADD 2
DEL 0
```

Modified:

```text
crates/base_train/src/atlas_runtime_final_output_real_loss.rs
crates/base_train/src/atlas_runtime_forward_wave_execution.rs
crates/base_train/src/atlas_runtime_real_loss_backward.rs
crates/base_train/src/atlas_runtime_route_admission.rs
crates/base_train/src/lib.rs
crates/base_train/src/packed_runtime_native_bootstrap_accumulation_wave_residency.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/burn_webgpu_backend/src/base_train_r14_post_rmsnorm_backward.rs
crates/burn_webgpu_backend/src/base_train_r15_neox_rope_backward.rs
crates/burn_webgpu_backend/src/base_train_r27r1_gradient_observability.rs
crates/burn_webgpu_backend/src/base_train_r2d_gradient_stream.rs
crates/burn_webgpu_backend/src/base_train_r6_gradient_accumulator.rs
```

Added:

```text
crates/base_train/src/tensorcube_table_r4d_r0a_hot_path_pipeline_residency.rs
tools/validate_ash_tensorcube_table_r4d_r0a_hot_path_pipeline_residency_static.py
```

## 20. Build Graph Preservation

```text
Cargo.toml byte-identical
Cargo.lock byte-identical
WGSL baseline files = 320
WGSL changed = 0
```

## 21. Static Acceptance

Executed in bake environment:

```text
PASS_TENSORCUBE_TABLE_R4D_R0A_HOT_PATH_PIPELINE_RESIDENCY_STATIC checks=104
PASS_TENSORCUBE_TABLE_R4C_CF6_DIRECT_BOUNDED_WEIGHT_UPLOAD_STATIC checks=135
PASS_TENSORCUBE_TABLE_R4C_CF5_HOST_COPY_COLLAPSE_STATIC checks=127
PASS_TENSORCUBE_TABLE_R4C_CF4_HOST_DEVICE_IO_ROUNDTRIP_ATTRIBUTION_STATIC checks=67
PASS_TENSORCUBE_TABLE_R4C_CF3_SLOT_LIFECYCLE_STATIC checks=77
PASS_TENSORCUBE_TABLE_R4B_CF3_FULL_ROUTE_HOST_LEDGER_COMPACTION_STATIC checks=127
PASS_TENSORCUBE_TABLE_R1_CF1_IMMUTABLE_BYTE_ACCOUNTING_STATIC
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF1_STATIC checks=63
PASS_EVE_MCU_R3H_CF11_PAGED_COW_CANDIDATE_WEIGHT_SUCCESSOR_STATIC checks=64
```

## 22. Compile / Runtime Evidence State

Bake environment contains no Rust toolchain.

Therefore:

```text
SOURCE       BAKED
STATIC       PASS
COMPILE      UNVERIFIED IN BAKE ENVIRONMENT
RUNTIME      UNVERIFIED AFTER R0A
PHYSICAL     UNVERIFIED AFTER R0A
PERFORMANCE  UNVERIFIED
```

No compile, runtime, or performance claim is made from static evidence.

## 23. Source Seals

```text
d47f29334104abe630c8da72202eed25a19edab26f2a57646b4d785726b0232a  crates/base_train/src/atlas_runtime_final_output_real_loss.rs
26e8fecc0bf6d3818d03c9df62fe4d4d3a6745300212fcd6cc54face87c270a5  crates/base_train/src/atlas_runtime_forward_wave_execution.rs
df84c02d8e824be78745d431076ee9bc450289ebe5f54998fe03fd221a2ecf7f  crates/base_train/src/atlas_runtime_real_loss_backward.rs
9dd4e406db5223eff4902bca38dcda88e68917687daf2044a5ab5b44158e038a  crates/base_train/src/atlas_runtime_route_admission.rs
df45f0633318d9066a2b50194048e25781ac1f0346faa6bfc66ffd0a3f0946ae  crates/base_train/src/lib.rs
b5db339dd833da703831178a807fe55f07a2b18137a2674d128ef03824fd3b7d  crates/base_train/src/packed_runtime_native_bootstrap_accumulation_wave_residency.rs
96df12edebb3596c0fa93f1c7dacb43e787457ca5ea2a73de8d2b49f2cef202d  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
9073d273cbcaadadad48bed00cff669fbe3ce4840b8fdc1087c4fe455bbae631  crates/burn_webgpu_backend/src/base_train_r14_post_rmsnorm_backward.rs
01ae7423f5c5274e85584890e11194946109ae5d16762f1cb40dd5434962db56  crates/burn_webgpu_backend/src/base_train_r15_neox_rope_backward.rs
072e20ded4c93e799ec28e1938b8dff805dc29cd46cdd0202f9738beedfaad1d  crates/burn_webgpu_backend/src/base_train_r27r1_gradient_observability.rs
97116812aa534e117a276566397582cdc11194a906ef331f25f8876702b82170  crates/burn_webgpu_backend/src/base_train_r2d_gradient_stream.rs
345e90eb8dfd62d43407a15ebf68e29880002a52cbe2ee44d31fa5b4946f3bef  crates/burn_webgpu_backend/src/base_train_r6_gradient_accumulator.rs
5b3329f1c052cca68d9c008d7f3a68cebce2f3770403c5a8662c752918f06987  crates/base_train/src/tensorcube_table_r4d_r0a_hot_path_pipeline_residency.rs
ae351ef8916cc76fd4136d4c838baa7b92cb474ad2ed0e4efed699e2d126821d  tools/validate_ash_tensorcube_table_r4d_r0a_hot_path_pipeline_residency_static.py
```

## 24. Artifact Seals

```text
Overlay code-only ZIP
SHA-256 7c8acd16545c6ed81a12e68b958a2d79c93b5f371c95ba811df39af4279edb2d
files=14
CRC=PASS

Full code-only ZIP
SHA-256 42c45b9afd077f82f83fa61b48ca6fec452474ee73a8696c215be2ae46687a06
files=8518
CRC=PASS
```

## 25. Local Compile Acceptance

Required on authoritative Windows source tree:

```powershell
cargo check `
  -p burn_webgpu_backend `
  --lib `
  --release `
  --locked `
  -j 1

cargo check `
  -p base_train `
  --lib `
  --release `
  --locked `
  -j 1

cargo build `
  -p base_train `
  --bin base_train `
  --release `
  --locked `
  -j 1
```

## 26. Physical Acceptance

Run with:

```text
ASH_TENSORCUBE_TABLE_R4D_R0A_MODE=ACTIVE
```

Same-source canary must establish:

```text
runtime_create_count > 0
headwise_dispatcher_create_count == runtime_create_count
headwise_dispatch_count > 0
r14_pipeline_create_count == runtime_create_count * 3
r14_dispatch_group_count > 0
r15_pipeline_create_count == runtime_create_count
r15_dispatch_count > 0
g204d_pipeline_create_count == runtime_create_count * 2
g204d_dispatch_count > 0
gradient_observer_pipeline_create_count == runtime_create_count
gradient_observer_dispatch_count > 0
gradient_sumsq_pipeline_create_count == runtime_create_count * 2
gradient_sumsq_dispatch_count > 0
R6 pipeline creation bounded per accumulator
no new readback policy change
```

## 27. Performance Acceptance

Compare same-source parent CF6 against R0A with identical runtime/log policy.

Measure at minimum:

```text
pipeline creation count
shader module creation count
dispatch count
CPU process time
optimizer-step wall time
generation wall time
```

No exact speedup percentage may be claimed before that physical A/B.

## 28. Successor

Next revision:

```text
TENSORCUBE-TABLE-R4D-R0B
GRADIENT OBSERVABILITY DEVICE AGGREGATION

+ per-gradient immediate readback removal
+ GPU nonfinite/nonzero/max_abs/sumsq ledger
+ optimizer-step bounded readback
+ immediate-safety-critical classification preservation
```

R0B may begin only after R0A compile/runtime authority is available, because R0B should aggregate observations over resident pipelines instead of simultaneously changing pipeline construction and synchronization.

## 29. Final Law

> Pipeline construction is configuration, not training work. A shader/pipeline whose device, layout, specialization, and runtime-generation identity are unchanged must be retained by a bounded runtime owner instead of rebuilt for every lane, layer, gradient, or observation.

> R0A moves pipeline lifetime without moving correctness barriers. Readback aggregation belongs to R0B.
