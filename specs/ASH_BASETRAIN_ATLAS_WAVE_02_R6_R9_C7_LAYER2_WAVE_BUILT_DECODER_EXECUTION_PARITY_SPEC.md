# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C7

## Layer-2 Wave-Built Decoder Execution Parity / Adopted Wave Block Execution Lease / Exact Input Hidden-2 Binding / Actual Input RMSNorm·QKV·Headwise·OProj·MLP Route / Legacy-Loader Reference Non-Authority Oracle / Hidden-3 Full-Surface Parity / Dispatch Evidence Parity / Zero Mismatch·Nonfinite / No Weight Reload·No Rebuild / No Payload Readback Seal

> Admission parent SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C6` physical PASS  
> Compile closure parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C6-D1`  
> Runtime source at C7 entry: resident wave-built weight Layer 2 / generation 2, hidden Layer 2 / generation 2  
> Runtime target on C7 PASS: resident weight Layer 2 / generation 2 unchanged, hidden Layer 3 / generation 3  
> Candidate weight source: C6-adopted C4/C5 wave-built Layer-2 block  
> Reference weight source: one private legacy full-layer loader build used only as a non-authoritative oracle  
> Candidate runtime weight reload/rebuild: `0 / 0`  
> Reference runtime publication: `0`  
> Tensor payload readback: `0`  
> Proof ledger: `HOLD` until physical C7 PASS

---

# 0. Purpose

C6 physically proved that a Layer-2 decoder block built through the C4/C5 decoder-weight wave path can replace Layer-1 runtime weights and become the single canonical resident runtime weight authority:

```text
Weight Layer1 / Generation1
  -> destructive extraction
  -> VacantForRebind
  -> C5 three-wave / nine-role build
  -> atomic adopt
  -> Weight Layer2 / Generation2
```

C6 deliberately stopped before executing Layer 2.

C7 is the first gate allowed to execute the C6-adopted wave-built Layer-2 block.

C7 must prove all of the following at the same time:

```text
1. the runtime execution lease resolves to the exact C6-adopted Layer-2 block;
2. the exact R6-R8 output Hidden2 is used as the input hidden state;
3. the wave-built block executes the real Input RMSNorm -> QKV -> Headwise -> OProj -> MLP route;
4. a separately built legacy-loader Layer-2 block is used only as a private non-authority oracle;
5. candidate and oracle begin from the same Hidden2 state and the same checkpoint tensor identities;
6. candidate and oracle produce exact full-surface Hidden3 parity with zero mismatch and zero nonfinite values;
7. candidate and oracle dispatch evidence agree semantically;
8. the candidate path does not reload weights or rebuild the adopted block;
9. no full tensor payload is read back to the CPU;
10. Hidden3 is published only after all parity gates pass.
```

The central C7 safety rule is:

> A wave-built Hidden3 may not become hidden SSOT until its non-publishing output has passed exact full-surface parity against a legacy-loader non-authority oracle.

---

# 1. Parent physical evidence

C7 admission requires physical C6 PASS, including at minimum:

```text
source_layer                       = 1
target_layer                       = 2
source_generation                  = 1
target_generation                  = 2
source_completion_bound            = 1
destructive_source_eviction        = 1
vacant_boundary                    = 1
staging_after_vacancy              = 1
plan_waves                         = 3
lanes                              = 9
roles                              = 9
checkpoint_reads                   = 9
decodes                            = 9
material_commits                   = 9
complete_nine_role_seal            = 1
runtime_adopt                      = 1
runtime_resident_blocks            = 1
runtime_resident_weight_tensors    = 9
runtime_authority_overlap          = 0
legacy_full_layer_loader           = 0
legacy_fallback                    = 0
source_rebuild                     = 0
hidden_layer                       = 2
hidden_generation                  = 2
hidden_pointer_unchanged           = 1
target_forward                     = 0
recovery_required_transition       = 0
gpu_weight_readback                = 0
```

C7 must consume the C6 session directly. It must not rerun the historical C1 generalized full-layer rebind path to obtain Layer 2.

---

# 2. Entry-state SSOT

At C7 entry the canonical runtime state is exactly:

```text
weight slot state                  = Resident
resident weight layer              = 2
weight residency generation        = 2
resident decoder block count       = 1
resident checkpoint tensor count   = 9
active weight execution leases     = 0
slot-owned strong references       = 1

hidden layer                       = 2
hidden generation                  = 2
active hidden execution leases     = 0
```

The weight pointer must be the exact C6 `adopted_weight_pointer`.

The hidden pointer must be the exact Hidden2 pointer preserved unchanged across C6.

Any drift is a C7 precondition failure.

---

# 3. C7 execution order

C7 uses the following strict order:

```text
A. run admitted C6 session
B. snapshot C6-adopted weight pointer and Hidden2 pointer
C. build private legacy-loader Layer2 reference oracle
D. prove oracle checkpoint/tensor/block provenance matches the C6-adopted target
E. execute oracle from exact Hidden2 through a non-publishing canonical block core
F. prove oracle did not mutate runtime weight or hidden SSOT
G. acquire adopted wave-built runtime weight lease + exact Hidden2 lease
H. execute candidate from exact Hidden2 through the same non-publishing canonical block core
I. release candidate execution leases after same-device completion
J. compare candidate vs oracle Hidden3 full surface exactly on GPU
K. compare normalized dispatch evidence semantically
L. require mismatch=0 and nonfinite=0
M. commit candidate Hidden3 once to LayerHiddenAuthoritySlot
N. compare committed Hidden3 vs candidate pre-publication output exactly
O. prove weight pointer remained C6-adopted Layer2 / generation2
P. drop oracle/private comparison resources
Q. emit C7 final receipt and PASS token
```

Hidden3 publication before steps J-K-L is forbidden.

---

# 4. Why execution and publication must be split

The existing R6-R8 helper `execute_resident_decoder_layer_from_session()` performs execution and Hidden publication in one wrapper.

That behavior is correct for already-admitted layer execution, but C7 is a parity gate for a newly wave-built runtime block.

If C7 were to:

```text
execute candidate
-> commit Hidden3
-> then compare against legacy oracle
```

and the comparison failed, hidden SSOT would already have advanced.

Therefore C7 requires a non-publishing execution core extracted from the already-proven R6-R8 route.

The extraction must not change the numerical route.

---

# 5. Non-publishing canonical block execution core

Introduce or extract one reusable Rust execution primitive equivalent to:

```rust
pub struct R6R8NonPublishingBlockExecution {
    pub final_hidden: Tensor<InferenceBackend, 3>,
    pub final_hidden_raw_lease: RawWgpuBufferLease,
    pub evidence: R6R8NonPublishingBlockExecutionEvidence,
}

pub fn execute_decoder_block_nonpublishing_canonical_route(
    runtime: &R6R6LiveBodyRuntime,
    block_bundle: &R6R6ActualDecoderBlockBundle,
    input_hidden: Tensor<InferenceBackend, 3>,
    selected_layer: u32,
    values: &BTreeMap<String, String>,
    route_kind: R6R8NonPublishingRouteKind,
) -> Result<R6R8NonPublishingBlockExecution>;
```

Exact names may differ.

The helper owns only numerical execution and typed execution evidence.

It must not:

```text
acquire runtime weight authority
mutate BaseTrainLayerWeightResidencySlot
commit LayerHiddenAuthoritySlot
change weight generation
change hidden generation
write runtime pointer state
load checkpoint weights
build a decoder block
```

The existing R6-R8 wrapper may be refactored to call this core and then perform its existing hidden commit/publication logic.

---

# 6. Numerical route preservation

The non-publishing core must preserve the already physically admitted R6-R8 numerical route.

Required route:

```text
Input Hidden BQH
  -> block.input_norm.forward
  -> Q projection
  -> K projection
  -> V projection
  -> reshape Q/K/V to BQHD
  -> Burn-to-raw same-device bridge
  -> NeoX RoPE
  -> Headwise prepared QKV
  -> selected shared Headwise runtime
     W5 / Stage10
     W6 / Stage11
     W7 / Stage12
  -> same-device context adoption
  -> OProj
  -> attention residual add
  -> post-attention RMSNorm
  -> Gate projection
  -> SiLU
  -> Up projection
  -> elementwise multiply
  -> Down projection
  -> FFN residual add
  -> final Hidden BQH
```

No simplified CPU reference path is admitted as the C7 candidate.

No dense-attention fallback may replace the selected Headwise path.

---

# 7. Intra-block reference vs legacy-loader oracle

R6-R8 already has an internal `reference` path for Headwise/context validation.

That existing path is not the C7 legacy-loader oracle.

C7 must use explicit terminology:

```text
intraBlockHeadwiseReference
  = existing same-block Headwise reference/context route

legacyLoaderBlockOracle
  = separate decoder block constructed from the historical full-layer loader
```

A PASS from `intraBlockHeadwiseReference` may not be borrowed as proof that the wave-built block matches a legacy-built block.

Required:

```text
crossReferencePassBorrowCount = 0
ambiguousReferenceAuthorityCount = 0
```

---

# 8. Candidate runtime execution lease

Candidate execution must use the canonical runtime weight slot lease API.

Required binding:

```text
selected layer                 = 2
expected weight generation     = 2
expected pointer digest        = C6 adopted pointer digest
```

C7 acquires:

```text
BaseTrainLayerWeightResidencySlot::acquire_execution_lease(
    2,
    2,
    adopted_pointer_digest,
)
```

The lease must prove:

```text
captured layer                 = 2
captured generation            = 2
captured pointer digest        = C6 adopted pointer digest
captured transition serial     = C6 adopted transition serial
captured block identity        = C6 target block identity digest
```

Candidate code must use `weight_lease.bundle()`.

Direct access to a stale C5 private candidate is forbidden.

---

# 9. Exact Hidden2 input binding

C7 candidate and oracle must both execute from the exact Hidden2 state produced by R6-R8 and preserved by C6.

Required Hidden2 identity fields:

```text
layer index                    = 2
hidden generation              = 2
pointer digest                 = C6 hidden pointer digest
buffer identity digest         = C6 hidden buffer identity digest
completion token digest        = C6 hidden completion token digest
semantic shape BQH             = C6 hidden semantic shape BQH
transition serial              = C6 hidden transition serial
```

No re-embedding, source-token replay, synthetic hidden reconstruction, CPU clone/reupload, or hidden normalization prepass outside the block is allowed.

---

# 10. Oracle execution gets Hidden2 before publication

The private legacy oracle executes before candidate Hidden3 publication.

The oracle acquires only a Hidden2 execution lease or equivalent exact Hidden2 tensor borrow.

It must not acquire a runtime weight lease because it is not runtime weight authority.

After oracle execution:

```text
hidden slot pointer == original Hidden2 pointer
hidden generation == 2
hidden transition serial unchanged
runtime weight pointer == C6 adopted pointer
```

The oracle output remains private and non-published.

---

# 11. Legacy-loader reference non-authority oracle construction

The C7 reference oracle must use the historical full-layer build route exactly once:

```text
load_base_train_atlas_wave_02_r6_r7_decoder_block_weights(
    checkpoint,
    2,
)

-> build_r6_r7_actual_decoder_block_for_layer(
    burn_device,
    authority.values,
)
```

This path is allowed only inside the explicitly named C7 reference oracle constructor.

It is forbidden on the candidate runtime path.

The oracle is not inserted into `BaseTrainLayerWeightResidencySlot`.

Required counts:

```text
legacyOracleBuildCount                 = 1
legacyOracleCheckpointPayloadReadCount = 9
legacyOracleRuntimeAdoptCount          = 0
legacyOracleRuntimeWeightAuthorityCount= 0
legacyOracleExecutionLeaseCount        = 0 for weight authority
```

---

# 12. No Weight Reload·No Rebuild seal semantics

The title `No Weight Reload·No Rebuild` applies to the adopted wave-built candidate execution path.

Required candidate counters:

```text
candidateCheckpointWeightReadCount = 0
candidateWeightReloadCount         = 0
candidateBlockRebuildCount         = 0
candidateC4PlanRebuildCount        = 0
candidateC5StagingExecutionCount   = 0
candidateRuntimeRebindCount        = 0
```

The one private legacy oracle build is not a candidate reload or rebuild.

It must be reported separately as oracle-only diagnostic work.

C7 must not hide the oracle's nine checkpoint reads inside a global `weight_reload=0` claim.

---

# 13. Oracle provenance equality

Before oracle execution, C7 must prove its weights represent the same Layer-2 checkpoint tensor set as the C6-adopted wave-built runtime block.

Required exact comparisons:

```text
oracle selected layer
  == 2

oracle checkpoint set digest
  == runtime checkpoint set digest

oracle tensor-set authority digest
  == C6 target tensor-set authority digest
  == adopted pointer layer_tensor_set_digest

oracle tensor identity digests
  == adopted pointer layer_tensor_identity_digests

oracle block module identity digest
  == adopted pointer actual_decoder_block_identity_digest
```

The reference block is numerically meaningful only after these provenance equalities pass.

---

# 14. Oracle is resource, not authority

During oracle lifetime the system may physically hold:

```text
1 canonical runtime Layer2 block
1 private legacy reference Layer2 block
```

This is resource overlap, not runtime authority overlap.

Required authority counts remain:

```text
runtime resident decoder blocks       = 1
runtime resident checkpoint tensors   = 9
runtime weight authorities            = 1
runtime authority overlap             = 0
```

C7 must not claim that total GPU weight resources equal one while the oracle exists.

It only claims that runtime SSOT authority remains singular.

---

# 15. Oracle route parity

The oracle must execute the same non-publishing canonical block route as the candidate.

It may not use:

```text
CPU matmul
CPU attention
simplified dense attention
model_core-only partial FFN test
R6-R8 final receipt replay without computation
precomputed Hidden3 fixture
```

Both candidate and oracle must pass through the selected same-device Headwise path.

---

# 16. Shared execution-input contract

Candidate and oracle execution core calls must bind one immutable `R6R9C7InputHiddenBinding` equivalent to:

```rust
pub struct R6R9C7InputHiddenBinding {
    pub layer_index: u32,
    pub hidden_generation: u64,
    pub pointer_digest: String,
    pub buffer_identity_digest: String,
    pub completion_token_digest: String,
    pub semantic_shape_bqh: [u32; 3],
    pub transition_serial: u64,
    pub binding_digest: String,
}
```

Both execution evidences must reference the same binding digest.

No route-specific hidden digest is allowed to silently replace it.

---

# 17. Candidate non-publishing evidence

Introduce typed candidate execution evidence equivalent to:

```rust
pub struct R6R9C7CandidateExecutionEvidence {
    pub schema_version: u32,
    pub selected_layer: u32,
    pub adopted_weight_pointer_digest: String,
    pub adopted_weight_generation: u64,
    pub adopted_weight_transition_serial: u64,
    pub adopted_block_identity_digest: String,
    pub input_hidden_binding_digest: String,
    pub qkv: R6R8QkvDispatchEvidence,
    pub shared_attention: R6R5SharedRuntimeDispatchEvidence,
    pub replay_attention: R6R5SharedRuntimeDispatchEvidence,
    pub continuation: R6R8ContinuationDispatchEvidence,
    pub intra_block_parity: R6R8FinalParityEvidence,
    pub final_hidden_shape_bqh: [u32; 3],
    pub final_hidden_buffer_identity_digest: String,
    pub payload_readback_count: u64,
    pub weight_reload_count: u32,
    pub block_rebuild_count: u32,
    pub runtime_rebind_count: u32,
    pub hidden_commit_count: u32,
    pub pass: bool,
    pub evidence_digest: String,
}
```

