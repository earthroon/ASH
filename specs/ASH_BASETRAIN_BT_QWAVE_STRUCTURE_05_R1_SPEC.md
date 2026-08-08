# ASH-BASETRAIN-BT-QWAVE-STRUCTURE-05-R1

## Atlas Parallel Wave Streaming Map Repair / Monolithic JSON Macro Retirement / QW01~QW05 Parallel Page Map / QW06 Terminal Graph Wave / Deterministic Ordered Merge / Parallel Receipt Lane Atlas / R05 Semantic Authority Preservation Seal

> Parent semantic SSOT: `ASH-BASETRAIN-BT-QWAVE-STRUCTURE-05`
>
> Physical parent: `BT-CHEONJIIN-STRUCTURE-04` physical PASS
>
> Repair trigger: Rust `serde_json::json!` macro recursion limit reached while expanding the monolithic R05 final receipt
>
> Repair rule: do not raise crate recursion limit; remove the structurally monolithic macro expansion
>
> Compute atlas revision: `BT-QWAVE-STRUCTURE-05-R1-atlas-parallel-wave-streaming-map-v1`
>
> Default physical fixture page size: `2`
>
> Q-wave formulas / CJI authority / edge membership / chain semantics: unchanged from R05
>
> Proof ledger: `HOLD`

---

# 1. Problem

The R05 implementation built the complete terminal receipt in one large `serde_json::json!({...})` invocation.
Rust macro expansion reached the crate recursion limit before runtime:

```text
error: recursion limit reached while expanding `$crate::json_internal!`
```

This is a compile-time artifact-construction failure, not a Q-wave numerical failure.

R1 must not hide the structural problem with:

```rust
#![recursion_limit = "256"]
```

or a larger value.

The receipt and stage scheduling are instead restructured as atlas waves.

---

# 2. R1 architecture

```text
R04 canonical CJI atlas
        ↓
Wave 0 / QW01 syllable-cell pages
        ├ page 0 → worker lane
        ├ page 1 → worker lane
        └ ...
        ↓ deterministic item-index merge
Wave 1 / QW02 pulse pages
        ↓ deterministic item-index merge
Wave 2 / QW03 R04-edge pages
        ↓ deterministic item-index merge
Wave 3 / QW04 connected-chain pages
        ↓ deterministic item-index merge
Wave 4 / QW05 overlay pages
        ↓ deterministic item-index merge
Wave 5 / QW06 terminal graph singleton wave
        ↓
BaseTrainQWaveStructureAuthority
        ↓
Parallel receipt-lane atlas
        ↓ wave-ordinal / lane-ordinal / lexicographic-key streaming merge
final_receipt.json
```

Dependencies remain ordered by wave. Only items that are independent inside one stage execute in parallel.

---

# 3. Compute atlas page map

Required generic contract:

```text
input slice
page_size > 0
page_count = ceil(item_count / page_size)
worker_count = min(available_parallelism, page_count)
workers consume disjoint page ordinals
worker output = Vec<(global_item_index, item)>
all worker shards merge by global_item_index ascending
```

Required:

```text
output item count == input item count
merged index i == expected i for every output item
```

Failure is fail-closed.

No worker completion order may affect authority ordering or digest ordering.

---

# 4. QW01 atlas wave

QW01 source items:

```text
R04 CJI rows
```

Each item independently reads immutable:

```text
R04 row
R03 matching structure row
R04 atom expansion ledger
R05 QW01 policy
```

and produces exactly one `BaseTrainQWaveSyllableCellV1` with:

```text
cell_index = global atlas item index
```

Current fixture:

```text
item_count = 8
page_size = 2
page_count = 4
```

---

# 5. QW02 atlas wave

QW02 source items:

```text
QW01 cells
```

Each pulse vector is independently computed from one cell and immutable R04 parent structure.

Local clamp/neutral counters are produced per item and reduced after deterministic merge.

No shared mutable counter is written by worker threads.

---

# 6. QW03 atlas wave

QW03 source items are exactly:

```text
R04 transition ledger entries
```

R04 remains the single edge-membership authority.

Current fixture:

```text
item_count = 4
page_size = 2
page_count = 2
```

Zero-edge input is valid:

```text
item_count = 0
page_count = 0
worker_count = 0
empty_wave_admitted = true
```

No dummy edge is inserted.

---

# 7. QW04 atlas wave

Connected-component membership is first derived deterministically from the full ordered QW03 edge map.

This produces immutable chain descriptors:

```text
(start_index, end_index, edge_indices)
```

Chain aggregation is then page-parallel because each descriptor owns a disjoint ordered cell/vector slice.

The chain index is the deterministic descriptor index, never worker completion order.

---

# 8. QW05 atlas wave

One QW04 chain is one QW05 map item.

In current `optional_explicit_absent_without_evidence` mode each chain independently emits one explicit absent overlay.

When morphology evidence is later present, item `i` may read only:

```text
chain[i]
evidence[i]
```

and must preserve the existing exact chain/span gates.

---

