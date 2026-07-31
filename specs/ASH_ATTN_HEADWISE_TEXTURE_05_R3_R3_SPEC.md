# ASH-ATTN-HEADWISE-TEXTURE-05-R3-R3

## Atlas Microtile Streaming /
## Bounded Upload Ring /
## Direct Final-Atlas Write /
## Layer·Page Wave Scheduling /
## In-Flight Slot Cap /
## Fence-Gated Slot Reuse /
## No Mega Staging Buffer /
## No Full-Span Candidate Scratch /
## Per-Wave Transient Byte Receipt /
## Peak Transient Budget Closure Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-05-R3-R3`  
> Build revision: `HEADWISE-TEXTURE-05-R3-R3-atlas-microtile-streaming-v1`  
> Parent: `ASH-ATTN-HEADWISE-TEXTURE-05-R3-R2`  
> Production authority: `BufferAtlasV1 / HeadwiseFullActive` unchanged  
> Candidate authority: `KvTextureGqa4V1` shadow evidence only

---

# 1. Trigger

R3-R2 measured:

```text
known_floor_bytes      95,944,792
peak_transient_bytes   19,867,776
corrected_peak_bytes  115,812,568
retirement_owner_zero  true
```

R3-R3 reduces the commit-transient peak without changing the fixed persistent floor. It does not treat the existing `plateau_pass=false` as proof that transient bytes alone caused the failure, because the disclosed corrected peak is already below the parent total budget. Parent R3-R2 invariants remain authoritative and cannot be masked by a lower transient estimate.

---

# 2. Canonical streaming geometry

```text
layers                    22
layer wave size            2
layer wave count          11
page tokens              128
token microtile size      32
microtiles per page        4
page wave size             1
ring slot count            3
max submitted slots        2
```

Per shadow commit:

```text
11 layer waves
× 60 healthy commits
= 660 wave receipts
```

The candidate pipeline cardinality becomes nine:

```text
BufferAtlasReference
TexturePopulation
TexturePersistentPopulation
TextureValidation
TextureIncrementalAppend
CandidateMicrotileAccumulate
CandidateMicrotileNormalize
Compare
Finalize
```

No pipeline may be created lazily inside a wave.

---

# 3. No full-span candidate scratch

The R3-R3 candidate path must not allocate:

```text
scores[row_count × seq_kv]
probabilities[row_count × seq_kv]
mega staging buffer
full-span candidate scratch
```

Required counters:

```text
full-span score buffer creation       0
full-span probability buffer creation 0
mega staging buffer creation          0
payload readback                      0
candidate output commit               0
```

Instead, each row retains only bounded streaming state:

```text
row max
row denominator
row output accumulator[head_dim]
```

The shader uses two deterministic passes over 32-token microtiles:

```text
Pass 1  stream token tiles to derive canonical row max
Pass 2  revisit tokens in ascending order and accumulate denominator/output
Normalize  write final output directly to the final candidate buffer
```

This preserves deterministic token order without materializing full-span score or probability arrays.

---

# 4. Layer·page wave scheduling

The physical gate processes layers in canonical waves:

```text
[0,1]
[2,3]
...
[20,21]
```

For each layer wave:

```text
acquire one free ring slot
bind current published texture generation
encode page/microtile streaming dispatches
submit wave
mark slot Submitted
obtain authoritative completion
release wave-local snapshots and bind groups
mark slot Free
reuse only after completion
```

The global layer index remains authoritative. Wave-local indices may not change layer identity, generation identity or coverage identity.

---

# 5. Bounded ring state machine

```text
Free
  -> Encoding
  -> Submitted
  -> Completed
  -> Free
```

Forbidden transitions:

```text
Submitted -> Encoding
Submitted -> Free without completion
Completed -> Submitted without reset
slot generation mismatch
more than two Submitted slots
more than three allocated slots
```

Completion authority is a queue/device completion receipt. CPU scheduling order alone is not sufficient.

---

# 6. Direct final write

The microtile candidate writes the normalized row output directly into the final candidate output buffer consumed by compare/finalize.

Forbidden:

```text
microtile output -> mega merge buffer -> final output
per-wave host merge
per-page readback
per-layer full output duplication
```

The compare path may consume each completed layer wave after its candidate output is complete. The compact final token remains one per shadow commit.

---

# 7. Transient-byte accounting

Parent transient baseline:

```text
19,867,776 bytes
```

R3-R3 patch-local ceiling:

```text
8,388,608 bytes
```

Required reduction:

```text
at least 11,479,168 bytes
at least 57.78 percent
```

Fixed persistent floor:

```text
95,944,792 bytes
```

R3-R3 corrected peak ceiling:

```text
104,333,400 bytes
```

Per-wave receipt records:

```text
shadow commit ordinal
texture generation
layer wave ordinal
first and last global layer
page and microtile geometry
ring slot index
slot state transitions
wave transient bytes
peak submitted slot count
submission serial
completion receipt
pipeline-set digest
full-span allocation counters
pass
receipt digest
```

Required totals:

```text
wave receipts                         660
full-span score allocations             0
full-span probability allocations       0
mega staging allocations                0
ring slot reuse before completion       0
max submitted slots                    <=2
observed ring slots                    <=3
peak transient bytes           <=8,388,608
```

---

# 8. Parent invariant non-masking

R3-R3 may reduce transient bytes but must not independently force `residency_plateau_within_budget=true`.

The final plateau predicate remains:

```text
parent R3-R2 fixed-floor pass
&& bootstrap-baseline pass
&& generation-page-ledger pass
&& ten-replay-zero-growth pass
&& current/previous refcount pass
&& retired/free-set convergence pass
&& transient-owner-delta pass
&& session-retirement-owner-zero pass
&& R3-R3 streaming transient ceiling pass
```

If any parent invariant fails, plateau remains false even if R3-R3 peak bytes are below the ceiling.

The legacy mixed-geometry ratio remains non-authoritative.

---

# 9. Runtime artifacts

```text
workspace/runtime/attention/headwise/texture/05/r3_r3/
  microtile_streaming_plan.json
  bounded_ring_receipt.json
  per_wave_transient_byte_receipts.json
  no_full_span_candidate_scratch_receipt.json
  fence_gated_slot_reuse_receipt.json
  peak_transient_budget_receipt.json
  parent_invariant_non_masking_receipt.json
```

Top-level:

```text
workspace/runtime/attention/headwise/texture/
  ash_attn_headwise_texture_05_r3_r3_runtime_artifact.json
  ash_attn_headwise_texture_05_r3_r3_local_manifest.json
```

Artifacts are Rust-authored through temporary write, atomic rename, readback and SHA-256 verification.

---

# 10. Verification gate

Binary:

```text
ash_attn_headwise_texture_05_r3_r3_gate
```

The gate verifies:

```text
37-key response-file cardinality
22 layers / 2-layer waves / 11 waves
128 page tokens / 32-token microtiles / 4 microtiles per page
3 ring slots / at most 2 submitted
9 pipeline kinds
no full-span score/probability surface
no mega staging buffer
stable two-pass streaming softmax
fence-gated slot reuse
660 wave receipt contract
8 MiB transient ceiling
parent invariant non-masking
runtime artifact and local manifest generation
```

---

# 11. Completion gate

```text
pipeline kind count                         9
layer wave size                             2
layer wave count                           11
ring slot count                             3
maximum submitted slots                   <=2
wave receipts                              660
full-span score buffer creations             0
full-span probability buffer creations       0
mega staging buffer creations                0
payload readbacks                            0
candidate output commits                      0
peak transient bytes                 <=8,388,608
corrected peak bytes                <=104,333,400
slot reuse before completion                  0
parent invariant masking count                0
production authority mutation count           0
```

Patch-local PASS token:

```text
PASS_ASH_ATTN_HEADWISE_TEXTURE_05_R3_R3_ATLAS_MICROTILE_STREAMING_BOUNDED_UPLOAD_RING_DIRECT_FINAL_ATLAS_WRITE_LAYER_PAGE_WAVE_SCHEDULING_IN_FLIGHT_SLOT_CAP_FENCE_GATED_REUSE_NO_MEGA_STAGING_NO_FULL_SPAN_CANDIDATE_SCRATCH_PER_WAVE_TRANSIENT_BYTE_PEAK_BUDGET_CLOSURE_SEALED
```

---

# 12. Direct execution

Verification gate:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_r3_r3_gate -- "@specs/cli/ash_attn_headwise_texture_05_r3_r3.args"
```

Physical Texture-05 gate:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_gate -- "@specs/cli/ash_attn_headwise_texture_05.args"
```

R3-R3 closes the mega transient shape. It does not claim that p95 or p99 latency is solved, and it does not override a failing parent page/refcount/owner invariant.
