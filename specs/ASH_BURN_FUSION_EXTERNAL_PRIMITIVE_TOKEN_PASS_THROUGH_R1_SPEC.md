# ASH-BURN-FUSION-EXTERNAL-PRIMITIVE-TOKEN-PASS-THROUGH-R1

## ACTUAL PRIMITIVE GLOBAL-REGISTRY RETIREMENT + SOFT-MATRIX TOKEN RESOLUTION + SEND/SYNC GRAPH CUT

### 0. Revision

```text
Patch ID: ASH-BURN-FUSION-EXTERNAL-PRIMITIVE-TOKEN-PASS-THROUGH-R1
Class: LOCAL BURN-FUSION OWNERSHIP SURGERY / RELEASE-COMPILE GRAPH CUT
Direct parent: ASH_PASS3_MCU_SOFT_TENSOR_MATRIX_R1A_BINDING_FIELD_COMPILEFIX_CODE_ONLY.zip
Parent SHA-256: 63666a9abcf4a2959edbc999971e3315d7ac63def9cdf852a91b797f53854947
Source release: STATIC SOURCE MATERIALIZATION / UNCOMPILED IN BAKE ENVIRONMENT
Physical qualification: HOLD
```

Observed boundary before this revision:

```text
cargo check -p burn_webgpu_backend --lib   PASS
cargo check -p base_train --lib            PASS
cargo test -p burn_webgpu_backend --lib    PASS (user-reported)
cargo test -p base_train --lib             PASS (user-reported)
release PHYS campaign binary               E0275 NumericDimension: Sync
```

Reserved tokens:

```text
PASS_ASH_BURN_FUSION_EXTERNAL_PRIMITIVE_TOKEN_R1_STATIC
PASS_ASH_BURN_FUSION_EXTERNAL_PRIMITIVE_TOKEN_R1_RELEASE_COMPILE
PASS_ASH_BURN_FUSION_EXTERNAL_PRIMITIVE_TOKEN_R1_NATIVE
HOLD_ASH_BURN_FUSION_EXTERNAL_PRIMITIVE_TOKEN_R1_WGPU_PENDING
```

### 1. Goal

Retire actual backend primitives from `burn-fusion-local`'s process-global resolved-primitive registry.

Previous shape:

```text
DashMap<Key, Entry>
Entry.primitive = Arc<dyn Any + Send + Sync>
P: Clone + Send + Sync + 'static
```

New shape:

```text
DashMap<Key, lightweight Entry>
Entry = reason + lifecycle state + generation + logical storage identity

ExternalPrimitiveTokenR1
    -> current Fusion runtime
    -> actual primitive resolve
```

The global registry no longer transitively owns WGPU primitives and does not impose a local `P: Send + Sync` bound on external primitive registration/resolution helpers.

### 2. Token ABI

Materialized:

```rust
ExternalPrimitiveTokenR1 {
    key,
    generation,
    storage_identity_digest,
    state,
    token_digest,
}
```

The token owns metadata only. It never owns or serializes `CubeTensor`, WGPU Device/Queue/Buffer/Pipeline/BindGroup, or arbitrary backend primitive payload.

Token generation advances on re-registration of the same full key. Generation overflow is explicit:

```text
E_BURN_FUSION_EXTERNAL_PRIMITIVE_TOKEN_GENERATION_OVERFLOW
```

### 3. Registry lifecycle preservation

Existing lifecycle vocabulary remains:

```text
BorrowedReadOnly
DetachedOwned
Tombstoned
```

Alias lookup, tombstone, fork snapshot and fork merge remain metadata operations. Fork merge no longer copies an actual primitive payload; detached-owned promotion updates token state/generation/storage metadata only.

### 4. Registration compatibility surface

The public generic registration function names are retained for source compatibility:

```text
register_external_resolved_float_primitive_for_fusion_tensor
register_detached_owned_float_primitive_for_fusion_tensor
register_external_resolved_float_primitive_for_fusion_tensor_with_state
```

