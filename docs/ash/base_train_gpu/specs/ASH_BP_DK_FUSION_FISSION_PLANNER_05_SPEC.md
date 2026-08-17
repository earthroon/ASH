# ASH-BP-DK-FUSION-FISSION-PLANNER-05

## Status

```text
Patch ID: ASH-BP-DK-FUSION-FISSION-PLANNER-05
Direct parent: ASH-BP-DK-FUSION-CANDIDATE-GRAPH-04
Required upstream: 03B / 03A / 02 / 01 / 00
Planner kind: active execution authority, not shadow
Fusion scope: same-parameter canonical 16x16 TensorCube pairs only
Maximum fusion domain: exactly two canonical cells
RIGHT pair: logical 16x32 Muon domain
DOWN pair: logical 32x16 domain executed through 16x32 transposed work orientation
Cross-parameter fusion: forbidden
Connected-component fusion: forbidden
Precision authority: unchanged
Residency policy authority: unchanged
```

## Central SSOT

05 is the first BP-DeltaK revision that can alter actual optimizer mathematics.

```text
04 immutable current-generation evidence graph
+ explicit revisioned planner policy
+ committed pair planner state
+ current fused-execution capability
        -> authoritative Local/Fused execution plan
        -> actual Local / Fused Muon candidate computation
```

A graph edge still does not imply fusion by itself. The 05 planner owns the decision; the WGPU executor owns physical candidate computation; the scheduler remains active/durable commit authority.

## Explicit operating modes

The production runtime recognizes:

```text
ASH_BP_DK_FUSION_PLANNER_MODE=DISABLED
ASH_BP_DK_FUSION_PLANNER_MODE=ACTIVE
```

If the variable is absent, the explicit control mode is `DISABLED`.

`ACTIVE` requires:

```text
ASH_BP_DK_FUSION_POLICY_PATH=<explicit JSON policy path>
```

There is no production default cosine or Delta-K threshold. Missing Active policy is an error rather than a silent default.

When the planner is Disabled, or when an Active plan contains no fused domains, the existing generation-sealed resident Local Muon path remains the execution path through `execute_resident_with_norm_path(...)`.

## Policy authority

`AshBpDkFusionFissionPolicy` owns:

```text
revision
fuse_cosine_min
fuse_information_max
fuse_material_min
fuse_delta_k_max
fuse_confirm_generations
fission_cosine_floor
fission_information_min
fission_material_floor
fission_delta_k_min
fission_confirm_generations
cooldown_generations
```

The canonical policy digest hashes exact F32 bit patterns and integer parameters.

Hysteresis validity is explicit:

```text
fission_cosine_floor < fuse_cosine_min
fission_information_min > fuse_information_max
fission_delta_k_min > fuse_delta_k_max
fission_material_floor <= fuse_material_min
fuse_confirm_generations >= 1
fission_confirm_generations >= 1
```

Invalid policies fail rather than being repaired.

## New fusion admission

A new pair can accumulate a fusion confirmation streak only when all four current edge predicates hold:

```text
gradient_cosine >= fuse_cosine_min
I_BRIDGE <= fuse_information_max
M_BRIDGE >= fuse_material_min
DeltaK_BRIDGE_PRE_smoothed <= fuse_delta_k_max
```

No weighted scalar `fusion_score`, compatibility score, priority score, or hidden collapse of local/Bridge evidence is introduced.

The pair becomes an actual fused execution domain only after:

```text
fuse_streak >= fuse_confirm_generations
```

A missing/Warming temporal edge resets Local-pair confirmation rather than carrying a stale streak across an evidence gap.

## Fission

Existing fused pairs are evaluated before any new pair is selected.

Hard fission is immediate when the current pair edge is absent or the current physical fused shape is unsupported. Topology/generation rebaselines also prevent stale fusion continuity.

Soft fission pressure is generated when any condition holds:

