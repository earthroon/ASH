# TENSORCUBE-TABLE-R3-CF1

## PRODUCTION CALLSITE ADOPTION

```text
+ REAL R6 DESCRIPTOR → R1 TENSOR TABLE MATERIALIZATION
+ REAL PARAMETER AUTHORITY / REAL GPU BUFFER BINDING
+ R2A ACTIVE VERIFIED SCHEDULER CONSTRUCTION
+ R3 ACTIVE VERIFIED SCHEDULER CONSTRUCTION
+ TRACKED PRODUCTION SUBMISSION / LEASE RETIREMENT

+ P4 EXACT-LEASE PRESERVATION
+ P5 ACTIVE-ASYNC SEMANTIC CONSUMER PRESERVATION
+ B06 TICKET CLAIM AFTER R3 PHYSICAL COMPLETION

+ R3 RUNTIME REACHABILITY RECEIPT
+ R3 PHYSICAL TABLE RECEIPT
+ R3 TRACKED SUBMISSION RECEIPT
+ R3 PHYSICAL HANDOFF RECEIPT

+ NO SYNTHETIC R6 DESCRIPTOR
+ NO TEST-ONLY TENSOR TABLE
+ NO SYNTHETIC BP-DK STATE
+ NO LEGACY FALLBACK WHEN ACTIVE VERIFIED
```

## Parent

```text
TENSORCUBE-TABLE-R3
ASH_PASS3_TENSORCUBE_TABLE_R3_PERSISTENT_DEVICE_SCHEDULER_CODE_ONLY.zip
SHA-256 97b2784042b95e5abc27da44f8a83c8e04514ec6086ec9bde7cf04021894b633
```

Parent state before CF1:

```text
SOURCE   PASS
STATIC   PASS
COMPILE  PASS (user-local)
Native CF1 PASS (user-local)

PRODUCTION CALLSITE REACHABILITY = MISSING
```

The parent scheduler existed only as a compiled/exported subsystem. Production search returned no constructor/encode reference outside the R3 implementation module.

## Closure

CF1 introduces a production adoption module:

```text
crates/base_train/src/tensorcube_table_r3_cf1_production_adoption.rs
```

and binds it into the existing ActiveAsync local-Muon production callsite:

```text
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
```

The production path is now:

```text
real R6 epoch seal
→ real descriptor_snapshot_for_r8()
→ real Consume-R1 projection
→ TensorCubeTableHostAuthorityR1::materialize()
→ TensorCubeTableAuthorityR1::upload()
→ TensorCubeTablePersistentSchedulerR3::new()
→ scheduler.encode_generation_epoch()
→ existing tracked backend submission/lease authority
→ physical completion
→ B06 ticket claim
→ existing HybridDeviceCommitCoordinator staging
```

## Real R6 / R1 lineage

The ActiveAsync wave context now retains the exact production:

```text
TensorCubeConsumeEpochProjectionR1
Vec<McuTensorCubeJobDescriptorR6>
```

obtained from the already-sealed R6 epoch.

CF1 does not recompute tile geometry or construct synthetic descriptors.

## Lifecycle seed

At the R3 adoption point the active-device candidate has already reached physical `DeviceCandidateReady`. The R1 table is seeded with:

```text
COMPUTE_DONE
MUON_CONSUME_READY
SUCCESSOR_READY
```

`SUCCESSOR_READY` is an armed handoff prerequisite only; the successor predicate still requires `MUON_CONSUMED`, so successor scheduling cannot occur before R3 Muon consumption.

## BP-DK boundary

The existing BP-DK post-update state is not yet materialized at this exact wave-consumer callsite. CF1 therefore binds:

```text
bpdk_binding_count=0
```

and does not synthesize a dummy parameter record or mark `BPDK_READY`.

Existing BP-DK post-update / checkpoint durability authority remains downstream and unchanged.

## Real source / destination buffers

R3 source buffers come from the real `LocalMuonActiveDeviceSuccessorR1::device_buffers()`:

