# ASH-ADAMS-RIB-EVE-PERSISTENT-ADAM-AUTHORITY-CROSS-INVOCATION-PHYSICAL-SEAL-R1

## 0. Revision

```text
Patch ID:
ASH-ADAMS-RIB-EVE
-PERSISTENT-ADAM-AUTHORITY
-CROSS-INVOCATION-PHYSICAL-SEAL-R1

Short name:
EVE-PHYS-R1
Persistent Adam Authority
Cross-Invocation Physical Seal

Status:
STATIC SOURCE MATERIALIZATION RELEASE
PHYSICAL QUALIFICATION: HOLD
```

Static token:

```text
PASS_ASH_ADAMS_RIB_EVE_PERSISTENT_ADAM_AUTHORITY_CROSS_INVOCATION_PHYSICAL_SEAL_R1_STATIC
```

Physical HOLD:

```text
HOLD_ASH_ADAMS_RIB_EVE_PERSISTENT_ADAM_AUTHORITY_CROSS_INVOCATION_PHYSICAL_SEAL_R1_PENDING
```

Reserved physical PASS:

```text
PASS_ASH_ADAMS_RIB_EVE_PERSISTENT_ADAM_AUTHORITY_CROSS_INVOCATION_PHYSICAL_SEAL_R1
```

Current source truth:

```text
observer materialized          = true
production callsite bound      = true
cross-invocation receipt bound = true
physical_pass_claimed          = false
```

## 1. Direct parent chain

EVE-PHYS-R1 consumes the existing authority chain without replacing it:

```text
Eve mutable RAM M/V authority R3
Eve persistent authority instance R3G
R3G exact lease sequencing
Trainable Session active owner R4
Trainable Session sealed admission R4A
MCU persistent execution fabric R7/R7A/R7B
```

The code bake is based on the current WGPU26/R2R1 tree after the MCU R7A bundle stale-field compile correction.

## 2. Compile-log update consumed by this revision

The supplied native Cargo log establishes that the previous MCU stale-access blocker was closed far enough for Cargo to compile/check:

```text
cubecl-wgpu 0.9.0 path fork
burn-wgpu-local
burn-fusion-local
burn_webgpu_backend
```

`burn_webgpu_backend` reached warning-only completion, after which `model_core` exposed three source errors in `headwise_texture_persistent_kv_binding.rs`:

```text
BackendBufferDescriptor missing
BackendBufferUsages missing x2
```

EVE-PHYS-R1 therefore includes one local WGPU26 facade correction:

```text
RuntimeWgpuBufferDescriptor
 -> BackendBufferDescriptor
 -> model_core import
```

and imports the already-existing `BackendBufferUsages` facade in the same callsite.

No WGPU version, CubeCL package, Burn package, Device/Queue ownership, shader, optimizer math or vendor path changes are made.

Because the bake environment used to construct this artifact has no Cargo/Rustc, post-correction workspace compile PASS is not claimed by this specification.

## 3. Physical claim being sealed

EVE-PHYS-R1 seals exactly this claim:

> Within one production `TrainableSessionRuntimeR4`, Adam M/V is hydrated once, bound once to one Eve R3G authority instance, parked after one invocation, restored into a successor invocation without reconstruction or reallocation, and durably written back only at final close.

Equivalent numerical state reconstructed into a new allocation is not accepted as persistent authority.

## 4. Production-path-only law

The observation surface is bound to the existing production R4 scheduler path.

It does not introduce:

```text
synthetic Adam loop
mock R4 session
alternate optimizer executor
CPU reference replacement
new checkpoint route
```

The instrumentation sits around the actual invocation open/close boundaries already used by `execute_r6_production_invocation_r4`.

## 5. New physical observer

Materialized:

```text
crates/base_train/src/eve_persistent_adam_cross_invocation_physical_seal_r1.rs
```

Authority:

```text
ash.adams_rib_eve.physical.cross_invocation.r1
```

It owns only process-local snapshots, cross-invocation continuity checks, and physical receipt construction. It owns no Adam M/V storage and no runtime Device/Queue resource.

