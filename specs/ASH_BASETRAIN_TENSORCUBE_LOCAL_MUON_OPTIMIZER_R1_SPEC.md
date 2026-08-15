# ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-OPTIMIZER-R1

## Status

Implementation-aligned experimental optimizer authority layered beside the current AdamW BaseTrain line.

This R1 bakes the exact 16×16 Local-Muon compute primitive, explicit eligibility/profile authorities, FP32 momentum ownership, bounded three-slot momentum lease machinery, CPU reference parity surface, drift-ledger schema, and CF1 static closure.

**R1 does not invent a TensorCube eligibility map.** No production model cube is routed to Muon until an explicit registry is supplied and physically reviewed. Existing AdamW N8 authority therefore remains untouched by default.

## Patch identity

```text
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-OPTIMIZER-R1
```

## Core contract

```text
TensorCube-Scoped Muon /
No Full-Matrix Muon /

16x16 Local Orthogonalization /
TensorCube Geometry Preservation /
No Cross-Cube Orthogonalization /

Cube-Resident Momentum Authority /
No Adam M/V Authority For Muon-Admitted Cubes /

TensorCube Eligibility Registry /
Explicit Muon-vs-AdamW Routing /
No Runtime Shape Guessing /

Newton-Schulz TensorCube Execution /
BF16 NS Compute Projection Allowed /
FP32 Momentum Authority Preservation /

Triple-Buffered Momentum Transfer Authority /
Existing TensorCube Ring Compatibility /
No Atlas/Optimizer Lease Identity Coupling /

Local-Muon Is Not Full-Matrix Muon /
No Global Orthogonality Claim /

AdamW Baseline Reference Surface /
Loss·Weight·Gradient Drift Ledger /
No Silent Optimizer Substitution
```

## 1. Optimizer scope

Muon is admitted only for explicitly registered 16×16 TensorCube-local regions.

The runtime must never infer Muon eligibility from tensor rank, shape, parameter name, layer type, or matrix appearance.

The optimizer family is intended to become:

```text
explicit MUON_LOCAL_16X16 region → Local Muon
all explicitly classified residual regions → AdamW
```

No full-parameter or full-model Muon conversion occurs in this patch.

## 2. Local Muon is not full-matrix Muon

For a full parameter matrix `G`, this R1 does not claim:

```text
LocalMuon(tile_0) ⊕ LocalMuon(tile_1) ... == Muon(G)
```

Each registered tile is orthogonalized independently.

Therefore the following claims are forbidden:

- global orthogonality;
- cross-cube singular-vector alignment;
- equivalence to full-matrix Muon;
- cross-cube Gram authority;
- whole-parameter Newton-Schulz authority.

## 3. Exact geometry

Muon execution geometry is fixed at:

```text
16 rows × 16 columns = 256 elements
```

A registered Local-Muon tile must have exactly:

```text
rows = 16
cols = 16
optimizerRoute = MUON_LOCAL_16X16
```

R1 does not admit 8×8, 32×32, rectangular, partial-edge, padded, or cross-cube Muon tiles.

## 4. TensorCube geometry preservation

An ASH `16×16×4` TensorCube is not silently flattened to `16×64`.

Any relationship between the TensorCube depth axis and Local-Muon planes must be supplied explicitly by the eligibility registry through `tensorCubeId`, `planeIdentity`, and `elementOffset`.

No runtime depth-axis reinterpretation is admitted.

## 5. Eligibility registry SSOT

Schema:

```text
ash.basetrain.tensorcube_local_muon_registry.v1
```

Each trainable parameter must appear exactly once in the registry with:

- exact `parameterId`;
- exact logical element count;
- explicit default route;
- zero or more explicit Muon tiles.

R1 requires the default route to be `ADAMW` and treats listed Local-Muon tiles as explicit non-overlapping overrides.

The registry must cover the entire trainable parameter inventory. Missing parameters fail closed.

## 6. No runtime shape guessing

Forbidden examples:

```text
rank == 2 → Muon
rows >= 16 → Muon
hidden layer name → Muon
matrix-shaped parameter → Muon
```

Runtime counter:

```text
runtimeShapeGuessCount = 0
```

is part of the structural receipt.

## 7. Registry range rules

Every Muon tile must satisfy:

