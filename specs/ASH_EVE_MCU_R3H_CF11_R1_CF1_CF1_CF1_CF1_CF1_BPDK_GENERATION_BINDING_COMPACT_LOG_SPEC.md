# EVE-MCU-R3H-CF11-R1-CF1-CF1-CF1-CF1-CF1

## BP-DK LOCAL OBSERVER
## SOURCE-OPTIMIZER / TARGET-BP GENERATION BINDING CLOSURE
## + CANDIDATE-TERMINAL SUCCESS LOG COMPACTION

```text
+ SOURCE OPTIMIZER GENERATION EXACT BINDING
+ TARGET BP GENERATION EXACT BINDING
+ PRODUCTION-FAITHFUL (N-1, N) FIXTURE
+ PENDING READ-ONLY SNAPSHOT PRESERVATION
+ NO EARLY COMMIT
+ R8A CLOSURE PRESERVATION
+ PACKED M/V CLOSURE PRESERVATION
+ CF11-R1 MEMORY PRESERVATION
+ DEFAULT SUCCESS RECEIPT COMPACTION
+ VERBOSE SUCCESS RECEIPTS OPT-IN
+ FAILURE DETAIL PRESERVATION
```

## 0. Parent

Direct parent:

```text
EVE-MCU-R3H-CF11-R1-CF1-CF1-CF1-CF1
```

Parent Full SHA-256:

```text
c509456026a55992c1b6d5ad1d057115e827862a9174fa7e2fda44ed57fea375
```

## 1. Physical Input Evidence

The parent candidate snapshot path executed and failed with:

```text
E_CF11_R1_CF1_CF1_CF1_CF1_BPDK_PENDING_OPTIMIZER_GENERATION_DRIFT:0:1
```

This proves:

```text
pending.optimizer_generation = 0
pending.bp_generation        = 1
caller expected              = (1,1)
```

The pending representation was correct. The caller collapsed source optimizer generation and target BP generation into one target step value.

## 2. Generation Contract

BP-DK pending coordinates are frozen as:

```text
optimizer_generation = source optimizer generation
bp_generation        = target BP generation
```

For a normal transition:

```text
source = N-1
target = N
pending = (N-1, N)
```

The backend must never infer source optimizer generation from target BP generation.

## 3. Production Fix

`ProductionMuonRuntime::persist_bp_dk_observer_state()` now calls:

```text
for_each_candidate_state_snapshot_mapped_r3h_cf4(
    self.lifecycle.source_optimizer_step,
    optimizer_step,
    ...
)
```

instead of:

```text
(optimizer_step, optimizer_step)
```

## 4. Backend Naming / Fail-Closed Binding

Candidate selection parameters are clarified as:

```text
expected_source_optimizer_generation
expected_target_bp_generation
```

Exact checks remain fail-closed.

Errors:

```text
E_CF11_R1_CF1_CF1_CF1_CF1_CF1_BPDK_SOURCE_OPTIMIZER_GENERATION_DRIFT
E_CF11_R1_CF1_CF1_CF1_CF1_CF1_BPDK_TARGET_BP_GENERATION_DRIFT
```

The receipt schema remains source-compatible; existing fields continue to carry the two explicit values.

## 5. Production-Faithful Fixtures

Required fixtures now include:

```text
source optimizer = 6
target BP        = 7
pending          = (6,7)
```

PASS fixture:

```text
candidate_snapshot_selection_r1(6, 7, Some((6, 7)))
```

Wrong-source fixture:

```text
candidate_snapshot_selection_r1(6, 7, Some((7, 7)))
→ SOURCE_OPTIMIZER_GENERATION_DRIFT
```

Wrong-target fixture:

```text
candidate_snapshot_selection_r1(6, 7, Some((6, 8)))
→ TARGET_BP_GENERATION_DRIFT
```

## 6. Transaction Preservation

No change to:

```text
pending buffer ownership
pending metadata ownership
Arc identity preservation
candidate read-only snapshot
commit_pending_generation_r1 finalization authority
abort authority
restore-as-committed semantics
```

No early commit is introduced.

## 7. Log ABI Change

This revision intentionally changes success logging.

Environment:

```text
ASH_EVE_VERBOSE_SUCCESS_RECEIPTS
```

Default:

```text
unset / 0 / false
```

In default mode, redundant success lines are suppressed for:

```text
CF11 open
CF11 paged candidate terminal
CF11-R1 workspace admission
CF11-R1 workspace closure
R3B packed M/V digest
R8A pre-durability seal
R8A stream verify
BP-DK transactional candidate snapshot
BP-DK observer checkpoint stream
```

The receipts, counters, SHA checks, memory accounting and validation remain active.

## 8. Compact Candidate Terminal Receipt

After successful BP-DK candidate persistence, default mode emits one compact line:

```text
[ASH-EVE-MCU-R3H][candidate-terminal]
```

It binds source/target generation, R3B/R8A/BP-DK stage success, pending/inherited counts, BP-DK snapshot digest, and marks downstream source-retirement/successor/commit as NR.

This is intentionally a candidate-terminal receipt, not a claim that source retirement or generation commit has completed.

## 9. Verbose Qualification Mode

Set:

```powershell
$env:ASH_EVE_VERBOSE_SUCCESS_RECEIPTS = "1"
```

Then the compact candidate-terminal line remains, and historical per-stage success receipts are also emitted.

Compact default:

```powershell
Remove-Item Env:ASH_EVE_VERBOSE_SUCCESS_RECEIPTS -ErrorAction SilentlyContinue
```

## 10. Failure Preservation

No `ensure!`, `bail!`, error string or failure control flow is suppressed by the logging flag.

A failing stage continues to emit its full error chain.

The verbosity flag affects textual successful receipt emission only.

## 11. Modified Files

```text
MOD crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
MOD crates/base_train/src/ram_resident_adam_mv.rs
MOD crates/base_train/src/ram_weight_pack_persistent_residency.rs
MOD crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
MOD crates/burn_webgpu_backend/src/bp_delta_k_local_observer.rs
MOD tools/validate_ash_eve_mcu_r3h_cf11_r1_cf1_cf1_cf1_cf1_bpdk_pending_snapshot_static.py
ADD tools/validate_ash_eve_mcu_r3h_cf11_r1_cf1_cf1_cf1_cf1_cf1_bpdk_generation_binding_static.py
```

## 12. Source SHA-256

```text
0fbd443da6eddb9e47c3c1517a712bced92eb7e37f976db39c8022cc11258340  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
2e5f3cca884caf3e923704ef78aecf5deedb705bf5e17760b5dd4347447cd260  crates/base_train/src/ram_resident_adam_mv.rs
8ad5e493faf28612c498d71f5bbf8d4e035bc6190df4dd15d68a011d334e37a9  crates/base_train/src/ram_weight_pack_persistent_residency.rs
16298ef287da44759c57cc6f663d065f53f302b83afa6892657b65c34502b8d0  crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
da396cb473ed2d80cedb71780cbb2bedcfb656f39321e50580404f39ef143e2f  crates/burn_webgpu_backend/src/bp_delta_k_local_observer.rs
ffd17f649d6f55a9af8acdd62c7dc083482a6055a75f7bb7157cf6d7df8d8041  tools/validate_ash_eve_mcu_r3h_cf11_r1_cf1_cf1_cf1_cf1_bpdk_pending_snapshot_static.py
753c101efea8a3ea432febc587339403dd54945506211c20449418b4f3bdffe1  tools/validate_ash_eve_mcu_r3h_cf11_r1_cf1_cf1_cf1_cf1_cf1_bpdk_generation_binding_static.py
```

## 13. Static Qualification

