# EVE-MCU-R7A-CF9-CF2

## PHYSICAL FREE-PAGE TRIM + BOOTSTRAP WARM-POOL RETENTION

**Revision:** `EVE-MCU-R7A-CF9-CF2`  
**Parent code:** `EVE-MCU-R3H-CF8`  
**Class:** physical VRAM reclamation / free-page retention bound / allocation-registry retirement

```text
+ LOGICAL LEASE RECLAIM PRESERVED
+ FREE R7A PAGE PHYSICAL DESTROY
+ A01 PHYSICAL ALLOCATION REGISTRY RETIREMENT
+ BOOTSTRAP VRAM WARM-POOL TARGET PRESERVED ACROSS RESEAL
+ CURRENT / FREE / DESTROYED VRAM ACCOUNTING
+ NO DEVICE / QUEUE RECONSTRUCTION
+ NO LIVE PAGE DESTROY
+ NO CANDIDATE HOST DEMOTION CLAIM
```

---

## 1. Purpose

The parent R7A arena returned completed leases to a reusable free page but retained the underlying `Arc<wgpu::Buffer>` indefinitely. Consequently a session could preserve its arena high-water VRAM even after pages were logically free.

CF9-CF2 adds a second reclamation stage:

```text
submission completion
→ logical lease reclaim
→ page.in_use = false
→ free-page trim eligibility
→ remove page from arena pool
→ retire A01 physical allocation registry entry
→ Buffer::destroy()
→ drop Arc<wgpu::Buffer>
→ decrement retained bytes / page count
```

This revision intentionally does **not** claim that the generation-wide Adam candidate W/M/V residency has been moved to CPU RAM. Those pages are still live while `AdamWDeviceSegmentedGenerationR1` owns them and therefore are not trim-eligible. Candidate host demotion remains the next residency revision.

---

## 2. Parent problem

Parent reclaim ended at:

```text
page.in_use = false
active_lease_count -= 1
```

The page remained in `ArenaRuntime.pools` and retained its `Arc<wgpu::Buffer>`.

Therefore:

```text
logical free != physical VRAM return
```

CF9-CF2 closes only the physical free-page half of that gap.

---

## 3. Physical retention target

The session's original R7A arena budget is captured before CF9 resource reseal:

```text
arena_physical_retain_target_bytes = initial config.arena_budget_bytes
```

For the current physical campaign this is expected to be the bootstrap `512 MiB` arena budget.

CF9 may still reseal `max_retained_bytes` upward for current generation geometry. CF9-CF2 does **not** use the resealed generation-wide limit as the warm free-pool target.

Instead:

```text
admission ceiling          = resealed CF9 resource budget
physical free-page target  = original bootstrap arena budget
```

The physical target is registered against every replacement R7A domain created by CF8/CF9 reseal.

---

## 4. Trim law

A page is trim-eligible only when all of the following are true:

```text
page.in_use == false
page.r7a_domain_digest == current domain
A01 physical allocation exists
no A01 Live lease references the allocation
current retained bytes > physical retain target
```

Free pages are considered largest-first, with page ordinal as deterministic tie-break.

Trim stops once:

```text
retained_bytes <= physical_retain_target_bytes
```

or no eligible free page remains.

Live pages are never destroyed merely to satisfy the target.

---

## 5. Allocation registry retirement

CF9-CF2 adds:

```text
assert_owned_physical_allocation_retirable
retire_owned_physical_allocation
```

Retirement fails closed when:

```text
allocation is unknown
or
any Live logical lease still references it
```

The A01 allocation→queue binding is removed before the destroyed page can be mistaken for a valid owned allocation later.

---

## 6. Lock-order / destruction law

`Buffer::destroy()` is not executed while holding the arena mutex.

The sequence is:

```text
A02 snapshot / candidate selection
→ A01 retirable preflight
→ A02 pool removal + accounting
→ release A02 lock
→ A01 registry retirement
→ Buffer::destroy()
```

