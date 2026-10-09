# HEADWISE-R3-CF3-PHYS-P0-B
## SELECTED SHORT32 / LONGGQA2_64 REAL WGPU OUTPUT PARITY + QUEUE/MAP/LIFETIME CLOSURE

**Class:** actual selected production WGPU dispatch, independent native reference, physical/finite/numerical observation  
**Parent:** `ASH_PASS3_HEADWISE_R3_CF4_CURRENT_SOURCE_HEAD_CHECKPOINT_LINEAGE_QUALITY_CODE_ONLY.zip`  
**Parent SHA-256:** `6f6ac28b6196104064893cbd81ac8bd2ef85d0c2e1d0ed2faef14c3a76bda01b`  
**Parent CF3:** `HEADWISE-R3-CF3 SELECTED PRODUCTION OUTPUT CANONICAL-REFERENCE QUALIFICATION` (SOURCE-baked)  
**P0-A dependency:** current-source identity can be consumed, but P0-A static PASS is **not** native physical proof  
**Status (2026-10-09): SOURCE runner implemented / STATIC 45/45 PASS, negative 30/30 rejected.** Rust COMPILE, Naga native, actual GPU Short32/Long64, Queue/Map and numerical parity are NOT_RUN. This SOURCE bake is *not* a PHYSICAL PASS; see exact SOURCE-bake annex.

```text
HEADWISE-R3-CF3-PHYS-P0-B

+ EXACT CF4 CODE/BINARY/SHADER SOURCE BINDING
+ NATIVE NAGA / WGPU26 PIPELINE CREATION
+ REAL SUBGROUP32 FEATURE + DEVICE/QUEUE CURRENTNESS
+ REAL SELECTED SHORT32 AND LONGGQA2_64 OUTPUT DISPATCH
+ REAL CF3 INDEPENDENT NATIVE SCALAR REFERENCE DISPATCH
+ SAME DEVICE / QUEUE / PREPARED Q/K/V / SCORE / CAUSAL INPUTS
+ 1023/1024 ACTUAL INCREMENTAL LUT BOUNDARY
+ CHUNKED SHORT ROUTE DISTINCT FROM INCREMENTAL LONG ROUTE
+ 16,384 F32 ELEMENT QUALIFICATION BUDGET
+ SENTINEL + 9-U32 COMPACT GPU STATUS ABI PRESERVATION
+ QUEUE CALLBACK + MAP CALLBACK + GPU MARKER INDEPENDENT TRUTH
+ RESOURCE COMPLETION BEFORE RETIREMENT
+ EXACT-F32 NUMERICAL CONTRACT, NO POST-HOC RELAXATION
+ SCOPED PER-FAMILY / PER-POLICY PHYSICAL RECEIPT
+ NO FAKE CHECKPOINT OR LIVE SESSION ADMISSION
+ NO DEFAULT-PRODUCTION OR AOF-CF5-D ACTIVE PROMOTION
```

---

## 0. Exact SOURCE baseline and limitation

The parent contains these real entry points:

```text
crates/burn_webgpu_backend/src/headwise_atlas.rs
  HeadwiseAtlasDispatcher::qualify_r3_cf3_selected_output(prepared, numerical_contract)
  HeadwiseAtlasDispatcher::encode_prepared_into_output_lease_with_route(...)
  HeadwiseAtlasDispatcher::observe_r3_family_topology(...)
  HeadwiseAtlasDispatcher::prepare_native_qkv_strict(...)
  HeadwiseAtlasDispatcher::prepare_raw_qkv_bqhd(...)

crates/burn_webgpu_backend/src/headwise_r3_cf3_matched_reference.rs
  validate_reference_prepared(...)
  encode_matched_reference(...)
  HeadwiseR3Cf3SelectedOutputReceipt

crates/burn_webgpu_backend/src/headwise_r3_cf1_selected_output.rs
  qualifier_owned_output(...)
  encode_selected_status(...)
  complete_selected_status(...)
```

CF3 SOURCE/STATIC previously passed `32/32`; that is **not** physical evidence. CF3's current code reports `kernel_fixture_only=true`, `live_session_qualified=false`, and `w8_w9a_physical_join_qualified=false`. Its `HeadwiseR3Cf3NumericalContract` has only `ExistingHeadwiseOutputParityExactF32`: `(atol=0, rtol=0, floor=f32::MIN_POSITIVE)`. The independent scalar three-pass softmax is not bitwise guaranteed equal to the selected subgroup/online-softmax reduction.