```text
gradient_cosine <= fission_cosine_floor
OR I_BRIDGE >= fission_information_min
OR M_BRIDGE <= fission_material_floor
OR DeltaK_BRIDGE_PRE_smoothed >= fission_delta_k_min
```

Actual soft fission occurs after:

```text
fission_streak >= fission_confirm_generations
```

A fissioned pair executes as two Local 16x16 TensorCubes in the same current optimizer generation. Optional cooldown blocks immediate re-fusion for the configured number of successful planner generations.

## Evidence-gap continuity

Pair confirmation state is generation-sensitive. A gap in planner observations cannot silently continue a prior fusion streak. Local streaks are reset across missing current edges, and explicit generation-gap rebaseline telemetry is recorded.

Planner pair state is independently sealed by:

```text
policy digest
03B Bridge topology digest
fused execution capability digest
last decision generation
```

The 04 graph topology/evidence digests remain execution-plan identity, while the persistent pair state uses the more stable 03B Bridge topology identity. This prevents a temporary Ready/Warming graph-edge change from being mistaken for physical topology mutation.

## No connected-component fusion

R1 domains contain at most two canonical cells.

Forbidden:

```text
A-B-C connected path -> one fused domain
2x2 four-cell fused domain
3-cell fused domain
diagonal fusion
cross-parameter fusion
cross-layer fusion
```

The planner performs deterministic non-overlapping pair selection only.

## Deterministic selection

Retained valid fused pairs reserve their canonical tiles before new candidates are considered.

Eligible new pairs are sorted lexicographically by:

```text
1. higher signed gradient cosine
2. lower I_BRIDGE
3. lower DeltaK_BRIDGE_PRE_smoothed
4. higher M_BRIDGE
5. lower canonical pair ordinal
```

The planner then performs deterministic greedy maximal matching:

```text
lhs unused AND rhs unused -> select and reserve
otherwise -> skip overlap
```

This revision does not claim maximum-weight matching or globally optimal matching.

## Canonical storage remains 16x16

Fusion changes the Muon orthogonalization execution domain, not canonical TensorCube storage.

Persistent state remains:

```text
weight tile A: canonical 16x16 slot
weight tile B: canonical 16x16 slot
momentum tile A: canonical 16x16 slot
momentum tile B: canonical 16x16 slot
```

There is no persistent 16x32/32x16 weight object and no persistent fused momentum layout.

This makes fission an execution-grouping change rather than a state-format conversion.

## Execution-plan contract

`AshBpDkFusionExecutionPlan` contains only:

```text
Local(tile)
FusedRight(pair)
FusedDown(pair)
```

Every full Muon tile must be covered exactly once. Fused domains cover exactly two tiles; Local domains cover exactly one. Duplicate ownership, uncovered tiles, cross-parameter pairs, or a fused pair not present in the current 04 graph fail closed.

The plan identity binds:

```text
parameter / generation identity
full tile count
04 graph topology digest
04 graph evidence digest
planner mode
planner policy revision/digest
current capability digest
committed planner-state digest
ordered execution domains
```

The plan digest is deterministic and becomes a replay surface for 06.

## Actual fused WGPU executor

05 adds a physically wired backend:

```text
TensorCubeFusedPairMuonExecutor
```

with shaders:

```text
base_train_tensorcube_fused_pair_muon_16x32.wgsl
base_train_tensorcube_fused_pair_muon_16x32_exact_subgroup32_norm.wgsl
```

A workgroup owns one selected pair. The logical fused payload contains 512 F32 values, while the workgroup remains 256 invocations with each invocation handling two logical elements. No 512-thread hardware assumption is made.

The backend probes current WGPU limits and subgroup capability before planner admission.

## RIGHT physical orientation

A RIGHT pair is interpreted directly as:

```text
lhs 16x16 | rhs 16x16 -> working matrix 16x32
```

The fused Newton-Schulz row Gram is therefore:

```text
X X^T -> 16x16
```

with the k reduction spanning 32 working columns.

## DOWN physical orientation

A DOWN pair is logically:

```text
lhs 16x16
---------
rhs 16x16
= 32x16
```

The shader maps it into the same 16x32 work orientation by transposition, runs the same rectangular Muon core, then maps the result back to the two canonical 16x16 payload slots.

Thus both R1 orientations retain a 16x16 Gram authority without creating a new 32x32 Newton-Schulz domain.

## Muon mathematical preservation

05 preserves the parent Local Muon authorities for:

```text
momentum recurrence
Nesterov recurrence
normalization epsilon
Newton-Schulz coefficients
Newton-Schulz iteration count
working precision projection
learning-rate authority
weight-decay formula
nonfinite fail behavior
```

The intentional mathematical change is the orthogonalization domain geometry for selected adjacent pairs.

Existing Local Muon WGSL files remain byte-preserved.

## Source and candidate buffer separation

Within Local/Fused kernel execution:

```text
gradient binding: read only
source weight binding: read only
source momentum binding: read only
candidate weight: separate writable output
candidate momentum: separate writable output
orthogonal update: separate writable output
```

The fused helper never writes `ProductionMuonRuntime::momentum` while the physical Local/Fused candidate for that parameter is still being assembled. Candidate outputs are first scattered into canonical per-tile positions and exact tile ownership is verified.

### Parent RAM fail-stop authority remains

05 deliberately does **not** allocate a second whole-model F32 momentum slab. After one parameter candidate succeeds, the existing parent `ProductionMuonRuntime` may copy that parameter's candidate momentum into its run-local RAM candidate slab before the final active-state commit, preserving the established parent fail-stop/no-rollback contract and the 36-GiB process-memory design.

This RAM slab is not a durable partial optimizer commit. If a later part of the optimizer generation fails, the run fails stop; the prior durable checkpoint is restart authority. 05 does not claim same-process rollback of the parent momentum slab.

`No partial optimizer commit` in this revision means no partial active/durable model generation is promoted and no fused failure is converted into a silently different committed route.

## No silent local fallback

Planner admission and runtime failure are separate.

If a shape is unsupported before planning, the edge is not admitted as fused.

If an already-authoritative fused plan reaches physical execution and that execution fails:

```text
optimizer generation fails
```

The runtime must not silently replace the domain with two Local executions, select a second-best pair, or rewrite the plan after execution begins.

05 hard-zero authorities include:

```text
silent_local_fallback_count = 0
runtime_replan_count = 0
cross_parameter_fusion_count = 0
connected_component_fusion_count = 0
domain_larger_than_two_count = 0
full_gradient_readback_count = 0
full_gradient_readback_bytes = 0
```

## Zero full-gradient D2H

The fused executor directly reads the existing generation-bound packed gradient lease. It never copies the full gradient payload to the host.

Candidate weights, candidate momentum, orthogonal updates, and compact status are read back because the current parent production path already materializes those candidate products before canonical commit/scatter. This must not be confused with gradient D2H.

## Current mixed-path residency/performance boundary

The all-Local control path preserves the existing generation-sealed immutable resident weight path.

When an Active plan contains at least one fused pair, the current 05 correctness-first mixed executor gathers the remaining Local source tiles and fused-pair source weights/momentum into candidate execution payloads. Consequently the mixed path can incur new source weight/momentum uploads and does not yet reuse the whole-parameter immutable resident cache for every planned sub-domain.

This is a performance/residency **implementation debt**, not a residency-policy authority migration. 05 makes no throughput or VRAM-traffic improvement claim. A later reusable fused workspace / resident sub-domain view should remove this upload debt without changing the 05 planner semantics.

## Planner temporal state

The planner persists pair-owned state:

```text
Local / Fused / Cooldown
fusion confirmation streak
fission confirmation streak
cooldown remaining
last decision generation
policy digest
Bridge topology digest
capability digest
```

Planner state is separate from 03B temporal Delta-K state.

Runtime sidecars are:

```text
bp_dk_fusion_fission_planner_state_manifest.json
bp_dk_fusion_fission_planner_state.json
```

