# ASH-ATTN-HEADWISE-TEXTURE-03

## Incremental KV Texel Append /
## Single-Token Page Update /
## Chunk Multi-Token Population Transaction /
## Atomic Page Seal /
## KV·Texture Generation Parity Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-03`  
> Build revision: `HEADWISE-TEXTURE-03-incremental-kv-texel-append-v1`  
> Parent: `ASH-ATTN-HEADWISE-TEXTURE-02` PASS  
> Canonical local source SHA-256: `210221613b188f719fb37ade8fcb931601ebefe11639535373a6312b14512b48`  
> Canonical local source lines: `1551`  
> Active executor: `BufferAtlasV1` unchanged  
> Candidate executor: `KvTextureGqa4V1`  
> Parent readiness: `PersistentKvResidencyBound`  
> Target readiness: `IncrementalAppendParityBound`  
> Output authority: `HeadwiseFullActive` unchanged

---

# 0. Purpose

TEXTURE-02 proves fixture-free full population from committed persistent DecodeState K/V. Re-populating the complete texture after every decode step would rewrite `O(total committed tokens)` data and would make immutable prior-generation pages impossible to preserve safely.

TEXTURE-03 derives only the newly committed token span into the texture candidate:

```text
W3-C3 or W3-C4 authoritative KV transaction Published
  -> adopt exact parent commit receipt
  -> verify base texture generation
  -> construct append-span authority
  -> acquire same-device committed K/V raw leases
  -> reuse untouched immutable pages
  -> copy-on-write the touched partial prefix page
  -> allocate new physical pages for new logical pages
  -> write append span only
  -> seal all touched pages
  -> seal all model layers
  -> verify KV/texture generation parity
  -> publish one new generation view
```

Texture append remains a derived candidate transaction. Failure does not roll back committed K/V, token history or the decode result. The previous published texture generation remains authoritative for the candidate and the candidate enters an explicit lag or resynchronization state.

---

# 1. Authority separation

Authoritative state:

```text
DecodeState persistent K/V
KvPositionLifecycle.content_generation
KvPositionLifecycle.committed_past_len
KvLayerCache key/value content generation
W3-C3 IncrementalKvStepTransaction Published receipt
W3-C4 ChunkedKvAppendTransaction Published receipt
```

Derived state:

```text
HeadwiseTextureGenerationView
HeadwiseTextureLayerGenerationView
immutable texture physical pages
physical page refcounts
texture append transaction receipt
```

Forbidden authority inversion:

```text
texture generation -> K/V generation mutation
texture page state -> token-history mutation
texture append result -> parent transaction result mutation
texture append failure -> committed K/V rollback
texture candidate -> production output authority
```

---

# 2. Parent closure

Required parents:

```text
W3-C3-R1 Incremental Full Activation PASS
W3-C4-R2 Chunked Decode Live Activation PASS
W3-C5-R1 Generic Forward Reconciliation PASS
W3-C6-R1 Headwise FullActive PASS
TEXTURE-01 Physical Executor Authority PASS
TEXTURE-02 Persistent KV Residency PASS
```

Required parent state:

```text
output authority              HeadwiseFullActive
active physical executor      BufferAtlasV1
candidate executor            KvTextureGqa4V1
candidate readiness           PersistentKvResidencyBound
published texture generation  present
layer count                   ModelSpec.num_layers exact
fixture and host movement     zero
```

Any parent artifact, manifest, model, device, session, kernel bundle or generation mismatch fails closed.

---

# 3. Append policy

```rust
pub enum HeadwiseTextureAppendSynchronizationPolicy {
    Disabled,
    PostCommitDerivedAppend,
}
```

Canonical policy:

```text
PostCommitDerivedAppend
```

Semantics:

```text
parent K/V commit succeeds independently
texture append starts only after parent publication
successful append publishes the same committed generation
failed append preserves the previous texture generation
silent full repopulation is forbidden
BufferAtlas remains production-active
```

---

# 4. Trigger authority

```rust
pub enum HeadwiseTextureAppendTriggerKind {
    PostIncrementalKvCommit,
    PostChunkKvCommit,
}

pub struct HeadwiseTextureAppendTrigger {
    pub model_instance_id: String,
    pub decode_session_id: String,
    pub session_epoch: u64,
    pub kind: HeadwiseTextureAppendTriggerKind,
    pub parent_commit_receipt_digest: String,
    pub prefix_generation: u64,
    pub committed_generation: u64,
    pub prefix_token_count: usize,
    pub committed_token_count: usize,
    pub append_span: HeadwiseTextureAppendSpan,
    pub route_identity_digest: String,
    pub trigger_digest: String,
}
```

Incremental requirements:

```text
parent state             Published
append token count       1
committed generation     prefix + 1
append begin             prefix token count
append end               prefix + 1
```

Chunk requirements:

```text
parent K/V and history state  Published
append token count            >= 2
committed generation          prefix + 1
append begin                  persistent prefix length
append end                    post-append length
```

