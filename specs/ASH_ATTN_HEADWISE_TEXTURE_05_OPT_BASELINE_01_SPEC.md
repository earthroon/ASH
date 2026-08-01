# ASH-ATTN-HEADWISE-TEXTURE-05-OPT-BASELINE-01

## Matched BufferAtlas·Texture Timing /
## AB·BA Order Balance /
## Candidate-Only·Reference-Only Isolation /
## Per-Cell Stage Ratio /
## Requested·Physical Memory Plane Split /
## Shader Variant Identity Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-05-OPT-BASELINE-01`  
> Build revision: `HEADWISE-TEXTURE-05-OPT-BASELINE-01-matched-isolated-baseline-v1`  
> Parents: `R3-R2`, `R3-R3-R2`, `R4`, `R4-R1`  
> Production executor: `BufferAtlasV1` unchanged  
> Candidate executor: `KvTextureGqa4V1` shadow evidence only  
> Production output authority: `HeadwiseFullActive` unchanged  
> Patch-local readiness: `MatchedExecutorOptimizationBaselineBound`  
> Production promotion claim: forbidden

---

# 0. Purpose

Texture-05 already has shadow-safety, persistent-residency, packetization and stage-attribution evidence. The current R4 ratio is not yet a production-grade optimization baseline because BufferAtlas and Texture are observed in one fixed order, both resource families are co-resident, isolated executor runs are absent, and every sample is not bound to one immutable shader/pipeline identity.

This patch creates the canonical pre-optimization V0 baseline.

```text
parent artifact verification
-> immutable experiment identity
-> five measurement epochs
-> balanced AB·BA paired execution
-> reference-only child process
-> candidate-only child process
-> per-cell and aggregate statistics
-> requested-memory owner ledger
-> optional physical-memory diagnostics
-> measurement admissibility
-> Rust-authored runtime specification, artifacts and manifest
```

It measures. It does not optimize, promote, reroute or relax existing gates.

---

# 1. Canonical geometry

```text
batch                       1
Q heads                    32
K/V heads                   4
head dimension             64
page tokens               128
model layers               22
KV representatives         64, 192, 384, 768, 1280, 1792
route/query shapes          Q1 incremental, Q2/Q6/Q12/Q24 chunked
coverage cells             30
```

The existing coverage-cell canonical ID remains authoritative. A second taxonomy is forbidden.

---

# 2. Canonical measurement profile

```text
measurement epochs                              5
paired measured pairs/cell/epoch                4
paired measured pairs/cell                     20
AB samples/cell                                10
BA samples/cell                                10
paired samples total                          600
reference-only samples/cell                    10
candidate-only samples/cell                    10
reference-only samples total                  300
candidate-only samples total                  300
measured executor invocations total         1,800
```

Warmup observations are diagnostic-only and excluded from canonical statistics. Smoke mode cannot write canonical admitted artifacts.

Within each KV bucket, route order rotates across epochs:

```text
E0 Q1,Q2,Q6,Q12,Q24
E1 Q2,Q6,Q12,Q24,Q1
E2 Q6,Q12,Q24,Q1,Q2
E3 Q12,Q24,Q1,Q2,Q6
E4 Q24,Q1,Q2,Q6,Q12
```

KV order remains monotonic. Texture shrink or silent full repopulation is forbidden.

---

# 3. Matched invocation identity

Every paired sample binds:

```text
model instance
decode session and epoch
coverage cell
pair ordinal
production and texture generation
Q/K/V lease digests
causal snapshot digest
geometry digest
invocation seed digest
```

BufferAtlas and Texture consume the same immutable Q/K/V and causal geometry, write separate private outputs, and cannot consume one another's output.

---

# 4. AB·BA balance

```text
A = BufferAtlasV1
B = KvTextureGqa4V1
```

Even epochs:

```text
AB, BA, BA, AB
```

Odd epochs:

```text
BA, AB, AB, BA
```

Across five epochs, every cell has exactly ten AB and ten BA samples. A missing sample invalidates the cell. End-of-run replacement samples are forbidden.

Each executor keeps its native command topology. No new fused comparison executor is admitted. Between the first and second executor in one pair there is no K/V mutation, texture generation publication, append, manual GC, shader replacement, pipeline creation or route mutation.

---

# 5. Timing authority

Primary GPU spans:

```text
reference_executor_gpu_ns = BufferAtlas reference stage
candidate_executor_gpu_ns = Texture accumulate + normalize
candidate/reference ratio = candidate_executor_gpu_ns / reference_executor_gpu_ns
```