Before cross-block parity:

```text
hidden_commit_count = 0
```

---

# 18. Oracle non-publishing evidence

Introduce typed oracle evidence equivalent to:

```rust
pub struct R6R9C7LegacyOracleExecutionEvidence {
    pub schema_version: u32,
    pub selected_layer: u32,
    pub checkpoint_set_digest: String,
    pub tensor_set_authority_digest: String,
    pub tensor_identity_digests: Vec<String>,
    pub block_identity_digest: String,
    pub input_hidden_binding_digest: String,
    pub qkv: R6R8QkvDispatchEvidence,
    pub shared_attention: R6R5SharedRuntimeDispatchEvidence,
    pub replay_attention: R6R5SharedRuntimeDispatchEvidence,
    pub continuation: R6R8ContinuationDispatchEvidence,
    pub intra_block_parity: R6R8FinalParityEvidence,
    pub final_hidden_shape_bqh: [u32; 3],
    pub final_hidden_buffer_identity_digest: String,
    pub checkpoint_payload_read_count: u32,
    pub runtime_publish_count: u32,
    pub runtime_weight_authority_count: u32,
    pub payload_readback_count: u64,
    pub pass: bool,
    pub evidence_digest: String,
}
```

Required:

```text
runtime_publish_count = 0
runtime_weight_authority_count = 0
```

---

# 19. Dispatch evidence semantic projection

Candidate and oracle evidence digests cannot simply be compared as raw equality because route labels, operation IDs, nonces, buffer identities, and receipt digests may legitimately differ.

C7 therefore defines a normalized dispatch semantic projection.

Equivalent shape:

```rust
pub struct R6R9C7DispatchSemanticProjection {
    pub selected_layer: u32,
    pub input_shape_bqh: [u32; 3],
    pub q_shape_bqhd: [u32; 4],
    pub k_shape_bqhd: [u32; 4],
    pub v_shape_bqhd: [u32; 4],
    pub input_norm_dispatch_count: u32,
    pub q_projection_count: u32,
    pub k_projection_count: u32,
    pub v_projection_count: u32,
    pub shared_attention_semantics: R6R9C7AttentionDispatchSemanticProjection,
    pub continuation_semantics: R6R9C7ContinuationSemanticProjection,
    pub final_hidden_shape_bqh: [u32; 3],
    pub host_upload_count: u64,
    pub tensor_payload_readback_count: u64,
    pub projection_digest: String,
}
```

The projection excludes route labels and diagnostic nonces.

---

# 20. Dispatch parity requirements

C7 requires exact equality of candidate and oracle normalized semantic projections.

At minimum compare:

```text
input BQH shape
Q BQHD shape
K BQHD shape
V BQHD shape
input RMSNorm count
Q projection count
K projection count
V projection count
selected shared Headwise stage evidence
Stage10/W5 semantic counts
Stage11/W6 semantic counts
Stage12/W7 semantic counts
selected context geometry
OProj count
attention residual add count
post-attention norm count
gate projection count
up projection count
SiLU multiply count
down projection count
FFN residual add count
final hidden BQH shape
payload readback count
host upload count
```

The comparison must use actual typed dispatch evidence.

Do not restore old flat hardcoded stage counts as coordinator truth.

---

# 21. Stage evidence truth

C2 retired synthetic/flat coordinator dispatch arithmetic.

C7 must preserve that retirement.

For Stage10/11/12, compare the actual typed shared runtime evidence fields produced by candidate and oracle.

Do not require historical terminal summaries such as:

```text
stage10=2
stage11=1
stage12=4
```

as the C7 dispatch SSOT.

The actual evidence projection is the authority.

---

# 22. Candidate lease lifecycle

Candidate execution requires:

```text
weight execution lease acquire count = 1
hidden execution lease acquire count = 1
```

Before use:

```text
weight lease validate = PASS
hidden lease validate = PASS
weight captured layer == hidden captured layer == 2
weight captured generation == hidden captured generation == 2
```

After non-publishing execution:

```text
device.poll(Wait)
weight lease release count = 1
hidden lease release count = 1
active weight leases = 0
active hidden leases = 0
```

No hidden commit may occur while either lease remains active.

---

# 23. Candidate block identity binding

The candidate weight lease must prove:

```text
captured block identity digest
  == C6 adopted pointer actual_decoder_block_identity_digest
  == C6 transaction target_block_identity_digest
  == C7 legacy oracle block identity digest
```

If these differ, C7 must fail before output parity is used as evidence.

---

# 24. Candidate no-reload static route

C7 candidate code must have zero call edges to:

```text
load_base_train_atlas_wave_02_r6_r7_decoder_block_weights
load_base_train_atlas_wave_02_r6_r6_decoder_block
plan_decoder_weight_atlas_waves
execute_layer_weight_build_staging_private_candidate
build_r6_r7_actual_decoder_block_for_layer
BaseTrainLayerWeightResidencySlot::adopt
rebind_resident_decoder_layer
```

Those functions may appear in the oracle or C6 parent path, but not inside the candidate execution function.

---

# 25. Cross-block Hidden3 comparison

After oracle and candidate non-publishing executions both succeed, C7 bridges their final hidden tensors to raw same-device leases.

Required bridge behavior:

```text
host upload count = 0
full tensor CPU readback = 0
```

C7 uses:

```text
HeadwiseOutputParityPipeline::compare_exact(
    legacy_oracle_hidden3,
    wave_candidate_hidden3,
)
```

Mixed envelope is not the C7 cross-block admission criterion.

Exact parity is required because both blocks bind the same checkpoint tensors and execute the same route from the same Hidden2 state.

---

# 26. Full-surface compared count

The compared scalar count must be derived from runtime Hidden3 semantic shape:

```text
B * Q * H
```

using checked arithmetic.

No fixed `65536` literal may become C7 authority.

The current fixture may physically produce `65536`, but the receipt must derive it from the actual BQH shape.

Required:

```text
runtime_geometry_compared_scalar_count
  == parity.compared_element_count
  == parity.expected_element_count
```

---

# 27. Zero mismatch and nonfinite

Cross-block admission requires:

```text
envelope_violation_count == 0
non_finite_count == 0
first_fault_linear_index == None
pass == true
```

Because `compare_exact` is used:

```text
absolute_tolerance == 0
relative_tolerance == 0
```

Any mismatch is a C7 failure.

No tolerance widening or post-hoc threshold relaxation is allowed.

---

# 28. Internal route finite/parity requirements

Candidate and oracle must each also retain the physically admitted finite/parity checks of the extracted R6-R8 core.

Required for both:

```text
QKV host readback = 0
QKV host upload = 0
Headwise output finite guard = PASS
shared/replay context parity = PASS
final hidden finite guard = PASS
intra-block reference parity = PASS
intra-block replay parity = PASS
internal tensor payload readback = 0
```

These checks are subordinate to, and not a substitute for, the C7 legacy-oracle cross-block parity.

---

# 29. No Payload Readback seal

C7 distinguishes compact diagnostic readback from tensor payload readback.

Allowed:

```text
compact parity counter/result readback
finite-guard compact diagnostic readback
```

Forbidden:

```text
candidate Hidden3 tensor payload CPU readback
oracle Hidden3 tensor payload CPU readback
Q/K/V tensor payload CPU readback
attention context tensor payload CPU readback
weight tensor GPU readback
```

Required final field:

```text
tensorPayloadReadbackCount = 0
```

