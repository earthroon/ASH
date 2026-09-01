# ASH-ADAMS-RIB-EVE-CANONICAL-ADAM-MATHEMATICAL-UPDATE-PRIMITIVE-AND-BACKEND-PARITY-MATERIALIZATION-R2

## `아담의_갈비뼈_이브` Canonical Adam/AdamW Mathematical Semantics / Exact Expression Topology / Hyperparameter ABI / CPU Oracle / WGPU Contract Binding / Legacy R6 Diagnostic Parity Harness / ActiveDevice Adoption / No Mutable Authority Migration

## 0. Revision identity

Revision:

`ASH-ADAMS-RIB-EVE-CANONICAL-ADAM-MATHEMATICAL-UPDATE-PRIMITIVE-AND-BACKEND-PARITY-MATERIALIZATION-R2`

Parent:

`ASH-ADAMS-RIB-EVE-COMMON-ADAM-STATE-GEOMETRY-SUCCESSOR-ABI-AND-PROJECTION-PRIMITIVE-MATERIALIZATION-R1`

Static/source PASS token:

`PASS_ASH_ADAMS_RIB_EVE_CANONICAL_ADAM_MATHEMATICAL_UPDATE_PRIMITIVE_BACKEND_PARITY_MATERIALIZATION_R2_STATIC`

Full release/physical PASS is not claimed by this source bake.

## 1. Purpose

R1 made `아담의_갈비뼈_이브` the dependency-neutral semantic authority for Adam range geometry, generation identity and projection classification. R2 adds the canonical Adam/AdamW mathematical contract without moving execution, mutable state, RAM authority, B06 ownership or durable commit into Eve.

This bake uses the current production shader `base_train_r6_adamw_candidate.wgsl` as the canonical expression-topology source.

## 2. Source truth after this bake

```text
Eve canonical Adam math expression                 true
Eve canonical BaseTrain beta/epsilon profile        true
Eve hyperparameter validation ABI                   true
Eve hyperparameter bit ABI                          true
Eve optimizer-step ABI                              true
Eve scalar CPU oracle                               true
Eve ULP/absolute-error parity comparator             true
Eve parity receipt ABI                              true
Legacy R6 WGPU Eve-math adoption                    true
ActiveDevice AdamW Eve-math adoption                true
Canonical R6 WGSL Eve R2 lineage marker             true
Legacy R6 bounded diagnostic parity harness         true
ActiveDevice dedicated diagnostic readback harness   false
Physical parity policy frozen                       false
Physical backend parity PASS                        false
Mutable Adam state moved into Eve                   false
Execution authority moved into Eve                  false
Durable authority moved into Eve                    false
Release compile                                     not claimed
RTX/WGPU physical qualification                      not claimed
```

## 3. New Eve R2 modules

New files:

```text
crates/아담의_갈비뼈_이브/src/hyperparameters_r2.rs
crates/아담의_갈비뼈_이브/src/math_r2.rs
crates/아담의_갈비뼈_이브/src/oracle_r2.rs
crates/아담의_갈비뼈_이브/src/parity_r2.rs
crates/아담의_갈비뼈_이브/src/math_receipt_r2.rs
```

The Eve dependency surface remains only `serde` and `sha2`.

## 4. Canonical production expression

The canonical semantic topology is:

```text
g = gradient, or +0.0 when the production gradient binding is absent

m = beta1 * m_prev + (1 - beta1) * g
v = beta2 * v_prev + (1 - beta2) * g * g

beta1_correction = 1 - pow(beta1, f32(optimizer_step))
beta2_correction = 1 - pow(beta2, f32(optimizer_step))

m_hat = m / beta1_correction
v_hat = v / beta2_correction

normalized = m_hat / (sqrt(v_hat) + epsilon)
decay = weight_decay * source_weight

candidate_weight = source_weight - learning_rate * (normalized + decay)
candidate_m = m
candidate_v = v
```

## 5. Exact topology authority

R2 canonizes the current expression order, not merely an algebraically equivalent textbook formula.

The following rewrites are not admitted by R2 without another revision:

```text
sqrt(v_hat + epsilon)
weight * (1 - lr * weight_decay) - lr * adam_term
candidate_m = m_hat
candidate_v = v_hat
step - 1 bias-correction exponent
```

The canonical expression identity is sealed by `ADAM_MATH_REVISION_R2` and `canonical_adam_math_expression_digest_r2()`.

## 6. BaseTrain canonical profile

Eve now owns the current common BaseTrain profile constants:

```text
beta1   = 0.9f32
beta2   = 0.999f32
epsilon = 1.0e-8f32
```

Learning rate and weight decay remain runtime configuration values.

Current production scheduler and atlas-runtime callsites import these constants from Eve instead of owning new duplicate constants.

## 7. Hyperparameter ABI

New:

`AdamHyperParametersR2`

Validation requires:

```text
learning_rate finite and > 0
0 < beta1 < 1
0 < beta2 < 1
epsilon finite and > 0
weight_decay finite and >= 0
```

New `AdamHyperParameterBitsR2` converts these values using exact `f32::to_bits()` so WGPU uniform bit identity is explicit.

## 8. Optimizer step ABI

New:

`AdamOptimizerStepR2`

Step zero is rejected. The step value is the exact exponent index consumed by the canonical bias-correction expression.

## 9. CPU oracle

New:

`adam_scalar_oracle_r2(...)`

and bounded qualification helper:

`adam_slice_oracle_r2(...)`.

The oracle follows the current WGSL operation topology, including `powf(step as f32)` and `sqrt`.

The CPU oracle is a qualification/reference surface only. It does not replace the production WGPU optimizer.

## 10. Finite semantics

The oracle rejects nonfinite source gradient/weight/M/V and reports a nonfinite successor verdict when the produced M, V or candidate weight is nonfinite.

R2 does not silently introduce numerical repair such as:

```text
max(v_hat, 0)
NaN -> 0
Inf saturation
epsilon inflation
```

for the current canonical R6 formula.

## 11. CPU/WGPU bit-exactness is not predeclared

The formula contains `pow` and `sqrt` across Rust and WGSL implementations. Therefore R2 does not fabricate universal CPU↔WGPU bit equality.

Exact requirements remain:

- hyperparameter bits;
- optimizer step;
- expression revision/digest;
- input geometry/cardinality;
- finite/nonfinite verdict policy.

Numerical output comparison uses an explicit parity policy.

## 12. Parity policy ABI

New:

`AdamBackendParityPolicyR2`

It carries independent Weight/M/V absolute and ULP limits, signed-zero policy and finite-verdict policy plus an explicit policy ID.

No default production tolerance is silently selected by Eve.

The policy validates finite nonnegative absolute-error bounds and requires a nonempty policy ID.

## 13. ULP and signed-zero observation

New:

`f32_ulp_distance_r2(...)`

tracks F32 ULP distance with sign-aware ordering.

`+0.0` and `-0.0` remain separately observable. Whether they must match exactly belongs to the supplied parity policy.

## 14. Parity evidence

New:

```text
AdamBackendParitySampleR2
AdamBackendParityReceiptR2
AdamMathProfileIdentityR2
```

Receipt fields preserve component-specific exact-match counts, max absolute errors, max ULP errors, finite-verdict mismatch count and signed-zero mismatch count.

## 15. Legacy R6 backend adoption

`base_train_r6_optimizer_continue.rs` now constructs:

```text
AdamOptimizerStepR2
AdamHyperParametersR2
AdamHyperParameterBitsR2
```

before encoding the existing WGPU uniform.

The backend no longer owns a competing semantic hyperparameter validation policy for this path.

Its WGPU `Params` layout remains local to the backend.

## 16. ActiveDevice backend adoption

`adamw_active_device_candidate_r1.rs` consumes the same Eve optimizer-step, hyperparameter validation and exact bit-packing authority before the real ActiveDevice submission.

The physical candidate buffers, SubmissionEpoch, source lease and pending ownership remain in the existing WGPU/P1 runtime.

## 17. Shared shader lineage

The canonical shader remains:

`crates/burn_webgpu_backend/src/shaders/base_train_r6_adamw_candidate.wgsl`

It is marked with:

`ASH.ADAMS.RIB.EVE.ADAM.MATH.R2`

R2 does not create a second Eve-specific production AdamW shader.

## 18. Legacy R6 diagnostic parity harness

New backend module:

`crates/burn_webgpu_backend/src/adamw_backend_parity_r2.rs`

New bounded diagnostic entrypoint:

`qualify_r6_adamw_candidate_against_eve_r2(...)`

It executes the existing R6 WGPU candidate path on a bounded fixture, evaluates the same host fixture through the Eve CPU oracle and produces an Eve parity receipt under a caller-supplied policy.

This diagnostic readback is qualification-only and does not change P1's ordinary candidate-D2H=0 production contract.

## 19. ActiveDevice physical parity boundary

ActiveDevice consumes the Eve R2 math contract in production source, but this bake does not add a dedicated candidate payload readback path to `PendingAdamWActiveDeviceCandidateR1`.

Therefore a separate physical ActiveDevice diagnostic campaign remains required before full R2 physical PASS.

No full candidate readback is added to ordinary ActiveVerified execution.

## 20. Zero-gradient semantics

The canonical R6 shader uses `+0.0` when the gradient binding is absent.

A zero-gradient step still updates M/V decay and applies AdamW weight decay; it is not an identity step.

The R6 diagnostic harness requires an absent-gradient fixture's host oracle input to contain exact positive-zero gradient values.

## 21. Triple-batch adoption

`r6_adamw_candidate_triple_batch(...)` now consumes the same Eve step/hyperparameter validation and bit-packing authority as the single R6 candidate path.