```text
candidate weight
candidate momentum
orthogonal update
```

R3 destination buffers are the real `MuonDeviceParameterAssemblyR2` device-resident parameter assembly:

```text
assembly weight
assembly momentum
assembly update
```

No second full W/M/update assembly is allocated for CF1.

## Tracked submission adoption

CF1 adds backend methods:

```text
submit_preencoded_tensorcube_table_r3_cf1()
try_collect_tensorcube_table_r3_cf1()
```

The R3 command buffer is encoded in `base_train` but submitted through the existing backend tracked-submission authority using the same source and destination allocation leases used by Consume-R2.

This preserves:

```text
source arena ownership
assembly arena ownership
nonblocking physical completion
lease release
source arena reclaim
assembly coverage accounting
```

R3 does not add a private unmanaged `queue.submit()` path.

## B06 preservation

The real successor remains owned by the pending R3 submission until physical completion.

Only after tracked completion does CF1 call:

```text
successor.claim_b06_ticket()
```

and the existing production callsite stages that ticket through:

```text
HybridDeviceCommitCoordinator::stage_muon_device_successor_ticket()
```

No synthetic B06 ticket or early publication is introduced.

## P4 / P5 preservation

R3 ActiveVerified requires:

```text
P4 exact atlas lease active
P5 ActiveAsync active
R2A ActiveVerified
R3 ActiveVerified
Consume-R2 ActiveVerified parent gate
```

P5 adds a distinct semantic consumer kind:

```text
TensorCubeTablePersistentSchedulerR3
```

The consumer token is released only after the tracked R3 submission physically completes and the B06 ticket is produced.

## Campaign seal

The existing ActiveAsync physical campaign now seals:

```text
ASH_TENSORCUBE_CONSUME_R2_MODE=ACTIVE_VERIFIED
ASH_TENSORCUBE_TABLE_R2A_MODE=ACTIVE_VERIFIED
ASH_TENSORCUBE_TABLE_R3_MODE=ACTIVE_VERIFIED
ASH_BP_DK_CHECKPOINT_R1_MODE=ACTIVE_VERIFIED
```

Runtime admission explicitly requires R2A and R3 ActiveVerified in addition to the previous P4/P5/R6/Consume-R2 gates.

## Receipts

Production callsite emits:

```text
[ASH-TENSORCUBE-TABLE-R3-CF1][reachability]
[ASH-TENSORCUBE-TABLE-R3-CF1][table]
[ASH-TENSORCUBE-TABLE-R3-CF1][submit]
[ASH-TENSORCUBE-TABLE-R3-CF1][physical-handoff]
```

Reachability receipt binds:

```text
real R6 descriptor count
R6 queue generation / epoch
source / target generation
TensorTable digest
R2A constructed
R3 constructed
real device / encoder binding
P4 exact lease
P5 ActiveAsync
legacy_scheduler_used=false
```

Table receipt binds:

```text
real row count
real parameter count
GPU-resident table
genuine source buffers
genuine successor buffers
bpdk_binding_count=0
synthetic_descriptor_count=0
test_fixture_row_count=0
```

## No hidden fallback

When R3 is `ActiveVerified`, the production successor takes the R3 path before the legacy Consume-R2 / fragment-copy match.

R3 construction, encoding, or tracked submission failure propagates as an error. It does not fall back to the legacy scheduler.

## Changed files

```text
MOD crates/base_train/src/lib.rs
MOD crates/base_train/src/bin/base_train.rs
MOD crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
MOD crates/base_train/src/unified_atlas_mcu_submission_epoch_dependency_active_async_r1.rs
ADD crates/base_train/src/tensorcube_table_r3_cf1_production_adoption.rs
MOD crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon_active_device_pending_r1.rs
MOD crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
ADD tools/validate_ash_tensorcube_table_r3_cf1_production_callsite_static.py
```

Delta:

```text
MOD 6
ADD 2
DEL 0
```

## Static qualification

