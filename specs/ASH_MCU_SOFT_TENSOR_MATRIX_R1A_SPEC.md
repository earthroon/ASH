# ASH-MCU-SOFT-TENSOR-MATRIX-R1A

## A01 / A02 / A03 ACTUAL-WGPU STATIC OWNERSHIP RETIREMENT
## + DEVICE SOFT SUBGROUP PASS-THROUGH

### 0. Revision

```text
Patch ID: ASH-MCU-SOFT-TENSOR-MATRIX-R1A
Class: LOCAL OWNERSHIP SURGERY / COMPILE-SURFACE REDUCTION
Direct parent: ASH-MCU-SOFT-TENSOR-MATRIX-R1
Parent artifact: ASH_PASS3_MCU_SOFT_TENSOR_MATRIX_R1_STATIC_SOURCE_BAKE_CODE_ONLY.zip
Parent SHA-256: 7d8b551c04f4fa6922a2a082f533a4ca770a16174d83959b2f67907e98cbbd2c
Source release: STATIC SOURCE MATERIALIZATION / UNCOMPILED IN BAKE ENVIRONMENT
Physical qualification: HOLD
```

Observed compile blocker:

```text
error[E0275]: overflow evaluating the requirement `validation::NumericDimension: Sync`
```

Observed trait path entered `ShaderModule -> RenderPipeline -> BindGroupLayout -> BindGroup -> Device/Queue -> LifetimeTracker`.

Reserved tokens:

```text
PASS_ASH_MCU_SOFT_TENSOR_MATRIX_R1A_STATIC
PASS_ASH_MCU_SOFT_TENSOR_MATRIX_R1A_COMPILE
PASS_ASH_MCU_SOFT_TENSOR_MATRIX_R1A_NATIVE
HOLD_ASH_MCU_SOFT_TENSOR_MATRIX_R1A_WGPU_PENDING
```

Static source materialization does not issue compile/native/WGPU PASS.

---

## 1. Goal

Retire actual WGPU ownership from the three process-global/static runtime surfaces that still transitively exposed WGPU-core object graphs to `Send/Sync` proof:

```text
A01 Submission Lease Runtime
    actual Queue object as authority key

A02 Usage-Segregated Buffer Arena
    actual Arc<Buffer> in global arena page

A03 Staging / Compact Readback Runtime
    actual Queue-keyed TransferDomain with StagingBelt objects
```

Target structure:

```text
static/global
    identity + generation + lease + allocation metadata + telemetry only
        |
        v
McuDeviceSoftSubgroupHandleR1A
    actual arena Buffer objects
    actual control/bulk StagingBelt objects
        |
        v
call-scoped Queue pass-through
        |
        v
existing WGPU execution
```

The revision does not serialize WGPU objects and does not add `unsafe impl Send/Sync`.

---

## 2. Non-goals

No change to:

```text
Adam mathematics
HiMuon mathematics
SubmissionEpoch meaning
LogicalLeaseId meaning
PhysicalAllocationId meaning
R7A1 exact multi-consumer retirement/reclaim law
arena reuse/incarnation safety
staging upload/readback bytes
R3C/R3C1 semantic commit
R7/R7B generation authority
Soft Tensor Matrix topology
Atlas grouping algorithm
```

Prohibited fixes:

```text
recursion_limit increase
unsafe Send / Sync implementation
thread_local actual-WGPU cache
raw-pointer / usize ownership disguises
new global WGPU object cache
Python loader
PowerShell loader
```

---

## 3. Core ownership law

```text
GLOBAL / STATIC
    = identity + ledger + metadata only

ACTUAL Buffer / StagingBelt
    = explicit device soft subgroup only

ACTUAL Queue
    = execution-call pass-through only
```

Static/global maps may contain `QueueAuthorityId`, `PhysicalAllocationId`, `SubmissionEpoch`, generation, page metadata, counters and receipts. They may not transitively own `wgpu::Queue`, `wgpu::Buffer`, `StagingBelt`, Pipeline, BindGroup, or producer objects.

---

## 4. Device soft subgroup

Materialized backend authority:

```rust
McuDeviceSoftSubgroupHandleR1A
```

The implementation is process-local and explicitly owned. It intentionally uses non-global `Rc<RefCell<_>>` ownership so the actual WGPU object graph is not promoted into a process-global `Mutex<T>: Sync` boundary.

It owns:

```text
McuDeviceSoftSubgroupBindingR1A
Arena Buffer object table
TransferObjectLaneR1A
    control StagingBelt
    bulk StagingBelt
```

It does **not** own the Queue object.

Binding metadata:

```text
DeviceAuthorityId
QueueAuthorityId
generation
```

Queue is supplied only at actual WGPU callsites.

---

## 5. A01 Submission Lease surgery

Previous authority shape:

```text
SubmissionLeaseRuntime
    queue_domains: HashMap<wgpu::Queue, QueueDomainState>
```

New authority shape:

```text
SubmissionLeaseRuntime
    queue_domains: BTreeMap<QueueAuthorityId, QueueDomainState>
    allocation_queue_bindings: PhysicalAllocationId -> QueueAuthorityId
    pending_site_writes: QueueAuthorityId -> metadata
```

