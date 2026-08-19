# ASH-WGSL-WGPU26-PARSER-COMPATIBILITY-GLOBAL-SEAL-R1

## 1. Patch identity

```text
ASH-WGSL-WGPU26-PARSER-COMPATIBILITY-GLOBAL-SEAL-R1

Canonical F32 Exponent-Mask Finite Predicate /
22 Unsupported Finite Callsite Removal /

Invalid Static Validator Contract Repair /
Static PASS = WGPU26-Compatible WGSL /

Naga26 Function Pointer-Space Closure /
Storage·Workgroup Pointer Argument Elimination /

Exact-Subgroup32 Election Compatibility /
18 subgroupElect Callsite Closure /

Dormant enable-subgroups Quarantine /
F16 Enable Preservation /

W6 Stale Builtin-Debt Ledger Retirement /

Standalone WGSL Corpus Scan /
Embedded Rust WGSL Scan /
Exact Naga26 Physical Parse Gate /
Corpus Failure Aggregation
```

## 2. Parent failure and purpose

The parent physical failure is a `wgpu 26.0.1` shader-module creation failure in
`ash_burn_vendor_variable_row_online_softmax.shader`, caused by WGSL source using
unsupported pseudo-builtins such as `isNan` and `isInf`.

After the first parser debt was closed, the exact Naga26 validator exposed an
additional pre-existing compatibility debt: user functions accepted pointer
arguments in address spaces that Naga26 does not admit for function parameters.
This R1 therefore closes both syntax and validator-level WGSL incompatibilities.

This R1 is not a one-file hotfix. It makes the production WGSL corpus, its static
validators, and the physical compiler gate agree on one compatibility authority.

Runtime compatibility authority is:

```text
wgpu 26.0.1
  -> Naga 26.0.0 WGSL parser and validator
  -> ASH production WGSL
  -> ASH static validators
```

Static validators may describe and enforce the source contract, but they must not
require syntax or pointer-space structures that the production parser/validator
rejects.

## 3. Non-goals

This patch does not change:

- TensorCube mathematics or geometry
- attention, softmax, RMSNorm, Muon, AdamW, or Delta-K formulas
- mask or causal semantics
- mixed-precision packing or FP32 accumulation semantics
- optimizer routing
- Atlas authority
- checkpoint authority
- workgroup topology
- exact-subgroup32 admission policy
- CPU fallback policy

The patch is a WGSL parser/runtime compatibility closure.

## 4. Canonical finite predicate

Production WGSL must not contain calls to:

```text
isFinite(
isNan(
isNaN(
isInf(
```

F32 finite classification uses exponent bits:

```wgsl
const F32_EXPONENT_MASK: u32 = 0x7f800000u;

fn finite_f32(value: f32) -> bool {
    return (bitcast<u32>(value) & F32_EXPONENT_MASK) != F32_EXPONENT_MASK;
}
```

The helper performs classification only. It must not clamp, repair, normalize, or
otherwise mutate the checked value.

The source audit baseline for this R1 is 22 unsupported finite pseudo-builtin call
occurrences:

```text
isFinite: 18
isNan:     2
isInf:     2
Total:    22
```

The affected production shader classes include:

- `vendor_fork_scaffold/burn-wgpu-local/src/shaders/variable_row_online_softmax.wgsl`
- `vendor_fork_scaffold/burn-wgpu-local/src/shaders/mixed_precision_tensor_primitives.wgsl`
- `crates/burn_webgpu_backend/src/shaders/base_train_qk_rmsnorm_attention_stability.wgsl`
- `crates/burn_webgpu_backend/src/shaders/base_train_bp_delta_k_local_observe_16x16.wgsl`
- `crates/burn_webgpu_backend/src/shaders/base_train_bp_delta_k_bridge_pair_cosine_16x16.wgsl`

All 22 occurrences must be removed before promotion.

## 5. Static validator contract repair

A static validator must never pass a shader because an unsupported spelling is
present. Checks such as the following are invalid authority:

```python
"isNan(value) || isInf(value)" in shader
"isFinite(mean_square)" in shader
"!isFinite(g)" in shader
```

The repaired validator contract requires:

1. the canonical exponent-mask finite predicate where finite classification is needed,
2. zero unsupported finite pseudo-builtin calls,
3. preservation of the original non-finite rejection or telemetry semantics,
4. preservation of source-path and route identity checks.

Known validators that must be repaired together with their shaders include:

- `tools/validate_ash_burn_vendor_mixed_precision_tensor_primitives_r1_static.py`
- `tools/validate_qk_rmsnorm_attention_stability_static.py`
- `tools/validate_ash_bp_dk_local_tensorcube_bp_dk_observation_01_static.py`

Parent source SHA seals that intentionally cover modified shader sources must be
updated atomically. An old parent SHA must not be retained merely to preserve a
historical validator count.

## 5A. Naga26 function argument pointer-space closure

Naga26 rejects user-function pointer arguments outside the function/private pointer
spaces. In particular, passing module-scope `storage` data or `workgroup` arrays by
pointer into a user helper produces `InvalidArgumentPointerSpace` during Naga
validation.

