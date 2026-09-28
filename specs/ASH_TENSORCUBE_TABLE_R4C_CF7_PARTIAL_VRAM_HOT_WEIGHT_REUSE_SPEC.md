# TENSORCUBE-TABLE-R4C-CF7

## PARTIAL VRAM HOT-WEIGHT FORWARD / BACKWARD REUSE

```text
TENSORCUBE-TABLE-R4C-CF7

PARTIAL VRAM HOT-WEIGHT
FORWARD / BACKWARD REUSE

+ EXISTING GpuWeightPageCache AUTHORITY PROMOTION
+ CF6 DIRECT BOUNDED UPLOAD PRESERVATION
+ BOUNDED VRAM HOT-WEIGHT CACHE
+ FORWARD-TO-BACKWARD REUSE AUTHORITY
+ PARAMETER / GENERATION / DIGEST EXACT CACHE IDENTITY
+ DEVICE / QUEUE / RUNTIME-GENERATION BINDING
+ EXPLICIT VRAM BUDGET
+ DETERMINISTIC ADMISSION / EVICTION
+ PINNED-SAFE CACHE BYPASS
+ H2D AVOIDED-BYTE RECEIPT
+ ZERO DUPLICATE H2D ON EXACT HIT
+ CF11 SOURCE-RETIREMENT PRESERVATION
+ NO NEW D2H
+ NO CACHE-INDUCED GPU WAIT
+ NO WGSL / NUMERICAL MATH CHANGE
```

## 1. Purpose

CF7 promotes the already-existing decoder-block `GpuWeightPageCache` into the canonical bounded forward-to-backward reuse authority. It does not introduce a second GPU cache.

Parent lineage:

```text
TENSORCUBE-TABLE-R4D-R0B
GRADIENT OBSERVABILITY DEVICE AGGREGATION

TENSORCUBE-TABLE-R4D-R0A
HOT-PATH PIPELINE RESIDENCY

TENSORCUBE-TABLE-R4C-CF6
DIRECT / BOUNDED WEIGHT UPLOAD

TENSORCUBE-TABLE-R4C-CF5
HOST COPY COLLAPSE
```

CF6 remains the canonical cache-miss / bypass upload path.

## 2. Runtime Modes

```text
ASH_TENSORCUBE_TABLE_R4C_CF7_MODE

OFF / DISABLED / 0
OBSERVE / OBSERVE_ONLY
ACTIVE / ACTIVE_VERIFIED / 1
```

Default is `OFF`.

CF7 requires R0A and R0B ACTIVE when CF7 is enabled.

VRAM budget:

```text
ASH_TENSORCUBE_TABLE_R4C_CF7_HOT_WEIGHT_BUDGET_BYTES
```

OBSERVE and ACTIVE require an explicit nonzero budget. The budget must be at least one 16 MiB page and 16 MiB aligned. A nonzero CF7 budget with mode OFF is rejected.

## 3. OBSERVE

OBSERVE does not physically retain a second GPU-cache authority.

It simulates the exact logical admission / hit / miss / bypass / eviction sequence using the same:

```text
source generation
decoder-block tensor-set digest
runtime identity
logical access sequence
VRAM budget
deterministic next-use policy
```

This qualifies the exact reuse set and budget behavior without making a performance claim.

## 4. ACTIVE

ACTIVE enables the existing physical `GpuWeightPageCache` in the self-materialized canary / production configuration.

Canonical path:

```text
forward
    -> CF6 canonical bounded upload
    -> exact CF7 admission
    -> forward compute
    -> GPU backing retained within budget

backward
    -> exact cache lookup
    -> HIT: same GPU backing, zero duplicate H2D
    -> MISS/BYPASS: CF6 canonical upload
```

CF7 never uses cache residency as model-commit or durability authority.

## 5. Exact Decoder-Block Identity

The decoder-block cache identity is sealed from the existing route metadata for the nine canonical decoder tensor roles:

```text
input RMSNorm
Q
K
V
O
post-attention RMSNorm
gate
up
down
```

Identity is bound to:

```text
parameter/tensor role
F32 representation
segment continuity
existing source_slice_digest
source generation
device authority
queue authority
runtime generation
representation revision
```

The tensor-set authority digest is created through the existing canonical decoder-block sealing authority.

No host source-byte reread or new SHA scan is added merely to compute cache identity.

## 6. Physical Runtime Binding

On first physical cache use, CF7 binds the cache to:

```text
runtime holder identity
device authority id
queue authority id
checkpoint identity
representation = F32_CANONICAL_BURN_BUFFER_V1
```

Later lookup with mismatched runtime/device/queue/checkpoint/representation fails closed or misses according to the canonical identity contract.

No cross-device or stale-runtime backing reuse is admitted.

## 7. Exact Hit Law

An exact physical hit requires the expected decoder-block tensor-set digest and tensor identities to match the retained entry.

CF7 adds the digest-aware lookup authority:

```text
contains_decoder_block_exact
```

The prior generation-only lookup remains available for parent compatibility, but CF7 promotion uses the exact identity surface.

A digest mismatch is never promoted as a hit.