The existing CF3 path can internally return a receipt with `kernel_fixture_parity_qualified=true` for a successful bounded fixture. P0-B must prove that this exact path **actually ran on WGPU**, rather than accepting a fabricated JSON or source-only observation. No current production code cutover is implied.

## 1. Native preflight and exact invocation identity

Before every GPU campaign freeze:

```text
CF4 full ZIP SHA-256 and extracted source manifest
Cargo.lock SHA-256
current training-source digest (19-input): 0b10...c9cc1a41094
ark_runtime_source_digest() or UNKNOWN when model runtime not constructed
backend qualification source digest
executed binary SHA-256 (not the source digest)
selected Short32 and LongGqa2_64 WGSL digests
CF3 reference WGSL + CF1 status WGSL digests
route LUT digest
adapter/backend/device/queue currentness and requested features
fixture seed, generator version, exact Q/K/V data digests
score policy + TextDensity uniform digest
causal position snapshot/epoch + layout + shape
```

Use a unique, **execution-owned** invocation ID for the campaign and bind it to the actual encoder submission and completed receipt. A campaign nonce is for identity correlation, not a substitute for physical WGPU completion. If a native Buffer/Queue owner identifier is missing, report `UNKNOWN` and withhold any claim requiring that identity; do not manufacture an address hash.

No external historical checkpoint is required for *fixture-only* kernel qualification. A live checkpoint session is separately gated on CF4's real newly trained checkpoint and native loading.

## 2. Native Device/Queue and subgroup admission

Use actual WGPU26 runtime handles, preferably the existing `HeadwiseAtlasDispatcher::from_runtime_handles`. Do not assume `try_new_default()` is qualified: the current helper requests `Features::empty()`. The R3 subgroup probe requires the **requested** `wgpu::Features::SUBGROUP` capability on `device.features()`, and reads real subgroup widths.

Mandatory:

- Enumerate adapter feature support and device requested features, with exact backend/adapter identity when available.
- Request/validate `SUBGROUP` on the actual Device used by candidate, reference, and comparator.
- Execute `observe_r3_family_topology(Short32)` or `(LongGqa2_64)` on the **same dispatcher/Device/Queue** used for its selected output.
- Record configured workgroup sizes 32/64 separately from *GPU-observed subgroup width 32*. Never report an inferred GPU-observed workgroup size.
- Reject missing/incorrect subgroup features, failed shader creation, failed pipeline/bind group, mismatched queue, or failed topology callback.
- No CPU reference-only or unrelated proxy dispatch may satisfy the selected output proof.

## 3. Real family selection (exact active LUT)

The current incremental LUT is authoritative:

| seq_kv | selected route | family when its other conditions hold |
|---|---|---|
| `1..=1023` | `Subgroup32SingleQueryHeadV1` | `Short32` |
| `1024..=u32::MAX` | `Subgroup32Gqa2LongKvTiledV2` | `LongGqa2_64`, **only** for actual IncrementalDecode and `query_heads_per_kv == 8` |

The source constant `HEADWISE_ATLAS_LONG_KV_THRESHOLD = 1536` is tagged **legacy diagnostic**; it is **not** the current selected incremental LUT boundary. `head_dim=64` is required for the selected production cooperative kernels. Long family is selected with GQA=8 and the required parallel group layout.

For a **ChunkedDecode** causal route the current `encode_prepared_into_output_lease_with_route` chooses `Subgroup32SingleQueryHeadV1` through a forced-probe receipt even when seq_kv is long. Do not label a chunked selected invocation `LongGqa2_64` based only on KV length. Distinguish `forced_probe_route` from actual LUT selection.

Candidate must be the real selected shader:

```text
Short32  -> shaders/headwise_atlas_attention_production_rw.wgsl
Long64   -> shaders/headwise_atlas_attention_production_long_kv_optimized_v2.wgsl
```

Bind selected kernel ID, route receipt digest, route policy, shader bytes, dispatched `[x,y,z]`, `score_policy_id`, and actual Q/K/V inputs. Do not substitute the legacy long-v1 source or a standalone topology shader.

