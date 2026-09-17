# EVE-MCU-R7A-CF9-CF4

## MUON WAVE-BOUNDED DEVICE SUCCESSOR
## + DIRECT HOST / DURABLE SUCCESSOR DEMOTION

**Revision:** `EVE-MCU-R7A-CF9-CF4`  
**Parent:** `EVE-MCU-R3H-CF10 + EVE-MCU-R7A-CF9-CF3A`  
**Parent full code-only SHA-256:** `e8d7a0f96f53f824097db87f65f26769a977acef92e2bf938008b010294063f2`  
**Class:** Muon device-residency cutover / direct canonical host successor / bounded D2H / A02 churn compaction

---

## 1. Problem statement

The physical run repeatedly showed the following allocation pattern before terminal failure:

```text
local_muon.*                 -> reuse-candidate
muon.assembly.weight.r2      -> frequently reuse-candidate
muon.assembly.momentum.r2    -> repeated new-local-page
muon.assembly.update.r2      -> repeated new-local-page
...
memory allocation of 2162688 bytes failed
```

Source inspection confirms that completed Muon W/M physical payloads can remain owned by:

```text
MuonDeviceSegmentedGenerationR1::segments
```

until generation closure. This conflicts with the intended Atlas streaming law:

```text
parameter N
  -> GPU compute
  -> physical completion / evidence
  -> successor transfer
  -> device retirement
  -> same pages reused by parameter N+1
```

### Evidence status before CF4

```text
CONFIRMED:
- completed Muon W/M can remain generation-wide GPU payload
- A02 repeatedly creates momentum/update assembly pages in the supplied physical run
- terminal run failed when a 2,162,688-byte host allocation was attempted

SUPPORTED:
- generation-wide Muon W/M retention materially contributes to residency/churn high-water

UNKNOWN:
- exact owner of the final 2,162,688-byte host allocation
```

---

## 2. CF4 ownership law

CF4 changes the target ActiveCompact + CF3A-direct production path to:

```text
GPU Muon W
  -> bounded D2H
  -> ResidentWeightPackBuilder canonical successor

GPU Muon M
  -> bounded D2H
  -> HiMuonMomentumAuthorityR8/R8A canonical host authority

GPU update
  -> existing BP-DK consumer closure
  -> release_parameter()

GPU W/M physical backing
  -> R3G2 prepared mutation evidence
  -> direct host write closure
  -> device release

completed generation
  -> descriptor + immutable R3G metadata only
```

The completed generation no longer needs live W/M `ArenaLease` payloads in the direct CF4 path.

---

## 3. Meaning-changing source authority cutover

Legacy behavior:

```text
committed_device_source.muon
= complete next-step Muon device source
```

Direct CF4 behavior:

```text
canonical host weight successor
+ canonical host HiMuon momentum authority
= next-step source authority

committed_device_source.muon
= None for direct-host-demoted CF4 generations
```

Next-step ActiveCompact source classification therefore admits:

```text
HOST_CANONICAL_CF4
```

when no committed segmented Muon device source exists and the B04 Atlas-wave RAM-canonical authority is active.

A direct-host-demoted CF4 metadata generation is explicitly rejected if code attempts to install it as a live device source:

```text
E_CF9_CF4_HOST_DEMOTED_GENERATION_IS_NOT_DEVICE_SOURCE
```

---

## 4. Exact implementation scope of this bake

This first CF4 bake intentionally activates direct Muon host demotion only when all of the following are true:

```text
Muon ActiveDeviceCandidate path
AND
non-ActiveAsync parameter path
AND
CF3A direct Adam/weight successor is active
AND
ResidentWeightPackBuilder is available
```

Therefore:

```text
ActiveCompact + CF3A direct
  -> CF4 direct host-demoted Muon successor

ActiveAsync / P5
  -> legacy device-generation path preserved in this bake
```

This prevents a silent semantic cutover of the async path before it receives its own bounded overlap implementation.

---

## 5. Canonical host destinations

CF4 does not create a second full-generation W/M host copy.

### Weight

Reuses:

```text
ResidentWeightPackBuilder
```

The mapped GPU tile is converted from Muon packed tile order into canonical model weight layout through the existing:

```text
write_successor_muon_tile_f32(...)
```

### Momentum

Reuses:

```text
HiMuonMomentumAuthorityR8 / R8A
```

