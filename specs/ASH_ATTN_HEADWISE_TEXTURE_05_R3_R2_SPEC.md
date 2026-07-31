# ASH-ATTN-HEADWISE-TEXTURE-05-R3-R2

## Persistent Residency Plateau Attribution /
## Fixed-Capacity Floor Accounting /
## Bootstrap Residency Baseline /
## Per-Generation Physical Page Ledger /
## Ten-Replay Zero-Growth Seal /
## Current·Previous Refcount Census /
## Retired Page Free-Set Convergence /
## Transient Owner Delta /
## Session-Retirement Owner-Zero Receipt /
## Driver-Reserved Memory Non-Authority Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-05-R3-R2`  
> Build revision: `HEADWISE-TEXTURE-05-R3-R2-persistent-residency-plateau-attribution-v1`  
> Parent: `ASH-ATTN-HEADWISE-TEXTURE-05-R3-R1`  
> Production authority: `HeadwiseFullActive / BufferAtlasV1` unchanged  
> Candidate authority: `KvTextureGqa4V1` shadow evidence only

---

# 1. Measured trigger

R3 completed the persistent residency contract:

```text
full population count       1
append count                5
texture generations         6
shadow commits             60
per-commit reconstruction   0
pipeline kinds              8
```

The physical gate nevertheless returned:

```text
latency_p95_within_budget       false
latency_p99_within_budget       false
residency_plateau_within_budget false
```

The legacy plateau estimator is not an authoritative allocation census. It derives logical payload from the current `seq_kv`, adds a previous-generation estimate using the same current geometry, and compares windows that contain different KV buckets. In the monotonic R3 order, expected working-set growth can therefore be classified as a leak.

R3-R2 preserves this value as:

```text
legacy_mixed_geometry_growth_ratio
legacy_ratio_authoritative = false
```

It must not directly decide `residency_plateau_within_budget`.

---

# 2. Goal

R3-R2 attributes persistent residency using explicit Rust-owned resource and physical-page evidence.

The authoritative predicate is the conjunction of:

```text
fixed_capacity_floor_pass
bootstrap_baseline_pass
per_generation_page_ledger_pass
ten_replay_zero_growth_pass
current_previous_refcount_census_pass
retired_page_free_set_convergence_pass
transient_owner_delta_pass
session_retirement_owner_zero_pass
corrected_total_peak_within_budget
```

No driver or OS memory counter may replace these receipts.

---

# 3. Ownership SSOT

```text
DeviceScoped
  device
  queue
  pipeline manager
  eight pipeline kinds

SessionPersistent
  residency registry
  twenty-two layer residency records
  twenty-two K textures
  twenty-two V textures
  forty-four texture views
  twenty-two validation buffers
  twenty-two physical page allocators
  twenty-two physical page tables
  persistent K source buffer
  persistent V source buffer

GenerationMetadata
  current generation view
  previous generation view

CommitTransient
  Q/reference snapshots
  candidate and compare scratch
  timestamp resources
  ticket registry
  transient bind groups

DiagnosticExternal
  optional driver/OS memory observations
```

`DiagnosticExternal` is never authoritative for Rust owner lifetime.

---

# 4. Fixed-capacity descriptor floor

Canonical persistent texture geometry:

```text
layers                           22
physical page capacity/layer     16
texture objects                  44
texture views                    44
validation buffers               22
persistent source buffers         2
```

Descriptor payload accounting:

```text
texture bytes/object          2,097,152
texture pair/layer            4,194,304
all layer texture bytes      92,274,688
persistent source bytes       3,670,016
validation token bytes               88
known session floor          95,944,792
```

This count represents Rust-requested descriptor payload. It excludes pipeline internal allocations, driver heap reservation, OS-reported dedicated memory and vendor allocator fragmentation.

Required invariants:

```text
bootstrap descriptor bytes == every post-append descriptor sample
bootstrap descriptor bytes == every post-replay descriptor sample
texture capacity rebuild count == 0
texture resize count == 0
```

---

# 5. Bootstrap baseline

Immediately after T0 bootstrap and before the first replay:

```text
committed tokens                    64
current page refs                   22
previous page refs                   0
total refcount                      22
unique active physical pages        22
free physical pages                330
allocator records                   22
active page-table entries           22
commit transient live owners         0
known session floor         95,944,792
```