Queue identity is no longer reconstructed from a Queue pointer or Queue object hash. Callers pass `McuQueueAuthorityBindingR1A` derived from the owning subgroup.

Existing semantics retained:

```text
SubmissionEpoch uniqueness
queue-domain isolation
CompletionCoverage
LogicalLeaseId
ReleasedAwaitingCompletion distinction
lease reuse rejection
exact completion observation
```

Queue-bearing functions use `&wgpu::Queue` only as call-scoped execution input and never persist that reference/object in A01 static state.

---

## 6. A02 Buffer Arena surgery

Global `ArenaPage` is metadata-only after R1A:

```text
ArenaPageId
PhysicalAllocationId
capacity
in_use
incarnation
generation relation
last site / semantic role
R7A domain digest
```

Actual `Arc<wgpu::Buffer>` lives in the owning `McuDeviceSoftSubgroupHandleR1A` arena lane keyed by `PhysicalAllocationId` and generation/incarnation.

Acquisition:

```text
static arena metadata decides reuse/new-page
    -> subgroup verifies/advances page generation
    -> subgroup resolves or installs actual Buffer object
    -> ArenaLease carries the admitted live object for callsite use
```

Reclaim law is unchanged. Reuse requires the existing reader/submission/lease retirement conditions. Generation/incarnation mismatch is fail-closed.

Important boundary:

`ArenaLease` may temporarily carry an `Arc<Buffer>` and the subgroup handle, but the lease is not stored in the process-global arena metadata. The compile-surface rule concerns process-global/static ownership, not all local typed WGPU values.

---

## 7. A03 Transfer surgery

Previous shape:

```text
TransferRuntime
    HashMap<wgpu::Queue, TransferDomain>

TransferDomain
    control StagingBelt
    bulk StagingBelt
    compact readback metadata
```

New shape:

```text
A03 static TransferRuntime
    QueueAuthorityId -> compact-slot metadata
    transfer telemetry

McuDeviceSoftSubgroupHandleR1A
    control StagingBelt
    bulk StagingBelt
    upload/finish state
```

Queue remains a call-scoped input to stage/submit operations. The transfer belts are resolved from the same subgroup that owns the target arena Buffer.

Existing upload/readback behavior and byte contracts are retained.

---

## 8. Soft Matrix / Atlas integration

Soft Tensor Matrix and Atlas remain metadata-only with respect to actual WGPU objects.

Parallel planning may contain:

```text
QueueAuthorityId
PhysicalAllocationId
segment / generation
usage class
Submission dependency metadata
```

It may not capture Queue/Buffer/StagingBelt/Pipeline/BindGroup actual objects.

Execution flow:

```text
Soft Matrix coordinate
    -> Atlas metadata wave
    -> Device Soft Subgroup binding
    -> typed arena/transfer lane resolve
    -> call-scoped Queue
    -> existing WGPU operation
```

No new generic global object cache is introduced.

---

## 9. Lifetime

The subgroup is owned by the persistent MCU device-resource/session path and survives same-R4-session invocation park/restore.

R1A does not claim cross-session process-global reuse of actual Buffer/StagingBelt objects. This is an explicit semantic narrowing from the old process-global ownership shape.

At KeepResident boundaries no transient Queue borrow may survive. At final close existing SubmissionEpoch completion, lease retirement, arena safety, transfer finish/recall requirements remain authoritative before subgroup release.

---

## 10. R1B / R7B compatibility

The subgroup is device-resource state and does not add a twelfth R1B persistent MCU child. Existing exact persistent child cardinality remains 11.

R7/R7B job/generation authority and R7A1 packed-gradient semantics remain unchanged.

---

## 11. Error contract

Minimum fail-closed errors:

```text
E_DEVICE_SOFT_SUBGROUP_NOT_BOUND
E_DEVICE_SOFT_SUBGROUP_DEVICE_AUTHORITY_DRIFT
E_DEVICE_SOFT_SUBGROUP_QUEUE_AUTHORITY_DRIFT
E_DEVICE_SOFT_SUBGROUP_ARENA_PAGE_MISSING
E_DEVICE_SOFT_SUBGROUP_ARENA_GENERATION_DRIFT
E_DEVICE_SOFT_SUBGROUP_ARENA_OBJECT_META_DRIFT
E_DEVICE_SOFT_SUBGROUP_TRANSFER_PHASE_INVALID
E_DEVICE_SOFT_SUBGROUP_SUBMISSION_SCOPE_DRIFT
E_DEVICE_SOFT_SUBGROUP_STATIC_WGPU_OWNER_DETECTED
```

---

## 12. Static acceptance

Required:

```text
A01 static actual Queue ownership = 0
A02 static actual Buffer ownership = 0
A03 static actual Queue ownership = 0
A03 static actual StagingBelt ownership = 0
global metadata remains lightweight
subgroup explicit owner materialized
Queue is pass-through only
arena Buffer resolves by allocation + generation
transfer belts resolve from subgroup
Atlas actual-WGPU capture = 0
Soft Matrix actual-WGPU cell ownership = 0
recursion_limit workaround = 0
unsafe Send/Sync workaround = 0
new Python/PowerShell loader = 0
```