The new observer module contains no Rust `if` statement; state and admission branching use `match`/typed enums.

## 6. Physical Adam body witness

`RamResidentAdamMv` now exposes a process-local physical witness for committed/candidate M/V allocation address and byte length.

The allocation lists are sorted by address before comparison. This intentionally permits A/B role swapping while rejecting replacement allocation. Pointer/address values are process-local evidence only and are never durable authority.

## 7. R3G authority continuity

Every observed invocation boundary requires one live `EveAuthorityInstanceIdentityR3G` and records authority ordinal, authority record digest, hydrated source M digest, and hydrated source V digest.

Across adjacent boundaries EVE-PHYS-R1 requires exact equality. The first R3G publication is counted from the real allocation/publish branch and physical PASS requires exactly one publication.

## 8. Root-guard continuity

The R3G session root guard path is recorded at every invocation boundary through `TrainableSessionRootGuardR3G::lock_path()` and must remain identical across park/restore.

## 9. Hydration continuity

Every snapshot requires `RamResidentAdamMv.hydration_count = 1`. Final R4 telemetry additionally requires `adam_hydration_count = 1` and `runtime_reconstruction_count = 0`.

## 10. Invocation sequencing

Observer boundary order is closed as Open(1) -> Close(1) -> Open(2) -> Close(2) and so on. The first invocation must not report restored runtime; every successor open must.

For each close -> successor-open transition, training generation, optimizer generation, next lease ordinal, issued lease count, R4A admission seal digest, R3G root guard, physical allocation sets and MCU session identity must match exactly.

## 11. Lease continuity

`ProductionMuonExecutionCounters` now accumulates the existing AdamW pending-generation R3G lease receipt values:

```text
eve_r3g_source_submit_count_r1
eve_r3g_unique_lease_count_r1
eve_r3g_lease_reuse_count_r1
```

Every snapshot requires lease reuse count zero and submit count equal to unique lease count. Physical PASS additionally requires at least one real Eve R3G source submission.

## 12. MCU continuity

`ProductionMuonRuntime` exposes read-only `McuSessionIdentityR7` and aggregate Eve R3G lease counters. Across park/restore the MCU session digest must remain identical and the existing MCU telemetry must end with `adam_executor_build_count = 1`.

## 13. Existing R4 telemetry reused

Physical PASS requires:

```text
session_open_count = 1
invocation_open_count = invocation_count
invocation_complete_count = invocation_count
adam_hydration_count = 1
weight_adoption_count = 1
production_muon_runtime_construction_count = 1
himuon_momentum_load_count = 1
mcu_session_open_count = 1
runtime_reconstruction_count = 0
runtime_park_count >= 1
runtime_restore_count >= 1
admission_profile_build_count_r4a = 1
admission_profile_replace_count_r4a = 0
hotpath_environment_read_count_r4a = 0
hotpath_config_reparse_count_r4a = 0
poisoned_count = 0
```

A new R4 telemetry field records only `eve_authority_publication_count_r1`.

## 14. Final writeback boundary

The final close snapshot reads the existing `RamResidentAdamMv` writeback counters. Physical PASS requires final M and V writeback count exactly one.

The physical receipt is attempted only after the R4 session reports it no longer remains open, so intermediate KeepResident invocations cannot prematurely promote the seal.

## 15. Existing hotpath disk-I/O authority retained

EVE-PHYS-R1 does not add a second file-I/O accounting system. The existing `RamResidentAdamMvReceipt` remains the authority for zero per-step M/V disk reads/writes and final durable writeback verification.

## 16. Emitted runtime evidence

The scheduler writes per-invocation open/close snapshots plus paired invocation evidence. At final session close, after at least two completed invocations and only when every physical invariant passes, it writes:

```text
eve_phys_r1_cross_invocation_physical_receipt.json
```

with the reserved physical PASS token.

A static bake alone never creates that receipt.

## 17. No source-tree scanning in physical hotpath

The observer performs no workspace scan, Git walk, source-tree SHA pass or Cargo metadata invocation during training. Runtime work is limited to small metadata snapshots and process-local pointer/length observation. No Adam tensor payload is hashed by EVE-PHYS-R1.