The baseline receipt binds the session owner summary, generation owner summary and persistent identity digest.

---

# 6. Six-generation physical page ledger

Canonical aggregate values across twenty-two layers:

```text
Generation  Current  Previous  Refcount  Active  Free  AllocationSerial  Retired
T0               22         0        22      22   330                22        0
T1               44        22        66      66   286                66        0
T2               66        44       110      88   264               110       22
T3              132        66       198     132   220               176       44
T4              220       132       352     220   132               264       44
T5              308       220       528     308    44               352       44
```

For every generation:

```text
allocator record set == active page-table physical set
free set == exact complement of allocator record set
active/free intersection == empty
allocator/free intersection == empty
zero-ref live allocator records == 0
current and previous page digests match allocator records
current and previous content generations match page-table entries
texture object creation delta == 0
texture capacity rebuild delta == 0
```

The first mismatching generation, layer and physical page must be localized when available.

---

# 7. Ten-replay zero-growth seal

Every texture generation is replayed ten times. Within one generation, all ten post-GC snapshots must preserve:

```text
persistent identity digest
texture descriptor bytes
texture object count
texture view count
allocator record count
free-page count
allocation serial
generation switch count
page state transition count
```

Required deltas:

```text
descriptor byte delta       0
texture object delta        0
texture view delta          0
allocator record delta      0
free page delta             0
allocation serial delta     0
generation switch delta     0
page transition delta       0
```

After every replay manual-GC boundary:

```text
CommitTransient live owner count == 0
CommitTransient live descriptor bytes == 0
```

Six independent zero-growth receipts are required.

---

# 8. Current and previous refcount census

For each layer and generation:

```text
observed allocator refcount sum
  == current layer page refs + previous layer page refs
```

Only current and previous generation metadata may remain live. Older generation metadata must be retired before the next publication completes.

Failures include:

```text
refcount underflow
zero-ref live allocator record
missing allocator record
missing active page-table entry
digest mismatch
content-generation mismatch
referenced page in free set
older-than-previous generation owner
```

---

# 9. Retired-page free-set convergence

Page retirement is one transaction:

```text
old previous view release
  -> generation refcount decrement
  -> page-table SealedImmutable to RetirementPending
  -> page-table RetirementPending to Retired
  -> allocator record removal
  -> physical page insertion into free set
  -> allocator/page-table retirement-set parity
```

A physical page becomes reusable only after both the allocator and page table have retired it.

Required checks:

```text
allocator record set == page-table active set
free set == capacity complement
retired page not present in allocator records
active page not present in free set
allocation serial monotonic
retirement count monotonic
```

---

# 10. Transient owner delta

R3-R2 writes one receipt for every manual-GC boundary:

```text
healthy shadow boundaries    60
fault-drill boundary          1
post-disable boundaries       8
total                         69
```

Each receipt records:

```text
pre-commit live count and bytes
peak live count and bytes
pre-GC live count and bytes
post-drop live count and bytes
post-poll live count and bytes
created count
retired count
owner delta
byte delta
unretired resource IDs
poll status
```

PASS requires:

```text
created count == retired count
owner delta == 0
post-drop live count == 0
post-poll live count == 0
post-drop live bytes == 0
post-poll live bytes == 0
unretired resource IDs empty
```

---

# 11. Session-retirement owner-zero

After candidate admission closes and submitted work drains:

```text
persistent source buffers dropped
residency registry dropped
SessionPersistent owners retired
GenerationMetadata owners retired
device.poll(Wait)
```

Required post-retirement values:

```text
SessionPersistent live owner count    0
GenerationMetadata live owner count   0
CommitTransient live owner count      0
session descriptor bytes              0
unretired resource IDs                empty

device retained                       true
queue retained                        true
pipeline manager retained             true
pipeline kind count                    8
```

Driver heap reservation remaining after this point is diagnostic-only and cannot by itself fail the Rust owner-zero receipt.

---

# 12. Corrected plateau predicate

```text
corrected_total_peak_bytes
  = known_session_descriptor_floor_bytes
  + peak_commit_transient_descriptor_bytes
```

```text
corrected_total_peak_within_budget
  = corrected_total_peak_bytes <= max_total_shadow_bytes
```