## 8. Budget / Eviction / Bypass

The existing deterministic next-use eviction authority is preserved.

CF7 changes cache pressure behavior so that optimization cannot become a correctness or synchronization failure.

If:

```text
candidate entry > budget
OR
no reclaimable capacity exists because entries are pinned
```

the result is:

```text
CACHE BYPASS
-> canonical CF6 upload
-> normal parent lifetime
```

not:

```text
forced device wait
fatal cache error
hidden VRAM overcommit
```

Physical retained bytes must remain within the configured budget.

## 9. Pin / Lease Safety

Pinned GPU backing is not evictable.

The existing Arc ownership authority remains the physical pin witness:

```text
Arc::strong_count(entry.bundle) != 1
    -> entry cannot be evicted
```

CF7 records `eviction_blocked_by_pin_count`.

No `device.poll(Wait)` is added merely to free cache capacity.

## 10. Duplicate H2D Law

On an exact cache hit:

```text
duplicate_h2d_bytes = 0
```

The same canonical GPU backing satisfies backward demand.

A hit followed by a second CF6 upload for the same consumer is an ACTIVE failure.

Receipt distinguishes:

```text
actual_h2d_bytes
parent_equivalent_h2d_bytes
forward_to_backward_bytes_avoided
duplicate_h2d_bytes
```

## 11. Source-Retirement Preservation

CF7 retains GPU backing only.

It does not retain:

```text
ResidentCheckpointRangeView
host source Arc<Vec<u8>>
host decode scratch
```

beyond the existing CF6 use scope.

Existing CF11 closure remains authoritative:

```text
reader_closed=true
live_alias_count=0
source_reservation_released=true
source_retired_before_successor_reservation=true
```

## 12. No New Transfer / Synchronization

CF7 adds no new:

```text
weight D2H
cache-validation D2H
raw tensor parity D2H
per-hit Poll(Wait)
per-hit device idle barrier
```

A miss/bypass uses the existing CF6 H2D path.

## 13. Telemetry

CF7 physical receipt includes at minimum:

```text
mode
budget_bytes
current/peak resident bytes
cache lookup/hit/miss/bypass counts
cache admission/eviction/reload counts
forward-to-backward lookup/hit/miss counts
forward_to_backward_bytes_avoided
actual_h2d_bytes
parent_equivalent_h2d_bytes
duplicate_h2d_bytes
generation_mismatch_count
digest_mismatch_count
runtime_identity_mismatch_count
eviction_blocked_by_pin_count
admitted
```

Terminal receipt:

```text
tensorcube_table_r4c_cf7_partial_vram_hot_weight_reuse_receipt.json
```

Compact log:

```text
[ASH-TENSORCUBE-TABLE-R4C-CF7][hot-weight-reuse]
```

Pass token:

```text
PASS_TENSORCUBE_TABLE_R4C_CF7_PARTIAL_VRAM_HOT_WEIGHT_REUSE
```

## 14. ACTIVE Fail-Closed

ACTIVE fails if any of these occur:

```text
peak_resident_bytes > budget_bytes
duplicate_h2d_bytes > 0 on an exact hit
stale generation accepted as hit
digest mismatch accepted as hit
runtime identity mismatch accepted as hit
pinned backing evicted
source alias leak introduced
```

Budget pressure itself is not a failure when canonical bypass is possible.

## 15. Actual Code Delta

```text
MOD 6
ADD 2
DEL 0
```

Modified:

```text
crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1b.rs
crates/base_train/src/lib.rs
crates/base_train/src/packed_runtime_native_bootstrap_accumulation_wave_residency.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/vram_hot_weight_page_residency.rs
tools/validate_ash_tensorcube_table_r4c_cf3_slot_lifecycle_static.py
```

Added:

```text
crates/base_train/src/tensorcube_table_r4c_cf7_partial_vram_hot_weight_reuse.rs
tools/validate_ash_tensorcube_table_r4c_cf7_partial_vram_hot_weight_reuse_static.py
```

The CF3 validator change is successor-awareness only: it accepts either the parent generation-only probe or CF7's exact digest-aware probe. CF3 runtime semantics are unchanged.

## 16. Static Acceptance

Executed in the bake environment:

```text
PASS_TENSORCUBE_TABLE_R4C_CF7_PARTIAL_VRAM_HOT_WEIGHT_REUSE_STATIC checks=151
PASS_TENSORCUBE_TABLE_R4D_R0B_GRADIENT_OBSERVABILITY_DEVICE_AGGREGATION_STATIC checks=178
PASS_TENSORCUBE_TABLE_R4D_R0A_HOT_PATH_PIPELINE_RESIDENCY_STATIC checks=104
PASS_TENSORCUBE_TABLE_R4C_CF6_DIRECT_BOUNDED_WEIGHT_UPLOAD_STATIC checks=135
PASS_TENSORCUBE_TABLE_R4C_CF5_HOST_COPY_COLLAPSE_STATIC checks=127
PASS_TENSORCUBE_TABLE_R4C_CF4_HOST_DEVICE_IO_ROUNDTRIP_ATTRIBUTION_STATIC checks=67
PASS_TENSORCUBE_TABLE_R4C_CF3_SLOT_LIFECYCLE_STATIC checks=77
PASS_TENSORCUBE_TABLE_R4B_CF3_FULL_ROUTE_HOST_LEDGER_COMPACTION_STATIC checks=127
PASS_TENSORCUBE_TABLE_R1_CF1_IMMUTABLE_BYTE_ACCOUNTING_STATIC
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF1_STATIC checks=63
PASS_EVE_MCU_R3H_CF11_PAGED_COW_CANDIDATE_WEIGHT_SUCCESSOR_STATIC checks=64
```

