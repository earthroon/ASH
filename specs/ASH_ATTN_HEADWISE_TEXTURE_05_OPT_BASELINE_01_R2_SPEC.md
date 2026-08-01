# ASH-ATTN-HEADWISE-TEXTURE-05-OPT-BASELINE-01-R2

## Physical Capture Producer /
## Existing Texture-05 Executor Reuse /
## Canonical Five-Epoch Runner /
## Four-Pair AB·BA Cell Schedule /
## Reference-Only Child Process /
## Candidate-Only Child Process /
## Live Timestamp Receipt Adoption /
## Requested Memory Live Census /
## Runtime Shader Identity Derivation /
## Worker Auto-Spawn /
## Typed Missing-Parent Preflight /
## No External Input JSON Dependency /
## Rust-Authored Specification·Manifest Seal

> Status: **SPEC RELEASE rev.1**  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-05-OPT-BASELINE-01-R2`  
> Build revision: `HEADWISE-TEXTURE-05-OPT-BASELINE-01-R2-physical-capture-producer-v1`  
> Parent implementation: `ASH-ATTN-HEADWISE-TEXTURE-05-OPT-BASELINE-01-R1` import closure  
> Parent verification state: `PASS`  
> Parent physical state: `BLOCKED - PhysicalCaptureProducerMissing`  
> Existing production executor: `BufferAtlasV1` unchanged  
> Existing candidate executor: `KvTextureGqa4V1` shadow-only unchanged  
> Output authority: `HeadwiseFullActive` unchanged  
> Patch-local readiness after PASS: `PhysicalOptimizationBaselineCaptured`  
> Performance-benefit decision: **not performed by this patch**  
> Production promotion: **forbidden**

---

# 0. Source-grounded diagnosis

## 0.1 Confirmed parent state

The R1 verification binary compiles and returns its canonical PASS token. The four physical parent runtime artifacts also exist and report PASS:

```text
ash_attn_headwise_texture_05_r3_r2_runtime_artifact.json
ash_attn_headwise_texture_05_r3_r3_r2_runtime_artifact.json
ash_attn_headwise_texture_05_r4_runtime_artifact.json
ash_attn_headwise_texture_05_r4_r1_runtime_artifact.json
```

The R1 physical gate nevertheless fails before baseline evaluation because the following files do not exist:

```text
paired_capture_bundle.json
reference_worker_runtime_artifact.json
candidate_worker_runtime_artifact.json
reference_shader_identity.json
candidate_shader_identity.json
```

## 0.2 Exact implementation gap

The R1 physical gate is a consumer. It calls `read_json` for a pre-existing paired bundle, two worker artifacts and two shader identities.

The R1 worker is also a consumer. It expects a pre-existing:

```text
job manifest
capture bundle
shader identity
requested-memory receipt
memory-plane-split receipt
```

The R1 verification gate creates deterministic synthetic fixtures, but does not execute BufferAtlas or Texture-05 physical GPU work.

Therefore the current graph is:

```text
physical capture producer       missing
R1 worker                       consumes pre-baked input JSON
R1 physical gate                consumes worker and paired JSON
R1 verification gate            validates schema and logic only
```

The Windows `os error 3` is a missing producer boundary, not a user path typo and not a failed GPU measurement.

## 0.3 Existing physical executor is present but trapped

The existing `ash_attn_headwise_texture_05_gate` already owns the required physical pieces:

```text
existing-device bootstrap
HeadwiseTexturePipelineManager
session-persistent K/V texture residency
one-time full population
monotonic append
BufferAtlas reference dispatch
Texture microtile wave dispatch
R3-R3-R2 packetization
R4 timestamp query ring
compact device comparison
manual GC
requested-resource owner ledger
session retirement
```

Its current helper `run_shadow_replay_against_current_generation` always performs the combined fixed order:

```text
BufferAtlas reference
-> reference capture
-> Texture candidate
-> compare/finalize
```

That helper is private to one binary and cannot produce BA order or true isolated lanes. R2 extracts and splits this executor rather than copying it.

---

# 1. Goal

R2 changes OPT-BASELINE-01 from:

```text
read externally prepared measurement JSON
-> validate
-> aggregate
-> write artifact
```

into:

```text
preflight parent lineage and runtime capability
-> derive one canonical run identity
-> create run-local Rust-authored specification
-> execute five paired physical epochs
-> retire paired resources to owner zero
-> self-spawn reference-only child epochs
-> self-spawn candidate-only child epochs
-> derive shader identities from live runtime construction
-> capture requested-memory owner ledgers
-> seal R1-compatible raw capture bundles
-> reuse R1 statistics and admissibility evaluator
-> write runtime artifact and local manifest
```

The command must not depend on a user-created `input/` directory or pre-baked capture JSON.

---

# 2. Non-negotiable authority boundary

## 2.1 Production authority preserved

```text
DecodeState K/V authority
BufferAtlasV1 production route
HeadwiseFullActive output authority
production token history
production generation lineage
```

## 2.2 R2 evidence authority

```text
measurement schedule
paired executor order
executor-local GPU timing
isolated timing
requested-memory owner census
runtime shader identity
child-process lifecycle
raw capture artifacts
baseline admissibility
```

## 2.3 Forbidden authority expansion

```text
R2 result -> production route mutation
R2 result -> candidate output commit
R2 result -> downstream candidate consumption
R2 result -> Texture production promotion
measurement runner -> production token-history mutation
worker failure -> BufferAtlas production suppression
candidate private output -> model state mutation
```

Required all-zero counters:

```text
candidate output commit count             0
candidate downstream consumer count       0
route authority mutation count            0
output authority mutation count           0
physical production executor switch count 0
production token-history mutation count   0
TensorCube texture consumer count          0
```

---

# 3. Reuse architecture

## 3.1 Extract one reusable physical executor

The physical executor currently embedded in:

```text
crates/orchestrator_local/src/bin/
  ash_attn_headwise_texture_05_gate.rs
