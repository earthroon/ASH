# ASH-BP-DK-OBSERVATION-CONTRACT-AND-AUTHORITY-SEPARATION-00

## Status

```text
Patch ID:
ASH-BP-DK-OBSERVATION-CONTRACT-AND-AUTHORITY-SEPARATION-00

Code parent SSOT:
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-EXACT-SUBGROUP32-NORM-PARALLEL-REDUCTION-AND-SERIAL-ORACLE-R1 full body

Existing Delta-K parent authority:
Decode-time ASH Delta-K implementation

Scope:
Observation contract / domain identity / authority separation / read-only decode adapter

BP Delta-K formula implementation:
not yet

HiMuon fusion execution:
forbidden

Precision commit:
forbidden

Residency movement:
forbidden
```

## 1. Existing decode Delta-K is the parent implementation

This patch does not replace or reinterpret the existing decoding Delta-K path.

The existing canonical decode implementation remains:

```text
crates/ash_core/src/delta_k.rs
```

with the existing stateful decode observer:

```rust
DeltaKComputer
DeltaKSnapshot
```

and the structural law already present in the repository:

```text
DeltaK = I * M^2
```

The existing decode observer still owns its current decode-domain inputs and temporal state:

```text
ratio
qmap_density
prev_ratio
alpha
theta_low
theta_high
last snapshot
compact / mix / reverb
```

R0 does not feed BP gradients into `DeltaKComputer::update()` and does not share its mutable EMA/history state with training.

## 2. Decode parent byte preservation

The following existing decode-related files remain byte-identical to the code parent:

```text
crates/ash_core/src/delta_k.rs
SHA256 4c7d02ff7492f9c07ea9bd59c42085f8ccdad0f49866df600d0d535074cce836

crates/ash_core/src/delta_k_phase_projection.rs
SHA256 0313d1fe94988b31da423567547b14f443b869963a74d44bbb7865d7d8a758e4

crates/model_core/src/semantic_prior_scores.rs
SHA256 7db6e0b632b5265f62b1e5a9b3a4ff5cf25c8627eef3e293581d9bd94d675cc7

crates/model_core/src/qw_mcts_hdc_state_encoder.rs
SHA256 04799c9be0e6d88f0a946fa878698537a06efd6e8b3b56971155a381bfb4b8ff
```

Therefore this patch does not change:

```text
DeltaKComputer decode math
DeltaK temporal smoothing
compact / mix / reverb decode mode
Delta-K to phase projection
semantic prior deltak_scores
QW-MCTS-02 existing DeltaK source reuse seal
```

QW-MCTS-02 continues to declare:

```text
new_delta_k_math_added = false
```

because this R0 adds an observation contract, not replacement decode Delta-K math.

## 3. Shared structural law, domain-owned observers

The only shared mathematical contract introduced by R0 is the existing structural law identity:

```text
ASH_DK_STRUCTURAL_LAW_I_TIMES_M_SQUARED_R1

DeltaK = I * M^2
```

The meaning and production of `I` and `M` remain observer-domain responsibilities.

```text
Decode observer:
    existing ratio / qmap-density-derived I and M

BackpropPre observer:
    not implemented in R0

UpdatePost observer:
    not implemented in R0
```

R0 therefore creates no gradient novelty formula, normalized displacement formula, Fisher term, BP threshold, or BP EMA policy.

## 4. New observation contract module

New source:

```text
crates/ash_core/src/delta_k_observation_contract.rs
```

Exported from:

```text
crates/ash_core/src/lib.rs
```

The module is intentionally located in `ash_core` because the contract is shared by decode, future training observation, and future post-update evidence while none of those consumers receives another domain's mutable state.

## 5. Observation domains

R0 adds:

```rust
pub enum AshDeltaKObservationDomain {
    Decode,
    BackpropPre,
    UpdatePost,
}
```

with separate logical namespaces:

```text
Decode       -> dk.decode
BackpropPre  -> dk.bp_pre
UpdatePost   -> dk.update_post
```

A raw `f32 delta_k` is not sufficient authority for cross-subsystem decisions. Domain identity travels with the observation.

## 6. Observation identity

Every observation envelope carries:

```text
observation_id
domain
structural_law_revision
source_revision
observer_revision
observation_policy_revision
generation
step
source_snapshot_id
```