Momentum is committed in 256-float tiles through the existing range-commit authority.

No generation-wide intermediate `Vec<f32>` is introduced for W or M.

---

## 6. Bounded D2H law

CF4 does not map an entire parameter W+M pair at once.

```text
CF4_COMPONENT_WINDOW_BYTES = 4 MiB

maximum component pair staging
= 4 MiB W + 4 MiB M
= 8 MiB
```

The same readback buffer is reused for successive chunks of the parameter.

For each chunk:

```text
W device range -> readback[0..chunk]
M device range -> readback[chunk..2*chunk]
map
canonical host writes
unmap
next chunk
```

No parameter-sized double staging is permitted.

---

## 7. No new large Rust host temporary

Momentum D2H is decoded tile-by-tile:

```text
256 f32
= 1 KiB stack tile
```

CF4 explicitly does **not** allocate a chunk-sized `Vec<f32>` for momentum.

This avoids creating a new multi-megabyte Rust heap allocation while repairing the memory high-water problem.

---

## 8. No new per-parameter CPU SHA hotpath

The first implementation draft considered hashing every mapped W/M byte on CPU. That was rejected.

CF4 does not perform a new per-parameter W/M SHA-256 pass.

The host-demotion receipt instead binds:

```text
canonical parameter identity
source/target generation
exact element/byte count
R3G2 prepared mutation receipts
bounded staging bytes
D2H submission count
retired device bytes
receipt digest over compact metadata
```

Canonical weight and momentum authorities keep their existing terminal identity/durability mechanisms.

This preserves the CF10 rule that hot success evidence must not re-grow into CPU checksum work.

---

## 9. R3G-before-retirement law

Before W/M device backing is released, CF4 creates exact R3G2 prepared mutation evidence for:

```text
MuonCandidateWeight
MuonCandidateMomentum
```

Each receipt must match:

```text
canonical_parameter_index
generation relation
logical byte length
physical allocation ordinal
submission completion
completion coverage
```

Only after the immutable receipts exist may:

```text
segment.release_in_place_close_r1()
```

retire the physical W/M arenas.

Historical physical allocation IDs remain evidence only, not live backing authority.

---

## 10. Update lifetime

The current ActiveCompact path already performs:

```text
BP-DK consume/update evidence
-> release_parameter(canonical_parameter_index)
```

CF4 preserves this order and performs W/M direct demotion only after that update evidence release point.

Expected direct CF4 terminal property:

```text
update_full_d2h_bytes=0
```

CF4 does not introduce a host full-update copy.

This bake does not claim a new persistent R3G update receipt. Persistent CF4 R3G2 metadata is for W/M successor mutation.

---

## 11. Metadata-only completed Muon generation

`MuonDeviceSegmentedGenerationR1` now separates:

```text
segments
  = currently live device payload only

published_descriptors
  = immutable parameter geometry/physical provenance

host_demoted_cf4
  = compact direct-host completion receipts
```

Direct CF4 completion requires:

```text
all expected descriptors published
all descriptors host-demoted
segments.is_empty()
```

The completed generation ledger therefore keeps metadata without retaining W/M GPU payload.

---

## 12. Full-trainable projection integration

Legacy full projection reads Muon candidate W from live Muon segment buffers.

Direct CF4 instead requires:

```text
full.muon.direct_host_demoted_cf4() == true
full.adamw.direct_host_demoted_cf3a() == true
ResidentWeightPackBuilder present
```

The projection reads the already-initialized canonical successor bytes using:

```text
copy_initialized_bytes_at_cf3a(...)
```

No late resurrection of Muon W device segments is allowed.

---

## 13. Commit / rotation integration

For direct CF4:

```text
new full generation commit
-> host W/M authorities already contain successor
-> drop CF4 metadata generation after commit handoff
-> committed_device_source.muon = None
```

Legacy/non-CF4 generations retain their previous device-source rotation behavior.

---

## 14. A02 success-log compaction

The following high-cardinality successful allocation diagnostics are disabled by default:

```text
[reuse-candidate]
[new-local-page]
[cross-subgroup-skip]
```

They can be explicitly re-enabled for qualification with:

```text
ASH_A02_VERBOSE_ACQUIRE_DIAGNOSTICS=1
```

Telemetry counters remain active regardless of logging.