However the supplied `P` is no longer stored globally. It is consumed/dropped after token registration.

**Semantic change F1:** registration now records logical external-resolution authority, not ownership of the supplied primitive object.

### 5. Runtime-local actual primitive resolution

`raw_access.rs` now resolves in two stages:

```text
external token lookup
    -> FusionTensor.client.resolve_tensor_float::<NativeWgpuRawBackend>()
    -> actual CubeTensor
```

This reuses the already-existing runtime-local Fusion resolution path from `live_raw_access.rs`.

`PrimitiveHandleMapAssumption` is retained as compatibility naming, but its route now identifies:

```text
external_primitive_token_runtime_resolve
burn_fusion_local.external_primitive_token_r1
```

### 6. Fixture registration boundary

`register_native_wgpu_fixture_primitive_for_fusion_tensor` remains callable so existing fixture builders do not need a broad API rewrite.

The supplied raw primitive is now a registration witness only and is not retained in a global Any registry. Subsequent raw resolution resolves the current Fusion tensor through its runtime client after token admission.

**Semantic change F2:** fixture registration no longer establishes a process-global raw-mirror primitive owner.

### 7. External alias barrier

The local helper bounds are reduced from:

```text
P: Clone + Send + Sync + 'static
```

to:

```text
P: Clone + 'static
```

Read-only token hits no longer return an actual `BorrowedPrimitive(P)` from the global registry. They return an explicit runtime-resolution route:

```text
burn_fusion_local.barrier.read_only.token_runtime_resolve
```

and the caller continues through its runtime-owned path.

Scaffold truth is updated:

```text
read_only_borrowed_resolution = false
read_only_token_runtime_resolution = true
```

### 8. Runtime splice

Promotion still returns the promoted primitive directly to the current caller.

Global post-promotion registration is token-only:

```text
detached_owned_registry_registration = false
detached_owned_token_registration = true
```

Future resolution of that logical identity must go through the current runtime rather than retrieving a stored primitive object from the global registry.

**Semantic change F3:** detached-owned global primitive persistence is retired; token persistence remains.

### 9. Legacy direct primitive resolver

The old public `try_resolve_external_float_primitive_*<P>` symbols remain as compatibility surfaces, but do not return an actual primitive from the token registry. They return `None` after a token hit, forcing existing caller fallback to the runtime-owned resolution path.

New authoritative lookup APIs:

```text
try_resolve_external_primitive_token_for_fusion_tensor
try_resolve_external_primitive_token_for_tensor_ir
```

### 10. Telemetry

The existing `read_only_borrowed` counter remains for historical compatibility.

New local telemetry distinguishes:

```text
read_only_token_runtime_resolve
```

`generic_any_downcast_count` and `generic_any_downcast_failure_count` remain in the public snapshot ABI but are not used by the token path; no Any downcast is performed.

Higher-level telemetry that does not yet project the new token counter is not claimed to provide complete R1 token-path attribution.

### 11. Send/Sync graph law

After R1, the active local Fusion extension source must contain no:

```text
Arc<dyn Any + Send + Sync>
P: Clone + Send + Sync + 'static
```

for external primitive registry helpers.

No workaround is permitted through:

```text
recursion_limit
unsafe impl Send
unsafe impl Sync
raw pointer / usize primitive owner
thread-local actual primitive registry
```

### 12. Non-goals

No change to:

```text
Adam mathematics
HiMuon mathematics
MCU / Soft Tensor Matrix ownership
A01 / A02 / A03 device subgroup
WGPU tensor representation
Burn core scheduling
R3C / R3C1 commit
```

This revision does not claim that upstream Burn's own generic backend contracts never require Send/Sync. It removes the additional local external-primitive registry requirement. If the release binary still produces the same E0275 after this cut, the next outer generic boundary must be identified from the new compiler output rather than hidden with trait workarounds.

