# ASH-ATTN-HEADWISE-TEXTURE-04

## Texture GQA4 Live Shadow Dispatch /
## BufferAtlas·KvTexture Dual Execution /
## Production KV Generation Consumption /
## Device-Guarded Output Parity /
## No Candidate Output Commit Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-04`  
> Build revision: `HEADWISE-TEXTURE-04-live-shadow-dispatch-v1`  
> Parent: `ASH-ATTN-HEADWISE-TEXTURE-03` PASS  
> Canonical local source SHA-256: `cbe9dfa8be758b4df6d82a7a090f165fb1dd91b23953ed1f0460e5588dd37c7d`  
> Canonical local source lines: `1528`  
> Canonical local source bytes: `36280`  
> Active executor: `BufferAtlasV1` unchanged  
> Candidate executor: `KvTextureGqa4V1`  
> Parent readiness: `IncrementalAppendParityBound`  
> Target readiness: `LiveShadowParityBound`  
> Output authority: `HeadwiseFullActive` unchanged

---

# 0. Purpose

TEXTURE-04 consumes the actual production attention Q, the exact committed texture K/V generation and the authoritative BufferAtlas output for the same invocation lineage. KvTexture GQA4 executes as an isolated live shadow and produces device-side parity evidence only.

```text
BufferAtlas production attention
  -> production Q GPU snapshot
  -> authoritative output GPU snapshot
  -> authoritative K/V commit
  -> TEXTURE-03 texture generation publish
  -> KvTexture GQA4 deferred live replay
  -> device-side parity token
```

The deferred replay is required because C3/C4 attention consumes staged-visible K/V before the authoritative K/V and texture generation are published. TEXTURE-04 does not relabel staged state as committed.

---

# 1. Authority boundary

```text
route authority             W3-C1 through W3-C5
production output authority W3-C6 HeadwiseFullActive
active physical executor    BufferAtlasV1
candidate executor          KvTextureGqa4V1
candidate result authority  shadow parity evidence only
```

Candidate output must not reach:

```text
o_proj
residual add
next layer
logits
sampling
token history
persistent K/V
production output ring
```

Required zero counters:

```text
candidate output commit
candidate downstream dispatch
candidate o_proj consumer
candidate residual consumer
candidate logits consumer
candidate sampling consumer
candidate token-history mutation
candidate K/V authority commit
route authority mutation
output authority mutation
physical executor switch
TensorCube texture consumer
```

---

# 2. Canonical route scope

Admitted:

```text
IncrementalDecode  seq_q == 1
ChunkedDecode      seq_q >= 2
```

Generic forward inherits only the canonical W3-C5 delegation result.

Prefill is explicitly:

```text
NotAdmittedBaselineUnavailable
```

TEXTURE-04 does not infer prefill parity from incremental or chunk evidence.

---

# 3. Live shadow policy

```rust
pub enum HeadwiseTextureLiveShadowPolicy {
    Disabled,
    CanaryEveryCommittedInvocation,
    SampledCommittedInvocation { interval: u32 },
}
```

Gate policy:

```text
CanaryEveryCommittedInvocation
```

A disabled or unsampled invocation leaves production untouched and cannot be counted as parity PASS.

---

# 4. Production payload capture

Capture is admitted only after BufferAtlas dispatch and production device guard succeed under a valid HeadwiseFullActive lease.

Q contract:

```text
shape   [1, q_heads, seq_q, head_dim]
dtype   f32
layout  contiguous B,H,S,D
mode    RawBorrowed
state   BorrowedBuffer
```

Q and authoritative output leases are copied on the GPU into invocation-owned snapshot buffers before allocator reuse.

```text
Q authorized lease range
  -> GPU buffer copy
  -> isolated Q snapshot

BufferAtlas downstream output lease
  -> GPU buffer copy
  -> isolated reference snapshot
```

Forbidden:

```text
host upload
host repack
CPU materialization
payload map/readback
cross-device copy
candidate/reference alias
```

---

# 5. Shadow ticket

Each layer ticket binds:

```text
model instance
decode session and epoch
route and layer index
attention invocation digest and generation
production dispatch receipt
production nonce and guard slot
causal position
shape reconciliation
prefix generation
expected committed generation and token count
Q snapshot identity
reference output snapshot identity
same-device capture submission serial
```

Tickets are ordered by exact layer index. Duplicate, missing, mixed-route, mixed-generation or mixed-shape tickets abort only the candidate transaction.

The bounded ring has explicit capacity, layer, query-token and snapshot-byte limits. Capacity exhaustion produces `CapacitySkipped`; it never stalls or mutates production.

---

# 6. Committed texture generation consumption

Candidate replay starts only after TEXTURE-03 publishes the exact generation expected by the ticket.

Required exact identity:

```text
model instance
session ID and epoch
committed generation
committed token count
layer count and order
generation-view digest
layer-view digest
page-LUT digest
same device and queue lineage
```

Generation lag requires explicit resynchronization. Generation ahead is quarantined. Latest-generation substitution is forbidden.

---

# 7. GQA4 live shadow geometry

Canonical gate geometry:

```text
batch count         1
query heads        32
K/V heads           4
head dimension     64
cluster width       4
subgroup width     32
page tokens       128
token tile         32
max seq_kv       2048
```