Capture, compare, compact-copy, timestamp resolve, map wait, GC and scheduler work are disclosed separately and excluded from the primary ratio.

GPU clock and host clock remain separate domains. Queue span and host poll time are never summed as independent work.

Per-cell statistics:

```text
paired sample count
AB and BA counts
reference p50/p95/max
candidate p50/p95/max
ratio p50/p95/max
AB median
BA median
order-bias ratio
five epoch medians
epoch-spread ratio
reference-only p50/p95/max
candidate-only p50/p95/max
isolated ratio
co-residency ratios
numeric and shader mismatch counts
```

Per-cell p99 is not an independent authority because twenty observations make nearest-rank p99 equal max. Aggregate p99 is computed across six hundred paired samples.

Order bias:

```text
L_AB = median(ln(candidate/reference) for AB)
L_BA = median(ln(candidate/reference) for BA)
order_bias_ratio = exp(abs(L_AB - L_BA)) - 1
```

Epoch spread:

```text
epoch_spread_ratio = max(epoch median) / min(epoch median) - 1
```

Measurement-quality ceilings:

```text
maximum order bias   0.10
maximum epoch spread 0.15
```

These are measurement-admissibility limits, not production-performance policy.

---

# 6. Isolated executor lanes

Reference-only and candidate-only lanes run in separate child processes. Process reuse between lane kinds is forbidden.

Reference-only:

```text
BufferAtlas admitted
Texture residency registry absent
Texture object creation 0
Texture dispatch 0
```

Candidate-only:

```text
Texture residency admitted
Texture execution admitted
BufferAtlas dispatch 0
candidate output private
production output commit 0
```

Candidate-only numeric validation compares against a previously sealed reference-output digest outside the timed executor span.

The parent verifies job digest, executable digest, source-tree digest, shader identity, model/adapter identity, owner-zero exit and artifact readback digest.

---

# 7. Requested and physical memory planes

Rust-requested memory classes:

```text
DeviceShared
ModelShared
ReferenceExclusive
CandidateExclusive
HarnessOnly
```

No allocation may appear in two exclusive classes.

Required values:

```text
process baseline requested bytes
shared requested bytes
executor-exclusive persistent bytes
executor-exclusive peak transient bytes
harness-only peak bytes
executor-exclusive peak bytes
post-retirement live bytes
unretired resource IDs
```

Comparable replacement deltas are admitted only when reference and candidate shared-owner-set digests match. Borrowed bytes remain physically present and cannot be reported as removed.

Physical/driver memory is diagnostic-only. Supported statuses:

```text
available
unsupported
permission_denied
sampling_failed
cross_source_inconsistent
```

Unsupported physical telemetry does not invalidate requested-memory evidence, but it sets `physical_memory_claim_admitted=false`. Driver memory never becomes Rust owner-lifetime authority.

---

# 8. Shader variant identity

Every measured sample binds:

```text
variant ID
executor kind
source-tree digest
executable digest
Rust module digests
WGSL source digests
bind-group and pipeline-layout digests
specialization constants
texture format
entry points
compiler-feature digest
wgpu backend
adapter and driver identity
```

V0 identities:

```text
buffer_atlas_v1_baseline
kv_texture_gqa4_v1_scalar_rgba4_baseline
```

Required closure:

```text
one identity/executor across all epochs
paired and isolated identity equality
pipeline creation delta during measurement 0
shader module creation delta during measurement 0
hot reload 0
fallback shader 0
```

Identity drift invalidates the complete baseline. Partial cross-variant aggregation is forbidden.

---

# 9. Runtime-generated specification and manifest

The code archive contains no Markdown specification and no prebuilt specification manifest.

The physical Rust gate generates after input verification:

```text
workspace/runtime/attention/headwise/texture/05/opt_baseline_01/runtime_specification.json
workspace/runtime/attention/headwise/texture/ash_attn_headwise_texture_05_opt_baseline_01_runtime_artifact.json
workspace/runtime/attention/headwise/texture/ash_attn_headwise_texture_05_opt_baseline_01_local_manifest.json
```

`runtime_specification.json` binds canonical counts, budgets, authority prohibitions, generator binary and schema. The local manifest binds the generated specification SHA-256, runtime artifact SHA-256 and all source-input digests.

All Rust-authored outputs use temporary sibling write, flush, atomic rename, readback and SHA-256 verification.

On HOLD, diagnostics may be written, but canonical admitted runtime artifact and local manifest remain absent or byte-identical.

---