Checkpoint file reads for constructing the oracle are not GPU payload readback and must be reported separately.

---

# 30. Candidate Hidden3 remains private before parity

Candidate final Hidden3 must remain a private tensor/result owner until cross-block parity and dispatch parity pass.

Before admission:

```text
LayerHiddenAuthoritySlot layer = 2
LayerHiddenAuthoritySlot generation = 2
candidate hidden commit count = 0
```

If candidate execution, oracle execution, provenance parity, dispatch parity, finite checks, or full-surface parity fail:

```text
Hidden2 remains canonical
Hidden3 commit count remains 0
C8 promotion remains blocked
```

---

# 31. C7 failure policy

C7 execution/parity failure occurs after a successful C6 rebind, while a complete Layer2 block is still resident.

C7 must not silently rebuild/rebind another Layer2 block.

Required failure behavior:

```text
no Hidden3 commit
no legacy fallback adoption
no second runtime weight authority
no source Layer1 reconstruction
return explicit C7 failure
terminate canary session
```

C7 does not reuse C6 `RecoveryRequired` because the runtime slot still owns a structurally complete resident bundle and the current `mark_recovery_required()` contract requires no resident bundle.

A future quarantine/demotion state for numerically untrusted resident blocks, if desired, is a separate SSOT change.

---

# 32. Hidden3 commit admission gate

Candidate Hidden3 may be committed only when all of the following are true:

```text
candidate non-publishing execution pass
oracle non-publishing execution pass
candidate/oracle checkpoint provenance exact
candidate/oracle block identity exact
input Hidden2 binding exact
candidate/oracle dispatch semantic projection exact
cross-block full-surface exact parity pass
cross-block mismatch count = 0
cross-block nonfinite count = 0
candidate payload readback = 0
oracle payload readback = 0
candidate weight reload = 0
candidate block rebuild = 0
runtime weight pointer still equals C6 adopted pointer
active candidate weight lease = 0
active candidate hidden lease = 0
```

---

# 33. Hidden3 commit

After the full C7 gate passes, commit exactly the candidate final hidden tensor:

```text
LayerHiddenAuthoritySlot::commit_next_layer(
    expected generation = 2,
    expected pointer = Hidden2 pointer,
    operation id = C7 operation id,
    tensor = candidate final Hidden3,
    source = WaveBuiltLayer2DecoderExecution,
    buffer identity digest = candidate final hidden buffer digest,
    completion token digest = C7 completion token digest,
)
```

Expected output:

```text
hidden layer = 3
hidden generation = 3
previous pointer digest = Hidden2 pointer digest
```

Oracle output must never be committed.

---

# 34. C7 completion token

The Hidden3 completion token digest must bind at least:

```text
C6 adopted weight pointer digest
C6 transaction receipt digest
candidate execution evidence digest
legacy oracle execution evidence digest
input Hidden2 binding digest
dispatch parity receipt digest
full-surface exact parity receipt digest
candidate finite guard digest
oracle finite guard digest
candidate lease release evidence
reference oracle runtime-publication count = 0
candidate weight reload count = 0
candidate block rebuild count = 0
completion observed = true
```

No digest aliasing is allowed.

---

# 35. Publication parity

After Hidden3 commit, acquire the published Hidden3 tensor and compare it exactly against the pre-publication candidate final hidden.

Required:

```text
publication compared scalar count = runtime BQH scalar count
publication mismatch = 0
publication nonfinite = 0
publication tensor payload readback = 0
publication pass = true
```

This proves hidden publication did not change the candidate output.

---

# 36. Weight immutability through C7

The runtime weight pointer must remain unchanged for the entire C7 execution.

Before oracle, before candidate, after candidate, after Hidden3 commit:

```text
state                     = Resident
resident layer            = 2
residency generation      = 2
pointer digest            = C6 adopted pointer digest
layer tensor-set digest   = C6 target tensor-set digest
actual block identity     = C6 target block identity digest
resident block count      = 1
resident tensor count     = 9
```

C7 does not bump weight generation.

---

# 37. Oracle cannot mutate weight SSOT

Before and after private oracle construction/execution require exact runtime weight snapshot equality.

The legacy oracle code must have zero call edges to:

```text
weight_slot.adopt
weight_slot.arm_eviction
weight_slot.begin_exclusive_destructive_rebind
weight_slot.mark_vacant
weight_slot.mark_recovery_required
```

Its lifetime ends with private drop only.

---

# 38. Candidate cannot use oracle authority

Candidate runtime lease resolution must happen against the C6 adopted pointer, not against oracle block identity alone.

Even if:

```text
candidate block identity == oracle block identity
```

C7 must still prove:

```text
candidate weight lease pointer == C6 adopted runtime pointer
```

The oracle never becomes a substitute runtime SSOT.

---

# 39. No parallel runtime weight authority

Required throughout:

```text
runtimeWeightAuthorityCount = 1
runtimeAuthorityOverlapCount = 0
```

Private oracle resources may coexist transiently, but:

```text
oracleRuntimeAuthorityCount = 0
oracleRuntimePublishCount = 0
```

Authority and allocation are distinct concepts.

---

# 40. Reference oracle lifetime

Recommended lifetime:

```text
build oracle
-> validate provenance
-> execute oracle non-publishing from Hidden2
-> preserve oracle Hidden3 comparison tensor
-> drop oracle block and decoded authority values
-> candidate execution
-> cross-block compare using preserved oracle Hidden3
-> drop oracle Hidden3 after comparison
```

No persistent legacy reference block cache is allowed.

No next-layer prefetch is allowed.

---

# 41. Oracle host ownership

The legacy oracle intentionally uses the old full-layer loader and may temporarily retain all nine decoded `Vec<f32>` values according to that historical implementation.

C7 must not present that oracle diagnostic memory shape as the candidate production path.

Required reporting separation:

```text
candidateWavePathHostDecodeCount = 0 during execution
oracleLegacyLoaderCheckpointReadCount = 9
oracleLegacyLoaderBuildCount = 1
```

C7 makes no memory-performance admission from the oracle path.

---

# 42. Candidate execution dispatch counts

The candidate must prove actual execution of the full block.

At minimum typed evidence must show:

```text
input_norm_dispatch_count = 1
q_projection_count = 1
k_projection_count = 1
v_projection_count = 1
oproj_dispatch_count = 1
attention_residual_add_count = 1
post_attn_norm_dispatch_count = 1
gate_proj_dispatch_count = 1
up_proj_dispatch_count = 1
silu_multiply_dispatch_count = 1
down_proj_dispatch_count = 1
ffn_residual_add_count = 1
```

Headwise Stage10/11/12 evidence must be actual typed child evidence, not fabricated constants.

---

# 43. Oracle dispatch counts

The oracle must satisfy the same semantic dispatch projection.

C7 does not require raw receipt digests to equal candidate receipts.

It requires normalized semantic equality.

This distinction prevents route labels, operation IDs, output handles, and diagnostic nonces from creating false parity failures.

---

# 44. Dispatch parity receipt

Introduce a typed receipt equivalent to:

```rust
pub struct R6R9C7DispatchParityEvidence {
    pub candidate_projection_digest: String,
    pub oracle_projection_digest: String,
    pub input_shape_match: bool,
    pub qkv_shape_match: bool,
    pub input_norm_count_match: bool,
    pub qkv_count_match: bool,
    pub shared_attention_match: bool,
    pub continuation_count_match: bool,
    pub final_hidden_shape_match: bool,
    pub host_upload_match: bool,
    pub payload_readback_match: bool,
    pub mismatch_field_count: u32,
    pub pass: bool,
    pub evidence_digest: String,
}
```

Required:

```text
mismatch_field_count = 0
pass = true
```

---

# 45. Full-surface parity evidence

