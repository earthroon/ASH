# ASH-HOTPATH-OWNERSHIP-BORROW-CLEANUP-16

## Copy-Geometry Route Projection / Short-Lived Registry Borrow / Adam M·V Single-Materialization / Local Capability Move / Intentional Snapshot Clone Preservation / No New Cache Owner

## 0. Status

```text
Patch ID: ASH-HOTPATH-OWNERSHIP-BORROW-CLEANUP-16
Direct parent: ASH-PRODUCTION-IMPORT-SURFACE-CONTRACTION-15
Runtime parent: ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
Transaction parent: ASH-GENERATION-TRANSACTION-COORDINATOR-CLOSURE-12
Recovery parent: ASH-GENERATION-FAILURE-RECOVERY-AND-LAST-GOOD-SEAL-13
Lineage family: optimizer-hotpath-ownership
Authority class: OptimizerDataPlane
Production authority: HotpathOwnershipProjection
Status: Active
Target data plane: bp-dk-data-plane/active-fusion/v1
```

16 reduces unnecessary host ownership in the current R6/Muon hot path without moving semantic state authority. It does not change optimizer formulas, BP-Delta-K formulas, transaction ordering, recovery semantics, checkpoint schemas, GPU/WGSL code, or the 15 build-surface contraction.

## 1. Central SSOT

```text
A CLONE IS NOT WRONG BECAUSE IT IS A CLONE.

REMOVE ONLY OWNERSHIP
THAT HAS NO SEMANTIC AUTHORITY.
```

Patch-16 clone classification is explicit:

```text
ELIMINATE
- parameter full-route clone
- scheduler full-route clone
- scheduler source-M intermediate Vec
- scheduler source-V intermediate Vec
- backend capability String clones

PRESERVE AUTHORITY SNAPSHOT
- source momentum precommit snapshot
- source weight delta witness

PRESERVE REPLAY ISOLATION
- fusion planner replay clone

PRESERVE DUAL OWNERSHIP
- Bridge temporal ready clone
- Bridge evidence clone
- fusion plan persistent clone
```

## 2. Route ownership before 16

The production Muon callsite previously began with:

```text
route_for_parameter(...)?
→ clone entire FirstCandidateParameterRoute
→ keep clone alive through the parameter execution
```

The scheduler separately repeated the same full route clone.

`FirstCandidateParameterRoute` contains heap-backed state including `String`, `Vec<u64>`, and an optional Muon grid with additional Strings. The hot path did not need that entire owned object after admission.

## 3. Copy-only parameter geometry

16 adds:

```text
ProductionMuonParameterGeometry
```

as a `pub(crate)`, `Copy` projection containing only:

```text
canonical_parameter_index: u32
rows: u64
cols: u64
full_tile_rows: u64
full_tile_cols: u64
tile_count: u64
muon_element_count: u64
momentum_base_element_offset: u64
```

The projection contains no `String`, `Vec`, `Box`, `Arc`, or `Rc` field and is not stored in `ProductionMuonRuntime`.

```text
Geometry != new owner
Geometry = short-lived borrow escape of primitive execution geometry
```

## 4. Canonical registry remains route SSOT

New helper:

```text
ProductionMuonRuntime::muon_parameter_geometry(...)
```

performs the existing parameter-index / parameter-id admission against the canonical registry.

Non-Muon routes preserve the previous behavior:

```text
muon_grid = None
→ Ok(None)
```

The rank-2 Muon gate is applied only after a Muon grid is present, preserving the previous non-Muon route semantics.

## 5. Full route clones removed

Exact targeted transition:

```text
Production Muon execute full-route clone: 1 -> 0
Scheduler Muon full-route clone:          1 -> 0
```

The scheduler now consumes the same `ProductionMuonParameterGeometry` projection instead of owning a full route clone.

## 6. PRE snapshot still consumes canonical route

16 does not reconstruct a shadow `FirstCandidateParameterRoute` from geometry.

Immediately around:

```text
seal_parameter_pre_snapshot(...)
```

the runtime reborrows the exact canonical route:

```text
registry route
→ short immutable borrow
→ PRE snapshot seal
→ borrow ends
```

Therefore geometry projection cannot silently become a second route authority.

## 7. Backend capability local ownership move

The physical fused-pair backend capability object was previously projected into `AshFusionExecutionCapability` through five owned String clones:

```text
backend_revision.clone()
device_limit_digest.clone()
kernel_revision.clone()
norm_reduction_path.clone()
capability_digest.clone()
```

The source capability local is not consumed afterward, so 16 moves those owned fields directly.

Exact targeted transition:

```text
backend capability String clones: 5 -> 0
```