```

must be extracted into:

```text
crates/orchestrator_local/src/
  headwise_texture_05_physical_executor.rs
```

Both the original Texture-05 gate and OPT-BASELINE R2 call the same module.

The extraction owns:

```rust
pub struct HeadwiseTexture05PhysicalExecutorConfig;
pub struct HeadwiseTexture05PhysicalSession;
pub struct HeadwiseTexture05PreparedInvocation;
pub struct HeadwiseTexture05ReferenceExecution;
pub struct HeadwiseTexture05CandidateExecution;
pub struct HeadwiseTexture05PairComparison;
pub struct HeadwiseTexture05PhysicalRetirementReceipt;
```

## 3.2 Existing implementation authority reused

R2 must call the existing implementations for:

```text
bootstrap_existing_device
HeadwiseTexturePipelineManager
HeadwiseTextureSessionResidencyRegistry
HeadwiseTexture05PersistentSourceBuffers
bootstrap_persistent_texture_generation
append_persistent_texture_generation
BufferAtlasV1 reference dispatch
Texture microtile wave dispatch
R3-R3-R2 packet planner and admission receipts
HeadwiseTexture05R4TimestampProbeRing
manual GC and owner-zero logic
```

Forbidden:

```text
second texture residency model
R2-only page allocator
R2-only BufferAtlas kernel
copied WGSL source
copied packet executor
synthetic physical timing
host-wall timing substituted for GPU timestamp
```

## 3.3 Original gate parity

After extraction, the original Texture-05 gate must produce byte-equivalent semantic receipts for an unchanged fixture, excluding explicitly versioned source-location fields.

Required regression:

```text
original coverage cell set equal
original generation plan equal
original R4 stage totals equal within timestamp replay tolerance
original packet topology equal
original numeric parity equal
original authority counters equal
```

---

# 4. Executor split required for AB·BA

## 4.1 Current combined helper is insufficient

The fixed helper cannot produce a genuine BA pair because Texture comparison currently expects a reference result that has already been captured.

R2 splits one invocation into three phases:

```text
ReferenceExecutor
CandidateExecutorDeferredCompare
PairCompareFinalize
```

## 4.2 Reference stage

```rust
pub fn execute_reference_stage(
    session: &mut HeadwiseTexture05PhysicalSession,
    invocation: &HeadwiseTexture05PreparedInvocation,
    probe: &HeadwiseTexture05ExecutorLocalProbe,
) -> Result<HeadwiseTexture05ReferenceExecution>;
```

The result contains:

```text
private reference output leases
22 reference dispatch receipts
reference stage GPU timestamp receipt
reference host encode/submit/poll receipt
reference requested-memory events
output fingerprint source handles
```

## 4.3 Candidate stage with deferred compare

```rust
pub fn execute_candidate_stage_deferred_compare(
    session: &mut HeadwiseTexture05PhysicalSession,
    invocation: &HeadwiseTexture05PreparedInvocation,
    probe: &HeadwiseTexture05ExecutorLocalProbe,
) -> Result<HeadwiseTexture05CandidateExecution>;
```

The candidate stage:

```text
uses the existing persistent texture generation
preserves R3-R3-R2 packet order
writes private candidate output only
records accumulate and normalize timestamps
retains candidate output until compare
performs no production commit
requires no reference output before execution
```

No candidate kernel arithmetic, microtile size, merge order or packet boundary may change.

## 4.4 Compare/finalize stage

```rust
pub fn compare_and_finalize_pair(
    session: &mut HeadwiseTexture05PhysicalSession,
    invocation: &HeadwiseTexture05PreparedInvocation,
    reference: HeadwiseTexture05ReferenceExecution,
    candidate: HeadwiseTexture05CandidateExecution,
) -> Result<HeadwiseTexture05PairComparison>;
```

This phase performs:

```text
existing device comparison
compact parity-token readback
reference/candidate output digest binding
private output retirement
pair receipt seal
```

Compare/finalize time is disclosed separately and excluded from both executor timing ratios.

## 4.5 No hidden re-execution

For every measured pair:

```text
reference executor count == 1
candidate executor count == 1
pair compare count        == 1
```

Forbidden:

```text
candidate dry run before BA candidate timing
candidate rerun after reference becomes available
reference rerun for digest generation
discarded first-stage output
silent AB fallback when BA is requested
```

---

# 5. Canonical five-epoch paired runner

## 5.1 Canonical cells

R2 reuses the existing OPT-BASELINE cell authority:

```text
seq_kv: 64, 192, 384, 768, 1280, 1792
routes:
  IncrementalDecode Q1
  ChunkedDecode Q2
  ChunkedDecode Q6
  ChunkedDecode Q12
  ChunkedDecode Q24
