# ASH-BP-DK-FUSION-CANDIDATE-GRAPH-04

## Status

```text
Patch ID: ASH-BP-DK-FUSION-CANDIDATE-GRAPH-04
Direct parent: ASH-BP-DK-BRIDGE-TEMPORAL-COUPLING-OBSERVATION-03B
Upstream: 03A Pair Evidence, 02 Freshness Seal, 01 Local BP-DK, 00 Observation Contract
Graph scope: same parameter only
Graph lifetime: current BP generation only
Fusion decision authority: none
Physical fusion authority: none
Muon momentum authority: none
Optimizer topology authority: none
New GPU shader: none
```

## Central SSOT

04 creates a deterministic evidence graph projection only:

```text
VerifiedCurrent local BP-DK observations
        -> graph nodes

03A current same-parameter pair evidence
+ 03B Ready temporal Bridge observations
        -> graph edges
```

Authority remains separated:

```text
Node evidence authority = 01 + 02
Spatial pair authority = 03A
Temporal Bridge Delta-K authority = 03B
Graph authority = derived current-generation projection only
```

A graph edge is not fusion permission. A connected path is not a fused domain. 04 contains no scalar fusion score, threshold, ranking policy, connected-component decision, Fuse/Fission/Cooldown output, or physical HiMuon fusion.

## VerifiedCurrent node admission

The production callsite already holds `bridge_verified_current` immediately after local BP-DK observation and 02 freshness verification. 04 consumes those exact `VerifiedCurrentBpDeltaKObservation` values rather than reading raw `AshBpPreDeltaKObservation` as graph authority.

The production callsite also records the typed canonical tile ordinal at the moment the VerifiedCurrent wrapper is created. Graph topology therefore does not recover tile coordinates by parsing `parameter_id` or `tensorcube_id` strings.

Node evidence preserves the existing local observation fields:

```text
observation_id
I_BP
M_BP
DeltaK_BP_PRE raw
DeltaK_BP_PRE smoothed
parameter_revision
optimizer_generation
bp_generation
source_weight_digest
registry_digest
optimizer_routing_digest
local observation policy digest
```

## Canonical node identity

Each node binds:

```text
parameter_id
canonical_parameter_index
tensorcube_id
tile_ordinal
cube_row
cube_col
row_start
col_start
```

Geometry comes from `FirstCandidateEligibilityRegistry::resolve_tile()` using the typed tile ordinal. Nodes are sorted by `tile_ordinal` ascending. Duplicate tile ordinals or duplicate TensorCube identities fail closed.

## Isolated node preservation

A VerifiedCurrent local node remains present even when none of its 03A pairs has a 03B Ready temporal observation.

Therefore the following is valid:

```text
V > 0
E = 0
```

03B Warming does not become a fake zero-valued edge and does not delete the local node.

## Same-parameter graph partition

04 produces one independent graph for each current Muon parameter invocation. No whole-step PRE barrier is introduced.

Production ordering remains:

```text
parameter-local gradient pack
-> local BP-DK
-> 02 VerifiedCurrent
-> 03A pair evidence
-> 03B temporal observation
-> 04 parameter-local graph projection
-> existing Local Muon execution
```

Cross-parameter, cross-layer, Q/K/V, Gate/Up/Down, or global graph edges remain outside this revision.

## 03A / 03B edge admission

An edge exists only when the same canonical pair has:

```text
03A current pair evidence
+
03B Ready temporal observation
+
both endpoint nodes present as VerifiedCurrent local nodes
```

03A evidence with 03B Warming is counted as missing temporal evidence and omitted from `edges[]`.

A 03B Ready temporal observation without its exact 03A pair is a structural contradiction and fails closed.

## Exact pair / temporal join

04 joins 03A and 03B by `AshBpDkBridgeTemporalPairKey`, derived from the typed `AshBpDkBridgePairIdentity`.

The join verifies:

```text
exact pair identity
parameter_revision
optimizer_generation
bp_generation
source_weight_digest
Bridge policy revision/digest
Bridge topology revision/digest
current signed gradient cosine bit identity
local endpoint I/M/Delta-K bit identity
```

No last-good edge, mixed-generation edge, or silent numeric reconciliation is admitted.

## Edge evidence vector

04 deliberately does not collapse evidence to a single scalar. Each canonical edge retains:

```text
03A:
    gradient dot
    lhs gradient norm2
    rhs gradient norm2
    signed exact-256D gradient cosine

03B:
    I_BRIDGE
    M_BRIDGE
    DeltaK_BRIDGE_PRE raw
    DeltaK_BRIDGE_PRE smoothed

Endpoint bindings:
    lhs local I/M/Delta-K
    rhs local I/M/Delta-K
```

Signed cosine remains signed. No `abs(cosine)`, negative-to-zero clamp, fusion score, compatibility score, priority score, or edge score is introduced.

## Canonical edge identity and ordering

04 reuses the exact 03A `AshBpDkBridgePairIdentity`. Each Right/Down evidence pair is stored exactly once in canonical `edges[]`.