No capability semantics or fields are recalculated.

## 8. Scheduler Adam M/V ownership before 16

For each Muon serialization chunk the parent path performed:

```text
resident M slice -> source_m Vec
resident V slice -> source_v Vec

source_m Vec -> candidate_m clone
source_v Vec -> candidate_v clone
```

This created two separate owned materializations for M and two for V before the candidate was committed.

## 9. Direct source hashing + one candidate materialization

16 changes the chunk flow to:

```text
resident M/V immutable slices
→ source SHA256 update directly from slices
→ one candidate_m / candidate_v Vec materialization
→ resident borrow scope ends
→ Adam residual execution
→ resident.update_slices(...)
```

Exact targeted transition:

```text
source_m intermediate Vec:        1 -> 0 per chunk
source_v intermediate Vec:        1 -> 0 per chunk
candidate_m from source clone:     1 -> 0 per chunk
candidate_v from source clone:     1 -> 0 per chunk
```

The remaining candidate materializations are intentional:

```text
m_slice.to_vec()
v_slice.to_vec()
```

once each per chunk.

## 10. Adam residual source semantics

After single materialization, Adam residual dispatch reads:

```text
candidate_m[local..local_end]
candidate_v[local..local_end]
```

before that exact range is overwritten by the returned candidate M/V.

The existing route traversal remains monotonic and the update order remains:

```text
read still-unmodified candidate source range
→ r6_adamw_candidate / zero-gradient candidate
→ copy returned M/V into candidate range
→ resident.update_slices(...)
```

16 does not add a second resident lookup, a new runtime overlap table, or an O(N) ownership guard.

## 11. Source M/V digest semantics preserved

Before 16, source M/V digest bytes came from the intermediate source Vecs.

After 16, the same resident F32 sequence is hashed directly:

```text
value.to_le_bytes()
```

before any resident mutation for the chunk.

No digest formula changes.

## 12. Intentionally preserved source momentum snapshot

The existing:

```text
source_momentum = authoritative momentum slice.to_vec()
```

remains exactly one owned parameter-local snapshot.

It is retained because it is used as precommit evidence across physical execution, replay, counterfactual comparison, source digest checks, and precommit mutation verification before authoritative momentum is updated.

```text
source momentum snapshot count: 1 -> 1
```

Removing this ownership would collapse source and candidate authority and is explicitly forbidden by the 16 validator.

## 13. Intentionally preserved replay isolation

The planner replay path retains:

```text
self.planning.bp_dk_fusion_planner.clone()
```

The clone is an isolated replay runtime, not redundant hot-path ownership.

```text
planner replay clone count: 1 -> 1
```

16 does not mutate the canonical planner twice and does not introduce snapshot-mutate-restore behavior.

## 14. Intentionally preserved Bridge dual ownership

The following remain:

```text
bridge_temporal_batch.ready.clone()
bridge_evidence.evidence.clone()
```

because the same generation evidence is consumed by the parameter-local Fusion graph path and retained by the canonical Bridge runtime owner.

```text
Bridge dual clones: 2 -> 2
```

Their ownership timing is not reordered for the sake of clone reduction.

## 15. Intentionally preserved Fusion-plan ownership

The canonical plan store retains:

```text
bp_dk_fusion_execution_plans.push(fusion_plan.clone())
```

while the local plan remains required by physical execution/replay/evidence paths.

```text
Fusion plan clone: 1 -> 1
```

16 does not postpone persistent plan ownership to function end because doing so would change failure-state semantics.

## 16. Source weight witness remains

The scheduler still retains:

```text
weight
candidate_weight = weight.clone()
```

because the source weight is later compared against candidate weight to calculate update nonzero count, sum-of-squares, and maximum absolute update.

Weight-copy removal would require a separate metric/streaming redesign and is outside 16.

## 17. Ownership workaround firewall

16 introduces no new:

```text
Arc owner
Rc owner
RefCell
Mutex
RwLock
unsafe borrow workaround
persistent geometry cache
```

The two target files retain only the parent-known scheduler `Arc<Vec<u8>>` residency representation and the existing Windows `unsafe` `MoveFileExW` call. The Muon callsite remains free of Arc/interior-mutability/unsafe ownership workarounds.

## 18. Runtime ownership topology preserved

07's nine top-level `ProductionMuonRuntime` owners remain unchanged:

```text
static_context
execution
observation
bridge
planning
control
evidence
telemetry
lifecycle
```

`ProductionMuonParameterGeometry` is not a runtime field and owns no durable state.

## 19. Transaction / recovery / fault boundaries preserved

16 retains:

```text
12 typed generation commit/abort coordinator
13 process recovery fence + exact recovery-source selection
14 cfg(test)-only physical fault seams
15 GPU70K build-surface contraction
09 R2E operational recovery route
```

The recovery fence remains checked before Muon geometry/execution admission.

No transaction stage ordering or recovery action is changed.

## 20. Lineage adoption

`ash_lineage_reconciliation_00_registry.py` adds:

```text
ASH-HOTPATH-OWNERSHIP-BORROW-CLEANUP-16

family = optimizer-hotpath-ownership
authority class = OptimizerDataPlane
production authority = HotpathOwnershipProjection
status = Active
direct parent = ASH-PRODUCTION-IMPORT-SURFACE-CONTRACTION-15
runtime parent = ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
```

Evidence parents include 10, 11, 12, 13, 14, and 15.

New head:

```text
optimizer-hotpath-ownership
→ ASH-HOTPATH-OWNERSHIP-BORROW-CLEANUP-16
```

The current optimizer execution authority remains the Production Muon callsite. 16 is not inserted into `CURRENT_EXECUTION_AUTHORITIES`.

## 21. CF1 classification

16 static validation is added to:

```text
ProductionValidators
```

because reintroducing full route clones, duplicate source-M/V materialization, or ownership workaround state is a current production hot-path regression.

The total CF1-enumerated Python validator set becomes:

```text
72
```

## 22. Forward-compatible validator repair

Four existing validators had source-spelling anchors that encoded the old ownership implementation rather than its semantic authority:

```text
BP-DK 01 local observation
BP-DK 03A Bridge pair evidence
reconciliation 02 PRE snapshot
Production Muon callsite R1
```

They were narrowed to recognize:

```text
Copy geometry admission
canonical-route PRE-seal reborrow
parameter_id input ownership
single candidate M/V materialization
```

without relaxing the original route, PRE snapshot, BP-DK, or hybrid Muon/Adam semantic gates.

## 23. Parent diff boundary

Compared with the exact 15 full-applied parent, 16 changes 12 files.

Runtime Rust:

```text
MOD crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
MOD crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

Tooling/governance:

```text
ADD tools/ash_hotpath_ownership_borrow_cleanup_16_registry.py
ADD tools/validate_ash_hotpath_ownership_borrow_cleanup_16.py
ADD tools/run_ash_hotpath_ownership_borrow_cleanup_16.ps1
MOD tools/ash_lineage_reconciliation_00_registry.py
MOD tools/validate_ash_lineage_reconciliation_00.py
MOD tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
MOD tools/validate_ash_bp_dk_bridge_pair_evidence_source_closure_03a_static.py
MOD tools/validate_ash_bp_dk_local_tensorcube_bp_dk_observation_01_static.py
MOD tools/validate_ash_bp_dk_parameter_pre_snapshot_authority_02.py
MOD tools/validate_tensorcube_local_muon_production_callsite_adoption_r1_static.py
```

```text
Rust runtime files changed = 2
WGSL files changed = 0
GPU70K historical source changed/deleted = 0 / 0
checkpoint schema files changed = 0
```

## 24. Targeted ownership delta

Static source comparison against parent 15 establishes:

```text
callsite full-route clone               1 -> 0
scheduler full-route clone              1 -> 0
scheduler source_m Vec materialization  1 -> 0
scheduler source_v Vec materialization  1 -> 0
candidate_m source clone                1 -> 0
candidate_v source clone                1 -> 0
backend capability owned-field clones   5 -> 0

source_momentum snapshot                1 -> 1
planner replay clone                    1 -> 1
Bridge dual clones                      2 -> 2
Fusion plan persistent clone            1 -> 1
```

These counts are source-structure evidence, not a measured wall-clock performance claim.

## 25. Baked static evidence

Validated source tree and re-extracted Full ZIP both pass the reconciliation chain:

```text
00  267 / 267 PASS
01  306 / 306 PASS
02  216 / 216 PASS
03  167 / 167 PASS
04  198 / 198 PASS
05   92 /  92 PASS
06  143 / 143 PASS
07  347 / 347 PASS
08   83 /  83 PASS
09   68 /  68 PASS
10   66 /  66 PASS
11   91 /  91 PASS
12  156 / 156 PASS
13  140 / 140 PASS
14  165 / 165 PASS
15   45 /  45 PASS
16   80 /  80 PASS
```

Additional evidence:

```text
BP-Delta-K *_static.py validators = 25 / 25 PASS
CF1-enumerated Python validators = 72 / 72 PASS
changed/new Python AST parse = 8 / 8 PASS
changed Rust delimiter/string/comment lexical sanity = 2 / 2 PASS
```

The packaged Full ZIP was re-extracted and directly re-ran 00→16, BP-Delta-K 25, and all CF1 72 validators successfully.

## 26. Packaging

```text
Overlay Code ZIP = 12 files
Full Applied Code ZIP = 7257 files
```

Full ZIP re-extraction versus the validated filtered work tree:

```text
missing = 0
extra = 0
hash mismatch = 0
forbidden generated content = 0
```

Code ZIPs exclude Markdown, `*.sha256`, `*.pyc`, `__pycache__`, generated target/artifact/report/receipt/manifest directories.

## 27. Runtime-source identity change

The 10/11/14 qualification chain binds receipts to the runtime-source digest over `base_train/src/**/*.rs`, `Cargo.toml`, and `Cargo.lock` when present.

Exact transition:

```text
Parent 15 runtime-source digest:
2960bb94abb4b9bece195e5c9b70ed195d84585d1228ad4aad2ed0151d691ca8

