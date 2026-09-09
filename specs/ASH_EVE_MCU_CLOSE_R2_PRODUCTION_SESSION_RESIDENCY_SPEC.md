# ASH-EVE-MCU-CLOSE-R2

## PRODUCTION SESSION RESIDENCY
### R13 immutable execution state + FFN cross-step lifetime + bounded status authority + generation-bound content refresh + F16 WGSL static closure

## 0. Revision

```text
Patch ID: ASH-EVE-MCU-CLOSE-R2
Parent: ASH_PASS3_WGPU26_VENDOR_R2_CUBECL_WGPU_EXACT_PATH_FORK_ACTIVATION_CODE_ONLY(1).zip
Parent SHA-256: 3193ceb019adb2d2518d6cb81a60aa95fbf92f626fae8015885d685e54f75cdb

Class:
  PRODUCTION RUNTIME LIFETIME REALIGNMENT
  SESSION RESIDENCY
  BOUNDED TRANSIENT RESOURCE AUTHORITY
  WGSL STATIC BLOCKER REPAIR

Algorithm change: NO
Optimizer math change: NO
R13 WGSL math change: NO
Mixed-precision policy change: NO
Checkpoint format change: NO
WGPU package graph change: NO
```

Two independent lanes are included:

```text
S0  F16 WGSL STATIC BLOCKER CLOSURE
R2  PRODUCTION SESSION RESIDENCY
```

## 1. Parent authority preserved

R2 extends the existing R4/R7 production authority. It does not add a competing session owner.

```text
Eve R3/R3G
Trainable Session R4/R4A
EVE-MCU-CLOSE-R1
MCU R7/R7A/R7B
HiMuon R8/R8A
ProductionMuonRuntime
resident weight pack / RAM Adam M/V
A01 SubmissionEpoch lease authority
A02 usage-segregated arena
A03 compact readback ring
FFN persistent content-key state machine
WGPU26-VENDOR-R2 package graph
P1B-CLOSE-R1 repairs
```

## 2. Confirmed parent defects

### R13

Parent `r13_linear_backward`, `r13_swiglu_backward`, and `r13_add2` create shader/pipeline objects inside individual calls. Production backward repeats those operations by layer, accumulation lane and optimizer step.

### FFN

`BaseTrainFfnTensorCubePersistentExecutor` is internally persistent, but parent route admission constructs it during route-context materialization. That does not establish cross-step/cross-invocation lifetime.

### F16 WGSL

These four sources use native `f16` and lacked `enable f16;` in the parent:

```text
base_train_tensorcube_local_muon_16x16_softmatrix16_subgroup32_e1_mixed_f16_f32_r7.wgsl
base_train_tensorcube_local_muon_16x16_softmatrix16_subgroup32_e1_mixed_f16_f32_r7_r8a_indexed.wgsl
base_train_tensorcube_local_muon_16x16_softmatrix16_subgroup32_e2_f16_r7.wgsl
base_train_tensorcube_local_muon_16x16_softmatrix16_subgroup32_e2_f16_r7_r8a_indexed.wgsl
```

Parent classification: `CONFLICT / STATIC`.

## 3. Session lifetime law

```text
TrainableSessionRuntimeR4
  -> TrainableSessionParkedRuntimeR4
       -> TrainableSessionExecutionResidencyR2
            -> Arc<BaseTrainFfnTensorCubePersistentExecutor>
            -> Arc<BaseTrainR13ExecutionRuntimeR2>
```

The R2 object is runtime-only, non-durable and non-checkpoint-authoritative.

Config adds:

```text
training.admit_eve_mcu_close_r2 = false
```

R2 Active requires R1, R4 owner/cross-invocation, R4A, R7 and R7B admissions. Missing parent authority is a rejection.

## 4. No hidden fallback

R2 Active rejects:

```text
missing session residency
partial FFN/R13 residency
Device/Queue identity drift
generation regression
restored R4 invocation without R2 residency
```

R2 Active must not silently reconstruct the old route-local FFN executor or stateless R13 path. The parent stateless functions remain available only to non-R2 consumers/tests.

## 5. R13 immutable execution state

`BaseTrainR13ExecutionRuntimeR2` owns session-resident:

```text
linear_dx BGL / pipeline
linear_dw BGL / pipeline
SwiGLU BGL / pipeline
add2 BGL / pipeline
bounded status buffers
Device / Queue identity
physical soft-subgroup binding
R2 telemetry
```

Production backward uses:

```text
r13_linear_backward_with_execution_r2
r13_swiglu_backward_with_execution_r2
r13_add2_with_execution_r2
```

The following WGSL math sources remain byte-identical to the parent:

```text
base_train_r13_linear_backward.wgsl
base_train_r13_swiglu_backward.wgsl
base_train_r13_add2.wgsl
```

Therefore R2 does not implement tiled GEMM, subgroup reduction, F16 conversion, fusion or a reduction-order change.

## 6. Bounded status + physical completion law

R13 session status capacity is fixed:

```text
EVE_MCU_CLOSE_R2_R13_STATUS_SLOT_COUNT = 4
```

A slot records in-use state, slot generation, status buffer and last `SubmissionEpoch`. Exhaustion is fail-visible:

```text
E_EVE_MCU_CLOSE_R2_STATUS_SLOT_EXHAUSTED
```

R2 reuses existing A01/A02/A03 authority:

```text
status producer submissions
 -> A01-tracked status-copy submission
 -> exact SubmissionEpoch completion
 -> map/read/unmap
 -> A01 release
 -> A03 reclaim
 -> R13 status slot Free
```

Training-generation advancement is never substituted for GPU completion. R2 intentionally keeps the exact wait; batching belongs to R2A.

## 7. FFN cross-step residency

`TrainableSessionExecutionResidencyR2::bind_or_materialize` creates FFN and R13 execution objects once, then reuses the same `Arc` instances after exact Device/Queue identity validation.

Route context may be rebuilt, but route reconstruction must not reconstruct those session-resident execution objects.

`base_train_ffn_tensorcube_persistent_executor.rs` required no source change. R2 reuses its existing handle validation and content-key/generation machinery and changes the owner above it.

## 8. Generation-bound content refresh

Allocation identity and content identity are distinct.

Existing FFN content-key authority remains intact, including:

```text
model_source_digest
model_spec_id
tensor_set_digest
layer_index
source_weight_generation
gate source identity digest
up source identity digest
packing revision
```

R2 tracks opened/active weight generation. `N -> N+1` may retain execution allocations while the FFN content-key machinery determines hit/repopulation. `N -> N-1` rejects with:

```text
E_EVE_MCU_CLOSE_R2_GENERATION_REGRESSION
```

## 9. Cross-invocation and final close

The scheduler moves the same R2 residency through R4 parked-runtime ownership. On a restored invocation, missing R2 residency is a hard failure:

```text
E_EVE_MCU_CLOSE_R2_RESIDENCY_LOST_AT_INVOCATION_BOUNDARY
```

`DurableCheckpointKeepResident` is not a pipeline-reconstruction boundary.

Final close performs an explicit R2 receipt snapshot/release before existing R3G/R7/R7B/R4 terminal closure. Runtime receipt:

```text
eve_mcu_close_r2_session_residency_receipt.json
```

Receipt type:

```text
EveMcuCloseR2ProductionSessionResidencyReceipt
```

It records construct/restore/release counts, generation transition/rejection counts, Device/Queue mismatch count, R13 pipeline telemetry and bounded-status telemetry. `physical_pass_claimed` remains false in this source bake.

## 10. S0 F16 repair

Exactly one top-level directive is added to each of the four target shaders:

```wgsl
enable f16;
```

This is a language-capability declaration only. It does not prove `SHADER_F16` device support, E1/E2 physical pipeline creation, Tensor Core execution or performance. Existing device feature gating remains authority.

## 11. Actual source delta

```text
ADD 0
MOD 12
DEL 0
```

Modified:

```text
crates/base_train/src/atlas_runtime_real_loss_backward.rs
crates/base_train/src/atlas_runtime_route_admission.rs
crates/base_train/src/config.rs
crates/base_train/src/packed_runtime_native_bootstrap_accumulation_wave_residency.rs
crates/base_train/src/pipeline.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/trainable_session_active_production_owner_r4.rs
crates/burn_webgpu_backend/src/base_train_r13_oproj_ffn_backward.rs
crates/burn_webgpu_backend/src/shaders/base_train_tensorcube_local_muon_16x16_softmatrix16_subgroup32_e1_mixed_f16_f32_r7.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_tensorcube_local_muon_16x16_softmatrix16_subgroup32_e1_mixed_f16_f32_r7_r8a_indexed.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_tensorcube_local_muon_16x16_softmatrix16_subgroup32_e2_f16_r7.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_tensorcube_local_muon_16x16_softmatrix16_subgroup32_e2_f16_r7_r8a_indexed.wgsl
```

Source-delta digest:

```text
3ca599f1d3c6659c71c6588f878b14d23c0385c71bb902475c1a45a4ad769645
```

## 12. Static preservation actually checked

```text
parent SHA-256 verified                            PASS
source delta ADD0/MOD12/DEL0                       PASS
changed-Rust delimiter scan                        PASS
root Cargo.toml byte-identical                     PASS
root Cargo.lock byte-identical                     PASS
R13 linear WGSL byte-identical                     PASS
R13 SwiGLU WGSL byte-identical                     PASS
R13 add2 WGSL byte-identical                       PASS
legacy R13 direct calls in production backward    0
R2-aware R13 production callsites                  29
F16 target files                                   4
`enable f16;` per target                           exactly 1
native-f16 WGSL source-token files scanned         9
native-f16 source-token files missing directive    0
new process-global R2 pipeline/session cache       0
```

The F16 corpus result is a source-token heuristic, not a Naga26 validation result.