Introduce a typed receipt equivalent to:

```rust
pub struct R6R9C7Hidden3FullSurfaceParityEvidence {
    pub semantic_shape_bqh: [u32; 3],
    pub runtime_geometry_compared_scalar_count: u64,
    pub observed_compared_scalar_count: u64,
    pub mismatch_count: u64,
    pub non_finite_count: u64,
    pub max_absolute_error_bits: u32,
    pub max_relative_error_bits: u32,
    pub first_fault_linear_index: Option<u32>,
    pub tensor_payload_readback_count: u64,
    pub parity_receipt_digest: String,
    pub pass: bool,
    pub evidence_digest: String,
}
```

For exact PASS:

```text
mismatch_count = 0
non_finite_count = 0
max_absolute_error = 0
max_relative_error = 0
first_fault_linear_index = None
tensor_payload_readback_count = 0
```

---

# 46. Candidate vs oracle output authority

Before Hidden3 commit:

```text
candidate Hidden3
  = candidate output under test

legacy oracle Hidden3
  = comparison oracle only
```

After parity PASS and publication:

```text
published Hidden3
  = candidate Hidden3 only
```

The oracle output never becomes runtime hidden authority.

---

# 47. Operation identities

C7 operation IDs must be deterministic and derived from stable parent identities.

Recommended inputs:

```text
C7 patch/build revision
C6 adopted pointer digest
Hidden2 pointer digest
checkpoint set digest
target layer 2
```

Separate operation IDs:

```text
c7 oracle operation id
c7 candidate operation id
c7 hidden commit operation id
```

No timestamp, random UUID, process pointer, thread scheduling order, or filesystem mtime may enter canonical digest identity.

---

# 48. Same-device lineage

Candidate and oracle execution must use the same canonical runtime device lineage:

```text
same process
same wgpu Device
same Queue
same Burn WgpuDevice
```

The legacy oracle may construct private tensors on the existing Burn device only.

Creating a second WGPU device for reference isolation is forbidden.

---

# 49. No re-embedding

C7 begins at Hidden2.

Required:

```text
token embedding execution count = 0
embedding row micro-atlas wave count = 0 within C7 execution body
source token reparse count = 0
```

Parent R6-R6/R6-R8 embedding evidence remains historical lineage only.

---

# 50. No decoder-weight wave rebuild

C7 must not rerun C4/C5 for the candidate.

Required candidate counts:

```text
decoderWeightWavePlanCount = 0
decoderWeightStagingSlotCreateCount = 0
decoderWeightWaveDecodeCount = 0
decoderWeightMaterialCommitCount = 0
```

C7 consumes the already adopted C6 runtime block.

---

# 51. No runtime weight rebind

C7 must not call any weight transition method.

Required:

```text
weightEvictionCount = 0
weightVacantTransitionCount = 0
weightAdoptCount = 0
weightRecoveryTransitionCount = 0
weightGenerationDelta = 0
```

---

# 52. Hidden authority transition

C7 is allowed exactly one hidden state transition, and only on PASS:

```text
Hidden2 / generation2
  -> Hidden3 / generation3
```

Required:

```text
hiddenCommitCount = 1
hiddenGenerationDelta = 1
hiddenLayerDelta = 1
```

On any pre-publication C7 failure:

```text
hiddenCommitCount = 0
```

---

# 53. Hidden publication pointer lineage

Expected final Hidden3 pointer:

```text
layer_index = 3
hidden_generation = 3
previous_pointer_digest = Hidden2 pointer digest
operation_id = C7 hidden commit operation id
semantic_shape_bqh = Hidden2 semantic shape BQH
```

Transition serial must advance monotonically from Hidden2.

No hardcoded transition serial is authority.

---

# 54. Weight pointer after Hidden3 commit

After hidden commit, re-snapshot weight slot.

Require exact equality with C6 adopted pointer.

No field may change because C7 executed a weight lease.

Specifically:

```text
pointer digest unchanged
transition serial unchanged
residency generation unchanged = 2
last execution completion digest unchanged from C6
```

C7 does not yet update weight pointer completion lineage. If later required for progressive execution coordinator semantics, that is a separate explicit contract.

---

# 55. Attention authority behavior

The non-publishing core may create/use the same temporary shared attention authority used by R6-R8.

It must complete its invocation and release temporary attention authority before the core returns.

Candidate and oracle must not share one mutable attention slot concurrently.

Sequential oracle then candidate execution is preferred for deterministic canary evidence.

---

# 56. No concurrency between oracle and candidate forward

C7 does not gain value from executing the two blocks concurrently.

Required canary scheduling:

```text
oracle forward completes
-> device completion observed
-> candidate forward begins
```

or the inverse if implementation requires, but never simultaneous dispatch for the first canary.

This removes cross-route resource interference from the parity proof.

---

# 57. Candidate/oracle ordering authority

The chosen execution order must be explicit in the receipt.

Canonical first C7 policy:

```text
legacy-oracle-first-then-wave-candidate-v1
```

Rationale:

```text
oracle construction/execution can fail without touching candidate hidden publication;
after oracle completes, the C6-adopted candidate runtime pointer is revalidated;
candidate then executes from the still-canonical Hidden2 pointer.
```

---

# 58. Revalidation after oracle

After oracle execution and before candidate lease acquisition, C7 revalidates:

```text
runtime weight pointer == C6 adopted pointer
runtime weight resident counts == 1 block / 9 tensors
active weight lease count == 0
Hidden2 pointer unchanged
Hidden2 generation == 2
active hidden lease count == 0
```

If oracle changed runtime state, C7 fails before candidate execution.

---

# 59. Revalidation before Hidden3 commit

After candidate execution and cross-block comparison but before commit:

```text
runtime weight pointer still == C6 adopted pointer
Hidden2 pointer still canonical
active weight lease count == 0
active hidden lease count == 0
candidate/oracle parity pass
candidate/oracle dispatch parity pass
```

This is the final publication gate.

---

# 60. Candidate final-hidden buffer identity

The candidate final hidden buffer identity digest must be computed from actual same-device output handle metadata, not host tensor contents.

Recommended binding:

```text
shape
device seam / native buffer identity
byte length
buffer offset
buffer size
candidate execution evidence digest
```

No CPU payload hash is required or allowed.

---

# 61. Oracle final-hidden buffer identity

The oracle final hidden gets an independent buffer identity digest.

Candidate and oracle buffer identity digests are expected to differ.

C7 must not require physical buffer identity equality.

Numerical exact parity is the authority for output equality.

---

# 62. Reference block drop

After cross-block parity evidence is sealed:

```text
drop legacy oracle block bundle
drop legacy oracle output tensor after no longer needed
device.poll(Wait) as required
```

C7 may report Rust owner release.

It must not claim physical VRAM freed solely due to drop.

---

# 63. Candidate output publication ownership

After Hidden3 commit the hidden slot owns the runtime hidden authority.

Temporary candidate output owners must be released after publication parity.

No second persistent Hidden3 tensor cache is introduced.

---

# 64. C7 runtime dispatch aggregate

Introduce an aggregate that distinguishes candidate actual dispatch from oracle diagnostic dispatch.

Recommended:

```rust
pub struct R6R9C7ActualDispatchAggregate {
    pub candidate: R6R9C7DispatchSemanticProjection,
    pub oracle: R6R9C7DispatchSemanticProjection,
    pub parity: R6R9C7DispatchParityEvidence,
    pub candidate_actual_dispatch_count: u64,
    pub oracle_diagnostic_dispatch_count: u64,
    pub cross_route_pass_borrow_count: u32,
    pub aggregate_digest: String,
}
```

Candidate actual dispatch and oracle diagnostic dispatch must never be summed into one value and then treated as runtime work performed by the candidate.

---

# 65. Candidate actual path counts