- unique TensorCube identity;
- non-empty plane identity;
- exact 256-element range;
- range fully inside its declared parameter;
- no overlap with another Muon tile;
- no duplicate cube identity.

The plan records:

```text
muonEligibleCubeCount
muonEligibleElementCount
adamwElementCount
unclassifiedElementCount
muonAdamOverlapElementCount
muonMutableRangeOverlapCount
```

Successful structural admission requires the last three invalid-domain counters to be zero.

## 8. Registry digest

The registry carries an explicit digest and is validated before use.

A changed route map is a different optimizer authority. There is no silent registry rewrite or implicit migration.

## 9. Local-Muon profile SSOT

Schema:

```text
ash.basetrain.tensorcube_local_muon_profile.v1
```

The profile explicitly binds:

- learning rate;
- momentum beta;
- weight decay;
- Nesterov mode;
- Newton-Schulz iteration count;
- Newton-Schulz coefficients `a`, `b`, `c`;
- normalization epsilon;
- NS working precision mode;
- momentum authority dtype;
- momentum initialization policy;
- full-matrix/cross-cube/global-orthogonality claim bits.

No production hyperparameter profile is silently baked by R1.

## 10. Profile digest uses exact numeric bits

Floating-point profile fields are digested from their exact F32 bit representations rather than JSON whitespace or decimal formatting.

Profile identity therefore cannot drift because another serializer prints an equivalent decimal differently.

## 11. Reference coefficient fixture

The unit-test reference uses the well-known quintic Muon/Newton-Schulz coefficient fixture:

```text
a = 3.4445
b = -4.7750
c = 2.0315
```

with five iterations and epsilon `1e-7` only as a deterministic reference fixture.

Those test values are not an automatically selected production profile. Runtime use still requires an explicit profile authority.

## 12. Persistent state ownership

For a production-admitted Local-Muon tile, the intended persistent optimizer state is:

```text
Weight
FP32 Muon Momentum
```

and not:

```text
Weight
Adam M
Adam V
```

The structural receipt therefore fixes:

```text
muonCubeAdamMAuthorityCount = 0
muonCubeAdamVAuthorityCount = 0
adamwCubeMuonMomentumAuthorityCount = 0
```

R1 does not claim the existing AdamW N8 checkpoint format has already been replaced. That durable hybrid checkpoint promotion remains closed until an explicit route registry is supplied and the hybrid state format is physically adopted.

## 13. FP32 momentum authority

Muon momentum authority is exactly:

```text
F32
```

The implementation owns a contiguous momentum pack indexed by explicit TensorCube identity.

No `Vec<Vec<f32>>` per-cube allocation forest is used for authoritative momentum.

## 14. Explicit new-lineage initialization

A Local-Muon optimizer lineage cannot reinterpret Adam `M` as Muon momentum.

Forbidden:

```text
MuonMomentum = AdamM
MuonMomentum = f(AdamM, AdamV)
```

The current R1 initialization contract accepts only:

```text
ZERO_NEW_OPTIMIZER_LINEAGE
```

for a newly created experimental Muon lineage.

This is explicit initialization, not a resume fallback.

## 15. No zero-momentum resume fallback

Once a Muon lineage has durable momentum authority, missing momentum must fail closed.

A later resume must never convert a missing momentum file into zero momentum.

R1 reserves:

```text
zeroMomentumResumeFallbackCount = 0
momentumReconstructionCount = 0
```

## 16. GPU Local-Muon candidate ABI

Backend ABI:

```text
tensorcube_local_muon_16x16_candidate(...)
```

Inputs:

- exact raw GPU gradient lease;
- local gradient element offset;
- 256 source weights;
- 256 source momentum values;
- global optimizer step;
- explicit Local-Muon profile.

Outputs:

- 256 candidate weights;
- 256 candidate momentum values;
- 256 orthogonalized update values;
- compact nonfinite/completion status.

Raw gradient payload readback remains zero.

## 17. Momentum recurrence

For each local element:

```text
m = beta * m_prev + (1 - beta) * grad
```

If Nesterov is enabled, the Local-Muon update seed is explicitly derived from gradient and updated momentum.

Momentum recurrence and Newton-Schulz orthogonalization are separate stages.

## 18. Local normalization

