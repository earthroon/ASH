# ASH-BP-DK-ACTIVE-FUSION-PHYSICAL-QUALIFICATION-08A

## Status

```text
Patch ID: ASH-BP-DK-ACTIVE-FUSION-PHYSICAL-QUALIFICATION-08A
Direct parent: ASH-BP-DK-ACTIVE-FUSION-POST-UPDATE-EFFECTIVENESS-LEDGER-07
Required upstream: 06 / 05 / 04 / 03B / 03A / 02 / 01 / 00
Purpose: physically qualify the already-wired 05-07 active Fusion/Fission path
New fusion policy: none
New Delta-K formula: none
New Muon mathematics: none
New WGPU fused shader: none
Precision authority: unchanged
Residency policy authority: unchanged
Performance promotion: forbidden
```

## Central SSOT

08A does not introduce a new optimizer algorithm. It establishes a capability-bound physical qualification surface for the existing active path:

```text
05 actual Fusion/Fission authority
+ 06 deterministic replay authority
+ 07 POST ledger authority
        -> Rust compile
        -> production WGSL module/pipeline creation
        -> physical FusedRight/FusedDown dispatch
        -> CPU/GPU numerical comparison
        -> same-path exact replay comparison
        -> real 05 planner transition-state-machine fixtures
        -> real 07 ledger-runtime pending/commit/abort/reload fixtures
        -> capability-bound qualification receipt
```

`FullyQualified` is reserved for an additional whole-production transaction witness that also observes the scheduler's actual `commit_active_state()` success/failure boundary and complete checkpoint/restart parity. The current bake does not fabricate that evidence.

## Qualification states

The typed state surface distinguishes:

```text
SourceContractReady
RustCompileQualified
ShaderQualified
PhysicalDispatchQualified
NumericalQualified
ReplayQualified
TransactionQualified
RestartQualified
FullyQualified

UnsupportedCapability
InsufficientPhysicalEvidence
NumericalMismatch
ReplayMismatch
TransactionMismatch
RestartMismatch
StructuralContradiction
```

A path that cannot be observed on the current device is not labelled false. It is `UnsupportedCapability` or insufficient physical evidence. A physically executed path that disagrees with its numerical/reference contract is `NumericalMismatch`.

## Capability-bound identity

Qualification is sealed to a concrete physical identity containing:

```text
backend revision
adapter name / backend / device type
vendor / device ID
driver / driver info
feature digest
limit digest
observed subgroup size
fused kernel revision
serial fused WGSL SHA-256
ExactSubgroup32 fused WGSL SHA-256
capability digest
```

Qualification on one capability digest is not automatically reusable on another device/driver/feature/limit/kernel identity.

## Production source reuse

08A reuses the 05 production backend and shaders directly:

```text
TensorCubeFusedPairMuonExecutor
base_train_tensorcube_fused_pair_muon_16x32.wgsl
base_train_tensorcube_fused_pair_muon_16x32_exact_subgroup32_norm.wgsl
```

Parent SHA anchors remain byte-preserved in the 08A bake:

```text
crates/burn_webgpu_backend/src/tensorcube_fused_pair_muon.rs
cebba82183a627d5c7d4a464398b56e63f833fff3ecd6b4b37c9c5ace970bc1d

base_train_tensorcube_fused_pair_muon_16x32.wgsl
4a84858058737977d8636491f58301d902b358c2c0c1d26623cf2632bf3bd6d6

base_train_tensorcube_fused_pair_muon_16x32_exact_subgroup32_norm.wgsl
2ab9700df95b67fd4bd337392a8e6aef99195e1ae29f8e381cfd9d0e1c61e369
```

No qualification-only WGSL is introduced.

## CPU rectangular Muon oracle

08A introduces an independent CPU oracle that reproduces the existing 05 fused mathematics without changing production authority:

```text
momentum recurrence
Nesterov recurrence
F32/BF16 working projection contract
full fused Frobenius normalization
existing Newton-Schulz coefficients and step count
existing weight-decay / learning-rate update
```

RIGHT uses the production logical mapping:

```text
16x16 A | 16x16 B -> 16x32 work matrix
```

DOWN uses the production transposed work mapping:

```text
32x16 logical A/B
-> 16x32 transposed work matrix
-> Muon
-> canonical A/B scatter
```

