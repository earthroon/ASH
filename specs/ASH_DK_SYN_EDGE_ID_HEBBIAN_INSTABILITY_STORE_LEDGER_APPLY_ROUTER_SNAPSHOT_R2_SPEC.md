# ASH-DK-SYN-EDGE-ID-HEBBIAN-INSTABILITY-STORE-LEDGER-APPLY-ROUTER-SNAPSHOT-R2

## 0. Revision

```text
Short name:
DK-SYN-R2

Patch ID:
ASH-DK-SYNAPSE
-EDGE-IDENTITY-HEBBIAN-INSTABILITY-COST-STORE
-COACTIVATION-LEDGER-BINDING
-PROPOSAL-APPLY-AUTHORITY
-ROUTER-COST-REINJECTION
-SNAPSHOT-COMMIT-ROLLBACK-CLOSURE
-R2
```

Static status at this bake:

```text
edge-id instability store                  = MATERIALIZED
complete registry-edge coverage            = MATERIALIZED
exact-edge coactivation projection         = MATERIALIZED
exact-edge instability proposal builder    = MATERIALIZED
candidate store transaction                = MATERIALIZED
commit / rollback authority                = MATERIALIZED
candidate-vs-committed publication state   = MATERIALIZED
R2 router store reinjection                = MATERIALIZED
legacy string cost ignored by R2 route     = MATERIALIZED
immutable snapshot persistence             = MATERIALIZED
Rust compile PASS                          = NOT CLAIMED BY BAKE ENVIRONMENT
semantic admission PASS                    = HOLD
production path-integral SSOT promotion    = NOT CLAIMED
```

Static token:

```text
PASS_ASH_DK_SYN_EDGE_ID_HEBBIAN_INSTABILITY_STORE_LEDGER_APPLY_ROUTER_SNAPSHOT_R2_STATIC
```

Semantic HOLD:

```text
HOLD_ASH_DK_SYN_EDGE_ID_HEBBIAN_INSTABILITY_STORE_LEDGER_APPLY_ROUTER_SNAPSHOT_R2_PENDING
```

Reserved semantic PASS:

```text
PASS_ASH_DK_SYN_EDGE_ID_HEBBIAN_INSTABILITY_STORE_LEDGER_APPLY_ROUTER_SNAPSHOT_R2
```

## 1. Direct parent

```text
ASH_PASS3_DK_SYN_R1_EDGE_ID_FAIL_CLOSED_SIGNED_BEAM_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 6e77d5c78c5948aa27058cde5d0c812bab76233297e84f55ffa16c6622b40959
entries 8,449
```

R1 already seals ordered edge-authoritative PathIdentity, fail-closed ranker/Delta-K evidence admission, signed action semantics, and deterministic finite-beam approximation semantics.

R2 closes the previously explicit `no_instability_cost_store` gap without changing Delta-K, Muon, WGPU, or optimizer mathematics.

## 2. Central authority

The learned instability-cost SSOT is exact:

```text
edge_id -> committed instability cost
```

The store SHALL NOT use sorted adapter pair, endpoint pair, path ID alone, mean path action, or report-path strings as its primary key.

## 3. Store / base-weight separation

Existing edge base action remains:

```text
C_base = -ln(runtime_weight)
```

R2 adds a separate non-negative term:

```text
C_instability >= 0
```

Canonical R2 step action is the existing action decomposition plus exactly one committed edge instability term.

Applying instability proposals does not mutate `runtime_weight`.

## 4. Complete store coverage

`AshEdgeInstabilityCostStoreSnapshotR2` contains one entry for every active registry edge.

New/unlearned edges are represented explicitly with:

```text
committed_cost = 0
```

Missing store entry is corruption and fails closed. No `unwrap_or(0)` authority is permitted for store-enabled routing.

## 5. Snapshot identity and publication state

Store snapshots contain:

```text
schema
store revision
registry semantic revision
policy id
Candidate / Committed publication state
sorted edge entries
source snapshot lineage
applied proposal IDs
SHA-256 snapshot digest
```

The digest is derived from deterministic binary material including f32 bit representations.

`Candidate` and `Committed` are separate authorities.

## 6. Candidate invisibility

A transaction candidate uses:

```text
publication_state = Candidate
```

R2 Active router rejects Candidate snapshots.

Persistence also rejects Candidate snapshots.

`commit_edge_instability_apply_transaction_r2()` changes the candidate to Committed and recalculates the digest before returning the next routing snapshot.

## 7. Registry revision binding

Every store snapshot binds one active registry revision.

Router admission requires exact registry/store revision equality and exact edge-ID set equality.

Revision mismatch fails closed.

## 8. Deterministic rebase

R2 rebase semantics are:

```text
same edge_id in new registry -> preserve cost
new edge_id                  -> initialize cost 0
removed edge_id              -> remove entry
```

No endpoint-based renamed-edge inference is allowed.