These are runtime checkpoint sidecars and are not included as generated bake artifacts in the delivered code ZIP.

Payload length and SHA-256 are verified on restore. Split planner sidecars fail closed. A pre-05 checkpoint with neither sidecar is an explicit legacy cold start rather than a fabricated fused state.

## Planner candidate-state commit

Planner state itself uses pending-vs-committed separation.

```text
current graph + committed planner state
-> execution plan + pending planner state
```

Pending planner state is serialized in the candidate transaction and is promoted in memory only through `record_step_commit()` after the scheduler successfully commits the active model state.

On active-state commit failure, `record_step_abort()` discards pending 03B and 05 planner state.

The existing parent RAM Muon momentum remains the separate fail-stop authority described above.

## No optimizer topology mutation

05 changes current execution grouping only. It does not rewrite:

```text
FirstCandidate registry
Muon/AdamW parameter partition
canonical TensorCube IDs
canonical momentum offsets
AdamW residual ownership
model topology
```

Residual elements continue through the exact parent AdamW residual route.

## Changed files

The 05 overlay contains exactly eleven changed/new code files:

```text
crates/ash_core/src/bp_dk_fusion_fission_planner.rs
crates/ash_core/src/lib.rs
crates/base_train/src/bp_delta_k_fusion_fission_planner.rs
crates/base_train/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/shaders/base_train_tensorcube_fused_pair_muon_16x32.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_tensorcube_fused_pair_muon_16x32_exact_subgroup32_norm.wgsl
crates/burn_webgpu_backend/src/tensorcube_fused_pair_muon.rs
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_fusion_fission_planner_05_static.py
```

No generated artifact/manifest/report directory and no `*.sha256` sidecar is included in the baked ZIPs.

## Static validation

New source gate:

```text
validate_ash_bp_dk_fusion_fission_planner_05_static.py
293/293 PASS
```

Revalidated BP-DeltaK lineage:

```text
00 Observation Contract                 149/149 PASS
01 Local BP-DK                          134/134 PASS
02 Stale Observation Seal               243/243 PASS
03A Bridge Pair Evidence                148/148 PASS
03B Bridge Temporal Coupling            157/157 PASS
04 Fusion Candidate Graph               235/235 PASS
05 Active Fusion/Fission Planner        293/293 PASS
```

Revalidated Local Muon lineage:

```text
Local Muon optimizer                    101/101 PASS
FirstCandidate registry                  97/97 PASS
Multi-tile batch                         61/61 PASS
Production callsite                      63/63 PASS
Registry loader repair                   38/38 PASS
ExactSubgroup32 norm                    128/128 PASS
X PAD17                                  52/52 PASS
Generation-sealed immutable cache        66/66 PASS
Immutable-cache backend rebind           35/35 PASS
```

05 is appended to the CF1 static validator chain without rewriting the 04 validator's parent AllValidators closure.

## Physical verification boundary

The bake environment does not contain `cargo`, `rustc`, `rustfmt`, a WGSL validator binary, or a physical WGPU device/runtime. Therefore the following are **not claimed** by this source bake:

```text
Rust compile success
WGSL shader compile success
physical fused-right dispatch success
physical fused-down dispatch success
CPU/GPU rectangular Muon parity
actual training throughput improvement
active hardware promotion
```

The correct status is:

```text
ACTIVE_SOURCE_PATH_WIRED
STATIC_SOURCE_CONTRACT_CLOSED
PHYSICAL_GPU_EXECUTION_UNVERIFIED
```

User-local Cargo/WGPU execution is the physical execution SSOT.

## Required physical gates before ActiveVerified promotion

```text
cargo fmt / cargo check
CF1 compile chain reaches 05
FusedRight 16x32 CPU/GPU candidate-weight parity
FusedRight candidate-momentum parity
FusedDown 32x16/transposed-16x32 CPU/GPU parity
serial vs ExactSubgroup32 oracle parity
all-Local Disabled parent parity
actual fused dispatch receipt
actual fission-to-Local receipt
no tile double ownership
zero full-gradient D2H receipt
fused execution failure produces step failure, not Local fallback
checkpoint/restart planner-plan parity
```