# 10. Required Rust modules

```text
crates/burn_webgpu_backend/src/
  headwise_texture_05_opt_baseline_timing.rs
  headwise_texture_05_opt_baseline_memory.rs
  headwise_texture_05_opt_baseline_identity.rs
  headwise_texture_05_opt_baseline_capture.rs

crates/model_core/src/
  headwise_texture_05_opt_baseline.rs

crates/orchestrator_local/src/
  headwise_texture_05_opt_baseline_01_artifact.rs
  headwise_texture_05_opt_baseline_01_cli_registry.rs

crates/orchestrator_local/src/bin/
  ash_attn_headwise_texture_05_opt_baseline_01_gate.rs
  ash_attn_headwise_texture_05_opt_baseline_01_worker.rs
  ash_attn_headwise_texture_05_opt_baseline_01_verification_gate.rs
```

The bake ZIP may contain response files under `specs/cli`, but contains no `.md`, no filename containing `manifest`, no `workspace/runtime`, no `target`, and no `.git` content.

---

# 11. Admissibility predicates

Canonical order:

```text
ParentArtifactsVerified
CanonicalProfileSelected
CoverageComplete
EpochScheduleComplete
PairedSampleCardinalityExact
PairOrderBalanceExact
IsolatedSampleCardinalityExact
MatchedInvocationIdentityPass
NumericParityPass
TimestampIntegrityPass
NativeTopologyPreserved
ShaderIdentityStable
PipelineWarmStateStable
RequestedMemoryEvidenceComplete
IsolatedWorkerOwnerZero
OrderBiasWithinBudget
EpochSpreadWithinBudget
AuthorityPreservationPass
ArtifactWriteAndReadbackPass
```

All true yields `Admit`; otherwise `Hold` with ordered false-predicate IDs.

Admit proves only that the V0 optimization baseline is matched, balanced, isolated, memory-plane-separated and identity-sealed. It does not prove Texture is faster, uses less physical memory, should become production authority, or that a specific optimization cause has been localized.

---

# 12. Authority preservation

Required zero counters:

```text
candidate output commits
candidate downstream consumers
route authority mutations
output authority mutations
physical executor switches
production token-history mutations
TensorCube texture consumers
```

BufferAtlas remains production-active. Texture remains shadow-only. Performance benefit and resource tradeoff remain unevaluated by this patch.

---

# 13. Completion gate

```text
parents R3-R2/R3-R3-R2/R4/R4-R1 verified
coverage cells 30
epochs 5
paired samples 600
AB/cell 10
BA/cell 10
reference-only 300
candidate-only 300
missing/replacement samples 0
matched identity mismatch 0
numeric mismatch 0
timestamp ownership mismatch 0
native topology mutation 0
pipeline creation during measured interval 0
shader creation during measured interval 0
shader identity drift 0
exclusive-owner overlap violation 0
isolated worker retained owners 0
order bias <= 0.10
epoch spread <= 0.15
authority counters all 0
artifact readback PASS
```

PASS token:

```text
PASS_ASH_ATTN_HEADWISE_TEXTURE_05_OPT_BASELINE_01_MATCHED_BUFFERATLAS_TEXTURE_TIMING_AB_BA_ORDER_BALANCE_CANDIDATE_REFERENCE_ISOLATION_PER_CELL_STAGE_RATIO_REQUESTED_PHYSICAL_MEMORY_PLANE_SPLIT_SHADER_VARIANT_IDENTITY_SEALED
```

---

# 14. Direct execution

Verification gate:

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_texture_05_opt_baseline_01_verification_gate `
  -- "@specs/cli/ash_attn_headwise_texture_05_opt_baseline_01_verification.args"
```

Physical gate:

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_texture_05_opt_baseline_01_gate `
  -- "@specs/cli/ash_attn_headwise_texture_05_opt_baseline_01.args"
```

---

# 15. Follow-up

An admitted V0 baseline becomes the immutable parent of:

```text
ASH-ATTN-HEADWISE-TEXTURE-05-CANDIDATE-ACCUMULATE-01

RGBA4 Single-Texel Load /
Ordered Four-Component FMA /
Workgroup Q Vec4 Cache /
Tile Token Page·Layer Cache /
Vec4 V Accumulation /
Scalar Oracle Reverse Shadow /
First-Cause Contribution Receipt Seal
```

All optimization variants must reuse the exact coverage, epoch schedule, AB·BA schedule, isolated-lane schedule, memory taxonomy and statistical formulas. Only executor/shader variant identity may change.