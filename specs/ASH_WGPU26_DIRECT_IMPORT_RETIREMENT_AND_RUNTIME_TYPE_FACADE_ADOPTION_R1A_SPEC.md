# ASH-WGPU26-DIRECT-IMPORT-RETIREMENT-AND-RUNTIME-TYPE-FACADE-ADOPTION-R1A

## Status

```text
Patch ID:
ASH-WGPU26-DIRECT-IMPORT-RETIREMENT-AND-RUNTIME-TYPE-FACADE-ADOPTION-R1A

STATIC MATERIALIZATION RELEASE

Static PASS:
PASS_ASH_WGPU26_DIRECT_IMPORT_RETIREMENT_AND_RUNTIME_TYPE_FACADE_ADOPTION_R1A_STATIC

Rust compile PASS: NOT CLAIMED
Cargo metadata PASS: NOT CLAIMED
GPU physical PASS: NOT CLAIMED

HOLD_ASH_WGPU26_R1A_PHYSICAL_PENDING
```

## Direct Parent

`ASH-WGPU26-WORKSPACE-SINGLE-GENERATION-DEPENDENCY-AND-TYPE-AUTHORITY-CUTOVER-R1`

R1 already establishes `ash-wgpu26-api` as the single ASH-owned requester of upstream `wgpu = 26.0.1`. R1A changes source-level type authority only and does not change WGPU generation.

## Runtime Type Facade

Materialized:

```text
crates/burn_webgpu_backend/src/runtime_wgpu_type_facade_r1a.rs
```

Authority:

```text
ash.runtime_wgpu_type_facade.wgpu26.r1a
```

The facade re-exports exact workspace primitive WGPU types from `ash_wgpu26_api`. It introduces no Device, Queue or Buffer wrappers and owns no runtime resources.

## Layering

```text
L0  ash-wgpu26-api
    workspace primitive package/type authority

L1  burn_webgpu_backend::runtime_wgpu_type_facade_r1a
    ASH runtime WGPU implementation namespace

L2  runtime_wgpu_type_authority + raw_bridge Backend*
    stable resource-handle ABI

L3  base_train / model_core / lora_train / orchestrator_local
    runtime consumers
```

Vendor raw access remains a low-level sibling and enters L0 through `burn-wgpu-local::gpu_api`.

## High-level Dependency Retirement

The following crates no longer have direct `ash-wgpu26-api` or transitional `wgpu26` Cargo dependencies:

```text
base_train
model_core
lora_train
orchestrator_local
```

Only these low-level implementation boundaries retain direct `ash-wgpu26-api` dependencies:

```text
burn_webgpu_backend
vendor_fork_scaffold/burn-wgpu-local
```

Both use canonical dependency key `ash_wgpu26_api`; the transitional Cargo key `wgpu26` is retired.

## Direct Source Import Retirement

Active Rust source now has zero direct `wgpu26` imports/qualified paths in:

```text
base_train
model_core
lora_train
orchestrator_local
burn_webgpu_backend
burn-wgpu-local
```

Historical diagnostic strings and authority IDs containing the text `wgpu26` remain historical evidence and are not active imports.

Backend implementation code uses `crate::runtime_wgpu_type_facade_r1a as wgpu`. High-level implementation-local descriptor/enum code uses `burn_webgpu_backend::runtime_wgpu_type_facade_r1a`. No WGPU descriptor values, feature selection, dispatch geometry or queue ordering are changed.

## Stable Resource Handles

Historical aliases remain and are now sourced through the R1A facade. R1A also materializes stable handle aliases for current cross-boundary objects including BindGroup, BindGroupLayout, CommandBuffer, PipelineLayout, QuerySet, ShaderModule, Texture and TextureView.

Existing canonical aliases remain:

```text
BackendDevice = RuntimeWgpuDevice
BackendQueue  = RuntimeWgpuQueue
BackendBuffer = RuntimeWgpuBuffer
```

Known model-core public GPU Buffer holders are migrated to `BackendBuffer`; the nominal underlying type remains upstream WGPU 26.0.1 Buffer.

## Vendor Boundary

`burn-wgpu-local/src/gpu_api.rs` now re-exports `ash_wgpu26_api`. Vendor implementation modules continue to consume primitives through `crate::gpu_api` rather than importing the workspace primitive crate directly.

R1A does not merge vendor and upstream `WgpuStorage/WgpuResource` ABIs. Canonical resource/storage unification remains R2 scope.