Only after these physical gates pass may the line be promoted as active verified fusion.

## Non-goals

```text
No shadow-only planner
No cross-parameter fusion
No cross-layer fusion
No 3-cell or 2x2 fusion
No connected-component fusion
No persistent fused TensorCube object
No persistent fused momentum layout
No scalar fusion score
No universal hardcoded Delta-K threshold
No runtime Local fallback after fused-plan failure
No mid-step replanning
No 03A cosine rewrite
No 03B Delta-K formula rewrite
No 04 graph mutation
No AdamW residual takeover
No precision decision
No residency-policy decision
No throughput claim
```

## Natural successor

After physical 05 verification, the next correctness revision is:

```text
ASH-BP-DK-ACTIVE-FUSION-DETERMINISTIC-REPLAY-06
```

It should seal identical source model, canonical momentum, 03B temporal state, 04 graph, 05 planner state, policy, and capability to identical plan digest, Local/Fused domain assignment, candidate outputs, and committed generation.

A separate performance successor can then introduce fused-domain resident views / reusable candidate workspaces to remove the current correctness-first mixed-path upload debt without changing planner semantics.

## Promotion seal

```text
BAKE_ASH_BP_DK_FUSION_FISSION_PLANNER_05

ACTIVE_PLANNER_SOURCE_WIRED
ACTUAL_FUSED_EXECUTOR_SOURCE_WIRED

EXPLICIT_REVISIONED_POLICY
NO_UNIVERSAL_HARDCODED_THRESHOLD
NO_SCALAR_FUSION_SCORE

PAIR_FUSION_ONLY
MAX_TWO_CANONICAL_TENSORCUBES
NO_CONNECTED_COMPONENT_FUSION
NO_CROSS_PARAMETER_FUSION

FUSION_CONFIRMATION_STREAK
FISSION_HYSTERESIS
HARD_FISSION
COOLDOWN
EVIDENCE_GAP_STREAK_RESET

DETERMINISTIC_NONOVERLAPPING_SELECTION
EXISTING_FUSION_CONTINUITY_FIRST

RIGHT_IS_LOGICAL_16X32
DOWN_IS_LOGICAL_32X16_TRANSPOSED_TO_16X32_WORKING_DOMAIN
CANONICAL_16X16_STORAGE_PRESERVED

EXISTING_MUON_COEFFICIENTS_PRESERVED
ORTHOGONALIZATION_DOMAIN_GEOMETRY_IS_INTENTIONAL_CHANGE

KERNEL_SOURCE_WEIGHT_READ_ONLY
KERNEL_SOURCE_MOMENTUM_READ_ONLY
CANDIDATE_WEIGHT_SEPARATE
CANDIDATE_MOMENTUM_SEPARATE

PARENT_FAIL_STOP_RAM_MOMENTUM_CANDIDATE_PRESERVED
NO_SECOND_WHOLE_MODEL_MOMENTUM_SLAB
NO_DURABLE_PARTIAL_OPTIMIZER_COMMIT

NO_SILENT_LOCAL_FALLBACK
NO_RUNTIME_REPLAN
NO_FULL_GRADIENT_D2H

PLANNER_PENDING_STATE_SEPARATE
ACTIVE_MODEL_COMMIT_PRECEDES_PLANNER_STATE_COMMIT
FAILED_ACTIVE_COMMIT_ABORTS_PENDING_PLANNER_STATE

MIXED_PATH_RESIDENT_CACHE_REUSE_NOT_YET_OPTIMIZED
NO_PERFORMANCE_PROMOTION_CLAIM

STATIC_05_293_OF_293_PASS
PARENT_STATIC_LINEAGE_PASS
PHYSICAL_GPU_EXECUTION_UNVERIFIED
```