```

```text
6 KV buckets × 5 route/query shapes = 30 cells
```

## 5.2 Epoch profile

```text
measurement epochs                           5
paired warmup pairs/cell/epoch               1
paired measured pairs/cell/epoch             4
paired warmup pair count                    150
paired measured pair count                  600
measured executor invocations             1,200
```

Every epoch creates a new physical Texture session:

```text
new decode_session_id
new session_epoch
one persistent registry
one full population at KV64
five monotonic append transitions
six texture generations
explicit session retirement
owner-zero receipt
```

Across paired execution:

```text
session full populations  5
append transactions       25
measured candidate runs  600
measured reference runs  600
```

Warmup runs are recorded but excluded from baseline statistics.

## 5.3 Route rotation

R2 reuses the R1 canonical route rotation:

```text
E0  Q1,  Q2,  Q6,  Q12, Q24
E1  Q2,  Q6,  Q12, Q24, Q1
E2  Q6,  Q12, Q24, Q1,  Q2
E3  Q12, Q24, Q1,  Q2,  Q6
E4  Q24, Q1,  Q2,  Q6,  Q12
```

KV order remains monotonic within each epoch:

```text
64 -> 192 -> 384 -> 768 -> 1280 -> 1792
```

## 5.4 Four-pair order block

Even epochs:

```text
AB, BA, BA, AB
```

Odd epochs:

```text
BA, AB, AB, BA
```

Permanent identity:

```text
A = BufferAtlasV1 reference executor
B = KvTextureGqa4V1 candidate executor
```

Per cell totals:

```text
AB 10
BA 10
```

## 5.5 Pair execution

AB:

```text
prepare immutable invocation
-> execute reference stage
-> execute candidate stage deferred compare
-> compare/finalize
-> retire pair transients
```

BA:

```text
prepare immutable invocation
-> execute candidate stage deferred compare
-> execute reference stage
-> compare/finalize
-> retire pair transients
```

Between the first and second executor:

```text
Q/K/V lease mutation                         0
texture generation transition                0
pipeline creation                            0
manual GC                                    0
route mutation                               0
first output retirement                      0
```

---

# 6. Matched invocation authority

Every pair uses one immutable identity:

```rust
pub struct HeadwiseTexture05R2MatchedInvocation {
    pub model_instance_id: String,
    pub decode_session_id: String,
    pub session_epoch: u64,
    pub measurement_epoch: u32,
    pub cell: HeadwiseTexture05OptBaselineCellKey,
    pub pair_ordinal_in_cell: u32,
    pub production_generation: u64,
    pub texture_generation: u64,
    pub q_source_lease_digest: String,
    pub k_source_lease_digest: String,
    pub v_source_lease_digest: String,
    pub causal_snapshot_digest: String,
    pub geometry_digest: String,
    pub invocation_seed_digest: String,
    pub identity_digest: String,
}
```

Required equality across A and B:

```text
model instance
session and epoch
cell
batch/head geometry
seq_q and seq_kv
Q source bytes
K source bytes
V source bytes
causal boundary
production generation
texture generation view
invocation seed
```

The execution order may change. Invocation content may not.

---

# 7. Live R4 timestamp adoption

## 7.1 Existing query authority

R2 extends, rather than replaces:

```text
HeadwiseTexture05R4TimestampProbeRing
HeadwiseTexture05R4CommitProbe
HeadwiseTexture05R4CommitMeasurement
```

New execution modes:

```rust
pub enum HeadwiseTexture05R2ProbeMode {
    Paired,
    ReferenceOnly,
    CandidateOnly,
}
```

## 7.2 Executor-local timing spans

Primary reference timing:

```text
sum of 22 BufferAtlas reference stage timestamp pairs
```

Primary candidate timing:

```text
sum of 22 candidate accumulate timestamp pairs
+ sum of 22 candidate normalize timestamp pairs
```

Compare, capture, compact readback, fingerprint and manual GC are excluded from executor ratios and disclosed separately.

## 7.3 No timing-topology mutation

```text
new timing-only submissions 0
new per-stage polls         0
per-layer readbacks         0
payload readback in timed span 0
```

Query resolution occurs once at the existing completion boundary for each executor invocation or pair.

## 7.4 BA timestamp validity

Candidate and reference query indices are stage-owned, not order-owned. BA may write candidate indices before reference indices. Query ownership remains unique and query resolution occurs after both executors and compare have completed.

## 7.5 Live receipt conversion

R2 converts physical R4 receipts directly into:

```text
HeadwiseTexture05PairedTimingSample
HeadwiseTexture05IsolatedTimingSample
```

No timing number may be loaded from a fixture, copied from a parent aggregate or synthesized from host-wall duration.

---

# 8. Paired output parity and oracle set

## 8.1 Paired parity remains authoritative

Every warmup and measured pair runs the existing device comparison.

Required:

```text
paired numeric mismatch count 0
compact parity-token readback count == pair count
candidate output commit count 0
payload readback count in paired path 0
```

## 8.2 Isolated oracle generation

The paired runner derives one canonical output fingerprint authority per:

```text
measurement epoch
cell
texture generation
invocation seed
```

The fingerprint is produced after the timed executor stage and is not included in executor timing.

```rust
pub struct HeadwiseTexture05R2OutputFingerprintReceipt {
    pub oracle_id: String,
    pub measurement_epoch: u32,
    pub cell_id: String,
    pub production_generation: u64,
    pub texture_generation: u64,
    pub output_word_count: u64,
    pub fingerprint_words: [u32; 8],
    pub source_executor: String,
    pub receipt_digest: String,
}
```

The paired device comparison remains the exact numerical authority. The compact fingerprint is an isolated-lane consistency and provenance check, not a replacement for exact pair parity.

## 8.3 Candidate-only independence

Candidate-only child execution receives the Rust-authored oracle set digest in its job manifest. It performs no BufferAtlas dispatch.

Required:

```text
candidate worker measured BufferAtlas dispatches 0
candidate worker total BufferAtlas dispatches    0
candidate fingerprint mismatch count             0
```

---

# 9. Child-process architecture

## 9.1 Single self-spawning binary

R2 uses one physical binary:

```text
ash_attn_headwise_texture_05_opt_baseline_01_r2_gate
```

Default mode is parent orchestration. Child modes are invoked by spawning `std::env::current_exe()`:

```text
parent
reference_only_child
candidate_only_child
```

A separate prebuilt worker executable is not required. Therefore `cargo run --bin ...r2_gate` cannot fail merely because a sibling worker binary was not built.

## 9.2 Epoch-scoped child processes

Each isolated epoch runs in a fresh child process.

```text
reference child processes 5
candidate child processes 5
total isolated children  10
```

Each child executes:

```text
30 cells
1 warmup invocation/cell
2 measured invocations/cell
```

Per lane totals:

```text
warmup samples   150
measured samples 300
```

## 9.3 Child launch order

To disclose process-order effects:

```text
E0 reference -> candidate
E1 candidate -> reference
E2 reference -> candidate
E3 candidate -> reference
E4 reference -> candidate
```

The launch order is recorded in the epoch receipt. It is diagnostic and does not replace paired AB·BA authority.

## 9.4 Parent-generated internal job contract

The parent atomically writes each child job manifest and response file under the run directory.

These are internal execution products, not external prerequisites.

The child validates:

```text
parent run identity
patch and build revision
source-tree digest
executable digest
adapter identity requirement
epoch number
lane kind
cell schedule digest
oracle-set digest
output paths
```

## 9.5 Child lifecycle receipt

```rust
pub struct HeadwiseTexture05R2ChildProcessReceipt {
    pub child_mode: String,
    pub measurement_epoch: u32,
    pub executable_path: String,
    pub executable_digest: String,
    pub job_manifest_digest: String,
    pub process_id: u32,
    pub launch_ordinal: u32,
    pub exit_code: i32,
    pub stdout_digest: String,
    pub stderr_digest: String,
    pub runtime_artifact_digest: String,
    pub local_manifest_digest: String,
    pub timed_out: bool,
    pub pass: bool,
    pub receipt_digest: String,
}
```

Silent retry is forbidden. A failed child produces a typed HOLD and preserves its stdout/stderr evidence.

---

# 10. Reference-only child

## 10.1 Execution contract

```text
BufferAtlasV1 reference execution admitted
Texture residency registry creation count 0
Texture object creation count 0
Texture candidate dispatch count 0
candidate output commit count 0
```

The child reuses the extracted reference executor and R4 reference timestamp span.

## 10.2 Sample output

For every measured invocation:

```text
reference executor GPU ns
host encode ns
host submit ns
host poll ns
output fingerprint
runtime shader identity digest
requested-memory receipt digest
physical-memory diagnostic digest or unsupported state
```

## 10.3 Retirement

After each epoch:

```text
reference-exclusive owner count 0
harness-only owner count 0
reference-exclusive descriptor bytes 0
device.poll(Wait) complete
unretired resource IDs empty
```

Device and pipeline manager may remain until process exit, but are classified as `DeviceShared`.

---

# 11. Candidate-only child

## 11.1 Execution contract

```text
persistent Texture residency admitted
one full population at KV64
five monotonic append transitions
Texture candidate execution admitted
BufferAtlas reference dispatch count 0
pair compare dispatch count 0
production output commit count 0
```

## 11.2 Candidate-only validation

The candidate output fingerprint is generated after the timed candidate stage and compared with the paired runner oracle for the same epoch/cell identity.

```text
fingerprint work excluded from candidate executor GPU ns
fingerprint mismatch fails the child
paired exact parity remains canonical numerical authority
```

## 11.3 Candidate topology preservation

```text
R3-R3-R2 packet order unchanged
microtile size unchanged
streaming-softmax merge order unchanged
final candidate private output retained only until fingerprint
queue-ahead unchanged
max in-flight packet unchanged
```

## 11.4 Retirement

After each epoch:

```text
SessionPersistent owner count 0
GenerationMetadata owner count 0
CommitTransient owner count 0
HarnessOnly owner count 0
candidate-exclusive descriptor bytes 0
unretired resource IDs empty
```

---

# 12. Requested-memory live census

## 12.1 No hand-authored memory receipt

R2 workers build `HeadwiseTexture05RequestedMemoryReceipt` from live allocation and retirement events.

The verification fixture may construct synthetic records. The physical path may not.

## 12.2 Owner classes

R2 reuses:

```text
DeviceShared
ModelShared
ReferenceExclusive
CandidateExclusive
HarnessOnly
```

## 12.3 Allocation observer

New observer:

```rust
pub trait HeadwiseTexture05OptBaselineAllocationObserver {
    fn on_create(&self, event: HeadwiseTexture05AllocationEvent) -> Result<()>;
    fn on_retire(&self, resource_id: &str, serial: u64) -> Result<()>;
    fn snapshot(
        &self,
        boundary: HeadwiseTexture05MemoryBoundary,
    ) -> Result<HeadwiseTexture05MemorySnapshot>;
}
```

The existing BufferAtlas and Texture-05 physical constructors accept an optional observer. `None` preserves all current production behavior.

## 12.4 Required boundaries

```text
P0 process start
P1 device and pipeline warm
P2 executor persistent state ready
P3 measured steady-state peak
P4 executor resources dropped
P5 device.poll(Wait) after retirement
```

## 12.5 Candidate memory adoption

Candidate memory records adapt the existing R3-R2 owner ledger rather than reconstructing totals from constants.

Expected geometry remains visible:

```text
44 K/V texture objects
22 validation buffers
2 persistent source buffers when owned
persistent registry and page tables
current/previous generation metadata
commit transients
```

`known_floor_bytes=95,944,792` may appear only when the live owner ledger sums to that value for the unchanged F32 geometry.

## 12.6 Reference memory adoption

BufferAtlas allocations currently lacking owner events must be instrumented at their actual create/drop sites.

Reference memory may not be inferred as:

```text
candidate bytes / claimed reduction ratio
parent process memory delta
OS dedicated-memory delta
```

## 12.7 Comparison authority

```text
shared owner-set digest equality required
exclusive requested peak compared separately
harness bytes excluded from executor-exclusive comparison
borrowed shared bytes remain physically present
```

If shared owner sets differ:

```text
requested_memory_comparison.status = incomparable_shared_ownership
baseline admissibility = HOLD
```

---

# 13. Physical-memory diagnostic plane

Physical telemetry remains diagnostic-only.

Allowed statuses:

```text
available
unsupported
permission_denied
sampling_failed
cross_source_inconsistent
```

Unsupported telemetry does not fail requested-memory evidence.

Required invariant:

```text
physical_memory_authoritative_for_owner_lifetime = false
```

R2 must not report a physical-memory reduction when the status is not `available` and internally consistent.

---

# 14. Runtime shader identity derivation

## 14.1 No pre-existing identity JSON

R2 derives identity during live pipeline construction.

Reference identity includes:

```text
BufferAtlas WGSL source digests
entry points
bind-group layout descriptor digest
pipeline layout descriptor digest
specialization constants
reference executor registration identity
```

Candidate identity includes:

```text
Texture partial/merge/normalize/finalize WGSL digests
entry points
texture format
bind-group layout descriptor digests
pipeline layout descriptor digests
packet profile
candidate executor registration identity
```

Both include:

```text
source-tree digest
executable digest
Cargo feature digest
wgpu backend identity
adapter identity
adapter features and limits digest
driver identity
```

## 14.2 Source-tree digest

R2 computes a canonical source-tree digest from an allowlisted file inventory. The inventory is generated in Rust and recorded in the runtime specification.

No `REPLACE_WITH_BAKED_SOURCE_TREE_SHA256` placeholder is permitted.

## 14.3 Bake archive digest

The extracted runtime may not have access to its source ZIP. Therefore bake archive digest is optional diagnostic metadata.

```text
provided and valid   -> recorded
not provided         -> status not_provided
placeholder text     -> typed preflight failure
```

Bake archive absence does not invalidate runtime shader identity.

## 14.4 Identity stability

Required across all physical samples:

```text
one reference identity digest
one candidate identity digest
pipeline creation delta during measured interval 0
shader module creation delta during measured interval 0
hot reload count 0
fallback shader count 0
```

---

# 15. Typed missing-parent and runtime preflight

## 15.1 Preflight runs before GPU allocation

Preflight order:

```text
CLI registry
-> response-file digest
-> parent path existence
-> parent JSON parse
-> parent schema/patch/pass validation
-> parent digest binding
-> source response-file validation
-> output-root write probe
-> current executable digest
-> source-tree inventory digest
-> placeholder rejection
-> adapter and timestamp capability probe
-> canonical schedule seal
-> runtime specification write
```

## 15.2 Error types

```rust
pub enum HeadwiseTexture05R2PreflightErrorCode {
    ParentArtifactMissing,
    ParentArtifactUnreadable,
    ParentArtifactJsonInvalid,
    ParentArtifactSchemaMismatch,
    ParentArtifactPatchMismatch,
    ParentArtifactNotPass,
    ParentArtifactDigestMismatch,
    SourceResponseFileMissing,
    SourceResponseFileInvalid,
    OutputRootNotWritable,
    RuntimePlaceholderPresent,
    TimestampFeatureUnavailable,
    AdapterIdentityUnavailable,
    ExistingRunCollision,
    CanonicalScheduleMismatch,
}
```

The process error must include code and exact path:

```text
Texture05OptBaselineR2PreflightHold:<Code>:<Path>
```

Generic `os error 3` without typed localization is forbidden.

## 15.3 Preflight artifact

Even on HOLD, Rust writes:

```text
preflight_receipt.json
preflight_failure_receipt.json, when applicable
```

No canonical baseline artifact is written on preflight HOLD.

---

# 16. No external input JSON dependency

## 16.1 Forbidden R2 CLI inputs

The R2 physical CLI must not contain required input keys for:

```text
--paired-capture-bundle
--reference-worker-runtime-artifact
--candidate-worker-runtime-artifact
--reference-shader-identity
--candidate-shader-identity
--reference-capture-bundle
--candidate-capture-bundle
--requested-memory-receipt
--memory-plane-split-receipt
```

## 16.2 Allowed reads

R2 may read only:

```text
four parent runtime artifacts
canonical Texture-05 source response file
Rust-authored run-local child job files created earlier in the same invocation
Rust-authored child outputs created by the spawned process
```

## 16.3 Run-local output root

```text
workspace/runtime/attention/headwise/texture/05/opt_baseline_01_r2/
  runs/<run_id>/