The existing batch execution topology is otherwise unchanged.

## 22. Historical R2E boundary

`base_train_r2e_adamw_step1_candidate.wgsl` is not promoted as the Eve R2 canonical expression.

That historical step-1 shader has distinct semantics including:

- genesis-zero moments;
- clip scale;
- denominator safety `max` operations;
- `sqrt(max(v_hat, 0))`.

R2 does not silently rewrite or collapse that historical math into the current R6/ActiveDevice formula.

The atlas runtime may reuse Eve's numerically identical BaseTrain beta/epsilon profile constants without implying R2E expression parity.

## 23. BaseTrain adoption receipt

New:

`crates/base_train/src/adams_rib_eve_canonical_adam_math_r2.rs`

It records the structural adoption truth and explicitly leaves:

```text
physical parity policy frozen = false
physical backend parity passed = false
```

## 24. Authority boundary

Eve R2 still contains no:

```text
WGPU Device / Queue / Buffer
SubmissionEpoch
ProductionMuonRuntime
HybridOptimizerCommitCoordinator
RAM Adam allocation
SequentialPackWriter
PackedRuntimeStateManifestV1
active_training_state.json
```

The mathematical SSOT moved. Mutable and durable ownership did not.

## 25. Static validator

New:

`tools/validate_ash_adams_rib_eve_canonical_adam_mathematical_update_primitive_backend_parity_materialization_r2_static.py`

It checks:

- R2 Eve modules and capabilities;
- dependency-neutral crate boundary;
- canonical profile constants;
- optimizer-step and bit ABI;
- exact CPU oracle expression topology;
- absence of silent numerical repair in the canonical oracle;
- ULP/parity vocabulary;
- canonical WGSL topology and revision marker;
- legacy R6 Eve adoption;
- ActiveDevice Eve adoption;
- legacy bounded diagnostic parity harness;
- production profile consolidation;
- R2 adoption receipt physical flags remain false;
- no state/execution/durable authority leakage into Eve.

## 26. Observed static regression state

This bake observed PASS for all nine source/static gates:

```text
Eve R1 common semantic materialization
Eve R2 canonical Adam math/parity materialization
P1 AdamW pending-generation scheduler
B06 multi-segment device generation ledger
FullModel AdamW segmented successor
02 bounded durable projection / host-scatter retirement
SubmissionEpoch active-async completion
P3 active transactional commit/restart
Unified Atlas MCU control plane
```

## 27. Compile boundary

A real Cargo compile remains mandatory because this revision changes:

- Eve public ABI;
- new Eve modules;
- BaseTrain imports;
- WGPU backend imports and validation flow;
- backend diagnostic parity module;
- BaseTrain R2 adoption module.

The assistant bake environment exposes no `cargo`, `rustc` or `rustfmt`.

Therefore release compile is not claimed.

## 28. Physical qualification boundary

Full physical R2 PASS requires at minimum:

```text
release compile PASS
frozen parity policy ID and limits
bounded R6 WGPU vs Eve oracle campaign PASS
ActiveDevice diagnostic parity campaign PASS
finite-verdict mismatch count = 0
zero-gradient equivalence PASS
single vs triple-batch equivalence PASS
segmentation invariance PASS
P1/B06/02 physical regressions remain valid
```

No such physical PASS is claimed by this source bake.

## 29. Packaging policy

The implementation ZIP excludes:

- this specification;
- all Markdown;
- `specs/`;
- bake manifests;
- generated manifests/receipts/evidence;
- runtime JSON/JSONL;
- qualification artifacts;
- runtime pack payloads;
- logs;
- `target/` and `target_*`;
- `.git/`;
- Python bytecode caches;
- backup files.

Implementation Rust/WGSL/Python source remains included.

## 30. GitHub publication policy

GitHub publication for this revision is specification-only. Implementation source remains in the delivered baked ZIP.

## 31. Exact next mainline boundary

After release and physical parity qualification, the mainline returns to:

`ASH-BASETRAIN-TRAINABLE-GENERATION-DURABILITY-DESCRIPTOR-AND-ACTIVE-TRAINING-STATE-HEAD-BINDING-R1`

R2 does not alter that durability roadmap.

## 32. Center sentence

**R1에서 이브가 Adam 상태의 뼈대를 가져왔다면 R2에서는 그 뼈가 움직이는 현재 production 수식의 의미를 가져온다. `m/v update → bias correction → sqrt(v_hat)+epsilon → source-weight decay → w-lr*(adam+decay)`의 연산 topology 자체가 canonical이고, legacy R6와 ActiveDevice는 동일한 Eve hyperparameter/step/bit authority를 소비한다. 다만 `pow`와 `sqrt`가 CPU와 WGSL 구현 경계를 건너므로 bit-exact를 지어내지 않는다. Eve는 oracle과 측정자를 제공하고 WGPU는 계속 실제 근육과 상태를 소유한다.**