The structural law revision is validated against:

```text
ASH_DK_STRUCTURAL_LAW_I_TIMES_M_SQUARED_R1
```

Observer revision and observation-policy revision are deliberately separate from consumer policy revision.

This means a future BP novelty definition can change without pretending that the `I*M^2` structural law changed, and a future fusion threshold can change without pretending that the observer formula changed.

## 7. Observation value and formula receipt

The common value envelope contains:

```text
information_term
material_term
delta_k_raw
delta_k_smoothed optional
confidence optional
```

Validation is fail-closed for:

```text
non-finite I
non-finite M
non-finite raw Delta-K
negative I
negative M
negative raw Delta-K
non-finite smoothed Delta-K
out-of-range confidence
I*M^2 formula mismatch
```

R0 does not silently apply:

```text
NaN -> 0
negative -> abs
negative -> clamp
```

The existing decode observer's own pre-existing clamping semantics are not retroactively rewritten by this cross-domain contract.

## 8. Read-only decode snapshot adapter

R0 adds:

```rust
decode_snapshot_to_observation(...)
```

The adapter accepts an already-produced existing `DeltaKSnapshot` and copies:

```text
snapshot.i              -> information_term
snapshot.m              -> material_term
snapshot.delta_k        -> delta_k_raw
snapshot.delta_k_smooth -> delta_k_smoothed
snapshot.mode           -> decode_mode
```

It does not:

```text
call DeltaKComputer::update
recompute decode Delta-K
change decode smoothing
interpret compact/mix/reverb as optimizer policy
reuse theta_low/theta_high as BP thresholds
reuse decode mutable EMA state for BP
```

The adapter exists only to place existing decode evidence into the new lineage/authority envelope.

## 9. Domain-specific typed observations

R0 defines separate typed shells:

```text
AshDecodeDeltaKObservation
AshBpPreDeltaKObservation
AshUpdatePostDeltaKObservation
```

`AshBpPreDeltaKObservation` includes training-specific lineage fields:

```text
tensorcube_id
parameter_region_id
parameter_revision
optimizer_generation
bp_generation
```

`AshUpdatePostDeltaKObservation` is a different Rust type and includes:

```text
tensorcube_id
parameter_region_id
parameter_revision
optimizer_generation
completed_bp_generation
```

R0 does not provide a BP calculator that creates these values yet. The types establish the legal destination for later `LOCAL-TENSORCUBE-BP-DK-OBSERVATION-01` work.

## 10. Consumer authority matrix

R0 introduces explicit consumers:

```text
DecodePhaseHint
DecodeSemanticPrior
DecodeAdapterRouting
BpFusionObservation
PostUpdateEvaluation
```

The admitted matrix is intentionally narrow:

| Observation domain | Decode phase | Decode semantic prior | Decode adapter routing | BP fusion observation | Post-update evaluation |
|---|---:|---:|---:|---:|---:|
| Decode | yes | yes | yes | no | no |
| BackpropPre | no | no | no | yes | no |
| UpdatePost | no | no | no | no | yes |

Every other domain-consumer pair is rejected as cross-domain or circular authority.

In particular:

```text
UpdatePost(t) -> current-step BP fusion admission(t)
```

is structurally rejected.

## 11. Decode consumer authority remains decode-only

The existing decode mode and phase/semantic consumers remain decoding concerns.

Forbidden shortcuts include:

```text
compact -> AdamW
mix     -> Local HiMuon
reverb  -> Fused HiMuon

theta_high -> BP fusion threshold
semantic_prior.deltak_scores[token] -> TensorCube BP fusion score
```

No such bindings are introduced by R0.

## 12. No shared mutable Delta-K state

R0 does not create a global mutable Delta-K state shared by:

```text
Decode
BackpropPre
UpdatePost
```

The existing `DeltaKComputer.prev_ratio` and `DeltaKComputer.last` remain owned by the existing decode observer.

Future BP smoothing must own a separate BP observation policy/state revision.

Future POST smoothing/effectiveness state must likewise be independent.

## 13. Explicit non-authority seals

R0 exports explicit foundation seals:

```text
ASH_DK_NO_DIRECT_PARAMETER_MUTATION = true
ASH_DK_NO_OPTIMIZER_STEP_AUTHORITY = true
ASH_DK_NO_PRECISION_COMMIT_AUTHORITY = true
ASH_DK_NO_RESIDENCY_COMMIT_AUTHORITY = true
ASH_DK_NO_PHYSICAL_TENSORCUBE_MUTATION = true
ASH_DK_NO_HIMUON_FUSION_EXECUTION_00 = true
```

The new module contains no WGPU dispatch, optimizer step, parameter write, residency movement, or HiMuon execution API.

## 14. Authority telemetry schema

R0 defines a foundation telemetry object containing:

```text
decode_observation_count
bp_pre_observation_count
update_post_observation_count
cross_domain_reject_count
circular_admission_reject_count
direct_parameter_mutation_count
optimizer_authority_leak_count
precision_authority_leak_count
residency_authority_leak_count
physical_tensorcube_mutation_count
himuon_fusion_execution_count
```

Foundation invariants require the authority-leak and physical-mutation counters to remain zero.

The telemetry is a contract schema in R0. R0 does not yet wire a BP runtime producer.

## 15. Unit-level contract fixtures

The module contains Rust tests for:

```text
decode snapshot adapter preserves existing values
UpdatePost cannot enter current-step BP fusion authority
Decode observation cannot become BP fusion authority
I*M^2 mismatch is rejected
```

Cargo/rustc is not available in the bake environment, so these tests are authored but not claimed as physically compiled/executed here.

## 16. Static validator

New validator:

```text
tools/validate_ash_bp_dk_observation_contract_authority_separation_00_static.py
149/149 PASS
```

It verifies:

```text
four decode parent SHA values remain exact
existing decode I*M^2 math remains
existing decode smoothing/modes remain
phase projection remains
semantic prior deltak_scores remains
QW-MCTS existing source reuse remains and new decode Delta-K math remains false
contract module/export exists
three observation domains and namespaces exist
identity/revision separation exists
formula reproduction/fail-closed validation exists
no BP gradient formula is implemented in R0
decode adapter copies snapshot values and does not call DeltaKComputer::update
no decode threshold/EMA reuse enters the new module
BP_PRE and UPDATE_POST are distinct typed observations
consumer authority matrix contains only admitted domain pairs
UpdatePost/Decode cannot enter BP fusion authority
no direct optimizer/parameter/precision/residency/WGPU execution API exists
foundation tests exist
CF1 validator wiring exists
```

## 17. Retained parent gates

The following existing static gates remain passing after R0:

```text
TensorCube Local Muon optimizer              101/101 PASS
FirstCandidate registry                       97/97 PASS
Muon production callsite                      63/63 PASS
Muon registry recursion repair                38/38 PASS
Muon exact-subgroup32 norm                   128/128 PASS
Generation-sealed immutable Muon cache        66/66 PASS
Muon immutable-cache backend rebind           35/35 PASS
```

This provides evidence that the observation-foundation patch did not alter those existing training/runtime contracts.

## 18. CF1 integration

The new validator is added to:

```text
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

as:

```text
validate_ash_bp_dk_observation_contract_authority_separation_00_static.py
```

The existing Cargo/check/test/build commands in CF1 are not changed.

## 19. Changed files

Overlay contains exactly four files:

```text
crates/ash_core/src/delta_k_observation_contract.rs
crates/ash_core/src/lib.rs
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_observation_contract_authority_separation_00_static.py
```

No existing decode Delta-K implementation file appears in the overlay.

## 20. Evidence boundary

The bake environment does not provide Cargo/rustc.

Therefore:

```text
STATIC_BAKED_READY
DECODE_PARENT_BYTES_PRESERVED
AUTHORITY_CONTRACT_STATIC_PASS
NO_LOCAL_RUST_COMPILE_CLAIM
NO_LOCAL_UNIT_TEST_EXECUTION_CLAIM
NO_BP_DELTA_K_RUNTIME_CLAIM
NO_HIMUON_FUSION_CLAIM
```

User-local Rust/Cargo execution remains the physical compile/test SSOT.

## 21. Physical verification targets

Local verification should establish at least:

```text
cargo check ash_core PASS
ash_core unit tests PASS
existing decode DeltaK tests/regressions PASS
same existing decode input/state -> unchanged DeltaK snapshot behavior
read-only adapter -> identical i/m/raw/smooth/mode values
UpdatePost -> BP fusion authority rejected
Decode -> BP fusion authority rejected
formula mismatch/nonfinite input rejected
CF1 chain reaches the new static gate
```

## 22. Non-goals

```text
No BP gradient novelty implementation
No BP normalized displacement implementation
No Fisher term
No BP smoothing state
No BP threshold
No Bridge Delta-K
No fusion candidate graph
No HiMuon fusion planner execution
No fused Muon workspace
No optimizer topology mutation
No precision switching
No VRAM/RAM/HDD movement
No Decode DeltaKComputer rewrite
No phase projection rewrite
No semantic prior rewrite
No QW-MCTS value/runtime authority escalation
```

## 23. Natural next patch

The next patch may now implement the first real training-domain observer without contaminating decode state:

```text
ASH-BP-DK-LOCAL-TENSORCUBE-BP-DK-OBSERVATION-01
```

Its responsibility is to bind BP-specific observation inputs into:

```text
I_BP
M_BP
DeltaK_BP_PRE = I_BP * M_BP^2
```

and emit an `AshBpPreDeltaKObservation` with exact TensorCube / parameter / optimizer / BP generation lineage.

It must not call the decode `DeltaKComputer::update()` as a training calculator.

## Promotion seal

```text
PROMOTE_ASH_BP_DK_OBSERVATION_CONTRACT_AND_AUTHORITY_SEPARATION_00

EXISTING_DECODE_DELTA_K_AUTHORITY_PRESERVED
DECODE_DELTA_K_PARENT_BYTES_PRESERVED
ASH_CORE_DELTA_K_COMPUTER_PRESERVED
I_TIMES_M_SQUARED_STRUCTURAL_LAW_PRESERVED
DECODE_OBSERVER_SEMANTICS_PRESERVED
DECODE_SMOOTHING_PRESERVED
DECODE_COMPACT_MIX_REVERB_PRESERVED
DELTA_K_PHASE_PROJECTION_PRESERVED
DECODE_SEMANTIC_PRIOR_DELTAK_SCORES_PRESERVED
QW_MCTS_EXISTING_DELTAK_REUSE_SEAL_PRESERVED
NO_NEW_DECODE_DELTA_K_MATH
DECODE_OBSERVATION_DOMAIN
BACKPROP_PRE_OBSERVATION_DOMAIN
UPDATE_POST_OBSERVATION_DOMAIN
DOMAIN_NAMESPACE_SEPARATION
STRUCTURAL_LAW_REVISION_REQUIRED
SOURCE_REVISION_REQUIRED
OBSERVER_REVISION_REQUIRED
OBSERVATION_POLICY_REVISION_REQUIRED
CONSUMER_POLICY_REVISION_SEPARATED
DETERMINISTIC_OBSERVATION_IDENTITY_ENVELOPE
DECODE_SNAPSHOT_READ_ONLY_ADAPTER
DECODE_I_M_RAW_SMOOTH_MODE_PRESERVED
NO_DECODE_UPDATE_RECOMPUTE
NO_CROSS_DOMAIN_MUTABLE_STATE
NO_CROSS_DOMAIN_EMA_REUSE
NO_CROSS_DOMAIN_THRESHOLD_REUSE
NO_DECODE_MODE_OPTIMIZER_LEAK
BP_PRE_AND_UPDATE_POST_TYPED_SEPARATION
UPDATE_POST_CURRENT_STEP_FUSION_AUTHORITY_REJECTED
DECODE_BP_FUSION_AUTHORITY_REJECTED
DELTA_K_SIGNAL_AUTHORITY_ONLY
ZERO_DIRECT_PARAMETER_MUTATION_AUTHORITY
ZERO_OPTIMIZER_STEP_AUTHORITY
ZERO_PRECISION_COMMIT_AUTHORITY
ZERO_RESIDENCY_COMMIT_AUTHORITY
ZERO_PHYSICAL_TENSORCUBE_MUTATION_AUTHORITY
ZERO_HIMUON_FUSION_EXECUTION_00
NO_BP_FORMULA_IMPLEMENTATION_YET
CF1_STATIC_GATE_WIRED
NO_LOCAL_COMPILE_CLAIM
SEALED
```