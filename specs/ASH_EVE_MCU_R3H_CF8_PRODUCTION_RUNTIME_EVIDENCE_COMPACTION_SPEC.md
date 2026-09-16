# EVE-MCU-R3H-CF8

## PRODUCTION RUNTIME EVIDENCE COMPACTION

**Revision:** `EVE-MCU-R3H-CF8`  
**Parent:** `EVE-MCU-R3H-CF6`  
**Class:** production observability compaction / successful wave-receipt cardinality reduction

```text
+ NO PER-WAVE SUCCESS LOG
+ PARAMETER-LOCAL BOUNDED EVIDENCE COUNTERS
+ ORDER-SENSITIVE SUCCESS EVIDENCE CHAIN
+ FIRST NONFATAL P2 FAILURE DETAIL ONLY
+ EXISTING TERMINAL RECEIPTS PRESERVED
+ NO VALIDATION / GPU / OPTIMIZER SEMANTICS CHANGE
```

## 1. Purpose

CF8 removes successful per-wave textual receipts from the production Muon streaming hotpath while preserving the validation and state transitions that produced them.

Retired successful wave families:

```text
ASH-MUON-ATLAS-WAVE-SOURCE-BINDING-R1
ASH-MCU-DETERMINISTIC-PRECISION-EXPERT-ROUTER-R8
ASH-UNIFIED-ATLAS-MCU-GPU-RESIDENT-EXPERT-BUCKET-VIEW-R8A
ASH-MCU-P4-ATLAS-LEASE-SUBMISSION
ASH-UNIFIED-ATLAS-MCU-HETEROGENEOUS-EXPERT-DISPATCH-R8A
ASH-MCU-P2-REAL-PRODUCTION-WAVE-SHADOW-R1 PASS / normal non-admission console output
ASH-MUON-ATLAS-WAVE-HOST-CANDIDATE-RETIREMENT-R1
ASH-MUON-ATLAS-WAVE-SOURCE-RETIREMENT-R1
```

CF8 does **not** remove the underlying validation, P2 structured evidence, parameter-terminal retirement receipts, CF6 packed-span summary, or hard failure propagation.

## 2. Bounded authority

CF8 adds one parameter-local fixed-shape authority:

```text
MuonProductionRuntimeEvidenceCf8
```

Lifetime:

```text
parameter entry
→ wave observations
→ parameter terminal closure
→ one compact summary
→ drop
```

Retained state is limited to family cardinalities, five fixed P2 non-admission counters, first/final completed wave identity, one SHA-256 state, and one boolean for first nonfatal P2 failure detail.

Forbidden replacement structures:

```text
Vec<WaveReceipt>
Vec<String>
per-wave HashMap / BTreeMap evidence history
unbounded logging queue
```

All new CF8 cardinality increments use checked arithmetic and fail closed on overflow.

## 3. Ordered success chain

Successful evidence that is no longer printed is folded into:

```text
success_evidence_chain_sha256
```

Domain separator:

```text
ASH-EVE-MCU-R3H-CF8\0
```

Each event feeds an event-kind byte, wave id, fixed-width little-endian scalars, and length-prefixed existing digest strings when applicable. No formatted per-wave String is built for hashing.

The chain is order-sensitive. Equal aggregate counts with different event order must not have the same digest.

P2 `FAIL` evidence is counted separately and is not folded into the success chain.

## 4. Source binding

Local and fused source-binding success prints become:

```text
record_source_binding(...)
```

CF8 tracks:

```text
source_binding_count
source_binding_local_count
source_binding_fused_count
```

Existing atlas-bound capacity validation remains before the observation. Terminal closure requires:

```text
cf8.source_binding_count == source_wave_binding_count
```

Source binding count is deliberately **not** equated with source retirement count because a single wave may contain both local and fused source partitions.

## 5. R8 / R8A / P4

Successful console receipts become bounded observations:

```text
record_router(...)
record_bucket_view(...)
record_atlas_lease(...)
record_r8a_dispatch(...)
```

The success chain still receives queue generation/epoch, assignment and bucket cardinalities, lease generation/submission/wait data, dispatch cardinalities, and existing manifest/view digests.

All parent validations remain before these observations, including R8A backend identity, job coverage, expert dispatch count, zero repack bytes, zero additional bucket D2H, submission observation, and exact-wait observation.

P4 terminal CF8 closure requires:

```text
atlas_lease_completion_count == atlas_lease_wave_count
```

No routing policy, bucket materialization, atlas lease lifetime, Device/Queue, submission, WGSL, or dispatch geometry changes.

## 6. P2 production-wave shadow

P2 persisted `McuRealProductionWaveShadowEvidenceR1` remains unchanged.

Normal PASS:

```text
record_p2_evidence(...)
no per-wave success console line
```

P2 comparison FAIL:

```text
p2_shadow_fail_wave_count += 1
first FAIL only → [ASH-EVE-MCU-R3H-CF8][first-failure]
subsequent FAILs → no repeated console stream
```

Shadow execution error:

```text
existing observe_shadow_execution_failure()
CF8 execution-failure counter
first failure detail only
```

Normal non-admission is represented by fixed counters for:

```text
ShadowBudgetExhausted
CurrentR8aCapacityExceeded
MissingCurrentBundleAuthority
RouterNotActive
UnsupportedExecutionDomain
```

No dynamic reason map is added.

## 7. Host / source retirement

Successful per-wave retirement prints become:

```text
record_host_retirement(...)
record_source_retirement(...)
```

Actual candidate commit, successor write, momentum commit, scratch clear and pending-tile behavior are unchanged.

Terminal CF8 closure requires:

```text
host_candidate_retirement_count == waves.len()
source_binding_count == source_wave_binding_count
source_retirement_count == source_wave_retirement_count
atlas_lease_completion_count == atlas_lease_wave_count
```

Parent terminal predicates remain:

```text
next_tile == tile_count
pending_tiles.is_empty()
owner_count == exactly one per logical tile
```

## 8. Existing terminal receipts preserved

CF8 retains:

```text
PASS_ASH_BASETRAIN_TENSORCUBE_MUON_ATLAS_WAVE_STREAMING_HOST_FULL_CANDIDATE_MATERIALIZATION_RETIREMENT_R1
ASH-MUON-ATLAS-WAVE-STREAMING-RETIREMENT-R1
ASH-MUON-ATLAS-WAVE-SOURCE-PACKING-RETIREMENT-R1
ASH-MUON-ATLAS-WAVE-HOST-SCRATCH-SLAB-REUSE-AND-PER-TILE-HEAP-CHURN-RETIREMENT-R1
```

They are parameter-terminal authorities rather than per-wave success streams.

## 9. CF8 terminal receipt

Each completed affected parameter emits one:

```text
[ASH-EVE-MCU-R3H-CF8][parameter-runtime-evidence-summary]
```

Current fields:

```text
parameter_index / generation / optimizer_step
wave_count / first_wave_id / final_wave_id
source_binding_count / local / fused / source_retirement_count
router_wave_count
r8a_bucket_view_wave_count
atlas_lease_wave_count / atlas_lease_completion_count
r8a_dispatch_wave_count
p2_shadow_pass_wave_count
p2_shadow_fail_wave_count
p2_shadow_execution_failure_count
five fixed P2 non-admission counters
host_candidate_retirement_count
success_evidence_chain_sha256
admitted=true
```

`admitted=true` means the CF8 compaction/cardinality closure completed. It does not replace P2 parity or later promotion gates.

## 10. Failure behavior

Hard validation errors continue to propagate from their existing `ensure!`, `context`, and `bail!` sites. CF8 does not build a second error framework.

The new bounded first-failure line exists only for P2 nonfatal comparison/execution failures that previously generated repeatable wave-level console output.

## 11. Validator realignment

Four existing static validators referenced retired successful marker strings and now inspect the CF8 bounded observation callsites / terminal summary instead:

```text
tools/validate_ash_basetrain_tensorcube_muon_atlas_wave_streaming_host_full_candidate_materialization_retirement_r1_static.py
tools/validate_ash_basetrain_tensorcube_muon_atlas_wave_source_packing_full_host_scratch_retirement_r1_static.py
tools/validate_ash_basetrain_unified_atlas_mcu_exact_atlas_slot_lease_generation_r1_static.py
tools/validate_ash_basetrain_unified_atlas_mcu_gpu_resident_expert_bucket_view_and_heterogeneous_dispatch_r8a_static.py
```

Dead success markers are not retained only to satisfy validators.

## 12. Tests added

Prefix:

```text
r3h_cf8_
```

Five tests are present in source:

```text
r3h_cf8_source_binding_cardinality_is_exact
r3h_cf8_success_chain_is_order_sensitive
r3h_cf8_p2_non_admission_uses_fixed_reason_counters
r3h_cf8_failure_detail_is_first_only
r3h_cf8_host_retirement_tracks_wave_bounds
```

User-side command:

```powershell
cargo test -p base_train --lib --release --locked r3h_cf8_ -- --nocapture
```

A zero-test result is not PASS.

## 13. Preserved semantics

CF8 changes no:

```text
optimizer / Muon / HiMuon mathematics
BP-DK policy
source / actual / local counterfactual semantics
WGSL / Device / Queue / pipeline / bind group
atlas geometry / submission count / copy geometry
CF2 borrowed mapped consumption
CF3 submission lease behavior
CF4 observer checkpoint streaming
CF5 compact objective projection
CF6 packed-span validation summary
RAM36 hard limit
R3C consuming commit
R3G completion-before-reuse
checkpoint ABI
```

CF6 scheduler is byte-preserved by this bake.

## 14. 512 MiB boundary

