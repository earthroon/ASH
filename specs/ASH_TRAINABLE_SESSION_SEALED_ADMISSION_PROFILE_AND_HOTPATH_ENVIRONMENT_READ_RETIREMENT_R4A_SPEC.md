# ASH-TRAINABLE-SESSION-SEALED-ADMISSION-PROFILE-AND-HOTPATH-ENVIRONMENT-READ-RETIREMENT-R4A

## 0. Revision

```text
Patch ID:
ASH-TRAINABLE-SESSION
-SEALED-ADMISSION-PROFILE
-AND-HOTPATH-ENVIRONMENT-READ-RETIREMENT-R4A

Short name:
ASH TRAINABLE SESSION R4A
SEALED ADMISSION PROFILE + HOTPATH ENVIRONMENT READ RETIREMENT

Status:
STATIC MATERIALIZATION RELEASE

Rust compile PASS:                 NOT CLAIMED
GPU physical PASS:                 NOT CLAIMED
environment-read physical PASS:    NOT CLAIMED
cross-invocation physical PASS:    NOT CLAIMED
```

Static token:

```text
PASS_ASH_TRAINABLE_SESSION_SEALED_ADMISSION_PROFILE_AND_HOTPATH_ENVIRONMENT_READ_RETIREMENT_R4A_STATIC
```

Physical state:

```text
HOLD_ASH_TRAINABLE_SESSION_R4A_PHYSICAL_PENDING
```

## 1. Direct Parent

Direct parent:

```text
ASH-TRAINABLE-SESSION
-ACTIVE-PRODUCTION-OWNER
-AND-CROSS-INVOCATION-RUNTIME-CUTOVER-R4
```

R4 makes one explicit trainable-session owner the live production lifetime authority. R4A freezes session-invariant semantic admission before that owner begins production invocation work.

R4A does not change Adam mathematics, HiMuon mathematics, optimizer routing, R3C/R3C1 commit semantics, R3D/R3E/R3F durability semantics, or MCU R7/R7A execution/resource authority.

## 2. Problem Closed

Before R4A, the same live R4 session could still reach semantic `from_environment()` and process-environment reads from production setup and hot execution helpers. That permits ambient process state to participate repeatedly in one already-running runtime incarnation.

R4A changes the authority relation to:

```text
raw config + ASH_* environment + qualification bindings
        -> one typed admission profile
        -> one immutable admission seal
        -> one R4 trainable session
        -> all successor invocations
```

Environment is admission input, not continuing runtime semantic authority.

## 3. Materialized Profile ABI

New module:

```text
crates/base_train/src/trainable_session_admission_profile_r4a.rs
```

Materialized typed children include:

```text
EveAdmissionProfileR4A
AdamWAdmissionProfileR4A
HiMuonAdmissionProfileR4A
McuAdmissionProfileR4A
WeightAdmissionProfileR4A
DurabilityAdmissionProfileR4A
MemoryAdmissionProfileR4A
CompatibilityAdmissionProfileR4A
TrainableSessionAdmissionProfileR4A
TrainableSessionAdmissionSealR4A
```

Mode combinations are represented with typed enums including:

```text
TrainableSessionExecutionModeR4A
McuResourceModeR4A
```

The new R4A module contains no authoritative Rust `if` branch; new state decisions are expressed with `match`.

## 4. Profile and Seal Identity

The profile binds session-invariant execution facts including:

```text
Eve R3/R3A/R3G admission
Adam optimizer identity and exact learning-rate / weight-decay bit patterns
HiMuon production admission and Wave lifetime modes
MCU R7/R7A admission and arena bounds
Weight residency / R3E policy
R3D/R3E/R3F durability admission
RAM36 / exact inventory admission
compatibility mode
backend identity
```

R4A also binds a SHA-256 digest of the complete serialized:

```text
BaseTrainingRuntimeConfig
BaseOptimizerConfig
BaseBackendRuntimeConfig
```

This `raw_runtime_config_digest` is checked at every R4 invocation entry. Existing code may still borrow immutable raw config fields during this revision, but any semantic mutation of those runtime config objects inside one session fails closed.