```text
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_BPDK_GENERATION_BINDING_STATIC checks=27
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_BPDK_PENDING_SNAPSHOT_STATIC checks=37
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_R8A_PREDURABILITY_SEAL_STATIC checks=30
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_MUON_PACKED_ADDRESS_STATIC checks=26
PASS_EVE_MCU_R3H_CF11_R1_CF1_PACKED_MV_DIGEST_STATIC checks=27
PASS_EVE_MCU_R3H_CF11_R1_BOUNDED_COW_WORKSPACE_STATIC checks=22
PYTHON_VALIDATOR_COMPILE_PASS
```

Rust toolchain is not installed in the bake environment; no compile/runtime/physical claim is made.

## 14. Artifacts

Overlay:

```text
ASH_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_BPDK_GENERATION_BINDING_COMPACT_LOG_OVERLAY_CODE_ONLY.zip
SHA-256 c29f534e55c30abf4026d810616e2bd2175a36c12a27e111d2755d1ef856367f
FILES 2
CRC PASS
```

Full:

```text
ASH_PASS3_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_BPDK_GENERATION_BINDING_COMPACT_LOG_CODE_ONLY.zip
SHA-256 c5aef3c9d8d01fd40cf9cbc07351291255b0b51f62a47860608e4a1f91365b56
FILES 8439
CRC PASS
```

Both exclude specs/, artifacts/, manifests/, Markdown, __pycache__, and *.pyc.

## 15. Physical Acceptance

Same fixture must show:

```text
bpdk_source_optimizer_generation=0
bpdk_target_generation=1
BPDK-SNAP:PASS
```

and must not show:

```text
BPDK_SOURCE_OPTIMIZER_GENERATION_DRIFT
BPDK_TARGET_BP_GENERATION_DRIFT
BpDkLocalSnapshotPendingGeneration
```

Parent closure preservation remains required: R8A stream verify exact, packed M/V exact, CF11-R1 workspace exact.

## 16. Final Law

> BP-DK pending optimizer generation is a source-generation coordinate, while BP generation is a target-generation coordinate.

> The production snapshot caller binds (source optimizer, target BP) explicitly and never collapses the pair into (target,target).

> Pending candidate snapshot semantics remain read-only and transactionally unresolved.

> Default success logs are compacted. Qualification can restore per-stage success receipts with ASH_EVE_VERBOSE_SUCCESS_RECEIPTS=1.

> The compact line emitted in this revision is a candidate-terminal receipt. It does not promote downstream source-retirement, successor or commit stages that have not yet executed.

> Failure diagnostics remain fail-closed and unsuppressed.

## Compilefix-1: compact terminal payload SHA ownership

First user compile exposed:

```text
error[E0382]: borrow of moved value: `payload_sha256`
```

The compact candidate-terminal log was added after:

```rust
let manifest = build_bp_dk_observer_state_stream_manifest_r3h_cf4(
    ...,
    payload_sha256,
    parameters,
)?;
```

The manifest builder intentionally owns the SHA string as part of the durable manifest. The later compact terminal `eprintln!` attempted to reuse the moved local string.

Compilefix-1 does not clone or change ownership semantics. It logs the already-owned manifest field after manifest creation/write:

```rust
manifest.payload_sha256
```

instead of the moved local:

```rust
payload_sha256
```

This preserves:

```text
manifest owns payload SHA
candidate-terminal log remains after manifest write
no extra String allocation
no BP-DK generation semantic change
no log ABI change
```

Static validator now also requires:

```text
compact terminal uses manifest.payload_sha256
compact terminal does not reuse the moved local payload_sha256
```

Compilefix evidence:

```text
SOURCE        APPLIED
STATIC        PASS 27/27
ARCHIVE CRC   PASS
RUST COMPILE  USER RE-RUN REQUIRED
RUNTIME       UNVERIFIED
PHYSICAL      UNVERIFIED
```
