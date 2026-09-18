# EVE-MCU-R3H-CF11-R1

## BOUNDED COW WORKSPACE ADMISSION
## + BOUNDED INITIALIZED-RANGE VERIFICATION
## + SOURCE-RETIREMENT PHYSICAL RESIDENCY CLOSURE

```text
+ NO FULL CANDIDATE W RESERVATION REINTRODUCTION
+ NO OPTIMIZER NUMERICAL CHANGE
+ NO R3C ATOMIC PROMOTION CHANGE
```

---

## 0. Revision

```text
Patch ID:
EVE-MCU-R3H-CF11-R1

Class:
HOST MEMORY ADMISSION CLOSURE
PAGED-COW WORKSPACE BOUND
INITIALIZED-RANGE VERIFY SCRATCH BOUND
SOURCE -> SUCCESSOR OWNERSHIP ORDERING CLOSURE
```

Direct parent:

```text
EVE-MCU-R3H-CF11
+ Compilefix-1 successor builder reborrow
+ Compilefix-2 CF10 backend ABI packaging
```

Parent full code-only SHA-256:

```text
018af076ecc8592208b0cf53667f63cca7b35fee3fdd62e4c453b11c3cab13a7
```

Parent GitHub spec head inspected before this bake:

```text
1596cd2e77e8a15e4e7cfeee436c5b83f4b3e16f
spec: close CF11 CF10 backend ABI packaging
```

---

## 1. Scope

CF11 already removed the second complete step-time candidate weight heap from the direct ActiveVerified + CF3A path.

R1 does not redesign that successor path.

R1 closes the remaining host-memory admission and ordering gaps:

```text
A. CF11 future workspace ceiling is RAM36-admitted before COW allocation begins.

B. append_or_verify_initialized() no longer allocates verify_len-sized temporary memory
   on the PagedCowCf11 path.

C. CF11 workspace reservation is released on both success and failure paths.

D. source host ownership retirement and successor full ResidentWeightPack reservation
   are bound by monotonic RAM36 event ordering.
```

---

## 2. Evidence Boundary

At bake time:

```text
SOURCE               APPLIED
STATIC               PASS
ARCHIVE CRC           PASS
RUST COMPILE          NOT RUN - Rust toolchain unavailable in bake environment
RUST TEST             NOT RUN
RUNTIME               NOT RUN
PHYSICAL              NOT RUN
PERFORMANCE           UNMEASURED
```

Historical allocation attribution remains unchanged:

```text
historical 512 MiB allocation exact owner              UNKNOWN
historical objective-probe activation at that failure UNKNOWN
```

No R1 conclusion promotes those historical failures to a proven CF11 owner.

---

## 3. Frozen CF11 Geometry

Preserved:

```text
CF11_PAGE_BYTES              = 67,108,864 bytes   (64 MiB)
CF11_MAX_DIRTY_RAM_PAGES     = 4
CF11_MAX_DIRTY_RAM_BYTES     = 268,435,456 bytes  (256 MiB)
```

New R1 verification bound:

```text
CF11_INITIALIZED_VERIFY_SCRATCH_BYTES_R1
= RESIDENT_WEIGHT_PACK_LOAD_CHUNK_BYTES
= 16,777,216 bytes
= 16 MiB
```

Execution workspace bound:

```text
256 MiB dirty cache
+ 16 MiB initialized-range verify scratch
= 272 MiB
= 285,212,672 bytes
```

Frozen authority:

```text
CF11_EXECUTION_WORKSPACE_BOUND_BYTES_R1 = 285,212,672
CF11_WORKSPACE_ADMISSION_BOUND_BYTES_R1 = 285,212,672
```

---

## 4. Final Merge Geometry Clarification

The CF11 final merge creates its page buffer at the resident load chunk size, but for a production 64 MiB page it executes:

```text
if page_buf.len() < page_len:
    page_buf.resize(page_len, 0)
```