CF4 binds an A02 telemetry baseline when the Muon target generation opens and reports generation-local deltas at terminal.

---

## 15. CF4 terminal receipt

Direct CF4 emits one generation summary:

```text
[ASH-MCU-R7A-CF9-CF4][muon-wave-bounded-successor]
```

Fields include:

```text
source_generation
target_generation
expected_parameter_count
published_parameter_count
expected_element_count
written_weight_elements
written_momentum_elements
weight_d2h_bytes
momentum_d2h_bytes
update_full_d2h_bytes
d2h_submission_count
bounded_staging_peak_bytes
live_segment_count
logical_device_retired_bytes
a02_generation_reuse_count
a02_generation_new_page_count
host_successor_complete
admitted
```

Direct success requires:

```text
published_parameter_count == expected_parameter_count
written_weight_elements == expected_element_count
written_momentum_elements == expected_element_count
weight_d2h_bytes == momentum_d2h_bytes
weight_d2h_bytes > 0
update_full_d2h_bytes == 0
bounded_staging_peak_bytes <= 8388608
live_segment_count == 0
logical_device_retired_bytes == weight_d2h_bytes + momentum_d2h_bytes
host_successor_complete == true
admitted == true
```

---

## 16. Performance boundary

CF4 targets residency and allocation churn.

It does **not** yet remove the synchronous per-chunk:

```text
copy
-> map_async
-> poll completion
-> host consume
```

barrier.

Therefore:

```text
VRAM / ownership improvement
= target of CF4

GPU utilization / compute-D2H overlap
= future async pipeline work (CF3B or successor)
```

No claim is made that CF4 alone reaches the project target:

```text
base_train <= ~120 seconds / optimizer step
```

---

## 17. Changed files

```text
MOD crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
MOD crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
MOD crates/base_train/src/unified_atlas_mcu_bp_dk_device_resident_post_update_segmented_successor_r1.rs
MOD crates/burn_webgpu_backend/src/usage_segregated_buffer_arena.rs
ADD tools/validate_ash_eve_mcu_r7a_cf9_cf4_muon_wave_bounded_device_successor_static.py
```

No other source file is changed by the overlay.

---

## 18. Source SHA-256

```text
344518e8d81cfb43b4591555213bb68cf4907f5465d448a2255bcd6ba5d19206  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
3debc5734ff7ba898bd40c0bdda14d6e0835fbdb968a72b7619f0351f369e50a  crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
fe91650d562222e0959f48d995edf8b53f116902cc5eb8e5a7c9101185bda999  crates/base_train/src/unified_atlas_mcu_bp_dk_device_resident_post_update_segmented_successor_r1.rs
bef8eec545be13c656695282f454d00ce3666359d8b38b7eec31b9bbd999c577  crates/burn_webgpu_backend/src/usage_segregated_buffer_arena.rs
c00b38b868b8a8a43632fa7bc32da554a68a8d4f5f017fbceb8413a837299d4b  tools/validate_ash_eve_mcu_r7a_cf9_cf4_muon_wave_bounded_device_successor_static.py
```

---

## 19. Artifact seals

Overlay:

```text
ASH_EVE_MCU_R7A_CF9_CF4_MUON_WAVE_BOUNDED_DEVICE_SUCCESSOR_OVERLAY_CODE_ONLY.zip
SHA-256 2d9c9bdc07037e1ad56be56d4713901dc5b52c25faac8ff8bed21a0c694aa256
FILES 5
CRC PASS
```

Full:

```text
ASH_PASS3_EVE_MCU_R7A_CF9_CF4_MUON_WAVE_BOUNDED_DEVICE_SUCCESSOR_CODE_ONLY.zip
SHA-256 4254f5a46f360e9e1d898050a6353c1cab3059bf41baa92a0934b66eeb561347
FILES 8432
CRC PASS
```

Archive exclusions:

```text
specs/       0
artifacts/   0
manifests/   0
Markdown     0
__pycache__  0
*.pyc        0
```

The full archive preserves `Cargo.toml` and `Cargo.lock`.

---

## 20. Static qualification performed in bake environment