The oracle does not parse TensorCube IDs and does not read back gradients.

## Numerical qualification policy

08A explicitly reuses the tolerance values already established by the existing TensorCube parity harness line:

```text
revision: ASH_TENSORCUBE_EXISTING_PARITY_TOLERANCE_R1
absolute tolerance: 1e-4
relative tolerance: 1e-4
mean absolute tolerance: 1e-5
```

The policy is revisioned and digest-bound. There is no automatic tolerance widening.

Each numerical receipt includes:

```text
max absolute error
max relative error
mean absolute error
RMS error
first failure index
reference value at first failure
physical value at first failure
```

## Deterministic physical fixtures

The WGPU harness uses fixed non-random, non-uniform and asymmetric lhs/rhs data. This is intended to expose:

```text
lhs/rhs swap
RIGHT concatenate error
DOWN transpose error
canonical scatter-back error
```

The primary physical fixtures are:

```text
Q08A-F1-FUSEDRIGHT-SERIAL
Q08A-F2-FUSEDDOWN-SERIAL
Q08A-F1-FUSEDRIGHT-SUBGROUP32
Q08A-F2-FUSEDDOWN-SUBGROUP32
```

Each supported fixture uses the actual `TensorCubeFusedPairMuonExecutor::execute_with_norm_path()` and checks:

```text
candidate weight CPU/GPU parity
candidate momentum CPU/GPU parity
orthogonal-update CPU/GPU parity
physical dispatch/workgroup/queue/poll witnesses
full-gradient D2H bytes == 0
```

## Same-path exact candidate replay

Each supported fixture executes the same production fused path a second time from the exact same:

```text
packed gradient lease
source weight
source momentum
optimizer step
kernel profile
norm-reduction path
orientation
```

The primary and replay results must have exact F32-bit SHA-256 equality for:

```text
candidate weight
candidate momentum
orthogonal update
```

CPU/GPU parity uses the explicit numerical policy; same-path primary/replay uses exact digest equality. These gates are not conflated.

## ExactSubgroup32 capability handling

The harness requests the SUBGROUP feature only when the adapter exposes it and uses the existing physical subgroup-size probe.

If ExactSubgroup32 is unsupported or the observed subgroup size is not 32:

```text
ExactSubgroup32 = unsupported for current capability
```

Serial success cannot silently promote ExactSubgroup32. The runner also exposes an explicit `-RequireExactSubgroup32` switch for qualification runs where subgroup32 is mandatory.

## Real 05 planner-state-machine qualification

The qualification binary uses the actual `AshBpDkFusionFissionPlannerRuntime`, not a shadow planner implementation.

It constructs typed valid 04 graph fixtures and physically executes the Rust state machine through:

```text
NewFusion
-> commit pending planner state
-> RetainedFusion
-> commit
-> SoftFission
-> commit
-> Cooldown Local
```

A separate lineage executes:

```text
NewFusion
-> commit
-> current graph missing edge
-> HardFission
```

The first fusion generation is also run against a cloned pre-call planner runtime to require exact plan equality. This is the 05 logical replay qualification surface.

The qualification policy used here is a test/qualification fixture written to an isolated temporary JSON file. It is not installed as a production default and is removed/restored after the fixture.

## Real 07 ledger-runtime transaction fixtures

The qualification binary uses the real `AshBpDkPostUpdateLedgerRuntime` to verify:

```text
pending entry/head remain separate from committed head
persist candidate entry/head
commit pending -> committed head promotion
reload committed head from candidate checkpoint directory
stage next generation
abort pending -> committed head unchanged
```

These fields are reported separately as:

```text
ledger_runtime_commit_qualified
ledger_runtime_abort_qualified
ledger_runtime_restart_qualified
```

They must not be confused with whole-scheduler transaction qualification.

## Whole-production transaction boundary remains explicit

The current low-level/synthetic qualification harness deliberately leaves these full promotion fields false:

```text
post_update_metrics_qualified = false
ledger_commit_qualified = false
ledger_abort_qualified = false
checkpoint_restart_qualified = false
```

Reason: those claims require the actual BaseTrain production transaction to witness:

```text
physical 05 candidate
-> 06 replay
-> 07 POST receipt
-> candidate checkpoint persistence
-> commit_active_state() success/failure
-> record_step_commit() / record_step_abort()
-> process destroy/restore checkpoint
-> next-generation exact replay/ledger parity
```

Static source wiring and isolated ledger-runtime fixtures are insufficient to claim that full sequence physically completed.

## No full-gradient D2H

The qualification gradient is created as a WGPU storage lease and consumed directly by the production fused executor. Both primary and replay receipts require:

```text
gradient_payload_readback_bytes = 0
```

Candidate output readback is allowed because the production 05 path already materializes candidate weight/momentum/update for commit/scatter and numerical qualification.

## User-local physical runner

08A adds:

```text
tools/run_ash_bp_dk_active_fusion_physical_qualification_08a.ps1
```

The runner performs:

```text
08A static contract
cargo fmt --check
cargo check qualification binary
cargo run --release qualification binary
```

Default output:

```text
target/ash-qualification/active-fusion-08a/<capability-digest>/qualification.json
```

Generated qualification receipts are runtime evidence and are not shipped inside the baked ZIP.

## CF1 binding

08A is appended to the existing CF1 static-validator lineage after 07. CF1 also performs a compile check for:

```text
--bin ash_bp_dk_active_fusion_physical_qualification_08a
```

CF1 does not automatically run the physical GPU harness because a build/CI environment may lack a qualifying WGPU adapter. Physical execution remains an explicit qualification command.

## Changed files

The 08A overlay contains exactly eight files:

```text
crates/ash_core/src/active_fusion_physical_qualification.rs
crates/ash_core/src/lib.rs
crates/base_train/src/bin/ash_bp_dk_active_fusion_physical_qualification_08a.rs
crates/base_train/src/bp_delta_k_active_fusion_physical_qualification.rs
crates/base_train/src/lib.rs
tools/run_ash_bp_dk_active_fusion_physical_qualification_08a.ps1
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_active_fusion_physical_qualification_08a_static.py
```

05 fused backend/WGSL, 06 replay implementation, 07 POST-ledger implementation and the production scheduler/callsite are not rewritten by 08A.

## Static validation

New gate:

```text
validate_ash_bp_dk_active_fusion_physical_qualification_08a_static.py
236/236 PASS
```

Revalidated BP-DeltaK lineage in the bake environment:

```text
00 Observation Contract                         149/149 PASS
01 Local BP-DK                                  134/134 PASS
02 Generation/Revision/Stale Seal               243/243 PASS
03A Bridge Pair Evidence                        148/148 PASS
03B Bridge Temporal Coupling                    157/157 PASS
04 Fusion Candidate Graph                       235/235 PASS
05 Active Fusion/Fission Planner                293/293 PASS
06 Active Fusion Deterministic Replay           210/210 PASS
07 POST Update Effectiveness Ledger             206/206 PASS
08A Physical Qualification source contract      236/236 PASS
```

Revalidated Local Muon lineage:

```text
Local Muon optimizer                            101/101 PASS
FirstCandidate registry                          97/97 PASS
Multi-tile batch                                 61/61 PASS
Production callsite                              63/63 PASS
Registry canonical-loader repair                 38/38 PASS
ExactSubgroup32 norm                            128/128 PASS
X PAD17                                          52/52 PASS
Generation-sealed immutable cache                66/66 PASS
Immutable-cache backend rebind                   35/35 PASS
```

## Bake-environment limitation

The bake environment used to author 08A does not contain `cargo`, `rustc`, `rustfmt`, or a usable physical WGPU adapter. Therefore no generated qualification receipt was produced here and the following are not claimed:

```text
Rust qualification binary compiled physically
production WGSL modules created on a real device
FusedRight/FusedDown GPU parity passed
ExactSubgroup32 physically passed
same-path GPU replay passed
whole scheduler transaction passed
checkpoint/restart physical parity passed
```

Current bake status is therefore:

```text
08A_QUALIFICATION_HARNESS_SOURCE_WIRED
08A_STATIC_SOURCE_CONTRACT_CLOSED
PARENT_05_06_07_PRODUCTION_SOURCES_PRESERVED
PHYSICAL_QUALIFICATION_PENDING_USER_LOCAL_EXECUTION
FULLY_QUALIFIED_NOT_CLAIMED
```

## Required path to FullyQualified