```

`run_id` binds:

```text
patch/build revision
parent artifact digests
source-tree digest
executable digest
model identity
adapter identity
canonical schedule digest
start nonce
```

Pre-existing files under another run ID are ignored. Pre-existing files under the same run ID cause `ExistingRunCollision`; silent reuse is forbidden in R2.

---

# 17. R1 schema and evaluator reuse

R2 writes R1-compatible evidence types:

```text
HeadwiseTexture05OptBaselinePairedCaptureBundle
HeadwiseTexture05OptBaselineWorkerCaptureBundle
HeadwiseTexture05PairedTimingSample
HeadwiseTexture05IsolatedTimingSample
HeadwiseTexture05RequestedMemoryReceipt
HeadwiseTexture05MemoryPlaneSplitReceipt
HeadwiseTexture05ShaderVariantIdentity
```

R2 then calls the existing:

```text
summarize_opt_baseline_statistics
evaluate_headwise_texture_05_opt_baseline_admissibility
```

R2 may add wrapper receipts, but it must not fork percentile, order-bias, epoch-spread or admissibility formulas.

---

# 18. Parent and child orchestration state machine

```rust
pub enum HeadwiseTexture05R2RunState {
    Cold,
    PreflightPassed,
    RuntimeSpecificationPublished,
    PairedEpochRunning {
        epoch: u32,
    },
    PairedResourcesRetiring,
    PairedOwnerZero,
    IsolatedChildRunning {
        epoch: u32,
        lane: HeadwiseTexture05IsolatedLaneKind,
    },
    ChildArtifactsVerified,
    Aggregating,
    Admitted,
    Held,
    Retired,
}
```

Forbidden transitions:

```text
Cold -> GPU execution
PairedEpochRunning -> isolated spawn before paired owner zero
child exit -> aggregation before artifact digest verification
Held -> canonical artifact publication
Admitted -> production authority mutation
```

---

# 19. Canonical execution counts

## 19.1 Paired lane

```text
paired warmup pairs                         150
paired measured pairs                       600
paired total pairs                          750
reference executions in paired lane         750
candidate executions in paired lane         750
pair comparisons                            750
measured paired executor invocations      1,200
```

## 19.2 Isolated reference lane

```text
child processes                               5
warmup invocations                          150
measured invocations                        300
BufferAtlas executions                      450
Texture executions                            0
```

## 19.3 Isolated candidate lane

```text
child processes                               5
warmup invocations                          150
measured invocations                        300
Texture executions                          450
BufferAtlas executions                        0
full population transactions                  5
append transactions                          25
```

## 19.4 Total physical executor work

```text
measured executor invocations              1,800
warmup executor invocations                  600
total executor invocations                 2,400
```

These values exclude compare/fingerprint kernels because they are validation work, not executor invocations.

---

# 20. Artifacts

## 20.1 Run-local artifacts

```text
runs/<run_id>/
  preflight_receipt.json
  runtime_specification.json
  source_inventory.json
  source_identity.json
  canonical_schedule.json
  paired/
    epoch_0.json
    epoch_1.json
    epoch_2.json
    epoch_3.json
    epoch_4.json
    warmup_samples.json
    measured_samples.json
    paired_capture_bundle.json
    output_oracle_set.json
    paired_retirement_receipt.json
  isolated/
    reference/
      epoch_0/
      epoch_1/
      epoch_2/
      epoch_3/
      epoch_4/
      merged_capture_bundle.json
      requested_memory_receipt.json
      memory_plane_split_receipt.json
      shader_identity.json
      worker_runtime_artifact.json
      worker_local_manifest.json
    candidate/
      epoch_0/
      epoch_1/
      epoch_2/
      epoch_3/
      epoch_4/
      merged_capture_bundle.json
      requested_memory_receipt.json
      memory_plane_split_receipt.json
      shader_identity.json
      worker_runtime_artifact.json
      worker_local_manifest.json
  child_process_receipts.json
  per_cell_stage_statistics.json
  aggregate_stage_statistics.json
  order_bias_receipts.json
  epoch_bias_receipts.json
  co_residency_attribution.json
  requested_memory_comparison.json
  physical_memory_diagnostics.json
  shader_identity_stability.json
  numeric_parity_summary.json
  measurement_admissibility.json
  artifact_write_receipt.json