Build graph:

```text
Cargo.toml byte-identical
Cargo.lock byte-identical
WGSL baseline = 320
WGSL changed = 0
WGSL added = 0
```

## 17. Source Seals

```text
e00e0b938fa1045896aa77efe5883e5216e16b26ce357cb7e128a40efbebf7bf  crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1b.rs
7cb53a4b30f8a41435fef98e67896e4fdbcd220077f036c6dc18bfbb9efe6d86  crates/base_train/src/lib.rs
ca3072741ad6af7356711ffbed8270e03fff1499a9e4ca71805590c624025396  crates/base_train/src/packed_runtime_native_bootstrap_accumulation_wave_residency.rs
5ca75cd1d5d84893633f0ad6b6f5f147c2925c33dddee77b77364dec626523ac  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
625c5922d24bbe24d7a651a63398f6985634d529e6cc27ad0ed702c36c1443cb  crates/base_train/src/vram_hot_weight_page_residency.rs
16e0ea4613d936239a012821889daa95d73dea163f3683410bf4a7914f01ec83  tools/validate_ash_tensorcube_table_r4c_cf3_slot_lifecycle_static.py
73fef1b3869474d1e258a21d3a1c19bc2d582687763ed18c823abeb32c3eef1e  crates/base_train/src/tensorcube_table_r4c_cf7_partial_vram_hot_weight_reuse.rs
d0a390119f5a60881ef2fad70a56ca775e410151552ebf36ef168d9111c023c0  tools/validate_ash_tensorcube_table_r4c_cf7_partial_vram_hot_weight_reuse_static.py
```

## 18. Artifact Seals

```text
Overlay code-only ZIP
SHA-256 19a569a74cfd17bd0ee04e94d2de2c14681d3c17004d12904601c02e1cdff3f1
files=8
CRC=PASS

Full code-only ZIP
SHA-256 e072b07caaa1bf589d5c84dbbca176d56df83378a5ad279612bf530de0e7c851
files=8522
CRC=PASS
```

## 19. Evidence State

Bake environment has no Rust toolchain.

```text
SOURCE       BAKED
STATIC       PASS
COMPILE      UNVERIFIED IN BAKE ENVIRONMENT
RUNTIME      UNVERIFIED AFTER CF7
PHYSICAL     UNVERIFIED AFTER CF7
PERFORMANCE  UNVERIFIED
```

No compile or speedup claim is inferred from static evidence.

## 20. Local Compile Acceptance

```powershell
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo build -p base_train --bin base_train --release --locked -j 1
```

All must PASS.

## 21. Runtime Qualification

First:

```text
R0A = ACTIVE
R0B = ACTIVE
CF7 = OBSERVE
CF7_HOT_WEIGHT_BUDGET_BYTES = explicit bounded value
```

OBSERVE must establish exact logical hit/miss identity, budget plan, deterministic eviction, and no stale-hit candidate.

Then:

```text
CF7 = ACTIVE
```

Physical acceptance requires:

```text
forward_to_backward_lookup_count > 0
forward_to_backward_hit_count > 0
forward_to_backward_bytes_avoided > 0
peak_resident_bytes <= budget_bytes
duplicate_h2d_bytes = 0
generation/digest/runtime mismatch accepted count = 0
new D2H = 0
new cache-induced blocking wait = 0
CF11 source-retirement closure PASS
```

## 22. Performance Boundary

Same-source A/B compares:

```text
R0A + R0B + CF6 parent
vs
R0A + R0B + CF7 ACTIVE
```

Measure weight H2D bytes, queue.write_buffer bytes, weight upload count, forward/backward wall time, optimizer-step wall time, generation wall time, and peak VRAM.

No exact speedup claim is permitted before physical A/B.

## 23. Successor

After CF7 physical closure:

```text
TENSORCUBE-TABLE-R4C-CF8
RESIDENT VALIDATION RECEIPT CACHE

+ immutable generation/range identity
+ SHA validation once
+ finite validation once
+ repeated CPU full-range scan elimination
```

## 24. Final Law

> CF7 does not make the whole model permanently resident. It retains only exact forward-to-backward reusable decoder weights under an explicit bounded VRAM authority.

> A cache hit means the same generation, digest, representation, device, queue, and runtime identity. Anything else is a miss or fail-closed mismatch.

> Budget pressure causes deterministic eviction or canonical CF6 bypass, never hidden overcommit or a forced GPU idle.

> The cache remains execution residency only and never becomes commit, checkpoint, or durability authority.