Canonical edge ordering:

```text
pair_ordinal ascending
```

A reverse `B -> A` evidence edge is not created.

## Bidirectional adjacency projection

Traversal convenience uses CSR-style adjacency:

```text
adjacency_offsets
adjacency_edge_indices
```

The same canonical edge index is referenced from both endpoint nodes. Therefore:

```text
adjacency reference count = 2 * canonical edge count
```

CSR is an acceleration/projection structure only. Canonical graph evidence remains `nodes[]` and `edges[]`.

R1 grid topology also seals:

```text
semantic undirected degree(node) <= 4
```

Any degree above four is a topology contradiction.

## O(V+E) assembly / no N² reconstruction

04 does not rediscover adjacency by comparing every node with every other node.

The implementation uses ordered maps keyed by typed tile/pair identities:

```text
node_index_by_tile
pair_by_key
temporal_by_key
```

and iterates admitted nodes, 03A pairs, 03B Ready observations, and canonical edges once. No pair combinations, Cartesian product, semantic similarity scan, or N² pair reconstruction is introduced.

## Generation-coherent graph identity

Each graph binds:

```text
schema revision
parameter_id
canonical_parameter_index
parameter_revision
optimizer_generation
bp_generation
source_weight_digest
registry_digest
optimizer_routing_digest
local observation policy digest
Bridge policy revision/digest
Bridge topology revision/digest
```

Nodes, 03A evidence, and 03B Ready temporal observations must match this identity. Contradictory lineage fails closed.

## Deterministic topology digest

04 introduces a structural digest over:

```text
Graph topology digest revision
graph schema
parameter identity
Bridge topology identity
ordered node identities
ordered edge identities
```

Numerical evidence is intentionally excluded.

Therefore a graph with the same nodes/edges but changed cosine keeps the same topology digest.

## Deterministic evidence digest

A separate evidence digest binds current-generation state and numerical evidence:

```text
parameter/generation/digest lineage
local policy identity
Bridge policy/topology identity
ordered node identities and local BP-DK evidence
ordered edge identities and all edge evidence fields
```

F32 values are hashed through exact `to_bits().to_le_bytes()` representation. Optional smoothed local Delta-K values have explicit presence tags.

Thus:

```text
same structure + changed numerical evidence
-> topology digest unchanged
-> evidence digest changed
```

These two digests prepare the later deterministic replay revision without granting replay authority to 04 itself.

## Current-generation lifetime

`ProductionMuonRuntime` stores only the current generation's `bp_dk_fusion_candidate_graphs` diagnostic/consumer surface.

When the existing BP-DK Bridge generation advances, the current graph vector is explicitly cleared together with the current 03A/03B surfaces.

No last-good graph, historical graph state, graph checkpoint sidecar, graph restore path, or durable graph authority is introduced.

## No GPU gradient work

04 adds no WGSL shader and no `burn_webgpu_backend` graph module.

Gradient direction evidence is reused from 03A. Therefore new 04 authority remains:

```text
full-gradient D2H = 0
new gradient GPU reduction = 0
new gradient shader = 0
```

The graph modules do not import WGPU or `burn_webgpu_backend`.

## No optimizer authority

04 does not bind or mutate:

```text
Muon momentum
candidate momentum
candidate weight
Adam M/V
Newton-Schulz workspace
optimizer route
tile ownership
precision policy
residency policy
```

Production hard-zero counters include:

```text
fusion_graph_n2_pair_scan_count = 0
fusion_graph_connected_component_decision_count = 0
fusion_graph_threshold_decision_count = 0
fusion_graph_fusion_decision_count = 0
fusion_graph_muon_momentum_read_count = 0
fusion_graph_muon_momentum_write_count = 0
fusion_graph_optimizer_topology_mutation_count = 0
fusion_graph_gradient_payload_readback_count = 0
fusion_graph_gradient_payload_readback_bytes = 0
fusion_graph_gradient_gpu_reduction_count = 0
```

## Runtime cardinality closure

Successful production execution seals:

```text
Right edge count + Down edge count
= canonical graph edge count

adjacency reference count
= 2 * canonical graph edge count

one graph build
= one Muon parameter invocation

duplicate node count = 0
duplicate edge count = 0
dangling edge count = 0
```

The graph can have zero nodes on a fully Warming local-BP generation and can have nodes with zero edges when 03B remains Warming.

## Structural fixtures

R1 physical topology expectations remain:

```text
1x1 all-current grid -> maximum E = 0
2x2 all-ready grid -> maximum E = 4
3x2 all-ready grid -> maximum E = 7
```

The actual 04 edge count can be lower because only 03B Ready pairs are admitted.

## Changed files

The baked 04 overlay contains exactly seven changed/new files:

```text
crates/ash_core/src/bp_dk_fusion_candidate_graph.rs
crates/ash_core/src/lib.rs
crates/base_train/src/bp_delta_k_fusion_candidate_graph.rs
crates/base_train/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_fusion_candidate_graph_04_static.py
```