R1 therefore forbids production WGSL helper signatures such as:

```wgsl
fn helper(data: ptr<storage, array<f32>, read>, index: u32) -> f32 { ... }
fn helper(tile: ptr<workgroup, array<vec4<f32>, 16>>, index: u32) -> f32 { ... }
```

The repair must preserve state ownership. Preferred transformations are:

1. keep module-scope storage/workgroup objects as the SSOT,
2. specialize a helper per owned buffer/tile and read the module-scope object directly,
3. or pass constructible scalar/vector/index values by value,
4. do not copy the whole storage/workgroup object into function-local state merely to satisfy the validator.

The affected source baseline discovered by the exact Naga26 gate is:

- `crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_headwise_prefill.wgsl`
- `crates/burn_webgpu_backend/src/shaders/qwave_gradient.wgsl`
- `crates/burn_webgpu_backend/src/shaders/qwave_tensor.wgsl`
- `crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_microtile_8x8_workgroup_ref.wgsl`

The intended repairs are ownership-preserving specializations:

- AW02 projection helpers read `qw`, `kw`, and `vw` directly,
- Q-wave gradient helpers read `delta_k` directly,
- Q-wave tensor helpers read `grad_t` and `grad_f` directly,
- TensorCube microtile accessors read `tile_a` and `tile_b` directly.

No attention/Q-wave/TensorCube formula, binding index, workgroup topology, or dispatch
shape is changed by this closure.

Promotion requires:

```text
disallowed function pointer argument count = 0
```

The global static validator must include negative fixtures for at least storage and
workgroup pointer arguments so this validator-level incompatibility cannot silently
re-enter the tree.

## 6. Exact-subgroup32 election compatibility

The source audit baseline contains 18 `subgroupElect()` calls across four
runtime-referenced exact-subgroup paths.

R1 removes all 18 calls.

The permitted replacement is an explicit lane-zero owner only where the existing
route proves exact subgroup32 admission and the branch is subgroup-uniform:

```wgsl
let exact_subgroup32_leader = subgroup_lane == 0u;
```

This is not a generic emulation of subgroup election. It is an exact-subgroup32
leader contract.

Before applying lane-zero ownership, the callsite must satisfy all of the following:

- `@builtin(subgroup_invocation_id)` is present,
- the Rust-side route requires subgroup capability,
- exact subgroup size 32 is part of route admission,
- lane 0 participates in the operation domain,
- the guarded branch is subgroup-uniform,
- the intended writer cardinality is preserved.

For one-writer-per-workgroup logic, `subgroup_lane == 0u` alone is insufficient when
a workgroup may contain multiple subgroups. Such a path also needs an explicit
workgroup-level owner condition, for example `subgroup_id == 0u`, when that matches
the original contract.

Mandatory reviewed shader classes include:

- `tensorcube_fused_attention_r2_wg32_subgroup.wgsl`
- `tensorcube_fused_attention_r3_wg32_subgroup_packed_half.wgsl`
- `base_train_tensorcube_local_muon_16x16_exact_subgroup32_norm.wgsl`
- `base_train_tensorcube_fused_pair_muon_16x32_exact_subgroup32_norm.wgsl`

Promotion requires:

```text
production subgroupElect callsites = 0
```

## 7. Dormant `enable subgroups` quarantine and F16 preservation

`enable subgroups` is not accepted as production WGSL authority for the current
wgpu26/Naga26 line.

A source such as:

```wgsl
enable f16, subgroups;
```

must not be promoted unchanged. When the shader still requires f16, the f16 enable
is retained:

```wgsl
enable f16;
```

Removing unsupported subgroup syntax must not silently change f16 storage or
arithmetic to f32.

A dormant shader that cannot yet satisfy the production parser is classified as
quarantined and must have no production module-construction authority until repaired.

## 8. W6 stale builtin-debt ledger retirement

Historical unsupported-builtin counts are evidence, not current source truth.

W6 must not require a frozen historical condition such as:

```text
latent unsupported builtin count == 18
```

The current compatibility truth is:

```text
unsupported finite pseudo-builtin callsite count == 0
```

Historical counts may remain in documentation, but they cannot gate a repaired
source tree.

## 9. Standalone WGSL corpus scan

A repository-wide compatibility validator must recursively inspect standalone
`*.wgsl` files and detect at least:

```text
isFinite(
isNan(
isNaN(
isInf(
subgroupElect(
enable subgroups
function argument ptr<storage, ...>
function argument ptr<workgroup, ...>
```

The pointer-space scan must also reject any other user-function pointer argument
space that Naga26 does not admit for this profile.

It must also validate f16 enable coverage for WGSL source that uses the f16 type.

The scanner must not confuse Markdown/spec text with production WGSL source.

Required structural PASS token:

```text
PASS_ASH_WGSL_WGPU26_GLOBAL_COMPATIBILITY_STRUCTURAL_R1
```

## 10. Embedded Rust WGSL scan

Rust source may contain WGSL in raw string literals or shader-source constructors.
The compatibility scan therefore covers both standalone WGSL files and embedded
Rust WGSL blocks.