`batch > 1`, noncanonical head mapping, unsupported subgroup width, malformed LUT or unsealed texture pages fail closed.

Candidate input:

```text
Q             production invocation GPU snapshot
K/V           exact committed texture generation
reference     BufferAtlas authoritative output snapshot
candidate out isolated scratch buffer
```

---

# 8. Device-side output parity

TEXTURE-04 compares final attention context output because the production BufferAtlas path does not expose internal score/probability buffers as public authority.

Canonical envelope:

```text
absolute threshold   5.0e-5
relative threshold   5.0e-4
relative floor       1.0e-4
nonfinite allowed    0
```

Device aggregation records:

```text
visited count
nonfinite count
mismatch count
maximum absolute error
maximum relative error
mean absolute error
RMS error
first fault layer and element
completed-layer mask
integrity XOR
```

Only the compact health token may be drained asynchronously. Output payload readback remains zero.

---

# 9. Runtime integration

New backend files:

```text
crates/burn_webgpu_backend/src/headwise_gqa4_live_shadow_dispatch.rs
crates/burn_webgpu_backend/src/shaders/headwise_gqa4_live_shadow_compare_dynamic.wgsl
crates/burn_webgpu_backend/src/shaders/headwise_gqa4_live_shadow_token_finalize.wgsl
```

New model file:

```text
crates/model_core/src/headwise_texture_live_shadow.rs
```

Modified runtime files:

```text
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/decode_state.rs
crates/model_core/src/headwise_texture_incremental_append.rs
crates/model_core/src/headwise_texture_persistent_kv_binding.rs
crates/model_core/src/lib.rs
crates/model_core/src/native_wgpu.rs
```

New gate surface:

```text
crates/orchestrator_local/src/headwise_texture_04_cli_registry.rs
crates/orchestrator_local/src/bin/ash_attn_headwise_texture_04_gate.rs
specs/cli/ash_attn_headwise_texture_04.args
```

Native runtime exposes capture and post-commit replay methods. Session retirement removes both residency and pending ticket state.

---

# 10. Canonical physical gate

```text
incremental
  prefix generation      7
  committed generation   8
  seq_q                   1
  seq_kv                130

chunk
  prefix generation      8
  committed generation   9
  seq_q                   8
  seq_kv                138
```

Across 22 layers and two commits:

```text
BufferAtlas reference dispatches  44
Q GPU snapshot copies             44
reference-output GPU copies       44
KvTexture candidate dispatches    44
device compare dispatches         44
all-layer shadow commits           2
```

Deterministic gate tensors must travel through the production capture-ticket, committed texture generation and post-commit replay APIs. Direct diagnostic helper invocation is insufficient.

---

# 11. Validation contract

```text
positive cases              176 / minimum 168
negative controls           184 / minimum 176
decision counters           148
child artifacts             122
CLI key/value pairs         104
response-file lines         208
expected model layers        22
expected shadow commits       2
expected layer dispatches    44
```

Child artifact ordered-list digest:

```text
374d228ac72c0bbd6b2df589e45b2ffef46a1eebb352bd7249ce1da72cbde258
```

Negative controls cover invalid parents, noncanonical route or geometry, ticket duplication/missing layers, generation mismatch, texture lag/ahead, unsealed pages, device/queue mismatch, lease-range mismatch, snapshot alias, host movement, payload readback, numerical divergence, compact-token corruption, ring overflow, candidate output/downstream/KV commit and every authority mutation.

---

# 12. Runtime artifacts

```text
workspace/runtime/attention/headwise/texture/04/
workspace/runtime/attention/headwise/texture/ash_attn_headwise_texture_04_runtime_artifact.json
workspace/runtime/attention/headwise/texture/ash_attn_headwise_texture_04_local_manifest.json
```

Code packages exclude Markdown, PowerShell/CMD helpers, hash sidecars and pre-generated TEXTURE-04 runtime output.

---

# 13. Direct execution

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_texture_04_gate `
  -- `
  "@specs/cli/ash_attn_headwise_texture_04.args"
```

Expected revision:

```text
HEADWISE-TEXTURE-04-live-shadow-dispatch-v1
```

Expected PASS token:

```text
PROMOTE_ASH_ATTN_HEADWISE_TEXTURE_04_TEXTURE_GQA4_LIVE_SHADOW_DISPATCH_BUFFER_ATLAS_KV_TEXTURE_DUAL_EXECUTION_PRODUCTION_KV_GENERATION_CONSUMPTION_DEVICE_GUARDED_OUTPUT_PARITY_NO_CANDIDATE_OUTPUT_COMMIT_SEALED
```

---

# 14. Completion state

After PASS:

```text
BufferAtlasV1
  ProductionActive
  ProductionBound

KvTextureGqa4V1
  CapabilityBoundCandidate
  PersistentKvResidencyBound
  IncrementalAppendParityBound
  LiveShadowParityBound
  ProductionDispatchForbidden
  OutputCommitForbidden
```

Next stage:

```text
ASH-ATTN-HEADWISE-TEXTURE-05

Sustained Live Shadow Soak /
Route·Length Bucket Coverage /
Async Health Aggregation /
Latency·Residency Budget /
Divergence Quarantine /
Promotion Eligibility Hold Seal
```