The 16×16 update seed is normalized only from the current Local-Muon tile.

No neighbor-cube or global parameter statistic enters the Local-Muon normalization path.

## 19. Newton-Schulz execution

The fixed-square tile computes a quintic iteration:

```text
A  = X · Xᵀ
AA = A · A
B  = b·A + c·AA
X  = a·X + B·X
```

for the profile-selected number of iterations.

All intermediate matrices are 16×16 workgroup-local values.

## 20. Workgroup geometry

The R1 WGSL kernel launches one 256-invocation workgroup for one 16×16 tile.

Each invocation owns one matrix element while workgroup barriers close the matrix stages.

R1 does not construct a generic large-matrix Muon kernel.

## 21. Decoupled weight decay

The Local-Muon candidate applies explicit decoupled weight decay followed by the orthogonalized update:

```text
candidateWeight = sourceWeight * (1 - lr * weightDecay) - lr * localMuonUpdate
```

Changing this formula requires a new optimizer profile/patch authority.

## 22. BF16 boundary

Persistent momentum remains FP32.

R1 supports the working precision identity:

```text
F32
BF16_EMULATED_F32_ARITHMETIC
```

The second mode projects NS working values to BF16 precision by explicit F32 bit rounding/truncation but continues arithmetic through WGSL F32 operations.

Therefore R1 does **not** claim native WGPU BF16 Tensor Core execution.

A later native BF16/TensorCore backend requires its own physical admission and measurement.

## 23. No silent precision fallback

If a future explicit profile requests a precision mode that is unsupported, it must fail closed.

R1 does not silently map an unknown BF16/native mode to F32.

## 24. Triple-buffered momentum transfer authority

Local-Muon owns an independent three-slot lease ring:

```text
slot0
slot1
slot2
```

This ring is distinct from the Adam M/V PCIe ring and distinct from the Atlas/TensorCube compute ring.

## 25. Muon lease lifecycle

R1 Local-Muon lease states:

```text
FREE
→ MOMENTUM_H2D
→ NS_COMPUTE
→ UPDATE_D2H
→ RAM_MOMENTUM_COMMIT
→ FREE
```

`FAILED` is an explicit quarantine state.

Each reuse increments a lease epoch.

## 26. No slot reuse before RAM commit

A slot cannot be reused before its candidate momentum is committed back to the FP32 RAM authority.

A stale lease epoch, identity mismatch, or illegal transition fails closed.

## 27. Atlas lease identity separation

Even if both systems use numeric slot `1`, these are different authorities:

```text
Atlas/TensorCube compute slot 1
Local-Muon optimizer slot 1
```

No implicit equality or shared lease epoch is permitted.

## 28. Existing Adam M/V PCIe ring separation

The Pass144 Adam M/V transfer ring remains untouched by this R1 bake.

The Local-Muon ring is a separate type and state machine. Existing AdamW N8 execution therefore remains the current physical baseline.

## 29. Hybrid global optimizer clock

The intended promoted hybrid optimizer will share one global optimizer step:

```text
OPT N
├─ explicit Local-Muon tiles at N
└─ explicit AdamW residual domain at N
```

A split epoch such as Muon at `N` and AdamW at `N-1` is invalid.

Production hybrid commit is not yet admitted by this bake because no concrete eligibility registry has been supplied.

## 30. No silent optimizer substitution

A Muon tile that fails cannot silently become AdamW.

An unclassified region cannot silently become AdamW.

An unsupported Muon precision mode cannot silently become F32.

Receipt counters remain:

```text
silentOptimizerSubstitutionCount = 0
optimizerMathRouteChangeCount = 0
```

## 31. AdamW baseline remains authoritative

Pass145 does not alter the current AdamW N8 path.

This is intentional. A Local-Muon experiment requires an explicit registry before it may touch physical model state.

Therefore the existing:

- GEN5 parent;
- RAM-resident Adam M/V;
- Pass144 triple-buffered Adam transfer;
- N8 scheduler extension;
- Storage Root authority;
- R14 path

remain unchanged.

## 32. CPU reference surface

R1 includes a deterministic CPU Local-Muon reference using the same:

- momentum recurrence;
- optional Nesterov seed;
- local normalization;
- quintic NS recurrence;
- BF16-emulated projection identity;
- weight-decay/update formula.