Therefore the actual production maximum is:

```text
page merge scratch = 64 MiB
BufWriter           = 16 MiB
----------------------------
final merge bound   = 80 MiB
```

R1 freezes:

```text
CF11_FINAL_MERGE_PAGE_SCRATCH_BYTES_R1   = 64 MiB
CF11_FINAL_MERGE_WRITER_BUFFER_BYTES_R1  = 16 MiB
CF11_FINAL_MERGE_WORKSPACE_BOUND_BYTES_R1= 80 MiB
```

The admission ceiling remains 272 MiB because the execution bound is larger than the final-merge bound.

---

## 5. RAM36 Owner

R1 adds one exact owner:

```text
HostRamOwner::ResidentWeightPagedCowWorkspaceCf11R1
```

It is intentionally distinct from:

```text
HostRamOwner::ResidentWeightPack
```

The CF11 workspace is not another resident weight generation.

---

## 6. Admission Ordering

On the production CF11 path:

```text
bind optimizer / generation attribution
    -> projection_snapshot_r1(272 MiB)
    -> RAM36 reserve ResidentWeightPagedCowWorkspaceCf11R1 272 MiB
    -> ResidentWeightPackBuilder::new_paged_cow_cf11(...)
    -> candidate execution
```

Admission failure is fail-closed:

```text
E_CF11_R1_WORKSPACE_ADMISSION_REJECTED
```

Forbidden:

```text
CF11 admission rejection -> legacy full candidate builder fallback
CF11 admission rejection -> continue without reservation
CF11 admission rejection -> silent page-count reduction
```

---

## 7. No Full Candidate W Reservation Reintroduction

The CF11 successor branch still returns:

```text
successor_reservation = None
```

for the step-time full ResidentWeightPack authority.

The new reservation is only:

```text
ResidentWeightPagedCowWorkspaceCf11R1 = 272 MiB
```

The full next-step ResidentWeightPack reservation is still created only after source retirement in:

```text
cf11_successor_reservation_after_source_retirement
```

---

## 8. Conservative Admission Semantics

The R1 workspace reservation remains in `Admitted` state while the COW workspace runs.

Therefore RAM36 may conservatively count:

```text
observed process-private workspace bytes
+
full 272 MiB unmaterialized reservation
```

for part of the step.

This is intentional fail-closed over-accounting.

R1 does not claim exact live/residual reservation reconciliation.

If this conservative admission produces a false rejection in physical testing, a later revision may introduce exact residual workspace reconciliation. R1 does not do so preemptively.

---

## 9. Failure-Safe Workspace Release

The candidate projection body is wrapped as one scoped result.

Required structure:

```text
reserve CF11 workspace
    -> run candidate projection / COW seal
    -> capture Result<PackedCandidateOutput>
    -> release workspace reservation
    -> return original result or release failure
```

This ensures the CF11 workspace reservation is released when:

```text
builder creation fails
page materialization fails
spool operation fails
candidate projection fails
final candidate seal fails
normal candidate projection succeeds
```

Release failure is explicit:

```text
E_CF11_R1_WORKSPACE_RESERVATION_LEAK
```

If both the primary operation and release fail, both are retained in the returned error context.

---

## 10. Bounded Initialized-Range Verification

Parent behavior on a preinitialized interval allocated:

```rust
let mut existing = vec![0u8; verify_len];
```

For `PagedCowCf11`, R1 changes this to bounded chunk verification:

```text
scratch <= 16 MiB

while verified < verify_len:
    chunk = min(remaining, 16 MiB)
    read candidate bytes into scratch[0..chunk]
    exact compare to incoming bytes
    advance
```

The legacy `Full(Vec<u8>)` builder preserves the parent interval-sized behavior.

R1 therefore changes only the CF11 paged production representation.

---

## 11. Verification Semantics Preservation

R1 does not change:

```text
byte order
append cursor
initialized range coverage
SHA input order
candidate SHA-256
source inheritance semantics
random write semantics
```

Any mismatch remains fatal:

```text
ResidentWeightPackBuilderPreinitializedByteMismatch
```

R1 additionally tracks:

```text
initialized_verify_total_bytes_r1
initialized_verify_chunk_count_r1
initialized_verify_scratch_peak_bytes_r1
initialized_verify_mismatch_count_r1
```

Admission requires:

```text
initialized_verify_scratch_peak_bytes_r1 <= 16 MiB
initialized_verify_mismatch_count_r1 == 0
```

---

## 12. Existing COW Semantics Preserved

No change to:

```text
partial first write -> source/spool materialization -> overwrite
full page overwrite -> fresh candidate page -> no source clone
packed dirty-page spool
eviction policy
random-order CF3A Adam W writes
random-order CF4 Muon W writes
canonical page-order final merge
candidate-file SHA seal
```

Dirty RAM remains:

```text
peak_dirty_ram_pages <= 4
peak_dirty_ram_bytes <= 256 MiB
```

---

## 13. Workspace Receipt

R1 adds:

```text
Cf11R1WorkspaceAdmissionReceipt
```

Fields bind:

```text
source / target generation and optimizer step
workspace owner
workspace reservation id
272 MiB admission bound
256 MiB dirty cache bound
16 MiB verify scratch bound
80 MiB final merge bound
private bytes at admission
projected bytes at admission
private bytes at release
RAM36 release event sequence
peak dirty page count / bytes
verification counters
full candidate heap allocation count
workspace admitted / released
receipt digest
```

Terminal log:

```text
[ASH-EVE-MCU-R3H-CF11-R1][workspace-residency-closure]
```

---

## 14. Source Last-Use Authority Preservation

Existing R3H gate remains:

```text
source_pack.backing_strong_count() == 1
live_alias_count == 0
reader_closed == true
```

R1 does not weaken it.

Application-level source ownership retirement remains distinct from proof of immediate Windows allocator page decommit.

---

## 15. RAM36 Event Ordering Closure

R1 exposes the current RAM36 event count through:

```text
HostProcessRamBudget::event_sequence_r1()
```

The runtime records:

```text
workspace_release_event_sequence
source_retirement_event_sequence
successor_reservation_event_sequence
```

Required:

```text
workspace_release_event_sequence < successor_reservation_event_sequence
source_retirement_event_sequence < successor_reservation_event_sequence
```

This is an application/RAM36 ordering claim.

It is not a claim that Windows physically decommitted every old source page before the next allocation.

---

## 16. Source-Retirement Closure Receipt

R1 adds:

```text
Cf11R1SourceRetirementClosureReceipt
```

It binds:

```text
workspace reservation id
source reservation id
successor reservation id
workspace release sequence
source retirement sequence
successor reservation sequence
source strong count at last use
source live alias count
source reservation release
candidate SHA-256
```

Persisted runtime receipt:

```text
eve_mcu_r3h_cf11_r1_workspace_residency_closure.json
```

Terminal log:

```text
[ASH-EVE-MCU-R3H-CF11-R1][source-retirement-closure]
```

---

## 17. No Numerical / R3C Change

R1 changes no:

```text
AdamW arithmetic
Muon / HiMuon arithmetic
learning rate
weight decay
gradient semantics
candidate Adam M/V representation
WGSL
Device / Queue authority
R3C prepare / apply atomic promotion semantics
checkpoint format
dataset/tokenizer
```

The pre-existing R3C1 validator drift is unchanged:

```text
parent: 25/30 PASS
R1:     25/30 PASS
```

Same five parent checks remain failed:

```text
scheduler precomputes seal
single tail eve no fail
single tail muon b06 no fail
single tail weight no fail
generation seal installed last
```

This is not promoted as an R1 regression.

---

## 18. Modified Files