## 4. Fixture input generation without invented live identity

Prepare two classes, separately labelled:

1. **`KernelFixtureGpuInput`**: deterministic, bounded CPU-generated Q/K/V may be uploaded **once to actual GPU buffers for fixture setup**. That input H2D is counted as fixture setup, not misreported as production zero-H2D. Use real `RawWgpuBufferLease` ownership and `prepare_raw_qkv_bqhd` where appropriate. This class never claims the Q/K/V came from a real model checkpoint.
2. **`NativeModelPreparedInput`**: use the real strict `prepare_native_qkv_strict` from the model-owned inference path and its actual same Device/Queue and zero-copy lease. This class is **HOLD** until valid checkpoint provenance and actual native model session are observed.

Both classes require actual GPU buffer identity, valid BQHD/BHQD shape and byte stride, non-overlapping candidate/reference outputs, and the exact same borrowed `PreparedAtlasInputs` for both producers. No re-running the model to produce a superficially matching second Q/K/V. No D2H readback of full Q/K/V to construct the reference.

The positive fixture must contain nondegenerate, distinct K and V for different KV heads, an asymmetric position tail, and a nonneutral TextDensity uniform for legacy policy tests. An all-zero, identical-head, or uniform-V fixture is insufficient to establish GQA, causal or score-policy sensitivity.

## 5. Independent reference producer and semantic parity

Use `encode_matched_reference()` with the actual CF3 WGSL scalar three-pass softmax. It is distinct from the production shader; preserve this independence.

**Canonical GQA:**

```text
score = dot(Q,K) / sqrt(head_dim)
context = softmax(causally masked score) @ V
```

**Legacy TextDensityAdjusted:** same Q/K/V and causal visibility, plus the selected score multiplier/clamp semantics and uniform identity. Do not compare Canonical GQA candidate to Legacy reference, or claim a mismatch between different policies is kernel error.

The reference and candidate must match:

```text
batch / q_heads / kv_heads / query_heads_per_kv
seq_q / seq_kv / head_dim=64
Q/K/V layout and raw buffer spans
per-query absolute causal positions and position_epoch
route_id (IncrementalDecode / ChunkedDecode)
GQA q_head -> kv_head mapping
score policy, TextDensity bytes, checked scale
finite-row/softmax semantics
```

Use `HeadwiseCausalPositionSnapshot::visible_count_for_query()` as host admission authority; the independent shader must implement the same domain. Reject zero-visible or stale/mismatched position snapshots at preflight. Verify K and V hidden tails separately; no `capacity == visible_length` substitution when those are distinct.

## 6. Real GPU encoder/submission ordering

Preserve one qualification-owned invocation, encoded in this order:

```text
exact PreparedAtlasInputs validation
      ↓
reference scalar producer dispatch into qualifier-owned buffer
      ↓
actual selected Short32/Long64 production dispatch into different qualifier-owned buffer
      ↓
CF1 GPU finite/sentinel/numerical comparator
      ↓
copy 9*u32 compact status to MAP_READ staging
      ↓
Queue::submit(encoder.finish())
      ↓
Queue::on_submitted_work_done callback
      + map_async(MAP_READ) callback
      ↓
PollType::Wait / callback-result validation
      ↓
validate GPU marker + actual status words
      ↓
unmap, retire staging/reference/candidate only after proven completion
      ↓
seal scoped receipt (no canonical publication)
```

The current `complete_selected_status()` is a concrete starting point. The queue callback, map callback, marker, and actual buffer retirement must be **distinct fields with real observation sources**. A successful marker does not substitute for callback completion. The source-defined `finished(true)` flag is admissible only after the just-completed native call has truly proved the required callback/map states; cannot be set by the CLI itself without that native observation.

Do not add this MAP_READ / Wait to normal token decode. The fixture is a distinct qualification-only campaign.

## 7. Bounded comparator ABI and exact numerical policy

Preserve:

```text
MAX_FIXTURE_ELEMENTS = 16_384 f32
OUTPUT_SENTINEL = 0x7fc00001
STATUS_MARKER = 0xC315ECF1
STATUS_BYTES = 9*u32 = 36
```