Current 16 runtime-source digest:
ea8df367b1434a20a03b41f21a060da87b55ad04a66d85f78821ba3ab48f8baf

runtime-source file count: 969 -> 969
```

Therefore all older 10/11/14 physical receipts are stale for the exact 16 source body and must be regenerated before a current-source physical closure claim.

## 28. Physical evidence boundary

The bake environment does not expose:

```text
cargo
rustc
rustfmt
pwsh
```

Therefore the following were not executed here:

```text
cargo metadata
cargo check --lib
cargo check --bin base_train
cargo check --all-targets
cargo test --lib --no-run
16 Rust ownership/unit execution
10 current-source physical behavior parity
11 current-source fresh-resume parity
14 current-source physical fault matrix
```

Current physical disposition:

```text
EvidenceInsufficient
```

Static PASS and lexical sanity are not Rust compile PASS.

## 29. Performance claim boundary

16 establishes a smaller ownership/materialization surface. It does not claim a measured speedup.

Allowed claim:

```text
full route ownership copies and the source-M/V intermediate materialization layer were removed from the qualified source structure
```

Not established here:

```text
X% faster
Y ms lower latency
Z GB/s higher throughput
```

A physical benchmark receipt is required for those claims.

## 30. Non-goals

16 does not implement:

```text
all-clone removal
source weight witness removal
source momentum snapshot removal
planner replay redesign
Bridge storage reorder
Fusion plan persistence reorder
route cache
descriptor cache
allocator/arena redesign
Arc/Rc ownership conversion
interior-mutability workaround
unsafe lifetime workaround
GPU buffer lifetime redesign
new synchronization primitives
```

## 31. Next revision

After the exact 16 body physically passes Cargo, 10, 11, and 14 qualification, profiling should determine the next optimization.

A conditional candidate is:

```text
ASH-HOTPATH-PARAMETER-ROUTE-CURSOR-AND-DESCRIPTOR-REUSE-17
```

but only if profiling establishes `packed_index_for_logical`, `route_span`, or descriptor construction as meaningful CPU overhead. Patch 17 should not be adopted merely because those operations exist.

## 32. Final seal

```text
THE REGISTRY REMAINS THE ROUTE SSOT

THE HOT PATH DOES NOT OWN THE WHOLE ROUTE
JUST TO ESCAPE A BORROW

ONLY COPY GEOMETRY ESCAPES
THE SHORT REGISTRY BORROW

THE CANONICAL ROUTE IS REBORROWED
WHEN PRE-SNAPSHOT AUTHORITY NEEDS IT

RESIDENT ADAM M/V ARE HASHED DIRECTLY

M/V ARE MATERIALIZED ONCE
AS CANDIDATE CHUNKS

THE STILL-UNMODIFIED CANDIDATE RANGE
IS THE ADAM SOURCE
UNTIL THAT EXACT RANGE IS OVERWRITTEN

SOURCE MOMENTUM REMAINS AN OWNED PRECOMMIT SNAPSHOT
PLANNER REPLAY REMAINS ISOLATED
BRIDGE DUAL OWNERSHIP REMAINS
FUSION PLAN PERSISTENCE REMAINS
SOURCE WEIGHT DELTA WITNESS REMAINS

NO CACHE IS INVENTED TO WIN A CLONE COUNT
NO OWNER IS MOVED TO SATISFY THE BORROW CHECKER
NO INTERIOR MUTABILITY IS ADDED
NO UNSAFE BORROW WORKAROUND IS ADDED

BORROW SCOPE GETS SHORTER
OWNERSHIP GETS SMALLER
SEMANTIC AUTHORITY DOES NOT MOVE

15 REMOVED HISTORICAL BUILD NOISE
16 REMOVES CURRENT HOTPATH OWNERSHIP NOISE
```
