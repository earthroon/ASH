# ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-FIRST-CANDIDATE-ELIGIBILITY-REGISTRY-R1

## Status

Implementation-aligned first-candidate routing authority layered on top of `ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-OPTIMIZER-R1`.

This R1 decides **which exact trainable parameter regions are eligible for TensorCube-local Muon and which remain AdamW**. It does not promote Local Muon to the canonical optimizer line and does not mutate the existing AdamW N8 parent.

## Patch identity

```text
TENSORCUBE-LOCAL-MUON-FIRST-CANDIDATE-ELIGIBILITY-REGISTRY-R1
```

## Core contract

```text
Canonical Trainable Parameter Inventory Authority /
Exact 201-Parameter Coverage /

154 Projection-Matrix First-Candidate Admission /
47 Parameter AdamW Preservation /

Q·K·V·O Projection Local-Muon Admission /
Gate·Up·Down Projection Local-Muon Admission /

Norm AdamW Preservation /
Embedding AdamW Preservation /
LM-Head AdamW Preservation /

Exact 16x16 TensorCube Enumeration /
Compact Deterministic Row-Major Grid Authority /
No Expanded Multi-Million Tile JSON Registry /

Strided Matrix Tile Address Authority /
No Fake Contiguous 256-Element Gradient Tile /

Partial Edge Residual → AdamW /
No Zero Padding /
No Cross-Parameter Cube /
No Cross-Layer Cube /

Explicit Element-Domain Partition /
Muon ∩ AdamW = ∅ /
Muon ∪ AdamW = All Trainable Elements /
Unclassified Element Count = 0 /

Registry Digest Authority /
Model-Spec Binding /
Parameter-Inventory Digest Binding /
Optimizer Routing Digest /

No Runtime Shape Guessing /
No Name-Heuristic Fallback /
No Silent Muon Expansion /
No Silent AdamW Fallback /

Immutable Whole-Run Routing /
First-Candidate Experimental Authority /
No Canonical Optimizer Promotion
```

## 1. Parent authority

Required parent implementation:

```text
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-OPTIMIZER-R1
```

The parent provides:

- 16×16 Local-Muon Newton-Schulz execution;
- FP32 Muon momentum authority;
- BF16 working-projection boundary;
- independent three-slot Muon optimizer lease authority;
- AdamW baseline preservation;
- no full-matrix Muon claim.

This R1 adds routing SSOT only.

## 2. Canonical trainable inventory

The first-candidate policy requires:

```text
22 decoder layers
201 logical trainable parameters
```

Canonical order is:

```text
model.embed_tokens.weight
for layer 0..21:
  model.layers.{L}.input_layernorm.weight
  model.layers.{L}.self_attn.q_proj.weight
  model.layers.{L}.self_attn.k_proj.weight
  model.layers.{L}.self_attn.v_proj.weight
  model.layers.{L}.self_attn.o_proj.weight
  model.layers.{L}.post_attention_layernorm.weight
  model.layers.{L}.mlp.gate_proj.weight
  model.layers.{L}.mlp.up_proj.weight
  model.layers.{L}.mlp.down_proj.weight
model.norm.weight
lm_head.weight
```

The registry generator rejects a decoder-layer count other than 22 and rejects a resulting canonical inventory count other than 201.

## 3. Model-spec-derived shapes

Shapes are derived from the supplied canonical `ModelSpec` rather than hard-coded training dimensions.

The generator consumes:

```text
vocab_size
hidden_size
num_layers
num_key_value_heads
head_dim
intermediate_size
```

and derives:

```text
q_proj    [hidden, hidden]
k_proj    [kv_width, hidden]
v_proj    [kv_width, hidden]
o_proj    [hidden, hidden]
gate_proj [intermediate, hidden]
up_proj   [intermediate, hidden]
down_proj [hidden, intermediate]
```

where:

```text
kv_width = num_key_value_heads × head_dim
```

`intermediate_size` is never guessed by the registry patch.

## 4. First-candidate Muon families

Exactly seven parameter families are eligible:

```text
Q_PROJ
K_PROJ
V_PROJ
O_PROJ
GATE_PROJ
UP_PROJ
DOWN_PROJ
```

Across 22 layers:

```text
22 × 7 = 154 projection parameters
```

The implementation requires:

```text
candidateProjectionParameterCount = 154
```

## 5. Explicit AdamW-preserved parameters

R1 preserves AdamW for:

```text
22 × input_layernorm.weight
22 × post_attention_layernorm.weight
model.norm.weight
model.embed_tokens.weight
lm_head.weight
```

Total:

```text
47 parameters
```

The implementation requires:

```text
explicitAdamwParameterCount = 47
```

Embedding and LM head remain AdamW even though they are rank-2 matrices.

## 6. No runtime shape guessing

Forbidden routing rules include:

```text
rank == 2 → Muon
name contains "proj" → Muon
name contains "attn" → Muon
matrix-shaped parameter → Muon
```

Routing originates only from the fixed first-candidate parameter-family table plus the exact canonical inventory.

Required counters:

```text
runtimeShapeGuessCount = 0
silentMuonExpansionCount = 0
silentAdamwFallbackCount = 0
```

## 7. Default route semantics

Every parameter entry declares:

```text
defaultRoute = ADAMW
```

For projection parameters, the explicit full 16×16 grid overrides the covered element region to:

```text
MUON_LOCAL_16X16
```

`defaultRoute = ADAMW` is **not** a missing-parameter fallback. All 201 parameter identities must be present in exact canonical order.

## 8. Exact local geometry

Local-Muon geometry is fixed:

```text
16 × 16 = 256 elements
```

No 8×8, 32×32, rectangular, padded, or cross-parameter tile is admitted in R1.

## 9. Compact exact grid authority

A naive registry that emits one JSON object for every 16×16 tile would create millions of tile entries for the current model class and would itself become a memory/parse/storage bottleneck.

R1 therefore stores exactly one compact grid descriptor per Muon-candidate parameter.

Required grid fields include:

```text
optimizerRoute = MUON_LOCAL_16X16
enumerationOrder = ROW_MAJOR_TILE_GRID
cubeIdentityFormat = muon16:<parameterId>:r<rowStart>:c<colStart>
originRow = 0
originCol = 0
tileRows = 16
tileCols = 16
rowStrideElements = parameter column count
fullTileRows = floor(rows / 16)
fullTileCols = floor(cols / 16)
tileCount = fullTileRows × fullTileCols
muonElementCount = tileCount × 256
momentumBaseElementOffset
```

Required global counters:

```text
compactGridDescriptorCount = 154
expandedTileJsonEntryCount = 0
```

This is a compact representation of an exact deterministic enumeration, not an automatic runtime shape heuristic.

## 10. Deterministic tile resolution

A tile is resolved from:

```text
parameter canonical index
cubeRow
cubeCol
```

with:

```text
rowStart = originRow + cubeRow × 16
colStart = originCol + cubeCol × 16
```

Cube identity:

```text
muon16:<parameterId>:r<rowStart>:c<colStart>
```

Tile ordinal:

```text
tileOrdinal = cubeRow × fullTileCols + cubeCol
```

Momentum offset:

```text
momentumElementOffset = momentumBaseElementOffset + tileOrdinal × 256
```

The same registry therefore determines both Local-Muon tile identity and deterministic momentum-pack address without storing millions of strings or a per-tile `BTreeMap` in the registry artifact.

## 11. Strided row-major tile address repair

A 16×16 submatrix inside a wider row-major matrix is **not** physically represented by one contiguous 256-element range.

For example, a tile inside `[2048, 2048]` has row stride 2048.

Therefore R1 supersedes the earlier simplified contiguous-gradient assumption.

Logical top-left offset:

```text
linearElementOffset = rowStart × rowStrideElements + colStart
```

Gradient address for local row/column `(r,c)`:

```text
gradientIndex =
  gradientBaseOffsetElements
  + r × gradientRowStrideElements
  + c
```

The WGSL Local-Muon kernel now accepts:

```text
gradient_base_offset_elements
gradient_row_stride_elements
```

and no longer reads:

```text
gradient[offset + localIndex]
```

as if the 16×16 matrix tile were contiguous.

## 12. Source weight and momentum working layout

The Local-Muon candidate kernel still receives bounded 256-element source-weight and source-momentum staging arrays.

Those arrays are local working projections, not claims that the parent parameter is physically contiguous by 16×16 tile in canonical storage.

The registry SSOT preserves logical matrix coordinates and row stride; physical packed-byte resolution remains owned by the existing packed parameter/segment authority.

## 13. No shadow packed-offset SSOT

The eligibility registry answers:

```text
WHO is Muon and at which logical matrix coordinates?
```

The existing packed runtime state answers:

```text
WHERE are the physical bytes?
```