Map the source's real 9 words:

| Word | Meaning |
|---|---|
| 0 | observed element visits |
| 1 | output sentinel / unwritten count |
| 2 | **aggregated** nonfinite count; do not invent disjoint classes |
| 3 | numerical mismatch count |
| 4 | first mismatch index (`u32::MAX` means none) |
| 5 | max absolute error bits |
| 6 | max relative error bits |
| 7 | completion marker |
| 8 | expected logical element count |

Admission requires every expected element visited, no sentinel, no aggregated nonfinite, no numerical mismatches, no first mismatch, finite comparison metrics, correct marker and physical completion.

Current numerical contract: `ExistingHeadwiseOutputParityExactF32`, with `atol=0`, `rtol=0`, `relative_floor=f32::MIN_POSITIVE`. Its identity and exact values must be frozen **before** executing the fixture. If a scalar reference and subgroup/online-softmax producer disagree solely because of reduction order, report **measured exact-f32 drift and HOLD numeric qualification**. Do not reinterpret this as arbitrary numerical tolerance PASS, nor assert that production is wrong without attribution. Any new tolerance envelope belongs to a separately authorized numerical policy revision, not an after-the-fact CLI flag.

Reject nonfinite candidate/reference values, subtraction/relative-error overflow, and overflowing allowed-tolerance calculation. The current status WGSL checks each of those as an aggregated nonfinite failure domain.

## 8. Required physical coverage

Predeclare an exact manifest for each supported route. These are **candidate targets**, not claimed completed runs:

| Axis | Required matrix |
|---|---|
| Family | Real Short32 and real LongGqa2_64 selected output |
| Incremental KV | `1`, `31`, `32`, `33`, `1023`, `1024`, `1025`, `1535`, `1536`, `1537`, `2048` where limits permit |
| Chunked visibility | `seq_q=2/3/4` under actual ChunkedDecode, **Short32** selected family; no fabricated chunked Long64 |
| Score policies | `CanonicalGqa`, `LegacyTextDensityAdjusted`, distinct runs |
| Layout | Actual Bhqd and Bqhd supported APIs, with explicit lease ownership |
| Head geometry | Actual GQA 8-to-1 for selected long route; applicable short GQA variations only with route admission |
| Position | Initial, nonzero base, u64 low-word carry, stale epoch negative |
| Content | Nonuniform heads, near-tie scores, high-sensitivity tail, exact zero & tiny magnitude cases |
| Resource | Ordinary completion, status mismatch, stale generation, wrong owner/Queue, missing callback, duplicate/early retirement |

The reference validates q_elements <=16,384 but does **not** imply a <=16,384 bound on KV input element count; validate WGPU physical storage limits and exact input byte bounds separately. For unsupported geometry or device limits record the case as `HOLD_REFERENCE_COVERAGE` / `NOT_APPLICABLE` only with exact evidence; do not silently drop a mandatory family.

Do not use `HEADWISE_ATLAS_LONG_KV_THRESHOLD=1536` to determine the actual `1023/1024` dispatch boundary. A matched `1023/1024` crossing is an essential positive/negative route test.

## 9. Negative runtime / static matrix

| Case | Failure classification |
|---|---|
| Wrong selected shader or forced route presented as natural LUT selection | `SELECTED_ROUTE_DRIFT` |
| Short32 receipt borrowed for Long64 | `FAMILY_PROVENANCE_DRIFT` |
| Score policy or TextDensity swapped after preflight | `REFERENCE_POLICY_MISMATCH` |
| Q/K/V alias or output overlaps source | `QKV_LEASE_ALIAS` |
| Q/K/V from second model invocation | `QKV_INVOCATION_DRIFT` |
| Incorrect causal snapshot, epoch or high-word carry | `CAUSAL_POSITION_DRIFT` |
| Incorrect KV mapping / wrong GQA grouping | `GQA_MAPPING_DRIFT` |
| Unwritten output remains sentinel | `OUTPUT_UNWRITTEN` |
| Candidate/reference or arithmetic nonfinite | `NONFINITE_OUTPUT_OR_COMPARISON` |
| Status marker missing / count incorrect | `GPU_STATUS_INVALID` |
| Callback absent, map failed, poll failed or device lost | `GPU_COMPLETION_UNQUALIFIED` |
| Staging/reference/candidate returned before completion | `PRECOMPLETION_RESOURCE_REUSE` |
| Matching caller-provided receipt JSON without native invocation | `FORGED_PHYSICAL_RECEIPT` |
| 1-bit perturbation in output/reference | GPU mismatch if executed; static mutation alone only STATIC |
| Mixed historical head checkpoint / CF4 current source | `CHECKPOINT_LINEAGE_DRIFT` |
| AOF CF5-D ACTIVE or normal per-token Wait added | `EARLY_PRODUCTION_PROMOTION` |