```text
residency_plateau_within_budget
  = fixed_capacity_floor_pass
  && bootstrap_baseline_pass
  && generation_page_ledger_pass
  && ten_replay_zero_growth_pass
  && current_previous_refcount_census_pass
  && retired_page_free_set_convergence_pass
  && transient_owner_delta_pass
  && session_retirement_owner_zero_pass
  && corrected_total_peak_within_budget
```

The legacy mixed-geometry ratio remains in diagnostics with `legacy_ratio_authoritative=false`.

Failure classification priority:

```text
same_generation_persistent_growth
current_previous_refcount_leak
retired_page_free_set_divergence
commit_transient_owner_leak
session_retirement_owner_leak
multiple_failures
expected_generation_occupancy
fixed_persistent_floor_only
```

---

# 13. Eligibility adoption

`ResidencyPlateauWithinBudget` must consume the corrected boolean predicate:

```text
observed = soak_receipt.plateau_pass as u64
budget   = 1
comparator = true
```

R3-R2 must not change latency predicates, numeric parity, production continuity or output authority.

A corrected residency PASS may still leave Texture-05 HOLD because p95 or p99 latency remains over budget.

---

# 14. Runtime artifacts

```text
workspace/runtime/attention/headwise/texture/05/r3_r2/
  fixed_capacity_floor_receipt.json
  bootstrap_residency_baseline.json
  per_generation_physical_page_ledger.json
  generation_residency_snapshots.json
  ten_replay_zero_growth_receipts.json
  current_previous_refcount_census.json
  retired_page_free_set_convergence.json
  transient_owner_delta_receipts.json
  owned_resource_ledger.json
  session_retirement_owner_zero_receipt.json
  driver_reserved_memory_diagnostic.json
  residency_plateau_attribution_receipt.json
```

Top-level:

```text
workspace/runtime/attention/headwise/texture/
  ash_attn_headwise_texture_05_r3_r2_runtime_artifact.json
  ash_attn_headwise_texture_05_r3_r2_local_manifest.json
```

All artifacts are Rust-authored through temporary write, rename, readback and SHA-256 verification.

---

# 15. Verification gate

Binary:

```text
ash_attn_headwise_texture_05_r3_r2_gate
```

The gate verifies:

```text
39-key response-file cardinality
fixed descriptor geometry and byte totals
six canonical page/refcount arrays
8 pipeline kinds
6 generations
10 replays/generation
60 shadow commits
69 transient-GC boundaries
physical source census binding
corrected predicate adoption
legacy ratio authority prohibition
driver memory authority prohibition
runtime artifact and local manifest generation
```

---

# 16. Completion gate

```text
fixed capacity floor                         PASS
bootstrap baseline                           PASS
six generation page ledgers                  PASS
six ten-replay zero-growth receipts          PASS
six current/previous refcount censuses       PASS
six retired/free-set convergence receipts    PASS
sixty-nine transient owner receipts          PASS
session retirement owner zero                PASS
driver memory owner authority               false
legacy ratio authority                      false
production authority mutation count             0
candidate output commit count                   0
```

Patch-local PASS token:

```text
PASS_ASH_ATTN_HEADWISE_TEXTURE_05_R3_R2_PERSISTENT_RESIDENCY_PLATEAU_ATTRIBUTION_FIXED_CAPACITY_FLOOR_BOOTSTRAP_BASELINE_PER_GENERATION_PAGE_LEDGER_TEN_REPLAY_ZERO_GROWTH_CURRENT_PREVIOUS_REFCOUNT_RETIRED_FREE_SET_TRANSIENT_OWNER_SESSION_RETIREMENT_OWNER_ZERO_DRIVER_MEMORY_NON_AUTHORITY_SEALED
```

---

# 17. Direct execution

Verification gate:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_r3_r2_gate -- "@specs/cli/ash_attn_headwise_texture_05_r3_r2.args"
```

Physical Texture-05 gate:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_gate -- "@specs/cli/ash_attn_headwise_texture_05.args"
```

Expected new disclosure:

```text
known_floor_bytes
peak_transient_bytes
corrected_peak_bytes
legacy_growth_ratio
legacy_authoritative=false
plateau_pass
retirement_owner_zero
```

R3-R2 is an attribution and authority-correction patch. It does not claim to close the remaining latency p95 or p99 failure.