```text
PASS_EVE_MCU_R7A_CF9_CF4_MUON_WAVE_BOUNDED_DEVICE_SUCCESSOR_STATIC checks=47
PASS_EVE_MCU_R3H_CF10_GPU_RESIDENT_EVIDENCE_REDUCTION_STATIC
PASS_ASH_EVE_HIMUON_FULL_TRAINABLE_GENERATION_COMMIT_PERMIT_JOIN_AND_ATOMIC_ADAM_MUON_WEIGHT_PROMOTION_CLOSURE_R3C_STATIC
PASS_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_TRANSACTIONAL_ADAM_AB_CANDIDATE_OVERLAY_AND_RESIDENT_WEIGHT_SUCCESSOR_HEADROOM_CLOSURE_R1_STATIC
```

Python validator AST parsing also passed.

A lightweight delimiter scan of all four modified Rust files found balanced Rust delimiters.

---

## 21. Known parent validator drift

The following validators already fail against the unmodified CF10 parent and are therefore not attributed to CF4:

```text
validate_ash_basetrain_unified_atlas_mcu_bp_dk_device_resident_post_update_segmented_successor_r1_static.py
  ACTIVE_DEVICE_CHILD_CONTAINS_EXACT_WAIT

validate_ash_basetrain_unified_atlas_mcu_local_muon_device_segmented_source_direct_submit_r1_static.py
  DIRECT_SOURCE_CHILD_CONTAINS_EXACT_WAIT

validate_ash_eve_himuon_full_trainable_generation_production_atomic_cutover_r3c1_static.py
  25/30 PASS on both parent and CF4 bake
```

These remain baseline debt and are not represented as CF4 PASS tokens.

---

## 22. Compile / runtime status

The bake environment does not contain `cargo`, `rustc`, or `rustfmt`.

Therefore:

```text
SOURCE:       APPLIED
STATIC:       PASS
ARCHIVE CRC:  PASS
RUST COMPILE: NOT RUN
WGSL COMPILE: NOT RUN
RUNTIME:      NOT RUN
PHYSICAL:     NOT RUN
PERFORMANCE:  UNMEASURED
```

No compile/runtime/physical/performance claim is made by this artifact.

No new `cf9_cf4_` Rust unit-test filter is claimed in this first bake. Do not treat a zero-test cargo invocation as qualification.

---

## 23. Physical acceptance

A direct CF4 campaign is admitted only when the generation terminal summary proves:

```text
live_segment_count=0
update_full_d2h_bytes=0
bounded_staging_peak_bytes <= 8388608
weight_d2h_bytes == momentum_d2h_bytes
weight_d2h_bytes > 0
logical_device_retired_bytes == weight_d2h_bytes + momentum_d2h_bytes
host_successor_complete=true
admitted=true
```

The default run must also show zero per-acquire A02 success diagnostics unless explicitly enabled:

```text
[reuse-candidate]
[new-local-page]
[cross-subgroup-skip]
```

The authoritative reuse/churn measurement is the terminal generation delta:

```text
a02_generation_reuse_count
a02_generation_new_page_count
```

Physical comparison should verify that new-page growth no longer rises linearly with completed Muon parameter count.

---

## 24. Promotion tokens

Static/source:

```text
PASS_EVE_MCU_R7A_CF9_CF4_MUON_WAVE_BOUNDED_DEVICE_SUCCESSOR_STATIC
```

Compile, only after user-side cargo qualification:

```text
PASS_EVE_MCU_R7A_CF9_CF4_MUON_WAVE_BOUNDED_DEVICE_SUCCESSOR
```

Physical, only after a real campaign:

```text
PASS_EVE_MCU_R7A_CF9_CF4_PHYSICAL
```

Performance, only after measured before/after:

```text
PASS_EVE_MCU_R7A_CF9_CF4_MEASURED_RESIDENCY_REDUCTION
```

Otherwise:

```text
HOLD_EVE_MCU_R7A_CF9_CF4_UNPROVEN
```

---

## 25. Final law

> A completed Muon parameter is successor state, not permanent GPU residency.
>
> Direct CF4 writes W/M into the already-existing canonical host authorities, captures immutable W/M R3G evidence, retires the physical device payload, and leaves only metadata behind.
>
> Update remains transient and is not copied wholesale to host.
>
> CF4 introduces no parameter-sized host staging, no chunk-sized momentum `Vec<f32>`, and no new per-parameter CPU SHA-256 success chain.
>
> The ActiveAsync/P5 path is intentionally not claimed as CF4-direct in this bake.
