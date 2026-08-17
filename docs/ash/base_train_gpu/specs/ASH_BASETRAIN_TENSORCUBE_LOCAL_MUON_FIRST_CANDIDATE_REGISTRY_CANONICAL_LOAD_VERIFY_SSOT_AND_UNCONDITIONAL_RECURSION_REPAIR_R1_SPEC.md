# ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-FIRST-CANDIDATE-REGISTRY-CANONICAL-LOAD-VERIFY-SSOT-AND-UNCONDITIONAL-RECURSION-REPAIR-R1

## Status

```text
Patch ID:
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-FIRST-CANDIDATE-REGISTRY-CANONICAL-LOAD-VERIFY-SSOT-AND-UNCONDITIONAL-RECURSION-REPAIR-R1

Parent code SSOT:
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-EXACT-SUBGROUP32-QK-REDUCTION-AND-STATE-BROADCAST-R3A full body

Repair scope:
Muon production FirstCandidate registry load / verify authority

Production self-recursion:
retired

Canonical registry load authority:
FirstCandidateEligibilityRegistry::load_verified

Registry semantic validation authority:
FirstCandidateEligibilityRegistry::validate(spec)
```

## Failure being repaired

The parent source contained:

```rust
impl ProductionMuonRuntime {
    pub fn load_registry_verified(
        spec: &ModelSpec,
        registry_path: &Path,
    ) -> Result<FirstCandidateEligibilityRegistry> {
        let registry = Self::load_registry_verified(spec, registry_path)?;
        // ...
        Ok(registry)
    }
}
```

There is no overload that resolves this call elsewhere. The method therefore unconditionally calls itself.

The active scheduler reaches the method through:

```text
admit_tensorcube_local_muon_production_callsite
    -> ProductionMuonRuntime::required_momentum_bytes
    -> ProductionMuonRuntime::load_registry_verified
    -> self recursion
```

and does so before `ProductionMuonRuntime::load_or_initialize`.

This is a production-entry correctness blocker, not a performance-only defect.

## Registry ownership closure

The registry type now owns file load, JSON decode, and semantic validation:

```rust
impl FirstCandidateEligibilityRegistry {
    pub fn load_verified(
        spec: &ModelSpec,
        registry_path: &Path,
    ) -> Result<Self> {
        let registry_bytes = fs::read(registry_path)
            .with_context(|| format!(
                "FirstCandidateRegistryRead:{}",
                registry_path.display()
            ))?;

        let registry: Self = serde_json::from_slice(&registry_bytes)
            .with_context(|| format!(
                "FirstCandidateRegistryDecode:{}",
                registry_path.display()
            ))?;

        registry
            .validate(spec)
            .with_context(|| format!(
                "FirstCandidateRegistryValidation:{}",
                registry_path.display()
            ))?;

        Ok(registry)
    }
}
```

State ownership is therefore:

```text
FirstCandidateEligibilityRegistry
    -> registry read / decode / validate semantics

ProductionMuonRuntime
    -> verified registry consumer
```

The runtime no longer duplicates registry semantic policy.

## Existing semantic validation preserved

`FirstCandidateEligibilityRegistry::validate(spec)` remains authoritative for the existing contracts, including:

```text
unclassified_element_count == 0
overlap_element_count == 0
runtime_shape_guess_count == 0
silent_muon_expansion_count == 0
silent_adamw_fallback_count == 0
```

as well as schema, patch identity, candidate policy, parameter coverage, canonical inventory/routing digests, registry digest, and tile/momentum coverage checks already present in the parent.

No eligibility rule is changed by this repair.

## Production wrapper repair

The existing public wrapper is retained for compatibility, but it no longer owns validation policy and cannot recurse:

```rust
pub fn load_registry_verified(
    spec: &ModelSpec,
    registry_path: &Path,
) -> Result<FirstCandidateEligibilityRegistry> {
    FirstCandidateEligibilityRegistry::load_verified(spec, registry_path)
}
```

The production module contains zero `Self::load_registry_verified` calls after this patch.

## Momentum sizing adoption