```

## 20.2 Canonical top-level artifacts

```text
workspace/runtime/attention/headwise/texture/
  ash_attn_headwise_texture_05_opt_baseline_01_r2_runtime_artifact.json
  ash_attn_headwise_texture_05_opt_baseline_01_r2_local_manifest.json
```

## 20.3 Atomic publication

All JSON is Rust-authored through:

```text
temporary sibling write
-> flush
-> atomic rename
-> readback
-> SHA-256 verification
```

Canonical top-level artifacts are written only after all physical evidence and R1 admissibility pass.

---

# 21. Rust-authored specification and manifest

## 21.1 Runtime specification

`runtime_specification.json` is generated after preflight and before physical execution. It records:

```text
patch/build revision
parent artifact paths and digests
source response-file digest
source-tree allowlist and digest
executable digest
model and adapter identity
canonical cell set
five-epoch route rotation
AB·BA blocks
warmup and measured counts
child launch plan
timestamp ownership plan
memory owner taxonomy
forbidden authority counters
output path map
```

## 21.2 Local manifest

The final local manifest binds:

```text
runtime specification digest
all run-local artifact digests
child process receipts
paired capture bundle
worker runtime artifacts
shader identities
requested-memory comparison
admissibility receipt
canonical runtime artifact digest
response-file digest
pass token
```

## 21.3 Packaging rule

The code-baked ZIP and overlay ZIP must exclude:

```text
Markdown specification files
runtime_specification.json
local manifest JSON
runtime artifacts
workspace/runtime
pre-generated measurement JSON
target
.git
```

CLI response files remain code-side execution contracts and may be included.

---

# 22. CLI contract

New response file:

```text
specs/cli/ash_attn_headwise_texture_05_opt_baseline_01_r2.args
```

Canonical keys:

```text
--repo-root
--expected-patch-id
--expected-build-revision
--texture05-source-response-file
--parent-r3-r2-runtime-artifact
--parent-r3-r3-r2-runtime-artifact
--parent-r4-runtime-artifact
--parent-r4-r1-runtime-artifact
--expected-model-instance-id
--profile-id
--measurement-epoch-count
--paired-warmup-pairs-per-cell-per-epoch
--paired-measured-pairs-per-cell-per-epoch
--isolated-warmup-per-cell-per-lane-per-epoch
--isolated-measured-per-cell-per-lane-per-epoch
--maximum-order-bias-ratio
--maximum-epoch-spread-ratio
--require-native-topology-preservation
--require-requested-memory-live-census
--require-runtime-shader-identity
--require-child-owner-zero
--forbid-external-input-json
--forbid-authority-mutation
--run-output-root
--canonical-runtime-artifact
--canonical-local-manifest
--optional-bake-archive-path
```

Canonical fixed values:

```text
profile-id                                    canonical
measurement-epoch-count                      5
paired-warmup-pairs-per-cell-per-epoch       1
paired-measured-pairs-per-cell-per-epoch     4
isolated-warmup-per-cell-per-lane/per-epoch  1
isolated-measured-per-cell/per-lane/per-epoch 2
maximum-order-bias-ratio                     0.10
maximum-epoch-spread-ratio                   0.15
forbid-external-input-json                   true
forbid-authority-mutation                    true
```

Unknown, duplicate and missing keys fail closed.

No digest placeholder requiring manual replacement is allowed.

---

# 23. Verification gate

New binary:

```text
ash_attn_headwise_texture_05_opt_baseline_01_r2_verification_gate
```

The verification gate uses an injected deterministic executor trait, not physical timing claims.

It verifies:

```text
physical executor extraction API
original Texture-05 gate regression adapter
five-epoch schedule cardinality
600 paired measured samples
AB/BA 10:10 per cell
BA deferred-compare order
one execution per executor per pair
no hidden rerun
paired owner-zero before child spawn
self-spawn parent/child protocol
five reference and five candidate child epochs
typed missing-parent localization
no external input JSON CLI keys
runtime source identity derivation
placeholder rejection
live-memory event to receipt conversion
reference/candidate owner-set comparison
child crash and timeout HOLD
shader identity drift HOLD
oracle fingerprint mismatch HOLD
R1 statistics reuse
R1 admissibility reuse
HOLD-before-canonical-publication
Rust-authored specification and manifest
ZIP exclusion static checks
```

Negative controls include:

```text
missing R4 parent
parent pass=false
BA silently executed as AB
candidate executed twice
candidate worker BufferAtlas dispatch count=1
reference worker Texture object count=1
unretired owner
pipeline creation during measured interval
shader digest drift after epoch 2
pre-existing run collision
external paired_capture_bundle CLI key
```

Verification PASS does not claim physical baseline PASS.

---

# 24. Physical completion gate

R2 physical PASS requires:

```text
Parent R3-R2 artifact verified                         PASS
Parent R3-R3-R2 artifact verified                     PASS
Parent R4 artifact verified                           PASS
Parent R4-R1 artifact verified                        PASS
Typed preflight                                       PASS
External required capture JSON count                     0
Canonical coverage cells                                30
Measurement epochs                                       5
Paired warmup pairs                                     150
Paired measured pairs                                   600
AB measured samples/cell                                 10
BA measured samples/cell                                 10
Paired reference executions                             750
Paired candidate executions                             750
Paired compare operations                               750
Hidden executor re-executions                             0
Reference child processes                                 5
Candidate child processes                                 5
Reference-only measured samples                         300
Candidate-only measured samples                         300
Reference worker Texture dispatches                       0
Candidate worker BufferAtlas dispatches                   0
Paired numeric mismatches                                 0
Isolated fingerprint mismatches                           0
Timestamp ownership mismatches                            0
Native topology mutations                                 0
Pipeline creations during measured intervals              0
Shader module creations during measured intervals         0
Shader identity drift events                              0
Requested-memory owner overlap violations                 0
Child post-retirement exclusive owners                     0
Paired post-retirement exclusive owners                    0
Per-cell order bias <= 0.10                             PASS
Per-cell epoch spread <= 0.15                           PASS
Candidate output commits                                  0
Candidate downstream consumers                            0
Route authority mutations                                 0
Output authority mutations                                0
Production executor switches                              0
TensorCube texture consumers                              0
Runtime specification Rust-authored                     PASS
Local manifest Rust-authored                            PASS
Artifact write and readback                             PASS
```

Physical-memory telemetry may be unsupported. Requested-memory live census remains mandatory.

---

# 25. Runtime artifact

Canonical runtime artifact schema:

```text
ash.attn.headwise.texture.05.opt_baseline_01_r2.runtime_artifact.v1
```

It records:

```text
physicalExecutionObserved=true
captureProducerPresent=true
externalInputJsonDependency=false
paired schedule and counts
child process counts and digests
reference/candidate shader identities
requested-memory comparison
physical-memory status
per-cell statistics digest
aggregate statistics
admissibility disposition
authority-zero counters
run-local artifact root
run identity digest
```

R2 PASS proves a physically produced baseline, not performance superiority.

---

# 26. Direct execution

Verification gate:

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_texture_05_opt_baseline_01_r2_verification_gate `
  -- "@specs/cli/ash_attn_headwise_texture_05_opt_baseline_01_r2_verification.args"