## 5. Environment Snapshot

At admission R4A snapshots all visible `ASH_*` key/value pairs, sorts them by key and binds only the resulting digest and count into the runtime seal.

The general environment map is not retained as a hot runtime lookup authority.

Fresh process/session admission may produce a different snapshot and a different seal.

## 6. Production Muon Environment Seal

R4A pre-resolves the current production-Muon environment-controlled semantic bundle before the R4 owner begins invocation work.

The sealed bundle includes the exact resolved values for:

```text
D10 production runtime admission receipt
active fusion replay config
BP/DK local counterfactual config
BP/DK counterfactual physical execution config
BP/DK counterfactual effect ledger config
BP/DK one-step objective probe config
BP/DK fusion trajectory config
BP/DK fusion calibration config
HybridDeviceCommitRuntimeMode
immutable MCU qualification bundle runtime binding
Muon Wave host-retirement mode
Muon Wave source-packing-retirement mode
Muon Wave host-scratch-slab-reuse mode
BP/DK production startup-binding path
```

`ProductionMuonRuntime` gains an R4A constructor that consumes this resolved profile rather than re-resolving those semantics from the environment.

Historical constructors retain environment reads for compatibility when R4A hotpath retirement is disabled.

## 7. MCU Active Transactional Commit Cutover

Historically the R6 production scheduler repeatedly evaluated:

```text
McuActiveTransactionalCommitModeR1::from_environment()
```

around restart validation, prepare and finalize boundaries.

Under admitted R4A the mode is resolved once during profile construction and the generation path consumes:

```text
seal.profile.mcu.active_transactional_commit_r1
```

The historical environment expression remains only as a compatibility/static-parent witness outside the active sealed branch.

## 8. D10 Runtime Admission Cutover

When R4A hotpath retirement is active, the first `ProductionMuonRuntime` materialization consumes the D10 admission receipt already resolved into the R4A seal.

A restored R4 runtime continues to republish the retained ProductionMuonRuntime admission receipt exactly as before.

The environment-based D10 path remains compatibility-only when R4A retirement is disabled.

## 9. HiMuon Wave Hotpath Cutover

The three existing Wave-time environment reads:

```text
ASH_MUON_ATLAS_WAVE_STREAMING_HOST_RETIREMENT_R1
ASH_MUON_ATLAS_WAVE_SOURCE_PACKING_RETIREMENT_R1
ASH_MUON_ATLAS_WAVE_HOST_SCRATCH_SLAB_REUSE_R1
```

are resolved at R4A admission and stored in `ProductionMuonExecutionRuntime` for the R4A path.

`execute_muon_parameter` consumes the sealed values. Environment reads remain only as compatibility fallbacks when no R4A environment profile was supplied.

## 10. BP/DK Startup Binding Cutover

The production startup-binding path used by Native07D-B control evidence is captured in the R4A ProductionMuon environment profile and retained in `ProductionMuonExecutionRuntime`.

The deep production method consumes this retained path when present. Direct environment lookup remains a compatibility fallback only.

## 11. R4 Owner Binding

`TrainableSessionRuntimeR4` now owns an optional exact:

```text
TrainableSessionAdmissionSealR4A
```

R4A production requires the seal before invocation entry.

The seal cannot be replaced during the live session. Invocation receipts include the same R4A seal digest and zero static hotpath environment/config-reparse deltas.

The production pipeline builds the seal before opening the R4 owner when R4A admission is enabled.

## 12. Configuration Surface

New default-OFF fields:

```text
admit_trainable_session_sealed_admission_profile_r4a
admit_trainable_session_hotpath_environment_read_retirement_r4a
```

Hotpath environment-read retirement requires the sealed-profile parent.

R4A itself requires the R4 active production owner.

## 13. Receipt

Every R4A invocation output root receives:

```text
trainable_session_admission_r4a.json
```

binding:

```text
profile digest
seal digest
environment snapshot digest
environment input count
semantic admission-time environment-resolution count
physicalPassClaimed = false
```

R4 invocation receipts also bind the R4A seal digest.