Shape alone never selects trigger kind.

---

# 5. Append span

```rust
pub struct HeadwiseTextureAppendSpan {
    pub token_begin: usize,
    pub token_end_exclusive: usize,
    pub token_count: usize,
    pub first_logical_page: u32,
    pub last_logical_page: u32,
    pub touched_logical_page_count: u32,
    pub first_page_token_offset: u32,
    pub last_page_valid_token_count_after: u32,
    pub span_digest: String,
}
```

Invariants:

```text
token_count > 0
token_end == token_begin + token_count
token_begin == committed prefix length
token_end == committed post-append length
first page == token_begin / page_tokens
last page == (token_end - 1) / page_tokens
```

Single-token and chunk append share this authority.

---

# 6. Immutable generation views

Sealed pages are never overwritten. A generation view maps logical pages to immutable physical pages:

```rust
pub struct HeadwiseTextureLogicalPageRef {
    pub logical_page_index: u32,
    pub physical_page_index: u32,
    pub content_generation: u64,
    pub valid_token_count: u32,
    pub content_digest: String,
}

pub struct HeadwiseTextureLayerGenerationView {
    pub layer_index: usize,
    pub committed_generation: u64,
    pub committed_token_count: usize,
    pub pages: Vec<HeadwiseTextureLogicalPageRef>,
    pub layer_view_digest: String,
}

pub struct HeadwiseTextureGenerationView {
    pub model_instance_id: String,
    pub decode_session_id: String,
    pub session_epoch: u64,
    pub committed_generation: u64,
    pub committed_token_count: usize,
    pub layer_views: Vec<HeadwiseTextureLayerGenerationView>,
    pub view_digest: String,
}
```

Untouched pages are shared by reference. Touched pages receive new physical-page identities.

Example:

```text
generation G
  logical 0 -> physical 2
  logical 1 -> physical 5

generation G+1
  logical 0 -> physical 2  shared immutable
  logical 1 -> physical 7  copy-on-write
  logical 2 -> physical 9  new
```

---

# 7. Physical page allocator

```rust
pub struct HeadwiseTexturePhysicalPageRecord {
    pub physical_page_index: u32,
    pub state: KvTexturePageState,
    pub content_generation: u64,
    pub valid_token_count: u32,
    pub content_digest: String,
    pub generation_ref_count: u32,
}
```

Allocator requirements:

```text
capacity admission before GPU work
one immutable content owner per physical page
reference-counted generation sharing
no retirement while referenced
no write after SealedImmutable
failed staged pages quarantined
retention window preserves current and previous generations
```

---

# 8. Copy-on-write and append GPU submission

A touched logical page that already exists in the base generation is copied to a new physical page on the GPU before append:

```text
K source texture layer -> K destination texture layer
V source texture layer -> V destination texture layer
append shader writes only committed token span
```

A new logical page is allocated without cloning.

Per-layer command ordering:

```text
texture-to-texture COW copies
  -> append compute pass
  -> one queue submission
  -> completion
  -> content digest assignment
  -> immutable page seal
```

The append shader reads committed persistent K/V in `[B,Hkv,S,D]` layout using strict borrowed storage-buffer windows and writes `rgba32float` D2-array texels with integer coordinates. Filtering and mipmaps are forbidden.

---

# 9. Incremental append

For one committed token:

```text
append length             1
source generation         G+1 committed K/V
base texture generation   G
published texture         G+1
```

Cases:

```text
inside partial final page
  -> clone final page + write one token row

at exact page boundary
  -> allocate new page + write one token row
```

All model layers use exact generation-bound K/V leases.

---

# 10. Chunk append

A chunk may contain:

```text
partial first page
zero or more full middle pages
partial or full final page
```

Only the first touched page may require COW. Remaining touched logical pages are new allocations. The transaction must handle multi-page spans in one authoritative append-span plan.

Canonical gate geometry:

```text
base generation         7
base tokens             129
incremental generation  8
incremental tokens      130
chunk generation        9
chunk append            259
chunk tokens            389
page tokens             128
```

This exercises a partial first page, a complete middle page and a partial final page.

---

# 11. All-layer publication atomicity

`atomic` means publication atomicity, not a hardware atomic instruction.

```text
all touched GPU page work complete
all page content digests committed
all touched pages SealedImmutable
all expected layers complete
KV/texture generation parity PASS
one generation-view publication
```

Partial layer or partial generation publication is forbidden. Any failure preserves the previous published generation and quarantines new candidate pages.

---

# 12. Generation parity

```rust
pub struct HeadwiseKvTextureGenerationParityReceipt {
    pub kv_committed_generation: u64,
    pub texture_committed_generation: u64,
    pub kv_committed_token_count: usize,
    pub texture_committed_token_count: usize,
    pub expected_layer_count: usize,
    pub texture_layer_count: usize,
    pub all_layer_generation_exact: bool,
    pub all_layer_token_count_exact: bool,
    pub append_span_exact: bool,
    pub page_validity_exact: bool,
    pub previous_generation_preserved: bool,
    pub parity_pass: bool,
    pub parity_digest: String,
}
```