`required_momentum_bytes()` now directly consumes the canonical verified loader:

```text
FirstCandidateEligibilityRegistry::load_verified
    -> muon_eligible_element_count
    -> checked_mul(4)
```

The existing F32 momentum byte formula and overflow guard are preserved.

No unverified registry may be used for RAM36 momentum reservation sizing.

## Runtime initialization adoption

`load_or_initialize()` previously contained an independent registry path:

```text
fs::read(registry_path)
serde_json::from_slice<FirstCandidateEligibilityRegistry>
registry.validate(spec)
```

That path is retired.

It now consumes:

```text
FirstCandidateEligibilityRegistry::load_verified(spec, registry_path)
```

before profile and momentum-state initialization.

The production runtime therefore has no direct FirstCandidate registry file read or direct FirstCandidate registry JSON decode path.

## File validator adoption

`validate_registry_file()` also consumes the canonical loader for registry read/decode/semantic validation.

Its separate model-file digest responsibility is preserved:

```text
model spec file bytes
    -> sha256_bytes
    -> registry.model_spec_digest parity
```

This distinction is intentional:

```text
Registry::load_verified
    = registry file read/decode + validate(spec)

validate_registry_file
    = model-file digest parity in addition to canonical registry load/verify
```

No model-file digest check is silently invented inside the runtime loader, because the runtime API receives `&ModelSpec`, not the original model-spec file bytes.

## Fail-closed behavior

The canonical loader propagates failure for:

```text
registry file read failure
registry JSON decode failure
registry semantic validation failure
```

There is no:

```text
unwrap_or_default registry synthesis
empty-registry synthesis
last-good registry substitution
old-registry fallback
unverified production admission
```

## Scheduler reachability preserved

The production scheduler order remains:

```text
Muon production admission
    -> explicit registry path
    -> required_momentum_bytes
    -> RAM36 momentum reservation
    -> load_or_initialize
    -> materialized momentum-byte verification
    -> production runtime
```

The repair does not reorder RAM36 reservation or runtime initialization semantics.

## Validation hardening

New focused validator:

```text
tools/validate_ash_basetrain_tensorcube_local_muon_first_candidate_registry_canonical_load_verify_ssot_recursion_repair_r1_static.py
38/38 PASS
```

It verifies, among other things:

```text
canonical loader definition count == 1
canonical loader reads exact registry path
canonical loader performs JSON decode
canonical loader invokes validate(spec)
production wrapper delegates canonical loader
production wrapper has no self recursion
required_momentum_bytes adopts canonical loader
load_or_initialize adopts canonical loader
production module has no direct registry read
production module has no direct registry decode
validate_registry_file adopts canonical loader
model-file digest parity remains
scheduler preflight occurs before runtime initialization
repair validator is wired into CF1
```

The existing validators were also strengthened rather than left as shallow callsite-existence checks.

### Parent static results

```text
FirstCandidate registry                       97/97 PASS
Production Muon callsite                      63/63 PASS
TensorCube local Muon optimizer              101/101 PASS
Muon multi-tile batch dispatch                61/61 PASS
Generation-sealed immutable Muon cache        66/66 PASS
Muon immutable cache backend rebind           35/35 PASS
R6 production scheduler                      112/112 PASS
```

## CF1 wiring

The new recursion/SSOT validator is included in:

```text
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

so the repaired contract becomes part of the existing CF1 static validation chain.

## Changed files

Overlay contains exactly six files:

```text
crates/base_train/src/tensorcube_local_muon_first_candidate_registry.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_basetrain_tensorcube_local_muon_first_candidate_registry_canonical_load_verify_ssot_recursion_repair_r1_static.py
tools/validate_tensorcube_local_muon_first_candidate_registry_static.py
tools/validate_tensorcube_local_muon_production_callsite_adoption_r1_static.py
```

Code ZIPs contain no Markdown, `*.sha256`, or Python cache artifacts.

## Evidence status

The bake environment does not contain Cargo/rustc.

```text
STATIC_BAKED_READY
NO_LOCAL_RUST_COMPILE_CLAIM
NO_LOCAL_RUNTIME_EXECUTION_CLAIM
PHYSICAL_CARGO_CHECK_REQUIRED
PHYSICAL_MUON_PRODUCTION_ENTRY_REQUIRED
```

User-local Rust/Cargo execution remains final physical execution SSOT.

## Physical verification targets

The local physical gate should establish at least:

```text
cargo check base_train PASS
production Muon admission reaches required_momentum_bytes
required_momentum_bytes returns exact checked F32 momentum bytes
load_or_initialize is reached after preflight
valid registry initializes runtime
invalid registry fails closed
missing registry fails closed
invalid JSON fails closed
unclassified/overlap/runtime-guess/silent-routing violations fail closed
no stack overflow
no alternate unverified registry path
```

## Non-goals

```text
No Muon optimizer math change
No momentum byte formula change
No momentum state layout change
No RAM36 policy change
No VRAM policy change
No eligibility reclassification
No FirstCandidate schema migration
No registry producer semantic change
No automatic registry repair
No verified-registry scheduler lease/cache yet
```

## Natural follow-up

Once physical Cargo/runtime execution closes this correctness repair, duplicate registry I/O can be optimized separately with:

```text
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-
VERIFIED-FIRST-CANDIDATE-REGISTRY-
SCHEDULER-LEASE-AND-SINGLE-READ-REUSE-R2
```

That follow-up may load the verified registry once in the scheduler and share a verified lease between momentum sizing and runtime initialization. It is intentionally not mixed into this correctness repair.

## Promotion seal

```text
PROMOTE_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_FIRST_CANDIDATE_REGISTRY_CANONICAL_LOAD_VERIFY_SSOT_AND_UNCONDITIONAL_RECURSION_REPAIR_R1

UNCONDITIONAL_SELF_RECURSION_RETIRED
ZERO_PRODUCTION_MUON_REGISTRY_LOADER_SELF_CALL
FIRST_CANDIDATE_ELIGIBILITY_REGISTRY_CANONICAL_LOAD_VERIFIED_AUTHORITY
SINGLE_REGISTRY_READ_DECODE_VALIDATE_IMPLEMENTATION
REGISTRY_VALIDATE_SPEC_SEMANTIC_AUTHORITY
UNCLASSIFIED_ZERO_CONTRACT_PRESERVED
OVERLAP_ZERO_CONTRACT_PRESERVED
RUNTIME_SHAPE_GUESS_ZERO_CONTRACT_PRESERVED
SILENT_MUON_EXPANSION_ZERO_CONTRACT_PRESERVED
SILENT_ADAMW_FALLBACK_ZERO_CONTRACT_PRESERVED
NO_PRODUCTION_SHADOW_VALIDATION
REQUIRED_MOMENTUM_BYTES_CANONICAL_LOADER_ADOPTION
LOAD_OR_INITIALIZE_CANONICAL_LOADER_ADOPTION
FILE_VALIDATOR_CANONICAL_LOADER_ADOPTION
MODEL_FILE_DIGEST_PARITY_PRESERVED
NO_PRODUCTION_DIRECT_REGISTRY_READ
NO_PRODUCTION_DIRECT_REGISTRY_DESERIALIZE
REGISTRY_READ_FAILURE_FAIL_CLOSED
REGISTRY_DECODE_FAILURE_FAIL_CLOSED
REGISTRY_VALIDATION_FAILURE_FAIL_CLOSED
NO_DEFAULT_REGISTRY_SYNTHESIS
NO_OLD_REGISTRY_FALLBACK
MUON_PRODUCTION_SCHEDULER_REACHABILITY_PRESERVED
MOMENTUM_BYTE_PREFLIGHT_CLOSURE
CF1_RECURSION_NEGATIVE_CONTROL
NO_MUON_MATH_MUTATION
NO_REGISTRY_SCHEMA_MUTATION
NO_ELIGIBILITY_RECLASSIFICATION
NO_LOCAL_COMPILE_CLAIM
SEALED
```