```

Physical producer gate:

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_texture_05_opt_baseline_01_r2_gate `
  -- "@specs/cli/ash_attn_headwise_texture_05_opt_baseline_01_r2.args"
```

The parent binary self-spawns child modes. No separate worker command is required.

Expected progress disclosure:

```text
[r2-preflight] parents/source/adapter/schedule/run-id
[r2-paired] epoch/cell/order/warmup-or-measured
[r2-retire] paired owner-zero
[r2-child] epoch/lane/pid/exit/artifact
[r2-memory] lane/shared/exclusive/peak/retired
[r2-identity] reference/candidate identity digests
[r2-statistics] ratio/order-bias/epoch-spread
[r2-disposition] admit or typed HOLD
```

---

# 27. PASS token

```text
PASS_ASH_ATTN_HEADWISE_TEXTURE_05_OPT_BASELINE_01_R2_PHYSICAL_CAPTURE_PRODUCER_EXISTING_EXECUTOR_REUSE_FIVE_EPOCH_AB_BA_REFERENCE_CANDIDATE_CHILD_LIVE_TIMESTAMP_MEMORY_CENSUS_RUNTIME_SHADER_IDENTITY_AUTO_SPAWN_TYPED_PREFLIGHT_NO_EXTERNAL_INPUT_RUST_SPEC_MANIFEST_SEALED
```

---

# 28. Follow-up boundary

After R2 physical PASS, the baseline becomes the immutable V0 parent of:

```text
ASH-ATTN-HEADWISE-TEXTURE-05-CANDIDATE-ACCUMULATE-01
```

Every optimization variant must preserve:

```text
same source fixture authority
same five-epoch schedule
same 30 cells
same AB·BA block
same isolated process protocol
same timestamp formulas
same memory owner taxonomy
same admissibility formulas
```

Only the candidate shader or explicitly declared executor variant identity may change.

R2 does not evaluate production performance policy. A separate benefit gate compares V0 and optimization variants.

---

# 29. Completion state

```text
OPT-BASELINE-01-R1
  CompileClosure        PASS
  VerificationGate      PASS
  PhysicalProducer      Missing
  PhysicalBaseline      Blocked

OPT-BASELINE-01-R2 after physical PASS
  CompileClosure        PASS
  VerificationGate      PASS
  PhysicalProducer      Bound
  PairedBaseline        Captured
  IsolatedBaseline      Captured
  RequestedMemory       LiveCensusBound
  ShaderIdentity        RuntimeDerived
  ExternalInputJSON     None
  PhysicalBaseline      Admitted

PerformanceBenefit      NotEvaluated
ResourceTradeoff        NotEvaluated
ProductionAuthority     HOLD
BufferAtlasV1            ProductionActive
KvTextureGqa4V1          ShadowOnly
```

R2 closes the empty middle of the graph. It does not ask the gate to believe that measurement JSON exists. It makes the same Rust process that owns the physical executors produce, verify and publish the measurement evidence itself.