This avoids introducing an A02-held physical destruction path and prevents the destroyed page from remaining discoverable in the reusable pool.

---

## 7. Accounting

`McuArenaTelemetryR7A` now includes:

```text
free_retained_bytes
physical_destroy_count
physical_destroyed_bytes
```

`McuArenaResourceStateSnapshotR7A` now includes:

```text
physical_retain_target_bytes
free_retained_bytes
physical_destroy_count
physical_destroyed_bytes
```

On successful physical trim:

```text
retained_bytes      -= destroyed bytes
page_count          -= destroyed pages
physical_destroy_*  += exact destroyed amount
```

Peak retained bytes remain historical high-water telemetry and are not decremented.

---

## 8. Runtime receipt

The generation resource summary marker becomes:

```text
[ASH-MCU-R7A-CF9-CF2][generation-resource-summary]
```

with additional fields:

```text
physical_retain_target_bytes
free_retained_bytes
physical_destroy_count
physical_destroyed_bytes
```

Each destroyed page may emit:

```text
[ASH-MCU-R7A-CF9-CF2][physical-free-page-trim]
```

containing only bounded scalar allocation/page identity and destroyed byte count.

---

## 9. Preserved execution semantics

CF9-CF2 does not modify:

```text
AdamW optimizer mathematics
Muon / HiMuon mathematics
WGSL
Device authority
Queue authority
pipeline cache
submission ordering
R3G completion-before-reuse
R3B target RAM writeback
CF6 packed-span validation
CF8 runtime evidence compaction
candidate generation digest
B06 generation ticket semantics
```

Logical lease reclaim still requires exact tracked completion before a page can become free.

---

## 10. Explicit non-closure

The current source still owns completed AdamW candidate GPU segments in:

```text
AdamWDeviceSegmentedGenerationR1
```

until the full device generation is consumed.

Therefore CF9-CF2 does **not** satisfy the final desired law:

```text
VRAM = wave-local candidate working set
CPU RAM = full candidate W/M authority
```

It only ensures that once a page becomes free, excess free VRAM is physically returned rather than retained indefinitely.

Next required revision:

```text
EVE-MCU-R7A-CF9-CF3
GPU → HOST CANDIDATE DEMOTION
+ WAVE-BOUNDED DEVICE CANDIDATE RESIDENCY
```

That revision must change the full-device-generation ownership contract rather than merely shrinking an arena budget number.

---

## 11. Source delta

```text
ADD 0
MOD 4
DEL 0
```

Modified:

```text
crates/burn_webgpu_backend/src/buffer_submission_lease.rs
crates/burn_webgpu_backend/src/usage_segregated_buffer_arena.rs
crates/base_train/src/mcu_device_resource_runtime_r7a.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

Source SHA-256 after bake:

```text
buffer_submission_lease.rs
2fb1df20664435104606723b5436daed79b5a492780159dadeef158018fe548a

usage_segregated_buffer_arena.rs
586226aeeffa8f297e53e7d5de15bbe8746b94705a6919b37156ff052b2b0537

mcu_device_resource_runtime_r7a.rs
39a86c45e9787c0a8ff85148a14e877a5a44196a5bf1368b5a7f49b167894b37

