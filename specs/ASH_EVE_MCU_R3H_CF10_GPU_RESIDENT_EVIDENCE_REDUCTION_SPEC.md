# EVE-MCU-R3H-CF10

## GPU-RESIDENT EVIDENCE REDUCTION

**Revision:** `EVE-MCU-R3H-CF10`  
**Parent code:** `EVE-MCU-R7A-CF9-CF3A + COMPILEFIX-1`  
**Class:** GPU evidence reduction / CPU success-checksum retirement / terminal compact readback

```text
+ FIXED-SIZE GPU CHECKSUM AUTHORITY
+ NO PER-WAVE CPU SHA-256 SUCCESS CHAIN
+ NO SUCCESS RECEIPT VEC
+ PARAMETER-TERMINAL GPU REDUCTION
+ 256-BYTE CPU READBACK
+ EXACT CF8 VALIDATION COUNTERS PRESERVED
+ FIRST NONFATAL FAILURE FAMILY ORDINAL
+ DURABLE SHA-256 AUTHORITIES PRESERVED
+ NO CANDIDATE OWNERSHIP CHANGE
```

---

## 1. Purpose

CF10 removes the CF8 production hotpath's CPU SHA-256 success-chain work.

Parent behavior:

```text
wave success
→ Rust scalar validation
→ Rust SHA-256 success-chain update
→ parameter terminal
→ formatted success-chain SHA
```

CF10 behavior:

```text
wave success
→ Rust exact scalar validation/counters only
→ parameter terminal
→ fixed 9-event aggregate set
→ GPU u32 checksum reduction
→ one 256-byte CPU readback
→ CF10 terminal receipt
```

No per-wave GPU evidence readback is introduced.

---

## 2. Scope boundary

The requested architectural target is eventually:

```text
one optimizer step
→ one GPU evidence epoch
→ one terminal readback
```

This bake performs the first production cutover at the existing CF8 authority boundary:

```text
one Muon parameter runtime
→ one CF10 GPU evidence reduction
→ one terminal readback
```

Therefore this revision does **not** claim:

```text
PASS_EVE_MCU_R3H_CF10_STEP_WIDE_SINGLE_READBACK
```

A future consolidation may lift parameter-terminal epochs into one optimizer-step epoch after exact parity is demonstrated.

---

## 3. Existing validation remains CPU-authoritative

CF10 does not replace exact validation predicates.

The following CF8 terminal predicates remain unchanged:

```text
host_candidate_retirement_count == wave_count
source_binding_count == source_wave_binding_count
source_retirement_count == source_wave_retirement_count
atlas_lease_completion_count == atlas_lease_wave_count
```

All existing wave-local `ensure!`, bounds, generation, routing, lease, and dispatch checks remain before the terminal reducer.

The GPU checksum is supporting identity evidence, not a substitute for exact validation.

---

## 4. CPU SHA success chain retirement

Removed from the production callsite:

```text
EVE_MCU_R3H_CF8_CHAIN_DOMAIN
cf8_chain_event(...)
MuonProductionRuntimeEvidenceCf8.success_chain: Sha256
success_chain_sha256()
success_evidence_chain_sha256
```

Per-wave success recording now updates only existing bounded scalar counters.

This removes repeated SHA-256 update work and digest-string mixing from the hot success path.

---

## 5. CF10 backend authority

Added:

```text
crates/burn_webgpu_backend/src/gpu_resident_evidence_reduction_cf10.rs
crates/burn_webgpu_backend/src/shaders/gpu_resident_evidence_reduction_cf10.wgsl
```

Primary Rust authorities:

```text
Cf10EvidenceEvent
GpuEvidenceCf10Executor
Cf10TerminalEvidenceReceipt
```

Schema:

```text
CF10_EVIDENCE_MIX_R1
```

---

## 6. Fixed event ABI

Each terminal aggregate event is:

```text
16 × u32
= 64 bytes
```

