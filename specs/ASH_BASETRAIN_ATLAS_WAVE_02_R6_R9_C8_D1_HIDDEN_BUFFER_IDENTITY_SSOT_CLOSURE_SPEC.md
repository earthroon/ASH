# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C8-D1

## C7 Published Hidden3 Buffer Identity SSOT Closure / C8 Source Completion Binding Repair / Ephemeral Raw-Bridge Seam Rehash Retirement / Fail-Closed C8 Check Preservation Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C8`  
> Observed physical failure: `R6R9C8SourceOutputHiddenBufferMismatch`  
> C6 physical parent: PASS  
> C7 execution parity parent: PASS before C8 binding  
> Runtime transport authority: unchanged  
> C8 source mismatch check: preserved fail-closed

## 1. Observed failure

The C8 physical run reached C7 PASS and then failed before destructive C8 source eviction:

```text
Error: R6R9C8SourceOutputHiddenBufferMismatch
```

Therefore C8 had not crossed its destructive source-extraction boundary and no C8 target payload staging or Layer3 adoption had occurred.

## 2. Root cause

C7's non-publishing candidate route already seals:

```text
candidate_route.evidence.final_hidden_buffer_identity_digest
```

from the candidate Hidden3 tensor's first strict raw bridge.

After candidate/oracle parity, C7 bridges the same candidate tensor a second time for cross-block parity/publication verification. The second bridge may receive a different bridge `seam_id`. C7 then recomputed the persistent Hidden3 pointer `buffer_identity_digest` from that second bridge lease.

Thus the same semantic Hidden3 tensor could produce:

```text
candidate route evidence buffer identity = hash(first bridge seam)
published Hidden3 pointer buffer identity = hash(second bridge seam)
```

C8 correctly compared the source execution route evidence against the published Hidden3 pointer and rejected this split identity.

The mismatch is therefore a C7 publication identity SSOT bug, not a reason to weaken C8 validation.

## 3. Canonical repair

C7 must not re-hash a second raw-bridge lease into a new persistent identity at commit time.

Before:

```rust
let final_hidden_buffer_identity_digest = sha256(&serde_json::to_vec(&json!({
    "shape": candidate_final_lease.shape,
    "seam": candidate_final_lease.active_handle.seam_id,
    "bytes": candidate_final_lease.len_bytes,
    "bufferOffset": candidate_final_lease.buffer_offset,
    "bufferSize": candidate_final_lease.buffer_size,
}))?);
```

After:

```rust
let final_hidden_buffer_identity_digest =
    candidate_route.evidence.final_hidden_buffer_identity_digest.clone();
```

The Hidden3 runtime pointer now inherits the already sealed candidate-route buffer identity.

## 4. Post-commit fail-closed invariant

Immediately after `commit_next_layer`, C7 requires:

```rust
ensure!(
    committed_hidden3.buffer_identity_digest
        == candidate_route.evidence.final_hidden_buffer_identity_digest,
    "R6R9C7PublishedHiddenBufferIdentityMismatch"
);
```

No silent reconciliation or fallback is allowed.

## 5. C8 validation is preserved

C8 retains:

```rust
ensure!(
    route.final_hidden_buffer_identity_digest == hidden_pointer.buffer_identity_digest,
    "R6R9C8SourceOutputHiddenBufferMismatch"
);
```

The gate is not removed, weakened, converted to warning, or replaced with pointer-digest-only validation.

## 6. Ownership meaning

The persistent `LayerHiddenAuthorityPointer::buffer_identity_digest` is an execution/publication lineage identity. It must remain stable across additional observational raw-bridge views of the same committed tensor.

A bridge-local `seam_id` is permitted to identify a specific bridge lease, but a second observational bridge must not silently redefine the already sealed persistent hidden-buffer identity.

## 7. Scope

Semantic changes are limited to:

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c7_layer2_wave_execution_parity.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c8_canonical_decoder_weight_wave_rebind.rs
```

The C8 file change only bumps the build revision so the closure is evidence-visible.

No changes to:

```text
C4 planning
C5 checkpoint decode/staging
C6 destructive rebind
residency state machine
hidden slot implementation
legacy loader retirement policy
same-operation fallback policy
WGSL
Headwise numerical route
Hidden3 parity policy
```

## 8. Required rerun behavior

The same canonical gate is rerun.

Expected ordering:

```text
C6 PASS
C7 PASS
C8 source completion binding PASS
C8 source Layer2 destructive extraction
VacantForRebind
C5 Layer3 wave staging
Layer3 atomic adopt
C8 PASS
```

C7 must still report:

```text
mismatch=0
nonfinite=0
payload_readback=0
hidden3_commit=1
hidden_layer=3
hidden_generation=3
publication_mismatch=0
```

C8 must then continue beyond the former buffer mismatch gate.

## 9. Build revisions

```text
C7 build revision = r6-r9-c7-layer2-wave-built-decoder-execution-parity-v1-c8-d1-hidden-buffer-identity-ssot
C8 build revision = r6-r9-c8-canonical-decoder-weight-wave-loader-adoption-v1-d1-hidden-buffer-identity-ssot
```

Patch IDs and PASS token meanings remain the existing C7 and C8 contracts.

## 10. Physical command

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args"
```

## 11. Admission

C8-D1 is statically admitted only when:

```text
C7 commit-time second-bridge identity rehash = 0
C7 persistent Hidden3 identity = candidate route evidence identity
C7 post-commit identity equality guard = present
C8 source route/pointer identity equality guard = present
C8 guard weakening = 0
legacy fallback introduction = 0
WGSL semantic change = 0
```

Physical C8 PASS remains pending until the user reruns Cargo/WGPU.

## Architecture seal

> A published hidden-buffer identity must be inherited from the execution route that produced the tensor, not silently regenerated from a later observational raw-bridge lease. C8-D1 makes C7 route evidence and the Hidden3 runtime pointer share one persistent buffer-identity SSOT while preserving C8's fail-closed source-completion validation unchanged.