---

## 13. Compile / native acceptance

The direct compile target after applying this bake is:

```powershell
cargo check -p burn_webgpu_backend --lib
cargo check -p base_train --lib
```

Success requires absence of:

```text
overflow evaluating the requirement `validation::NumericDimension: Sync`
```

without any recursion-limit increase.

Then:

```powershell
cargo test -p burn_webgpu_backend --lib -j 1 --no-fail-fast
cargo test -p base_train --lib -j 1 --no-fail-fast
```

Static validation is not a substitute for these commands.

---

## 14. WGPU acceptance

After compile/native PASS, return to the existing production campaign. Minimum smoke evidence:

```text
submission succeeds
arena Buffer is actually bound
staging upload succeeds
exact completion observed
arena reclaim succeeds
```

Then run the existing 8 / 4+4 / 2+2+4 campaign. R1A creates no new training algorithm or alternate executor.

---

## 15. Explicit semantic changes

```text
S1 A01 Queue object:
   process-global ownership -> call-scoped pass-through

S2 A02 Buffer objects:
   process-global arena ownership -> persistent subgroup ownership

S3 A03 StagingBelt objects:
   process-global Queue-domain ownership -> persistent subgroup transfer lane

S4 cross-session actual-resource reuse:
   previously implicit process-global behavior -> NOT CLAIMED by R1A
```

These are lifetime/ownership changes, not numerical changes.

---

## 16. Completion law

R1A is complete only when the source ownership cut is present **and** the user's native environment confirms compile/native PASS without the WGPU-core trait overflow.

After that, no additional cache/ownership closure revision is planned. Return directly to physical WGPU campaign and modify only concrete failures.

---

# Appendix A. Actual source bake record

```text
Release class: STATIC SOURCE MATERIALIZATION / UNCOMPILED
Direct parent files: 8,413
ADD: 1
MOD: 29
DEL: 0
Output full files: 8,414
New Python loader: 0
New PowerShell loader: 0
```

Added:

```text
crates/burn_webgpu_backend/src/device_soft_subgroup_r1a.rs
```

The 29 modified files are API plumbing required to replace prior implicit Queue-derived identities and global arena ownership with an explicit subgroup/queue binding. This change count does not represent 29 new features.

Primary modified authorities:

```text
crates/burn_webgpu_backend/src/buffer_submission_lease.rs
crates/burn_webgpu_backend/src/usage_segregated_buffer_arena.rs
crates/burn_webgpu_backend/src/staging_compact_readback_ring.rs
crates/base_train/src/mcu_device_resource_runtime_r7a.rs
crates/base_train/src/mcu_session_runtime_r7.rs
```

Other modified Rust files are existing A01/A02/A03 callsites migrated to the explicit subgroup/queue-binding API. Three existing static validators were updated to check the new ownership location instead of stale direct-object expressions.

# Appendix B. Static validation actually executed

Final recorded results:

```text
R7A static: 83 / 83 PASS
R7 static: 55 / 55 PASS
R7B static: 83 / 83 PASS
R7A1 static: 82 / 82 PASS
Eve R3G static: 35 / 35 PASS
R3C1 static: 30 / 30 PASS
```

No failing entry remains in the final validation log.

The bake environment does not expose Cargo/Rustc, therefore compile, borrow checking, linking and WGPU execution are NOT RUN / 판단불가 here.

# Appendix C. Artifacts

Full code-only bake:

```text
ASH_PASS3_MCU_SOFT_TENSOR_MATRIX_R1A_DEVICE_SOFT_SUBGROUP_CODE_ONLY.zip
SHA-256: 4d30435295fd6c8b443ce6214734c80be75c5ef0648c0aa452534776be605e8f
Bytes: 21,383,792
Files: 8,414
CRC: PASS
Duplicate paths: 0
PowerShell files: 0
```

Overlay from direct parent:

```text
ASH_MCU_SOFT_TENSOR_MATRIX_R1A_DEVICE_SOFT_SUBGROUP_OVERLAY.zip
SHA-256: b1ac1c9de9bada4dc523c4da19d540aa7bf6d1909c9265191c851d475cfaecef
Bytes: 487,537
Files: 30
CRC: PASS
Duplicate paths: 0
PowerShell files: 0
```

Code ZIPs exclude generated spec/artifact/manifest/report directories. Cargo/build-required source metadata is preserved.

# Appendix D. Final law

> A01 remembers Queue authority and SubmissionEpoch, not an owned Queue object.
>
> A02 global metadata remembers page identity/generation, while actual Buffer objects live in the explicit device subgroup.
>
> A03 global metadata remembers transfer state, while actual StagingBelt objects live in the subgroup transfer lane.
>
> Soft Matrix and Atlas pass coordinates, generations and ledgers; actual WGPU objects never become their global/static ownership payload.
>
> No recursion-limit or unsafe Send/Sync workaround is accepted as the fix.