No `burn_webgpu_backend` or WGSL file changed.

## Static validation

New gate:

```text
validate_ash_bp_dk_fusion_candidate_graph_04_static.py
235/235 PASS
```

Revalidated gates in the bake environment:

```text
BP-DK contract 00                                      149/149 PASS
BP-DK local observation 01                             134/134 PASS
BP-DK stale observation seal 02                        243/243 PASS
BP-DK Bridge pair evidence 03A                         148/148 PASS
BP-DK Bridge temporal coupling 03B                     157/157 PASS
Fusion Candidate Graph 04                              235/235 PASS
Local Muon optimizer                                   101/101 PASS
FirstCandidate registry                                 97/97 PASS
Local Muon multi-tile batch                             61/61 PASS
Local Muon production callsite                          63/63 PASS
Muon registry canonical loader repair                   38/38 PASS
Muon ExactSubgroup32 norm                              128/128 PASS
Muon X PAD17                                            52/52 PASS
```

04 is appended to the existing CF1 static validator chain.

Parent byte-preservation anchors for Decode Delta-K and existing Local Muon WGSL remain unchanged.

## Physical execution boundary

The bake environment does not provide `cargo`, `rustc`, `rustfmt`, or a physical WGPU runtime. Therefore this bake does not claim local Rust compilation or physical training execution.

User-local verification remains the physical SSOT for:

```text
cargo fmt / cargo check
CF1 compile chain
1x1 / 2x2 / 3x2 runtime graph fixtures
03B Warming -> node-preserved edge omission
same structure / changed evidence digest behavior
04 ON/OFF Local Muon candidate parity
```

Static evidence is sufficient for source-contract closure only.

## Bake packaging

The delivered code bake is separated into full-body and overlay ZIPs. The overlay contains the exact seven files listed above. Generated artifact/manifest/report directories and `*.sha256` files are excluded from the ZIP packaging.

## Non-goals

```text
No cross-parameter graph
No cross-layer graph
No new Delta-K formula
No scalar fusion score
No edge ranking
No fusion/cosine/Delta-K threshold
No connected-component fusion
No transitive fusion implication
No shadow Fuse/Fission/Cooldown planner yet
No logical fused TensorCube domain
No physical fused Muon
No fused momentum
No fused Newton-Schulz
No POST effectiveness judgment
No precision authority
No residency authority
No graph checkpoint authority
No new gradient shader
No gradient D2H
No optimizer topology mutation
```

## Natural successor

```text
ASH-BP-DK-SHADOW-FUSION-FISSION-PLANNER-05
```

05 may consume the immutable current-generation 04 graph and an explicit planner policy to emit shadow-only `would_stay_local`, `would_fuse`, `would_fission`, and `would_cooldown` decisions. 05 must not mutate the 04 graph and must still leave physical optimizer state untouched.

## Promotion seal

```text
PROMOTE_ASH_BP_DK_FUSION_CANDIDATE_GRAPH_04

VERIFIED_CURRENT_LOCAL_NODE_AUTHORITY
03A_CURRENT_PAIR_EVIDENCE_BOUND
03B_READY_TEMPORAL_EVIDENCE_BOUND

SAME_PARAMETER_GRAPH_ONLY
NO_GLOBAL_PRE_BARRIER

CANONICAL_TYPED_NODE_IDENTITY
CANONICAL_TYPED_EDGE_IDENTITY
NO_PARAMETER_ID_STRING_PARSING

CANONICAL_EDGE_SINGLE_STORAGE
BIDIRECTIONAL_ADJACENCY_IS_PROJECTION_ONLY
DEGREE_BOUND_FOUR

GENERATION_COHERENT_EVIDENCE_JOIN
NO_MIXED_GENERATION_GRAPH
NO_LAST_GOOD_GRAPH

O_V_PLUS_E_ASSEMBLY
NO_N2_PAIR_RECONSTRUCTION

LOCAL_I_M_DELTAK_PRESERVED
SIGNED_256D_COSINE_PRESERVED
BRIDGE_I_M_DELTAK_PRESERVED

NO_SCALAR_FUSION_SCORE
NO_THRESHOLD
NO_RANKING
NO_CONNECTED_COMPONENT_FUSION
NO_TRANSITIVE_FUSION_IMPLICATION

ISOLATED_NODES_PRESERVED
GRAPH_IS_DERIVED_PROJECTION
GRAPH_IS_NOT_OBSERVATION_SSOT

DETERMINISTIC_TOPOLOGY_DIGEST
DETERMINISTIC_EVIDENCE_DIGEST

NO_NEW_GPU_GRADIENT_WORK
NO_GRADIENT_D2H

NO_FUSE_DECISION
NO_FISSION_DECISION
NO_COOLDOWN_DECISION
NO_PHYSICAL_FUSION
NO_MUON_MOMENTUM_MUTATION
NO_OPTIMIZER_TOPOLOGY_MUTATION
```