The current production bridge emits exactly 9 aggregate events per completed parameter runtime.

Domains cover:

```text
1 source binding / retirement
2 router
3 R8A bucket view
4 atlas lease
5 R8A dispatch
6 P2 shadow
7 P2 non-admission counters
8 host candidate retirement / wave bounds
9 parameter terminal identity
```

No `Vec<Receipt>` or `Vec<String>` is created by CF10.

---

## 7. Fixed GPU evidence block

CF10 GPU result buffer:

```text
64 × u32
= 256 bytes
```

Current populated fields:

```text
event_count u64
failure_count u64
checksum lanes[8]
first_failure_family_ordinal u32
```

Unused words remain reserved for future exact GPU counters without changing the 256-byte ABI.

---

## 8. Checksum semantics

The checksum is a deterministic GPU-friendly fingerprint.

It uses:

```text
u32 mix
atomicXor
atomicAdd
fixed domain ids
fixed aggregate ordinals
```

It is **not** a cryptographic hash.

Do not use it as checkpoint or artifact authentication.

---

## 9. Failure evidence

CF10 currently folds P2 nonfatal failure presence into the terminal GPU block.

The GPU block records:

```text
failure_count
first_failure_family_ordinal
```

Existing CPU first-failure semantic detail remains authoritative.

Hard errors such as:

```text
allocation failure
WGPU validation failure
DeviceLost
filesystem failure
configuration failure
```

remain immediate CPU/runtime failures and do not wait for CF10 terminal reduction.

---

## 10. Readback law

For each covered parameter runtime:

```text
GPU reduce dispatch
→ copy fixed 256-byte evidence block
→ MAP_READ
→ one CPU decode
```

Required:

```text
gpu_evidence_readback_bytes = 256
gpu_evidence_readback_count = 1
```

No per-wave CF10 readback exists.

---

## 11. Pipeline cache law

`GpuEvidenceCf10Executor` is lazily materialized and cached inside:

```text
TensorCubeLocalMuonBatchExecutor
```

The pipeline is not recreated for every parameter.

Per-parameter input/evidence/readback buffers are currently small ephemeral allocations.

Session-resident reuse of those tiny buffers is a future optimization, not required for CF10 correctness.

---

## 12. CF10 terminal receipt

A successful covered parameter emits:

```text
[ASH-EVE-MCU-R3H-CF10][gpu-evidence-terminal]
```

Fields:

```text
schema
parameter_index
generation
optimizer_step
event_count
failure_count
first_failure_family_ordinal
checksum256
gpu_evidence_readback_bytes
gpu_evidence_readback_count
admitted
```

Current event count target:

```text
9
```

---

## 13. CF8 terminal compatibility

CF8 parameter summary remains.

Changed field:

```text
success_evidence_chain_sha256
```

becomes:

```text
success_evidence_checksum256
```

This is an intentional evidence-representation change.

It does not change the exact CF8 cardinality predicates.

---

## 14. Meaning change

The parent CF8 supporting success fingerprint was order-sensitive because it hashed every successful event in Rust.

CF10's current production bridge fingerprints the exact terminal aggregate state using fixed domain ordinals.

Therefore:

```text
per-wave event-order fingerprint parity
```

is **not claimed** in this bake.

This does not weaken existing exact wave/coverage validations, but it does change the supporting fingerprint semantics.

If event-order identity is later required as a promotion predicate, it must be reintroduced as a GPU-resident streaming ordinal mix without restoring CPU SHA hotpath work.

---

## 15. Durable SHA boundary

CF10 does not modify SHA-256 authorities used for:

```text
checkpoint integrity
durable file identity
canonical artifact identity
promotion seals requiring cryptographic digest
```

Only CF8's hot success-chain SHA is retired.

---

## 16. CF9 lineage preservation

CF10 changes no:

```text
CF9-CF2 physical free-page trim
CF9-CF3 wave-bounded candidate VRAM
CF9-CF3A direct W/M/V host demotion
R3G completion-before-retirement
RAM36 ownership
R3B / R3C transactional semantics
```

No tensor payload ownership is added to CF10.

---

## 17. No receipt collection

Static law:

```text
NO Vec<Cf10EvidenceEvent>
NO Vec<String>
NO per-wave success receipt type
NO per-wave success JSON
```

CF10 terminal events are a fixed stack array in the production bridge.

---

## 18. New tests

Backend unit-test prefix:

```text
r3h_cf10_
```

Added tests:

```text
r3h_cf10_fixed_block_layout_stable
r3h_cf10_aggregate_event_is_ordinal_sensitive
```

The second test verifies fixed aggregate ordinal binding, not per-wave order parity.

---

## 19. Static validator

Added:

```text
tools/validate_ash_eve_mcu_r3h_cf10_gpu_resident_evidence_reduction_static.py
```

It checks:

```text
CF10 backend module present
WGSL reducer present
fixed 256-byte block authority
atomic XOR / ADD / MIN reduction
lazy cached executor integration
CF10 terminal marker present
CF8 exact terminal predicates preserved
old CPU SHA success chain absent
no CF10 success Vec/String collection
```

Static result at bake time:

```text
PASS_EVE_MCU_R3H_CF10_GPU_RESIDENT_EVIDENCE_REDUCTION_STATIC
```

---

## 20. Parent static drift note

The existing validator:

```text
validate_ash_basetrain_tensorcube_muon_atlas_wave_streaming_host_full_candidate_materialization_retirement_r1_static.py
```

reports two failures:

```text
atlas page authority used
streaming path mutates persistent momentum per tile
```

The same two failures reproduce on the CF3A parent before CF10 changes.

Therefore they are treated as pre-existing baseline drift, not CF10 regressions.

---

## 21. Source delta

```text
ADD 3
MOD 3
DEL 0
```

Added:

```text
crates/burn_webgpu_backend/src/gpu_resident_evidence_reduction_cf10.rs
crates/burn_webgpu_backend/src/shaders/gpu_resident_evidence_reduction_cf10.wgsl
tools/validate_ash_eve_mcu_r3h_cf10_gpu_resident_evidence_reduction_static.py
```

Modified:

```text
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
```

Source SHA-256:

```text
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
d829e447a31f47cf32bae9c36baff17ccf6b9b036522a8f3635cfae9bb961247

crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
a6f205b62f7d2872626a818da9a674d5f578c6f0583d37306d43140d86d475a2

crates/burn_webgpu_backend/src/gpu_resident_evidence_reduction_cf10.rs
459335c2aadf6ffdfcba0951b6b2b1d67d588c6b1339d3d4dd12cea7b46d19c6

crates/burn_webgpu_backend/src/lib.rs
84f5a9934792f1b6098d5796a7f0752d29e757c2cd9c444b183d02ab77fce30c

crates/burn_webgpu_backend/src/shaders/gpu_resident_evidence_reduction_cf10.wgsl
95f03893627cedc4fc0444cb0960a9795a373718a2899b8706a6ec739bcc79d6

tools/validate_ash_eve_mcu_r3h_cf10_gpu_resident_evidence_reduction_static.py
5c8f6f9b7ba8aa99439e6f8f02221195e8f82b74b4e46a33ab7a6e2ac434e7bf
```

---

## 22. Code-only archives

Overlay:

```text
ASH_EVE_MCU_R3H_CF10_GPU_RESIDENT_EVIDENCE_REDUCTION_OVERLAY_CODE_ONLY.zip
SHA-256 1677ceeb0c8fee35731988ab3dd13d2707b985e0ff72c37a441d1869f0415cd8
FILES 6
CRC PASS
```

Full applied:

```text
ASH_PASS3_EVE_MCU_R3H_CF10_GPU_RESIDENT_EVIDENCE_REDUCTION_CODE_ONLY.zip
SHA-256 e8d7a0f96f53f824097db87f65f26769a977acef92e2bf938008b010294063f2
FILES 8431
CRC PASS
```

Both archives contain:

```text
specs/       0
artifacts/   0
manifests/   0
Markdown     0
__pycache__  0
*.pyc        0
```

Build inputs `Cargo.toml` and `Cargo.lock` remain in the Full archive.

---

## 23. Qualification commands

Static:

```powershell
python .\tools\validate_ash_eve_mcu_r3h_cf10_gpu_resident_evidence_reduction_static.py
```

Backend tests:

```powershell
cargo test -p burn_webgpu_backend --lib --release --locked r3h_cf10_ -- --nocapture
```

CF8 regression:

```powershell
cargo test -p base_train --lib --release --locked r3h_cf8_ -- --nocapture
```

Release compile:

```powershell
cargo build -p base_train --bin base_train --release --locked -j 1
```

---

## 24. Physical acceptance

A successful production parameter must emit:

```text
[ASH-EVE-MCU-R3H-CF10][gpu-evidence-terminal]
```

with:

```text
schema=CF10_EVIDENCE_MIX_R1
event_count=9
gpu_evidence_readback_bytes=256
gpu_evidence_readback_count=1
```

The old field/token:

```text
success_evidence_chain_sha256
```

must not appear in the production CF8 summary.

The new field:

```text
success_evidence_checksum256
```

must appear.

---

## 25. Performance evidence boundary

Expected reductions:

```text
per-wave Rust SHA-256 work ↓
success digest String mixing ↓
host success-evidence ownership ↓
```

Added cost:

```text
one tiny GPU reduction dispatch per completed parameter
one 256-byte readback per completed parameter
```

No performance improvement is claimed until same-fixture measurement.

This bake does not yet close the larger compute/D2H serialization problem responsible for low GPU utilization.

---

## 26. Evidence status at bake time

```text
SOURCE / STATIC       PASS
ARCHIVE / CRC         PASS
RUST COMPILE          UNVERIFIED
WGSL COMPILE          UNVERIFIED
RUST TEST             UNVERIFIED
PHYSICAL              UNVERIFIED
PERFORMANCE           UNMEASURED
STEP-WIDE READBACK    NOT IMPLEMENTED / NOT CLAIMED
```

The bake environment does not provide a Rust toolchain.

---

## 27. Promotion tokens

Static / compile candidate:

```text
PASS_EVE_MCU_R3H_CF10_GPU_RESIDENT_EVIDENCE_REDUCTION
```

Parameter-terminal compact evidence:

```text
PASS_EVE_MCU_R3H_CF10_PARAMETER_TERMINAL_GPU_EVIDENCE
```

Physical:

```text
PASS_EVE_MCU_R3H_CF10_PHYSICAL
```

Performance:

```text
PASS_EVE_MCU_R3H_CF10_MEASURED_EVIDENCE_OVERHEAD_REDUCTION
```

Hold:

```text
HOLD_EVE_MCU_R3H_CF10_UNPROVEN
```

---

## 28. Completion law

CF10 current bake is complete only when:

1. CF8 exact validation predicates remain unchanged.
2. old CPU SHA success-chain code is absent.
3. CF10 terminal checksum is produced on GPU.
4. CPU reads exactly one 256-byte evidence block per covered parameter runtime.
5. no CF10 success receipt Vec/String history exists.
6. durable SHA-256 authorities remain unchanged.
7. CF9-CF3A tensor ownership remains unchanged.
8. backend CF10 tests pass.
9. CF8 regressions pass.
10. physical runtime produces exact CF10 terminal receipts.

> CF10 moves the hot success fingerprint out of Rust's per-wave SHA path and into a fixed GPU terminal reduction without weakening the exact CF8 validation counters. This bake intentionally stops at the existing parameter-terminal authority; step-wide single-readback promotion remains a later optimization.