## 9. Exact-edge evidence ledger

Added:

```text
crates/ash_core/src/edge_instability_evidence_ledger_r2.rs
```

`AshEdgeInstabilityEvidenceLedgerR2` projects R1 ordered `selected_edge_ids` from coactivation events into exact edge entries.

Each exposed edge tracks:

```text
exposure
pass
fail
warning
rejected
mean output score
mean path action
fail ratio
confidence
evidence event IDs
```

The confidence formula remains the existing `n / (n + 3)` behavior.

## 10. Legacy edge-less evidence

Historical events without ordered edge IDs may remain in the legacy adapter-pair ledger.

They increment the R2 legacy edge-less evidence count but do not mutate exact-edge R2 evidence.

A non-empty edge ID not present in the active registry is rejected rather than guessed from adapter endpoints.

## 11. Pair ledger remains evidence only

Existing adapter-pair coactivation stats remain available for weight/inhibitory proposals and diagnostics.

They are not the R2 instability-cost identity authority.

## 12. Pair-based instability proposal retirement

Legacy `path_cost_proposal()` and pair-derived instability-cost proposals are retired from `build_hebbian_update_proposals()`.

That legacy builder continues to create weight and inhibitory proposals.

Canonical R2 instability proposals are created only by:

```text
build_edge_instability_update_proposals_r2(...)
```

using exact-edge evidence plus the committed store.

## 13. Old-cost authority

R2 instability proposal:

```text
old_cost = committed_store[edge_id].committed_cost
```

`mean_path_action` is evidence only and is no longer used as the current instability-cost surrogate.

## 14. Proposal direction

R2 retains existing learning-rate constants and evidence thresholds where applicable.

For exact-edge instability proposal generation, failure evidence has first precedence, warning evidence second, and stable pass evidence may decrease a nonzero committed penalty.

The generated proposal always carries an exact `edge_id` and requires explicit apply.

## 15. Proposal evidence snapshot

The proposal-set `ledger_version` is the exact edge-ledger snapshot digest.

The R2 apply transaction receives and validates the actual `AshEdgeInstabilityEvidenceLedgerR2` snapshot.

It requires proposal event IDs, pass/fail/warning/rejected counts, confidence, registry revision, and ledger snapshot identity to match the supplied exact-edge ledger.

## 16. Dedicated store apply authority

Added:

```text
crates/ash_core/src/edge_instability_apply_transaction_r2.rs
```

Instability proposals are not remapped into registry weight mutations.

The legacy ASH-19 registry apply gate now quarantines such proposals with:

```text
instability_cost_store_r2_requires_dedicated_apply
```

The former `no_instability_cost_store` branch text is retired.

## 17. Transaction law

`build_edge_instability_apply_transaction_r2(...)` requires:

```text
Committed parent store
PASS proposal set
matching registry revision
matching exact-edge ledger snapshot
exact edge_id
old-cost match
non-negative bounded proposed cost
minimum evidence support
one proposal per edge per transaction
```

It creates a Candidate snapshot only.

## 18. Stale proposal rejection

If another committed store revision changes the target cost before apply, the old proposal fails old-cost compare-and-swap validation.

Duplicate proposal targets in one transaction are rejected to avoid order-dependent reducers.

## 19. Commit / rollback

Validated candidate:

```text
commit   -> Committed snapshot, new digest
rollback -> transaction RolledBack, prior committed store unchanged
```

No partial committed mutation is performed.

## 20. Router reinjection

`path_integral_synapse_router.rs` now has a source-aware core with three instability sources:

```text
LegacyReportStrings
Disabled
Store(committed snapshot)
```

Existing `build_path_integral_synapse_route_plan()` retains legacy compatibility.

New canonical R2 API:

```text
build_path_integral_synapse_route_plan_r2(...)
```

supports Disabled / ObserveOnly / Active store-aware routing.

Active validates and captures one Committed store snapshot for the complete beam invocation.

## 21. ObserveOnly

`build_path_integral_synapse_route_observe_only_r2(...)` returns both:

```text
baseline plan with instability disabled
store-aware shadow plan
```

without making the shadow plan the baseline physical route.

This is the admission seam for DK-SYN-R2A.

## 22. Legacy string retirement on R2 route

The old `coactivation_fail_ratio=...` parser remains only in `LegacyReportStrings` compatibility routing.

R2 Active `Store` routing does not parse or add that value.

Therefore one edge receives exactly one learned instability term from the committed store.

## 23. Persistence

Added:

```text
crates/ash_core/src/edge_instability_store_persistence_r2.rs
```

Committed snapshots may be written as immutable JSON artifacts through a same-directory staging file, `sync_all`, and atomic rename to a previously absent final snapshot path.

The loader validates schema, registry revision, policy, complete edge coverage, publication state, and digest before returning the snapshot.

R2 does not introduce a mutable in-place JSON store.

## 24. Static regression fixture

Added:

```text
crates/ash_core/tests/dk_syn_r2_contract.rs
```

Static fixtures cover:

```text
complete edge coverage
missing-entry fail-closed
exact-edge ledger projection
store-authoritative old_cost
Candidate invisible to Active router
commit visibility
rollback invariance
router exact reinjection
ObserveOnly baseline/shadow split
registry rebase
parallel-edge independent costs
stale proposal rejection
duplicate target rejection
legacy report-string ignored by R2 Active route
persistence roundtrip
legacy pair builder no longer emits instability-store proposals
static receipt remains semantic HOLD
```

The existing ASH-19 test is updated to verify dedicated R2-store quarantine instead of the retired `no_instability_cost_store` behavior.

## 25. Static source delta

Relative to the direct R1 parent:

```text
ADD 5
MOD 5
DEL 0
```

Added:

```text
crates/ash_core/src/edge_instability_apply_transaction_r2.rs
crates/ash_core/src/edge_instability_cost_store_r2.rs
crates/ash_core/src/edge_instability_evidence_ledger_r2.rs
crates/ash_core/src/edge_instability_store_persistence_r2.rs
crates/ash_core/tests/dk_syn_r2_contract.rs
```

Modified:

```text
crates/ash_core/src/hebbian_update.rs
crates/ash_core/src/lib.rs
crates/ash_core/src/path_integral_synapse_router.rs
crates/ash_core/src/synapse_proposal_apply_gate.rs
crates/ash_core/tests/ash_19_synapse_proposal_apply_gate.rs
```

## 26. Code artifacts

Full code-only artifact:

```text
ASH_PASS3_DK_SYN_R2_EDGE_INSTABILITY_STORE_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 82f324e19c3acff1e3ad5e73ae7e46c5aae171d3f55a9f1cec2ad1c719692e95
entries 8,454
```

Overlay artifact:

```text
ASH_PASS3_DK_SYN_R2_EDGE_INSTABILITY_STORE_STATIC_SOURCE_BAKE_OVERLAY.zip
SHA-256 3585ee3ea00a8cf0d7829fe008ba602d266980b9bb6e401ac695b69bcbc2b305
entries 10
```

Tree digest:

```text
SHA-256 7e45e55e0671be24fe645bce682ef65de18d4ac3b589067196aab2090a6b429d
```

Parent + overlay reproduces the full baked tree byte-for-byte.

## 27. Compile truth

The artifact-construction environment does not provide Cargo/Rustc.

Therefore post-bake compile PASS and semantic PASS are not claimed.

Immediate local gates:

```powershell
cargo check --locked -p ash_core --all-targets
cargo check --locked -p orchestrator_local --all-targets
```

Then run the targeted DK-SYN-R1/R2 and ASH-18/19/32 tests.

## 28. Semantic PASS requirements

Before the reserved R2 PASS token may be emitted, qualification must verify at minimum:

```text
R1 identity/evidence/action/beam fixtures remain PASS
store edge set == registry edge set
parallel/directed edge costs remain independent
missing store entry fails closed
exact-edge ledger lineage is deterministic
R2 proposal old_cost equals committed store
candidate snapshot rejected by Active router
commit becomes visible only to subsequent route invocation
rollback leaves committed route behavior unchanged
runtime_weight unchanged by instability transaction
R2 Active ignores legacy report-string penalty
snapshot persistence/reload validates identical digest
```

## 29. Explicit non-claims

This static R2 bake does not claim:

```text
path-integral router is the sole production routing SSOT
Hebbian thresholds are globally optimal
automatic online self-modification is enabled
finite beam is globally optimal
instability feedback is empirically stable
oscillation/lock-in are solved
```

## 30. Direct successor

```text
DK-SYN-R2A

Hebbian Closed-Loop Stability Admission
+ Store OFF / ObserveOnly / Active Same-Source A/B
+ Oscillation / Lock-In Receipts
+ Proposal Effect Attribution
+ Promotion Seal
```

## 31. Final law

> Coactivation is evidence. The committed edge store is learned-cost authority.

> Exact `edge_id` is the learned-cost key.

> Every qualified store explicitly covers every registry edge, including zero-cost unlearned edges.

> Missing entry is corruption, not a neutral fallback.

> Instability cost is a separate non-negative penalty and never silently rewrites signed edge base weight.

> Pair-level path-cost proposals no longer create instability-store mutations.

> R2 proposals derive from ordered edge lineage and read `old_cost` from the committed store.

> Apply creates a Candidate snapshot. Candidate snapshots cannot route or persist.

> Commit creates a new Committed digest. Rollback preserves the prior committed authority.

> R2 Active router reads committed instability cost directly by edge ID exactly once and does not parse legacy report strings as numeric authority.

> DK-SYN-R2 is complete only after compile and semantic fixtures verify this exact-edge closed loop without reintroducing adapter-pair targeting, silent zero fallback, candidate leakage, or edge-weight remapping.