production_multistep_loop_accumulation8_scheduler.rs
73474c21ddc3b268ff47c301ecf2e4db1a20ad84bbadaa149be9f8328f616375
```

---

## 12. Code-only archives

Parent full code-only archive:

```text
ASH_PASS3_EVE_MCU_R3H_CF8_PRODUCTION_RUNTIME_EVIDENCE_COMPACTION_CODE_ONLY.zip
SHA-256 b7dcf05dbe80f4511c420f95eafcf393310c150caeb594794ca17ca8b3f6bde9
```

Overlay:

```text
ASH_EVE_MCU_R7A_CF9_CF2_PHYSICAL_FREE_PAGE_TRIM_OVERLAY_CODE_ONLY.zip
SHA-256 cb314f12be44e004cc7341be1946852d24965f24f877b44e265ef82f1a3a38e7
FILES 4
CRC PASS
```

Full applied code-only:

```text
ASH_PASS3_EVE_MCU_R7A_CF9_CF2_PHYSICAL_FREE_PAGE_TRIM_CODE_ONLY.zip
SHA-256 400e94cdd7c4cdab2774dfa8d279f60bafe84eeecb4f044bd588d08213adf060
FILES 8426
CRC PASS
```

Both code-only archives contain:

```text
specs/       0
artifacts/   0
manifests/   0
Markdown     0
```

Build inputs such as `Cargo.toml` and `Cargo.lock` remain in the full archive.

---

## 13. Qualification

Added source test:

```text
r7a_physical_retain_target_is_stable_cf9_cf2
```

Required user-side qualification:

```powershell
cargo test -p burn_webgpu_backend --lib --release --locked r7a_physical_retain_target_is_stable_cf9_cf2 -- --nocapture
cargo test -p base_train --lib --release --locked r3h_cf8_ -- --nocapture
cargo build -p base_train --bin base_train --release --locked -j 1
```

Physical qualification requires an R7A physical run and inspection of:

```text
[ASH-MCU-R7A-CF9-CF2][physical-free-page-trim]
[ASH-MCU-R7A-CF9-CF2][generation-resource-summary]
```

A successful trim must demonstrate nonzero `physical_destroyed_bytes` when free retained pages exceed the target.

---

## 14. Evidence boundary at bake time

```text
SOURCE / STATIC       PASS
ARCHIVE / CRC         PASS
FIRST USER COMPILE    FAIL / MISSING anyhow::Context IMPORT
COMPILEFIX SOURCE     APPLIED
RUST RECOMPILE        REQUIRED / UNVERIFIED
RUST TEST             UNVERIFIED
PHYSICAL              UNVERIFIED
VRAM PERFORMANCE      UNMEASURED
CANDIDATE HOST DEMOTE NOT IMPLEMENTED / NOT CLAIMED
```

The first user-side Rust compile exposed a source-level import omission in `usage_segregated_buffer_arena.rs`: the CF9-CF2 implementation used `.context(...)` without importing the `anyhow::Context` trait. The code-only archives were re-sealed with:

```rust
use anyhow::{anyhow, ensure, Context, Result};
```

This compilefix closes the reported E0599 source defect only. A successful user-side recompile is still required before compile promotion. The bake environment does not contain `cargo`, `rustc`, or `rustfmt`, so runtime/physical promotion is not claimed.

---

## 15. Promotion tokens

Static / compile qualification:

```text
PASS_EVE_MCU_R7A_CF9_CF2_PHYSICAL_FREE_PAGE_TRIM
```

Physical VRAM trim:

```text
PASS_EVE_MCU_R7A_CF9_CF2_PHYSICAL_VRAM_RETURN
```

Hold:

```text
HOLD_EVE_MCU_R7A_CF9_CF2_PHYSICAL_TRIM_UNPROVEN
```

The following token is explicitly unavailable in this revision:

```text
PASS_EVE_MCU_R7A_WAVE_BOUNDED_CANDIDATE_RESIDENCY
```

---

## 16. Completion law

CF9-CF2 is complete only when:

1. exact-completion logical reclaim remains required;
2. a live page cannot enter physical trim;
3. free R7A pages above the bootstrap physical retention target leave the arena pool;
4. their A01 physical allocation entries are retired;
5. their WGPU buffers are explicitly destroyed outside the arena lock;
6. retained-byte and page accounting decrease exactly;
7. the Device / Queue / pipeline session authorities remain unchanged;
8. a physical campaign observes VRAM return for eligible free pages.

> CF9-CF2 closes physical reclamation for pages that are already logically free. It does not yet make Adam candidate residency wave-local. That requires moving the generation-wide candidate authority from live GPU segments to a host-backed successor in CF9-CF3.