### 13. Static acceptance

Required source facts:

```text
global actual primitive Any registry = 0
local generic external primitive Send+Sync bounds = 0
ExternalPrimitiveTokenR1 present
token registration present
token fusion lookup present
token TensorIr lookup present
raw access token lookup present
raw access runtime-local Fusion client resolve present
read-only token runtime route present
detached-owned token registration present
fork merge actual primitive copy = 0
unsafe Send/Sync workaround = 0
recursion_limit workaround = 0
```

### 14. Compile acceptance

Run in order:

```powershell
cargo check -p burn_webgpu_backend --lib
cargo check -p base_train --lib
cargo build -p base_train --lib --release -j 1
cargo build -p base_train --bin ash_basetrain_eve_mcu_close_phys_r1 --release -j 1
```

Direct success condition:

```text
validation::NumericDimension: Sync E0275 = absent
```

No recursion-limit increase is accepted as PASS evidence.

### 15. Native acceptance

```powershell
cargo test -p burn_webgpu_backend --lib -j 1 --no-fail-fast
cargo test -p base_train --lib -j 1 --no-fail-fast
```

Four token helper tests are materialized in `resolved_primitive_override.rs` but were NOT RUN in the bake environment.

### 16. WGPU next step

After release compile/native PASS, return directly to the existing PHYS campaign. No new training executor is added.

```text
SUCCESS_ABC
8
4+4
2+2+4
```

### 17. Actual source bake

```text
ADD 0
MOD 5
DEL 0
```

Modified files:

```text
vendor_fork_scaffold/burn-fusion-local/src/resolved_primitive_override.rs
vendor_fork_scaffold/burn-fusion-local/src/external_alias_barrier.rs
vendor_fork_scaffold/burn-fusion-local/src/runtime_splice.rs
vendor_fork_scaffold/burn-fusion-local/src/raw_access.rs
vendor_fork_scaffold/burn-fusion-local/src/lib.rs
```

No MCU, Soft Matrix, backend kernel, Cargo or WGSL file is changed by this revision.

### 18. Static validation actually executed

```text
R1 token source-contract focused checks: PASS
  Any+Send+Sync registry removed
  local P Send+Sync bounds removed
  token ABI / registration / lookup present
  runtime-local client resolver present
  unsafe Send/Sync absent
  recursion-limit workaround absent
  explicit token generation overflow guard present

Existing vendor/storage static regression:
117 / 117 PASS
```

Bake environment has no Cargo/Rustc. Compile, link, native execution and WGPU are NOT RUN / 판단불가.

### 19. Artifacts

Full code-only bake:

```text
ASH_PASS3_BURN_FUSION_EXTERNAL_PRIMITIVE_TOKEN_PASS_THROUGH_R1_CODE_ONLY.zip
SHA-256: 48e75a915417166b669533142ebbe0ac775868d18f10cd680baea0242c7de0f1
Bytes: 21,471,712
Files: 8,414
CRC: PASS
Duplicate paths: 0
```

Overlay from direct parent:

```text
ASH_BURN_FUSION_EXTERNAL_PRIMITIVE_TOKEN_PASS_THROUGH_R1_OVERLAY.zip
SHA-256: 57452e10f3935c1fc2a210bb7d53134852c1ef89c029f8f5d08f8c9b299ed1fe
Bytes: 12,318
Files: 5
CRC: PASS
Duplicate paths: 0
```

Code ZIPs contain no generated spec/artifact/manifest/report directory and no PowerShell file.

### 20. Final law

> Fusion global registry owns token metadata, never an actual WGPU primitive.
>
> The actual primitive resolves through the current Fusion runtime at the point of use.
>
> Token Send/Sync requirements must not be promoted into actual WGPU primitive Send/Sync requirements by the local extension.
>
> No recursion-limit, unsafe Send/Sync, raw pointer or thread-local actual primitive store is accepted as the fix.