For device-loss/missing-callback tests that cannot be safely and deterministically induced on the available hardware, explicitly report `NOT_EXECUTED`; do not fabricate completion or silently classify PASS.

## 10. Native runner and source touch points

**Preferred narrow implementation:** use an opt-in native qualification command linked to existing backend APIs, with no production default branch rewrite.

Existing code owners:

```text
crates/burn_webgpu_backend/src/headwise_atlas.rs
crates/burn_webgpu_backend/src/headwise_r3_cf3_matched_reference.rs
crates/burn_webgpu_backend/src/headwise_r3_cf1_selected_output.rs
crates/burn_webgpu_backend/src/headwise_r3_subgroup_admission.rs
crates/burn_webgpu_backend/src/headwise_route_lut.rs
crates/burn_webgpu_backend/src/headwise_causal.rs
crates/model_core/src/aof_r1_admission.rs
```

Potential **new**, proposed files (not present in CF4 parent):

```text
crates/orchestrator_local/src/bin/ash_headwise_r3_cf3_physical_gate.rs
crates/orchestrator_local/src/headwise_r3_cf3_physical_campaign.rs
tools/validate_ash_headwise_r3_cf3_p0b_physical_static.py
```

Register a new bin only if it actually exists, using the existing `orchestrator_aof_r1_audit_bins` feature or the least permissive existing audit feature applicable. Reuse backend-owned shader, buffer, and numerical-comparison APIs. Do not introduce an unrelated CPU reference or clone an independent production shader under a misleading name.

If the runner adds a new WGSL file or edits CF3 WGSL, update `ark_runtime_source_digest()` and the backend qualification digest with **actual source bytes**. Do not change the 19-input head training files. Any unavoidable training-input change means a new training lineage and blocks current-checkpoint claims until separately qualified.

## 11. Strict campaign schema / receipt SSOT

Proposed input: `headwise_r3_cf3_p0b_physical_campaign.json`  
Proposed per-fixture output: `headwise_r3_cf3_p0b_selected_output_physical_receipt.json`

```text
schema_version
parent_zip_sha256 / parent_source_tree_digest
Cargo.lock_sha256 / binary_sha256 / backend_source_digest
model_runtime_source_digest: None for fixture-only; genuine digest for live
kernel_fixture_only=true/false
actual_device_queue_identity: optional, only from native owner
adapter_features / device_requested_features
selected_family / selected_kernel_id / shader_sha256 / route_lut_digest
route_selection_kind: NaturalIncrementalLut | ChunkedForcedShort
selected_workgroup_size / gpu_observed_subgroup_widths
Q/K/V fixture_seed / hashes / owner+generation if known
shape / layout / buffer offsets / stride / bounded byte sizes
score_policy / TextDensity_digest / causal_snapshot_digest
reference_producer_receipt_sha256 / reference_shader_sha256
numerical_contract_id / exact tolerance bits
expected_elements / observed_elements / sentinel / aggregated_nonfinite
numeric_mismatch_count / first_mismatch / max_abs / max_rel
queue_submit_count / queue_callback / map_callback / status_marker
resource_retirement_verified / status_D2H_bytes / full_context_readback_count
stage_wall_ns / kernel_gpu_time_ns: null without actual timestamp-query source
fixture_physical_status / fixture_numerical_status
checkpoint_lineage_status: NOT_EVALUATED for fixture-only
w8_w9a_physical_status: HOLD
general_production_promoted=false / cf5_d_active=false
first_failure_stage / first_failure_code / receipt_sha256
```

The output JSON is a **durable audit receipt only**. No disk JSON shall be converted into a reusable live pointer/lease permit.