It is intended as a parity oracle for later physical GPU adoption.

## 33. Deterministic CPU regression test

The library includes a fixed 16×16 deterministic test that runs the CPU reference twice and requires byte-identical F32 vectors for:

```text
candidate weight
candidate momentum
orthogonalized update
```

The test is compile/CF1-visible but does not substitute for a real GPU physical receipt.

## 34. Drift ledger schema

R1 defines Local-Muon drift evidence fields including:

```text
optimizerStep
tensorCubeId
gradientL2
momentumL2
orthogonalizedUpdateL2
weightUpdateL2
nonfiniteCount
```

Raw tensor payload logging remains zero.

## 35. Baseline comparison semantics

AdamW and Local Muon are different optimizers, so bit parity between their candidate weights is not a valid success condition.

The valid comparison surface is:

- same source weight authority;
- same gradient authority;
- same dataset/microbatch source;
- same optimizer-step boundary;
- deterministic Local-Muon rerun;
- measured update/loss/weight drift;
- measured optimizer-state and transfer footprint.

## 36. Current physical-claim boundary

Pass145 bakes a real WGSL candidate kernel but this environment has no Rust/Cargo/WGPU physical device execution authority.

Therefore none of the following are claimed yet:

```text
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_PHYSICAL_R1
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_ADAMW_HYBRID_R1
```

Those tokens are reserved for later physical gates.

## 37. Current structural PASS

Static/compile-admission token:

```text
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_OPTIMIZER_STRUCTURAL_R1
```

Its meaning is limited to:

- Local-Muon implementation present;
- exact 16×16 geometry present;
- explicit registry/profile authorities present;
- full-matrix/cross-cube/global claims closed;
- FP32 momentum authority present;
- Local-Muon GPU candidate ABI present;
- triple-buffer lease authority present;
- CPU reference/parity surface present;
- CF1 static validator wired.

## 38. Current HOLD

Until a concrete eligibility registry and profile are provided and physically executed:

```text
HOLD_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_ADAMW_BASELINE_COMPARISON_NOT_YET_ADMITTED
```

After comparison, production promotion remains separately held by:

```text
HOLD_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_PRODUCTION_PROMOTION_NOT_YET_ADMITTED
```

## 39. Static validator

Validator:

```text
tools/validate_tensorcube_local_muon_optimizer_static.py
```

It verifies the Local-Muon scope, exact geometry, route registry, FP32 momentum authority, BF16 working projection boundary, lease state machine, raw-gradient GPU binding, Newton-Schulz formula surfaces, CPU reference, drift ledger, crate exports, and CF1 registration.

## 40. CF1 binding

The Local-Muon static validator is part of the existing R6A-R2-R2 CF1 compile chain.

Any source change from this bake invalidates the previous CF1 source-tree digest and requires a fresh CF1 receipt before later BaseTrain physical execution.

## 41. Explicit non-goals

R1 does not silently add:

- full-matrix Muon;
- cross-cube orthogonalization;
- global Gram matrices;
- runtime shape-based eligibility;
- native BF16/TensorCore performance claims;
- production Local-Muon registry content;
- automatic Adam-M → Muon-momentum migration;
- durable hybrid checkpoint promotion;
- canonical-parent replacement;
- Local-Muon production promotion.

Those require explicit later authorities.

## SSOT seal

```text
MUON SCOPE              = explicit 16×16 TensorCube-local tiles only
ELIGIBILITY             = external explicit registry, never guessed
FULL-MATRIX MUON        = forbidden
CROSS-CUBE NS           = forbidden
GLOBAL ORTHOGONALITY    = not claimed

MUON MOMENTUM AUTHORITY = FP32
MUON TILE ADAM M/V      = no authority
BF16                     = NS working projection only
NATIVE BF16 CLAIM       = none

MUON TRANSFER RING      = three independent leases
ATLAS LEASE             ≠ Muon optimizer lease
ADAM PCIe LEASE         ≠ Muon optimizer lease

CURRENT N8 BASELINE     = existing AdamW path unchanged
PHYSICAL MUON PASS      = not yet claimed
HYBRID COMMIT PASS      = not yet claimed
NEXT INPUT REQUIRED     = explicit TensorCube eligibility registry + Local-Muon profile
```