C7 final receipt should separately expose candidate counts:

```text
candidate_input_norm
candidate_qkv
candidate_stage10
candidate_stage11
candidate_stage12
candidate_oproj
candidate_gate
candidate_up
candidate_down
```

Values come from typed evidence, not literals.

---

# 66. Oracle diagnostic path counts

Likewise expose oracle diagnostic counts separately:

```text
oracle_input_norm
oracle_qkv
oracle_stage10
oracle_stage11
oracle_stage12
oracle_oproj
oracle_gate
oracle_up
oracle_down
```

These counts cannot be borrowed to repair missing candidate evidence.

---

# 67. Cross-route PASS borrowing prohibition

Required:

```text
candidatePassDerivedFromOracle = false
oraclePassDerivedFromCandidate = false
dispatchParityPassDerivedFromHiddenParity = false
hiddenParityPassDerivedFromDispatchParity = false
crossRoutePassBorrowCount = 0
```

Every admission surface has independent typed evidence.

---

# 68. C7 final typed receipt

Introduce a final receipt equivalent to:

```rust
pub struct R6R9C7Layer2WaveExecutionParityReceipt {
    pub schema_version: u32,
    pub patch_id: String,
    pub build_revision: String,
    pub c6_transaction_receipt_digest: String,
    pub adopted_weight_pointer_digest: String,
    pub adopted_weight_generation: u64,
    pub input_hidden_binding_digest: String,
    pub legacy_oracle_authority_digest: String,
    pub legacy_oracle_block_identity_digest: String,
    pub candidate_execution_evidence_digest: String,
    pub oracle_execution_evidence_digest: String,
    pub dispatch_parity_evidence_digest: String,
    pub hidden3_full_surface_parity_evidence_digest: String,
    pub published_hidden3_pointer_digest: String,
    pub publication_parity_receipt_digest: String,
    pub runtime_geometry_compared_scalar_count: u64,
    pub mismatch_count: u64,
    pub non_finite_count: u64,
    pub candidate_weight_reload_count: u32,
    pub candidate_block_rebuild_count: u32,
    pub candidate_runtime_rebind_count: u32,
    pub oracle_checkpoint_payload_read_count: u32,
    pub oracle_private_build_count: u32,
    pub oracle_runtime_publish_count: u32,
    pub runtime_weight_authority_overlap_count: u32,
    pub tensor_payload_readback_count: u64,
    pub hidden_commit_count: u32,
    pub pass: bool,
    pub receipt_digest: String,
}
```

---

# 69. Final receipt required success values

```text
adopted_weight_generation          = 2
candidate_weight_reload_count      = 0
candidate_block_rebuild_count      = 0
candidate_runtime_rebind_count     = 0
oracle_checkpoint_payload_read_count = 9
oracle_private_build_count         = 1
oracle_runtime_publish_count       = 0
runtime_weight_authority_overlap_count = 0
mismatch_count                     = 0
non_finite_count                   = 0
tensor_payload_readback_count      = 0
hidden_commit_count                = 1
pass                               = true
```

---

# 70. Artifact receipt wave isolation

C7 final artifacts remain metadata-only and use the existing:

```text
ArtifactReceiptParallelStreamingWaveMap
```

Recommended artifact waves:

```text
0 identity-and-parent
1 C6-adopted-weight-and-Hidden2-binding
2 legacy-oracle-provenance
3 oracle-nonpublishing-execution
4 candidate-runtime-lease-and-nonpublishing-execution
5 dispatch-semantic-parity
6 Hidden3-full-surface-exact-parity
7 Hidden3-publication-and-publication-parity
8 no-reload-no-rebuild-no-readback-closure
```

Artifact receipt waves must not be confused with decoder-weight payload waves or Headwise dispatch waves.

---

# 71. Artifact root key uniqueness

C4-D1 global root-key uniqueness remains enforced.

C7 must use globally unique root fields such as:

```text
c7InputHiddenBinding
c7LegacyOracleProvenance
c7OracleExecutionEvidence
c7CandidateExecutionEvidence
c7DispatchParityEvidence
c7Hidden3FullSurfaceParity
c7PublicationEvidence
c7ExecutionClosure
```

Duplicate-key fail-closed must not be weakened.

---

# 72. Digest hierarchy

Keep independent:

```text
C6 transaction receipt digest
C6 adopted pointer digest
Hidden2 input binding digest
legacy oracle weight authority digest
legacy oracle block identity digest
oracle execution evidence digest
candidate execution evidence digest
candidate dispatch semantic projection digest
oracle dispatch semantic projection digest
dispatch parity evidence digest
cross-block exact parity receipt digest
Hidden3 full-surface parity evidence digest
candidate final-hidden buffer identity digest
oracle final-hidden buffer identity digest
Hidden3 completion token digest
published Hidden3 pointer digest
publication parity receipt digest
C7 final receipt digest
ArtifactReceiptWaveMap digest
```

No one digest may substitute for another authority.

---

# 73. CLI contract

Recommended required flags:

```text
--require-r6-r9-c7-layer2-wave-built-execution-parity true
--r6-r9-c7-target-layer 2
--require-r6-r9-c7-adopted-wave-block-execution-lease true
--require-r6-r9-c7-exact-hidden2-input-binding true
--require-r6-r9-c7-nonpublishing-candidate-forward true
--require-r6-r9-c7-legacy-loader-reference-oracle true
--require-r6-r9-c7-oracle-non-authority true
--require-r6-r9-c7-dispatch-evidence-parity true
--require-r6-r9-c7-hidden3-full-surface-exact-parity true
--require-r6-r9-c7-zero-mismatch true
--require-r6-r9-c7-zero-nonfinite true
--require-r6-r9-c7-publication-after-parity true
--require-r6-r9-c7-publication-exact-parity true
--allow-r6-r9-c7-candidate-weight-reload false
--allow-r6-r9-c7-candidate-block-rebuild false
--allow-r6-r9-c7-candidate-runtime-rebind false
--allow-r6-r9-c7-oracle-runtime-publication false
--allow-r6-r9-c7-oracle-runtime-weight-authority false
--allow-r6-r9-c7-hidden3-pre-parity-commit false
--allow-r6-r9-c7-tensor-payload-readback false
--allow-r6-r9-c7-tolerance-widening false
--allow-r6-r9-c7-cross-route-pass-borrow false
```

Existing R6-R8/Headwise geometry policy remains reused.

---

# 74. First canary execution ordering policy

Recommended fixed canary value:

```text
--r6-r9-c7-oracle-candidate-order legacy-oracle-first-then-wave-candidate-v1
```

This is a canary ordering policy, not a future production requirement.

C8 may remove the oracle entirely from the canonical active path after C7 parity admission.

---

# 75. Implementation surface

Expected semantic implementation files:

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r8_layer1_live_body.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c7_layer2_wave_execution_parity.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

Potential model-core change only if a public non-publishing block execution helper must be exposed without duplicating existing logic:

```text
crates/model_core/src/actual_decoder_block_split_forward.rs
```

No decoder-weight loader semantic change is required.

No residency state-machine semantic change is required.

---

# 76. Candidate/oracle shared-core requirement

C7 should extract shared numerical route code rather than copy hundreds of lines of R6-R8 execution into a second oracle implementation.

Required:

```text
one canonical non-publishing route implementation
candidate calls it
oracle calls it
R6-R8 wrapper may call it
```

Route-specific ownership/admission wrappers remain separate.

This provides SSOT for numerical execution while preserving authority separation.

---

# 77. R6-R8 regression preservation

If R6-R8 is refactored to use the extracted non-publishing core, its existing physical behavior must remain unchanged:

```text
resident Layer1 execution
weight/hide lease validation
actual QKV
Headwise shared/replay/reference validation
OProj/MLP continuation
Hidden2 commit
publication parity
zero payload readback
```