Separate aggregate documents for Short32 and Long64, and a final matrix coverage summary that lists **every planned case** and its real PASS, FAIL, HOLD, or NOT_RUN state. No unbounded per-element host logs.

## 12. SOURCE / COMPILE / NAGA / PHYSICAL acceptance

**SOURCE / STATIC**, on the exact parent and new implementation:

```powershell
python .\tools\validate_ash_headwise_r3_cf3_selected_reference_static.py --negative-tests
python .\tools\validate_ash_headwise_r3_cf4_checkpoint_lineage_static.py --negative-tests

# Only after the proposed verifier exists:
python .\tools\validate_ash_headwise_r3_cf3_p0b_physical_static.py --negative-tests
```

**COMPILE and existing regression:**

```powershell
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p orchestrator_local --lib --release --locked -j 1
cargo test -p burn_webgpu_backend --lib headwise_r3_cf3 --release --locked -j 1
```

If the proposed new native CLI is baked:

```powershell
cargo build -p orchestrator_local --bin ash_headwise_r3_cf3_physical_gate `
  --features orchestrator_aof_r1_audit_bins --release --locked -j 1

# Syntax is proposed and must be implemented before invocation:
.\target\release\ash_headwise_r3_cf3_physical_gate.exe `
  --campaign .\workspace\headwise_r3_cf3_p0b_physical_campaign.json
```

Run native Naga26 parse/validate over the exact **four production/reference/comparator WGSL files** (selected short, selected long, independent reference, status comparator), plus the R3 subgroup-probe shader, and actual WGPU shader-module/pipeline/bind-group creation and dispatch. Rust `cargo check` is not Naga or GPU evidence. The repository has an existing WGPU26/Naga corpus qualification bin; use its exact actual CLI flags discovered from source, not invented aliases.

If the external `vendor/sherpa-rs-main/crates/sherpa-rs` path is absent in the code-only checkout, restore the legitimate dependency. Never create a dummy replacement or quietly alter version constraints to make metadata pass.

**PHYSICAL:** run the declared fixture matrix on an actual GPU whose requested subgroup features and limits satisfy the selected families; observe true queue completion, map callback, GPU status and resource retirement. Finish with a fixed input-shape/score/causal reference parity receipt.

## 13. Scoped PASS / HOLD semantics

A single case may distinguish:

```text
SourceBound
NativePipelineCreated
ActualSelectedDispatched
QueueAndMapCompleted
NumericExactPass
NumericExactFail
PhysicalUnavailable
```

A **family-scoped** physical/numerical PASS may be emitted only when **all applicable mandatory fixture cases in that family** have true physical completion and exact-f32 parity under their frozen policy. A smaller successful subset emits a **case-scoped PASS**, not the all-family token.

Conditional target tokens (not currently issued):

```text
PASS_HEADWISE_R3_CF3_P0B_SHORT32_SELECTED_OUTPUT_PHYSICAL
PASS_HEADWISE_R3_CF3_P0B_LONGGQA2_64_SELECTED_OUTPUT_PHYSICAL
PASS_HEADWISE_R3_CF3_P0B_SELECTED_OUTPUT_MATRIX_PHYSICAL
```

`HEADWISE-R3-CF3-PHYS-P0-B` may report real `PHYSICAL_COMPLETED_NUMERICAL_HOLD` when callbacks and retirement passed but exact scalar/subgroup numerical parity failed. This truth must not be labeled either numerical PASS or hardware crash.

No matter the fixture result, the following stay independent:

```text
CF4 current-source newly trained head checkpoint and native load
CF2 original W8/W9A same-invocation physical join
AOF CF5-C native Headwise/TensorCube capacity-strided consumer
Headwise RequireSelectedProductionOutput global production default
AOF CF5-D ACTIVE
```

## 14. Performance accounting (non-promoting)

Capture independently where available:

```text
fixture setup Q/K/V H2D bytes
reference/candidate/status dispatch counts
pipeline creation/cache hit counts
qualification-only Queue submissions
36-byte status D2H + topology-probe readback
queue wait wall / map wall / total qualification wall
actual timestamp-query GPU times ONLY if supported, requested and captured
peak transient candidate/reference/staging memory
```