R1 does not duplicate packed byte offsets into a second optimizer storage registry.

## 14. Partial-edge policy

For a candidate matrix of shape `[rows, cols]`:

```text
fullTileRows = floor(rows / 16)
fullTileCols = floor(cols / 16)
```

Only:

```text
fullTileRows × fullTileCols × 256
```

elements are Muon-eligible.

All remaining edge elements stay AdamW:

```text
edgeResidualElementCount = parameterElementCount - muonElementCount
```

No zero padding is permitted.

## 15. No cross-boundary assembly

Forbidden:

- joining edge rows from two parameters;
- joining tiles across decoder layers;
- flattening TensorCube depth into another matrix axis without explicit authority;
- joining non-adjacent matrix regions into one Local-Muon tile.

Each Local-Muon tile belongs to one parameter and one explicit matrix plane.

## 16. Exact element-domain partition

Let:

```text
T = all trainable elements
M = Local-Muon eligible elements
A = AdamW elements
```

R1 requires:

```text
M ∪ A = T
M ∩ A = ∅
unclassifiedElementCount = 0
overlapElementCount = 0
```

The registry records:

```text
totalTrainableElementCount
muonEligibleElementCount
adamwElementCount
edgeResidualElementCount
muonTileCount
```

These element counts are computed from the supplied model spec and are not hard-coded in the patch.

## 17. Momentum domain

The compact grids establish the future Muon momentum domain.

Momentum is allocated only for Local-Muon eligible elements:

```text
MuonMomentumElementCount = muonEligibleElementCount
```

Each candidate parameter receives a deterministic `momentumBaseElementOffset` in canonical parameter order.

The registry does not yet delete or rewrite existing Adam M/V checkpoint state. Hybrid state materialization remains a separate later authority.

## 18. Model-spec binding

The generator hashes the exact supplied model-spec file bytes:

```text
modelSpecDigest = SHA256(model_spec_file_bytes)
```

It also binds:

```text
modelSpecId
```

A registry produced for one model-spec file cannot be silently reused with another file whose digest differs.

## 19. Parameter-inventory digest

The inventory digest binds canonical ordered fields:

```text
parameterId
canonicalIndex
parameterFamily
rank
shape
elementCount
dtypeExpectation
```

The inventory digest is independent of JSON whitespace.

## 20. Optimizer-routing digest

A second digest binds routing semantics:

```text
parameter identity
canonical index
family
default route
compact Muon grid geometry
row stride
grid extent
tile count
momentum base offset
```

This digest represents the whole-run optimizer route map.

## 21. Registry digest

The registry also carries a registry-document digest over the complete serialized semantic object with its own digest field cleared.

The three authorities remain distinct:

```text
parameterInventoryDigest
optimizerRoutingDigest
registryDigest
```

## 22. Whole-run immutability

Once a hybrid Local-Muon run is admitted, `optimizerRoutingDigest` is immutable for the run.

Changing the grid set or candidate policy creates a new optimizer lineage; runtime hot reload of routing is not admitted.

## 23. Generator binary

R1 adds:

```text
generate_tensorcube_local_muon_first_candidate_registry
```

Inputs:

```text
--model-spec-path <MODEL_SPEC>
--output-path <REGISTRY_JSON>
```

The binary loads the canonical `ModelSpec`, computes the first-candidate registry, verifies it, writes compact JSON, prints the exact counts/digests, then emits:

```text
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_FIRST_CANDIDATE_ELIGIBILITY_REGISTRY_R1
HOLD_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_FIRST_CANDIDATE_REGISTRY_READY_PHYSICAL_HYBRID_NOT_YET_ADMITTED
```

## 24. Rust instance validator

R1 adds:

```text
validate_tensorcube_local_muon_first_candidate_registry
```

Inputs:

```text
--model-spec-path <MODEL_SPEC>
--registry-path <REGISTRY_JSON>
```

It verifies model-spec SHA, inventory, counts, compact grids, routing digest, registry digest, exact partition, and deterministic momentum coverage.

## 25. Independent Python instance validator

R1 also adds:

```text
tools/validate_tensorcube_local_muon_registry_instance.py
```

This performs a second semantic validation surface over:

- exact 201-parameter count;
- 154/47 policy split;
- model-spec SHA;
- compact grid geometry;
- row stride;
- tile counts;
- momentum-base continuity;
- element union;
- edge residuals;
- no silent routing counters.