## 14. What Is Retired

The active R4A source path retires repeated semantic environment resolution for the specific production authorities materialized by this revision:

```text
MCU P3 active-transaction mode
D10 runtime admission
BP/DK and fusion runtime modes listed above
Hybrid B06 mode during ProductionMuonRuntime construction
MCU qualification bundle environment binding
Muon Wave streaming/source/slab modes
BP/DK startup-binding path
```

## 15. Explicit Remaining Compatibility Reads

R4A does not claim removal of every `std::env` call in BaseTrain.

Examples intentionally outside the claimed semantic hotpath retirement include:

```text
D09 BenchmarkLane diagnostic output selection
process executable discovery
qualification/test fixture paths
legacy constructors and compatibility branches
```

R4A also does not yet remove the raw `BaseTrainConfig` parameter from the entire giant R6 execution function. Instead the full runtime-config digest is sealed and checked at invocation entry while critical semantic ambient reads are replaced with typed profile values.

## 16. Static Validation

Validator:

```text
tools/validate_ash_trainable_session_sealed_admission_profile_hotpath_environment_read_retirement_r4a_static.py
```

Current result:

```text
65 / 65 PASS
```

Static token:

```text
PASS_ASH_TRAINABLE_SESSION_SEALED_ADMISSION_PROFILE_AND_HOTPATH_ENVIRONMENT_READ_RETIREMENT_R4A_STATIC
```

## 17. Parent Regression

Current bake retains:

```text
Trainable Session R4       64 / 64 PASS
Eve R3G                    35 / 35 PASS
MCU SESSION R7             55 / 55 PASS
MCU R7A                    73 / 73 PASS
R3C                        18 / 18 PASS
R3C1                       30 / 30 PASS
R3D                        41 / 41 PASS
R3E                        52 / 52 PASS
R3F                        66 / 66 PASS
Unified Atlas MCU R6       PASS
Mixed-precision MCU R7     PASS
SubmissionEpoch async      PASS
Resident Weight validator  67 / 67 PASS
```

Two historical direct-parent baselines remain unchanged and are not R4A regressions:

```text
RAM exact inventory        66 / 67
N8 RAM resume-cut         117 / 118
```

Both reproduce identically on the direct R4 parent ZIP.

## 18. Compile Boundary

The bake environment exposes no `cargo`, `rustc` or `rustfmt` executable.

Therefore Rust compile PASS is not claimed.

The R4A Python validator passes `py_compile`; changed Rust files pass UTF-8 and structural delimiter checks.

## 19. Physical Qualification

Physical promotion requires one R4/R4A session with multiple live invocations and must prove at minimum:

```text
profile build count = 1
profile replacement count = 0
same seal digest across invocations
runtime config digest stable
semantic hotpath environment read count = 0
semantic hotpath config reparse count = 0
process environment mutation cannot change the active session
fresh session may observe newly admitted configuration
R4 live runtime reconstruction count = 0
R3C1 commit atomicity preserved
no numerical divergence
```

Until then:

```text
HOLD_ASH_TRAINABLE_SESSION_R4A_PHYSICAL_PENDING
```

## 20. Explicit Non-claims

R4A does not claim:

```text
all ASH environment access removed
BaseTrainConfig removed from hot execution signatures
all configuration booleans eliminated
all config state converted to enums
ProductionMuonRuntime decomposed
MCU children physically extracted
HiMuon segmented momentum complete
multi-device execution
tensor parallelism
```

## 21. Direct Successor

Recommended next structural revision:

```text
ASH-MCU
-CHILD-AUTHORITY-PHYSICAL-EXTRACTION
-AND-GENERATION-RUNTIME-OWNERSHIP-CLOSURE-R7B
```

R4A fixes the session configuration axis so R7B can move physical MCU children without allowing ambient configuration to change ownership semantics mid-session.

## 22. Final Law

> Environment and raw configuration decide how a trainable session is admitted. They do not continuously redefine the meaning of that already-running session.

> Critical production semantic environment decisions are resolved once into typed profile state; remaining raw runtime config is immutable by exact session digest.