Do **not** attribute fixture extra work to normal decode steady state; do not claim wall-time speedup or KV residency improvement without separate A/B. No global per-token map/wait/CPU reference is allowed.

## 15. Completion law

```text
EXACT CF4 SOURCE / BINARY / WGPU FEATURES
+ REAL SHORT32 / LONGGQA2_64 ROUTE SELECTION
+ SAME PREPARED GPU Q/K/V
+ INDEPENDENT POLICY-MATCHED SCALAR REFERENCE
+ ACTUAL SELECTED WGPU DISPATCH
+ BOUNDED SENTINEL / FINITE / EXACT-NUMERICAL COMPARISON
+ PHYSICAL QUEUE + MAP + STATUS MARKER OBSERVATION
+ COMPLETION-ORDERED RESOURCE RETIREMENT
+ COMPLETE APPLICABLE MATRIX, NO FAKE COVERAGE
= SCOPED CF3 SELECTED OUTPUT PHYSICAL QUALIFICATION

NOT = trained head checkpoint proof
NOT = W8/W9A same-invocation GPU proof
NOT = general production cutover
NOT = AOF capacity-strided consumer proof
NOT = CF5-D ACTIVE
NOT = performance promotion
```

All mandatory unobserved fields remain `None`, `UNKNOWN`, or `NOT_RUN`. If a mandatory case is unavailable or numerical policy is insufficient, the aggregate status is **HOLD**, not an invented PASS. No code or hardware outcome is claimed by this specification.

---

## 16. SOURCE bake evidence annex (2026-10-09)

**Evidence tier:** Native WGPU runner SOURCE implemented / STATIC only. This annex supersedes the initial SPECIFICATION ONLY status above. No successful Rust/Naga build or physical Short32/Long64 execution is claimed.

### Artifacts (ZIP SHA-256 / entries / CRC)

| Artifact | SHA-256 | Entries | CRC |
|---|---|---:|---|
| P0-A Full parent | `eba90c54dada1f6138ca51401e4aad2e1611791cb660e8ad767dd01d8c32d96b` | 8,757 | PASS |
| P0-B Overlay | `534c3eedcd99d09867b8da677c3f593a529d62bfbebc22189575e18a3cb69249` | 5 | PASS |
| P0-B Full (P0-A + P0-B) | `0bbc0bfbc2f26e8c43c988bb2bc251a865afceb9e02ab0fab6e5e057acf5b808` | 8,761 | PASS |

### Exact changed files

- `MOD crates/orchestrator_local/Cargo.toml` (opt-in audit binary)
- `ADD crates/orchestrator_local/src/headwise_r3_cf3_p0b_physical.rs`
- `ADD crates/orchestrator_local/src/bin/ash_headwise_r3_cf3_physical_gate.rs`
- `ADD tools/fixtures/headwise_r3_cf3_p0b_campaign.json`
- `ADD tools/validate_ash_headwise_r3_cf3_p0b_physical_static.py`

### Verified and missing evidence

```text
P0-B                       STATIC 45/45 PASS; negative 30/30 rejected
P0-A                       STATIC 60/60 PASS; negative 25/25 rejected
Headwise R3-CF2/CF3/CF4    STATIC 41/41, 32/32, 35/35 PASS
19-input training digest   0b10d1d645ce22356ca4c44bc9e0e4c4ef109f6daf9d143175cd5c9cc1a41094
Campaign positive fixtures 28 SOURCE-defined, NOT_RUN
RUST COMPILE / NAGA        NOT_RUN
GPU Short32 / Long64      NOT_RUN
Queue/Map / Numeric        NOT_RUN
Device-loss negatives     NOT_RUN
Live head checkpoint      NOT_PROVIDED
Global physical PASS      HOLD
CF5-D ACTIVE              false
```

The opt-in runner is designed to request `SUBGROUP`, upload fixture-only Q/K/V, invoke the existing selected Short32/Long64 + independent CF3 reference, and write separate Queue/Map/numeric receipts. It freezes exact-f32 tolerance and the 1023/1024 route boundary. Only pre-dispatch negative admission cases are SOURCE-implemented; the complete device-loss/callback/live-session negative matrix is **not** physically executed. No default decode, canonical KV, token, stop or emit behavior changes. The GitHub commit contains this specification only, not the code-only ZIP.