# 9. QW06 terminal wave

QW06 depends on the complete ordered QW04 chain set and exact boundary provenance.

It therefore remains a terminal singleton atlas item:

```text
wave item_count = 1
page_count = 1
```

The same wave scheduler is used so the R05 execution graph remains one uniform wave-map contract.

---

# 10. Compute atlas receipt

Publish:

```text
qwave_compute_atlas_receipt.json
```

Required top-level fields:

```text
schema
builder revision
page size
wave count = 6
wave receipts
atlas digest
```

Each wave receipt includes:

```text
wave ordinal
wave name
item count
page size
page count
worker count
parallel page build = true
deterministic merge order
empty wave admitted
digest
```

Worker count and page count are runtime execution evidence and do not enter the semantic Q-wave authority digest.

---

# 11. Final receipt atlas

The previous giant:

```rust
let final_receipt = json!({ ... many fields ... });
```

is forbidden.

Use six ordered receipt waves:

```text
Wave 0 identity + parent
Wave 1 QW01 + QW02
Wave 2 QW03 + QW04
Wave 3 QW05 + QW06
Wave 4 topology/legacy + safety/reproducibility
Wave 5 digests + terminal seal
```

Each wave has independently constructed lanes.
Lane maps are encoded in parallel worker threads and streamed into the root map only after deterministic lane-order sorting.

Required root compatibility:

```text
all former final receipt keys remain top-level keys
```

plus:

```text
qwaveAtlasWaveMap
qwaveAtlasWaveMapRevision
qwaveAtlasPageSize
qwaveComputeWaveCount
qwaveComputeAtlasDigest
```

This preserves downstream `.get("pass")`, `.get("passToken")`, and other key lookups.

---

# 12. Receipt merge determinism

Final receipt merge order:

```text
wave_ordinal
→ lane_ordinal
→ key lexicographic order
```

Duplicate keys fail closed at three levels:

```text
duplicate key inside lane
duplicate key inside fragment
duplicate root key between waves/lanes
```

No last-writer-wins receipt behavior is permitted.

---

# 13. Semantic invariants preserved

R1 does not alter:

```text
R04 CJI authority
QW01 phasor formula
QW02 pulse formula
QW03 R04-owned edge membership
QW03 dynamic formulas
QW04 connected component semantics
QW05 context-candidate semantics
QW06 adjacent-chain graph semantics
legacy authority = 0
hidden fusion = 0
logit mutation = 0
sampler mutation = 0
Medusa prediction = 0
model forward = 0
training mutation = 0
```

Semantic authority digests must be reproducible regardless of page worker scheduling.

---

# 14. CLI additions

Required:

```text
--bt-qwave-atlas-page-size
2

--require-bt-qwave-atlas-parallel-page-map
true

--require-bt-qwave-atlas-streaming-wave-receipt
true

--require-bt-qwave-deterministic-atlas-merge
true

--allow-bt-qwave-monolithic-final-json
false

--allow-bt-qwave-serial-stage-map
false
```

Page size is a runtime scheduling parameter, not a language-model semantic parameter.

---

# 15. Static closure gates

Required before bake:

```text
monolithic final-receipt json! count = 0
crate recursion_limit workaround count = 0
atlas compute waves = 6
QW01 parallel map present
QW02 parallel map present
QW03 parallel map present
QW04 parallel map present
QW05 parallel map present
QW06 terminal wave present
deterministic index merge present
parallel receipt lane worker present
streaming receipt root merge present
duplicate receipt key fail-closed present
R04 edge membership unchanged
legacy authority zero unchanged
hidden/logit/sampler/Medusa/model/training zero unchanged
```

---

# 16. Expected physical evidence

In addition to the existing R05 line, R1 should expose atlas evidence such as:

```text
qwave_atlas_revision=BT-QWAVE-STRUCTURE-05-R1-atlas-parallel-wave-streaming-map-v1
qwave_atlas_page_size=2
qwave_compute_wave_count=6
qw01_page_count=4
qw03_page_count=2
parallel_page_build=1
deterministic_index_merge=1
monolithic_final_json=0
parallel_receipt_lane_build=1
streaming_receipt_merge=1
```

Actual worker counts depend on `available_parallelism()` and are runtime observations.

---

# 17. R1 PASS meaning

A physical R1 PASS proves both:

```text
R05 semantic Q-wave authority is unchanged and reproducible
```

and:

```text
QW01~QW05 independent items are physically scheduled through page-parallel atlas waves,
QW06 closes the ordered dependency graph as a terminal wave,
and the final receipt is built through parallel lanes with deterministic streaming merge,
without using a monolithic json! macro or increased Rust recursion limit.
```

---

# 18. Natural next boundary

R1 does not change the roadmap:

```text
BT-QWAVE-STRUCTURE-05-R1 physical PASS
        ↓
BT-STRUCTURAL-MEDUSA-TARGETS-06A
```

R06A may consume semantic R05 authority fields only. Atlas worker/page scheduling metadata is execution evidence and must not become a Korean structural target.