C7 must not weaken the R6-R8 parent gate.

---

# 78. No WGSL semantic change

C7 requires:

```text
WGSL semantic changed file count = 0
```

Existing Headwise and parity shaders are reused.

C7 is a Rust orchestration/authority/parity gate.

---

# 79. No JS/TS core path

C7 core execution, oracle construction, parity, receipts, leases, and publication remain Rust/WGPU/WGSL.

JavaScript/TypeScript may not enter crate/core/runtime/model execution paths.

---

# 80. Static route audit

Before physical run, require at minimum:

```text
C7 calls C6 session entry point = present
C6 adopted pointer exact binding = present
Hidden2 exact pointer/generation binding = present
legacy oracle private loader call = exactly 1 route
legacy oracle runtime adopt call = 0
legacy oracle weight-slot mutation calls = 0
candidate weight lease acquire = present
candidate hidden lease acquire = present
candidate weight reload call = 0
candidate block rebuild call = 0
candidate C4 planner call = 0
candidate C5 staging call = 0
candidate runtime rebind call = 0
shared non-publishing execution core = present
oracle and candidate both use shared core = true
candidate Hidden3 commit before cross-block parity = 0
HeadwiseOutputParityPipeline::compare_exact cross-block = present
dispatch semantic projection = present
dispatch parity mismatch count gate = present
runtime BQH scalar count derived = present
fixed 65536 C7 authority = absent
cross-block tolerance widening = absent
tensor payload readback = 0 path
publication commit after parity = present
publication exact parity = present
weight pointer equality after C7 = present
WGSL semantic change = 0
```

---

# 81. Candidate no-rebuild static search targets

Inside the candidate execution function/module specifically, static audit must find zero references to:

```text
load_base_train_atlas_wave_02_r6_r7_decoder_block_weights
load_base_train_atlas_wave_02_r6_r6_decoder_block
build_r6_r7_actual_decoder_block_for_layer
plan_decoder_weight_atlas_waves
execute_layer_weight_build_staging_private_candidate
weight_slot.adopt
begin_exclusive_destructive_rebind
```

Oracle module scope is exempt only for its explicit private legacy build call.

---

# 82. Runtime compare count source

C7 must compute:

```text
checked_bqh_scalar_count(input_hidden.semantic_shape_bqh)
checked_bqh_scalar_count(candidate_output_shape_bqh)
checked_bqh_scalar_count(oracle_output_shape_bqh)
checked_bqh_scalar_count(published_hidden3.semantic_shape_bqh)
```

All four counts must match.

Overflow is fail-closed.

---

# 83. Shape contract

Required:

```text
candidate input Hidden2 BQH
  == oracle input Hidden2 BQH

candidate Q/K/V shapes
  == oracle Q/K/V shapes

candidate context shape
  == oracle context shape

candidate final Hidden3 BQH
  == oracle final Hidden3 BQH
  == Hidden2 BQH

published Hidden3 BQH
  == candidate final Hidden3 BQH
```

No implicit squeeze/flatten/rebroadcast is permitted for parity comparison.

---

# 84. Checkpoint identity contract

The oracle and candidate ultimately represent the same nine checkpoint roles.

Required exact tensor identity coverage:

```text
role count = 9
tensor identity count = 9
candidate target tensor-set digest == oracle authority digest
candidate tensor identity vector == oracle tensor identity vector
```

Order is the canonical role-registry order from C4.

---

# 85. Module identity contract

Required:

```text
candidate adopted module identity digest
  == oracle built module identity digest
```

If the module identity formula is structural rather than payload-content-complete, tensor identity equality remains independently required.

Neither check replaces the numerical Hidden3 parity gate.

---

# 86. Runtime LoRA contract

Candidate and oracle must bind equivalent runtime LoRA state.

Current BaseTrain route expects:

```text
runtime LoRA set count = 1
trainable LoRA slot count = 0
```

Required:

```text
candidate runtime LoRA binding digest
  == oracle runtime LoRA set digest
```

If the existing bundle receipt exposes equivalent digest fields, reuse them.

No new LoRA path is introduced.

---

# 87. Headwise route identity

Candidate and oracle must bind the same selected Headwise runtime configuration and geometry.

Compare:

```text
attention head count
KV head count
head dim
sequence length
valid length
position IDs
shared runtime route identity
partition/canonical order semantics required by typed evidence
```

No route switching between candidate and oracle is allowed.

---

# 88. Nonce and diagnostic identity

Candidate and oracle may use different diagnostic nonces to prevent accidental receipt identity collision.

Those nonces are not numerical input authority and must be excluded from dispatch semantic parity projection.

They may influence only diagnostic receipt identity where the existing R6-R8 implementation already does so.

---

# 89. Exact parity source order

For receipt semantics use:

```text
reference = legacy oracle Hidden3
candidate = wave-built candidate Hidden3
```

This ordering must remain stable so first-fault interpretation is deterministic.

---

# 90. Zero mismatch interpretation

`mismatch_count=0` in C7 means exact GPU comparison between the complete oracle and candidate Hidden3 surfaces.

It does not mean:

```text
only sampled values match
CPU-readback spot check passes
mean error below threshold
only final token matches
only attention context matches
```

Coverage must be full B*Q*H.

---

# 91. Nonfinite interpretation

Nonfinite count covers both comparison inputs through the parity shader/guard contract.

C7 additionally requires each route's own final finite guard to pass.

No NaN/Inf masking, replacement, clamping, or finite fallback is admitted.

---

# 92. Oracle failure behavior

If the legacy oracle fails to load/build/execute:

```text
candidate execution is not admitted
Hidden2 remains canonical
C7 fails
```

C7 must not say the candidate is correct merely because the oracle is unavailable.

Evidence insufficient -> judgment deferred/fail-closed.

---

# 93. Candidate failure behavior

If candidate lease acquisition or execution fails:

```text
Hidden2 remains canonical
oracle output is dropped
C7 fails
```

No candidate rebuild, legacy oracle adoption, or hidden fallback commit is allowed.

---

# 94. Dispatch parity failure behavior

If numerical Hidden3 parity happens to be exact but dispatch semantic parity fails:

```text
Hidden3 commit = 0
C7 = FAIL
```

Matching output alone does not prove the intended route executed.

---

# 95. Numerical parity failure behavior

If dispatch parity passes but Hidden3 exact comparison fails:

```text
Hidden3 commit = 0
C7 = FAIL
```

Matching dispatch structure alone does not prove equivalent weights or results.

---

# 96. Publication parity failure behavior

If candidate/oracle parity passes but the committed Hidden3 differs from the pre-publication candidate output:

```text
C7 = FAIL
```

The hidden pointer has already advanced in this late failure class, so the failure receipt must explicitly report `postCommitPublicationParityFailure=true`.

No silent rollback is allowed.

This is the only C7 failure class after Hidden3 commit, and commit is deferred until all earlier parity gates pass to minimize that boundary.

---

# 97. Publication atomicity

The existing `LayerHiddenAuthoritySlot::commit_next_layer` remains the only runtime hidden publication authority.

C7 must not manually mutate pointer/tensor fields.

No partial Hidden3 publication exists.

---

# 98. C7 receipt parent bindings

Final C7 receipt must bind:

```text
C6 final receipt digest
C6 transaction receipt digest
C6 adopted pointer digest
C6 target tensor-set digest
C6 target block identity digest
R6-R8 Hidden2 pointer digest
R6-R8 Hidden2 completion token digest
```

This proves C7 executed the exact C6 product, not a separately rebuilt equivalent candidate.

---

# 99. C7 physical terminal line

Expected shape:

```text
[r6-r9-c7-layer2-wave-execution-parity]
weight_layer=2
weight_generation=2
adopted_weight_lease=1
input_hidden_layer=2
input_hidden_generation=2
input_hidden_exact_bound=1
candidate_weight_reload=0
candidate_block_rebuild=0
candidate_rebind=0
oracle_legacy_loader_reads=9
oracle_private_build=1
oracle_runtime_publish=0
oracle_runtime_weight_authority=0
candidate_input_norm=1
candidate_qkv=1
candidate_oproj=1
candidate_gate=1
candidate_up=1
candidate_down=1
dispatch_parity=1
compared=<runtime-derived BQH scalar count>
mismatch=0
nonfinite=0
payload_readback=0
hidden3_commit=1
hidden_layer=3
hidden_generation=3
publication_mismatch=0
weight_pointer_unchanged=1
runtime_authority_overlap=0
candidate_evidence_digest=<sha256>
oracle_evidence_digest=<sha256>
dispatch_parity_digest=<sha256>
hidden3_parity_digest=<sha256>
published_hidden3_pointer_digest=<sha256>
proof_ledger=HOLD
```

Headwise stage values may also be printed but must come from typed evidence.

---

# 100. PASS token

Recommended token:

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R9_C7_LAYER2_WAVE_BUILT_DECODER_EXECUTION_PARITY_C6_PHYSICAL_PARENT_EXACT_C6_ADOPTED_LAYER2_WEIGHT_POINTER_GENERATION2_EXECUTION_LEASE_EXACT_R6_R8_HIDDEN2_GENERATION2_INPUT_BINDING_NONPUBLISHING_WAVE_CANDIDATE_FORWARD_ACTUAL_INPUT_RMSNORM_QKV_NEOX_ROPE_HEADWISE_W5_W6_W7_OPROJ_ATTENTION_RESIDUAL_POST_ATTN_RMSNORM_SWIGLU_GATE_UP_DOWN_FFN_RESIDUAL_ROUTE_LEGACY_FULL_LAYER_LOADER_PRIVATE_REFERENCE_BLOCK_NON_AUTHORITY_ORACLE_EXACT_NINE_TENSOR_PROVENANCE_AND_MODULE_IDENTITY_BINDING_SHARED_NONPUBLISHING_NUMERICAL_ROUTE_DISPATCH_SEMANTIC_EVIDENCE_PARITY_ZERO_FIELD_MISMATCH_HIDDEN3_FULL_SURFACE_GPU_EXACT_PARITY_ZERO_MISMATCH_ZERO_NONFINITE_RUNTIME_DERIVED_BQH_COVERAGE_CANDIDATE_WEIGHT_RELOAD_ZERO_CANDIDATE_BLOCK_REBUILD_ZERO_CANDIDATE_REBIND_ZERO_ORACLE_RUNTIME_PUBLICATION_ZERO_RUNTIME_WEIGHT_AUTHORITY_OVERLAP_ZERO_TENSOR_PAYLOAD_READBACK_ZERO_HIDDEN3_PUBLICATION_ONLY_AFTER_PARITY_PUBLICATION_EXACT_PARITY_WEIGHT_LAYER2_GENERATION2_UNCHANGED_HIDDEN_LAYER3_GENERATION3_SINGLE_COMMIT_CANONICAL_GENERALIZED_WAVE_LOADER_ADOPTION_PROGRESSIVE_N_LAYER_FINAL_NORM_LM_HEAD_FORWARD_LOSS_BACKWARD_OPTIMIZER_PRODUCTION_INFERENCE_BLOCKED_PROOF_LEDGER_HOLD_SEALED
```

---

# 101. Physical PASS meaning

C7 physical PASS proves:

```text
the exact C6-adopted wave-built Layer2 block is executable through a runtime weight lease;
the exact Hidden2 parent state is used;
the candidate performs the actual admitted decoder route;
a private block built by the legacy loader represents the same checkpoint tensor set;
the oracle has no runtime authority;
candidate and oracle dispatch semantics match;
candidate and oracle Hidden3 surfaces match exactly across all runtime BQH elements;
no nonfinite values are present;
the candidate path does not reload/rebuild/rebind weights;
no tensor payload is read back;
Hidden3 is committed only after parity admission;
weight Layer2 / generation2 remains resident unchanged.
```

---

# 102. Physical PASS does not prove

C7 PASS does not prove:

```text
destructive C6 failure injection / RecoveryRequired branch
oracle-free canonical generalized wave-loader adoption
Layer2 -> Layer3 wave rebind
progressive N-layer execution
22-layer long-horizon memory behavior
final RMSNorm
LM head
logits parity
forward loss
backward
optimizer
production inference
physical VRAM/RSS improvement
performance improvement
```

---

# 103. Admission matrix after C7 PASS

```text
R6-R6 live body                                  = ADMITTED
R6-R7 layer-weight residency                     = ADMITTED
R6-R8 Layer1 forward                             = ADMITTED
R6-R9-C1 historical Layer2 step                  = ADMITTED
R6-R9-C2 coordinator evidence truth              = ADMITTED
R6-R9-C3 wave-domain split                       = ADMITTED
R6-R9-C4 decoder-weight wave planner             = ADMITTED_PLANNER_ONLY
R6-R9-C4-D1 plan collection closure              = ADMITTED
R6-R9-C5 private staging/build                   = ADMITTED_PRIVATE_CANDIDATE
R6-R9-C6 Layer1 -> Layer2 wave rebind canary     = ADMITTED_RUNTIME_REBIND_CANARY
R6-R9-C7 wave-built Layer2 execution parity      = ADMITTED_EXECUTION_PARITY on PASS

DecoderWeightAtlasWave planning                  = ADMITTED
DecoderWeightAtlasWave private build             = ADMITTED
DecoderWeightAtlasWave runtime adoption          = ADMITTED_CANARY_ONLY
DecoderWeightAtlasWave executed-block parity     = ADMITTED on PASS
canonical generalized wave-loader adoption       = BLOCKED / C8
progressive N-layer promotion                    = BLOCKED / C9
long-horizon residency/memory ledger             = BLOCKED / C10
full N-layer execution                           = BLOCKED
final RMSNorm / LM head                          = BLOCKED
forward loss                                     = BLOCKED
backward                                         = BLOCKED
optimizer                                        = BLOCKED
production inference                             = BLOCKED
proof ledger                                     = HOLD
```

---

# 104. Next boundary

After physical C7 PASS:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C8

Canonical Decoder Weight Wave Loader Adoption /
R6-R7 Legacy Full-Layer Target Loader Retirement /
Generalized Source-N -> Target-N+1 Wave Rebind /
C4 Planner + C5 Staging + C6 Destructive Transaction Reuse /
C7 Execution-Parity Admission Binding /
No Oracle On Canonical Active Path /
No Parallel Legacy Rebind Authority /
Single Decoder Weight Transport Authority Seal
```

C8 is the first gate allowed to replace the canonical generalized R6-R7/R6-R9 target-weight loader with the admitted decoder-weight wave transport.

The legacy full-layer loader remains available only as explicitly named validation/reference tooling if later retained.

---

# 105. Architecture seal

> C7 does not ask whether a privately wave-built block can exist; C5 proved that. It does not ask whether such a block can become runtime weight SSOT; C6 proved that. C7 asks the harder question: when the exact C6-adopted Layer2 block takes a real runtime execution lease and consumes the exact Hidden2 state, does it execute the same decoder computation and produce the exact same full Hidden3 surface as an independently built legacy-loader Layer2 block, while the candidate performs zero weight reloads, zero rebuilds, zero rebinds, and zero tensor payload readbacks? Only after the answer is independently YES for provenance, dispatch semantics, numerical full-surface parity, and finite-state checks may candidate Hidden3 become the next hidden SSOT.