## 13. Validation boundary

This bake environment has no `cargo`, `rustc` or `rustfmt`.

```text
Rust compile:                 NOT RUN
Rust tests:                   NOT RUN
Naga26 global WGSL validator: NOT RUN
Native WGPU runtime:          HOLD
GPU physical qualification:  HOLD
Performance measurement:      HOLD
```

No COMPILE/RUNTIME/PHYSICAL/PERFORMANCE claim is issued.

Required user-machine sequence:

```powershell
cargo run -p orchestrator_local `
  --bin ash_wgsl_wgpu26_parser_compatibility_global_seal_r1 `
  --release --locked

cargo run -p ash-wgpu26-qualification --release --locked -- `
  vendor-r2-seal --workspace .

cargo test -p base_train --lib --locked
cargo build -p burn_webgpu_backend --lib --release --locked
cargo build -p base_train --lib --release --locked -j 1
```

Expected WGSL/vendor tokens remain requirements, not current results:

```text
PASS_ASH_WGSL_WGPU26_EXACT_NAGA26_PARSE_R1
PASS_WGPU26_VENDOR_R2_SINGLE_PACKAGE_GRAPH
```

## 14. Physical acceptance requirements

A later R2 campaign must prove:

```text
one R4 production session
execution residency construct = 1
R13 pipeline slab build = 1
FFN executor construct = 1
cross-step reuse of same residency
cross-invocation reuse of same residency
R13 R2 hotpath local pipeline create = 0
stale FFN content reuse = 0
Device/Queue drift = 0
generation regression = 0
in-flight status overwrite = 0
final R2 release receipt = 1
```

Performance improvement remains `UNKNOWN / HOLD` until same-workload A/B measurement.

## 15. ZIP exclusion policy

Generated sidecars are outside both ZIPs:

```text
ASH_EVE_MCU_CLOSE_R2_MANIFEST.json
ASH_EVE_MCU_CLOSE_R2_STATIC_QUALIFICATION_ARTIFACT.json
ASH_EVE_MCU_CLOSE_R2_STATIC_QUALIFICATION_REPORT.md
ASH_EVE_MCU_CLOSE_R2_PRODUCTION_SESSION_RESIDENCY_SPEC.md
```

Existing source modules whose names contain `manifest`, `artifact` or `spec` remain code and are preserved.

Generated sidecar hits in both code ZIPs: `0`.

## 16. Final bake identities

Full code-only:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PRODUCTION_SESSION_RESIDENCY_CODE_ONLY.zip
SHA-256: 0dcf28ce1afac158f56390e41075813cffefd6568f31b1ca6b5d1b53c894a703
Files: 8420
CRC: PASS
```

Review-only overlay:

```text
ASH_EVE_MCU_CLOSE_R2_PRODUCTION_SESSION_RESIDENCY_OVERLAY_REVIEW_ONLY_CODE_ONLY.zip
SHA-256: f15ed0b5fc6951a45a48db5b9b1dd665492846d67a652902a6ebbfda3a2b01cd
Files: 12
CRC: PASS
```

## 17. Promotion state

This bake admits only:

```text
PASS_EVE_MCU_CLOSE_R2_SOURCE_BAKE
PASS_EVE_MCU_CLOSE_R2_STATIC_SOURCE_SCOPE
PASS_EVE_MCU_CLOSE_R2_F16_SOURCE_DIRECTIVE_CLOSURE
HOLD_EVE_MCU_CLOSE_R2_NAGA26_GLOBAL_VALIDATION_PENDING
HOLD_EVE_MCU_CLOSE_R2_COMPILE_PENDING
HOLD_EVE_MCU_CLOSE_R2_NATIVE_PENDING
HOLD_EVE_MCU_CLOSE_R2_PHYSICAL_PENDING
HOLD_EVE_MCU_CLOSE_R2_PERFORMANCE_PENDING
```

`FullClosureSealed` is not admitted here.

## 18. Next boundary

```text
EVE-MCU-CLOSE-R2A
  BOUNDED ASYNC STATUS
  + SUBMIT / WAIT CLOSURE
  + COMPACT OBSERVATION BATCHING

then

R13-BWD-R1
  TILED LINEAR DX / DW
```

Attribution remains:

```text
R2       lifetime / ownership
R2A      synchronization
R13-R1   computation
```

## 19. Final law

> R2 extends the existing R4/R7 production session to resources that were still reconstructed below that boundary. It does not create another session.

> R13 immutable pipelines and the FFN executor become session-resident while tensor contents remain generation/content-key bound.

> R13 status reuse is bounded and tied to existing A01 SubmissionEpoch and A03 compact-readback authority. Generation advancement is not physical completion.

> The four F16 shaders explicitly declare `enable f16;`, closing the source-level blocker without claiming device F16 execution.

> Root Cargo graph, optimizer math, checkpoint format and R13 shader math are preserved.

> Current evidence is SOURCE/STATIC only. Compile, Naga26, native, physical and performance remain HOLD.