```text
MOD crates/base_train/src/ram36_process_budget.rs
MOD crates/base_train/src/ram_weight_pack_persistent_residency.rs
MOD crates/base_train/src/resident_weight_replacement_authority_r3h.rs
MOD crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
ADD tools/validate_ash_eve_mcu_r3h_cf11_r1_bounded_cow_workspace_static.py
```

No WGSL file changes.

No optimizer kernel changes.

---

## 19. Source SHA-256

```text
40134763d9f75d27d44d3ac8fb8f3a62904497991f7e58f4218c0332b1cf79d6  crates/base_train/src/ram36_process_budget.rs
42b57a09968e15c2d84171345e625653ff3fdc7ab4a94ff35c0af8dbe3559b80  crates/base_train/src/ram_weight_pack_persistent_residency.rs
a0368f39edc1061550924d9adbca1d4abe6a4ea0f2a3a6b6b377de72c9c418c5  crates/base_train/src/resident_weight_replacement_authority_r3h.rs
500ba42648b425d5acae9217dc7bc466198f4b7985a62c29d7d64baafea429c1  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
f91b03d7e90bf28943d00ecab1e95895b2228cab2a824bc7047f6b8ee41dd2ee  tools/validate_ash_eve_mcu_r3h_cf11_r1_bounded_cow_workspace_static.py
```

---

## 20. Static Qualification

Passed in bake environment:

```text
PASS_EVE_MCU_R3H_CF11_R1_BOUNDED_COW_WORKSPACE_STATIC checks=20
PASS_EVE_MCU_R3H_CF11_PAGED_COW_CANDIDATE_WEIGHT_SUCCESSOR_STATIC checks=64
PASS_EVE_MCU_R7A_CF9_CF4_MUON_WAVE_BOUNDED_DEVICE_SUCCESSOR_STATIC checks=47
PASS_EVE_MCU_R7A_CF9_CF3A_DIRECT_HOST_DEMOTION_STATIC
PASS_EVE_MCU_R3H_CF10_GPU_RESIDENT_EVIDENCE_REDUCTION_STATIC
PASS_ASH_BASETRAIN_RAM36_SUCCESSOR_WEIGHT_RESERVATION_PHYSICAL_ALLOCATION_OWNERSHIP_TRANSITION_CLOSURE_R1_STATIC
PASS_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_TRANSACTIONAL_ADAM_AB_CANDIDATE_OVERLAY_AND_RESIDENT_WEIGHT_SUCCESSOR_HEADROOM_CLOSURE_R1_STATIC
```

R3C1 inherited baseline:

```text
25/30 PASS on parent
25/30 PASS on R1
```

---

## 21. Rust Tests Added

Prefix:

```text
r3h_cf11_r1_
```

Added:

```text
r3h_cf11_r1_verify_large_initialized_range_is_chunk_bounded
r3h_cf11_r1_verify_mismatch_across_chunk_boundary_rejected
r3h_cf11_r1_workspace_geometry_is_bounded
```

The first verification fixture is larger than 16 MiB and therefore cannot pass through a single bounded verify chunk.

These tests were added at source level but were not executed in the bake environment because no Rust toolchain is installed.

---

## 22. Code-Only Artifacts

Overlay:

```text
ASH_EVE_MCU_R3H_CF11_R1_BOUNDED_COW_WORKSPACE_ADMISSION_OVERLAY_CODE_ONLY.zip
SHA-256 7567e7a1a505048f57a905395e8a5f3847743275d0b4a646f8432f0751f4cc68
FILES 5
CRC PASS
```

Full:

```text
ASH_PASS3_EVE_MCU_R3H_CF11_R1_BOUNDED_COW_WORKSPACE_ADMISSION_CODE_ONLY.zip
SHA-256 00df8604da109e73ad5b2aa398df0bf14e81862c4e63377439c66d4536202b83
FILES 8434
CRC PASS
```

Both ZIPs exclude:

```text
specs/      0
artifacts/  0
manifests/  0
Markdown    0
__pycache__ 0
*.pyc       0
```

The Full ZIP retains normal build inputs including:

```text
Cargo.toml
Cargo.lock
```

---

## 23. Compile Acceptance

Required user-side validation:

```powershell
cargo check `
  -p base_train `
  --lib `
  --release `
  --locked `
  -j 1
```

Then:

```powershell
cargo test `
  -p base_train `
  --lib `
  --release `
  --locked `
  -j 1 `
  r3h_cf11_r1_ `
  -- `
  --nocapture
```

Zero discovered tests is not PASS.

Parent regression:

```powershell
cargo test `
  -p base_train `
  --lib `
  --release `
  --locked `
  -j 1 `
  r3h_cf11_ `
  -- `
  --nocapture
```

---

## 24. Physical Acceptance

A production CF11-R1 step is physically admitted only when the real campaign proves:

```text
workspace admission receipt present
workspace owner == ResidentWeightPagedCowWorkspaceCf11R1
workspace admission bound == 285,212,672
workspace released == true

full_candidate_heap_allocation_count == 0
peak_dirty_ram_pages <= 4
peak_dirty_ram_bytes <= 268,435,456
initialized_verify_scratch_peak_bytes <= 16,777,216
initialized_verify_mismatch_count == 0
candidate SHA exact

source_backing_strong_count_at_last_use == 1
source_live_alias_count_at_last_use == 0
source reservation released == true

workspace_release_sequence < successor_reservation_sequence
source_retirement_sequence < successor_reservation_sequence

post-retirement full ResidentWeightPack materializes successfully

no OutOfMemory
no DeviceLost
no WGPU Validation Error
```

Absence of a failure is not sufficient evidence by itself.

---

## 25. Multi-Generation Gate

One successful replacement does not prove absence of accumulation.

Required later campaign:

```text
generation N -> N+1 -> N+2 -> ...
```

Verify each generation returns to:

```text
CF11 workspace active reservation count = 0 after candidate seal
old resident source reservation retired before successor reserve
one canonical ResidentWeightPack after promotion
no CF11 dirty-page lifetime accumulation
no stale workspace reservation accumulation
```

---

## 26. Promotion Tokens

```text
PASS_EVE_MCU_R3H_CF11_R1_BOUNDED_COW_WORKSPACE_STATIC
PASS_EVE_MCU_R3H_CF11_R1_COMPILED
PASS_EVE_MCU_R3H_CF11_R1_PHYSICAL
PASS_EVE_MCU_R3H_CF11_R1_MULTI_GENERATION_RESIDENCY
HOLD_EVE_MCU_R3H_CF11_R1_UNPROVEN
```

Evidence ladder remains:

```text
SOURCE < STATIC < COMPILE < RUNTIME < PHYSICAL < PERFORMANCE < PROMOTED
```

---

## 27. Final Law

> CF11-R1 does not reintroduce a second full candidate weight reservation.

> The step-time candidate remains source inheritance plus at most four 64 MiB dirty pages and the packed dirty-page spool.

> The CF11 future workspace is fail-closed admitted under a dedicated 272 MiB RAM36 owner before the paged builder opens.

> Paged initialized-range verification remains byte-exact while its temporary scratch is bounded to 16 MiB.

> The final canonical merge remains bounded to 64 MiB page scratch plus 16 MiB BufWriter, for an 80 MiB explicit merge workspace.

> The CF11 workspace reservation is released on both success and failure return paths before later full successor reservation.

> Existing source `Arc` last-use authority remains exact: strong count 1, live alias count 0.

> RAM36 event order must prove both workspace release and source reservation retirement precede the full successor reservation.

> Application ownership retirement is not automatically promoted to proof of immediate operating-system page decommit.

> No optimizer numerical semantics, WGSL, R3C atomic promotion semantics, checkpoint format, dataset or tokenizer semantics change in this revision.