A full 08A promotion receipt must eventually contain physical evidence for the current capability tuple showing:

```text
Rust compile PASS
production WGSL module/pipeline creation PASS
FusedRight physical dispatch + CPU/GPU numerical parity PASS
FusedDown physical dispatch + transpose/scatter parity PASS
active production norm path qualified
all-Local parent control PASS
mixed Local/Fused ownership PASS
New/Retained Fusion transition PASS
Soft/Hard Fission PASS
Cooldown PASS
06 PlanOnly exact replay PASS
06 CandidateDigest exact same-path replay PASS
07 POST RMS/cosine PASS
actual scheduler active commit -> ledger promotion PASS
actual scheduler failed commit -> pending-ledger abort PASS
checkpoint destroy/restore -> next-plan/candidate/ledger parity PASS
full-gradient D2H == 0
silent Local fallback == 0
runtime replan == 0
```

Only then may `FullyQualified` be emitted for that capability digest.

## Non-goals

```text
No new fusion threshold
No new planner score
No new Delta-K equation
No new Newton-Schulz coefficients
No new fused WGSL
No silent capability substitution
No Serial-to-Subgroup promotion substitution
No numerical tolerance auto-widening
No precision policy
No residency policy
No performance/throughput promotion
No Fusion-is-better-than-Local claim
```

## Natural successor

After the user-local whole 08A physical qualification closes, the next correctness revision is:

```text
ASH-BP-DK-ACTIVE-FUSION-SAME-SOURCE-LOCAL-COUNTERFACTUAL-08B
```

08B can execute the actual fused candidate and a non-committing all-Local candidate from the exact same gradient/weight/momentum source. Only that later revision can begin causal statements about how Fusion changes the update relative to Local.

## Bake seal

```text
BAKE_ASH_BP_DK_ACTIVE_FUSION_PHYSICAL_QUALIFICATION_08A

07_DIRECT_PARENT
05_PRODUCTION_FUSED_BACKEND_BYTE_PRESERVED
05_PRODUCTION_FUSED_WGSL_BYTE_PRESERVED
06_REPLAY_SOURCE_PRESERVED
07_POST_LEDGER_SOURCE_PRESERVED

CAPABILITY_BOUND_QUALIFICATION_SCHEMA
EXPLICIT_EXISTING_TENSORCUBE_NUMERICAL_POLICY
NO_TOLERANCE_AUTO_WIDEN

CPU_RECTANGULAR_MUON_ORACLE_WIRED
FUSEDRIGHT_PHYSICAL_HARNESS_WIRED
FUSEDDOWN_PHYSICAL_HARNESS_WIRED
SERIAL_PHYSICAL_PATH_WIRED
EXACT_SUBGROUP32_CAPABILITY_GATED

CANDIDATE_WEIGHT_PARITY_GATE_WIRED
CANDIDATE_MOMENTUM_PARITY_GATE_WIRED
ORTHOGONAL_UPDATE_PARITY_GATE_WIRED
SAME_PATH_EXACT_CANDIDATE_REPLAY_GATE_WIRED

REAL_05_PLANNER_TRANSITION_FIXTURES_WIRED
NEW_FUSION_FIXTURE_WIRED
RETAINED_FUSION_FIXTURE_WIRED
SOFT_FISSION_FIXTURE_WIRED
HARD_FISSION_FIXTURE_WIRED
COOLDOWN_FIXTURE_WIRED

REAL_07_LEDGER_RUNTIME_COMMIT_ABORT_RELOAD_FIXTURES_WIRED
FULL_SCHEDULER_TRANSACTION_QUALIFICATION_NOT_FABRICATED
FULL_CHECKPOINT_RESTART_QUALIFICATION_NOT_FABRICATED

NO_NEW_GRADIENT_D2H
NO_NEW_FUSION_POLICY
NO_NEW_DELTAK_FORMULA
NO_NEW_MUON_MATHEMATICS
NO_PRECISION_AUTHORITY
NO_RESIDENCY_AUTHORITY
NO_PERFORMANCE_PROMOTION

STATIC_08A_236_OF_236_PASS
PARENT_STATIC_LINEAGE_PASS
PHYSICAL_QUALIFICATION_PENDING_USER_LOCAL_EXECUTION
FULLY_QUALIFIED_NOT_CLAIMED
```