It does not replace the Rust digest verifier; it is independent evidence against generator/consumer coupling errors.

## 26. Static validator

R1 adds:

```text
tools/validate_tensorcube_local_muon_first_candidate_registry_static.py
```

It verifies implementation surfaces including:

- exact candidate family table;
- exact 201 / 22 / 154 / 47 constants;
- compact grid authority;
- no expanded tile JSON;
- model-spec-derived intermediate size;
- deterministic row-major resolution;
- routing/inventory/model binding;
- row-stride gradient repair;
- generator and instance-validator binaries;
- CF1 registration.

## 27. Parent Local-Muon validator repair

The existing Local-Muon static validator is strengthened to require:

```text
gradient_tile_base_element_offset
gradient_row_stride_elements
strided WGSL gradient address
```

and to reject the former fake contiguous expression:

```text
params.gradient_offset_elements + i
```

## 28. CF1 binding

The new static validator is part of:

```text
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

Any source change in this R1 invalidates the previous CF1 source-tree digest. A fresh CF1 receipt is required before later physical training execution.

## 29. Current static evidence

Container static evidence at bake time:

```text
First-Candidate Registry        92/92 PASS
TensorCube Local Muon parent   101/101 PASS
RAM Adam M/V PCIe overlap       PASS
RAM Resident Adam M/V           PASS
N8 Long Horizon                70/70 PASS
Storage Root                   39/39 PASS
Scheduler Extension            23/23 PASS
Subgroup32 AdamW               36/36 PASS
R14                            52/52 PASS
```

This is static evidence only. No Rust toolchain/WGPU physical device was available in the bake environment, so compile or physical Local-Muon PASS is not claimed.

## 30. PASS meaning

Registry instance PASS:

```text
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_FIRST_CANDIDATE_ELIGIBILITY_REGISTRY_R1
```

means only:

- the supplied model spec yields the exact canonical 201-parameter inventory;
- exactly 154 projection parameters carry compact Local-Muon 16×16 grid authority;
- exactly 47 parameters are explicitly AdamW-preserved;
- every trainable element is assigned exactly once to Muon or AdamW;
- no partial tile is padded into Muon;
- routing is model/inventory/digest bound;
- tile resolution is deterministic and row-stride correct.

It does **not** mean Local Muon is faster, converges better, or is ready for canonical optimizer promotion.

## 31. HOLD frontier

After a valid registry exists:

```text
HOLD_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_FIRST_CANDIDATE_REGISTRY_READY_PHYSICAL_HYBRID_NOT_YET_ADMITTED
```

The natural next authority is hybrid optimizer-state materialization:

```text
Muon domain  → FP32 Momentum Pack
AdamW domain → Adam M/V authority
```

with one global optimizer transaction and no split optimizer epoch.

## 32. Non-goals

R1 does not add:

- full-matrix Muon;
- automatic rank-2 Muon routing;
- embedding Muon;
- LM-head Muon;
- norm Muon;
- zero-padded edge Muon;
- cross-layer/cross-parameter tiles;
- multi-million expanded tile registry artifacts;
- native BF16/TensorCore performance claims;
- existing Adam state deletion;
- automatic Adam-to-Muon state migration;
- canonical optimizer promotion.

## SSOT seal

```text
TRAINABLE PARAMETER COUNT = 201
DECODER LAYERS            = 22

FIRST-CANDIDATE MUON      = q/k/v/o + gate/up/down
MUON CANDIDATE PARAMETERS = 154
ADAMW-PRESERVED PARAMETERS= 47

MUON TILE                 = exact 16×16
ENUMERATION               = deterministic row-major compact grid
EXPANDED TILE JSON        = 0
PARTIAL EDGE              = AdamW

MATRIX TILE ADDRESS       = strided row-major
FAKE CONTIGUOUS 256 READ  = forbidden

MUON ∪ ADAMW              = all trainable elements
MUON ∩ ADAMW              = empty
UNCLASSIFIED              = 0

MODEL BINDING             = modelSpecId + exact file SHA256
INVENTORY BINDING         = parameterInventoryDigest
ROUTING BINDING           = optimizerRoutingDigest

RUNTIME SHAPE GUESS       = 0
SILENT MUON EXPANSION     = 0
SILENT ADAMW FALLBACK     = 0

CURRENT ADAMW N8 PARENT   = unchanged
PHYSICAL HYBRID           = not yet admitted
CANONICAL PROMOTION       = not admitted
```