## 18. WGPU26 facade compile correction included

This bake adds the missing stable alias `RuntimeWgpuBufferDescriptor -> BackendBufferDescriptor` through `runtime_wgpu_type_authority.rs`, `raw_bridge.rs`, and `burn_webgpu_backend/lib.rs`, then imports `BackendBufferDescriptor` and `BackendBufferUsages` in `model_core/src/headwise_texture_persistent_kv_binding.rs`.

This is a source-level WGPU26 facade completion only.

## 19. Exact code-bake delta

Relative to `ASH_PASS3_BURN_CUBECL_WGPU26_R2R1_MCU_R7A_BUNDLE_ACCESS_COMPILE_FIX_CODE_ONLY.zip`:

```text
ADD 1
MOD 9
DEL 0
```

Added:

```text
crates/base_train/src/eve_persistent_adam_cross_invocation_physical_seal_r1.rs
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/ram_resident_adam_mv.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/trainable_session_active_production_owner_r4.rs
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/raw_bridge.rs
crates/burn_webgpu_backend/src/runtime_wgpu_type_authority.rs
crates/model_core/src/headwise_texture_persistent_kv_binding.rs
```

## 20. Code-only artifact

Full source artifact:

```text
ASH_PASS3_EVE_PHYS_R1_PERSISTENT_ADAM_CROSS_INVOCATION_STATIC_CODE_ONLY.zip
SHA-256 = c185aa82bd825cdd93e6f90a013eba067f69b789b59ef3ff13124786eb4c4398
entries = 8,415
```

Overlay artifact:

```text
ASH_PASS3_EVE_PHYS_R1_PERSISTENT_ADAM_CROSS_INVOCATION_OVERLAY.zip
SHA-256 = 092cec3e2be02af2b8acb65b6928e89d5b220fa9364fc001f7f5462fc7167345
entries = 10
```

Applying the overlay to the direct parent reproduces the full source tree byte-for-byte.

## 21. Static bake claims

This bake claims observer/materialization/callsite binding and the source correction for the model_core WGPU26 facade blocker. It does not claim post-correction workspace Cargo PASS or EVE physical campaign PASS.

## 22. Physical rejection conditions

The campaign rejects second hydration, authority drift, authority republish, root-guard drift, lease sequencer reset/reuse, generation discontinuity, M/V allocation replacement, runtime reconstruction, MCU session drift/reopen, AdamW producer rebuild, admission seal drift, missing final M/V writeback, or poisoned session.

## 23. Physical admission sequence

Canonical campaign is one process and one TrainableSessionRuntimeR4: invocation 1 hydrates/publishes/executes/parks; invocation 2 restores the same body/authority/guard/session/lease sequence, executes, performs final durable writeback, and closes.

## 24. Physical promotion rule

Only a real same-process production campaign satisfying all receipt invariants may emit the physical PASS token. Static inspection, compiler-only PASS, synthetic JSON, or reconstructed equivalent Adam state cannot.

## 25. Explicit non-claims

EVE-PHYS-R1 does not claim workspace-wide Adam-family adoption, LoRA Adam retirement, process-restart persistence, multi-device Adam, tensor-parallel optimizer state, GPU-resident Adam M/V, WGPU Device/Queue/Buffer physical lineage, or Fusion writable external-alias adoption.

## 26. Direct successor

After physical PASS the Eve core lifetime problem is considered closed. The next Adam-side revision becomes `EVE-ADOPT-R1 Workspace Adam ABI Adoption + Independent Adam-Family Retirement`.

## 27. Final law

> Persistent Adam authority means the same live RAM allocations cross the invocation boundary, not merely equal numerical state.

> A/B role swaps are legal; physical allocation replacement is not.

> The R3G authority, root guard, lease sequencer, MCU session identity and admission seal cross the boundary with the Adam body.

> Hydration occurs once. Runtime reconstruction occurs zero times. Final M/V durable writeback occurs once at final close.

> Until a real production campaign emits the physical receipt, the EVE-PHYS-R1 physical HOLD remains authoritative.