## Runtime Authority and Type Equality

Historical runtime authority remains:

```text
ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1
```

R1A materializes `RuntimeWgpuFacadeBindingR1A` and updates the R1 compile-time equality witness to the canonical workspace crate name.

Conversion-free witnesses cover workspace/runtime/facade Device, Queue and Buffer identities plus Burn WgpuSetup, Burn WgpuResource and vendor WgpuResource Buffer types. The witness contains no unsafe generation bridge, transmute or from_raw conversion.

Actual compile equality PASS remains unclaimed because the bake environment has no Rust compiler.

## Cargo.lock

R1A retains:

```text
ash-wgpu26-api -> wgpu 26.0.1
burn_webgpu_backend -> ash-wgpu26-api
burn-wgpu-local -> ash-wgpu26-api
```

and removes direct authority edges from base_train, model_core, lora_train and orchestrator_local.

Resolved suite remains:

```text
wgpu       26.0.1
wgpu-core  26.0.1
wgpu-hal   26.0.6
wgpu-types 26.0.0
naga       26.0.0
```

There is still exactly one resolved upstream WGPU package.

## R1 Parent Successor Mode

The R1 validator is updated monotonically. It accepts historical R1 compatibility mode or the stricter R1A successor graph while preserving R1's sole upstream owner, single resolved WGPU package and exact 26.0.1 checks.

Current R1 result remains:

```text
84 / 84 PASS
```

## R1A Static Validation

Validator:

```text
tools/validate_ash_wgpu26_direct_import_retirement_runtime_type_facade_adoption_r1a_static.py
```

Current result:

```text
107 / 107 PASS
PASS_ASH_WGPU26_DIRECT_IMPORT_RETIREMENT_AND_RUNTIME_TYPE_FACADE_ADOPTION_R1A_STATIC
```

## Parent Regression

```text
HiMuon R8A                 115 / 115 PASS
HiMuon R8                    90 / 90 PASS
packed-gradient R7A1         82 / 82 PASS
MCU R7B                      78 / 78 PASS
MCU R7A                      73 / 73 PASS
Trainable Session R4A        65 / 65 PASS
Trainable Session R4         64 / 64 PASS
Eve R3G                      35 / 35 PASS
R3C                          18 / 18 PASS
R3C1                         30 / 30 PASS
R3D                          41 / 41 PASS
R3E                          52 / 52 PASS
R3F                          66 / 66 PASS
Unified Atlas MCU R6         PASS
Mixed-precision MCU R7       PASS
SubmissionEpoch async        PASS
Resident Weight              PASS
```

Historical unchanged baselines reproduce on the direct R1 parent:

```text
RAM exact inventory          66 / 67
N8 RAM resume-cut           117 / 118
```

## Compile Boundary

The bake environment exposes no `cargo`, `rustc` or `rustfmt`. Therefore Cargo metadata/check, Rust compile and compiler type-equality PASS are not claimed.

Modified Cargo manifests and Cargo.lock parse as TOML. R1/R1A validators pass Python py_compile. Critical authority/audit Rust files pass UTF-8/NUL and structural delimiter checks.

## Physical Qualification

Physical promotion requires workspace and vendor-feature compilation, compiler acceptance of the R1/R1A equality witnesses, existing Device/Queue bootstrap, Burn/vendor raw resource borrow and representative BaseTrain/ModelCore/LoRA/orchestrator GPU execution while proving no new Device/Queue, no resource copy introduced by the facade and no numerical/dispatch change.

Until then:

```text
HOLD_ASH_WGPU26_R1A_PHYSICAL_PENDING
```

## Explicit Non-claims

R1A does not claim vendor WgpuStorage canonicalization, Burn WgpuResource ABI replacement, CubeCL fork activation, device feature/limit capability sealing, a WGPU upgrade beyond 26.0.1, multi-device completion or tensor parallelism.

## Direct Successor

```text
ASH-BURN-CUBECL-WGPU26-VENDOR-FORK-CANONICAL-STORAGE-AND-RESOURCE-ABI-R2
```

R1 fixed package authority and R1A fixes source type authority. R2 can therefore focus only on the remaining duplicate storage/resource ABI.

## Final Law

> R1 made WGPU 26 one workspace dependency decision.

> R1A makes it one ASH runtime source-level type authority.

> High-level ASH code no longer depends directly on the workspace primitive WGPU package; backend and vendor code enter the same nominal WGPU 26 types through explicit low-level authority seams.