Publication requires:

```text
texture generation == committed K/V generation
texture token count == committed K/V token count
all layers exact
append begin/end exact
logical page count exact
last-page valid token count exact
untouched page identities preserved
touched page identities newly sealed
```

---

# 13. Lag and recovery

```text
texture generation < required K/V prefix generation
  -> Lagging
  -> FullResynchronizationRequired

texture generation > required K/V prefix generation
  -> Quarantined
  -> HOLD
```

Recovery uses an explicit TEXTURE-02 full snapshot. Silent generation skipping and silent full repopulation are forbidden.

---

# 14. Runtime integration

New backend files:

```text
crates/burn_webgpu_backend/src/headwise_kv_texture_incremental_append.rs
crates/burn_webgpu_backend/src/headwise_kv_texture_generation_view.rs
crates/burn_webgpu_backend/src/shaders/headwise_kv_texture_append_persistent_cache_rgba4.wgsl
```

Modified backend:

```text
headwise_kv_texture_residency.rs
lib.rs
```

New model file:

```text
crates/model_core/src/headwise_texture_incremental_append.rs
```

Modified model runtime:

```text
headwise_texture_persistent_kv_binding.rs
decode_state.rs
native_wgpu.rs
lib.rs
```

New gate:

```text
crates/orchestrator_local/src/headwise_texture_03_cli_registry.rs
crates/orchestrator_local/src/bin/ash_attn_headwise_texture_03_gate.rs
specs/cli/ash_attn_headwise_texture_03.args
```

The W3-C3 incremental and W3-C4 chunk hooks run only after authoritative transaction publication. Hook failure is recorded without changing the authoritative decode return value.

---

# 15. Nonmutation boundary

```text
active executor                    BufferAtlasV1
candidate executor                 KvTextureGqa4V1
candidate readiness                IncrementalAppendParityBound
output authority                   HeadwiseFullActive

physical executor switch           0
KvTexture production dispatch      0
KvTexture output commit            0
KvTexture K/V authority commit     0
route authority mutation           0
output authority mutation          0
TensorCube texture consumer        0
```

Texture append dispatch is residency maintenance, not production attention dispatch.

---

# 16. Validation contract

```text
positive cases              >= 152
implementation target       160
negative controls           >= 160
implementation target       168
decision counters           132
child artifacts             104
CLI key/value pairs          96
response-file lines         192
expected model layers        22
```

Negative controls cover stale/ahead/missing base generations, invalid parent receipts, malformed spans, non-single incremental appends, short chunk appends, capacity exhaustion, sealed-page overwrite, invalid COW source/destination, page-copy mismatch, append destination mismatch, seal-before-submit, missing page digest, partial publication, parity mismatch, stale publication, lease/device/range mismatch, host movement, fixture admission, production dispatch/output mutation and TensorCube consumer admission.

Child artifact ordered-list digest:

```text
191048d952857c5d5d392a181f76339245afd4c245892d180074516755b99a24
```

---

# 17. Runtime artifacts

```text
workspace/runtime/attention/headwise/texture/03/
workspace/runtime/attention/headwise/texture/ash_attn_headwise_texture_03_runtime_artifact.json
workspace/runtime/attention/headwise/texture/ash_attn_headwise_texture_03_local_manifest.json
```

Code packages exclude Markdown, PowerShell/CMD helpers, hash sidecars and pre-generated TEXTURE-03 runtime output.

---

# 18. Direct execution

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_texture_03_gate `
  -- `
  "@specs/cli/ash_attn_headwise_texture_03.args"
```

Expected first log:

```text
[ash-attn-headwise-texture-03][build] revision=HEADWISE-TEXTURE-03-incremental-kv-texel-append-v1 child_artifact_expected=104 child_artifact_list_sha256=191048d952857c5d5d392a181f76339245afd4c245892d180074516755b99a24
```

PASS token:

```text
PROMOTE_ASH_ATTN_HEADWISE_TEXTURE_03_INCREMENTAL_KV_TEXEL_APPEND_SINGLE_TOKEN_PAGE_UPDATE_CHUNK_MULTI_TOKEN_POPULATION_TRANSACTION_ATOMIC_PAGE_SEAL_KV_TEXTURE_GENERATION_PARITY_SEALED
```

---

# 19. Completion state

After PASS:

```text
KvTextureGqa4V1
  CapabilityBoundCandidate
  PersistentKvResidencyBound
  IncrementalAppendParityBound
  ProductionDispatchForbidden
```

The next stage is:

```text
ASH-ATTN-HEADWISE-TEXTURE-04

Texture GQA4 Live Shadow Dispatch /
BufferAtlas·KvTexture Dual Execution /
Production KV Generation Consumption /
Device-Guarded Output Parity /
No Candidate Output Commit Seal
```