CF8 does not claim to repair:

```text
memory allocation of 536870912 bytes failed
```

Its exact allocation owner remains `UNKNOWN / 판단불가` from current physical evidence. Any behavior change after CF8 still requires controlled attribution.

## 15. Bake delta

```text
ADD 0
MOD 5
DEL 0
```

Production source:

```text
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
parent SHA-256 48099ce049f37ce0ac32433273e1f8701cd65d636206d8ee01dbf09146615948
CF8   SHA-256 60dd15c922783fd72d1eb7f1586cadcb70dec7056a66488edca18177f85067ea
```

CF6 scheduler preserved:

```text
57c5c0f2140196acbce35c315fd19c7bbdaf26909221d1bfba6069cdbbc7b308
```

Changed validator SHA-256:

```text
e4fbd88e2ecd57bf83aa1aae468e6353600446bb1093c85cd561fc819f41a468  source-packing validator
c168aa1f09a592f268c42a38dee10c69ef8e800b30df65fd6e78046393bb8531  streaming-retirement validator
b0eda40851c364d950c5c399382829ceab5d7c9ebceed3477dcdab135b2efe66  P4 lease validator
96f1505dfe35f875d4e8fefc1f29a5a3ea0e6aa66ed658b7cde9c67dd7540be5  R8A validator
```

Source delta digest over sorted changed path/SHA pairs:

```text
6cd8d843ada0e45c662de982fc70314dc21f09f2e247fb2c3d606aa0d177e6fd
```

## 16. Code-only archives

Overlay:

```text
ASH_EVE_MCU_R3H_CF8_PRODUCTION_RUNTIME_EVIDENCE_COMPACTION_OVERLAY_CODE_ONLY.zip
SHA-256 fbb5937a406d8853252f8d5ee253fb3db875f2b422a8fbf9707a9e40463d7e4d
FILES 5
CRC PASS
```

Full applied tree:

```text
ASH_PASS3_EVE_MCU_R3H_CF8_PRODUCTION_RUNTIME_EVIDENCE_COMPACTION_CODE_ONLY.zip
SHA-256 b7dcf05dbe80f4511c420f95eafcf393310c150caeb594794ca17ca8b3f6bde9
FILES 8426
CRC PASS
```

Both archives contain:

```text
specs/ entries     0
artifacts/ entries 0
manifests/ entries 0
Markdown files     0
__pycache__ / pyc  0
```

`Cargo.toml` and `Cargo.lock` remain in the full archive because they are build inputs, not generated runtime manifests.

## 17. Bake-environment evidence

Performed:

```text
CF8 source static-shape checks             PASS
retired success-marker absence             PASS
CF8 terminal marker presence               PASS
r3h_cf8_ source test count                 5
Python syntax for modified validators      PASS
ZIP CRC                                     PASS
code-only exclusion audit                  PASS
CF6 scheduler byte preservation            PASS
```

Bake environment limitation:

```text
cargo     unavailable
rustc     unavailable
rustfmt   unavailable
```

Therefore:

```text
RUST PARSE / FORMAT    UNVERIFIED
RUST COMPILE           UNVERIFIED
RUST UNIT TEST         NOT RUN
PHYSICAL               NOT RUN
PERFORMANCE            UNMEASURED
```

Sampled parent validators already fail unrelated stale exact-string expectations in the CF6 parent (atlas-page authority / momentum mutation and a P4 field token). CF8 does not widen scope to repair those parent drifts. The R8A validator also requires a `specs/` file intentionally absent from code-only archives.

## 18. Promotion

Targets:

```text
PASS_EVE_MCU_R3H_CF8_PRODUCTION_RUNTIME_EVIDENCE_COMPACTION
PASS_EVE_MCU_R3H_CF8_EXACT_RUNTIME_EVIDENCE_AGGREGATION
PASS_EVE_MCU_R3H_CF8_PHYSICAL_COMPACT_RUNTIME_EVIDENCE
PASS_EVE_MCU_R3H_CF8_MEASURED_LOGGING_OVERHEAD_REDUCTION
```

Current bake state:

```text
HOLD_EVE_MCU_R3H_CF8_COMPILE_AND_PHYSICAL_UNPROVEN
```

## 19. Completion law

CF8 promotes only when the real workspace establishes:

1. parent validation logic still executes;
2. targeted successful per-wave text output is absent;
3. bounded counters replace success cardinality without wave-history allocation;
4. success-chain ordering tests pass;
5. P2 persisted evidence remains intact;
6. first nonfatal P2 failure detail remains available;
7. existing parameter-terminal receipts remain valid;
8. CF6 summaries remain unchanged;
9. Rust compile/tests pass;
10. physical execution emits one compact CF8 summary per completed affected parameter.

> CF8 reduces successful runtime-evidence representation cost. It does not weaken validation, change optimizer/GPU semantics, or claim to resolve the unresolved 512 MiB allocation failure.