```text
PASS_TENSORCUBE_TABLE_R3_CF1_PRODUCTION_CALLSITE_STATIC checks=51
PASS_TENSORCUBE_TABLE_R3_PERSISTENT_SCHEDULER_STATIC checks=52
PASS_TENSORCUBE_TABLE_R2A_PARALLEL_COMPACTION_STATIC checks=39
PASS_TENSORCUBE_TABLE_R2_GPU_PARALLEL_CONSUMER_STATIC checks=28
PASS_TENSORCUBE_TABLE_R1_STATIC checks=20
PASS_ASH_WGSL_WGPU26_GLOBAL_COMPATIBILITY_STRUCTURAL_R1
DELIMITER_COUNT_PASS
PYTHON_VALIDATOR_COMPILE_PASS
```

Production source search now returns R3 references outside the implementation module, including the ActiveAsync production callsite and P5 consumer authority.

## Evidence boundary

Bake environment:

```text
RUST_TOOLCHAIN=UNAVAILABLE

SOURCE=PASS
STATIC=PASS
COMPILE=NOT_RUN
RUNTIME=NOT_RUN
PHYSICAL=NOT_RUN
PERFORMANCE=UNMEASURED
PROMOTED=NO
```

No compile/runtime/physical/performance claim is made by this bake.

## Artifacts

Overlay:

```text
ASH_TENSORCUBE_TABLE_R3_CF1_PRODUCTION_CALLSITE_OVERLAY_CODE_ONLY.zip
SHA-256 b0cb57c375120c357225368f55e3d1027d17fa30d80fdd84c048c5a9af310c5a
FILES 8
CRC PASS
```

Full:

```text
ASH_PASS3_TENSORCUBE_TABLE_R3_CF1_PRODUCTION_CALLSITE_ADOPTION_CODE_ONLY.zip
SHA-256 d3e73da75f35fe7a01b8ba78bc0a8b446fdf14bb0720d3ef7c7cbd6b2662da8d
FILES 8478
CRC PASS
```

## Compile acceptance

Required first local gates:

```text
python tools/validate_ash_tensorcube_table_r3_cf1_production_callsite_static.py
cargo test -p base_train --lib tensorcube_table_r3_ --release --locked
cargo build -p base_train --bin base_train --release --locked
```

Because CF1 changes `base_train.exe`, any binary-bound Native CF1 / immutable physical qualification lineage must be regenerated for the exact resulting executable before Active physical admission.

## Runtime acceptance

A real ActiveAsync run must contain:

```text
[ASH-TENSORCUBE-TABLE-R3-CF1][reachability] ... admitted=true
[ASH-TENSORCUBE-TABLE-R3-CF1][table] ... admitted=true
[ASH-TENSORCUBE-TABLE-R3-CF1][submit] ... admitted=true
[ASH-TENSORCUBE-TABLE-R3-CF1][physical-handoff] ... admitted=true
```

Required conditions include:

```text
real_r6_descriptor_count > 0
r2a_constructed=true
r3_constructed=true
real_device_bound=true
real_encoder_bound=true
p4_exact_lease=true
p5_active_async=true
legacy_scheduler_used=false
gpu_resident=true
synthetic_descriptor_count=0
test_fixture_row_count=0
```

`physical-handoff` proves tracked R3 submission completion and real B06-ticket production. It does not by itself claim final generation commit or BP-DK durability.

## Final law

> R3-CF1 is the first revision in which the TensorTable persistent scheduler is invoked by the real ActiveAsync Muon production callsite.

> Exact production R6 descriptors and Consume-R1 projection materialize the GPU TensorTable. R3 consumes the real active-device successor buffers and writes the real parameter assembly buffers. The resulting command buffer is submitted through the existing tracked lease authority rather than an unmanaged side submission.

> ActiveVerified has one scheduler authority. Failure is fail-closed; there is no hidden legacy fallback.

> BP-DK durability, B06 final publication, generation commit, RAM36/CF11 residency, and R8A identity remain independent downstream authorities.