The embedded scan applies the same forbidden-token contract:

```text
unsupported finite pseudo-builtin = 0
subgroupElect = 0
unsupported subgroup enable = 0
disallowed function pointer argument = 0
```

An embedded block identified as WGSL must not be omitted merely because it has no
separate `.wgsl` file.

## 11. Exact Naga26 parse and validation gate

Static grep is not physical parser evidence.

The R1 parse gate uses the exact production compiler line:

```text
wgpu 26.0.1
Naga 26.0.0
```

Every discovered standalone and embedded WGSL module is processed through:

```rust
let module = naga::front::wgsl::parse_str(source)?;

naga::valid::Validator::new(
    naga::valid::ValidationFlags::all(),
    naga::valid::Capabilities::all(),
)
.validate(&module)?;
```

Parse and semantic validation are separate gates. A source that parses but fails
Naga validation is not compatible.

The corpus gate must not stop after the first invalid shader. It must visit the full
discovered corpus, collect every parse/validation failure, print the complete failure
set, and then return one non-zero result. This prevents compatibility debt from being
revealed one shader at a time across repeated user runs.

Required token:

```text
PASS_ASH_WGSL_WGPU26_EXACT_NAGA26_PARSE_R1
```

## 12. Physical wgpu shader-module gate

Where a physical adapter is available, the same compatibility binary must support a
physical mode that requests the existing subgroup capability and calls
`Device::create_shader_module` for the mandatory production matrix.

The minimum physical matrix covers:

1. vendor variable-row online softmax,
2. vendor mixed-precision tensor primitives,
3. QK RMSNorm attention stability,
4. BP Delta-K local observer,
5. BP Delta-K bridge cosine observer,
6. TensorCube fused attention R2 subgroup path,
7. TensorCube fused attention R3 subgroup path,
8. TensorCube local Muon exact-subgroup32 path,
9. TensorCube fused-pair Muon exact-subgroup32 path.

Required token:

```text
PASS_ASH_WGSL_WGPU26_SHADER_MODULE_CREATION_PHYSICAL_R1
```

The original variable-row online-softmax shader-module failure must be included in
this regression matrix.

## 13. Exact-subgroup32 semantic gate

Removing `subgroupElect()` is not sufficient by itself. The physical regression path
must preserve:

- one-owner or one-owner-per-subgroup cardinality as originally intended,
- reduction output,
- candidate state writes,
- atomic/status write count,
- attention and Muon result parity for the covered route.

Required token:

```text
PASS_ASH_WGSL_WGPU26_EXACT_SUBGROUP32_ELECTION_COMPATIBILITY_R1
```

If physical writer-cardinality evidence is not yet available, this token remains
HOLD even when static source replacement is complete.

## 14. Validation order

Recommended order:

```text
WGSL global structural compatibility scan
-> repaired subsystem static validators
-> cargo check/build
-> exact Naga26 standalone + embedded parse/validate
-> physical wgpu shader-module construction matrix
-> existing subsystem GPU regression harnesses
```

A static PASS must not be promoted into a physical PASS claim.

## 15. Failure policy

The compatibility seal is HOLD if any mandatory production source has:

- unsupported finite pseudo-builtins,
- `subgroupElect()`,
- unsupported subgroup enable syntax,
- disallowed function argument pointer space,
- required f16 without `enable f16`,
- a Naga parse failure,
- a Naga validation failure,
- a physical shader-module construction failure,
- unverified subgroup writer cardinality,
- a stale validator that requires invalid WGSL,
- a W6 debt gate that requires historical unsupported callsites.

Production parser/validator failure is fail-closed. This patch must not hide failure
by silently selecting generic attention, CPU, or other fallback routes.

## 16. Packaging contract

The baked code package is source-oriented.

Generated artifact directories, generated patch manifests, and SHA sidecars are not
required for the distributed code ZIP and should be excluded. Source-critical files
such as `Cargo.toml`, Rust source, WGSL source, static validators, and runtime scripts
remain included.

The compatibility binaries print their PASS/HOLD state directly; a generated
artifact or manifest file is not itself promotion authority.

## 17. Promotion conditions

The global seal may be promoted only when all applicable mandatory gates are true:

```text
unsupported finite callsites = 0
subgroupElect callsites = 0
production unsupported subgroup-enable count = 0
disallowed function pointer argument count = 0
missing f16-enable count = 0
stale validator contract count = 0
stale W6 builtin-debt contract count = 0
Naga parse failures = 0
Naga validation failures = 0
physical shader-module creation failures = 0
exact-subgroup32 writer-cardinality contract = verified
```

Required global promotion token:

```text
PROMOTE_ASH_WGSL_WGPU26_PARSER_COMPATIBILITY_GLOBAL_SEAL_R1
```

## 18. Central authority declaration

WGSL correctness is not defined by a static validator finding the string it expected.
For this R1, correctness means that the source obeys the ASH semantic contract,
passes the exact wgpu26/Naga26 parser and validator, and preserves the required
runtime writer/state semantics on the physical route.

This R1 therefore closes the gap between "STATIC PASS" and "the production WGSL is
actually acceptable to the compiler that ASH is running."
